"""
Resource for the Report 2.0.
"""

from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Tuple, Union

import altair as alt
from pandas import DataFrame

from aidkit_client._endpoints.models import (
    ModelNormStats,
    Report2Request,
    Report2Response,
)
from aidkit_client._endpoints.report2 import Report2API
from aidkit_client.aidkit_api import HTTPService
from aidkit_client.configuration import get_api_client
from aidkit_client.resources.dataset import Dataset, Subset
from aidkit_client.resources.ml_model import MLModelVersion


@dataclass
class DataCentricView:
    """
    Data-centric view of the report.
    """

    plot: alt.LayerChart
    stats: DataFrame


class Report2:
    """
    A report which compares model versions.
    """

    def __init__(self, api_service: HTTPService, report2_response: Report2Response) -> None:
        """
        Create a new instance from the server response.

        :param api_service: Service instance to use for communicating with the
            server.
        :param report2_response: Server response describing the report
            to be created.
        """
        self._data = report2_response
        self._api_service = api_service

    @classmethod
    async def get(
        cls,
        model: str,
        model_versions: List[Union[str, MLModelVersion]],
        dataset: Union[str, Dataset],
        subset: Union[str, Subset],
        metrics: List[str],
    ) -> "Report2":
        """
        Get the adversarial report to compare the given model versions.

        :param model: Name of the uploaded model of which versions are compared in the report.
        :param model_versions: Model versions to compare in the report.
        :param dataset: Dataset to use for the comparison.
        :param subset: Subset whose observations are used for the comparison.
        :param metrics: Distance metrics to consider in the comparison.
        :return: Instance of the report.
        """
        model_version_names = [
            model_version.name if isinstance(model_version, MLModelVersion) else model_version
            for model_version in model_versions
        ]
        dataset_name = dataset.name if isinstance(dataset, Dataset) else dataset
        subset_name = subset.name if isinstance(subset, Subset) else subset
        api_service = get_api_client()
        return Report2(
            api_service=api_service,
            report2_response=await Report2API(api_service).get(
                request=Report2Request(
                    model=model,
                    model_versions=model_version_names,
                    dataset=dataset_name,
                    subset=subset_name,
                    metrics=metrics,
                )
            ),
        )

    @property
    def data(self) -> DataFrame:
        """
        Get the data of the report.

        :return: DataFrame containing sample data for the report. The returned DataFrame has one row
            per combination of

            * Configured Adversarial Attack: All those adversarial attacks which were run on all
                compared model versions and evaluated with all considered norms are included.
            * Observation: Observation: All observations in the subset the report is requested for.
            * Model Version: All model versions the report is requested for.
            * Metric Name: All norms the report is requested for.

            The returned DataFrame has the following columns:

            * ``successful``: Boolean; Whether the generated perturbation changed the model's
                prediction.
            * ``distance_metric_value``: Float; Distance between the perturbation and the original
                observation.
            * ``method_name``: Categorical; Name of the method used to create the perturbation.
            * ``param_string`` Categorical; Parameters for the method used to create the
                perturbation.
            * ``observation_id``: Integer; ID of the observation an adversarial example was created
                for.
            * ``artifact_id``: Integer; ID of the generated perturbation.
            * ``distance_metric_name``: Categorical; Name of the metric used to measure
                ``distance_metric_value``.
                One of the names in ``metric_names``.
            * ```model_version``: Categorical; Name of the model version the adversarial example was
                created for.
                One of the names in ``model_version_names``.
        """
        return DataFrame(self._data.data).astype(
            {
                "model_version": "category",
                "distance_metric_name": "category",
                "method_name": "category",
                "param_string": "category",
            }
        )

    def _fill_plot_with_data(self, plot: alt.LayerChart) -> alt.LayerChart:
        plot_copy = plot.copy(deep=True)
        plot_copy.data = self.data
        return plot_copy

    @staticmethod
    def _get_stats(stats_dict: Dict[str, Dict[str, ModelNormStats]]) -> DataFrame:
        stats_dict_in_pandas_form: Dict[Tuple[str, str], Dict[str, float]] = defaultdict(dict)
        for model_version, model_stats in stats_dict.items():
            for norm_name, stats in model_stats.items():
                for stat_name, stat_value in stats.dict().items():
                    stats_dict_in_pandas_form[(norm_name, stat_name)][model_version] = stat_value
        return DataFrame(data=stats_dict_in_pandas_form)

    @property
    def data_centric_view(self) -> DataCentricView:
        """
        Get the data centric view of the report.

        :return: Data centric view containing a plot and summary statistics.
        """
        return DataCentricView(
            plot=self._fill_plot_with_data(
                alt.LayerChart.from_dict(self._data.plot_recipes.data_centric_csr)
            ),
            stats=self._get_stats(self._data.stats.data_centric_stats),
        )

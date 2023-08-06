from aidkit_client._endpoints.constants import Constants
from aidkit_client._endpoints.models import Report2Request, Report2Response
from aidkit_client.aidkit_api import HTTPService


class Report2API:
    api: HTTPService

    def __init__(self, api: HTTPService):
        self.api = api

    async def get(self, request: Report2Request) -> Report2Response:
        result = await self.api.post_json(
            path=f"{Constants.REPORT2_PATH}",
            parameters=None,
            body=request.dict(),
        )
        return Report2Response(
            **result.body_dict_or_error(f"Error fetching Report for model '{request.model}'.")
        )

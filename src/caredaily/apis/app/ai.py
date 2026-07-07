# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "requests",
# ]
# ///

from typing import Dict

from ...models import (
    Result,
)
from ..api import API


class AI(API):
    """
    AI API for user-facing OpenAI requests proxied through the CareDaily cloud.

    Note: the v61 API spec documents these endpoints under /clouse/json/...,
    which is assumed to be a typo for /cloud/json/....

    Reference:
        https://app.peoplepowerco.com/cloud/apidocs/cloud.html
    """
    def send_openai_request(
        self,
        location_id: int,
        openai_path: int,
        request_data: Dict,
        openai_organization: str = None,
    ) -> Result:
        """
        Send a request to OpenAI.

        Args:
            location_id: Location ID (required)
            openai_path: OpenAI API path identifier (required)
            request_data: OpenAI request data containing the 'answer' object with
                          model, input, messages and temperature
            openai_organization: An organization which will be used (charged) for
                                 an OpenAI API request

        Returns:
            Result: API response with the OpenAI answer

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/AI/operation/Send%20a%20request%20to%20OpenAI
        """
        params = {
            "locationId": location_id,
            "openAiPath": openai_path,
            "openAiOrganization": openai_organization,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.post(
            "/espapi/cloud/json/openai",
            ep_params=params,
            ep_json=request_data,
        )
        return result

    def get_openai_token(
        self,
        location_id: int,
        expiry: int,
    ) -> Result:
        """
        Get OpenAI client token.

        Args:
            location_id: Location ID (required)
            expiry: Token expiry (required)

        Returns:
            Result: API response with the OpenAI client token

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/AI/operation/Get%20OpenAI%20client%20token
        """
        params = {
            "locationId": location_id,
            "expiry": expiry,
        }
        result: Result = self.adapter.get(
            "/espapi/cloud/json/openaiToken",
            ep_params=params,
        )
        return result

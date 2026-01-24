# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "requests",
# ]
# ///
import json
from typing import Dict, List

from ...models import (
    APIKeyType,
)

from ..api import API

class Execution(API):
    """
    Provides methods for listening to device execution analytics and events via the DeviceIO API.

    Reference:
        https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bots-Execution
    """
    def listen(
            self,
            app_instance_id: int,
            timeout: int = None,
            clean_time_ms: int = None,
            clean: bool = None,
    ):
        """
        Listen for device execution analytics/events for a given app instance.

        Args:
            app_instance_id: The ID of the app instance to listen for events on.
            timeout: Optional timeout in seconds for the listen request.
            clean_time_ms: Optional time in milliseconds to clean up old events.
            clean: Optional flag to clean up events after listening.

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bots-Execution/operation/Local%20Execution%20on%20a%20Computer
        """
        params = {
            "appInstanceId": app_instance_id,
            "timeout": timeout,
            "cleanTime": clean_time_ms,
            "clean": clean,
        }
        params = {k: v for k, v in params.items() if v is not None}
        key = self.adapter._headers.get("ADMIN_KEY") or self.adapter._headers.get("API_KEY")
        return self.adapter.get(
            "/deviceio/analytic",
            ep_params=params,
            ep_headers=self.adapter._get_headers(
                api_key=key,
                key_type=APIKeyType.USER,
            ),
        )
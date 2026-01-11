# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "requests",
# ]
# ///

from ..api import API

from ...models import (
    APIKeyType,
    Result,
)


class System(API):
    def get_system_status(
        self,
        organization_id: int = None,
    ) -> Result:
        """
        Get detailed statistics about different system components for the last 24 hours.

        The response contains 3 major sections:
        - pulses: General statuses of running modules (deviceio, device streaming, wsapi, etc.)
        - min5Statuses: System statistics for last 60 minutes (5-minute intervals)
        - hourStatuses: System statistics for last 24 hours (60-minute intervals)

        Args:
            organization_id: Filter response by specific organization

        Returns:
            Result: API response with system status data

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Status/operation/Get%20System%20Status
        """
        params = {
            "organizationId": organization_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/espapi/admin/json/status",
            ep_params=params,
            ep_headers=self.adapter._get_headers(
                {"ADMIN_KEY": self.adapter._headers.get("ADMIN_KEY")}
            ),
        )
        return result

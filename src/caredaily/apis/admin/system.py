# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "requests",
# ]
# ///

from ...models import (
    APIKeyType,
    Result,
)
from ..api import API


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
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.ADMIN,
            ),
        )
        return result

    def get_time_states(
        self,
        organization_id: int,
        start_date: str,
        end_date: str,
        location_id: int = None,
        priority_category: int = None,
        name: str = None,
    ) -> Result:
        """
        Get Location Time-series States.

        Returns time-series state records for locations within an organization,
        filtered by date range and optional location, priority category, or state name.

        Args:
            organization_id: Organization ID (required)
            start_date: Return states with dates greater than this value (required)
            end_date: Return states with dates less than or equal to this value (required)
            location_id: Location IDs filter, multiple values supported
            priority_category: Filter by location priority category, multiple values supported
            name: State name(s), multiple values supported

        Returns:
            Result: API response with time-series states data

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Users-and-Locations/operation/Get%20Location%20Time-series%20States
        """
        params = {
            "organizationId": organization_id,
            "locationId": location_id,
            "priorityCategory": priority_category,
            "startDate": start_date,
            "endDate": end_date,
            "name": name,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/espapi/admin/json/timeStates",
            ep_params=params,
            ep_headers=self.adapter._get_headers(
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.ADMIN,
            ),
        )
        return result

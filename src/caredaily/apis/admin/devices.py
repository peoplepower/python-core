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


class Devices(API):
    """
    Devices API for retrieving and filtering organization device instances.

    This class provides methods to list and search devices linked to users and locations within an organization.
    Supports filtering by user, location, device type, tags, update date, and device parameters.

    Reference:
        https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Users-and-Locations
    """
    def get_organization_devices(
        self,
        organization_id: int = None,
        user_id: int = None,
        location_id: int = None,
        device_id: str = None,
        device_type: int = None,
        search_by: str = None,
        search_tag: str = None,
        less_update_date: str = None,
        more_update_date: str = None,
        param_name: str = None,
        param_value: str = None,
        limit: int = None,
        get_tags: bool = None,
    ) -> Result:
        """
        Retrieve device instances linked to users and/or locations inside the organization.

        Args:
            organization_id: Organization ID
            user_id: Filter by user ID
            location_id: Filter by location ID
            device_id: Filter by device ID
            device_type: Filter by device types (multiple values supported)
            search_by: Search by device ID or description
            search_tag: Search by tag
            less_update_date: Request devices where last update date is less than this
            more_update_date: Request devices where last update date is more than this
            param_name: Request devices which sent this parameter to the cloud
            param_value: Requested parameter value
            limit: Limit the response size by this number
            get_tags: Return device tags

        Returns:
            Result: API response with devices data

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Users-and-Locations/operation/Get%20Devices
        """
        params = {
            "organizationId": organization_id,
            "userId": user_id,
            "locationId": location_id,
            "deviceId": device_id,
            "deviceType": device_type,
            "searchBy": search_by,
            "searchTag": search_tag,
            "lessUpdateDate": less_update_date,
            "moreUpdateDate": more_update_date,
            "paramName": param_name,
            "paramValue": param_value,
            "limit": limit,
            "getTags": get_tags,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/espapi/admin/json/devices",
            ep_params=params,
            ep_headers=self.adapter._get_headers(
                {"API_KEY": self.adapter._headers.get("ADMIN_KEY")}
            ),
        )
        return result

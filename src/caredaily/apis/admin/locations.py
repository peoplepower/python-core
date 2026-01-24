# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "requests",
# ]
# ///

from typing import Dict, List

from ..api import API

from ...models import (
    APIKeyType,
    Result,
)


class Locations(API):
    """
    Locations API for managing organization locations and related operations.

    This class provides methods to list, create, update, delete, and batch manage locations within an organization.
    It supports searching, filtering, and handling location metadata, tags, and user roles.

    Reference:
        https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Users-and-Locations
    """
    def get_organization_locations(
        self,
        organization_id: int = None,
        location_id: int = None,
        sub_type: int = None,
        external_id: str = None,
        search_by: str = None,
        event: str = None,
        location_type: int = None,
        exclude_type: int = None,
        search_tag: str = None,
        search_device_tag: str = None,
        device_type: int = None,
        service_plan_id: int = None,
        state_id: int = None,
        country_id: int = None,
        priority_category: int = None,
        external_user_id: str = None,
        user_role: int = None,
        state_name: str = None,
        get_tags: bool = None,
        limit: int = None,
    ) -> Result:
        """
        List and search user and device locations within an organization.

        Location fields are described in user account APIs documentation.

        Args:
            organization_id: Organization ID
            location_id: Location IDs to retrieve (multiple values supported)
            sub_type: Filter locations by sub-type
            external_id: Search locations by external IDs (multiple values supported)
            search_by: Filter by location name and address (use * for wildcard)
            event: Filter by part of location event name (use * for wildcard)
            location_type: Filter by location type (multiple values supported)
            exclude_type: Excluding filter by location type (multiple values supported)
            search_tag: Search by location tags (multiple values supported)
            search_device_tag: Search by device tags (multiple values supported)
            device_type: Filter by devices of these types (multiple values supported)
            service_plan_id: Filter by service plan ID
            state_id: Filter by location address state ID
            country_id: Filter by location address country ID
            priority_category: Filter by location priority category (multiple values supported)
            external_user_id: Search by external user ID
            user_role: Return location users with this role
            state_name: Return location state variable with this name
            get_tags: Return location tags
            limit: Limit the response size

        Returns:
            Result: API response with locations data

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Users-and-Locations/operation/Get%20Locations
        """
        params = {
            "organizationId": organization_id,
            "locationId": location_id,
            "subType": sub_type,
            "externalId": external_id,
            "searchBy": search_by,
            "event": event,
            "locationType": location_type,
            "excludeType": exclude_type,
            "searchTag": search_tag,
            "searchDeviceTag": search_device_tag,
            "deviceType": device_type,
            "servicePlanId": service_plan_id,
            "stateId": state_id,
            "countryId": country_id,
            "priorityCategory": priority_category,
            "externalUserId": external_user_id,
            "userRole": user_role,
            "stateName": state_name,
            "getTags": get_tags,
            "limit": limit,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/espapi/admin/json/locations",
            ep_params=params,
            ep_headers=self.adapter._get_headers(
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            ),
        )
        return result

    def create_organization_location(
        self,
        organization_id: int,
        location_data: Dict,
        parent_id: int = None,
        user_id: int = None,
    ) -> Result:
        """
        Create a new location in an organization.

        Args:
            organization_id: Organization ID
            location_data: Location data as JSON object with 'location' key
            parent_id: Parent location ID to assign the new location as a sub-location
            user_id: User ID with admin access to this location

        Returns:
            Result: API response confirming creation

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Users-and-Locations/operation/Create%20Location
        """
        params = {
            "parentId": parent_id,
            "userId": user_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.post(
            f"/espapi/admin/json/organizations/{organization_id}/locations",
            ep_params=params,
            ep_json=location_data if location_data else None,
            ep_headers=self.adapter._get_headers(
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            ),
        )
        return result

    def update_organization_location(
        self,
        organization_id: int,
        location_id: int,
        location_data: Dict,
    ) -> Result:
        """
        Update a location in an organization.

        Args:
            organization_id: Organization ID
            location_id: Location ID to update
            location_data: Location data as JSON object with 'location' key

        Returns:
            Result: API response confirming update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Users-and-Locations/operation/Update%20Location
        """
        params = {
            "locationId": location_id,
        }
        result: Result = self.adapter.put(
            f"/espapi/admin/json/organizations/{organization_id}/locations",
            ep_params=params,
            ep_json=location_data if location_data else None,
            ep_headers=self.adapter._get_headers(
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            ),
        )
        return result

    def delete_organization_location(
        self,
        organization_id: int,
        location_id: int,
    ) -> Result:
        """
        Delete a location from an organization.

        Args:
            organization_id: Organization ID
            location_id: Location ID to delete

        Returns:
            Result: API response confirming deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Users-and-Locations/operation/Delete%20Location
        """
        params = {
            "locationId": location_id,
        }
        result: Result = self.adapter.delete(
            f"/espapi/admin/json/organizations/{organization_id}/locations",
            ep_params=params,
            ep_headers=self.adapter._get_headers(
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            ),
        )
        return result

    def add_update_delete_organization_locations(
        self,
        organization_id: int,
        location_ids: List[int],
        notes: str = None,
        delete: bool = None,
    ) -> Result:
        """
        Batch API to manage locations in an organization.

        Locations will be added or moved to the organization automatically if they are not there.
        To remove locations from the organization, set the delete field to True.

        Note: This API does not guarantee that the request will be performed for all locations.
        The error code may not be returned in this case.

        Args:
            organization_id: Organization ID
            location_ids: List of location IDs to add, update, or delete
            notes: Notes text to add/update
            delete: Set to True to remove locations from the organization

        Returns:
            Result: API response confirming operation

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Users-and-Locations/operation/Add%20or%20Update%20or%20Remove%20locations
        """
        data = {
            "locationIds": location_ids,
            "notes": notes,
            "delete": delete,
        }
        data = {k: v for k, v in data.items() if v is not None}
        result: Result = self.adapter.put(
            f"/espapi/admin/json/organizations/{organization_id}/locationStatus",
            ep_json=data if data else None,
            ep_headers=self.adapter._get_headers(
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            ),
        )
        return result

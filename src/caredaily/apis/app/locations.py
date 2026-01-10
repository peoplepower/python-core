# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "requests",
# ]
# ///

import json
from typing import Dict, List, Optional

from ...models import (
    APIKeyType,
    Cloud,
    MQTT,
    Result,
    Server,
    ServerType,
    SignatureAlgorithm,
)
from ..api import API

class Locations(API):
    """
    Locations API for managing user locations and location-related operations.

    This class provides comprehensive methods for location operations including
    creation, retrieval, updates, deletion, location users, spaces, events, and narratives.

    Reference:
        https://app.peoplepowerco.com/cloud/apidocs/cloud.html#locations
    """

    def create_location(
        self,
        data: Dict,
    ):
        """
        Create a new location for the current user.

        Args:
            data: Dictionary containing location data including:
                - name: Location name (required)
                - type: Location type (residential, commercial, etc.)
                - address: Location address information
                - timezone: Timezone for the location
                - Additional location metadata

        Returns:
            Result: API response with created location ID and details

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#create-location
        """
        result: Result = self.adapter.post(
            "/espapi/cloud/json/location",
            ep_json=json.dumps(data),
        )
        return result

    def update_location(
        self,
        location_id: int,
        data: Dict,
        analytic_key: str = None,
    ):
        """
        Update an existing location.

        Args:
            location_id: Location ID to update
            data: Dictionary containing location data to update
            analytic_key: Optional analytic API key for bot access

        Returns:
            Result: API response confirming update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#update-location
        """
        headers = None
        if analytic_key:
            headers = self.adapter._get_headers(analytic_key, APIKeyType.ANALYTIC)
        result: Result = self.adapter.put(
            f"/espapi/cloud/json/location/{location_id}",
            ep_json=json.dumps(data),
            ep_headers=headers,
        )
        return result

    def delete_location(
        self,
        location_id: int,
    ):
        """
        Delete a location.

        This will permanently delete the location and all associated data.

        Args:
            location_id: Location ID to delete

        Returns:
            Result: API response confirming deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#delete-location
        """
        result: Result = self.adapter.delete(
            f"/espapi/cloud/json/location/{location_id}"
        )
        return result

    def put_location_to_organization(
        self,
        location_id: int,
        organization_id: int,
    ):
        """
        Associate a location with an organization.

        Args:
            location_id: Location ID to associate
            organization_id: Organization ID to associate with

        Returns:
            Result: API response confirming association

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#put-location-to-organization
        """
        params = {
            "organizationId": organization_id,
        }
        result: Result = self.adapter.put(
            f"/espapi/cloud/json/location/{location_id}/organization", ep_params=params
        )
        return result

    def update_location_organization(
        self,
        location_id: int,
        domain_name: str,
    ) -> Result:
        """
        Update Location Organization.

        Update the organization association for a location by domain name.

        Args:
            location_id: Location ID (required)
            domain_name: Organization domain name (required)

        Returns:
            Result: API response confirming update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Locations/operation/Update%20Location%20Organization
        """
        result: Result = self.adapter.put(
            f"/espapi/cloud/json/location/{location_id}/organization/{domain_name}",
        )
        return result

    def post_location_event(
        self,
        location_id: int,
        event: Dict,
    ):
        """
        Post an event to a location.

        Args:
            location_id: Location ID to post event to
            event: Dictionary containing event data including:
                - eventType: Type of event
                - timestamp: Event timestamp
                - Additional event metadata

        Returns:
            Result: API response confirming event creation

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#post-location-event
        """
        result: Result = self.adapter.post(
            f"/espapi/cloud/json/location/{location_id}/events",
            ep_json=json.dumps(event),
        )
        return result

    def change_location_scene(
        self,
        location_id: int,
        event_name: str,
        event_data: Optional[Dict] = None,
    ) -> Result:
        """
        Change the Scene at a Location.

        By changing the scene at a location, you may cause AI logic to execute such as
        "When I am home do something" or "When I am going to sleep turn off the TV".

        Args:
            location_id: The Location ID for which to trigger an event (required)
            event_name: Developer-defined name of the scene (e.g., 'HOME', 'AWAY', 'SLEEP', 'VACATION', 'FOOSBALL') (required)
            event_data: Optional event data as JSON object

        Returns:
            Result: API response confirming scene change

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Locations/operation/Change%20the%20Scene%20at%20a%20Location
        """
        result: Result = self.adapter.post(
            f"/espapi/cloud/json/location/{location_id}/event/{event_name}",
            ep_json=event_data,
        )
        return result

    def get_location_events_history(
        self,
        location_id: int,
        start_date_ms: int = None,
        end_date_ms: int = None,
    ):
        """
        Get location events history.

        Args:
            location_id: Location ID to get events for
            start_date_ms: Start date in milliseconds since epoch
            end_date_ms: End date in milliseconds since epoch

        Returns:
            Result: API response containing list of location events

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#get-location-events-history
        """
        params = {
            "startDate": start_date_ms,
            "endDate": end_date_ms,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            f"/espapi/cloud/json/location/{location_id}/events",
            ep_params=params,
        )
        return result

    def get_location_priorities_history(
        self,
        location_id: int,
        start_date_ms: int = None,
        end_date_ms: int = None,
    ):
        """
        Get location priorities history.

        Args:
            location_id: Location ID to get priorities for
            start_date_ms: Start date in milliseconds since epoch
            end_date_ms: End date in milliseconds since epoch

        Returns:
            Result: API response containing location priorities history

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#get-location-priorities-history
        """
        params = {
            "startDate": start_date_ms,
            "endDate": end_date_ms,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            f"/espapi/cloud/json/location/{location_id}/priorities",
            ep_params=params,
        )
        return result

    def get_countries(
        self,
        state_id: int = None,
    ):
        """
        Get list of available countries and their states.

        Args:
            state_id: Optional state ID to get specific state information

        Returns:
            Result: API response containing list of countries and states

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#get-countries
        """
        params = {
            "stateId": state_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/espapi/cloud/json/countries", ep_params=params
        )
        return result

    def get_location_users(
        self,
        location_id: int,
    ):
        """
        Get list of users with access to a location.

        Args:
            location_id: Location ID to get users for

        Returns:
            Result: API response containing list of users with their roles and permissions

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#get-location-users
        """
        result: Result = self.adapter.get(
            f"/espapi/cloud/json/location/{location_id}/users"
        )
        return result

    def add_location_users(
        self,
        location_id: int,
        users: List[Dict],
    ):
        """
        Add users to a location.

        Args:
            location_id: Location ID to add users to
            users: List of user dictionaries containing:
                - userId: User ID to add
                - locationAccess: Access level (owner, admin, user, etc.)
                - temporary: Whether access is temporary

        Returns:
            Result: API response confirming user additions

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#add-location-users
        """
        data = {"users": users}
        result: Result = self.adapter.post(
            f"/espapi/cloud/json/location/{location_id}/users",
            ep_json=json.dumps(data),
        )
        return result

    def update_location_user(
        self,
        location_id: int,
        user_id: int,
        location_access: int = None,
        temporary: bool = None,
    ):
        """
        Update a user's access to a location.

        Args:
            location_id: Location ID to update user access for
            user_id: User ID to update
            location_access: New access level
            temporary: Whether access is temporary

        Returns:
            Result: API response confirming update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#update-location-user
        """
        params = {
            "locationAccess": location_access,
            "temporary": temporary,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.put(
            f"/espapi/cloud/json/location/{location_id}/users/{user_id}",
            ep_params=params,
        )
        return result

    def delete_location_user(
        self,
        location_id: int,
        user_id: int,
    ):
        """
        Remove a user's access to a location.

        Args:
            location_id: Location ID to remove user from
            user_id: User ID to remove

        Returns:
            Result: API response confirming removal

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#delete-location-user
        """
        result: Result = self.adapter.delete(
            f"/espapi/cloud/json/location/{location_id}/users/{user_id}"
        )
        return result

    def add_sub_location(
        self,
        location_id: int,
        sub_location_id: int,
    ):
        """
        Add a sub-location to a parent location.

        Args:
            location_id: Parent location ID
            sub_location_id: Sub-location ID to add

        Returns:
            Result: API response confirming addition

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#add-sub-location
        """
        params = {
            "subLocationId": sub_location_id,
        }
        result: Result = self.adapter.post(
            f"/espapi/cloud/json/location/{location_id}/subLocations",
            ep_params=params,
        )
        return result

    def delete_sub_location(
        self,
        location_id: int,
        sub_location_id: int,
    ):
        """
        Remove a sub-location from a parent location.

        Args:
            location_id: Parent location ID
            sub_location_id: Sub-location ID to remove

        Returns:
            Result: API response confirming removal

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#delete-sub-location
        """
        params = {
            "subLocationId": sub_location_id,
        }
        result: Result = self.adapter.delete(
            f"/espapi/cloud/json/location/{location_id}/subLocations",
            ep_params=params,
        )
        return result

    def add_sub_location_v2(
        self,
        location_id: int,
        sub_location_id: int,
        start_date: Optional[str] = None,
    ) -> Result:
        """
        Add Sub-Location.

        An administrator of a location can assign a sub-location to this location.
        A sub-location must have `subType > 0`.

        Args:
            location_id: Location ID (required)
            sub_location_id: Sub-Location ID (required)
            start_date: Assignment start date

        Returns:
            Result: API response confirming addition

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Locations/operation/Add%20Sub-Location
        """
        params = {
            "subLocationId": sub_location_id,
        }
        if start_date is not None:
            params["startDate"] = start_date
        result: Result = self.adapter.put(
            f"/espapi/cloud/json/location/{location_id}/subs",
            ep_params=params,
        )
        return result

    def delete_sub_location_v2(
        self,
        location_id: int,
        sub_location_id: int,
    ) -> Result:
        """
        Delete Sub-Location.

        Remove a sub-location from a parent location.

        Args:
            location_id: Location ID (required)
            sub_location_id: Sub-Location ID (required)

        Returns:
            Result: API response confirming deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Locations/operation/Delete%20Sub-Location
        """
        params = {
            "subLocationId": sub_location_id,
        }
        result: Result = self.adapter.delete(
            f"/espapi/cloud/json/location/{location_id}/subs",
            ep_params=params,
        )
        return result

    def update_location_users(
        self,
        location_id: int,
        users_data: Dict,
    ) -> Result:
        """
        Update Location Users.

        Update users' access to a location.

        Args:
            location_id: Location ID (required)
            users_data: Users data as JSON object with 'users' key

        Returns:
            Result: API response confirming update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Locations/operation/Update%20Location%20Users
        """
        result: Result = self.adapter.put(
            f"/espapi/cloud/json/location/{location_id}/users",
            ep_json=users_data,
        )
        return result

    def delete_location_users(
        self,
        location_id: int,
        user_id: int,
    ) -> Result:
        """
        Delete Location Users.

        Remove a user's access to a location.

        Args:
            location_id: Location ID (required)
            user_id: User ID (required)

        Returns:
            Result: API response confirming deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Locations/operation/Delete%20Location%20Users
        """
        params = {
            "userId": user_id,
        }
        result: Result = self.adapter.delete(
            f"/espapi/cloud/json/location/{location_id}/users",
            ep_params=params,
        )
        return result

    def get_location_spaces(
        self,
        location_id: int,
    ):
        """
        Get list of spaces for a location.

        Args:
            location_id: Location ID to get spaces for

        Returns:
            Result: API response containing list of spaces with their details

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#get-location-spaces
        """
        result: Result = self.adapter.get(
            f"/espapi/cloud/json/location/{location_id}/spaces"
        )
        return result

    def create_location_space(
        self,
        location_id: int,
        space: Dict,
    ) -> Result:
        """
        Create Location Space.

        Create a new space for a location.

        Args:
            location_id: Location ID (required)
            space: Space data as JSON object with 'space' key

        Returns:
            Result: API response with created space ID

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Locations/operation/Create%20Location%20Space
        """
        result: Result = self.adapter.post(
            f"/espapi/cloud/json/location/{location_id}/spaces",
            ep_json=space,
        )
        return result

    def delete_location_space(
        self,
        location_id: int,
        space_id: int,
    ):
        """
        Delete a location space.

        Args:
            location_id: Location ID containing the space
            space_id: Space ID to delete

        Returns:
            Result: API response confirming deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#delete-location-space
        """
        params = {
            "spaceId": space_id,
        }
        result: Result = self.adapter.delete(
            f"/espapi/cloud/json/location/{location_id}/spaces",
            ep_params=params,
        )
        return result

    def get_narratives(
        self,
        location_id: int,
        row_count: int,
        narrative_id: int = None,
        narrative_time: int = None,
        narrative_type: int = None,
        scope: int = None,
        priority: int = None,
        to_priority: int = None,
        status: int = None,
        event_type: str = None,
        search_by: str = None,
        start_date_ms: int = None,
        end_date_ms: int = None,
        page_marker: str = None,
        analytic_key: str = None,
    ):
        """
        Get narratives for a location.

        Args:
            location_id: Location ID to get narratives for
            row_count: Maximum number of narratives to return
            narrative_id: Optional narrative ID filter
            narrative_time: Optional narrative time filter
            narrative_type: Optional narrative type filter
            scope: Narrative scope (user, location, organization)
            priority: Minimum priority level filter
            to_priority: Maximum priority level filter
            status: Narrative status filter
            event_type: Event type filter
            search_by: Search text filter
            start_date_ms: Start date in milliseconds since epoch
            end_date_ms: End date in milliseconds since epoch
            page_marker: Page marker for pagination
            analytic_key: Optional analytic API key for bot access

        Returns:
            Result: API response containing list of narratives

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#get-narratives
        """
        params = {
            "rowCount": row_count,
            "narrativeId": narrative_id,
            "narrativeTime": narrative_time,
            "narrativeType": narrative_type,
            "scope": scope,
            "priority": priority,
            "toPriority": to_priority,
            "status": status,
            "eventType": event_type,
            "searchBy": search_by,
            "startDate": start_date_ms,
            "endDate": end_date_ms,
            "pageMarker": page_marker,
        }
        params = {k: v for k, v in params.items() if v is not None}
        headers = None
        if analytic_key:
            headers = self.adapter._get_headers(analytic_key, APIKeyType.ANALYTIC)
        result: Result = self.adapter.get(
            f"/espapi/cloud/json/locations/{location_id}/narratives",
            ep_params=params,
            ep_headers=headers,
        )
        return result

    def put_narrative(
        self,
        location_id: int,
        scope: int,
        narrative: Dict,
        publish: bool = None,
        narrative_id: int = None,
        narrative_time_ms: int = None,
        analytic_key: str = None,
    ):
        """
        Create or update a narrative for a location.

        Args:
            location_id: Location ID to create/update narrative for
            scope: Narrative scope (user, location, organization)
            narrative: Dictionary containing narrative data
            publish: Whether to publish the narrative
            narrative_id: Optional narrative ID to update existing narrative
            narrative_time_ms: Narrative timestamp in milliseconds since epoch
            analytic_key: Optional analytic API key for bot access

        Returns:
            Result: API response with narrative creation/update confirmation

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#put-narrative
        """
        params = {
            "scope": scope,
            "narrativeId": narrative_id,
            "narrativeTime": narrative_time_ms,
            "publish": publish,
        }
        params = {k: v for k, v in params.items() if v is not None}
        headers = None
        if analytic_key:
            headers = self.adapter._get_headers(analytic_key, APIKeyType.ANALYTIC)
        result: Result = self.adapter.put(
            f"/espapi/cloud/json/locations/{location_id}/narratives",
            ep_json=json.dumps(narrative),
            ep_params=params,
            ep_headers=headers,
        )
        return result

    def delete_a_narrative(
        self,
        location_id: int,
        scope: int,
        narrative_id: int,
        narrative_time_ms: int,
        publish: bool = None,
        event_type: str = None,
        analytic_key: str = None,
    ):
        """
        Delete a narrative from a location.

        Args:
            location_id: Location ID containing the narrative
            scope: Narrative scope (user, location, organization)
            narrative_id: Narrative ID to delete
            narrative_time_ms: Narrative timestamp in milliseconds since epoch
            publish: Whether to publish the deletion
            event_type: Optional event type filter
            analytic_key: Optional analytic API key for bot access

        Returns:
            Result: API response confirming deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#delete-narrative
        """
        params = {
            "scope": scope,
            "narrativeId": narrative_id,
            "narrativeTime": narrative_time_ms,
            "publish": publish,
            "eventType": event_type,
        }
        params = {k: v for k, v in params.items() if v is not None}
        headers = None
        if analytic_key:
            headers = self.adapter._get_headers(analytic_key, APIKeyType.ANALYTIC)
        result: Result = self.adapter.delete(
            f"/espapi/cloud/json/locations/{location_id}/narratives",
            ep_params=params,
            ep_headers=headers,
        )
        return result
    
    def stream_message(
        self,
        scope: str,
        address: str,
        feed: dict,
        location_id: int = None,
        organization_id: int = None,
        locations: List[int] = None,
        bots: List[int] = None,
    ):
        """
        Stream a message to locations or bots.

        Args:
            scope: Message scope
            address: Target address for the message
            feed: Message feed data dictionary
            location_id: Optional specific location ID
            organization_id: Optional organization ID
            locations: Optional list of location IDs to stream to
            bots: Optional list of bot IDs to stream to

        Returns:
            Result: API response confirming message stream

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#stream-message
        """
        params = {
            "scope": scope,
            "address": address,
            "locationId": location_id,
            "organizationId": organization_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        body = {
            "locations": locations,
            "bots": bots,
            "feed": feed,
        }
        body = {k: v for k, v in body.items() if v is not None}
        headers = self.adapter._get_headers()
        if "ADMIN_KEY" in self.adapter._headers:
            headers = self.adapter._get_headers(
                self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            )
        result: Result = self.adapter.post(
            "/espapi/cloud/appstore/stream",
            ep_json=body,
            ep_params=params,
            ep_headers=headers,
        )
        return result

    def get_summary(
        self,
        location_id: int,
        organization_id: int = None,
    ):
        """
        Get summary information for a location.

        Args:
            location_id: Location ID to get summary for
            organization_id: Optional organization ID filter

        Returns:
            Result: API response containing location summary

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#get-summary
        """
        params = {
            "locationId": location_id,
            "organizationId": organization_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        headers = self.adapter._get_headers()
        if "ADMIN_KEY" in self.adapter._headers:
            headers = self.adapter._get_headers(
                self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            )
        result: Result = self.adapter.get(
            "/espapi/cloud/appstore/summary",
            ep_params=params,
            ep_headers=headers,
        )
        return result

    def put_state(
        self,
        location_id: int,
        name: str,
        state: Dict,
        overwrite: bool = None,
        publish: bool = None,
        updated: str = None,
        deleted: str = None,
    ):
        """
        Create or update location state.

        Args:
            location_id: Location ID to set state for
            name: State variable name
            state: State data dictionary
            overwrite: Whether to overwrite existing state
            publish: Whether to publish the state update
            updated: Comma-separated list of updated field names
            deleted: Comma-separated list of deleted field names

        Returns:
            Result: API response confirming state update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#put-state
        """
        params = {
            "name": name,
            "overwrite": overwrite,
            "publish": publish,
            "upd": updated,
            "del": deleted,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.put(
            f"/espapi/cloud/json/locations/{location_id}/state",
            ep_json=json.dumps(state),
            ep_params=params,
        )
        return result

    def get_state(
        self,
        location_id: int,
        name: List[str] | str = None,
    ):
        """
        Get location state variables.

        Args:
            location_id: Location ID to get state for
            name: Optional state variable name or list of names to filter

        Returns:
            Result: API response containing state variables

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#get-state
        """
        params = {
            "name": name,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            f"/espapi/cloud/json/locations/{location_id}/state",
            ep_params=params,
        )
        return result

    def delete_all_location_states(
        self,
        location_id: int,
    ):
        """
        Delete all location states.

        Args:
            location_id: Location ID to delete states for

        Returns:
            Result: API response confirming deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#delete-states
        """
        params = {
            "locationId": location_id,
        }
        result: Result = self.adapter.delete(
            "/espapi/cloud/json/locations/{locationId}/state".format(locationId=location_id),
            ep_params=params,
        )
        return result

    def put_time_state(
        self,
        location_id: int,
        name: str,
        timestamp_ms: int,
        state: Dict,
        overwrite: bool = None,
        publish: bool = None,
        updated: str = None,
        deleted: str = None,
    ):
        """
        Create or update time-series location state.

        Args:
            location_id: Location ID to set time state for
            name: State variable name
            timestamp_ms: Timestamp in milliseconds since epoch
            state: State data dictionary
            overwrite: Whether to overwrite existing state
            publish: Whether to publish the state update
            updated: Comma-separated list of updated field names
            deleted: Comma-separated list of deleted field names

        Returns:
            Result: API response confirming time state update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#put-time-state
        """
        params = {
            "name": name,
            "timestampMs": timestamp_ms,
            "overwrite": overwrite,
            "publish": publish,
            "upd": updated,
            "del": deleted,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.put(
            f"/espapi/cloud/json/locations/{location_id}/timeStates",
            ep_json=json.dumps(state),
            ep_params=params,
        )
        return result

    def get_time_state(
        self,
        location_id: int,
        start_date_ms: int,
        end_date_ms: int = None,
        name: List[str] | str = None,
        field: List[str] | str = None,
        keep_parent: bool = None,
        aggregation: int = None,
    ):
        """
        Get time-series location state variables.

        Args:
            location_id: Location ID to get time state for
            start_date_ms: Start date in milliseconds since epoch
            end_date_ms: End date in milliseconds since epoch
            name: Optional state variable name or list of names to filter
            field: Optional field name or list of field names to filter
            keep_parent: Whether to keep parent object structure
            aggregation: Aggregation type for time series data

        Returns:
            Result: API response containing time-series state variables

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#get-time-state
        """
        params = {
            "startDate": start_date_ms,
            "endDate": end_date_ms,
            "name": name,
            "field": field,
            "keepParent": keep_parent,
            "aggregation": aggregation,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            f"/espapi/cloud/json/locations/{location_id}/timeStates",
            ep_params=params,
        )
        return result

    def get_location_totals(
        self,
        organization_id: int = None,
    ):
        """
        Get location totals and statistics.

        Args:
            organization_id: Optional organization ID filter

        Returns:
            Result: API response containing location totals

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#get-location-totals
        """
        params = {
            "organizationId": organization_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/espapi/cloud/json/locationTotals", ep_params=params
        )
        return result

    def get_presence_ids(
        self,
        location_id: int,
    ):
        """
        Get presence IDs for a location.

        Args:
            location_id: Location ID to get presence IDs for

        Returns:
            Result: API response containing presence IDs

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#get-presence-ids
        """
        result: Result = self.adapter.get(
            f"/espapi/cloud/json/location/{location_id}/presence"
        )
        return result

    def get_presence(
        self,
    ) -> Result:
        """
        Get Presence IDs.

        These APIs determine if a person is physically present nearby one of location gateways,
        where the user has read access. It return UUIDs provided by all gateways, where the user has read access.

        Returns:
            Result: API response with iBeacon UUIDs

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Locations/operation/Get%20Presence%20IDs
        """
        result: Result = self.adapter.get(
            "/espapi/cloud/json/presence",
        )
        return result

    def authorize_presence_access(
        self,
        params_map: Dict,
    ) -> Result:
        """
        Authorize Access.

        Authorize access to the location, where the gateway with provided parameters is located.

        Args:
            params_map: Dictionary containing:
                - ibeaconUuid: iBeacon UUID (required)
                - ibeaconMajor: iBeacon major number (optional)
                - ibeaconMinor: iBeacon minor number (optional)

        Returns:
            Result: API response with location ID

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Locations/operation/Authorize%20Access
        """
        data = {
            "paramsMap": params_map,
        }
        result: Result = self.adapter.post(
            "/espapi/cloud/json/presence",
            ep_json=data,
        )
        return result

    def add_location_presence(
        self,
        location_id: int,
        presence_data: Dict,
    ):
        """
        Add presence information to a location.

        Args:
            location_id: Location ID to add presence to
            presence_data: Dictionary containing presence information

        Returns:
            Result: API response confirming presence addition

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#add-location-presence
        """
        result: Result = self.adapter.post(
            f"/espapi/cloud/json/location/{location_id}/presence",
            ep_json=json.dumps(presence_data),
        )
        return result

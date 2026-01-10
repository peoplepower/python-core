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


class Narratives(API):
    """
    Narratives API for retrieving organization narratives and related metadata.

    This class provides methods to search, filter, and paginate narrative records for organizations and their child organizations.
    Supports filtering by tags, location, type, priority, status, event type, and date range.

    Reference:
        https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Users-and-Locations
    """
    def get_organization_narratives(
        self,
        organization_id: int,
        row_count: int,
        search_tag: str = None,
        location_id: int = None,
        narrative_time: int = None,
        narrative_id: int = None,
        parent_id: int = None,
        narrative_type: int = None,
        priority: int = None,
        to_priority: int = None,
        status: int = None,
        event_type: str = None,
        search_by: str = None,
        start_date: str = None,
        end_date: str = None,
        page_marker: str = None,
    ) -> Result:
        """
        Get organization narratives for the specified organization and child organizations.

        The search results are organized by "pages". Each page contains a set of elements
        sorted by narrativeTime in descending order. The pages follow one another in
        reverse chronological order.

        The row_count parameter specifies the maximum number of elements per page.

        The result may include the nextMarker property - this means there are more pages
        for the current search criteria. To get the next page, pass the value of nextMarker
        to the page_marker parameter on the next API call.

        Args:
            organization_id: Organization ID
            row_count: Maximum number of elements per page (required)
            search_tag: Filter by location's tags (multiple values supported)
            location_id: Filter by location IDs (multiple values supported)
            narrative_time: Specific narrative time
            narrative_id: Filter by ID
            parent_id: Filter by parent ID
            narrative_type: Filter by narrative type (multiple values supported)
            priority: Filter by priority higher or equal than this
            to_priority: Filter by priority less or equal than this
            status: Filter by status (deleted are not returned by default)
            event_type: Filter by event type
            search_by: Filter by title or description (use * for wildcard)
            start_date: Narrative date range start (ISO 8601 format)
            end_date: Narrative date range end (ISO 8601 format)
            page_marker: Marker to the next page

        Returns:
            Result: API response with narratives data and optional nextMarker

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Users-and-Locations/operation/Get%20Organization%20Narratives
        """
        params = {
            "searchTag": search_tag,
            "locationId": location_id,
            "narrativeTime": narrative_time,
            "narrativeId": narrative_id,
            "parentId": parent_id,
            "narrativeType": narrative_type,
            "priority": priority,
            "toPriority": to_priority,
            "status": status,
            "eventType": event_type,
            "searchBy": search_by,
            "startDate": start_date,
            "endDate": end_date,
            "rowCount": row_count,
            "pageMarker": page_marker,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            f"/espapi/admin/json/organizations/{organization_id}/narratives",
            ep_params=params,
            ep_headers=self.adapter._get_headers(
                {"API_KEY": self.adapter._headers.get("ADMIN_KEY")}
            ),
        )
        return result

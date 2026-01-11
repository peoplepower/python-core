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


class Tags(API):
    def get_popular_tags(
        self,
        organization_id: int,
        tag_type: int,
        category: int = None,
        limit: int = None,
    ) -> Result:
        """
        Get a list of popular tags and their number of occurrences in this organization.

        This API call will return the top N user tags.

        Args:
            organization_id: Organization ID
            tag_type: Tag type filter (required)
            category: Location tag category (default 0)
            limit: Maximum number of elements to be returned

        Returns:
            Result: API response with popular tags and their counts

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Tags/operation/Popular%20Tags
        """
        params = {
            "type": tag_type,
            "category": category,
            "limit": limit,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            f"/espapi/admin/json/organizations/{organization_id}/tags",
            ep_params=params,
            ep_headers=self.adapter._get_headers(
                {"API_KEY": self.adapter._headers.get("ADMIN_KEY")}
            ),
        )
        return result

    def apply_tags(
        self,
        organization_id: int,
        tags_data: List[Dict],
    ) -> Result:
        """
        Apply tags to users, locations, and devices.

        Tags are a way to categorize sets of users, or devices.

        Args:
            organization_id: Organization ID
            tags_data: List of tag objects, each with 'type', 'id', and 'tag' fields

        Returns:
            Result: API response confirming tags applied

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Tags/operation/Apply%20Tags
        """
        data = {
            "tags": tags_data,
        }
        result: Result = self.adapter.put(
            f"/espapi/admin/json/organizations/{organization_id}/tags",
            ep_json=data if data else None,
            ep_headers=self.adapter._get_headers(
                {"API_KEY": self.adapter._headers.get("ADMIN_KEY")}
            ),
        )
        return result

    def delete_tag(
        self,
        organization_id: int,
        tag_type: int,
        entity_id: str,
        tag: str,
        app_id: int = None,
    ) -> Result:
        """
        Delete the given tag from the given user, location or device.

        An administrator can delete only tags related to his organization or to the specific bot.

        Args:
            organization_id: Organization ID
            tag_type: Tag type (required)
            entity_id: ID of user, location or device (required)
            tag: Tag value (required)
            app_id: Bot's app ID to delete the bot tag

        Returns:
            Result: API response confirming tag deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Tags/operation/Delete%20Tags
        """
        params = {
            "type": tag_type,
            "id": entity_id,
            "tag": tag,
            "appId": app_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.delete(
            f"/espapi/admin/json/organizations/{organization_id}/tags",
            ep_params=params,
            ep_headers=self.adapter._get_headers(
                {"API_KEY": self.adapter._headers.get("ADMIN_KEY")}
            ),
        )
        return result

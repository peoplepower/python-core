# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "requests",
# ]
# ///

from typing import Dict

from ..api import API

from ...models import (
    APIKeyType,
    Result,
)


class Groups(API):
    """
    Organization Groups API.

    Note: This API implementation is based on expected endpoints.
    The specific endpoints for organization groups were not found in the
    published admin.yaml documentation and may need verification.
    """

    def create_organization_group(
        self,
        organization_id: int,
        group_data: Dict,
    ) -> Result:
        """
        Create an organization group.

        Args:
            organization_id: Organization ID
            group_data: Group data as JSON object

        Returns:
            Result: API response with created group data

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html
        """
        result: Result = self.adapter.post(
            f"/espapi/admin/json/organizations/{organization_id}/groups",
            ep_json=group_data if group_data else None,
            ep_headers=self.adapter._get_headers(
                {"API_KEY": self.adapter._headers.get("ADMIN_KEY")}
            ),
        )
        return result

    def get_organization_groups(
        self,
        organization_id: int,
        group_id: int = None,
    ) -> Result:
        """
        Get organization groups.

        Args:
            organization_id: Organization ID
            group_id: Optional group ID to filter by

        Returns:
            Result: API response with groups data

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html
        """
        params = {
            "groupId": group_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            f"/espapi/admin/json/organizations/{organization_id}/groups",
            ep_params=params,
            ep_headers=self.adapter._get_headers(
                {"API_KEY": self.adapter._headers.get("ADMIN_KEY")}
            ),
        )
        return result

    def edit_organization_group(
        self,
        organization_id: int,
        group_id: int,
        group_data: Dict,
    ) -> Result:
        """
        Edit an organization group.

        Args:
            organization_id: Organization ID
            group_id: Group ID to edit
            group_data: Group data as JSON object

        Returns:
            Result: API response confirming update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html
        """
        result: Result = self.adapter.put(
            f"/espapi/admin/json/organizations/{organization_id}/groups/{group_id}",
            ep_json=group_data if group_data else None,
            ep_headers=self.adapter._get_headers(
                {"API_KEY": self.adapter._headers.get("ADMIN_KEY")}
            ),
        )
        return result

    def remove_organization_group(
        self,
        organization_id: int,
        group_id: int,
    ) -> Result:
        """
        Remove an organization group.

        Args:
            organization_id: Organization ID
            group_id: Group ID to remove

        Returns:
            Result: API response confirming deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html
        """
        result: Result = self.adapter.delete(
            f"/espapi/admin/json/organizations/{organization_id}/groups/{group_id}",
            ep_headers=self.adapter._get_headers(
                {"API_KEY": self.adapter._headers.get("ADMIN_KEY")}
            ),
        )
        return result

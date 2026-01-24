# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "requests",
# ]
# ///

from typing import Dict

from ..api import API

from ...models import (
    Result,
    APIKeyType,
)


class UserGroups(API):
    """
    User Groups API for managing user groups and group members.

    This class provides methods to create, retrieve, update, and delete user groups,
    as well as manage group members.

    Reference:
        https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Users-and-Locations
    """

    def get_user_groups(
        self,
        organization_id: int = None,
        group_id: int = None,
    ) -> Result:
        """
        Retrieve user groups.

        Args:
            organization_id: Organization ID to filter by
            group_id: User group ID to filter by

        Returns:
            Result: API response with user groups data

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html
        """
        params = {
            "organizationId": organization_id,
            "groupId": group_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/espapi/admin/json/userGroups",
            ep_params=params,
            ep_headers=self.adapter._get_headers(
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            ),
        )
        return result

    def create_user_group(
        self,
        group_data: Dict,
    ) -> Result:
        """
        Create a user group.

        Args:
            group_data: User group data as JSON object

        Returns:
            Result: API response with created group data

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html
        """
        result: Result = self.adapter.post(
            "/espapi/admin/json/userGroups",
            ep_json=group_data if group_data else None,
            ep_headers=self.adapter._get_headers(
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            ),
        )
        return result

    def update_user_group(
        self,
        group_id: int,
        group_data: Dict,
    ) -> Result:
        """
        Update a user group.

        Args:
            group_id: User group ID to update
            group_data: User group data as JSON object

        Returns:
            Result: API response confirming update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html
        """
        params = {
            "groupId": group_id,
        }
        result: Result = self.adapter.put(
            "/espapi/admin/json/userGroups",
            ep_params=params,
            ep_json=group_data if group_data else None,
            ep_headers=self.adapter._get_headers(
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            ),
        )
        return result

    def delete_user_group(
        self,
        group_id: int,
    ) -> Result:
        """
        Delete a user group.

        Args:
            group_id: User group ID to delete

        Returns:
            Result: API response confirming deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html
        """
        params = {
            "groupId": group_id,
        }
        result: Result = self.adapter.delete(
            "/espapi/admin/json/userGroups",
            ep_params=params,
            ep_headers=self.adapter._get_headers(
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            ),
        )
        return result

    def add_user_group_member(
        self,
        group_id: int,
        user_id: int,
    ) -> Result:
        """
        Add a user as a member to a user group.

        Args:
            group_id: User group ID
            user_id: User ID to add to the group

        Returns:
            Result: API response confirming member addition

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html
        """
        params = {
            "groupId": group_id,
            "userId": user_id,
        }
        result: Result = self.adapter.post(
            "/espapi/admin/json/userGroups/members",
            ep_params=params,
            ep_headers=self.adapter._get_headers(
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            ),
        )
        return result

    def remove_user_group_member(
        self,
        group_id: int,
        user_id: int,
    ) -> Result:
        """
        Remove a user from a user group.

        Args:
            group_id: User group ID
            user_id: User ID to remove from the group

        Returns:
            Result: API response confirming member removal

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html
        """
        params = {
            "groupId": group_id,
            "userId": user_id,
        }
        result: Result = self.adapter.delete(
            "/espapi/admin/json/userGroups/members",
            ep_params=params,
            ep_headers=self.adapter._get_headers(
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            ),
        )
        return result

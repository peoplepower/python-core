# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "requests",
# ]
# ///

from ..api import API

from ...models import (
    Result,
    APIKeyType,
)


class Users(API):
    """
    Users API for managing user accounts, roles, and permissions in the admin context.

    This class provides methods to retrieve users, manage roles, manage organization administrators,
    and manage notification users.

    Reference:
        https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Users-and-Locations
    """

    def get_users(
        self,
        organization_id: int = None,
        location_id: int = None,
        user_id: int = None,
        search_by: str = None,
        search_address: str = None,
        service_plan_id: int = None,
        search_tag: str = None,
        external_user_id: str = None,
        limit: int = None,
        get_tags: bool = None,
    ) -> Result:
        """
        Retrieve a list of users and their information based on the search criteria.

        System administrators can access all users, while Organization administrators
        can access users from within the organization they manage.

        Args:
            organization_id: Organization ID to search within
            location_id: Search for a user at a specific location ID
            user_id: Get a specific user by ID
            search_by: Searches for matching user login name, ID, email address, phone number, first name, last name. Use * for a wildcard
            search_address: Searches by location address fields: street, city, zip code
            service_plan_id: Filter users who have specific service plan
            search_tag: Search by user tag
            external_user_id: Search by external user ID
            limit: The maximum number of user records to retrieve in this request
            get_tags: Return user tags

        Returns:
            Result: API response with users data

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Users-and-Locations/operation/Get%20Users
        """
        params = {
            "organizationId": organization_id,
            "locationId": location_id,
            "userId": user_id,
            "searchBy": search_by,
            "searchAddress": search_address,
            "servicePlanId": service_plan_id,
            "searchTag": search_tag,
            "externalUserId": external_user_id,
            "limit": limit,
            "getTags": get_tags,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/espapi/admin/json/users",
            ep_params=params,
            ep_headers=self.adapter._get_headers(
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            ),
        )
        return result

    def get_roles(self) -> Result:
        """
        Retrieve administrative roles which can be granted to another user by an administrator.

        Returns:
            Result: API response with roles data

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Administrators/operation/Get%20Roles
        """
        result: Result = self.adapter.get(
            "/espapi/admin/json/roles",
            ep_headers=self.adapter._get_headers(
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            ),
        )
        return result

    def grant_user_role(
        self,
        user_id: int,
        role_id: int,
    ) -> Result:
        """
        Grant an administrative role to a user.

        A role can be granted or revoked only by an administrator with a corresponding permission.

        Args:
            user_id: User ID to grant this role to
            role_id: The Role ID to grant. This is specified by the "Get Roles" API

        Returns:
            Result: API response confirming role grant

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Administrators/operation/Grant%20Administrative%20Roles
        """
        result: Result = self.adapter.put(
            f"/espapi/admin/json/users/{user_id}/roles/{role_id}",
            ep_headers=self.adapter._get_headers(
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            ),
        )
        return result

    def revoke_user_role(
        self,
        user_id: int,
    ) -> Result:
        """
        Revoke administrative roles from a user.

        This removes all administrative roles from the specified user.

        Args:
            user_id: User ID for which to revoke administrative privileges

        Returns:
            Result: API response confirming role revocation

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Administrators/operation/Revoke%20Administrative%20Roles
        """
        result: Result = self.adapter.delete(
            f"/espapi/admin/json/users/{user_id}/roles",
            ep_headers=self.adapter._get_headers(
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            ),
        )
        return result

    def get_organization_admins(
        self,
        organization_id: int,
        parents: bool = None,
    ) -> Result:
        """
        Retrieve administrators for an organization.

        Args:
            organization_id: Organization ID to get administrators from
            parents: Get administrators from parent organizations as well

        Returns:
            Result: API response with administrators data

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Administrators/operation/Get%20Administrators
        """
        params = {
            "parents": parents,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            f"/espapi/admin/json/organizations/{organization_id}/admins",
            ep_params=params,
            ep_headers=self.adapter._get_headers(
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            ),
        )
        return result

    def add_organization_admin(
        self,
        organization_id: int,
        user_id: int,
        brand: str = None,
    ) -> Result:
        """
        Add a user as an administrator for an organization.

        Args:
            organization_id: Organization ID
            user_id: Administrator user ID to add to this organization
            brand: Notification brand

        Returns:
            Result: API response confirming admin addition

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Administrators/operation/Add%20an%20Administrator
        """
        params = {
            "brand": brand,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.put(
            f"/espapi/admin/json/organizations/{organization_id}/admins/{user_id}",
            ep_params=params,
            ep_headers=self.adapter._get_headers(
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            ),
        )
        return result

    def remove_organization_admin(
        self,
        organization_id: int,
        user_id: int,
    ) -> Result:
        """
        Remove administrator privileges from a user for an organization.

        Args:
            organization_id: Organization ID
            user_id: Administrator user ID to remove from this organization

        Returns:
            Result: API response confirming admin removal

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Administrators/operation/Remove%20Administrator
        """
        result: Result = self.adapter.delete(
            f"/espapi/admin/json/organizations/{organization_id}/admins/{user_id}",
            ep_headers=self.adapter._get_headers(
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            ),
        )
        return result

    def get_notification_groups(
        self,
        organization_id: int,
        group_id: int = None,
    ) -> Result:
        """
        Retrieve notification groups for an organization.

        Optional organization notification categories for backward compatibility:
        - 1: Manager
        - 2: Technician
        - 3: Organization Billing
        - 4: Research
        - 5: Provider
        - 6: Reports

        Args:
            organization_id: Organization ID
            group_id: Filter by group ID

        Returns:
            Result: API response with notification groups and their users

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Notifications/operation/Get%20Notification%20Groups
        """
        params = {}
        if group_id is not None:
            params["groupId"] = group_id
        result: Result = self.adapter.get(
            f"/espapi/admin/json/organizations/{organization_id}/notificationGroups",
            ep_params=params if params else None,
            ep_headers=self.adapter._get_headers(
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            ),
        )
        return result

    def create_notification_group(
        self,
        organization_id: int,
        name: str = None,
        group_id: int = None,
        category: int = None,
        description: str = None,
        default_group: bool = None,
        location_tag: str = None,
    ) -> Result:
        """
        Create or update an organization notification group.

        Args:
            organization_id: Organization ID
            name: Group name
            group_id: Optional group ID to update existing group
            category: Optional notification category
            description: Optional group description
            default_group: Default group for notifications
            location_tag: Location tag filter

        Returns:
            Result: API response with created or updated group ID

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Notifications/operation/Create%20Notification%20Group
        """
        group = {
            "groupId": group_id,
            "category": category,
            "name": name,
            "description": description,
            "defaultGroup": default_group,
            "locationTag": location_tag,
        }
        group = {k: v for k, v in group.items() if v is not None}
        result: Result = self.adapter.post(
            f"/espapi/admin/json/organizations/{organization_id}/notificationGroups",
            ep_json={"group": group},
            ep_headers=self.adapter._get_headers(
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            ),
        )
        return result

    def delete_notification_group(
        self,
        organization_id: int,
        group_id: int,
    ) -> Result:
        """
        Delete an organization notification group.

        Args:
            organization_id: Organization ID
            group_id: Group ID to delete

        Returns:
            Result: API response confirming deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Notifications/operation/Delete%20Notification%20Group
        """
        result: Result = self.adapter.delete(
            f"/espapi/admin/json/organizations/{organization_id}/notificationGroups",
            ep_params={"groupId": group_id},
            ep_headers=self.adapter._get_headers(
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            ),
        )
        return result

    def update_notification_users(
        self,
        organization_id: int,
        users: list[dict],
    ) -> Result:
        """
        Add and remove notification users to and from notification groups.

        Args:
            organization_id: Organization ID
            users: Users to add to or delete from notification groups.
                Each dict may contain:
                - userId: User ID
                - groupId: Group ID. If not set for the delete request, the user
                  will be deleted from all groups in the organization.
                - delete: Delete the user from the group

        Returns:
            Result: API response confirming the update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Notifications/operation/Update%20Notification%20Users
        """
        result: Result = self.adapter.put(
            f"/espapi/admin/json/organizations/{organization_id}/notificationUsers",
            ep_json={"users": users},
            ep_headers=self.adapter._get_headers(
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            ),
        )
        return result

    def get_notification_assignments(
        self,
        organization_id: int,
    ) -> Result:
        """
        Get notification group assignments.

        Return all possible notifications declared by bots, which are approved
        for the organization or included to the organization's service plans,
        and assigned notification groups.

        Args:
            organization_id: Organization ID

        Returns:
            Result: API response with notifications, their assigned groups and bots

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Notifications/operation/Get%20Notification%20Assignments
        """
        result: Result = self.adapter.get(
            f"/espapi/admin/json/organizations/{organization_id}/notificationAssignments",
            ep_headers=self.adapter._get_headers(
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            ),
        )
        return result

    def update_notification_assignments(
        self,
        organization_id: int,
        groups: list[dict],
    ) -> Result:
        """
        Update notification group assignments.

        Add or delete organization notification groups to or from notifications.
        Configured notifications must be declared by bots, which are either
        approved for the organization or included to the organization's
        service plans.

        Args:
            organization_id: Organization ID
            groups: Group operations. Each dict may contain:
                - notificationId: Notification ID
                - groupId: Group ID to add to or delete from the notification
                - delete: Delete it

        Returns:
            Result: API response confirming the update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Notifications/operation/Update%20Notification%20Assignmets
        """
        result: Result = self.adapter.put(
            f"/espapi/admin/json/organizations/{organization_id}/notificationAssignments",
            ep_json={"groups": groups},
            ep_headers=self.adapter._get_headers(
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            ),
        )
        return result

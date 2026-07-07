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

    def get_notification_users(
        self,
        organization_id: int,
    ) -> Result:
        """
        Retrieve notification users for an organization.

        Organization Notification Categories:
        - 1: Manager
        - 2: Technician
        - 3: Organization Bills
        - 4: Research
        - 5: Provider

        Args:
            organization_id: Organization ID

        Returns:
            Result: API response with notification users data

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Users-and-Locations/operation/Get%20Notification%20Users
        """
        result: Result = self.adapter.get(
            f"/espapi/admin/json/organizations/{organization_id}/notificationUsers",
            ep_headers=self.adapter._get_headers(
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            ),
        )
        return result

    def update_notification_user(
        self,
        organization_id: int,
        user_id: int,
        add_category: int = None,
        delete_category: int = None,
    ) -> Result:
        """
        Update notification user settings by adding or removing notification categories.

        This API allows to add and remove notification users with required categories.
        The response contains an array of this user notification categories after the operation completed.

        Args:
            organization_id: Organization ID
            user_id: User ID
            add_category: Notification categories to add, multiple values supported
            delete_category: Notification categories to remove, multiple values supported

        Returns:
            Result: API response with updated notification categories

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Users-and-Locations/operation/Update%20Notification%20User
        """
        params = {
            "userId": user_id,
            "addCategory": add_category,
            "deleteCategory": delete_category,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.put(
            f"/espapi/admin/json/organizations/{organization_id}/notificationUsers",
            ep_params=params,
            ep_headers=self.adapter._get_headers(
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            ),
        )
        return result

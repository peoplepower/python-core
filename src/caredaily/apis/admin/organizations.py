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


class Organizations(API):
    """
    Organizations API for managing organization records and related operations.

    This class provides methods to retrieve, create, update, and delete organizations, as well as get organization totals for locations and devices.
    Supports searching by ID, domain, and name, and includes hierarchical organization management.

    Reference:
        https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Organizations
    """
    def get_organizations(
        self,
        organization_id: int = None,
        domain_name: str = None,
        name: str = None,
    ) -> Result:
        """
        Retrieve organizations information.

        Args:
            organization_id: Specific organization ID to get information about
            domain_name: Exact domain name to search for
            name: First characters of organization name to search for

        Returns:
            Result: API response with organizations data

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Organizations/operation/Get%20Organizations
        """
        params = {
            "organizationId": organization_id,
            "domainName": domain_name,
            "name": name,
        }
        params = {k: v for k, v in params.items() if v is not None}
        headers = self.adapter._get_headers(key_type=APIKeyType.USER, api_key=self.adapter._headers.get('ADMIN_KEY'))
        result: Result = self.adapter.get(
            "/espapi/admin/json/organizations",
            ep_params=params,
            ep_headers=headers,
        )
        return result

    def create_organization(
        self,
        organization_data: Dict,
        parent_organization_id: int = None,
    ) -> Result:
        """
        Create an organization.

        Organizations can be created inside other organizations by users with
        "organization administrator" permission in the parent organization.
        Users with both "access all" and "organization administrator" permissions
        can create top level organizations.

        Args:
            organization_data: Organization data as JSON object with 'organization' key
            parent_organization_id: Parent organization ID where sub-organization will be created

        Returns:
            Result: API response with organizationId

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Organizations/operation/Create%20an%20Organization
        """
        params = {
            "organizationId": parent_organization_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        headers = self.adapter._get_headers(key_type=APIKeyType.USER, api_key=self.adapter._headers.get('ADMIN_KEY'))
        result: Result = self.adapter.post(
            "/espapi/admin/json/organizations",
            ep_params=params,
            ep_json=organization_data if organization_data else None,
            ep_headers=headers,
        )
        return result

    def edit_organization(
        self,
        organization_id: int,
        organization_data: Dict,
    ) -> Result:
        """
        Update an organization.

        Args:
            organization_id: Organization ID to update
            organization_data: Organization data as JSON object with 'organization' key

        Returns:
            Result: API response confirming update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Organizations/operation/Update%20Organization
        """
        params = {
            "organizationId": organization_id,
        }
        headers = self.adapter._get_headers(key_type=APIKeyType.USER, api_key=self.adapter._headers.get('ADMIN_KEY'))
        result: Result = self.adapter.put(
            "/espapi/admin/json/organizations",
            ep_params=params,
            ep_json=organization_data if organization_data else None,
            ep_headers=headers,
        )
        return result

    def delete_organization(
        self,
        organization_id: int,
    ) -> Result:
        """
        Delete an organization.

        Args:
            organization_id: Organization ID to delete

        Returns:
            Result: API response confirming deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Organizations/operation/Delete%20Organization
        """
        params = {
            "organizationId": organization_id,
        }
        headers = self.adapter._get_headers(key_type=APIKeyType.USER, api_key=self.adapter._headers.get('ADMIN_KEY'))
        result: Result = self.adapter.delete(
            "/espapi/admin/json/organizations",
            ep_params=params,
            ep_headers=headers,
        )
        return result

    def get_organization_totals(
        self,
        organization_id: int,
        locations: bool = None,
        user_devices: bool = None,
    ) -> Result:
        """
        Get total numbers of locations and devices in the organization.

        Totals returned:
        - locationsCount: Total number of locations
        - organizationDevices: Number of active and inactive devices

        Args:
            organization_id: Organization ID
            locations: Return total number of locations
            user_devices: Return number of devices

        Returns:
            Result: API response with totals data

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Users-and-Locations/operation/Get%20Organization%20Totals
        """
        params = {
            "locations": locations,
            "userDevices": user_devices,
        }
        params = {k: v for k, v in params.items() if v is not None}
        headers = self.adapter._get_headers(key_type=APIKeyType.USER, api_key=self.adapter._headers.get('ADMIN_KEY'))
        result: Result = self.adapter.get(
            f"/espapi/admin/json/organizations/{organization_id}/totals",
            ep_params=params,
            ep_headers=headers,
        )
        return result

    def get_brands(
        self,
    ) -> Result:
        """
        Get all supported brands.

        Available only to administrators with `access all` privilege.

        Returns:
            Result: API response with brands data

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Organizations/operation/Get%20Brands
        """
        headers = self.adapter._get_headers(key_type=APIKeyType.USER, api_key=self.adapter._headers.get('ADMIN_KEY'))
        result: Result = self.adapter.get(
            "/espapi/admin/json/brands",
            ep_headers=headers,
        )
        return result

    def get_organization_objects(
        self,
        organization_id: int,
    ) -> Result:
        """
        Retrieve all large objects and small properties by the organization.

        Anyone can call it. Private records are returned only for administrators.

        Args:
            organization_id: Organization ID

        Returns:
            Result: API response with organization objects data

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Organizations/operation/List%20Objects%20and%20Properties
        """
        headers = self.adapter._get_headers(key_type=APIKeyType.USER, api_key=self.adapter._headers.get('ADMIN_KEY'))
        result: Result = self.adapter.get(
            f"/espapi/admin/json/organizations/{organization_id}/objects",
            ep_headers=headers,
        )
        return result

    def set_organization_properties(
        self,
        organization_id: int,
        organization_objects: Dict,
    ) -> Result:
        """
        Update organization property values.

        Only administrator can call it.

        Args:
            organization_id: Organization ID
            organization_objects: Organization objects data as JSON object with 'organizationObjects' key

        Returns:
            Result: API response confirming update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Organizations/operation/Set%20Properties
        """
        headers = self.adapter._get_headers(key_type=APIKeyType.USER, api_key=self.adapter._headers.get('ADMIN_KEY'))
        result: Result = self.adapter.post(
            f"/espapi/admin/json/organizations/{organization_id}/objects",
            ep_json=organization_objects if organization_objects else None,
            ep_headers=headers,
        )
        return result

    def get_organization_object(
        self,
        organization_id: int,
        object_name: str,
    ) -> Result:
        """
        Return the previously uploaded object content.

        Private objects content is available only for organization administrators.
        Public objects content is available for any user.

        Args:
            organization_id: Organization ID
            object_name: Object name

        Returns:
            Result: API response with object content

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Organizations/operation/Get%20Object%20Content
        """
        headers = self.adapter._get_headers(key_type=APIKeyType.USER, api_key=self.adapter._headers.get('ADMIN_KEY'))
        result: Result = self.adapter.get(
            f"/espapi/admin/json/organizations/{organization_id}/objects/{object_name}",
            ep_headers=headers,
        )
        return result

    def upload_organization_object(
        self,
        organization_id: int,
        object_name: str,
        object_data: bytes,
        content_type: str,
        private: bool = None,
    ) -> Result:
        """
        Upload a large binary or text object like images, videos and email templates for an organization.

        This API is only available to organization administrators or organization bots.

        The `Content-Type` header must be like `video/*`, `image/*`, `text/plain`, `application/octet-stream` or `application/json`.

        Args:
            organization_id: Organization ID
            object_name: Object name
            object_data: Binary data of the object
            content_type: Content type (e.g., 'image/png', 'video/mp4')
            private: Set to true, if the object is private

        Returns:
            Result: API response confirming upload

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Organizations/operation/Upload%20Large%20Object
        """
        params = {}
        if private is not None:
            params["private"] = private
        headers = self.adapter._get_headers(key_type=APIKeyType.USER, api_key=self.adapter._headers.get('ADMIN_KEY'))
        headers["Content-Type"] = content_type
        result: Result = self.adapter.put(
            f"/espapi/admin/json/organizations/{organization_id}/objects/{object_name}",
            ep_params=params if params else None,
            ep_data=object_data,
            ep_headers=headers,
        )
        return result

    def delete_organization_object(
        self,
        organization_id: int,
        object_name: str,
    ) -> Result:
        """
        Delete an organization object.

        Args:
            organization_id: Organization ID
            object_name: Object name

        Returns:
            Result: API response confirming deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Organizations/operation/Delete%20Object
        """
        headers = self.adapter._get_headers(key_type=APIKeyType.USER, api_key=self.adapter._headers.get('ADMIN_KEY'))
        result: Result = self.adapter.delete(
            f"/espapi/admin/json/organizations/{organization_id}/objects/{object_name}",
            ep_headers=headers,
        )
        return result

    def get_ehr_facilities(
        self,
        organization_id: int,
    ) -> Result:
        """
        Return a list of partners facilities mapped to sub-organizations.

        Available for organization editors.

        Args:
            organization_id: Parent organization ID

        Returns:
            Result: API response with EHR facilities data

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/EHR/operation/Get%20EHR%20Facilities
        """
        headers = self.adapter._get_headers(key_type=APIKeyType.USER, api_key=self.adapter._headers.get('ADMIN_KEY'))
        result: Result = self.adapter.get(
            f"/espapi/admin/json/organizations/{organization_id}/ehrFacilities",
            ep_headers=headers,
        )
        return result

    def set_ehr_locations_filter(
        self,
        organization_id: int,
        application_id: int,
        facility_id: str,
        location_filter: Dict,
    ) -> Result:
        """
        Update a filter so Care Daily will only monitor a subset of rooms within each facility.

        Available for organization editors.

        Args:
            organization_id: Sub-organization ID
            application_id: Partner's application ID
            facility_id: Partner's facility ID
            location_filter: Location filter data as JSON object with 'locationFilter' key

        Returns:
            Result: API response confirming update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/EHR/operation/Set%20EHR%20Locations%20Filter
        """
        params = {
            "applicationId": application_id,
            "facilityId": facility_id,
        }
        headers = self.adapter._get_headers(key_type=APIKeyType.USER, api_key=self.adapter._headers.get('ADMIN_KEY'))
        result: Result = self.adapter.put(
            f"/espapi/admin/json/organizations/{organization_id}/ehrFacilities",
            ep_params=params,
            ep_json=location_filter if location_filter else None,
            ep_headers=headers,
        )
        return result

    def delete_ehr_facility(
        self,
        organization_id: int,
        application_id: int = None,
        facility_id: str = None,
    ) -> Result:
        """
        Delete an EHR facility mapping.

        Args:
            organization_id: Sub-organization ID
            application_id: Partner's application ID (optional)
            facility_id: Partner's facility ID (optional)

        Returns:
            Result: API response confirming deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/EHR/operation/Delete%20EHR%20Facility
        """
        params = {}
        if application_id is not None:
            params["applicationId"] = application_id
        if facility_id is not None:
            params["facilityId"] = facility_id
        headers = self.adapter._get_headers(key_type=APIKeyType.USER, api_key=self.adapter._headers.get('ADMIN_KEY'))
        result: Result = self.adapter.delete(
            f"/espapi/admin/json/organizations/{organization_id}/ehrFacilities",
            ep_params=params if params else None,
            ep_headers=headers,
        )
        return result

    def test_organization_notifications(
        self,
        organization_id: int,
        notification_data: Dict,
    ) -> Result:
        """
        Request to generate possible common notifications including emails, SMS, push notifications.
        The API will return all notification texts in a zip archive.

        Args:
            organization_id: Organization ID
            notification_data: Notification test data as JSON object with optional keys:
                - brand: Brand to overwrite the organization's brand
                - template: Test the specific notification template
                - language: Generate notifications in specific language
                - model: Notification template parameters key/value string map

        Returns:
            Result: API response with ZIP archive

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Organizations/operation/Test%20notifications
        """
        headers = self.adapter._get_headers(key_type=APIKeyType.USER, api_key=self.adapter._headers.get('ADMIN_KEY'))
        result: Result = self.adapter.post(
            f"/espapi/admin/json/organizations/{organization_id}/notifications",
            ep_json=notification_data if notification_data else None,
            ep_headers=headers,
        )
        return result

    def get_organization_surveys(
        self,
        organization_id: int,
    ) -> Result:
        """
        Get Organization Surveys.

        Return a list of surveys available for an organization or parent organizations.

        Args:
            organization_id: Organization ID

        Returns:
            Result: API response with surveys data

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Surveys/operation/Get%20Organization%20Surveys
        """
        headers = self.adapter._get_headers(key_type=APIKeyType.USER, api_key=self.adapter._headers.get('ADMIN_KEY'))
        result: Result = self.adapter.get(
            f"/espapi/admin/json/organizations/{organization_id}/surveys",
            ep_headers=headers,
        )
        return result

    def get_organization_survey_questions(
        self,
        organization_id: int,
        survey_key: str,
    ) -> Result:
        """
        Get Organization Survey Questions.

        Return specific survey details, sections, and questions.

        Args:
            organization_id: Organization ID
            survey_key: Survey Key

        Returns:
            Result: API response with survey details

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Surveys/operation/Get%20Organization%20Survey%20Questions
        """
        headers = self.adapter._get_headers(key_type=APIKeyType.USER, api_key=self.adapter._headers.get('ADMIN_KEY'))
        result: Result = self.adapter.get(
            f"/espapi/admin/json/organizations/{organization_id}/surveys/{survey_key}",
            ep_headers=headers,
        )
        return result

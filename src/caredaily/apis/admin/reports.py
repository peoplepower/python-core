# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "requests",
# ]
# ///

from typing import Dict, Optional

from ..api import API

from ...models import (
    Result,
    APIKeyType,
)


class Reports(API):
    """
    Reports API for managing report groups, generating reports, and retrieving report data.

    This class provides methods to manage report groups, generate reports, and retrieve
    report execution history and data.

    Reference:
        https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Reports
    """

    def get_report_groups(
        self,
        organization_id: int,
        analytic: bool = None,
        all_groups: bool = None,
    ) -> Result:
        """
        Get report groups available for organizations.

        Report groups allow configuring scheduled report parameters and assigning
        these groups to organization hierarchies.

        Args:
            organization_id: ID of organization included to some hierarchy
            analytic: Return only groups which include analytic reports (default: false)
            all_groups: Return all groups including not assigned to the organization (default: true)

        Returns:
            Result: API response with report groups data

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Reports/operation/Get%20Report%20Groups
        """
        params = {}
        if analytic is not None:
            params["analytic"] = analytic
        if all_groups is not None:
            params["all"] = all_groups
        result: Result = self.adapter.get(
            f"/espapi/reports/groups/{organization_id}",
            ep_params=params if params else None,
            ep_headers=self.adapter._get_headers(
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            ),
        )
        return result

    def set_report_group_organization(
        self,
        organization_id: int,
        report_group_id: int,
        notification_category: Optional[int] = None,
    ) -> Result:
        """
        Assign a report group to specific organization or update an existing assignment.

        A report group can be assigned to only one organization in the hierarchy.
        It is recommended to assign it to the top level organization.

        Args:
            organization_id: Organization ID
            report_group_id: Group ID
            notification_category: Notification category of organization users.
                                  To clear the notification category set it to 0.

        Returns:
            Result: API response confirming assignment

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Reports/operation/Set%20Report%20Group%20Organization
        """
        params = {
            "reportGroupId": report_group_id,
        }
        if notification_category is not None:
            params["notificationCategory"] = notification_category
        result: Result = self.adapter.put(
            f"/espapi/reports/groups/{organization_id}",
            ep_params=params,
            ep_headers=self.adapter._get_headers(
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            ),
        )
        return result

    def delete_report_group_organization(
        self,
        organization_id: int,
        report_group_id: int,
        notification_category: Optional[int] = None,
    ) -> Result:
        """
        Delete report group organization assignment.

        Args:
            organization_id: Organization ID
            report_group_id: Group ID
            notification_category: Notification category of organization users

        Returns:
            Result: API response confirming deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Reports/operation/Delete%20Report%20Group%20Organization
        """
        params = {
            "reportGroupId": report_group_id,
        }
        if notification_category is not None:
            params["notificationCategory"] = notification_category
        result: Result = self.adapter.delete(
            f"/espapi/reports/groups/{organization_id}",
            ep_params=params,
            ep_headers=self.adapter._get_headers(
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            ),
        )
        return result

    def get_reports(
        self,
        report_id: Optional[int] = None,
        organization_id: Optional[int] = None,
        report_group_id: Optional[int] = None,
        analytic: Optional[bool] = None,
    ) -> Result:
        """
        Get the list of reports available for an organization or a list of system reports if organization is not specified.

        For each report, the API returns the report id, report name, description, parameters and fields.
        Also, each report entry contains a list of report groups to which the report is included.

        Args:
            report_id: Filter by report ID
            organization_id: Filter by organization ID
            report_group_id: Filter by report group ID
            analytic: Filter by 'analytic' report flag

        Returns:
            Result: API response with reports data

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Reports/operation/Get%20Reports
        """
        params = {}
        if report_id is not None:
            params["reportId"] = report_id
        if organization_id is not None:
            params["organizationId"] = organization_id
        if report_group_id is not None:
            params["reportGroupId"] = report_group_id
        if analytic is not None:
            params["analytic"] = analytic
        result: Result = self.adapter.get(
            "/espapi/reports/reports",
            ep_params=params if params else None,
            ep_headers=self.adapter._get_headers(
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            ),
        )
        return result

    def generate_report(
        self,
        report_id: int,
        delivery_type: int,
        organization_id: Optional[int] = None,
        **kwargs,
    ) -> Result:
        """
        Generate specific report. The result is provided in the CSV format.

        Reports can be delivered by email or stored in the system and requested by calling
        the Get Report Data API.

        All report parameters should be provided in the query string.

        Args:
            report_id: Report ID
            delivery_type: Way to return report data (2=send by email, 3=save result to be retrieved later)
            organization_id: Generate report for specific organization
            **kwargs: Additional report parameters to pass in query string

        Returns:
            Result: API response with token to use in Get Report Data API

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Reports/operation/Generate%20Report
        """
        params = {
            "reportId": report_id,
            "deliveryType": delivery_type,
        }
        if organization_id is not None:
            params["organizationId"] = organization_id
        params.update(kwargs)
        result: Result = self.adapter.get(
            "/espapi/reports/generate",
            ep_params=params,
            ep_headers=self.adapter._get_headers(
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            ),
        )
        return result

    def get_report_executions(
        self,
        report_id: int,
        report_group_id: int,
        start_date: str,
        end_date: str,
        organization_id: Optional[int] = None,
    ) -> Result:
        """
        Get report executions history.

        Reports are executed according to the schedules defined for the report groups to which they belong.

        The output format of the report data depends on whether the report is analytical or not:
        - For analytical reports: single-row data returned as key-value pairs
        - For non-analytical reports: set of rows stored as a zip archive in AWS S3 with pre-signed URL

        Args:
            report_id: Report ID
            report_group_id: Report group ID
            start_date: Start date
            end_date: End date
            organization_id: Organization ID, required for organizational report group

        Returns:
            Result: API response with report executions data

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Reports/operation/Get%20Report%20Executions
        """
        params = {
            "reportId": report_id,
            "reportGroupId": report_group_id,
            "startDate": start_date,
            "endDate": end_date,
        }
        if organization_id is not None:
            params["organizationId"] = organization_id
        result: Result = self.adapter.get(
            "/espapi/reports/data",
            ep_params=params,
            ep_headers=self.adapter._get_headers(
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            ),
        )
        return result

    def get_report_collections(
        self,
        organization_id: int,
        collection_id: int = None,
        report_id: int = None,
    ) -> Result:
        """
        Get report collections for an organization.

        If collection_id is specified, returns only the matching collection.
        If report_id is specified, returns only collections that contain the given report.
        Otherwise, returns all collections for the organization.

        Args:
            organization_id: Organization ID
            collection_id: Filter by collection ID
            report_id: Filter by report ID

        Returns:
            Result: API response with report collections data

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Reports/operation/Get%20Report%20Collections
        """
        params = {}
        if collection_id is not None:
            params["collectionId"] = collection_id
        if report_id is not None:
            params["reportId"] = report_id
        result: Result = self.adapter.get(
            f"/espapi/reports/{organization_id}/collections",
            ep_params=params if params else None,
            ep_headers=self.adapter._get_headers(
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            ),
        )
        return result

    def create_report_collection(
        self,
        organization_id: int,
        name: str,
        execution_schedule: str,
        description: str = None,
        notification_categories: list[int] = None,
        start_date: str = None,
        reports: list[dict] = None,
    ) -> Result:
        """
        Create a new report collection for an organization.

        The collection name and execution schedule are required.
        The execution schedule is a cron expression.

        Optionally, a list of reports can be included.
        Each report must have a reportId.
        The combination of reportId and parameters must be unique across the collection.

        Args:
            organization_id: Organization ID
            name: Collection name
            execution_schedule: Cron expression for the execution schedule
            description: Collection description
            notification_categories: Notification categories
            start_date: Start date in ISO-8601 format. Defaults to the current date and time.
            reports: List of report dicts, each with reportId and optional parameters dict

        Returns:
            Result: API response with created collection data

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Reports/operation/Create%20Report%20Collection
        """
        body = {
            "name": name,
            "executionSchedule": execution_schedule,
        }
        if description is not None:
            body["description"] = description
        if notification_categories is not None:
            body["notificationCategories"] = notification_categories
        if start_date is not None:
            body["startDate"] = start_date
        if reports is not None:
            body["reports"] = reports
        result: Result = self.adapter.post(
            f"/espapi/reports/{organization_id}/collections",
            ep_json=body,
            ep_headers=self.adapter._get_headers(
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            ),
        )
        return result

    def update_report_collection(
        self,
        organization_id: int,
        collection_id: int,
        name: str = None,
        description: str = None,
        execution_schedule: str = None,
        notification_categories: list[int] = None,
        start_date: str = None,
        reports: list[dict] = None,
    ) -> Result:
        """
        Update an existing report collection.

        All request body fields are optional. Fields that are not provided retain their existing values.

        The reports array supports the following operations:
        - Keep existing report unchanged: provide collectionReportId only.
        - Add a new report: provide reportId without collectionReportId.
        - Modify an existing report's parameters: provide collectionReportId with new parameters.
        - Delete a report: provide collectionReportId with deleted set to true.

        The combination of reportId and parameters must be unique across the collection.

        Args:
            organization_id: Organization ID
            collection_id: Collection ID
            name: Collection name
            description: Collection description
            execution_schedule: Cron expression for the execution schedule
            notification_categories: Notification categories
            start_date: Start date in ISO-8601 format
            reports: List of report operation dicts

        Returns:
            Result: API response with updated collection data

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Reports/operation/Update%20Report%20Collection
        """
        body = {}
        if name is not None:
            body["name"] = name
        if description is not None:
            body["description"] = description
        if execution_schedule is not None:
            body["executionSchedule"] = execution_schedule
        if notification_categories is not None:
            body["notificationCategories"] = notification_categories
        if start_date is not None:
            body["startDate"] = start_date
        if reports is not None:
            body["reports"] = reports
        result: Result = self.adapter.put(
            f"/espapi/reports/{organization_id}/collections/{collection_id}",
            ep_json=body,
            ep_headers=self.adapter._get_headers(
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            ),
        )
        return result

    def delete_report_collection(
        self,
        organization_id: int,
        collection_id: int,
    ) -> Result:
        """
        Delete a report collection.

        Args:
            organization_id: Organization ID
            collection_id: Collection ID

        Returns:
            Result: API response confirming deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Reports/operation/Delete%20Report%20Collection
        """
        result: Result = self.adapter.delete(
            f"/espapi/reports/{organization_id}/collections/{collection_id}",
            ep_headers=self.adapter._get_headers(
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            ),
        )
        return result

    def get_report_data(
        self,
        token: str,
    ) -> Result:
        """
        Get report data by token.

        Args:
            token: Token from Generate Report API response

        Returns:
            Result: API response with report data

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Reports/operation/Get%20Report%20Data
        """
        result: Result = self.adapter.get(
            f"/espapi/reports/data/{token}",
            ep_headers=self.adapter._get_headers(
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            ),
        )
        return result

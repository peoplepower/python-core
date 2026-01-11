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
                {"API_KEY": self.adapter._headers.get("ADMIN_KEY")}
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
                {"API_KEY": self.adapter._headers.get("ADMIN_KEY")}
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
                {"API_KEY": self.adapter._headers.get("ADMIN_KEY")}
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
                {"API_KEY": self.adapter._headers.get("ADMIN_KEY")}
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
                {"API_KEY": self.adapter._headers.get("ADMIN_KEY")}
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
                {"API_KEY": self.adapter._headers.get("ADMIN_KEY")}
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
                {"API_KEY": self.adapter._headers.get("ADMIN_KEY")}
            ),
        )
        return result

# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "requests",
# ]
# ///

import json
from typing import Dict

from ..api import API

from ...models import (
    APIKeyType,
    Result,
)


class Billing(API):
    """
    Billing API for managing organization billing items, plans, versions, and bills.

    This class provides methods to retrieve, create, update, and delete billing items, plans, and bills for organizations.
    Supports plan assignment, bill generation, and retrieval of bill content in various formats.

    Reference:
        https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Billing
    """
    def get_billing_items(
        self,
    ) -> Result:
        """
        Get billing items.

        Billing items are base services for which organizations can be charged.
        An organization billing plan includes prices for each required billing item.

        Returns:
            Result: API response with billing items data

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Billing/operation/Get%20Billing%20Items
        """
        result: Result = self.adapter.get(
            "/espapi/admin/json/billingItems",
            ep_headers=self.adapter._get_headers(
                {"API_KEY": self.adapter._headers.get("ADMIN_KEY")}
            ),
        )
        return result

    def create_billing_plan(
        self,
        plan_data: Dict,
    ) -> Result:
        """
        Create a new billing plan.

        Args:
            plan_data: Plan data as JSON object with 'plan' key containing 'name' field

        Returns:
            Result: API response with created plan data

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Billing/operation/Get%20Billing%20Plans
        """
        result: Result = self.adapter.post(
            "/espapi/admin/json/billingPlans",
            ep_json=plan_data if plan_data else None,
            ep_headers=self.adapter._get_headers(
                {"API_KEY": self.adapter._headers.get("ADMIN_KEY")}
            ),
        )
        return result

    def update_billing_plan(
        self,
        plan_id: int,
        plan_data: Dict,
    ) -> Result:
        """
        Create or update an existing billing plan.

        Args:
            plan_id: Plan ID to update
            plan_data: Plan data as JSON object with 'plan' key containing 'name' field

        Returns:
            Result: API response confirming plan update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Billing/operation/Create%20or%20Update%20Billing%20Plan
        """
        params = {
            "planId": plan_id,
        }
        result: Result = self.adapter.post(
            "/espapi/admin/json/billingPlans",
            ep_params=params,
            ep_json=plan_data if plan_data else None,
            ep_headers=self.adapter._get_headers(
                {"API_KEY": self.adapter._headers.get("ADMIN_KEY")}
            ),
        )
        return result

    def get_billing_plans(
        self,
    ) -> Result:
        """
        Get billing plans.

        A billing plan is a collection of billing prices for each time period.
        A billing plan must be assigned to an organization to generate bills.

        Returns:
            Result: API response with billing plans data

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Billing/operation/Get%20Billing%20Plans
        """
        result: Result = self.adapter.get(
            "/espapi/admin/json/billingPlans",
            ep_headers=self.adapter._get_headers(
                {"API_KEY": self.adapter._headers.get("ADMIN_KEY")}
            ),
        )
        return result

    def create_billing_plan_version(
        self,
        plan_id: int,
        version_data: Dict,
    ) -> Result:
        """
        Create a new version of a billing plan.

        Args:
            plan_id: Billing plan ID
            version_data: Version data as JSON object with 'version' key containing 'startDate' and 'prices' fields

        Returns:
            Result: API response with created version data

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Billing/operation/Get%20Billing%20Plan%20Versions
        """
        result: Result = self.adapter.post(
            f"/espapi/admin/json/billingPlans/{plan_id}/versions",
            ep_json=version_data if version_data else None,
            ep_headers=self.adapter._get_headers(
                {"API_KEY": self.adapter._headers.get("ADMIN_KEY")}
            ),
        )
        return result

    def update_billing_plan_version(
        self,
        plan_id: int,
        plan_version_id: int,
        version_data: Dict,
    ) -> Result:
        """
        Create or update an existing version of a billing plan.

        Args:
            plan_id: Billing plan ID
            plan_version_id: Plan version ID to update
            version_data: Version data as JSON object with 'version' key containing 'startDate' and 'prices' fields

        Returns:
            Result: API response confirming version update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Billing/operation/Create%20or%20Update%20Billing%20Plan%20Version
        """
        params = {
            "planVersionId": plan_version_id,
        }
        result: Result = self.adapter.post(
            f"/espapi/admin/json/billingPlans/{plan_id}/versions",
            ep_params=params,
            ep_json=version_data if version_data else None,
            ep_headers=self.adapter._get_headers(
                {"API_KEY": self.adapter._headers.get("ADMIN_KEY")}
            ),
        )
        return result

    def get_billing_plan_versions(
        self,
        plan_id: int,
    ) -> Result:
        """
        Get billing plan versions for a specific plan.

        Args:
            plan_id: Billing plan ID

        Returns:
            Result: API response with billing plan versions data

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Billing/operation/Get%20Billing%20Plan%20Versions
        """
        result: Result = self.adapter.get(
            f"/espapi/admin/json/billingPlans/{plan_id}/versions",
            ep_headers=self.adapter._get_headers(
                {"API_KEY": self.adapter._headers.get("ADMIN_KEY")}
            ),
        )
        return result

    def get_organization_billing_plans(
        self,
        organization_id: int,
        start_date: str = None,
        end_date: str = None,
    ) -> Result:
        """
        Get billing plans for a specific organization.

        Args:
            organization_id: Organization ID
            start_date: Limit plans and versions by date (ISO 8601 format)
            end_date: Limit plans and versions by date (ISO 8601 format)

        Returns:
            Result: API response with organization billing plans data

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Billing/operation/Get%20Organization%20Billing%20Plans
        """
        params = {
            "startDate": start_date,
            "endDate": end_date,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            f"/espapi/admin/json/organizations/{organization_id}/billingPlans",
            ep_params=params,
            ep_headers=self.adapter._get_headers(
                {"API_KEY": self.adapter._headers.get("ADMIN_KEY")}
            ),
        )
        return result

    def set_organization_billing_plan(
        self,
        organization_id: int,
        plan_id: int,
        start_date: str = None,
    ) -> Result:
        """
        Set or update billing plan for an organization.

        Args:
            organization_id: Organization ID
            plan_id: Billing plan ID
            start_date: New plan start date (ISO 8601 format)

        Returns:
            Result: API response confirming plan assignment

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Billing/operation/Set%20Organization%20Billing%20Plan
        """
        params = {
            "planId": plan_id,
            "startDate": start_date,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.post(
            f"/espapi/admin/json/organizations/{organization_id}/billingPlans",
            ep_params=params,
            ep_headers=self.adapter._get_headers(
                {"API_KEY": self.adapter._headers.get("ADMIN_KEY")}
            ),
        )
        return result

    def delete_organization_billing_plan(
        self,
        organization_id: int,
        start_date: str = None,
    ) -> Result:
        """
        Delete billing plan assignment from an organization.

        Args:
            organization_id: Organization ID
            start_date: Stop billing date (ISO 8601 format)

        Returns:
            Result: API response confirming plan deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Billing/operation/Delete%20Organization%20Billing%20Plan
        """
        params = {
            "startDate": start_date,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.delete(
            f"/espapi/admin/json/organizations/{organization_id}/billingPlans",
            ep_params=params,
            ep_headers=self.adapter._get_headers(
                {"API_KEY": self.adapter._headers.get("ADMIN_KEY")}
            ),
        )
        return result

    def generate_bill(
        self,
        organization_id: int,
        start_date: str = None,
        end_date: str = None,
    ) -> Result:
        """
        Generate bills for an organization for one or multiple billing periods.

        The API (re)generates bills for one or multiple billing periods (months).
        The generated bills are saved in the database and returned in the response body.

        Bills can be generated starting from the previous organization's billing date or before it.
        All previous bills will be deleted.

        By default only one bill is generated. To generate multiple bills the endDate parameter must be provided.

        Args:
            organization_id: Organization ID
            start_date: Start date of the first billing period (ISO 8601 format)
            end_date: End date of the last billing period (ISO 8601 format)

        Returns:
            Result: API response with generated bill data

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Billing/operation/Generate%20Bills
        """
        params = {
            "startDate": start_date,
            "endDate": end_date,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.put(
            f"/espapi/admin/json/organizations/{organization_id}/bills",
            ep_params=params,
            ep_headers=self.adapter._get_headers(
                {"API_KEY": self.adapter._headers.get("ADMIN_KEY")}
            ),
        )
        return result

    def get_bills(
        self,
        organization_id: int,
        start_date: str,
        end_date: str = None,
    ) -> Result:
        """
        Get the list of bills generated for the organization for specified date range.

        Args:
            organization_id: Organization ID
            start_date: Start date (ISO 8601 format, required)
            end_date: End date, default is 1st day of the current month (ISO 8601 format)

        Returns:
            Result: API response with bills data

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Billing/operation/Get%20Bills
        """
        params = {
            "startDate": start_date,
            "endDate": end_date,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            f"/espapi/admin/json/organizations/{organization_id}/bills",
            ep_params=params,
            ep_headers=self.adapter._get_headers(
                {"API_KEY": self.adapter._headers.get("ADMIN_KEY")}
            ),
        )
        return result

    def get_bill_content(
        self,
        organization_id: int,
        bill_id: int,
        format: str,
    ) -> Result:
        """
        Return an organization bill in PDF or CSV format.

        Args:
            organization_id: Organization ID
            bill_id: Bill ID
            format: Bill file format ('pdf' or 'csv')

        Returns:
            Result: API response with bill content data

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Billing/operation/Get%20Bill%20Content
        """
        params = {
            "format": format,
        }
        result: Result = self.adapter.get(
            f"/espapi/admin/json/organizations/{organization_id}/bills/{bill_id}",
            ep_params=params,
            ep_headers=self.adapter._get_headers(
                {"API_KEY": self.adapter._headers.get("ADMIN_KEY")}
            ),
        )
        return result

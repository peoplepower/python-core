# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "requests",
# ]
# ///

from datetime import datetime
from typing import Dict

from ...models import Result
from ..api import API


class PaidServices(API):
    """
    Paid Services API for managing service plans, subscriptions, and payments.

    This class provides methods to retrieve service plans, manage subscriptions,
    handle purchases, manage payment profiles, and process transactions.

    Reference:
        https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Subscriptions
    """

    def get_service_plans(
        self,
        location_id: int = None,
        app_name: str = None,
        user_id: int = None,
        organization_id: int = None,
        deleted: bool = None,
        hidden_prices: bool = None,
        plans_only: bool = None,
        payment_type: int = None,
    ) -> Result:
        """
        Get Available Service Plans.

        Return a list of paid service plans for sale, or having been purchased by the user.

        Args:
            location_id: Location ID, required to get data for specific location
            app_name: Retrieve service plans available for the given unique app name
            user_id: Used by administrators to specify another user
            organization_id: Receive plans for another user in specific organization
            deleted: Return deleted plans
            hidden_prices: Return hidden prices
            plans_only: Return only service plans data without checking availability
            payment_type: Return only plans with prices of this payment type

        Returns:
            Result: API response with service plans

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Subscriptions/operation/Get%20Available%20Service%20Plans
        """
        params = {
            "locationId": location_id,
            "appName": app_name,
            "userId": user_id,
            "organizationId": organization_id,
            "deleted": deleted,
            "hiddenPrices": hidden_prices,
            "plansOnly": plans_only,
            "paymentType": payment_type,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/espapi/cloud/json/servicePlans",
            ep_params=params,
        )
        return result

    def get_location_service_plans(
        self,
        location_id: int,
        status: int = None,
        user_plan_id: int = None,
        get_card: bool = None,
        user_id: int = None,
    ) -> Result:
        """
        Get Location Service Plans.

        This API returns all service plans on specific location or purchased by a user or manually assigned to him.

        Args:
            location_id: Get plan on this location
            status: Service plan status filter
            user_plan_id: Get specific service plan by ID
            get_card: Retrieve payment card information from the payment provider
            user_id: Get plan by this user. Used by organization administrators.

        Returns:
            Result: API response with service plans

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Subscriptions/operation/Get%20Location%20Service%20Plans
        """
        params = {
            "locationId": location_id,
            "status": status,
            "userPlanId": user_plan_id,
            "getCard": get_card,
            "userId": user_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/espapi/cloud/json/userServicePlans",
            ep_params=params,
        )
        return result

    def post_an_apple_purchase_receipt(
        self,
        receipt_data: Dict,
        location_id: int = None,
        app_name: str = None,
    ) -> Result:
        """
        Apple Purchase.

        Submit an Apple purchase receipt to the Care Daily AI Platform.

        Args:
            receipt_data: Receipt data from Apple
            location_id: Location ID (required)
            app_name: Unique app name that is making the purchase

        Returns:
            Result: API response

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Subscriptions/operation/Apple%20Purchase
        """
        params = {
            "locationId": location_id,
            "appName": app_name,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.post(
            "/espapi/cloud/json/receipt/apple",
            ep_params=params,
            ep_json=receipt_data,
        )
        return result

    def get_payment_profiles(self) -> Result:
        """
        Get Payment Profiles.

        Returns payment profiles for the user.

        Returns:
            Result: API response with payment profiles

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html
        """
        result: Result = self.adapter.get("/espapi/cloud/json/paymentProfiles")
        return result

    def post_purchase_info(
        self,
        purchase_data: Dict,
        location_id: int = None,
    ) -> Result:
        """
        Post Purchase Info.

        Create a new purchase/subscription.

        Args:
            purchase_data: Purchase data including plan information
            location_id: Location ID

        Returns:
            Result: API response

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html
        """
        params = {
            "locationId": location_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.post(
            "/espapi/cloud/json/userServicePlans",
            ep_params=params,
            ep_json=purchase_data,
        )
        return result

    def update_purchase_info(
        self,
        purchase_id: int,
        purchase_data: Dict,
        location_id: int = None,
    ) -> Result:
        """
        Update Purchase Info.

        Update an existing purchase/subscription.

        Args:
            purchase_id: User service plan ID
            purchase_data: Purchase data to update
            location_id: Location ID

        Returns:
            Result: API response

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html
        """
        params = {
            "locationId": location_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.put(
            f"/espapi/cloud/json/userServicePlans/{purchase_id}",
            ep_params=params,
            ep_json=purchase_data,
        )
        return result

    def upgrade_purchased_plan(
        self,
        purchase_id: int,
        new_plan_id: int,
        location_id: int = None,
    ) -> Result:
        """
        Upgrade Purchased Plan.

        Upgrade an existing purchase to a new plan.

        Args:
            purchase_id: User service plan ID
            new_plan_id: New service plan ID to upgrade to
            location_id: Location ID

        Returns:
            Result: API response

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html
        """
        params = {
            "locationId": location_id,
            "newPlanId": new_plan_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.put(
            f"/espapi/cloud/json/userServicePlans/{purchase_id}/upgrade",
            ep_params=params,
        )
        return result

    def get_transactions(
        self,
        location_id: int,
        start_date_ms: int = None,
        end_date_ms: int = None,
        user_service_plan_id: int = None,
        upgrade: bool = None,
    ) -> Result:
        """
        Get Transactions.

        This API returns all payment transactions for specific user service plan or location.

        Args:
            location_id: Location ID (required)
            start_date_ms: Start date in milliseconds
            end_date_ms: End date in milliseconds
            user_service_plan_id: User service plan ID
            upgrade: Return only transactions, which caused service plan change

        Returns:
            Result: API response with transactions

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Subscriptions/operation/Get%20Transactions
        """
        params = {
            "locationId": location_id,
            "upgrade": upgrade,
        }
        # Convert milliseconds to ISO date strings if provided
        if start_date_ms:
            start_date = datetime.fromtimestamp(start_date_ms / 1000).isoformat()
            params["startDate"] = start_date
        if end_date_ms:
            end_date = datetime.fromtimestamp(end_date_ms / 1000).isoformat()
            params["endDate"] = end_date
        params = {k: v for k, v in params.items() if v is not None}
        
        # Use userServicePlanId if provided, otherwise use a general endpoint
        if user_service_plan_id:
            result: Result = self.adapter.get(
                f"/espapi/cloud/json/userServicePlanTransactions/{user_service_plan_id}",
                ep_params=params,
            )
        else:
            # If no userServicePlanId, use a general transactions endpoint
            result: Result = self.adapter.get(
                "/espapi/cloud/json/userServicePlanTransactions",
                ep_params=params,
            )
        return result

    def assign_services_to_location(
        self,
        assignment_data: Dict,
        location_id: int = None,
        organization_id: int = None,
        end_date: str = None,
    ) -> Result:
        """
        Assign Services to Location.

        Assign a service plan to a location or multiple locations.

        Args:
            assignment_data: Assignment data as JSON object with location IDs
            location_id: Location ID to assign the service plan (optional if in assignment_data)
            organization_id: Organization ID. Required if called by an organization administrator
            end_date: The end date of the service plan

        Returns:
            Result: API response confirming assignment

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Subscriptions
        """
        params = {
            "locationId": location_id,
            "organizationId": organization_id,
            "endDate": end_date,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.post(
            "/espapi/cloud/json/locationServicePlans/assign",
            ep_params=params,
            ep_json=assignment_data if assignment_data else None,
        )
        return result

    def assign_services_to_group_of_users(
        self,
        service_plan_id: int,
        assignment_data: Dict,
        location_id: int = None,
        organization_id: int = None,
        end_date: str = None,
    ) -> Result:
        """
        Assign Services to Group of Users.

        This API can be called by any user to assign free services.
        An administrator with a corresponding privilege level must provide a list of locations
        where to assign the service plan. User IDs are optional, but if set, their access
        to locations will be verified.

        Args:
            service_plan_id: The Service Plan ID to assign
            assignment_data: Assignment data as JSON object with 'locations' array containing location and user IDs
            location_id: Location ID to assign the service plan (optional if in assignment_data)
            organization_id: Organization ID. Required if called by an organization administrator
            end_date: The end date of the service plan

        Returns:
            Result: API response with result codes for assigning the plan to each location

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Subscriptions/operation/Assign%20Service%20Plan%20to%20Locations
        """
        params = {
            "locationId": location_id,
            "organizationId": organization_id,
            "endDate": end_date,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.post(
            f"/espapi/cloud/json/userServicePlans/{service_plan_id}",
            ep_params=params,
            ep_json=assignment_data if assignment_data else None,
        )
        return result

    def cancel_user_service_plan(
        self,
        service_plan_id: int,
        location_id: int = None,
        organization_id: int = None,
    ) -> Result:
        """
        Cancel User Service Plan.

        Cancel assigned service plan.

        Args:
            service_plan_id: The User service plan ID to cancel
            location_id: Location ID to cancel the service plan
            organization_id: Organization ID. Required if called by an organization administrator

        Returns:
            Result: API response confirming cancellation

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Subscriptions/operation/Cancel%20Service%20Plan
        """
        params = {
            "locationId": location_id,
            "organizationId": organization_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.delete(
            f"/espapi/cloud/json/userServicePlans/{service_plan_id}",
            ep_params=params,
        )
        return result

    def get_market_products(
        self,
        location_id: int = None,
        app_name: str = None,
        organization_id: int = None,
    ) -> Result:
        """
        Get Market Products.

        Retrieve market products available for purchase.

        Args:
            location_id: Location ID to filter products
            app_name: Filter products by app name
            organization_id: Filter products by organization ID

        Returns:
            Result: API response with market products list

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Subscriptions
        """
        params = {
            "locationId": location_id,
            "appName": app_name,
            "organizationId": organization_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/espapi/cloud/json/marketProducts",
            ep_params=params,
        )
        return result

    def get_chargify_token(
        self,
        user_id: int = None,
        location_id: int = None,
    ) -> Result:
        """
        Get Chargify Token.

        Retrieve a token for Chargify payment gateway integration.

        Args:
            user_id: User ID to get token for
            location_id: Location ID to get token for

        Returns:
            Result: API response with Chargify token

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Subscriptions
        """
        params = {
            "userId": user_id,
            "locationId": location_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/espapi/cloud/json/chargifyToken",
            ep_params=params,
        )
        return result

import unittest
from unittest.mock import MagicMock
from caredaily.apis.app import PaidServices

class TestPaidServices(unittest.TestCase):
    def setUp(self):
        self.ps = PaidServices()
        self.mock_adapter = MagicMock()
        self.ps.adapter = self.mock_adapter

    def test_get_service_plans(self):
        self.mock_adapter.get.return_value = 'service-plans-result'
        result = self.ps.get_service_plans()
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, 'service-plans-result')

    def test_post_an_apple_purchase_receipt(self):
        receipt_data = {'receipt': 'data'}
        self.mock_adapter.post.return_value = 'apple-purchase-result'
        result = self.ps.post_an_apple_purchase_receipt(receipt_data=receipt_data)
        self.mock_adapter.post.assert_called_once()
        self.assertEqual(result, 'apple-purchase-result')

    def test_get_payment_profiles(self):
        self.mock_adapter.get.return_value = 'payment-profiles-result'
        result = self.ps.get_payment_profiles()
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, 'payment-profiles-result')

    def test_post_purchase_info(self):
        purchase_data = {'purchase': {'planId': 1}}
        self.mock_adapter.post.return_value = 'post-purchase-info-result'
        result = self.ps.post_purchase_info(purchase_data=purchase_data)
        self.mock_adapter.post.assert_called_once()
        self.assertEqual(result, 'post-purchase-info-result')

    def test_update_purchase_info(self):
        purchase_id = 1
        purchase_data = {'purchase': {'status': 'active'}}
        self.mock_adapter.put.return_value = 'update-purchase-info-result'
        result = self.ps.update_purchase_info(purchase_id=purchase_id, purchase_data=purchase_data)
        self.mock_adapter.put.assert_called_once()
        self.assertEqual(result, 'update-purchase-info-result')

    def test_upgrade_purchased_plan(self):
        purchase_id = 1
        new_plan_id = 2
        self.mock_adapter.put.return_value = 'upgrade-plan-result'
        result = self.ps.upgrade_purchased_plan(purchase_id=purchase_id, new_plan_id=new_plan_id)
        self.mock_adapter.put.assert_called_once()
        self.assertEqual(result, 'upgrade-plan-result')

    def test_get_location_service_plans(self):
        location_id = 1
        self.mock_adapter.get.return_value = 'location-service-plans-result'
        result = self.ps.get_location_service_plans(location_id=location_id)
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, 'location-service-plans-result')

    def test_get_transactions(self):
        location_id = 1
        start_date_ms = 1000
        end_date_ms = 2000
        self.mock_adapter.get.return_value = 'transactions-result'
        result = self.ps.get_transactions(location_id=location_id, start_date_ms=start_date_ms, end_date_ms=end_date_ms)
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, 'transactions-result')

    def test_get_service_plans_with_all_params(self):
        self.mock_adapter.get.return_value = {'plans': []}
        result = self.ps.get_service_plans(
            location_id=123,
            app_name='test_app',
            user_id=456,
            organization_id=789,
            deleted=False,
            hidden_prices=True,
            plans_only=False,
            payment_type=1
        )
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['locationId'], 123)
        self.assertEqual(kwargs['ep_params']['appName'], 'test_app')
        self.assertEqual(kwargs['ep_params']['userId'], 456)
        self.assertEqual(kwargs['ep_params']['organizationId'], 789)
        self.assertEqual(kwargs['ep_params']['deleted'], False)
        self.assertEqual(kwargs['ep_params']['hiddenPrices'], True)
        self.assertEqual(kwargs['ep_params']['plansOnly'], False)
        self.assertEqual(kwargs['ep_params']['paymentType'], 1)

    def test_get_location_service_plans_with_all_params(self):
        self.mock_adapter.get.return_value = {'plans': []}
        result = self.ps.get_location_service_plans(
            location_id=123,
            status=1,
            user_plan_id=10,
            get_card=True,
            user_id=456
        )
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['status'], 1)
        self.assertEqual(kwargs['ep_params']['userPlanId'], 10)
        self.assertEqual(kwargs['ep_params']['getCard'], True)
        self.assertEqual(kwargs['ep_params']['userId'], 456)

    def test_post_an_apple_purchase_receipt_with_params(self):
        receipt_data = {'receipt': 'data'}
        self.mock_adapter.post.return_value = {'purchaseId': 1}
        result = self.ps.post_an_apple_purchase_receipt(
            receipt_data=receipt_data,
            location_id=123,
            app_name='test_app'
        )
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['locationId'], 123)
        self.assertEqual(kwargs['ep_params']['appName'], 'test_app')

    def test_post_purchase_info_with_location(self):
        purchase_data = {'purchase': {'planId': 1}}
        self.mock_adapter.post.return_value = {'purchaseId': 1}
        result = self.ps.post_purchase_info(
            purchase_data=purchase_data,
            location_id=123
        )
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['locationId'], 123)

    def test_update_purchase_info_with_location(self):
        purchase_id = 1
        purchase_data = {'purchase': {'status': 'active'}}
        self.mock_adapter.put.return_value = {'updated': True}
        result = self.ps.update_purchase_info(
            purchase_id=purchase_id,
            purchase_data=purchase_data,
            location_id=123
        )
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_params']['locationId'], 123)

    def test_upgrade_purchased_plan_with_location(self):
        purchase_id = 1
        new_plan_id = 2
        self.mock_adapter.put.return_value = {'upgraded': True}
        result = self.ps.upgrade_purchased_plan(
            purchase_id=purchase_id,
            new_plan_id=new_plan_id,
            location_id=123
        )
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_params']['locationId'], 123)

    def test_get_transactions_with_all_params(self):
        self.mock_adapter.get.return_value = {'transactions': []}
        result = self.ps.get_transactions(
            location_id=123,
            start_date_ms=1000,
            end_date_ms=2000,
            user_service_plan_id=10,
            upgrade=True
        )
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/userServicePlanTransactions/10')
        self.assertEqual(kwargs['ep_params']['upgrade'], True)

    def test_get_transactions_without_user_service_plan_id(self):
        self.mock_adapter.get.return_value = {'transactions': []}
        result = self.ps.get_transactions(
            location_id=123,
            start_date_ms=1000,
            end_date_ms=2000
        )
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/userServicePlanTransactions')

    def test_assign_services_to_location(self):
        assignment_data = {'locations': [{'locationId': 123}]}
        self.mock_adapter.post.return_value = {'assigned': True}
        result = self.ps.assign_services_to_location(assignment_data=assignment_data)
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/locationServicePlans/assign')
        self.assertEqual(kwargs['ep_json'], assignment_data)
        self.assertEqual(result, {'assigned': True})

    def test_assign_services_to_location_with_params(self):
        assignment_data = {'locations': [{'locationId': 123}]}
        self.mock_adapter.post.return_value = {'assigned': True}
        result = self.ps.assign_services_to_location(
            assignment_data=assignment_data,
            location_id=123,
            organization_id=456,
            end_date='2024-12-31'
        )
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['locationId'], 123)
        self.assertEqual(kwargs['ep_params']['organizationId'], 456)
        self.assertEqual(kwargs['ep_params']['endDate'], '2024-12-31')

    def test_assign_services_to_group_of_users(self):
        assignment_data = {'locations': [{'locationId': 123, 'userIds': [1, 2]}]}
        self.mock_adapter.post.return_value = {'assigned': True}
        result = self.ps.assign_services_to_group_of_users(
            service_plan_id=10,
            assignment_data=assignment_data
        )
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/userServicePlans/10')
        self.assertEqual(kwargs['ep_json'], assignment_data)
        self.assertEqual(result, {'assigned': True})

    def test_assign_services_to_group_of_users_with_params(self):
        assignment_data = {'locations': [{'locationId': 123}]}
        self.mock_adapter.post.return_value = {'assigned': True}
        result = self.ps.assign_services_to_group_of_users(
            service_plan_id=10,
            assignment_data=assignment_data,
            location_id=123,
            organization_id=456,
            end_date='2024-12-31'
        )
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['locationId'], 123)
        self.assertEqual(kwargs['ep_params']['organizationId'], 456)
        self.assertEqual(kwargs['ep_params']['endDate'], '2024-12-31')

    def test_cancel_user_service_plan(self):
        self.mock_adapter.delete.return_value = {'cancelled': True}
        result = self.ps.cancel_user_service_plan(service_plan_id=10)
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/userServicePlans/10')
        self.assertEqual(result, {'cancelled': True})

    def test_cancel_user_service_plan_with_params(self):
        self.mock_adapter.delete.return_value = {'cancelled': True}
        result = self.ps.cancel_user_service_plan(
            service_plan_id=10,
            location_id=123,
            organization_id=456
        )
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(kwargs['ep_params']['locationId'], 123)
        self.assertEqual(kwargs['ep_params']['organizationId'], 456)

    def test_get_market_products(self):
        self.mock_adapter.get.return_value = {'products': []}
        result = self.ps.get_market_products()
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/marketProducts')
        self.assertEqual(result, {'products': []})

    def test_get_market_products_with_filters(self):
        self.mock_adapter.get.return_value = {'products': []}
        result = self.ps.get_market_products(
            location_id=123,
            app_name='test_app',
            organization_id=456
        )
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['locationId'], 123)
        self.assertEqual(kwargs['ep_params']['appName'], 'test_app')
        self.assertEqual(kwargs['ep_params']['organizationId'], 456)

    def test_get_chargify_token(self):
        self.mock_adapter.get.return_value = {'token': 'test_token'}
        result = self.ps.get_chargify_token()
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/chargifyToken')
        self.assertEqual(result, {'token': 'test_token'})

    def test_get_chargify_token_with_params(self):
        self.mock_adapter.get.return_value = {'token': 'test_token'}
        result = self.ps.get_chargify_token(user_id=123, location_id=456)
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['userId'], 123)
        self.assertEqual(kwargs['ep_params']['locationId'], 456)

import unittest
from unittest.mock import MagicMock

from caredaily.apis.admin import Billing


class TestBilling(unittest.TestCase):
    def setUp(self):
        self.billing = Billing()
        self.mock_adapter = MagicMock()
        self.billing.adapter = self.mock_adapter
        self.mock_adapter._headers = {'ADMIN_KEY': 'admin_key'}
        self.mock_adapter._get_headers = MagicMock(return_value={'API_KEY': 'admin_key'})

    def test_get_billing_items_success(self):
        self.mock_adapter.get.return_value = {'items': []}
        result = self.billing.get_billing_items()
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, {'items': []})

    def test_create_billing_plan_success(self):
        plan_data = {'plan': {'name': 'Basic Plan'}}
        self.mock_adapter.post.return_value = {'planId': 1}
        result = self.billing.create_billing_plan(plan_data)
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_json'], plan_data)
        self.assertEqual(result, {'planId': 1})

    def test_update_billing_plan_success(self):
        plan_data = {'plan': {'name': 'Updated Plan'}}
        self.mock_adapter.post.return_value = {'status': 'ok'}
        result = self.billing.update_billing_plan(plan_id=1, plan_data=plan_data)
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['planId'], 1)
        self.assertEqual(kwargs['ep_json'], plan_data)
        self.assertEqual(result, {'status': 'ok'})

    def test_get_billing_plans_success(self):
        self.mock_adapter.get.return_value = {'plans': []}
        result = self.billing.get_billing_plans()
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, {'plans': []})

    def test_create_billing_plan_version_success(self):
        version_data = {'version': {'startDate': '2024-01-01', 'prices': []}}
        self.mock_adapter.post.return_value = {'versionId': 1}
        result = self.billing.create_billing_plan_version(plan_id=1, version_data=version_data)
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_json'], version_data)
        self.assertEqual(result, {'versionId': 1})

    def test_update_billing_plan_version_success(self):
        version_data = {'version': {'startDate': '2024-01-01', 'prices': []}}
        self.mock_adapter.post.return_value = {'status': 'ok'}
        result = self.billing.update_billing_plan_version(
            plan_id=1,
            plan_version_id=2,
            version_data=version_data
        )
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['planVersionId'], 2)
        self.assertEqual(kwargs['ep_json'], version_data)
        self.assertEqual(result, {'status': 'ok'})

    def test_get_billing_plan_versions_success(self):
        self.mock_adapter.get.return_value = {'versions': []}
        result = self.billing.get_billing_plan_versions(plan_id=1)
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, {'versions': []})

    def test_get_organization_billing_plans_success(self):
        self.mock_adapter.get.return_value = {'plans': []}
        result = self.billing.get_organization_billing_plans(
            organization_id=123,
            start_date='2024-01-01',
            end_date='2024-12-31'
        )
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['startDate'], '2024-01-01')
        self.assertEqual(kwargs['ep_params']['endDate'], '2024-12-31')
        self.assertEqual(result, {'plans': []})

    def test_get_organization_billing_plans_no_dates(self):
        self.mock_adapter.get.return_value = {'plans': []}
        self.billing.get_organization_billing_plans(organization_id=123)
        args, kwargs = self.mock_adapter.get.call_args
        self.assertNotIn('startDate', kwargs['ep_params'])
        self.assertNotIn('endDate', kwargs['ep_params'])

    def test_set_organization_billing_plan_success(self):
        self.mock_adapter.post.return_value = {'status': 'ok'}
        result = self.billing.set_organization_billing_plan(
            organization_id=123,
            plan_id=1,
            start_date='2024-01-01'
        )
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['planId'], 1)
        self.assertEqual(kwargs['ep_params']['startDate'], '2024-01-01')
        self.assertEqual(result, {'status': 'ok'})

    def test_set_organization_billing_plan_no_start_date(self):
        self.mock_adapter.post.return_value = {'status': 'ok'}
        self.billing.set_organization_billing_plan(organization_id=123, plan_id=1)
        args, kwargs = self.mock_adapter.post.call_args
        self.assertNotIn('startDate', kwargs['ep_params'])

    def test_delete_organization_billing_plan_success(self):
        self.mock_adapter.delete.return_value = {'status': 'ok'}
        result = self.billing.delete_organization_billing_plan(
            organization_id=123,
            start_date='2024-01-01'
        )
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(kwargs['ep_params']['startDate'], '2024-01-01')
        self.assertEqual(result, {'status': 'ok'})

    def test_delete_organization_billing_plan_no_start_date(self):
        self.mock_adapter.delete.return_value = {'status': 'ok'}
        self.billing.delete_organization_billing_plan(organization_id=123)
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertNotIn('startDate', kwargs['ep_params'])

    def test_generate_bill_success(self):
        self.mock_adapter.put.return_value = {'billId': 1}
        result = self.billing.generate_bill(
            organization_id=123,
            start_date='2024-01-01',
            end_date='2024-01-31'
        )
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_params']['startDate'], '2024-01-01')
        self.assertEqual(kwargs['ep_params']['endDate'], '2024-01-31')
        self.assertEqual(result, {'billId': 1})

    def test_generate_bill_no_dates(self):
        self.mock_adapter.put.return_value = {'billId': 1}
        self.billing.generate_bill(organization_id=123)
        args, kwargs = self.mock_adapter.put.call_args
        self.assertNotIn('startDate', kwargs['ep_params'])
        self.assertNotIn('endDate', kwargs['ep_params'])

    def test_get_bills_success(self):
        self.mock_adapter.get.return_value = {'bills': []}
        result = self.billing.get_bills(
            organization_id=123,
            start_date='2024-01-01',
            end_date='2024-01-31'
        )
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['startDate'], '2024-01-01')
        self.assertEqual(kwargs['ep_params']['endDate'], '2024-01-31')
        self.assertEqual(result, {'bills': []})

    def test_get_bills_no_end_date(self):
        self.mock_adapter.get.return_value = {'bills': []}
        self.billing.get_bills(organization_id=123, start_date='2024-01-01')
        args, kwargs = self.mock_adapter.get.call_args
        self.assertNotIn('endDate', kwargs['ep_params'])

    def test_get_bill_content_success(self):
        self.mock_adapter.get.return_value = {'content': 'pdf_content'}
        result = self.billing.get_bill_content(
            organization_id=123,
            bill_id=1,
            format='pdf'
        )
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['format'], 'pdf')
        self.assertEqual(result, {'content': 'pdf_content'})

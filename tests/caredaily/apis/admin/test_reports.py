import unittest
from unittest.mock import MagicMock

from caredaily.apis.admin import Reports


class TestReports(unittest.TestCase):
    def setUp(self):
        self.reports = Reports()
        self.mock_adapter = MagicMock()
        self.reports.adapter = self.mock_adapter
        self.mock_adapter._headers = {'ADMIN_KEY': 'admin_key'}
        self.mock_adapter._get_headers = MagicMock(return_value={'API_KEY': 'admin_key'})

    def test_get_report_groups_success(self):
        self.mock_adapter.get.return_value = {'groups': []}
        result = self.reports.get_report_groups(organization_id=123)
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, {'groups': []})

    def test_get_report_groups_with_filters(self):
        self.mock_adapter.get.return_value = {'groups': []}
        self.reports.get_report_groups(organization_id=123, analytic=True, all_groups=False)
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['analytic'], True)
        self.assertEqual(kwargs['ep_params']['all'], False)

    def test_get_report_groups_no_filters(self):
        self.mock_adapter.get.return_value = {'groups': []}
        self.reports.get_report_groups(organization_id=123)
        args, kwargs = self.mock_adapter.get.call_args
        self.assertIsNone(kwargs.get('ep_params'))

    def test_set_report_group_organization_success(self):
        self.mock_adapter.put.return_value = {'resultCode': 0}
        result = self.reports.set_report_group_organization(
            organization_id=123,
            report_group_id=1,
            notification_category=6
        )
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_params']['reportGroupId'], 1)
        self.assertEqual(kwargs['ep_params']['notificationCategory'], 6)
        self.assertEqual(result, {'resultCode': 0})

    def test_set_report_group_organization_without_notification_category(self):
        self.mock_adapter.put.return_value = {'resultCode': 0}
        self.reports.set_report_group_organization(
            organization_id=123,
            report_group_id=1
        )
        args, kwargs = self.mock_adapter.put.call_args
        self.assertNotIn('notificationCategory', kwargs['ep_params'])

    def test_delete_report_group_organization_success(self):
        self.mock_adapter.delete.return_value = {'resultCode': 0}
        result = self.reports.delete_report_group_organization(
            organization_id=123,
            report_group_id=1,
            notification_category=6
        )
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(kwargs['ep_params']['reportGroupId'], 1)
        self.assertEqual(kwargs['ep_params']['notificationCategory'], 6)
        self.assertEqual(result, {'resultCode': 0})

    def test_get_reports_success(self):
        self.mock_adapter.get.return_value = {'reports': []}
        result = self.reports.get_reports()
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertIsNone(kwargs.get('ep_params'))
        self.assertEqual(result, {'reports': []})

    def test_get_reports_with_all_filters(self):
        self.mock_adapter.get.return_value = {'reports': []}
        self.reports.get_reports(
            report_id=1,
            organization_id=123,
            report_group_id=2,
            analytic=True
        )
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['reportId'], 1)
        self.assertEqual(kwargs['ep_params']['organizationId'], 123)
        self.assertEqual(kwargs['ep_params']['reportGroupId'], 2)
        self.assertEqual(kwargs['ep_params']['analytic'], True)

    def test_generate_report_success(self):
        self.mock_adapter.get.return_value = {'token': 'abc123'}
        result = self.reports.generate_report(
            report_id=1,
            delivery_type=3,
            organization_id=123,
            startDate='2020-01-01',
            endDate='2020-01-31'
        )
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['reportId'], 1)
        self.assertEqual(kwargs['ep_params']['deliveryType'], 3)
        self.assertEqual(kwargs['ep_params']['organizationId'], 123)
        self.assertEqual(kwargs['ep_params']['startDate'], '2020-01-01')
        self.assertEqual(kwargs['ep_params']['endDate'], '2020-01-31')
        self.assertEqual(result, {'token': 'abc123'})

    def test_generate_report_without_organization_id(self):
        self.mock_adapter.get.return_value = {'token': 'abc123'}
        self.reports.generate_report(
            report_id=1,
            delivery_type=2
        )
        args, kwargs = self.mock_adapter.get.call_args
        self.assertNotIn('organizationId', kwargs['ep_params'])

    def test_get_report_executions_success(self):
        self.mock_adapter.get.return_value = {'executions': []}
        result = self.reports.get_report_executions(
            report_id=1,
            report_group_id=2,
            start_date='2020-01-01',
            end_date='2020-01-31',
            organization_id=123
        )
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['reportId'], 1)
        self.assertEqual(kwargs['ep_params']['reportGroupId'], 2)
        self.assertEqual(kwargs['ep_params']['startDate'], '2020-01-01')
        self.assertEqual(kwargs['ep_params']['endDate'], '2020-01-31')
        self.assertEqual(kwargs['ep_params']['organizationId'], 123)
        self.assertEqual(result, {'executions': []})

    def test_get_report_executions_without_organization_id(self):
        self.mock_adapter.get.return_value = {'executions': []}
        self.reports.get_report_executions(
            report_id=1,
            report_group_id=2,
            start_date='2020-01-01',
            end_date='2020-01-31'
        )
        args, kwargs = self.mock_adapter.get.call_args
        self.assertNotIn('organizationId', kwargs['ep_params'])

    def test_get_report_data_success(self):
        self.mock_adapter.get.return_value = {'data': 'report content'}
        result = self.reports.get_report_data(token='abc123')
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, {'data': 'report content'})

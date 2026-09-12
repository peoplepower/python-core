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
            notification_group_id=6
        )
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_params']['reportGroupId'], 1)
        self.assertEqual(kwargs['ep_params']['notificationGroupId'], 6)
        self.assertEqual(result, {'resultCode': 0})

    def test_set_report_group_organization_without_notification_group(self):
        self.mock_adapter.put.return_value = {'resultCode': 0}
        self.reports.set_report_group_organization(
            organization_id=123,
            report_group_id=1
        )
        args, kwargs = self.mock_adapter.put.call_args
        self.assertNotIn('notificationGroupId', kwargs['ep_params'])

    def test_delete_report_group_organization_success(self):
        self.mock_adapter.delete.return_value = {'resultCode': 0}
        result = self.reports.delete_report_group_organization(
            organization_id=123,
            report_group_id=1
        )
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(kwargs['ep_params'], {'reportGroupId': 1})
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
        self.assertNotIn('subOrgs', kwargs['ep_params'])
        self.assertNotIn('demandUserId', kwargs['ep_params'])

    def test_get_report_executions_with_sub_orgs_and_demand_user(self):
        self.mock_adapter.get.return_value = {'executions': []}
        self.reports.get_report_executions(
            report_id=1,
            report_group_id=2,
            organization_id=123,
            sub_orgs=True,
            demand_user_id=456,
        )
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['subOrgs'], True)
        self.assertEqual(kwargs['ep_params']['demandUserId'], 456)

    def test_get_report_data_success(self):
        self.mock_adapter.get.return_value = {'data': 'report content'}
        result = self.reports.get_report_data(token='abc123')
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, {'data': 'report content'})

    # Report Collections

    def test_get_report_collections_success(self):
        self.mock_adapter.get.return_value = {'collections': []}
        result = self.reports.get_report_collections(organization_id=123)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], "/espapi/reports/123/collections")
        self.assertIsNone(kwargs.get('ep_params'))
        self.assertEqual(result, {'collections': []})

    def test_get_report_collections_with_collection_id(self):
        self.mock_adapter.get.return_value = {'collections': []}
        self.reports.get_report_collections(organization_id=123, collection_id=5)
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['collectionId'], 5)

    def test_get_report_collections_with_report_id(self):
        self.mock_adapter.get.return_value = {'collections': []}
        self.reports.get_report_collections(organization_id=123, report_id=10)
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['reportId'], 10)

    def test_get_report_collections_with_both_filters(self):
        self.mock_adapter.get.return_value = {'collections': []}
        self.reports.get_report_collections(
            organization_id=123, collection_id=5, report_id=10
        )
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['collectionId'], 5)
        self.assertEqual(kwargs['ep_params']['reportId'], 10)

    def test_create_report_collection_success(self):
        self.mock_adapter.post.return_value = {'resultCode': 0}
        result = self.reports.create_report_collection(
            organization_id=123,
            name="Weekly Reports",
            execution_schedule="0 0 8 ? * MON",
        )
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(args[0], "/espapi/reports/123/collections")
        self.assertEqual(kwargs['ep_json']['name'], "Weekly Reports")
        self.assertEqual(kwargs['ep_json']['executionSchedule'], "0 0 8 ? * MON")
        self.assertNotIn('description', kwargs['ep_json'])
        self.assertEqual(result, {'resultCode': 0})

    def test_create_report_collection_with_all_params(self):
        self.mock_adapter.post.return_value = {'resultCode': 0}
        reports_list = [{"reportId": 1, "parameters": {"roleId": "1"}}]
        self.reports.create_report_collection(
            organization_id=123,
            name="Weekly Reports",
            execution_schedule="0 0 8 ? * MON",
            description="Weekly activity reports",
            notification_group_id=1,
            start_date="2025-01-15T08:00:00Z",
            reports=reports_list,
        )
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_json']['description'], "Weekly activity reports")
        self.assertEqual(kwargs['ep_json']['notificationGroupId'], 1)
        self.assertEqual(kwargs['ep_json']['startDate'], "2025-01-15T08:00:00Z")
        self.assertEqual(kwargs['ep_json']['reports'], reports_list)

    def test_update_report_collection_success(self):
        self.mock_adapter.put.return_value = {'resultCode': 0}
        result = self.reports.update_report_collection(
            organization_id=123,
            collection_id=1,
            name="Updated Reports",
        )
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], "/espapi/reports/123/collections/1")
        self.assertEqual(kwargs['ep_json']['name'], "Updated Reports")
        self.assertEqual(result, {'resultCode': 0})

    def test_update_report_collection_with_reports(self):
        self.mock_adapter.put.return_value = {'resultCode': 0}
        reports_list = [
            {"collectionReportId": 10},
            {"reportId": 2, "parameters": {"startDate": "2025-01-01"}},
            {"collectionReportId": 11, "deleted": True},
        ]
        self.reports.update_report_collection(
            organization_id=123,
            collection_id=1,
            reports=reports_list,
        )
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_json']['reports'], reports_list)

    def test_delete_report_collection_success(self):
        self.mock_adapter.delete.return_value = {'resultCode': 0}
        result = self.reports.delete_report_collection(
            organization_id=123,
            collection_id=1,
        )
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(args[0], "/espapi/reports/123/collections/1")
        self.assertEqual(result, {'resultCode': 0})

    def test_generate_report_with_collection(self):
        self.mock_adapter.get.return_value = {'resultCode': 0}
        result = self.reports.generate_report(
            report_id=5,
            delivery_type=3,
            collection_id=7,
            execution_date=1750000000000,
        )
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/reports/generate')
        self.assertEqual(kwargs['ep_params']['collectionId'], 7)
        self.assertEqual(kwargs['ep_params']['executionDate'], 1750000000000)
        self.assertEqual(result, {'resultCode': 0})

    def test_get_report_executions_collection_mode(self):
        self.mock_adapter.get.return_value = {'executions': []}
        result = self.reports.get_report_executions(
            collection_id=7,
            organization_id=123,
            start_date='2026-01-01',
            end_date='2026-02-01',
        )
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/reports/data')
        self.assertEqual(kwargs['ep_params']['collectionId'], 7)
        self.assertEqual(kwargs['ep_params']['organizationId'], 123)
        self.assertNotIn('reportId', kwargs['ep_params'])
        self.assertEqual(result, {'executions': []})

    def test_delete_report_executions(self):
        self.mock_adapter.delete.return_value = {'resultCode': 0}
        result = self.reports.delete_report_executions(
            collection_id=7,
            organization_id=123,
            execution_date='2026-01-15',
            report_id=5,
        )
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(args[0], '/espapi/reports/data')
        self.assertEqual(kwargs['ep_params']['collectionId'], 7)
        self.assertEqual(kwargs['ep_params']['organizationId'], 123)
        self.assertEqual(kwargs['ep_params']['executionDate'], '2026-01-15')
        self.assertEqual(kwargs['ep_params']['reportId'], 5)
        self.assertNotIn('collectionReportId', kwargs['ep_params'])
        self.assertEqual(result, {'resultCode': 0})

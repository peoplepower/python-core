import unittest
from unittest.mock import MagicMock

from caredaily.apis.admin import System


class TestSystem(unittest.TestCase):
    def setUp(self):
        self.system = System()
        self.mock_adapter = MagicMock()
        self.system.adapter = self.mock_adapter

    def test_get_system_status_success(self):
        self.mock_adapter.get.return_value = {
            'pulses': [],
            'min5Statuses': [],
            'hourStatuses': []
        }
        self.mock_adapter._headers = {'ADMIN_KEY': 'admin_key'}
        self.mock_adapter._get_headers = MagicMock(return_value={'API_KEY': 'admin_key'})
        result = self.system.get_system_status()
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params'], {})
        self.assertEqual(result, {
            'pulses': [],
            'min5Statuses': [],
            'hourStatuses': []
        })

    def test_get_system_status_with_organization_id(self):
        self.mock_adapter.get.return_value = {'status': 'ok'}
        self.mock_adapter._headers = {'ADMIN_KEY': 'admin_key'}
        self.mock_adapter._get_headers = MagicMock(return_value={'API_KEY': 'admin_key'})
        result = self.system.get_system_status(organization_id=123)
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['organizationId'], 123)
        self.assertEqual(result, {'status': 'ok'})

    def test_get_time_states_required_params(self):
        self.mock_adapter.get.return_value = {'resultCode': 0, 'states': []}
        self.mock_adapter._headers = {'ADMIN_KEY': 'admin_key'}
        self.mock_adapter._get_headers = MagicMock(return_value={'ADMIN_KEY': 'admin_key'})
        result = self.system.get_time_states(
            organization_id=42,
            start_date="2025-01-01T00:00:00Z",
            end_date="2025-01-31T23:59:59Z",
        )
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], "/espapi/admin/json/timeStates")
        self.assertEqual(kwargs['ep_params']['organizationId'], 42)
        self.assertEqual(kwargs['ep_params']['startDate'], "2025-01-01T00:00:00Z")
        self.assertEqual(kwargs['ep_params']['endDate'], "2025-01-31T23:59:59Z")
        self.assertNotIn('locationId', kwargs['ep_params'])
        self.assertNotIn('priorityCategory', kwargs['ep_params'])
        self.assertNotIn('name', kwargs['ep_params'])

    def test_get_time_states_all_params(self):
        self.mock_adapter.get.return_value = {'resultCode': 0, 'states': [{'name': 'awake'}]}
        self.mock_adapter._headers = {'ADMIN_KEY': 'admin_key'}
        self.mock_adapter._get_headers = MagicMock(return_value={'ADMIN_KEY': 'admin_key'})
        result = self.system.get_time_states(
            organization_id=42,
            start_date="2025-01-01T00:00:00Z",
            end_date="2025-01-31T23:59:59Z",
            location_id=100,
            priority_category=2,
            name="awake",
        )
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['organizationId'], 42)
        self.assertEqual(kwargs['ep_params']['locationId'], 100)
        self.assertEqual(kwargs['ep_params']['priorityCategory'], 2)
        self.assertEqual(kwargs['ep_params']['name'], "awake")

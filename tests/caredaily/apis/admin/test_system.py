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

import unittest
from unittest.mock import MagicMock

from caredaily.apis.admin import Devices
from caredaily.models import APIKeyType


class TestDevices(unittest.TestCase):
    def setUp(self):
        self.dev = Devices()
        self.mock_adapter = MagicMock()
        self.dev.adapter = self.mock_adapter

    def test_get_organization_devices_success(self):
        self.mock_adapter.get.return_value = {'devices': []}
        result = self.dev.get_organization_devices(organization_id=1)
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, {'devices': []})

    def test_get_organization_devices_with_params(self):
        self.dev.get_organization_devices(organization_id=1, device_id='abc', limit=5)
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['deviceId'], 'abc')
        self.assertEqual(kwargs['ep_params']['limit'], 5)

    def test_get_organization_devices_all_filters(self):
        self.mock_adapter._headers = {'ADMIN_KEY': 'admin_key'}
        self.mock_adapter._get_headers = MagicMock(return_value={'API_KEY': 'admin_key'})
        self.dev.get_organization_devices(
            organization_id=1,
            user_id=10,
            location_id=20,
            device_id='dev123',
            device_type=5,
            search_by='sensor',
            search_tag='temperature',
            less_update_date='2024-01-01',
            more_update_date='2024-01-02',
            param_name='temp',
            param_value='25',
            limit=100,
            get_tags=True
        )
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['organizationId'], 1)
        self.assertEqual(kwargs['ep_params']['userId'], 10)
        self.assertEqual(kwargs['ep_params']['locationId'], 20)
        self.assertEqual(kwargs['ep_params']['deviceId'], 'dev123')
        self.assertEqual(kwargs['ep_params']['deviceType'], 5)
        self.assertEqual(kwargs['ep_params']['searchBy'], 'sensor')
        self.assertEqual(kwargs['ep_params']['searchTag'], 'temperature')
        self.assertEqual(kwargs['ep_params']['lessUpdateDate'], '2024-01-01')
        self.assertEqual(kwargs['ep_params']['moreUpdateDate'], '2024-01-02')
        self.assertEqual(kwargs['ep_params']['paramName'], 'temp')
        self.assertEqual(kwargs['ep_params']['paramValue'], '25')
        self.assertEqual(kwargs['ep_params']['limit'], 100)
        self.assertEqual(kwargs['ep_params']['getTags'], True)

    def test_get_organization_devices_filters_none(self):
        self.mock_adapter._headers = {'ADMIN_KEY': 'admin_key'}
        self.mock_adapter._get_headers = MagicMock(return_value={'API_KEY': 'admin_key'})
        self.dev.get_organization_devices()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params'], {})

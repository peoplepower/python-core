import unittest
from unittest.mock import MagicMock
from caredaily.apis.app import CloudConnectivity

class TestCloudConnectivity(unittest.TestCase):
    def setUp(self):
        self.app = CloudConnectivity()
        self.mock_adapter = MagicMock()
        self.app.adapter = self.mock_adapter

    def test_check_availability_success(self):
        self.mock_adapter.get.return_value = {'status': 'ok'}
        result = self.app.check_availability()
        self.mock_adapter.get.assert_called_once_with('/espapi/watch', ep_headers={'Content-Type': 'text/plain'})
        self.assertEqual(result, {'status': 'ok'})

    def test_get_version_html(self):
        self.mock_adapter.get.return_value = 'html-version'
        result = self.app.get_version(version=True)
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, 'html-version')

    def test_get_version_json(self):
        self.mock_adapter.get.return_value = 'json-version'
        result = self.app.get_version(json_format=True)
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, 'json-version')

    def test_get_cloud_settings_with_params(self):
        self.mock_adapter.get.return_value = MagicMock(data={'clouds': []})
        result = self.app.get_cloud_settings(device_id='dev1', connected=True, version='1.0')
        self.mock_adapter.get.assert_called_once()
        self.assertTrue(hasattr(result, 'data'))

    def test_get_server_settings_with_params(self):
        self.mock_adapter.get.return_value = MagicMock(data={'server': {}, 'mqtt': {}})
        result = self.app.get_server_settings(server_type=MagicMock(value='RESTFUL'), crtTag=True, deviceId='dev1', connected=True, brand='brand', appName='app')
        self.mock_adapter.get.assert_called_once()
        self.assertTrue(hasattr(result, 'data'))

    def test_get_server_settings_url_with_params(self):
        self.mock_adapter.get.return_value = 'server-url-result'
        result = self.app.get_server_settings_url(server_type=MagicMock(value='RESTFUL'), device_id='dev1', connected=True, ssl=True, brand='brand', appName='app')
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, 'server-url-result')

    def test_get_cloud_instances(self):
        self.mock_adapter.get.return_value = 'cloud-instances-result'
        result = self.app.get_cloud_instances(device_id='dev1')
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, 'cloud-instances-result')

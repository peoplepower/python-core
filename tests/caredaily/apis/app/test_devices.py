import unittest
import json
from unittest.mock import MagicMock
from caredaily.apis.app import Devices

class TestDevices(unittest.TestCase):
    def setUp(self):
        self.dev = Devices()
        self.mock_adapter = MagicMock()
        self.dev.adapter = self.mock_adapter

    def test_register_device(self):
        self.mock_adapter.post.return_value = 'register-result'
        result = self.dev.register_device(
            device_id='dev1', location_id=1, device_type=2, description='Test device'
        )
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/devices/dev1')
        self.assertEqual(kwargs['ep_params']['locationId'], 1)
        self.assertEqual(kwargs['ep_params']['deviceType'], 2)
        self.assertEqual(kwargs['ep_params']['desc'], 'Test device')
        self.assertEqual(result, 'register-result')

    def test_get_devices(self):
        self.mock_adapter.get.return_value = 'devices-result'
        result = self.dev.get_devices(location_id=1)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/devices')
        self.assertEqual(kwargs['ep_params']['locationId'], 1)
        self.assertEqual(result, 'devices-result')

    def test_get_devices_with_all_params(self):
        self.mock_adapter.get.return_value = 'devices-result'
        result = self.dev.get_devices(
            location_id=1, user_id=2, check_persistent=True, space_id=3, get_tags=True
        )
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['locationId'], 1)
        self.assertEqual(kwargs['ep_params']['userId'], 2)
        self.assertEqual(kwargs['ep_params']['checkPersistent'], True)
        self.assertEqual(kwargs['ep_params']['spaceId'], 3)
        self.assertEqual(kwargs['ep_params']['getTags'], True)
        self.assertEqual(result, 'devices-result')

    def test_delete_multiple_devices(self):
        self.mock_adapter.delete.return_value = 'delete-multiple-result'
        result = self.dev.delete_multiple_devices(
            location_id=1, device_ids=['dev1', 'dev2'], clear_measurements=True
        )
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/devices')
        self.assertEqual(kwargs['ep_params']['locationId'], 1)
        self.assertEqual(kwargs['ep_params']['deviceId'], ['dev1', 'dev2'])
        self.assertEqual(kwargs['ep_params']['clearMeasurements'], True)
        self.assertEqual(result, 'delete-multiple-result')

    def test_get_device(self):
        self.mock_adapter.get.return_value = 'single-device-result'
        result = self.dev.get_device(device_id='dev1', location_id=1)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/devices/dev1')
        self.assertEqual(kwargs['ep_params']['locationId'], 1)
        self.assertEqual(result, 'single-device-result')

    def test_get_device_with_check_connected(self):
        self.mock_adapter.get.return_value = 'single-device-result'
        result = self.dev.get_device(device_id='dev1', location_id=1, check_connected=True)
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['checkConnected'], True)
        self.assertEqual(result, 'single-device-result')

    def test_get_device_services(self):
        self.mock_adapter.get.return_value = 'services-result'
        result = self.dev.get_device_services(device_id='dev1', location_id=1)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/devices/dev1/services')
        self.assertEqual(kwargs['ep_params']['locationId'], 1)
        self.assertEqual(result, 'services-result')

    def test_update_device(self):
        self.mock_adapter.put.return_value = 'update-result'
        result = self.dev.update_device(
            device_id='dev1', location_id=1, description='Updated description'
        )
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/devices/dev1')
        self.assertEqual(kwargs['ep_params']['locationId'], 1)
        self.assertEqual(kwargs['ep_params']['desc'], 'Updated description')
        self.assertEqual(result, 'update-result')

    def test_update_device_with_spaces(self):
        spaces_data = [{'spaceId': 1, 'name': 'Living Room'}]
        self.mock_adapter.put.return_value = 'update-result'
        result = self.dev.update_device(
            device_id='dev1', location_id=1, spaces=spaces_data
        )
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_json'], json.dumps({'spaces': spaces_data}))
        self.assertEqual(result, 'update-result')

    def test_delete_device(self):
        self.mock_adapter.delete.return_value = 'delete-result'
        result = self.dev.delete_device(device_id='dev1', location_id=1, clear_measurements=True)
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/devices/dev1')
        self.assertEqual(kwargs['ep_params']['locationId'], 1)
        self.assertEqual(kwargs['ep_params']['clearMeasurements'], True)
        self.assertEqual(result, 'delete-result')

    def test_get_device_sim_card(self):
        self.mock_adapter.get.return_value = 'sim-card-result'
        result = self.dev.get_device_sim_card(device_id='dev1', location_id=1)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/devices/dev1/simCard')
        self.assertEqual(kwargs['ep_params']['locationId'], 1)
        self.assertEqual(result, 'sim-card-result')

    def test_copy_device_simulator(self):
        self.mock_adapter.post.return_value = 'copy-simulator-result'
        result = self.dev.copy_device_simulator(
            device_id='dev1', location_id=1, new_device_id='dev2'
        )
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/devices/dev1/simulator')
        self.assertEqual(kwargs['ep_params']['locationId'], 1)
        self.assertEqual(kwargs['ep_params']['newDeviceId'], 'dev2')
        self.assertEqual(result, 'copy-simulator-result')

    def test_get_device_activation_info(self):
        self.mock_adapter.get.return_value = 'activation-info-result'
        result = self.dev.get_device_activation_info(device_id='dev1', location_id=1)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/devices/dev1/activation')
        self.assertEqual(kwargs['ep_params']['locationId'], 1)
        self.assertEqual(result, 'activation-info-result')

    def test_get_device_properties(self):
        self.mock_adapter.get.return_value = 'device-properties-result'
        result = self.dev.get_device_properties(device_id='dev1', location_id=1)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/devices/dev1/properties')
        self.assertEqual(kwargs['ep_params']['locationId'], 1)
        self.assertEqual(result, 'device-properties-result')

    def test_get_device_properties_with_filters(self):
        self.mock_adapter.get.return_value = 'properties-result'
        result = self.dev.get_device_properties(
            device_id='dev1', location_id=1, name='prop_name', index='0'
        )
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['name'], 'prop_name')
        self.assertEqual(kwargs['ep_params']['index'], '0')
        self.assertEqual(result, 'properties-result')

    def test_set_device_properties(self):
        properties_data = [{'name': 'prop1', 'value': 'value1'}]
        self.mock_adapter.put.return_value = 'set-properties-result'
        result = self.dev.set_device_properties(
            device_id='dev1', location_id=1, properties=properties_data
        )
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/devices/dev1/properties')
        self.assertEqual(kwargs['ep_params']['locationId'], 1)
        self.assertEqual(kwargs['ep_json'], json.dumps({'properties': properties_data}))
        self.assertEqual(result, 'set-properties-result')

    def test_delete_device_property(self):
        self.mock_adapter.delete.return_value = 'delete-property-result'
        result = self.dev.delete_device_property(
            device_id='dev1', location_id=1, name='prop_name', index='0'
        )
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/devices/dev1/properties')
        self.assertEqual(kwargs['ep_params']['locationId'], 1)
        self.assertEqual(kwargs['ep_params']['name'], 'prop_name')
        self.assertEqual(kwargs['ep_params']['index'], '0')
        self.assertEqual(result, 'delete-property-result')

    def test_delete_device_property_no_index(self):
        self.mock_adapter.delete.return_value = 'delete-property-result'
        result = self.dev.delete_device_property(device_id='dev1', location_id=1, name='prop_name')
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertNotIn('index', kwargs['ep_params'])
        self.assertEqual(result, 'delete-property-result')

    def test_link_device_to_space(self):
        self.mock_adapter.post.return_value = 'link-space-result'
        result = self.dev.link_device_to_space(device_id='dev1', location_id=1, space_id=2)
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/devices/dev1/spaces')
        self.assertEqual(kwargs['ep_params']['locationId'], 1)
        self.assertEqual(kwargs['ep_params']['spaceId'], 2)
        self.assertEqual(result, 'link-space-result')

    def test_unlink_device_from_space(self):
        self.mock_adapter.delete.return_value = 'unlink-space-result'
        result = self.dev.unlink_device_from_space(device_id='dev1', location_id=1, space_id=2)
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/devices/dev1/spaces')
        self.assertEqual(kwargs['ep_params']['locationId'], 1)
        self.assertEqual(kwargs['ep_params']['spaceId'], 2)
        self.assertEqual(result, 'unlink-space-result')

    def test_get_firmware_update_jobs(self):
        self.mock_adapter.get.return_value = 'firmware-jobs-result'
        result = self.dev.get_firmware_update_jobs(device_id='dev1', location_id=1)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/devices/dev1/firmware')
        self.assertEqual(kwargs['ep_params']['locationId'], 1)
        self.assertEqual(result, 'firmware-jobs-result')

    def test_set_firmware_update_status(self):
        self.mock_adapter.put.return_value = 'firmware-status-result'
        result = self.dev.set_firmware_update_status(
            device_id='dev1', location_id=1, status=1, job_id=123
        )
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/devices/dev1/firmware')
        self.assertEqual(kwargs['ep_params']['locationId'], 1)
        self.assertEqual(kwargs['ep_params']['status'], 1)
        self.assertEqual(kwargs['ep_params']['jobId'], 123)
        self.assertEqual(result, 'firmware-status-result')

    def test_set_firmware_update_status_no_job_id(self):
        self.mock_adapter.put.return_value = 'firmware-status-result'
        result = self.dev.set_firmware_update_status(device_id='dev1', location_id=1, status=1)
        args, kwargs = self.mock_adapter.put.call_args
        self.assertNotIn('jobId', kwargs['ep_params'])
        self.assertEqual(result, 'firmware-status-result')

    def test_get_device_logs(self):
        self.mock_adapter.get.return_value = 'logs-result'
        result = self.dev.get_device_logs(
            device_id='dev1', location_id=1, start_date_ms=1000, end_date_ms=2000
        )
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/devices/dev1/logs')
        self.assertEqual(kwargs['ep_params']['locationId'], 1)
        self.assertEqual(kwargs['ep_params']['startDate'], 1000)
        self.assertEqual(kwargs['ep_params']['endDate'], 2000)
        self.assertEqual(result, 'logs-result')

    def test_get_device_log_content(self):
        self.mock_adapter.get.return_value = 'log-content-result'
        result = self.dev.get_device_log_content(device_id='dev1', location_id=1, log_id=123)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/devices/dev1/logContent')
        self.assertEqual(kwargs['ep_params']['locationId'], 1)
        self.assertEqual(kwargs['ep_params']['logId'], 123)
        self.assertEqual(result, 'log-content-result')

    def test_upload_sensitivity_map(self):
        self.mock_adapter.post.return_value = 'upload-map-result'
        result = self.dev.upload_sensitivity_map(
            device_id='dev1', location_id=1, sensitivity_map='map_data'
        )
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/devices/dev1/sensitivityMap')
        self.assertEqual(kwargs['ep_params']['locationId'], 1)
        self.assertEqual(kwargs['ep_json'], json.dumps({'sensitivityMap': 'map_data'}))
        self.assertEqual(result, 'upload-map-result')

    def test_delete_sensitivity_map(self):
        self.mock_adapter.delete.return_value = 'delete-map-result'
        result = self.dev.delete_sensitivity_map(device_id='dev1', location_id=1)
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/devices/dev1/sensitivityMap')
        self.assertEqual(kwargs['ep_params']['locationId'], 1)
        self.assertEqual(result, 'delete-map-result')

    def test_register_device_voip_account(self):
        self.mock_adapter.post.return_value = 'voip-register-result'
        result = self.dev.register_device_voip_account(
            device_id='dev1',
            location_id=1,
            voip_account='account@example.com',
            voip_password='password',
            voip_server='server.example.com',
            voip_port=5060
        )
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/devices/dev1/voip')
        self.assertEqual(kwargs['ep_params']['locationId'], 1)
        body_dict = json.loads(kwargs['ep_json'])
        self.assertEqual(body_dict['account'], 'account@example.com')
        self.assertEqual(body_dict['password'], 'password')
        self.assertEqual(body_dict['server'], 'server.example.com')
        self.assertEqual(body_dict['port'], 5060)
        self.assertEqual(result, 'voip-register-result')

    def test_register_device_voip_account_minimal(self):
        self.mock_adapter.post.return_value = 'voip-register-result'
        result = self.dev.register_device_voip_account(
            device_id='dev1', location_id=1, voip_account='account@example.com', voip_password='password'
        )
        args, kwargs = self.mock_adapter.post.call_args
        body_dict = json.loads(kwargs['ep_json'])
        self.assertEqual(body_dict['account'], 'account@example.com')
        self.assertEqual(body_dict['password'], 'password')
        self.assertNotIn('server', body_dict)
        self.assertNotIn('port', body_dict)
        self.assertEqual(result, 'voip-register-result')

    def test_remove_device_voip_registration(self):
        self.mock_adapter.delete.return_value = 'voip-remove-result'
        result = self.dev.remove_device_voip_registration(device_id='dev1', location_id=1)
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/devices/dev1/voip')
        self.assertEqual(kwargs['ep_params']['locationId'], 1)
        self.assertEqual(result, 'voip-remove-result')

    def test_make_device_voip_call(self):
        self.mock_adapter.put.return_value = 'voip-call-result'
        result = self.dev.make_device_voip_call(
            device_id='dev1', location_id=1, callee='+1234567890', call_type='audio'
        )
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/devices/dev1/voipCall')
        self.assertEqual(kwargs['ep_params']['locationId'], 1)
        body_dict = json.loads(kwargs['ep_json'])
        self.assertEqual(body_dict['callee'], '+1234567890')
        self.assertEqual(body_dict['type'], 'audio')
        self.assertEqual(result, 'voip-call-result')

    def test_make_device_voip_call_no_type(self):
        self.mock_adapter.put.return_value = 'voip-call-result'
        result = self.dev.make_device_voip_call(device_id='dev1', location_id=1, callee='+1234567890')
        args, kwargs = self.mock_adapter.put.call_args
        body_dict = json.loads(kwargs['ep_json'])
        self.assertEqual(body_dict['callee'], '+1234567890')
        self.assertNotIn('type', body_dict)
        self.assertEqual(result, 'voip-call-result')

    def test_hangup_device_voip_call(self):
        self.mock_adapter.delete.return_value = 'voip-hangup-result'
        result = self.dev.hangup_device_voip_call(device_id='dev1', location_id=1)
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/devices/dev1/voipCall')
        self.assertEqual(kwargs['ep_params']['locationId'], 1)
        self.assertEqual(result, 'voip-hangup-result')

    def test_get_device_logs_list(self):
        """Test Case ID: TC-Devices-001
        Title: Get Device Logs List
        Priority: P1
        """
        self.mock_adapter.get.return_value = {'logs': []}
        result = self.dev.get_device_logs_list(
            location_id=123,
            device_id='dev1',
            start_date='2024-01-01',
            end_date='2024-01-31'
        )
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/deviceLogs')
        self.assertEqual(kwargs['ep_params']['locationId'], 123)
        self.assertEqual(kwargs['ep_params']['deviceId'], 'dev1')
        self.assertEqual(kwargs['ep_params']['startDate'], '2024-01-01')
        self.assertEqual(kwargs['ep_params']['endDate'], '2024-01-31')
        self.assertEqual(result, {'logs': []})

    def test_get_device_logs_list_minimal(self):
        """Test Case ID: TC-Devices-002
        Title: Get Device Logs List with Required Parameters Only
        Priority: P1
        """
        self.mock_adapter.get.return_value = {'logs': []}
        result = self.dev.get_device_logs_list(location_id=123)
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['locationId'], 123)
        self.assertNotIn('deviceId', kwargs['ep_params'])
        self.assertEqual(result, {'logs': []})

    def test_get_device_log_content_url(self):
        """Test Case ID: TC-Devices-003
        Title: Get Device Log Content URL
        Priority: P1
        """
        self.mock_adapter.get.return_value = {'url': 'https://example.com/log'}
        result = self.dev.get_device_log_content_url(
            location_id=123,
            device_id='dev1',
            log_date='2024-01-15'
        )
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/deviceLogContent')
        self.assertEqual(kwargs['ep_params']['locationId'], 123)
        self.assertEqual(kwargs['ep_params']['deviceId'], 'dev1')
        self.assertEqual(kwargs['ep_params']['logDate'], '2024-01-15')
        self.assertEqual(result, {'url': 'https://example.com/log'})

    def test_get_preregistered_device(self):
        """Test Case ID: TC-Devices-004
        Title: Get Pre-registered Device by ID
        Priority: P1
        """
        self.mock_adapter.get.return_value = {'device': {'id': 'dev1', 'type': 1}}
        result = self.dev.get_preregistered_device(device_id='dev1')
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/preregistered/dev1')
        self.assertEqual(result, {'device': {'id': 'dev1', 'type': 1}})

import unittest
from unittest.mock import MagicMock

from caredaily.apis.admin import Firmware


class TestFirmware(unittest.TestCase):
    def setUp(self):
        self.firmware = Firmware()
        self.mock_adapter = MagicMock()
        self.firmware.adapter = self.mock_adapter
        self.mock_adapter._headers = {'ADMIN_KEY': 'admin_key'}
        self.mock_adapter._get_headers = MagicMock(return_value={'API_KEY': 'admin_key'})

    def test_get_firmware_versions_success(self):
        self.mock_adapter.get.return_value = {'versions': []}
        result = self.firmware.get_firmware_versions(device_type=31)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['deviceType'], 31)
        self.assertEqual(result, {'versions': []})

    def test_upload_firmware_version_success(self):
        self.mock_adapter.post.return_value = {'versionId': 123}
        result = self.firmware.upload_firmware_version(
            device_type=31,
            firmware='Sensor_1.2.0',
            file_name='sensor.bin',
            check_sum='abc123',
            index='0'
        )
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['deviceType'], 31)
        self.assertEqual(kwargs['ep_params']['firmware'], 'Sensor_1.2.0')
        self.assertEqual(kwargs['ep_params']['fileName'], 'sensor.bin')
        self.assertEqual(kwargs['ep_params']['checkSum'], 'abc123')
        self.assertEqual(kwargs['ep_params']['index'], '0')
        self.assertEqual(result, {'versionId': 123})

    def test_upload_firmware_version_without_index(self):
        self.mock_adapter.post.return_value = {'versionId': 123}
        self.firmware.upload_firmware_version(
            device_type=31,
            firmware='Sensor_1.2.0',
            file_name='sensor.bin',
            check_sum='abc123'
        )
        args, kwargs = self.mock_adapter.post.call_args
        self.assertNotIn('index', kwargs['ep_params'])

    def test_delete_firmware_version_success(self):
        self.mock_adapter.delete.return_value = {'resultCode': 0}
        result = self.firmware.delete_firmware_version(version_id=123)
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(kwargs['ep_params']['versionId'], 123)
        self.assertEqual(result, {'resultCode': 0})

    def test_get_firmware_groups_success(self):
        self.mock_adapter.get.return_value = {'groups': []}
        result = self.firmware.get_firmware_groups()
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertIsNone(kwargs.get('ep_params'))
        self.assertEqual(result, {'groups': []})

    def test_get_firmware_groups_with_organization_id(self):
        self.mock_adapter.get.return_value = {'groups': []}
        self.firmware.get_firmware_groups(organization_id=123)
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['organizationId'], 123)

    def test_update_firmware_group_for_device_success(self):
        self.mock_adapter.put.return_value = {'resultCode': 0}
        result = self.firmware.update_firmware_group_for_device(
            device_id='abc123',
            group_id=1
        )
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_params']['deviceId'], 'abc123')
        self.assertEqual(kwargs['ep_params']['groupId'], 1)
        self.assertEqual(result, {'resultCode': 0})

    def test_update_firmware_group_for_device_without_group_id(self):
        self.mock_adapter.put.return_value = {'resultCode': 0}
        self.firmware.update_firmware_group_for_device(device_id='abc123')
        args, kwargs = self.mock_adapter.put.call_args
        self.assertNotIn('groupId', kwargs['ep_params'])

    def test_get_firmware_update_jobs_success(self):
        self.mock_adapter.get.return_value = {'jobs': []}
        result = self.firmware.get_firmware_update_jobs(device_type=31)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['deviceType'], 31)
        self.assertEqual(result, {'jobs': []})

    def test_get_firmware_update_jobs_with_group_id(self):
        self.mock_adapter.get.return_value = {'jobs': []}
        self.firmware.get_firmware_update_jobs(device_type=31, group_id=1)
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['deviceType'], 31)
        self.assertEqual(kwargs['ep_params']['groupId'], 1)

    def test_create_firmware_update_job_success(self):
        self.mock_adapter.post.return_value = {'jobId': 186}
        result = self.firmware.create_firmware_update_job(version_id=123)
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['versionId'], 123)
        self.assertEqual(result, {'jobId': 186})

    def test_create_firmware_update_job_with_all_params(self):
        self.mock_adapter.post.return_value = {'jobId': 186}
        self.firmware.create_firmware_update_job(
            version_id=123,
            forced=True,
            group_id=1
        )
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['versionId'], 123)
        self.assertEqual(kwargs['ep_params']['forced'], True)
        self.assertEqual(kwargs['ep_params']['groupId'], 1)

    def test_delete_firmware_update_job_success(self):
        self.mock_adapter.delete.return_value = {'resultCode': 0}
        result = self.firmware.delete_firmware_update_job(job_id=186)
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(kwargs['ep_params']['jobId'], 186)
        self.assertEqual(result, {'resultCode': 0})

import unittest
import pytest
from unittest.mock import MagicMock

from caredaily.apis.app import DeviceFiles


class TestDeviceFiles(unittest.TestCase):
    def setUp(self):
        self.df = DeviceFiles()
        self.mock_adapter = MagicMock()
        self.df.adapter = self.mock_adapter

    def test_upload_file(self):
        device_id = 'dev1'
        location_id = 1
        file_data = {'file': 'data'}
        self.mock_adapter.post.return_value = 'upload-file-result'
        result = self.df.upload_file(device_id=device_id, location_id=location_id, file_data=file_data)
        self.mock_adapter.post.assert_called_once()
        self.assertEqual(result, 'upload-file-result')

    def test_upload_file_with_all_params(self):
        device_id = 'dev1'
        location_id = 1
        file_data = {'file': 'data'}
        self.mock_adapter.post.return_value = {'fileId': 1}
        result = self.df.upload_file(
            device_id=device_id,
            location_id=location_id,
            file_data=file_data,
            proxy_id='proxy1',
            ext='jpg',
            expected_size=1024,
            timestamp='1234567890',
            timesec='1234567',
            duration=30,
            rotate=90,
            file_id=5,
            thumbnail=True,
            incomplete=False,
            upload_url=True,
            file_type=1
        )
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['proxyId'], 'proxy1')
        self.assertEqual(kwargs['ep_params']['ext'], 'jpg')
        self.assertEqual(kwargs['ep_params']['type'], 1)

    def test_get_files(self):
        device_id = 'dev1'
        location_id = 1
        self.mock_adapter.get.return_value = 'get-files-result'
        result = self.df.get_files(device_id=device_id, location_id=location_id)
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, 'get-files-result')

    def test_get_files_with_all_params(self):
        device_id = 'dev1'
        location_id = 1
        self.mock_adapter.get.return_value = {'files': []}
        result = self.df.get_files(
            device_id=device_id,
            location_id=location_id,
            file_type=1,
            owners=2,
            owner_id=10,
            device_description='Camera',
            start_date='2024-01-01',
            end_date='2024-01-31'
        )
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['type'], 1)
        self.assertEqual(kwargs['ep_params']['owners'], 2)
        self.assertEqual(kwargs['ep_params']['ownerId'], 10)
        self.assertEqual(kwargs['ep_params']['deviceDescription'], 'Camera')

    def test_delete_all_files(self):
        device_id = 'dev1'
        location_id = 1
        self.mock_adapter.delete.return_value = 'delete-all-files-result'
        result = self.df.delete_all_files(device_id=device_id, location_id=location_id)
        self.mock_adapter.delete.assert_called_once()
        self.assertEqual(result, 'delete-all-files-result')

    def test_upload_a_binary_files_parts_or_thumbnail(self):
        self.mock_adapter.post.return_value = {'uploaded': True}
        result = self.df.upload_a_binary_files_parts_or_thumbnail(
            file_id=123,
            proxy_id='proxy1',
            file_data={'data': 'chunk'}
        )
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/files/123')
        self.assertEqual(kwargs['ep_params']['proxyId'], 'proxy1')
        self.assertEqual(kwargs['ep_json'], {'data': 'chunk'})
        self.assertEqual(result, {'uploaded': True})

    def test_upload_a_binary_files_parts_or_thumbnail_with_options(self):
        self.mock_adapter.post.return_value = {'uploaded': True}
        result = self.df.upload_a_binary_files_parts_or_thumbnail(
            file_id=123,
            proxy_id='proxy1',
            file_data={'data': 'chunk'},
            thumbnail=True,
            incomplete=False,
            index=0
        )
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['thumbnail'], True)
        self.assertEqual(kwargs['ep_params']['incomplete'], False)
        self.assertEqual(kwargs['ep_params']['index'], 0)

    def test_get_last_n_files(self):
        self.mock_adapter.get.return_value = {'files': []}
        result = self.df.get_last_n_files(count=10, location_id=123)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/filesByCount/10')
        self.assertEqual(kwargs['ep_params']['locationId'], 123)
        self.assertEqual(result, {'files': []})

    def test_get_last_n_files_with_filters(self):
        self.mock_adapter.get.return_value = {'files': []}
        result = self.df.get_last_n_files(
            count=10,
            location_id=123,
            start_date='2024-01-01',
            end_date='2024-01-31',
            file_type=1,
            device_id='dev1',
            device_description='Camera'
        )
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['startDate'], '2024-01-01')
        self.assertEqual(kwargs['ep_params']['type'], 1)
        self.assertEqual(kwargs['ep_params']['deviceId'], 'dev1')

    def test_get_file_download_urls(self):
        self.mock_adapter.get.return_value = {'urls': {}}
        result = self.df.get_file_download_urls(file_id=123, location_id=1)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/files/123/url')
        self.assertEqual(kwargs['ep_params']['locationId'], 1)
        self.assertEqual(result, {'urls': {}})

    def test_get_file_download_urls_with_options(self):
        self.mock_adapter.get.return_value = {'urls': {}}
        result = self.df.get_file_download_urls(
            file_id=123,
            location_id=1,
            content=True,
            thumbnail=True,
            expiration=3600000
        )
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['content'], True)
        self.assertEqual(kwargs['ep_params']['thumbnail'], True)
        self.assertEqual(kwargs['ep_params']['expiration'], 3600000)

    def test_download_file(self):
        self.mock_adapter.get.return_value = b'file content'
        result = self.df.download_file(file_id=123, location_id=1)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/files/123')
        self.assertEqual(kwargs['ep_params']['locationId'], 1)
        self.assertEqual(result, b'file content')

    def test_download_file_with_options(self):
        self.mock_adapter.get.return_value = b'file content'
        result = self.df.download_file(
            file_id=123,
            location_id=1,
            user_id=10,
            thumbnail=True,
            attach=True,
            range_header='bytes=0-1023'
        )
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['thumbnail'], True)
        self.assertEqual(kwargs['ep_params']['attach'], True)
        self.assertEqual(kwargs['ep_headers']['Range'], 'bytes=0-1023')

    def test_update_file(self):
        file_data = {'file': {'viewed': True}}
        self.mock_adapter.put.return_value = {'updated': True}
        result = self.df.update_file(
            file_id=123,
            location_id=1,
            file_data=file_data
        )
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/files/123')
        self.assertEqual(kwargs['ep_params']['locationId'], 1)
        self.assertEqual(kwargs['ep_json'], file_data)
        self.assertEqual(result, {'updated': True})

    def test_update_file_with_options(self):
        file_data = {'file': {'favourite': True}}
        self.mock_adapter.put.return_value = {'updated': True}
        result = self.df.update_file(
            file_id=123,
            location_id=1,
            file_data=file_data,
            proxy_id='proxy1',
            incomplete=False,
            recover=True,
            pure=True
        )
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_params']['proxyId'], 'proxy1')
        self.assertEqual(kwargs['ep_params']['incomplete'], False)
        self.assertEqual(kwargs['ep_params']['recover'], True)
        self.assertEqual(kwargs['ep_params']['pure'], True)

    def test_delete_single_file(self):
        self.mock_adapter.delete.return_value = {'deleted': True}
        result = self.df.delete_single_file(file_id=123, location_id=1)
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/files/123')
        self.assertEqual(kwargs['ep_params']['locationId'], 1)
        self.assertEqual(result, {'deleted': True})

    def test_get_files_summary(self):
        self.mock_adapter.get.return_value = {'summary': {}}
        result = self.df.get_files_summary(aggregation=2, location_id=123)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/filesSummary/2')
        self.assertEqual(kwargs['ep_params']['locationId'], 123)
        self.assertEqual(result, {'summary': {}})

    def test_get_files_summary_with_filters(self):
        self.mock_adapter.get.return_value = {'summary': {}}
        result = self.df.get_files_summary(
            aggregation=2,
            location_id=123,
            start_date='2024-01-01',
            end_date='2024-01-31',
            owners=1,
            details=True
        )
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['startDate'], '2024-01-01')
        self.assertEqual(kwargs['ep_params']['owners'], 1)
        self.assertEqual(kwargs['ep_params']['details'], True)

    def test_get_file_info(self):
        self.mock_adapter.get.return_value = {'file': {}}
        result = self.df.get_file_info(file_id=123, location_id=1)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/filesInfo/123')
        self.assertEqual(kwargs['ep_params']['locationId'], 1)
        self.assertEqual(result, {'file': {}})

    def test_get_file_devices(self):
        self.mock_adapter.get.return_value = {'devices': []}
        result = self.df.get_file_devices(location_id=123)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/fileDevices')
        self.assertEqual(kwargs['ep_params']['locationId'], 123)
        self.assertEqual(result, {'devices': []})

    def test_apply_file_tags(self):
        tags = {'tags': ['tag1', 'tag2']}
        self.mock_adapter.put.return_value = {'applied': True}
        result = self.df.apply_file_tags(file_id=123, tags=tags)
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/files/123/tags')
        self.assertEqual(kwargs['ep_json'], tags)
        self.assertEqual(result, {'applied': True})

    def test_delete_file_tags(self):
        tags = {'tags': ['tag1']}
        self.mock_adapter.delete.return_value = {'deleted': True}
        result = self.df.delete_file_tags(file_id=123, tags=tags)
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/files/123/tags')
        self.assertEqual(kwargs['ep_json'], tags)
        self.assertEqual(result, {'deleted': True})

    def test_delete_file_tags_without_tags(self):
        self.mock_adapter.delete.return_value = {'deleted': True}
        result = self.df.delete_file_tags(file_id=123)
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertIsNone(kwargs['ep_json'])

    def test_report_file(self):
        self.mock_adapter.put.return_value = {'reported': True}
        result = self.df.report_file(file_id=123)
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/files/123/report/abuse')
        self.assertEqual(result, {'reported': True})

    def test_report_file_with_type(self):
        self.mock_adapter.put.return_value = {'reported': True}
        result = self.df.report_file(file_id=123, report_type='spam')
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/files/123/report/spam')

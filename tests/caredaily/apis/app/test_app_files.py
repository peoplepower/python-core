import unittest
from unittest.mock import MagicMock
from caredaily.apis.app import AppFiles

class TestAppFiles(unittest.TestCase):
    def setUp(self):
        self.af = AppFiles()
        self.mock_adapter = MagicMock()
        self.af.adapter = self.mock_adapter


    def test_upload_file_content(self):
        file_content = b'file content bytes'
        self.mock_adapter.post.return_value = 'upload-file-content-result'
        result = self.af.upload_file_content(
            file_content=file_content,
            content_type='image/jpeg',
            file_type=1
        )
        self.mock_adapter.post.assert_called_once_with(
            "/espapi/cloud/json/appfiles",
            ep_params={'type': 1},
            ep_data=file_content,
            ep_headers={'Content-Type': 'image/jpeg'}
        )
        self.assertEqual(result, 'upload-file-content-result')

    def test_upload_file_content_default_content_type(self):
        file_content = b'file content bytes'
        self.mock_adapter.post.return_value = 'upload-file-content-result'
        result = self.af.upload_file_content(
            file_content=file_content,
            file_type=1
        )
        self.mock_adapter.post.assert_called_once_with(
            "/espapi/cloud/json/appfiles",
            ep_params={'type': 1},
            ep_data=file_content,
            ep_headers={'Content-Type': 'application/octet-stream'}
        )
        self.assertEqual(result, 'upload-file-content-result')

    def test_get_files(self):
        self.mock_adapter.get.return_value = 'get-files-result'
        result = self.af.get_files()
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, 'get-files-result')

    def test_download_file(self):
        file_id = 'file123'
        self.mock_adapter.get.return_value = 'download-file-result'
        result = self.af.download_file(file_id=file_id)
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, 'download-file-result')

    def test_delete_file(self):
        file_id = 'file123'
        self.mock_adapter.delete.return_value = 'delete-file-result'
        result = self.af.delete_file(file_id=file_id)
        self.mock_adapter.delete.assert_called_once()
        self.assertEqual(result, 'delete-file-result')

import unittest
from unittest.mock import patch

from caredaily.apis.api import API


class TestAPI(unittest.TestCase):
    @patch("caredaily.apis.api.RestAdapter")
    def test_api_init_with_config(self, mock_rest_adapter):
        config = {
            "hostname": "testhost",
            "api_key": "key",
            "key_type": 1,
            "ssl_verify": False,
        }
        api = API(config)
        mock_rest_adapter.assert_called_once()
        args, kwargs = mock_rest_adapter.call_args
        self.assertEqual(kwargs["hostname"], "testhost")
        self.assertEqual(kwargs["api_key"], "key")
        self.assertEqual(kwargs["key_type"], 1)
        self.assertFalse(kwargs["ssl_verify"])

    @patch("caredaily.apis.api.RestAdapter")
    def test_api_init_without_config(self, mock_rest_adapter):
        api = API()
        mock_rest_adapter.assert_called_once()

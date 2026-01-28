import unittest
from unittest.mock import MagicMock, call
from caredaily.apis.bot import Execution
from caredaily.models import APIKeyType


class TestExecution(unittest.TestCase):
    """Test suite for Bot Execution API methods"""

    def setUp(self):
        """Set up test fixtures before each test method"""
        self.exec_api = Execution()
        self.mock_adapter = MagicMock()
        self.exec_api.adapter = self.mock_adapter
        # Set up default headers
        self.mock_adapter._headers = {}
        self.mock_adapter._get_headers = MagicMock(return_value={"Content-Type": "application/json"})

    def test_listen_with_all_params(self):
        """Test listen method with all parameters provided"""
        self.mock_adapter.get.return_value = {'result': 'ok'}
        result = self.exec_api.listen(app_instance_id=1, timeout=10, clean_time_ms=100, clean=True)
        
        self.mock_adapter.get.assert_called_once()
        call_args = self.mock_adapter.get.call_args
        self.assertEqual(call_args[0][0], "/deviceio/analytic")
        self.assertEqual(call_args[1]["ep_params"]["appInstanceId"], 1)
        self.assertEqual(call_args[1]["ep_params"]["timeout"], 10)
        self.assertEqual(call_args[1]["ep_params"]["cleanTime"], 100)
        self.assertEqual(call_args[1]["ep_params"]["clean"], True)
        self.assertEqual(result, {'result': 'ok'})

    def test_listen_with_minimal_params(self):
        """Test listen method with only required parameter"""
        self.mock_adapter.get.return_value = {'result': 'ok'}
        result = self.exec_api.listen(app_instance_id=1)
        
        self.mock_adapter.get.assert_called_once()
        call_args = self.mock_adapter.get.call_args
        self.assertEqual(call_args[0][0], "/deviceio/analytic")
        # Verify only appInstanceId is in params (None values filtered out)
        self.assertEqual(call_args[1]["ep_params"]["appInstanceId"], 1)
        self.assertNotIn("timeout", call_args[1]["ep_params"])
        self.assertNotIn("cleanTime", call_args[1]["ep_params"])
        self.assertNotIn("clean", call_args[1]["ep_params"])
        self.assertEqual(result, {'result': 'ok'})

    def test_listen_filters_none_params(self):
        """Test that None parameter values are filtered out"""
        self.mock_adapter.get.return_value = {'result': 'ok'}
        result = self.exec_api.listen(app_instance_id=1, timeout=None, clean_time_ms=None, clean=None)
        
        call_args = self.mock_adapter.get.call_args
        params = call_args[1]["ep_params"]
        # Only appInstanceId should be present
        self.assertEqual(len(params), 1)
        self.assertEqual(params["appInstanceId"], 1)
        self.assertNotIn("timeout", params)
        self.assertNotIn("cleanTime", params)
        self.assertNotIn("clean", params)

    def test_listen_with_timeout_only(self):
        """Test listen method with only timeout parameter"""
        self.mock_adapter.get.return_value = {'result': 'ok'}
        result = self.exec_api.listen(app_instance_id=1, timeout=30)
        
        call_args = self.mock_adapter.get.call_args
        params = call_args[1]["ep_params"]
        self.assertEqual(params["appInstanceId"], 1)
        self.assertEqual(params["timeout"], 30)
        self.assertNotIn("cleanTime", params)
        self.assertNotIn("clean", params)

    def test_listen_with_clean_time_ms_only(self):
        """Test listen method with only clean_time_ms parameter"""
        self.mock_adapter.get.return_value = {'result': 'ok'}
        result = self.exec_api.listen(app_instance_id=1, clean_time_ms=5000)
        
        call_args = self.mock_adapter.get.call_args
        params = call_args[1]["ep_params"]
        self.assertEqual(params["appInstanceId"], 1)
        self.assertEqual(params["cleanTime"], 5000)
        self.assertNotIn("timeout", params)
        self.assertNotIn("clean", params)

    def test_listen_with_clean_flag_only(self):
        """Test listen method with only clean flag"""
        self.mock_adapter.get.return_value = {'result': 'ok'}
        result = self.exec_api.listen(app_instance_id=1, clean=True)
        
        call_args = self.mock_adapter.get.call_args
        params = call_args[1]["ep_params"]
        self.assertEqual(params["appInstanceId"], 1)
        self.assertEqual(params["clean"], True)
        self.assertNotIn("timeout", params)
        self.assertNotIn("cleanTime", params)

    def test_listen_with_clean_false(self):
        """Test listen method with clean flag set to False"""
        self.mock_adapter.get.return_value = {'result': 'ok'}
        result = self.exec_api.listen(app_instance_id=1, clean=False)
        
        call_args = self.mock_adapter.get.call_args
        params = call_args[1]["ep_params"]
        self.assertEqual(params["appInstanceId"], 1)
        self.assertEqual(params["clean"], False)

    def test_listen_with_zero_timeout(self):
        """Test listen method with timeout set to zero (edge case)"""
        self.mock_adapter.get.return_value = {'result': 'ok'}
        result = self.exec_api.listen(app_instance_id=1, timeout=0)
        
        call_args = self.mock_adapter.get.call_args
        params = call_args[1]["ep_params"]
        self.assertEqual(params["timeout"], 0)

    def test_listen_with_zero_clean_time_ms(self):
        """Test listen method with clean_time_ms set to zero (edge case)"""
        self.mock_adapter.get.return_value = {'result': 'ok'}
        result = self.exec_api.listen(app_instance_id=1, clean_time_ms=0)
        
        call_args = self.mock_adapter.get.call_args
        params = call_args[1]["ep_params"]
        self.assertEqual(params["cleanTime"], 0)

    def test_listen_with_large_app_instance_id(self):
        """Test listen method with large app instance ID (boundary case)"""
        self.mock_adapter.get.return_value = {'result': 'ok'}
        large_id = 999999999
        result = self.exec_api.listen(app_instance_id=large_id)
        
        call_args = self.mock_adapter.get.call_args
        params = call_args[1]["ep_params"]
        self.assertEqual(params["appInstanceId"], large_id)

    def test_listen_uses_correct_endpoint(self):
        """Test that listen method calls the correct endpoint"""
        self.mock_adapter.get.return_value = {'result': 'ok'}
        self.exec_api.listen(app_instance_id=1)
        
        call_args = self.mock_adapter.get.call_args
        self.assertEqual(call_args[0][0], "/deviceio/analytic")

    def test_listen_uses_get_method(self):
        """Test that listen method uses GET HTTP method"""
        self.mock_adapter.get.return_value = {'result': 'ok'}
        self.exec_api.listen(app_instance_id=1)
        
        self.mock_adapter.get.assert_called_once()
        # Verify post/put/delete were not called
        self.mock_adapter.post.assert_not_called()
        self.mock_adapter.put.assert_not_called()
        self.mock_adapter.delete.assert_not_called()

    def test_listen_headers_without_admin_key(self):
        """Test listen method headers when ADMIN_KEY is not present"""
        self.mock_adapter.get.return_value = {'result': 'ok'}
        self.mock_adapter._headers = {}
        default_headers = {"Content-Type": "application/json"}
        self.mock_adapter._get_headers.return_value = default_headers

        self.exec_api.listen(app_instance_id=1)

        call_args = self.mock_adapter.get.call_args
        # Should use default headers with None key and USER type
        self.mock_adapter._get_headers.assert_called_with(api_key=None, key_type=APIKeyType.USER)
        self.assertEqual(call_args[1]["ep_headers"], default_headers)

    def test_listen_headers_with_admin_key(self):
        """Test listen method headers when ADMIN_KEY is present (should use USER key type)"""
        self.mock_adapter.get.return_value = {'result': 'ok'}
        admin_key = "admin_key_123"
        self.mock_adapter._headers = {"ADMIN_KEY": admin_key}

        user_headers = {"Content-Type": "application/json", "API_KEY": admin_key}
        self.mock_adapter._get_headers.return_value = user_headers

        self.exec_api.listen(app_instance_id=1)

        # Verify _get_headers was called once with admin_key and USER key type
        self.mock_adapter._get_headers.assert_called_once_with(api_key=admin_key, key_type=APIKeyType.USER)

        # Verify the final headers passed to get() are the user headers
        call_args = self.mock_adapter.get.call_args
        self.assertEqual(call_args[1]["ep_headers"], user_headers)

    def test_listen_returns_adapter_response(self):
        """Test that listen method returns the adapter's response"""
        expected_response = {
            'result': 'ok',
            'data': [{'event': 'test', 'timestamp': 1234567890}]
        }
        self.mock_adapter.get.return_value = expected_response
        
        result = self.exec_api.listen(app_instance_id=1)
        
        self.assertEqual(result, expected_response)

    def test_listen_with_negative_timeout(self):
        """Test listen method with negative timeout value (edge case)"""
        self.mock_adapter.get.return_value = {'result': 'ok'}
        result = self.exec_api.listen(app_instance_id=1, timeout=-1)
        
        call_args = self.mock_adapter.get.call_args
        params = call_args[1]["ep_params"]
        self.assertEqual(params["timeout"], -1)

    def test_listen_with_negative_clean_time_ms(self):
        """Test listen method with negative clean_time_ms value (edge case)"""
        self.mock_adapter.get.return_value = {'result': 'ok'}
        result = self.exec_api.listen(app_instance_id=1, clean_time_ms=-100)
        
        call_args = self.mock_adapter.get.call_args
        params = call_args[1]["ep_params"]
        self.assertEqual(params["cleanTime"], -100)

    def test_listen_with_combination_timeout_and_clean(self):
        """Test listen method with timeout and clean flag combination"""
        self.mock_adapter.get.return_value = {'result': 'ok'}
        result = self.exec_api.listen(app_instance_id=1, timeout=60, clean=True)
        
        call_args = self.mock_adapter.get.call_args
        params = call_args[1]["ep_params"]
        self.assertEqual(params["appInstanceId"], 1)
        self.assertEqual(params["timeout"], 60)
        self.assertEqual(params["clean"], True)
        self.assertNotIn("cleanTime", params)

    def test_listen_with_combination_clean_time_and_clean(self):
        """Test listen method with clean_time_ms and clean flag combination"""
        self.mock_adapter.get.return_value = {'result': 'ok'}
        result = self.exec_api.listen(app_instance_id=1, clean_time_ms=10000, clean=False)
        
        call_args = self.mock_adapter.get.call_args
        params = call_args[1]["ep_params"]
        self.assertEqual(params["appInstanceId"], 1)
        self.assertEqual(params["cleanTime"], 10000)
        self.assertEqual(params["clean"], False)
        self.assertNotIn("timeout", params)

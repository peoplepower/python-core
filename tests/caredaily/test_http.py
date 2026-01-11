import logging
import unittest
from unittest.mock import Mock, patch, MagicMock
from json import JSONDecodeError

from caredaily.http import RestAdapter
from caredaily.models import APIKeyType, Result, ResultCode
from caredaily.exceptions import CareDailyException


class TestRestAdapter(unittest.TestCase):
    def test_init_with_default_values(self):
        adapter = RestAdapter()
        self.assertEqual(adapter.url, "https://app.peoplepowerco.com")
        self.assertEqual(adapter._headers, {"Content-Type": "application/json"})
        self.assertTrue(adapter._ssl_verify)
        self.assertIsNone(adapter._proxies)
        self.assertIsInstance(adapter._logger, logging.Logger)

    def test_init_with_custom_hostname(self):
        adapter = RestAdapter(hostname="custom.example.com")
        self.assertEqual(adapter.url, "https://custom.example.com")

    def test_init_with_user_api_key(self):
        adapter = RestAdapter(api_key="test_key", key_type=APIKeyType.USER)
        self.assertIn("API_KEY", adapter._headers)
        self.assertEqual(adapter._headers["API_KEY"], "test_key")
        self.assertIn("Content-Type", adapter._headers)

    def test_init_with_admin_api_key(self):
        adapter = RestAdapter(api_key="admin_key", key_type=APIKeyType.ADMIN)
        self.assertIn("ADMIN_KEY", adapter._headers)
        self.assertEqual(adapter._headers["ADMIN_KEY"], "admin_key")
        self.assertIn("Content-Type", adapter._headers)

    def test_init_with_analytic_api_key(self):
        adapter = RestAdapter(api_key="analytic_key", key_type=APIKeyType.ANALYTIC)
        self.assertIn("ANALYTIC_API_KEY", adapter._headers)
        self.assertEqual(adapter._headers["ANALYTIC_API_KEY"], "analytic_key")
        self.assertIn("Content-Type", adapter._headers)

    def test_init_with_integer_key_type(self):
        adapter = RestAdapter(api_key="test_key", key_type=0)
        self.assertIn("API_KEY", adapter._headers)
        self.assertEqual(adapter._headers["API_KEY"], "test_key")

    def test_init_with_invalid_key_type(self):
        adapter = RestAdapter(api_key="test_key", key_type="invalid")
        self.assertNotIn("API_KEY", adapter._headers)
        self.assertNotIn("ADMIN_KEY", adapter._headers)
        self.assertNotIn("ANALYTIC_API_KEY", adapter._headers)

    @patch("caredaily.http.requests.packages.urllib3.disable_warnings")
    def test_init_with_ssl_verify_disabled(self, mock_disable_warnings):
        adapter = RestAdapter(ssl_verify=False)
        self.assertFalse(adapter._ssl_verify)
        mock_disable_warnings.assert_called_once()

    def test_init_with_proxies(self):
        proxies = {"http": "http://proxy.example.com:8080"}
        adapter = RestAdapter(proxies=proxies)
        self.assertEqual(adapter._proxies, proxies)

    def test_init_with_custom_logger(self):
        custom_logger = logging.getLogger("custom")
        adapter = RestAdapter(logger=custom_logger)
        self.assertEqual(adapter._logger, custom_logger)

    def test_get_headers_with_no_api_key(self):
        adapter = RestAdapter()
        headers = adapter._get_headers()
        self.assertEqual(headers, {"Content-Type": "application/json"})

    def test_get_headers_with_user_key(self):
        adapter = RestAdapter()
        headers = adapter._get_headers(api_key="user_key", key_type=APIKeyType.USER)
        self.assertEqual(headers["API_KEY"], "user_key")
        self.assertEqual(headers["Content-Type"], "application/json")

    def test_get_headers_with_admin_key(self):
        adapter = RestAdapter()
        headers = adapter._get_headers(api_key="admin_key", key_type=APIKeyType.ADMIN)
        self.assertEqual(headers["ADMIN_KEY"], "admin_key")
        self.assertEqual(headers["Content-Type"], "application/json")

    def test_get_headers_with_analytic_key(self):
        adapter = RestAdapter()
        headers = adapter._get_headers(api_key="analytic_key", key_type=APIKeyType.ANALYTIC)
        self.assertEqual(headers["ANALYTIC_API_KEY"], "analytic_key")
        self.assertEqual(headers["Content-Type"], "application/json")

    @patch("caredaily.http.requests.request")
    def test_get_request(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {"resultCode": 0}
        mock_response.text = '{"resultCode": 0}'
        mock_request.return_value = mock_response

        adapter = RestAdapter()
        result = adapter.get("/test")

        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        self.assertEqual(kwargs["method"], "GET")
        self.assertEqual(kwargs["url"], "https://app.peoplepowerco.com/test")
        self.assertIsInstance(result, Result)

    @patch("caredaily.http.requests.request")
    def test_post_request(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {"resultCode": 0}
        mock_response.text = '{"resultCode": 0}'
        mock_request.return_value = mock_response

        adapter = RestAdapter()
        result = adapter.post("/test", ep_json={"key": "value"})

        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        self.assertEqual(kwargs["method"], "POST")
        self.assertEqual(kwargs["json"], {"key": "value"})
        self.assertIsInstance(result, Result)

    @patch("caredaily.http.requests.request")
    def test_put_request(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {"resultCode": 0}
        mock_response.text = '{"resultCode": 0}'
        mock_request.return_value = mock_response

        adapter = RestAdapter()
        result = adapter.put("/test", ep_json={"key": "value"})

        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        self.assertEqual(kwargs["method"], "PUT")
        self.assertIsInstance(result, Result)

    @patch("caredaily.http.requests.request")
    def test_delete_request(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {"resultCode": 0}
        mock_response.text = '{"resultCode": 0}'
        mock_request.return_value = mock_response

        adapter = RestAdapter()
        result = adapter.delete("/test")

        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        self.assertEqual(kwargs["method"], "DELETE")
        self.assertIsInstance(result, Result)

    @patch("caredaily.http.requests.request")
    def test_request_with_custom_headers(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {"resultCode": 0}
        mock_response.text = '{"resultCode": 0}'
        mock_request.return_value = mock_response

        adapter = RestAdapter()
        custom_headers = {"X-Custom-Header": "value"}
        result = adapter.get("/test", ep_headers=custom_headers)

        args, kwargs = mock_request.call_args
        self.assertIn("X-Custom-Header", kwargs["headers"])
        self.assertEqual(kwargs["headers"]["X-Custom-Header"], "value")
        self.assertIn("Content-Type", kwargs["headers"])

    @patch("caredaily.http.requests.request")
    def test_request_with_params(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {"resultCode": 0}
        mock_response.text = '{"resultCode": 0}'
        mock_request.return_value = mock_response

        adapter = RestAdapter()
        params = {"param1": "value1", "param2": "value2"}
        result = adapter.get("/test", ep_params=params)

        args, kwargs = mock_request.call_args
        self.assertEqual(kwargs["params"], params)

    @patch("caredaily.http.requests.request")
    def test_request_with_data(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {"resultCode": 0}
        mock_response.text = '{"resultCode": 0}'
        mock_request.return_value = mock_response

        adapter = RestAdapter()
        data = "raw data"
        result = adapter.post("/test", ep_data=data)

        args, kwargs = mock_request.call_args
        self.assertEqual(kwargs["data"], data)

    @patch("caredaily.http.requests.request")
    def test_request_exception(self, mock_request):
        import requests
        mock_request.side_effect = requests.exceptions.RequestException("Connection error")

        adapter = RestAdapter()
        with self.assertRaises(CareDailyException) as context:
            adapter.get("/test")

        self.assertEqual(str(context.exception), "Request failed")

    @patch("caredaily.http.requests.request")
    def test_json_response_with_success(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {
            "resultCode": 0,
            "resultCodeMessage": "Success"
        }
        mock_response.text = '{"resultCode": 0, "resultCodeMessage": "Success"}'
        mock_request.return_value = mock_response

        adapter = RestAdapter()
        result = adapter.get("/test")

        self.assertEqual(result.result_code, ResultCode.SUCCESS)
        self.assertIsNotNone(result.data)

    @patch("caredaily.http.requests.request")
    def test_json_response_with_error_code(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {
            "resultCode": 2,
            "resultCodeMessage": "Wrong API key"
        }
        mock_response.text = '{"resultCode": 2, "resultCodeMessage": "Wrong API key"}'
        mock_request.return_value = mock_response

        adapter = RestAdapter()
        with self.assertRaises(CareDailyException) as context:
            adapter.get("/test")

        self.assertIn("2", str(context.exception))
        self.assertIn("Wrong API key", str(context.exception))

    @patch("caredaily.http.requests.request")
    def test_json_response_with_invalid_json(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.side_effect = JSONDecodeError("Invalid JSON", "", 0)
        mock_response.text = "invalid json"
        mock_request.return_value = mock_response

        adapter = RestAdapter()
        with self.assertRaises(CareDailyException) as context:
            adapter.get("/test")

        self.assertEqual(str(context.exception), "Bad JSON response")

    @patch("caredaily.http.requests.request")
    def test_json_response_with_validation_error(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {
            "resultCode": "invalid_code"  # Invalid result code type
        }
        mock_response.text = '{"resultCode": "invalid_code"}'
        mock_request.return_value = mock_response

        adapter = RestAdapter()
        with self.assertRaises(CareDailyException) as context:
            adapter.get("/test")

        self.assertEqual(str(context.exception), "Invalid JSON")

    @patch("caredaily.http.requests.request")
    def test_json_response_with_http_error(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {
            "message": "Bad request"
        }
        mock_response.text = '{"message": "Bad request"}'
        mock_request.return_value = mock_response

        adapter = RestAdapter()
        with self.assertRaises(Exception):
            adapter.get("/test")

    @patch("caredaily.http.requests.request")
    def test_text_response_with_success(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "text/plain"}
        mock_response.text = "Success text"
        mock_request.return_value = mock_response

        adapter = RestAdapter()
        result = adapter.get("/test")

        self.assertIsInstance(result, Result)
        self.assertEqual(result.result_code, ResultCode.SUCCESS)
        self.assertEqual(result.data["text"], "Success text")

    @patch("caredaily.http.requests.request")
    def test_text_response_with_error(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.headers = {"Content-Type": "text/plain"}
        mock_response.text = "Error text"
        mock_request.return_value = mock_response

        adapter = RestAdapter()
        with self.assertRaises(CareDailyException) as context:
            adapter.get("/test")

        self.assertEqual(str(context.exception), "Error text")

    @patch("caredaily.http.requests.request")
    def test_xml_response_with_success(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/xml"}
        mock_response.text = "<xml>Success</xml>"
        mock_request.return_value = mock_response

        adapter = RestAdapter()
        result = adapter.get("/test")

        self.assertIsInstance(result, Result)
        self.assertEqual(result.result_code, ResultCode.SUCCESS)
        self.assertEqual(result.data["text"], "<xml>Success</xml>")

    @patch("caredaily.http.requests.request")
    def test_xml_response_with_error(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.headers = {"Content-Type": "application/xml"}
        mock_response.text = "<error>Server error</error>"
        mock_request.return_value = mock_response

        adapter = RestAdapter()
        with self.assertRaises(CareDailyException) as context:
            adapter.get("/test")

        self.assertEqual(str(context.exception), "<error>Server error</error>")

    @patch("caredaily.http.requests.request")
    def test_unsupported_content_type(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/pdf"}
        mock_response.text = "PDF content"
        mock_request.return_value = mock_response

        adapter = RestAdapter()
        with self.assertRaises(CareDailyException) as context:
            adapter.get("/test")

        self.assertEqual(str(context.exception), "Bad response")

    @patch("caredaily.http.requests.request")
    def test_request_with_ssl_verify(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {"resultCode": 0}
        mock_response.text = '{"resultCode": 0}'
        mock_request.return_value = mock_response

        adapter = RestAdapter(ssl_verify=True)
        result = adapter.get("/test")

        args, kwargs = mock_request.call_args
        self.assertTrue(kwargs["verify"])

    @patch("caredaily.http.requests.request")
    def test_request_with_proxies(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {"resultCode": 0}
        mock_response.text = '{"resultCode": 0}'
        mock_request.return_value = mock_response

        proxies = {"http": "http://proxy.example.com:8080"}
        adapter = RestAdapter(proxies=proxies)
        result = adapter.get("/test")

        args, kwargs = mock_request.call_args
        self.assertEqual(kwargs["proxies"], proxies)

    @patch("caredaily.http.requests.request")
    def test_response_with_result_code_none(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {}
        mock_response.text = '{}'
        mock_request.return_value = mock_response

        adapter = RestAdapter()
        result = adapter.get("/test")

        self.assertIsNone(result.result_code)
        self.assertIsNotNone(result.data)

    @patch("caredaily.http.requests.request")
    def test_response_without_content_type_header(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {"resultCode": 0}
        mock_response.text = '{"resultCode": 0}'
        mock_request.return_value = mock_response

        adapter = RestAdapter()
        result = adapter.get("/test")

        # Should use default Content-Type from headers
        self.assertIsInstance(result, Result)

    @patch("caredaily.http.requests.request")
    def test_logging_on_success(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {"resultCode": 0}
        mock_response.text = '{"resultCode": 0}'
        mock_request.return_value = mock_response

        mock_logger = Mock(spec=logging.Logger)
        adapter = RestAdapter(logger=mock_logger)
        result = adapter.get("/test")

        # Verify logger.debug was called
        self.assertTrue(mock_logger.debug.called)

    @patch("caredaily.http.requests.request")
    def test_logging_on_error(self, mock_request):
        import requests
        mock_request.side_effect = requests.exceptions.RequestException("Connection error")

        mock_logger = Mock(spec=logging.Logger)
        adapter = RestAdapter(logger=mock_logger)

        with self.assertRaises(CareDailyException):
            adapter.get("/test")

        # Verify logger.error was called
        self.assertTrue(mock_logger.error.called)

    @patch("caredaily.http.requests.request")
    def test_all_result_codes(self, mock_request):
        """Test handling of various result codes"""
        test_cases = [
            (1, "INTERNAL_ERROR"),
            (2, "WRONG_API_KEY"),
            (4, "WRONG_DEVICE_ID"),
            (7, "ACCESS_DENIED"),
            (12, "INVALID_CREDENTIALS"),
        ]

        for result_code, message in test_cases:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.headers = {"Content-Type": "application/json"}
            mock_response.json.return_value = {
                "resultCode": result_code,
                "resultCodeMessage": message
            }
            mock_response.text = f'{{"resultCode": {result_code}, "resultCodeMessage": "{message}"}}'
            mock_request.return_value = mock_response

            adapter = RestAdapter()
            with self.assertRaises(CareDailyException) as context:
                adapter.get("/test")

            self.assertIn(str(result_code), str(context.exception))


if __name__ == "__main__":
    unittest.main()

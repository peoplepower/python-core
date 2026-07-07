import json
import unittest
from unittest.mock import MagicMock
from caredaily.apis.app import Authentication
from caredaily.models import APIKeyType, SignatureAlgorithm

class TestAuthentication(unittest.TestCase):
    def setUp(self):
        self.auth = Authentication()
        self.mock_adapter = MagicMock()
        self.mock_adapter._headers = {"API_KEY": "user-key"}
        self.auth.adapter = self.mock_adapter

    def test_login_by_username(self):
        self.mock_adapter.get.return_value = 'login-result'
        result = self.auth.login_by_username('user', password='pw')
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/cloud/json/login')
        self.assertEqual(kwargs['ep_params']['username'], 'user')
        self.assertEqual(kwargs['ep_headers']['PASSWORD'], 'pw')
        self.assertEqual(result, 'login-result')

    def test_login_by_username_with_all_params(self):
        self.mock_adapter.get.return_value = 'login-result'
        result = self.auth.login_by_username(
            'user', password='pw', passcode='123456',
            expiry=3600000, key_type=APIKeyType.USER,
            app_name='test_app', brand='test_brand'
        )
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['username'], 'user')
        self.assertEqual(kwargs['ep_params']['expiry'], 3600000)
        self.assertEqual(kwargs['ep_params']['appName'], 'test_app')
        self.assertEqual(kwargs['ep_headers']['PASSWORD'], 'pw')
        self.assertEqual(kwargs['ep_headers']['passcode'], '123456')
        self.assertEqual(result, 'login-result')

    def test_send_passcode(self):
        self.mock_adapter.get.return_value = 'passcode-result'
        result = self.auth.send_passcode('user@example.com', pref_delivery_type=1, brand='test')
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/cloud/json/passcode')
        self.assertEqual(kwargs['ep_params']['username'], 'user@example.com')
        self.assertEqual(kwargs['ep_params']['prefDeliveryType'], 1)
        self.assertEqual(kwargs['ep_params']['brand'], 'test')
        self.assertEqual(result, 'passcode-result')

    def test_login_by_key(self):
        self.mock_adapter.get.return_value = 'login-key-result'
        result = self.auth.login_by_key('key')
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/cloud/json/loginByKey')
        self.assertEqual(kwargs['ep_headers']['API_KEY'], 'key')
        self.assertEqual(result, 'login-key-result')

    def test_login_by_key_with_params(self):
        self.mock_adapter.get.return_value = 'login-key-result'
        result = self.auth.login_by_key('key', passcode='123456', expiry=3600000)
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_headers']['API_KEY'], 'key')
        self.assertEqual(kwargs['ep_headers']['passcode'], '123456')
        self.assertEqual(kwargs['ep_params']['expiry'], 3600000)
        self.assertEqual(result, 'login-key-result')

    def test_logout(self):
        self.mock_adapter.get.return_value = 'logout-result'
        result = self.auth.logout()
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/cloud/json/logout')
        self.assertEqual(result, 'logout-result')

    def test_create_totp_factor(self):
        self.mock_adapter.post.return_value = 'totp-create-result'
        result = self.auth.create_totp_factor(name='test_factor', issuer='TestApp')
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(args[0], '/cloud/json/totp')
        self.assertEqual(kwargs['ep_params']['name'], 'test_factor')
        self.assertEqual(kwargs['ep_params']['issuer'], 'TestApp')
        self.assertEqual(result, 'totp-create-result')

    def test_create_totp_factor_no_params(self):
        self.mock_adapter.post.return_value = 'totp-create-result'
        result = self.auth.create_totp_factor()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params'], {})
        self.assertEqual(result, 'totp-create-result')

    def test_confirm_totp_factor(self):
        self.mock_adapter.put.return_value = 'totp-confirm-result'
        result = self.auth.confirm_totp_factor(name='test_factor', code='123456')
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/cloud/json/totp')
        self.assertEqual(kwargs['ep_params']['name'], 'test_factor')
        self.assertEqual(kwargs['ep_params']['code'], '123456')
        self.assertEqual(result, 'totp-confirm-result')

    def test_get_totp_factors(self):
        self.mock_adapter.get.return_value = 'totp-factors-result'
        result = self.auth.get_totp_factors()
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/cloud/json/totp')
        self.assertEqual(result, 'totp-factors-result')

    def test_delete_totp_factor(self):
        self.mock_adapter.delete.return_value = 'totp-delete-result'
        result = self.auth.delete_totp_factor(name='test_factor')
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(args[0], '/cloud/json/totp')
        self.assertEqual(kwargs['ep_params']['name'], 'test_factor')
        self.assertEqual(result, 'totp-delete-result')

    def test_get_private_key(self):
        self.mock_adapter.get.return_value = 'private-key-result'
        result = self.auth.get_private_key(app_name='test_app')
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/cloud/json/signatureKey')
        self.assertEqual(kwargs['ep_params']['appName'], 'test_app')
        # v61: authenticated with the user API key; no override for user-key adapters
        self.assertIsNone(kwargs['ep_headers'])
        self.assertEqual(result, 'private-key-result')

    def test_get_private_key_with_admin_key(self):
        self.mock_adapter._headers = {"ADMIN_KEY": "admin-key"}
        self.mock_adapter._get_headers.return_value = {"API_KEY": "admin-key"}
        self.mock_adapter.get.return_value = 'private-key-result'
        result = self.auth.get_private_key(app_name='test_app')
        args, kwargs = self.mock_adapter.get.call_args
        # An admin key must be mapped into the API_KEY header for app endpoints
        self.mock_adapter._get_headers.assert_called_with(
            api_key='admin-key', key_type=APIKeyType.USER,
        )
        # ADMIN_KEY is set to None so requests drops the adapter's base header
        self.assertEqual(
            kwargs['ep_headers'], {"API_KEY": "admin-key", "ADMIN_KEY": None}
        )
        self.assertEqual(result, 'private-key-result')

    def test_get_private_key_end_user(self):
        self.mock_adapter.get.return_value = 'private-key-result'
        result = self.auth.get_private_key(app_name='test_app', end_user=True)
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['endUser'], True)
        self.assertEqual(result, 'private-key-result')

    def test_get_private_key_no_params(self):
        self.mock_adapter.get.return_value = 'private-key-result'
        result = self.auth.get_private_key()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params'], {})
        self.assertEqual(result, 'private-key-result')

    def test_put_public_key(self):
        self.mock_adapter.put.return_value = 'public-key-result'
        result = self.auth.put_public_key(app_name='test_app', public_key='-----BEGIN PUBLIC KEY-----')
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/cloud/json/signatureKey')
        self.assertEqual(kwargs['ep_params']['appName'], 'test_app')
        self.assertEqual(json.loads(kwargs['ep_data'])['publicKey'], '-----BEGIN PUBLIC KEY-----')
        # v61: authenticated with the user API key; no override for user-key adapters
        self.assertIsNone(kwargs['ep_headers'])
        self.assertEqual(result, 'public-key-result')

    def test_put_public_key_end_user(self):
        self.mock_adapter.put.return_value = 'public-key-result'
        result = self.auth.put_public_key(
            app_name='test_app', public_key='-----BEGIN PUBLIC KEY-----', end_user=True
        )
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_params']['endUser'], True)
        self.assertEqual(result, 'public-key-result')

    def test_get_operation_token(self):
        self.mock_adapter.get.return_value = 'token-result'
        result = self.auth.get_operation_token(token_type=1)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/cloud/json/token')
        self.assertEqual(kwargs['ep_params']['type'], 1)
        self.assertEqual(result, 'token-result')

    def test_get_operation_token_no_type(self):
        self.mock_adapter.get.return_value = 'token-result'
        result = self.auth.get_operation_token()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params'], {})
        self.assertEqual(result, 'token-result')

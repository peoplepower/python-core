import unittest
import json
from unittest.mock import MagicMock
from caredaily.apis.app import UserAccounts

class TestUserAccounts(unittest.TestCase):
    def setUp(self):
        self.ua = UserAccounts()
        self.mock_adapter = MagicMock()
        self.ua.adapter = self.mock_adapter

    def test_create_user_account(self):
        self.mock_adapter.post.return_value = 'create-result'
        result = self.ua.create_user_account(
            username='testuser',
            password='password',
            email='test@example.com',
            community_name='test_community'
        )
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/user')
        self.assertEqual(kwargs['ep_params']['username'], 'testuser')
        self.assertEqual(kwargs['ep_params']['email'], 'test@example.com')
        self.assertEqual(kwargs['ep_headers']['PASSWORD'], 'password')
        self.assertEqual(result, 'create-result')

    def test_create_user_account_no_password(self):
        self.mock_adapter.post.return_value = 'create-result'
        result = self.ua.create_user_account(username='testuser')
        args, kwargs = self.mock_adapter.post.call_args
        self.assertIsNone(kwargs.get('ep_headers'))
        self.assertEqual(result, 'create-result')

    def test_get_user_information(self):
        self.mock_adapter.get.return_value = 'user-info-result'
        result = self.ua.get_user_information(user_id=1, organization_id=2)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/user')
        self.assertEqual(kwargs['ep_params']['userId'], 1)
        self.assertEqual(kwargs['ep_params']['organizationId'], 2)
        self.assertEqual(result, 'user-info-result')

    def test_get_user_information_no_params(self):
        self.mock_adapter.get.return_value = 'user-info-result'
        result = self.ua.get_user_information()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params'], {})
        self.assertEqual(result, 'user-info-result')

    def test_update_user(self):
        self.mock_adapter.put.return_value = 'update-result'
        result = self.ua.update_user(
            email='new@example.com',
            username='newuser',
            first_name='John',
            last_name='Doe'
        )
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/user')
        self.assertEqual(kwargs['ep_params']['email'], 'new@example.com')
        self.assertEqual(kwargs['ep_params']['username'], 'newuser')
        self.assertEqual(kwargs['ep_params']['firstName'], 'John')
        self.assertEqual(kwargs['ep_params']['lastName'], 'Doe')
        self.assertEqual(result, 'update-result')

    def test_delete_user(self):
        self.mock_adapter.delete.return_value = 'delete-result'
        result = self.ua.delete_user(user_id=1, send_email=True)
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/user')
        self.assertEqual(kwargs['ep_params']['userId'], 1)
        self.assertEqual(kwargs['ep_params']['sendEmail'], True)
        self.assertEqual(result, 'delete-result')

    def test_delete_user_no_params(self):
        self.mock_adapter.delete.return_value = 'delete-result'
        result = self.ua.delete_user()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(kwargs['ep_params'], {})
        self.assertEqual(result, 'delete-result')

    def test_get_pronouns(self):
        self.mock_adapter.get.return_value = 'pronouns-result'
        result = self.ua.get_pronouns()
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/pronouns')
        self.assertEqual(result, 'pronouns-result')

    def test_send_verification_message(self):
        self.mock_adapter.get.return_value = 'verification-result'
        result = self.ua.send_verification_message(type=1, brand='test_brand')
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/emailVerificationMessage')
        self.assertEqual(kwargs['ep_params']['type'], 1)
        self.assertEqual(kwargs['ep_params']['brand'], 'test_brand')
        self.assertEqual(result, 'verification-result')

    def test_provide_verification_code(self):
        self.mock_adapter.put.return_value = 'verify-result'
        result = self.ua.provide_verification_code(code='123456', type=1)
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/emailVerificationMessage')
        self.assertEqual(kwargs['ep_params']['code'], '123456')
        self.assertEqual(kwargs['ep_params']['type'], 1)
        self.assertEqual(result, 'verify-result')

    def test_put_new_password(self):
        self.mock_adapter.put.return_value = 'password-result'
        result = self.ua.put_new_password(
            new_password='newpass',
            old_password='oldpass',
            passcode='123456'
        )
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/newPassword')
        self.assertEqual(kwargs['ep_headers']['NEW_PASSWORD'], 'newpass')
        self.assertEqual(kwargs['ep_headers']['PASSWORD'], 'oldpass')
        self.assertEqual(kwargs['ep_headers']['passcode'], '123456')
        self.assertEqual(kwargs['ep_json']['oldPassword'], 'oldpass')
        self.assertEqual(kwargs['ep_json']['newPassword'], 'newpass')
        self.assertEqual(result, 'password-result')

    def test_put_new_password_minimal(self):
        self.mock_adapter.put.return_value = 'password-result'
        result = self.ua.put_new_password(new_password='newpass')
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_headers']['NEW_PASSWORD'], 'newpass')
        self.assertNotIn('PASSWORD', kwargs['ep_headers'])
        self.assertEqual(kwargs['ep_json']['newPassword'], 'newpass')
        self.assertEqual(result, 'password-result')

    def test_recover_password(self):
        self.mock_adapter.post.return_value = 'recover-result'
        result = self.ua.recover_password(
            username='testuser',
            email='test@example.com',
            brand='test_brand'
        )
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/recoverPassword')
        self.assertEqual(kwargs['ep_params']['username'], 'testuser')
        self.assertEqual(kwargs['ep_params']['email'], 'test@example.com')
        self.assertEqual(kwargs['ep_params']['brand'], 'test_brand')
        self.assertEqual(result, 'recover-result')

    def test_reset_user_badges(self):
        self.mock_adapter.put.return_value = 'reset-badges-result'
        result = self.ua.reset_user_badges(user_id=1)
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/userBadges')
        self.assertEqual(kwargs['ep_params']['userId'], 1)
        self.assertEqual(result, 'reset-badges-result')

    def test_reset_user_badges_no_user_id(self):
        self.mock_adapter.put.return_value = 'reset-badges-result'
        result = self.ua.reset_user_badges()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_params'], {})
        self.assertEqual(result, 'reset-badges-result')

    def test_get_terms_of_service(self):
        self.mock_adapter.get.return_value = 'terms-result'
        result = self.ua.get_terms_of_service(signature_id=1)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/termsOfServices')
        self.assertEqual(kwargs['ep_params']['signatureId'], 1)
        self.assertEqual(result, 'terms-result')

    def test_get_terms_of_service_no_id(self):
        self.mock_adapter.get.return_value = 'terms-result'
        result = self.ua.get_terms_of_service()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params'], {})
        self.assertEqual(result, 'terms-result')

    def test_put_terms_of_service(self):
        self.mock_adapter.put.return_value = 'sign-terms-result'
        result = self.ua.put_terms_of_service(signature_id=1)
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/termsOfServices/1')
        self.assertEqual(result, 'sign-terms-result')

    def test_put_user_tag(self):
        self.mock_adapter.put.return_value = 'tag-result'
        result = self.ua.put_user_tag(tag='test_tag')
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/usertags/test_tag')
        self.assertEqual(result, 'tag-result')

    def test_delete_user_tag(self):
        self.mock_adapter.delete.return_value = 'delete-tag-result'
        result = self.ua.delete_user_tag(tag='test_tag')
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/usertags/test_tag')
        self.assertEqual(result, 'delete-tag-result')

    def test_put_user_code(self):
        self.mock_adapter.put.return_value = 'code-result'
        result = self.ua.put_user_code(
            name='test_code',
            code='1234',
            location_id=1,
            type=2
        )
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/userCodes')
        self.assertEqual(kwargs['ep_params']['name'], 'test_code')
        self.assertEqual(kwargs['ep_params']['code'], '1234')
        self.assertEqual(kwargs['ep_params']['locationId'], 1)
        self.assertEqual(kwargs['ep_params']['type'], 2)
        self.assertEqual(result, 'code-result')

    def test_get_user_codes(self):
        self.mock_adapter.get.return_value = 'codes-result'
        result = self.ua.get_user_codes()
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/userCodes')
        self.assertEqual(result, 'codes-result')

    def test_delete_user_code(self):
        self.mock_adapter.delete.return_value = 'delete-code-result'
        result = self.ua.delete_user_code(name='test_code', location_id=1)
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/userCodes')
        self.assertEqual(kwargs['ep_params']['name'], 'test_code')
        self.assertEqual(kwargs['ep_params']['locationId'], 1)
        self.assertEqual(result, 'delete-code-result')

    def test_delete_user_code_no_location(self):
        self.mock_adapter.delete.return_value = 'delete-code-result'
        result = self.ua.delete_user_code(name='test_code')
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(kwargs['ep_params']['name'], 'test_code')
        self.assertNotIn('locationId', kwargs['ep_params'])
        self.assertEqual(result, 'delete-code-result')

    def test_get_new_password(self):
        """Test Case ID: TC-UserAccounts-001
        Title: Get New Password (Recover Password)
        Priority: P1
        """
        self.mock_adapter.get.return_value = {'resultCode': 0}
        result = self.ua.get_new_password(username='test@example.com')
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/newPassword')
        self.assertEqual(kwargs['ep_params']['username'], 'test@example.com')
        self.assertEqual(result, {'resultCode': 0})

    def test_get_new_password_with_brand(self):
        """Test Case ID: TC-UserAccounts-002
        Title: Get New Password with Brand Parameter
        Priority: P2
        """
        self.mock_adapter.get.return_value = {'resultCode': 0}
        result = self.ua.get_new_password(username='test@example.com', brand='test_brand')
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['username'], 'test@example.com')
        self.assertEqual(kwargs['ep_params']['brand'], 'test_brand')
        self.assertEqual(result, {'resultCode': 0})

    def test_put_new_password_enhanced(self):
        """Test Case ID: TC-UserAccounts-003
        Title: Put New Password with Enhanced Parameters
        Priority: P1
        """
        self.mock_adapter.put.return_value = {'resultCode': 0}
        result = self.ua.put_new_password(
            new_password='newpass123',
            old_password='oldpass123',
            brand='test_brand',
            strong_password=True,
            keep_key_version=False
        )
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/newPassword')
        self.assertEqual(kwargs['ep_params']['brand'], 'test_brand')
        self.assertEqual(kwargs['ep_params']['strongPassword'], True)
        self.assertEqual(kwargs['ep_params']['keepKeyVersion'], False)
        self.assertEqual(kwargs['ep_headers']['NEW_PASSWORD'], 'newpass123')
        self.assertEqual(kwargs['ep_headers']['PASSWORD'], 'oldpass123')
        self.assertEqual(kwargs['ep_json']['oldPassword'], 'oldpass123')
        self.assertEqual(kwargs['ep_json']['newPassword'], 'newpass123')
        self.assertEqual(result, {'resultCode': 0})

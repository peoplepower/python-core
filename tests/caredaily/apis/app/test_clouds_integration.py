import unittest
import pytest
from unittest.mock import MagicMock
from caredaily.apis.app import CloudsIntegration

class TestCloudsIntegration(unittest.TestCase):
    def setUp(self):
        self.ci = CloudsIntegration()
        self.mock_adapter = MagicMock()
        self.ci.adapter = self.mock_adapter

    def test_get_3rd_party_clouds(self):
        self.mock_adapter.get.return_value = '3rd-party-clouds-result'
        result = self.ci.get_3rd_party_clouds()
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, '3rd-party-clouds-result')

    def test_access_3rd_party_cloud(self):
        cloud_id = 'cloud123'
        credentials = {'key': 'value'}
        self.mock_adapter.post.return_value = 'access-cloud-result'
        result = self.ci.access_3rd_party_cloud(cloud_id=cloud_id, credentials=credentials)
        self.mock_adapter.post.assert_called_once()
        self.assertEqual(result, 'access-cloud-result')

    def test_revoke_access_to_3rd_party_cloud(self):
        cloud_id = 'cloud123'
        self.mock_adapter.delete.return_value = 'revoke-access-result'
        result = self.ci.revoke_access_to_3rd_party_cloud(cloud_id=cloud_id)
        self.mock_adapter.delete.assert_called_once()
        self.assertEqual(result, 'revoke-access-result')

    def test_authorize_3rd_party_client(self):
        client_data = {'clientId': 'client123'}
        self.mock_adapter.post.return_value = 'authorize-client-result'
        result = self.ci.authorize_3rd_party_client(client_data=client_data)
        self.mock_adapter.post.assert_called_once()
        self.assertEqual(result, 'authorize-client-result')

    def test_approve_or_deny_client_authorization(self):
        client_id = 'client123'
        approve = True
        self.mock_adapter.post.return_value = 'approve-deny-result'
        result = self.ci.approve_or_deny_client_authorization(client_id=client_id, approve=approve)
        self.mock_adapter.post.assert_called_once()
        self.assertEqual(result, 'approve-deny-result')

    def test_get_access_token(self):
        client_id = 'client123'
        self.mock_adapter.get.return_value = 'access-token-result'
        result = self.ci.get_access_token(client_id=client_id)
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, 'access-token-result')

    def test_update_oauth_client(self):
        client_id = 'client123'
        client_data = {'name': 'Updated Client'}
        self.mock_adapter.put.return_value = 'update-oauth-result'
        result = self.ci.update_oauth_client(client_id=client_id, client_data=client_data)
        self.mock_adapter.put.assert_called_once()
        self.assertEqual(result, 'update-oauth-result')

    def test_revoke_oauth_client(self):
        client_id = 'client123'
        self.mock_adapter.delete.return_value = 'revoke-oauth-result'
        result = self.ci.revoke_oauth_client(client_id=client_id)
        self.mock_adapter.delete.assert_called_once()
        self.assertEqual(result, 'revoke-oauth-result')

    def test_approve_oauth_authorization(self):
        """Test Case ID: TC-CloudsIntegration-001
        Title: Approve OAuth Authorization
        Priority: P1
        """
        self.mock_adapter.get.return_value = {'resultCode': 0, 'redirectUrl': 'https://example.com'}
        result = self.ci.approve_oauth_authorization(
            approved=True,
            client_id='client123',
            state='state123',
            location_id=456
        )
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/oauth/approve/true')
        self.assertEqual(kwargs['ep_params']['client_id'], 'client123')
        self.assertEqual(kwargs['ep_params']['state'], 'state123')
        self.assertEqual(kwargs['ep_params']['locationId'], 456)
        self.assertEqual(result, {'resultCode': 0, 'redirectUrl': 'https://example.com'})

    def test_approve_oauth_authorization_deny(self):
        """Test Case ID: TC-CloudsIntegration-002
        Title: Deny OAuth Authorization
        Priority: P1
        """
        self.mock_adapter.get.return_value = {'resultCode': 0}
        result = self.ci.approve_oauth_authorization(
            approved=False,
            client_id='client123'
        )
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/oauth/approve/false')
        self.assertEqual(kwargs['ep_params']['client_id'], 'client123')
        self.assertNotIn('state', kwargs['ep_params'])
        self.assertEqual(result, {'resultCode': 0})

    def test_access_3rd_party_cloud_with_all_params(self):
        """Test access_3rd_party_cloud with all optional parameters"""
        cloud_id = 'cloud123'
        credentials = {'key': 'value'}
        location_id = 456
        scope = 'read write'
        brand = 'test_brand'
        self.mock_adapter.post.return_value = 'access-cloud-result'
        result = self.ci.access_3rd_party_cloud(
            cloud_id=cloud_id,
            credentials=credentials,
            location_id=location_id,
            scope=scope,
            brand=brand
        )
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(args[0], f'/espapi/auth/authorize/{cloud_id}')
        self.assertEqual(kwargs['ep_params']['locationId'], location_id)
        self.assertEqual(kwargs['ep_params']['scope'], scope)
        self.assertEqual(kwargs['ep_params']['brand'], brand)
        self.assertEqual(kwargs['ep_json'], credentials)
        self.assertEqual(result, 'access-cloud-result')

    def test_access_3rd_party_cloud_no_credentials(self):
        """Test access_3rd_party_cloud without credentials"""
        cloud_id = 'cloud123'
        self.mock_adapter.post.return_value = 'access-cloud-result'
        result = self.ci.access_3rd_party_cloud(cloud_id=cloud_id)
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_json'], None)

    def test_authorize_3rd_party_cloud_no_params(self):
        """Test authorize_3rd_party_cloud with only required parameters"""
        app_id = 123
        location_id = 456
        self.mock_adapter.get.return_value = 'authorize-result'
        result = self.ci.authorize_3rd_party_cloud(app_id=app_id, location_id=location_id)
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], f'/espapi/auth/authorize/{app_id}')
        self.assertEqual(kwargs['ep_params']['locationId'], location_id)
        self.assertEqual(result, 'authorize-result')

    def test_authorize_3rd_party_cloud_with_all_params(self):
        """Test authorize_3rd_party_cloud with all optional parameters"""
        app_id = 123
        location_id = 456
        scope = 'read'
        brand = 'test_brand'
        self.mock_adapter.get.return_value = 'authorize-result'
        result = self.ci.authorize_3rd_party_cloud(
            app_id=app_id,
            location_id=location_id,
            scope=scope,
            brand=brand
        )
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['locationId'], location_id)
        self.assertEqual(kwargs['ep_params']['scope'], scope)
        self.assertEqual(kwargs['ep_params']['brand'], brand)
        self.assertEqual(result, 'authorize-result')

    def test_authorize_3rd_party_client_with_brand(self):
        """Test authorize_3rd_party_client with brand parameter"""
        client_data = {'clientId': 'client123', 'response_type': 'code'}
        brand = 'test_brand'
        self.mock_adapter.post.return_value = 'authorize-client-result'
        result = self.ci.authorize_3rd_party_client(client_data=client_data, brand=brand)
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(args[0], '/espapi/oauth/authorize')
        self.assertEqual(kwargs['ep_params']['brand'], brand)
        self.assertEqual(kwargs['ep_params']['clientId'], 'client123')
        self.assertEqual(result, 'authorize-client-result')

    def test_authorize_3rd_party_client_get_no_optional_params(self):
        """Test authorize_3rd_party_client_get with only required parameters"""
        brand = 'test_brand'
        client_id = 'client123'
        response_type = 'code'
        self.mock_adapter.get.return_value = 'authorize-get-result'
        result = self.ci.authorize_3rd_party_client_get(
            brand=brand,
            client_id=client_id,
            response_type=response_type
        )
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], f'/espapi/oauth/authorize/{brand}')
        self.assertEqual(kwargs['ep_params']['client_id'], client_id)
        self.assertEqual(kwargs['ep_params']['response_type'], response_type)
        self.assertNotIn('state', kwargs['ep_params'])
        self.assertEqual(result, 'authorize-get-result')

    def test_authorize_3rd_party_client_get_with_all_params(self):
        """Test authorize_3rd_party_client_get with all optional parameters"""
        brand = 'test_brand'
        client_id = 'client123'
        response_type = 'code'
        state = 'state123'
        redirect_uri = 'https://example.com/callback'
        scope = 'read write'
        self.mock_adapter.get.return_value = 'authorize-get-result'
        result = self.ci.authorize_3rd_party_client_get(
            brand=brand,
            client_id=client_id,
            response_type=response_type,
            state=state,
            redirect_uri=redirect_uri,
            scope=scope
        )
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['state'], state)
        self.assertEqual(kwargs['ep_params']['redirect_uri'], redirect_uri)
        self.assertEqual(kwargs['ep_params']['scope'], scope)
        self.assertEqual(result, 'authorize-get-result')

    def test_approve_or_deny_client_authorization_with_all_params(self):
        """Test approve_or_deny_client_authorization with all optional parameters"""
        client_id = 'client123'
        approve = True
        state = 'state123'
        response_type = 'code'
        location_id = 456
        brand = 'test_brand'
        self.mock_adapter.post.return_value = 'approve-deny-result'
        result = self.ci.approve_or_deny_client_authorization(
            client_id=client_id,
            approve=approve,
            state=state,
            response_type=response_type,
            location_id=location_id,
            brand=brand
        )
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(args[0], '/espapi/oauth/approve/true')
        self.assertEqual(kwargs['ep_params']['client_id'], client_id)
        self.assertEqual(kwargs['ep_params']['state'], state)
        self.assertEqual(kwargs['ep_params']['response_type'], response_type)
        self.assertEqual(kwargs['ep_params']['locationId'], location_id)
        self.assertEqual(kwargs['ep_params']['brand'], brand)
        self.assertEqual(result, 'approve-deny-result')

    def test_approve_or_deny_authorization_get_approve(self):
        """Test approve_or_deny_authorization_get with approve=True"""
        approved = True
        client_id = 'client123'
        state = 'state123'
        response_type = 'code'
        location_id = 456
        brand = 'test_brand'
        self.mock_adapter.get.return_value = 'approve-get-result'
        result = self.ci.approve_or_deny_authorization_get(
            approved=approved,
            client_id=client_id,
            state=state,
            response_type=response_type,
            location_id=location_id,
            brand=brand
        )
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/oauth/approve/true')
        self.assertEqual(kwargs['ep_params']['client_id'], client_id)
        self.assertEqual(kwargs['ep_params']['state'], state)
        self.assertEqual(kwargs['ep_params']['response_type'], response_type)
        self.assertEqual(kwargs['ep_params']['locationId'], location_id)
        self.assertEqual(kwargs['ep_params']['brand'], brand)
        self.assertEqual(result, 'approve-get-result')

    def test_approve_or_deny_authorization_get_deny(self):
        """Test approve_or_deny_authorization_get with approve=False"""
        approved = False
        client_id = 'client123'
        self.mock_adapter.get.return_value = 'deny-get-result'
        result = self.ci.approve_or_deny_authorization_get(
            approved=approved,
            client_id=client_id
        )
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/oauth/approve/false')
        self.assertEqual(kwargs['ep_params']['client_id'], client_id)
        self.assertNotIn('state', kwargs['ep_params'])
        self.assertEqual(result, 'deny-get-result')

    def test_get_access_token_with_code(self):
        """Test get_access_token with authorization code"""
        client_id = 'client123'
        code = 'auth_code_123'
        client_secret = 'secret123'
        self.mock_adapter.get.return_value = 'access-token-result'
        result = self.ci.get_access_token(
            client_id=client_id,
            code=code,
            client_secret=client_secret
        )
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/oauth/token')
        self.assertEqual(kwargs['ep_params']['client_id'], client_id)
        self.assertEqual(kwargs['ep_params']['code'], code)
        self.assertEqual(kwargs['ep_params']['client_secret'], client_secret)
        self.assertEqual(result, 'access-token-result')

    def test_get_access_token_with_refresh_token(self):
        """Test get_access_token with refresh token"""
        client_id = 'client123'
        refresh_token = 'refresh_token_123'
        self.mock_adapter.get.return_value = 'access-token-result'
        result = self.ci.get_access_token(
            client_id=client_id,
            refresh_token=refresh_token
        )
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['refresh_token'], refresh_token)
        self.assertEqual(result, 'access-token-result')

    def test_get_access_token_post_no_optional_params(self):
        """Test get_access_token_post with only required client_id"""
        client_id = 'client123'
        self.mock_adapter.post.return_value = 'access-token-post-result'
        result = self.ci.get_access_token_post(client_id=client_id)
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(args[0], '/espapi/oauth/token')
        self.assertEqual(kwargs['ep_params']['client_id'], client_id)
        self.assertNotIn('code', kwargs['ep_params'])
        self.assertEqual(result, 'access-token-post-result')

    def test_get_access_token_post_with_code(self):
        """Test get_access_token_post with authorization code"""
        client_id = 'client123'
        code = 'auth_code_123'
        client_secret = 'secret123'
        self.mock_adapter.post.return_value = 'access-token-post-result'
        result = self.ci.get_access_token_post(
            client_id=client_id,
            code=code,
            client_secret=client_secret
        )
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['code'], code)
        self.assertEqual(kwargs['ep_params']['client_secret'], client_secret)
        self.assertEqual(result, 'access-token-post-result')

    def test_get_access_token_post_with_refresh_token(self):
        """Test get_access_token_post with refresh token"""
        client_id = 'client123'
        refresh_token = 'refresh_token_123'
        self.mock_adapter.post.return_value = 'access-token-post-result'
        result = self.ci.get_access_token_post(
            client_id=client_id,
            refresh_token=refresh_token
        )
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['refresh_token'], refresh_token)
        self.assertEqual(result, 'access-token-post-result')

    def test_get_access_token_post_with_grant_type(self):
        """Test get_access_token_post with grant_type"""
        client_id = 'client123'
        grant_type = 'client_credentials'
        self.mock_adapter.post.return_value = 'access-token-post-result'
        result = self.ci.get_access_token_post(
            client_id=client_id,
            grant_type=grant_type
        )
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['grant_type'], grant_type)
        self.assertEqual(result, 'access-token-post-result')

    def test_update_oauth_client_with_location_id(self):
        """Test update_oauth_client with location_id"""
        client_id = 'client123'
        client_data = {'name': 'Updated Client', 'devices': []}
        location_id = 456
        self.mock_adapter.put.return_value = 'update-oauth-result'
        result = self.ci.update_oauth_client(
            client_id=client_id,
            client_data=client_data,
            location_id=location_id
        )
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/authClient')
        self.assertEqual(kwargs['ep_params']['clientId'], client_id)
        self.assertEqual(kwargs['ep_params']['locationId'], location_id)
        self.assertEqual(kwargs['ep_json'], client_data)
        self.assertEqual(result, 'update-oauth-result')

    def test_create_oauth_client_no_location_id(self):
        """Test create_oauth_client without location_id"""
        client_data = {'name': 'New Client', 'devices': []}
        self.mock_adapter.post.return_value = 'create-oauth-result'
        result = self.ci.create_oauth_client(client_data=client_data)
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/authClient')
        self.assertEqual(kwargs['ep_params'], None)
        self.assertEqual(kwargs['ep_json'], client_data)
        self.assertEqual(result, 'create-oauth-result')

    def test_create_oauth_client_with_location_id(self):
        """Test create_oauth_client with location_id"""
        client_data = {'name': 'New Client', 'devices': []}
        location_id = 456
        self.mock_adapter.post.return_value = 'create-oauth-result'
        result = self.ci.create_oauth_client(
            client_data=client_data,
            location_id=location_id
        )
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['locationId'], location_id)
        self.assertEqual(result, 'create-oauth-result')

    def test_revoke_access_to_3rd_party_cloud_with_location_id(self):
        """Test revoke_access_to_3rd_party_cloud with location_id"""
        cloud_id = 'cloud123'
        location_id = 456
        self.mock_adapter.delete.return_value = 'revoke-access-result'
        result = self.ci.revoke_access_to_3rd_party_cloud(
            cloud_id=cloud_id,
            location_id=location_id
        )
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(args[0], f'/espapi/cloud/json/authorizations/{cloud_id}')
        self.assertEqual(kwargs['ep_params']['locationId'], location_id)
        self.assertEqual(result, 'revoke-access-result')

    def test_revoke_oauth_client_with_user_and_location(self):
        """Test revoke_oauth_client with user_id and location_id"""
        client_id = 'client123'
        user_id = 789
        location_id = 456
        self.mock_adapter.delete.return_value = 'revoke-oauth-result'
        result = self.ci.revoke_oauth_client(
            client_id=client_id,
            user_id=user_id,
            location_id=location_id
        )
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/authClient')
        self.assertEqual(kwargs['ep_params']['clientId'], client_id)
        self.assertEqual(kwargs['ep_params']['userId'], user_id)
        self.assertEqual(kwargs['ep_params']['locationId'], location_id)
        self.assertEqual(result, 'revoke-oauth-result')

import unittest
from unittest.mock import MagicMock

from caredaily.apis.admin import Users
from caredaily.models import APIKeyType


class TestUsers(unittest.TestCase):
    def setUp(self):
        self.users = Users()
        self.mock_adapter = MagicMock()
        self.users.adapter = self.mock_adapter
        self.mock_adapter._headers = {'ADMIN_KEY': 'admin_key', 'USER_KEY': 'user_key'}
        self.mock_adapter._get_headers = MagicMock(return_value={'API_KEY': 'admin_key'})

    def test_get_users(self):
        self.mock_adapter.get.return_value = 'users-result'
        result = self.users.get_users(
            organization_id=1,
            location_id=2,
            search_by='test',
            limit=10
        )
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/admin/json/users')
        self.assertEqual(kwargs['ep_params']['organizationId'], 1)
        self.assertEqual(kwargs['ep_params']['locationId'], 2)
        self.assertEqual(kwargs['ep_params']['searchBy'], 'test')
        self.assertEqual(kwargs['ep_params']['limit'], 10)
        self.mock_adapter._get_headers.assert_called_once_with(api_key='admin_key', key_type=APIKeyType.USER)
        self.assertEqual(result, 'users-result')

    def test_get_users_minimal(self):
        self.mock_adapter.get.return_value = 'users-result'
        result = self.users.get_users()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params'], {})
        self.assertEqual(result, 'users-result')

    def test_get_users_by_user_id(self):
        self.mock_adapter.get.return_value = 'users-result'
        result = self.users.get_users(organization_id=1, user_id=42)
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/admin/json/users')
        self.assertEqual(kwargs['ep_params']['userId'], 42)
        self.assertEqual(result, 'users-result')

    def test_get_roles(self):
        self.mock_adapter.get.return_value = 'roles-result'
        result = self.users.get_roles()
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/admin/json/roles')
        self.mock_adapter._get_headers.assert_called_once_with(api_key='admin_key', key_type=APIKeyType.USER)
        self.assertEqual(result, 'roles-result')

    def test_grant_user_role(self):
        self.mock_adapter.put.return_value = 'grant-role-result'
        result = self.users.grant_user_role(user_id=1, role_id=2)
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/espapi/admin/json/users/1/roles/2')
        self.mock_adapter._get_headers.assert_called_once_with(api_key='admin_key', key_type=APIKeyType.USER)
        self.assertEqual(result, 'grant-role-result')

    def test_revoke_user_role(self):
        self.mock_adapter.delete.return_value = 'revoke-role-result'
        result = self.users.revoke_user_role(user_id=1)
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(args[0], '/espapi/admin/json/users/1/roles')
        self.mock_adapter._get_headers.assert_called_once_with(api_key='admin_key', key_type=APIKeyType.USER)
        self.assertEqual(result, 'revoke-role-result')

    def test_get_organization_admins(self):
        self.mock_adapter.get.return_value = 'admins-result'
        result = self.users.get_organization_admins(organization_id=1, parents=True)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/admin/json/organizations/1/admins')
        self.assertEqual(kwargs['ep_params']['parents'], True)
        self.mock_adapter._get_headers.assert_called_once_with(api_key='admin_key', key_type=APIKeyType.USER)
        self.assertEqual(result, 'admins-result')

    def test_get_organization_admins_no_parents(self):
        self.mock_adapter.get.return_value = 'admins-result'
        result = self.users.get_organization_admins(organization_id=1)
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params'], {})
        self.assertEqual(result, 'admins-result')

    def test_add_organization_admin(self):
        self.mock_adapter.put.return_value = 'add-admin-result'
        result = self.users.add_organization_admin(organization_id=1, user_id=2, brand='test_brand')
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/espapi/admin/json/organizations/1/admins/2')
        self.assertEqual(kwargs['ep_params']['brand'], 'test_brand')
        self.mock_adapter._get_headers.assert_called_once_with(api_key='admin_key', key_type=APIKeyType.USER)
        self.assertEqual(result, 'add-admin-result')

    def test_add_organization_admin_no_brand(self):
        self.mock_adapter.put.return_value = 'add-admin-result'
        result = self.users.add_organization_admin(organization_id=1, user_id=2)
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_params'], {})
        self.assertEqual(result, 'add-admin-result')

    def test_remove_organization_admin(self):
        self.mock_adapter.delete.return_value = 'remove-admin-result'
        result = self.users.remove_organization_admin(organization_id=1, user_id=2)
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(args[0], '/espapi/admin/json/organizations/1/admins/2')
        self.mock_adapter._get_headers.assert_called_once_with(api_key='admin_key', key_type=APIKeyType.USER)
        self.assertEqual(result, 'remove-admin-result')

    def test_get_notification_groups(self):
        self.mock_adapter.get.return_value = 'notification-groups-result'
        result = self.users.get_notification_groups(organization_id=1)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/admin/json/organizations/1/notificationGroups')
        self.assertIsNone(kwargs['ep_params'])
        self.mock_adapter._get_headers.assert_called_once_with(api_key='admin_key', key_type=APIKeyType.USER)
        self.assertEqual(result, 'notification-groups-result')

    def test_get_notification_groups_by_group_id(self):
        self.mock_adapter.get.return_value = 'notification-groups-result'
        result = self.users.get_notification_groups(organization_id=1, group_id=123)
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/admin/json/organizations/1/notificationGroups')
        self.assertEqual(kwargs['ep_params']['groupId'], 123)
        self.assertEqual(result, 'notification-groups-result')

    def test_create_notification_group(self):
        self.mock_adapter.post.return_value = 'create-group-result'
        result = self.users.create_notification_group(
            organization_id=1,
            name='Managers',
            category=1,
            description='Manager group',
            default_group=True,
            location_tag='tag1',
        )
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(args[0], '/espapi/admin/json/organizations/1/notificationGroups')
        self.assertEqual(kwargs['ep_json']['group']['name'], 'Managers')
        self.assertEqual(kwargs['ep_json']['group']['category'], 1)
        self.assertEqual(kwargs['ep_json']['group']['description'], 'Manager group')
        self.assertTrue(kwargs['ep_json']['group']['defaultGroup'])
        self.assertEqual(kwargs['ep_json']['group']['locationTag'], 'tag1')
        self.assertNotIn('groupId', kwargs['ep_json']['group'])
        self.mock_adapter._get_headers.assert_called_once_with(api_key='admin_key', key_type=APIKeyType.USER)
        self.assertEqual(result, 'create-group-result')

    def test_create_notification_group_update_existing(self):
        self.mock_adapter.post.return_value = 'update-group-result'
        result = self.users.create_notification_group(
            organization_id=1,
            group_id=123,
            name='Managers',
        )
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_json']['group']['groupId'], 123)
        self.assertEqual(kwargs['ep_json']['group']['name'], 'Managers')
        self.assertEqual(result, 'update-group-result')

    def test_delete_notification_group(self):
        self.mock_adapter.delete.return_value = 'delete-group-result'
        result = self.users.delete_notification_group(organization_id=1, group_id=123)
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(args[0], '/espapi/admin/json/organizations/1/notificationGroups')
        self.assertEqual(kwargs['ep_params']['groupId'], 123)
        self.mock_adapter._get_headers.assert_called_once_with(api_key='admin_key', key_type=APIKeyType.USER)
        self.assertEqual(result, 'delete-group-result')

    def test_update_notification_users(self):
        self.mock_adapter.put.return_value = 'update-notification-result'
        users = [
            {'userId': 2, 'groupId': 123},
            {'userId': 3, 'groupId': 123, 'delete': True},
        ]
        result = self.users.update_notification_users(organization_id=1, users=users)
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/espapi/admin/json/organizations/1/notificationUsers')
        self.assertEqual(kwargs['ep_json'], {'users': users})
        self.mock_adapter._get_headers.assert_called_once_with(api_key='admin_key', key_type=APIKeyType.USER)
        self.assertEqual(result, 'update-notification-result')

    def test_get_notification_assignments(self):
        self.mock_adapter.get.return_value = 'notification-assignments-result'
        result = self.users.get_notification_assignments(organization_id=1)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/admin/json/organizations/1/notificationAssignments')
        self.mock_adapter._get_headers.assert_called_once_with(api_key='admin_key', key_type=APIKeyType.USER)
        self.assertEqual(result, 'notification-assignments-result')

    def test_update_notification_assignments(self):
        self.mock_adapter.put.return_value = 'update-assignments-result'
        groups = [
            {'notificationId': 1, 'groupId': 456},
            {'notificationId': 2, 'groupId': 789, 'delete': True},
        ]
        result = self.users.update_notification_assignments(organization_id=1, groups=groups)
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/espapi/admin/json/organizations/1/notificationAssignments')
        self.assertEqual(kwargs['ep_json'], {'groups': groups})
        self.mock_adapter._get_headers.assert_called_once_with(api_key='admin_key', key_type=APIKeyType.USER)
        self.assertEqual(result, 'update-assignments-result')

import unittest
from unittest.mock import MagicMock

from caredaily.apis.admin import Users


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
        self.mock_adapter._get_headers.assert_called_once_with({'API_KEY': 'admin_key'})
        self.assertEqual(result, 'users-result')

    def test_get_users_minimal(self):
        self.mock_adapter.get.return_value = 'users-result'
        result = self.users.get_users()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params'], {})
        self.assertEqual(result, 'users-result')

    def test_get_roles(self):
        self.mock_adapter.get.return_value = 'roles-result'
        result = self.users.get_roles()
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/admin/json/roles')
        self.mock_adapter._get_headers.assert_called_once_with({'API_KEY': 'admin_key'})
        self.assertEqual(result, 'roles-result')

    def test_grant_user_role(self):
        self.mock_adapter.put.return_value = 'grant-role-result'
        result = self.users.grant_user_role(user_id=1, role_id=2)
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/espapi/admin/json/users/1/roles/2')
        self.mock_adapter._get_headers.assert_called_once_with({'API_KEY': 'admin_key'})
        self.assertEqual(result, 'grant-role-result')

    def test_revoke_user_role(self):
        self.mock_adapter.delete.return_value = 'revoke-role-result'
        result = self.users.revoke_user_role(user_id=1)
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(args[0], '/espapi/admin/json/users/1/roles')
        self.mock_adapter._get_headers.assert_called_once_with({'API_KEY': 'admin_key'})
        self.assertEqual(result, 'revoke-role-result')

    def test_get_organization_admins(self):
        self.mock_adapter.get.return_value = 'admins-result'
        result = self.users.get_organization_admins(organization_id=1, parents=True)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/admin/json/organizations/1/admins')
        self.assertEqual(kwargs['ep_params']['parents'], True)
        self.mock_adapter._get_headers.assert_called_once_with({'API_KEY': 'admin_key'})
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
        self.mock_adapter._get_headers.assert_called_once_with({'API_KEY': 'admin_key'})
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
        self.mock_adapter._get_headers.assert_called_once_with({'API_KEY': 'admin_key'})
        self.assertEqual(result, 'remove-admin-result')

    def test_get_notification_users(self):
        self.mock_adapter.get.return_value = 'notification-users-result'
        result = self.users.get_notification_users(organization_id=1)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/admin/json/organizations/1/notificationUsers')
        self.mock_adapter._get_headers.assert_called_once_with({'API_KEY': 'admin_key'})
        self.assertEqual(result, 'notification-users-result')

    def test_update_notification_user(self):
        self.mock_adapter.put.return_value = 'update-notification-result'
        result = self.users.update_notification_user(
            organization_id=1,
            user_id=2,
            add_category=1,
            delete_category=2
        )
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/espapi/admin/json/organizations/1/notificationUsers')
        self.assertEqual(kwargs['ep_params']['userId'], 2)
        self.assertEqual(kwargs['ep_params']['addCategory'], 1)
        self.assertEqual(kwargs['ep_params']['deleteCategory'], 2)
        self.mock_adapter._get_headers.assert_called_once_with({'API_KEY': 'admin_key'})
        self.assertEqual(result, 'update-notification-result')

    def test_update_notification_user_partial(self):
        self.mock_adapter.put.return_value = 'update-result'
        result = self.users.update_notification_user(organization_id=1, user_id=2, add_category=1)
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_params']['userId'], 2)
        self.assertEqual(kwargs['ep_params']['addCategory'], 1)
        self.assertNotIn('deleteCategory', kwargs['ep_params'])
        self.assertEqual(result, 'update-result')

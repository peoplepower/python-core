import unittest
from unittest.mock import MagicMock

from caredaily.apis.admin import UserGroups
from caredaily.models import APIKeyType


class TestUserGroups(unittest.TestCase):
    def setUp(self):
        self.user_groups = UserGroups()
        self.mock_adapter = MagicMock()
        self.user_groups.adapter = self.mock_adapter
        self.mock_adapter._headers = {'ADMIN_KEY': 'admin_key'}
        self.mock_adapter._get_headers = MagicMock(return_value={'API_KEY': 'admin_key'})

    def test_get_user_groups(self):
        self.mock_adapter.get.return_value = 'groups-result'
        result = self.user_groups.get_user_groups(organization_id=1, group_id=2)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/admin/json/userGroups')
        self.assertEqual(kwargs['ep_params']['organizationId'], 1)
        self.assertEqual(kwargs['ep_params']['groupId'], 2)
        self.mock_adapter._get_headers.assert_called_once_with(api_key='admin_key', key_type=APIKeyType.USER)
        self.assertEqual(result, 'groups-result')

    def test_get_user_groups_no_params(self):
        self.mock_adapter.get.return_value = 'groups-result'
        result = self.user_groups.get_user_groups()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params'], {})
        self.assertEqual(result, 'groups-result')

    def test_create_user_group(self):
        group_data = {'name': 'Test Group'}
        self.mock_adapter.post.return_value = 'create-result'
        result = self.user_groups.create_user_group(group_data=group_data)
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(args[0], '/espapi/admin/json/userGroups')
        self.assertEqual(kwargs['ep_json'], group_data)
        self.mock_adapter._get_headers.assert_called_once_with(api_key='admin_key', key_type=APIKeyType.USER)
        self.assertEqual(result, 'create-result')

    def test_update_user_group(self):
        group_data = {'name': 'Updated Group'}
        self.mock_adapter.put.return_value = 'update-result'
        result = self.user_groups.update_user_group(group_id=1, group_data=group_data)
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/espapi/admin/json/userGroups')
        self.assertEqual(kwargs['ep_params']['groupId'], 1)
        self.assertEqual(kwargs['ep_json'], group_data)
        self.mock_adapter._get_headers.assert_called_once_with(api_key='admin_key', key_type=APIKeyType.USER)
        self.assertEqual(result, 'update-result')

    def test_delete_user_group(self):
        self.mock_adapter.delete.return_value = 'delete-result'
        result = self.user_groups.delete_user_group(group_id=1)
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(args[0], '/espapi/admin/json/userGroups')
        self.assertEqual(kwargs['ep_params']['groupId'], 1)
        self.mock_adapter._get_headers.assert_called_once_with(api_key='admin_key', key_type=APIKeyType.USER)
        self.assertEqual(result, 'delete-result')

    def test_add_user_group_member(self):
        self.mock_adapter.post.return_value = 'add-member-result'
        result = self.user_groups.add_user_group_member(group_id=1, user_id=2)
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(args[0], '/espapi/admin/json/userGroups/members')
        self.assertEqual(kwargs['ep_params']['groupId'], 1)
        self.assertEqual(kwargs['ep_params']['userId'], 2)
        self.mock_adapter._get_headers.assert_called_once_with(api_key='admin_key', key_type=APIKeyType.USER)
        self.assertEqual(result, 'add-member-result')

    def test_remove_user_group_member(self):
        self.mock_adapter.delete.return_value = 'remove-member-result'
        result = self.user_groups.remove_user_group_member(group_id=1, user_id=2)
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(args[0], '/espapi/admin/json/userGroups/members')
        self.assertEqual(kwargs['ep_params']['groupId'], 1)
        self.assertEqual(kwargs['ep_params']['userId'], 2)
        self.mock_adapter._get_headers.assert_called_once_with(api_key='admin_key', key_type=APIKeyType.USER)
        self.assertEqual(result, 'remove-member-result')

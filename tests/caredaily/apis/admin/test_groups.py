import unittest
from unittest.mock import MagicMock

from caredaily.apis.admin import Groups


class TestGroups(unittest.TestCase):
    def setUp(self):
        self.groups = Groups()
        self.mock_adapter = MagicMock()
        self.groups.adapter = self.mock_adapter
        self.mock_adapter._headers = {'ADMIN_KEY': 'admin_key'}
        self.mock_adapter._get_headers = MagicMock(return_value={'API_KEY': 'admin_key'})

    def test_create_organization_group_success(self):
        group_data = {'group': {'name': 'Test Group'}}
        self.mock_adapter.post.return_value = {'groupId': 1}
        result = self.groups.create_organization_group(
            organization_id=123,
            group_data=group_data
        )
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_json'], group_data)
        self.assertEqual(result, {'groupId': 1})

    def test_get_organization_groups_success(self):
        self.mock_adapter.get.return_value = {'groups': []}
        result = self.groups.get_organization_groups(organization_id=123)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params'], {})
        self.assertEqual(result, {'groups': []})

    def test_get_organization_groups_with_group_id(self):
        self.mock_adapter.get.return_value = {'group': {}}
        self.groups.get_organization_groups(organization_id=123, group_id=5)
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['groupId'], 5)

    def test_edit_organization_group_success(self):
        group_data = {'group': {'name': 'Updated Group'}}
        self.mock_adapter.put.return_value = {'status': 'ok'}
        result = self.groups.edit_organization_group(
            organization_id=123,
            group_id=1,
            group_data=group_data
        )
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_json'], group_data)
        self.assertEqual(result, {'status': 'ok'})

    def test_remove_organization_group_success(self):
        self.mock_adapter.delete.return_value = {'status': 'ok'}
        result = self.groups.remove_organization_group(
            organization_id=123,
            group_id=1
        )
        self.mock_adapter.delete.assert_called_once()
        self.assertEqual(result, {'status': 'ok'})

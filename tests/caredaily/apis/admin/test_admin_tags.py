import unittest
from unittest.mock import MagicMock

from caredaily.apis.admin import Tags


class TestTags(unittest.TestCase):
    def setUp(self):
        self.tags = Tags()
        self.mock_adapter = MagicMock()
        self.tags.adapter = self.mock_adapter
        self.mock_adapter._headers = {'ADMIN_KEY': 'admin_key'}
        self.mock_adapter._get_headers = MagicMock(return_value={'API_KEY': 'admin_key'})

    def test_get_popular_tags_success(self):
        self.mock_adapter.get.return_value = {'tags': [{'tag': 'sensor', 'count': 10}]}
        result = self.tags.get_popular_tags(
            organization_id=123,
            tag_type=1
        )
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['type'], 1)
        self.assertEqual(result, {'tags': [{'tag': 'sensor', 'count': 10}]})

    def test_get_popular_tags_with_category_and_limit(self):
        self.mock_adapter.get.return_value = {'tags': []}
        self.tags.get_popular_tags(
            organization_id=123,
            tag_type=1,
            category=2,
            limit=50
        )
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['type'], 1)
        self.assertEqual(kwargs['ep_params']['category'], 2)
        self.assertEqual(kwargs['ep_params']['limit'], 50)

    def test_get_popular_tags_no_optional_params(self):
        self.mock_adapter.get.return_value = {'tags': []}
        self.tags.get_popular_tags(organization_id=123, tag_type=1)
        args, kwargs = self.mock_adapter.get.call_args
        self.assertNotIn('category', kwargs['ep_params'])
        self.assertNotIn('limit', kwargs['ep_params'])

    def test_apply_tags_success(self):
        tags_data = [
            {'type': 1, 'id': '123', 'tag': 'sensor'},
            {'type': 2, 'id': '456', 'tag': 'home'}
        ]
        self.mock_adapter.put.return_value = {'status': 'ok'}
        result = self.tags.apply_tags(
            organization_id=123,
            tags_data=tags_data
        )
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_json']['tags'], tags_data)
        self.assertEqual(result, {'status': 'ok'})

    def test_delete_tag_success(self):
        self.mock_adapter.delete.return_value = {'status': 'ok'}
        result = self.tags.delete_tag(
            organization_id=123,
            tag_type=1,
            entity_id='123',
            tag='sensor'
        )
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(kwargs['ep_params']['type'], 1)
        self.assertEqual(kwargs['ep_params']['id'], '123')
        self.assertEqual(kwargs['ep_params']['tag'], 'sensor')
        self.assertEqual(result, {'status': 'ok'})

    def test_delete_tag_with_app_id(self):
        self.mock_adapter.delete.return_value = {'status': 'ok'}
        self.tags.delete_tag(
            organization_id=123,
            tag_type=1,
            entity_id='123',
            tag='sensor',
            app_id=5
        )
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(kwargs['ep_params']['appId'], 5)

import unittest
from unittest.mock import MagicMock
import json

from caredaily.apis.bot import BotStore
from caredaily.models import APIKeyType


class TestBotStore(unittest.TestCase):
    def setUp(self):
        self.bot_store = BotStore()
        self.mock_adapter = MagicMock()
        self.bot_store.adapter = self.mock_adapter
        self.mock_adapter._headers = {'ADMIN_KEY': 'admin_key'}
        self.mock_adapter._get_headers = MagicMock(return_value={'API_KEY': 'admin_key'})

    def test_add_bot_to_organization(self):
        self.mock_adapter.post.return_value = {'status': 'ok'}
        result = self.bot_store.add_bot_to_organization('com.example.bot', 123)
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['bundle'], 'com.example.bot')
        self.assertEqual(result, {'status': 'ok'})

    def test_remove_bot_from_organization(self):
        self.mock_adapter.delete.return_value = {'status': 'ok'}
        result = self.bot_store.remove_bot_from_organization('com.example.bot', 123)
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(kwargs['ep_params']['bundle'], 'com.example.bot')
        self.assertEqual(result, {'status': 'ok'})

    def test_approve_bot_for_organization(self):
        self.mock_adapter.put.return_value = {'status': 'approved'}
        result = self.bot_store.approve_bot_for_organization('com.example.bot', 123, status=1, development=True)
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_params']['bundle'], 'com.example.bot')
        self.assertEqual(kwargs['ep_params']['status'], 1)
        self.assertEqual(kwargs['ep_params']['development'], True)
        self.mock_adapter._get_headers.assert_called_once_with(api_key='admin_key', key_type=APIKeyType.USER)
        self.assertEqual(result, {'status': 'approved'})

    def test_approve_bot_for_organization_without_development(self):
        self.mock_adapter.put.return_value = {'status': 'approved'}
        self.bot_store.approve_bot_for_organization('com.example.bot', 123, status=1)
        args, kwargs = self.mock_adapter.put.call_args
        self.assertNotIn('development', kwargs['ep_params'])

    def test_get_bot_organizations(self):
        self.mock_adapter.get.return_value = {'organizations': []}
        result = self.bot_store.get_bot_organizations('com.example.bot')
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['bundle'], 'com.example.bot')
        self.assertEqual(result, {'organizations': []})

    def test_get_bot_notifications(self):
        self.mock_adapter.get.return_value = {'apps': []}
        result = self.bot_store.get_bot_notifications(123)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/cloud/appstore/botNotifications/123')
        self.assertIsNone(kwargs['ep_params'])
        self.mock_adapter._get_headers.assert_called_once_with(api_key='admin_key', key_type=APIKeyType.USER)
        self.assertEqual(result, {'apps': []})

    def test_get_bot_notifications_with_bundle(self):
        self.mock_adapter.get.return_value = {'apps': []}
        result = self.bot_store.get_bot_notifications(123, bundle='com.example.bot')
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/cloud/appstore/botNotifications/123')
        self.assertEqual(kwargs['ep_params']['bundle'], 'com.example.bot')
        self.assertEqual(result, {'apps': []})

    def test_update_bot_notifications(self):
        self.mock_adapter.put.return_value = {'resultCode': 0}
        groups = [
            {'notificationId': 1, 'groupId': 456},
            {'notificationId': 2, 'groupId': 789, 'delete': True},
        ]
        result = self.bot_store.update_bot_notifications(123, 'com.example.bot', groups)
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/espapi/cloud/appstore/botNotifications/123')
        self.assertEqual(kwargs['ep_params']['bundle'], 'com.example.bot')
        self.assertEqual(kwargs['ep_json'], {'groups': groups})
        self.mock_adapter._get_headers.assert_called_once_with(api_key='admin_key', key_type=APIKeyType.USER)
        self.assertEqual(result, {'resultCode': 0})

    def test_search_bots(self):
        self.mock_adapter.get.return_value = {'bots': []}
        result = self.bot_store.search_bots(
            search_by='weather',
            categories=['utility'],
            compatible=True,
            lang='en',
            core=1,
            location_id=123,
            organization_id=456,
            object_names=['object1'],
            limit=10
        )
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['searchBy'], 'weather')
        self.assertEqual(kwargs['ep_params']['categories'], ['utility'])
        self.assertEqual(kwargs['ep_params']['compatible'], True)
        self.assertEqual(kwargs['ep_params']['lang'], 'en')
        self.assertEqual(kwargs['ep_params']['core'], 1)
        self.assertEqual(kwargs['ep_params']['locationId'], 123)
        self.assertEqual(kwargs['ep_params']['organizationId'], 456)
        self.assertEqual(kwargs['ep_params']['objectNames'], ['object1'])
        self.assertEqual(kwargs['ep_params']['limit'], 10)
        self.assertEqual(result, {'bots': []})

    def test_search_bots_minimal(self):
        self.mock_adapter.get.return_value = {'bots': []}
        result = self.bot_store.search_bots()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params'], {})
        self.assertEqual(result, {'bots': []})

    def test_get_bot_info(self):
        self.mock_adapter.get.return_value = {'bot': {}}
        result = self.bot_store.get_bot_info('com.example.bot', lang='en', last_n_version=5, object_name='icon')
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['bundle'], 'com.example.bot')
        self.assertEqual(kwargs['ep_params']['lang'], 'en')
        self.assertEqual(kwargs['ep_params']['lastNVersion'], 5)
        self.assertEqual(kwargs['ep_params']['objectName'], 'icon')
        self.assertEqual(result, {'bot': {}})

    def test_get_bot_info_minimal(self):
        self.mock_adapter.get.return_value = {'bot': {}}
        result = self.bot_store.get_bot_info('com.example.bot')
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['bundle'], 'com.example.bot')
        self.assertNotIn('lang', kwargs['ep_params'])
        self.assertNotIn('lastNVersion', kwargs['ep_params'])
        self.assertNotIn('objectName', kwargs['ep_params'])

    def test_purchase_bot(self):
        self.mock_adapter.post.return_value = {'appInstanceId': 789}
        result = self.bot_store.purchase_bot('com.example.bot', location_id=123, organization_id=456)
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['bundle'], 'com.example.bot')
        self.assertEqual(kwargs['ep_params']['locationId'], 123)
        self.assertEqual(kwargs['ep_params']['organizationId'], 456)
        self.assertEqual(result, {'appInstanceId': 789})

    def test_purchase_bot_location_only(self):
        self.mock_adapter.post.return_value = {'appInstanceId': 789}
        self.bot_store.purchase_bot('com.example.bot', location_id=123)
        args, kwargs = self.mock_adapter.post.call_args
        self.assertNotIn('organizationId', kwargs['ep_params'])

    def test_purchase_bot_organization_only(self):
        self.mock_adapter.post.return_value = {'appInstanceId': 789}
        self.bot_store.purchase_bot('com.example.bot', organization_id=456)
        args, kwargs = self.mock_adapter.post.call_args
        self.assertNotIn('locationId', kwargs['ep_params'])

    def test_configure_my_bot(self):
        data = {'config': 'value'}
        self.mock_adapter.put.return_value = {'status': 'ok'}
        result = self.bot_store.configure_my_bot(123, status=1, data=data)
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_params']['appInstanceId'], 123)
        self.assertEqual(kwargs['ep_params']['status'], 1)
        self.assertEqual(kwargs['ep_data'], json.dumps(data))
        self.assertEqual(result, {'status': 'ok'})

    def test_configure_my_bot_without_status(self):
        data = {'config': 'value'}
        self.mock_adapter.put.return_value = {'status': 'ok'}
        self.bot_store.configure_my_bot(123, data=data)
        args, kwargs = self.mock_adapter.put.call_args
        self.assertNotIn('status', kwargs['ep_params'])

    def test_configure_my_bot_without_data(self):
        self.mock_adapter.put.return_value = {'status': 'ok'}
        self.bot_store.configure_my_bot(123, status=1)
        args, kwargs = self.mock_adapter.put.call_args
        self.assertIsNone(kwargs['ep_data'])

    def test_get_my_bots(self):
        self.mock_adapter.get.return_value = {'bots': []}
        result = self.bot_store.get_my_bots(
            app_instance_id=123,
            bundle='com.example.bot',
            location_id=456,
            organization_id=789,
            user_id=10,
            object_names=['obj1', 'obj2']
        )
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['appInstanceId'], 123)
        self.assertEqual(kwargs['ep_params']['bundle'], 'com.example.bot')
        self.assertEqual(kwargs['ep_params']['locationId'], 456)
        self.assertEqual(kwargs['ep_params']['organizationId'], 789)
        self.assertEqual(kwargs['ep_params']['userId'], 10)
        self.assertEqual(kwargs['ep_params']['objectNames'], ['obj1', 'obj2'])
        self.assertEqual(self.mock_adapter._get_headers.call_count, 2)
        self.mock_adapter._get_headers.assert_any_call('admin_key', key_type=APIKeyType.USER)
        self.assertEqual(result, {'bots': []})

    def test_get_my_bots_minimal(self):
        self.mock_adapter.get.return_value = {'bots': []}
        result = self.bot_store.get_my_bots()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params'], {})
        self.assertEqual(result, {'bots': []})

    def test_get_my_bots_without_admin_key(self):
        self.mock_adapter._headers = {}
        self.mock_adapter.get.return_value = {'bots': []}
        self.bot_store.get_my_bots()
        args, kwargs = self.mock_adapter.get.call_args
        # Should use default headers when ADMIN_KEY is not present
        self.mock_adapter._get_headers.assert_called_once_with()

    def test_remove_from_my_bots(self):
        self.mock_adapter.delete.return_value = {'status': 'ok'}
        result = self.bot_store.remove_from_my_bots(123)
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(kwargs['ep_params']['appInstanceId'], 123)
        self.assertEqual(result, {'status': 'ok'})

    def test_send_data_stream_message(self):
        data = {'message': 'test'}
        self.mock_adapter.post.return_value = {'status': 'sent'}
        result = self.bot_store.send_data_stream_message(
            scope=1,
            address='address123',
            data=data,
            location_id=456,
            organization_id=789
        )
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['scope'], 1)
        self.assertEqual(kwargs['ep_params']['address'], 'address123')
        self.assertEqual(kwargs['ep_params']['locationId'], 456)
        self.assertEqual(kwargs['ep_params']['organizationId'], 789)
        self.assertEqual(kwargs['ep_json'], json.dumps(data))
        self.assertEqual(result, {'status': 'sent'})

    def test_send_data_stream_message_minimal(self):
        data = {'message': 'test'}
        self.mock_adapter.post.return_value = {'status': 'sent'}
        self.bot_store.send_data_stream_message(1, 'address123', data)
        args, kwargs = self.mock_adapter.post.call_args
        self.assertNotIn('locationId', kwargs['ep_params'])
        self.assertNotIn('organizationId', kwargs['ep_params'])

    def test_get_summary(self):
        self.mock_adapter.get.return_value = {'summary': {}}
        result = self.bot_store.get_summary(location_id=123, organization_id=456)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['locationId'], 123)
        self.assertEqual(kwargs['ep_params']['organizationId'], 456)
        self.assertEqual(result, {'summary': {}})

    def test_get_summary_location_only(self):
        self.mock_adapter.get.return_value = {'summary': {}}
        self.bot_store.get_summary(location_id=123)
        args, kwargs = self.mock_adapter.get.call_args
        self.assertNotIn('organizationId', kwargs['ep_params'])

    def test_get_summary_organization_only(self):
        self.mock_adapter.get.return_value = {'summary': {}}
        self.bot_store.get_summary(organization_id=456)
        args, kwargs = self.mock_adapter.get.call_args
        self.assertNotIn('locationId', kwargs['ep_params'])

    def test_get_summary_minimal(self):
        self.mock_adapter.get.return_value = {'summary': {}}
        result = self.bot_store.get_summary()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params'], {})
        self.assertEqual(result, {'summary': {}})

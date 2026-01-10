import unittest
from unittest.mock import MagicMock
import json

from caredaily.apis.bot import BotDeveloper

class TestBotDeveloper(unittest.TestCase):
    def setUp(self):
        self.bot = BotDeveloper()
        self.mock_adapter = MagicMock()
        self.bot.adapter = self.mock_adapter

    def test_create_update_bot(self):
        self.mock_adapter.put.return_value = {'result': 'ok'}
        result = self.bot.create_update_bot('bundle', {'foo': 'bar'}, developer_team='team')
        self.mock_adapter.put.assert_called_once()
        self.assertEqual(result, {'result': 'ok'})

    def test_create_update_bot_version(self):
        self.mock_adapter.put.return_value = {'result': 'ok'}
        result = self.bot.create_update_bot_version('bundle', status=1, version='v1', data={'foo': 'bar'})
        self.mock_adapter.put.assert_called_once()
        self.assertEqual(result, {'result': 'ok'})

    def test_upload_bot_code(self):
        self.mock_adapter.post.return_value = {'upload': 'ok'}
        result = self.bot.upload_bot_code('data', 'application/zip', bundle='bundle', runtime=1)
        self.mock_adapter.post.assert_called_once()
        self.assertEqual(result, {'upload': 'ok'})

    def test_get_upload_bot_code_result(self):
        self.mock_adapter.get.return_value = {'status': 'done'}
        result = self.bot.get_upload_bot_code_result('reqid')
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, {'status': 'done'})

    def test_update_bot_parameters(self):
        self.mock_adapter.put.return_value = {'params': 'updated'}
        result = self.bot.update_bot_parameters('bundle', memory=128, timeout=30, development=True)
        self.mock_adapter.put.assert_called_once()
        self.assertEqual(result, {'params': 'updated'})

    def test_set_bot_version_status(self):
        self.mock_adapter.put.return_value = {'status': 'set'}
        result = self.bot.set_bot_version_status('bundle', status=2)
        self.mock_adapter.put.assert_called_once()
        self.assertEqual(result, {'status': 'set'})

    def test_get_bots(self):
        self.mock_adapter.get.return_value = {'bots': []}
        result = self.bot.get_bots(bundle='bundle')
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, {'bots': []})

    def test_get_bots_without_bundle(self):
        self.mock_adapter.get.return_value = {'bots': []}
        result = self.bot.get_bots()
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertNotIn('bundle', kwargs['ep_params'])
        self.assertEqual(result, {'bots': []})

    def test_get_bot_versions(self):
        self.mock_adapter.get.return_value = {'versions': []}
        result = self.bot.get_bot_versions('bundle', statuses=['active'], version='v1')
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['bundle'], 'bundle')
        self.assertEqual(kwargs['ep_params']['status'], ['active'])
        self.assertEqual(kwargs['ep_params']['version'], 'v1')
        self.assertEqual(result, {'versions': []})

    def test_get_bot_versions_minimal(self):
        self.mock_adapter.get.return_value = {'versions': []}
        result = self.bot.get_bot_versions('bundle')
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['bundle'], 'bundle')
        self.assertNotIn('status', kwargs['ep_params'])
        self.assertNotIn('version', kwargs['ep_params'])

    def test_get_bot_statistics(self):
        self.mock_adapter.get.return_value = {'stats': {'runs': 100}}
        result = self.bot.get_bot_statistics('bundle')
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['bundle'], 'bundle')
        self.assertEqual(result, {'stats': {'runs': 100}})

    def test_upload_bot_object(self):
        data = b'image_data'
        self.mock_adapter.put.return_value = {'upload': 'ok'}
        result = self.bot.upload_bot_object('icon.png', 'bundle', data, 'image/png')
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_params']['bundle'], 'bundle')
        self.assertEqual(kwargs['ep_data'], data)
        self.assertEqual(kwargs['ep_headers']['Content-Type'], 'image/png')
        self.assertEqual(result, {'upload': 'ok'})

    def test_upload_bot_object_default_content_type(self):
        data = b'image_data'
        self.mock_adapter.put.return_value = {'upload': 'ok'}
        self.bot.upload_bot_object('icon.png', 'bundle', data)
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_headers']['Content-Type'], 'image/png')

    def test_set_message_topics(self):
        topics = {'topic1': 'value1', 'topic2': 'value2'}
        self.mock_adapter.put.return_value = {'status': 'ok'}
        result = self.bot.set_message_topics('bundle', topics)
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_params']['bundle'], 'bundle')
        self.assertEqual(kwargs['ep_json'], json.dumps(topics))
        self.assertEqual(result, {'status': 'ok'})

    def test_get_execution_history(self):
        self.mock_adapter.get.return_value = {'history': []}
        result = self.bot.get_execution_history(
            start_date_ms=1000000,
            end_date_ms=2000000,
            bundle='bundle',
            developer=True,
            app_instance_id=123,
            flow=1,
            trigger=2,
            errors_only=True,
            row_count=50,
            sort_order='asc'
        )
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['startDate'], 1000000)
        self.assertEqual(kwargs['ep_params']['endDate'], 2000000)
        self.assertEqual(kwargs['ep_params']['bundle'], 'bundle')
        self.assertEqual(kwargs['ep_params']['developer'], True)
        self.assertEqual(kwargs['ep_params']['appInstanceId'], 123)
        self.assertEqual(kwargs['ep_params']['flow'], 1)
        self.assertEqual(kwargs['ep_params']['trigger'], 2)
        self.assertEqual(kwargs['ep_params']['errorsOnly'], True)
        self.assertEqual(kwargs['ep_params']['rowCount'], 50)
        self.assertEqual(kwargs['ep_params']['sortOrder'], 'asc')
        self.assertEqual(result, {'history': []})

    def test_get_execution_history_minimal(self):
        self.mock_adapter.get.return_value = {'history': []}
        result = self.bot.get_execution_history(1000000, 2000000)
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['startDate'], 1000000)
        self.assertEqual(kwargs['ep_params']['endDate'], 2000000)
        self.assertNotIn('bundle', kwargs['ep_params'])

    def test_get_execution_info(self):
        self.mock_adapter.get.return_value = {'info': {}}
        result = self.bot.get_execution_info(123, 1, 1000000)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['appInstanceId'], 123)
        self.assertEqual(kwargs['ep_params']['flow'], 1)
        self.assertEqual(kwargs['ep_params']['requestDate'], 1000000)
        self.assertEqual(result, {'info': {}})

    def test_manage_bot_instance_logging(self):
        self.mock_adapter.put.return_value = {'status': 'ok'}
        result = self.bot.manage_bot_instance_logging(123, 1, 1, end_date_ms=2000000)
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_params']['appInstanceId'], 123)
        self.assertEqual(kwargs['ep_params']['flow'], 1)
        self.assertEqual(kwargs['ep_params']['status'], 1)
        self.assertEqual(kwargs['ep_params']['endDate'], 2000000)
        self.assertEqual(result, {'status': 'ok'})

    def test_manage_bot_instance_logging_without_end_date(self):
        self.mock_adapter.put.return_value = {'status': 'ok'}
        self.bot.manage_bot_instance_logging(123, 1, 1)
        args, kwargs = self.mock_adapter.put.call_args
        self.assertNotIn('endDate', kwargs['ep_params'])

    def test_describe_bot_instance_logging(self):
        self.mock_adapter.get.return_value = {'logging': {}}
        result = self.bot.describe_bot_instance_logging(123, 1)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['appInstanceId'], 123)
        self.assertEqual(kwargs['ep_params']['flow'], 1)
        self.assertEqual(result, {'logging': {}})

    def test_export_bot_instance_log(self):
        self.mock_adapter.post.return_value = {'taskId': 'task123'}
        result = self.bot.export_bot_instance_log(123, 1, 1000000, end_date_ms=2000000)
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['appInstanceId'], 123)
        self.assertEqual(kwargs['ep_params']['flow'], 1)
        self.assertEqual(kwargs['ep_params']['startDate'], 1000000)
        self.assertEqual(kwargs['ep_params']['endDate'], 2000000)
        self.assertEqual(result, {'taskId': 'task123'})

    def test_export_bot_instance_log_without_end_date(self):
        self.mock_adapter.post.return_value = {'taskId': 'task123'}
        self.bot.export_bot_instance_log(123, 1, 1000000)
        args, kwargs = self.mock_adapter.post.call_args
        self.assertNotIn('endDate', kwargs['ep_params'])

    def test_get_exported_bot_instance_log(self):
        self.mock_adapter.get.return_value = {'log': 'data'}
        result = self.bot.get_exported_bot_instance_log('task123')
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['taskId'], 'task123')
        self.assertEqual(result, {'log': 'data'})

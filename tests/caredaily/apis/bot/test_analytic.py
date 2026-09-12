import unittest
from unittest.mock import MagicMock

from caredaily.apis.bot import Analytic


class TestAnalytic(unittest.TestCase):
    def setUp(self):
        self.analytic = Analytic()
        self.mock_adapter = MagicMock()
        self.analytic.adapter = self.mock_adapter

    def test_get_app_key_success(self):
        self.mock_adapter.get.return_value = {'key': 'abc123', 'expiry': 1234567890}
        result = self.analytic.get_app_key(app_instance_id=123)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['appInstanceId'], 123)
        self.assertEqual(result, {'key': 'abc123', 'expiry': 1234567890})

    def test_start_execution_success(self):
        self.mock_adapter.post.return_value = {'resultCode': 0}
        result = self.analytic.start_execution(start_key=456)
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['startKey'], 456)
        self.assertEqual(result, {'resultCode': 0})

    def test_start_execution_with_aws_params(self):
        self.mock_adapter.post.return_value = {'resultCode': 0}
        self.analytic.start_execution(
            start_key=456,
            aws_request_id='req-123',
            log_stream_name='stream-456'
        )
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['startKey'], 456)
        self.assertEqual(kwargs['ep_params']['awsRequestId'], 'req-123')
        self.assertEqual(kwargs['ep_params']['logStreamName'], 'stream-456')

    def test_request_execution_in_seconds(self):
        self.mock_adapter.put.return_value = {'timer': 1740348539000}
        result = self.analytic.request_execution(in_seconds=60)
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_params']['in'], 60)
        self.assertEqual(result, {'timer': 1740348539000})

    def test_request_execution_at_timestamp(self):
        self.mock_adapter.put.return_value = {'timer': 1740348539000}
        self.analytic.request_execution(at_timestamp=1740348539000)
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_params']['at'], 1740348539000)

    def test_cancel_execution_success(self):
        self.mock_adapter.delete.return_value = {'resultCode': 0}
        result = self.analytic.cancel_execution()
        self.mock_adapter.delete.assert_called_once()
        self.assertEqual(result, {'resultCode': 0})

    def test_get_secret_success(self):
        self.mock_adapter.get.return_value = {'secretValue': 'Secret'}
        result = self.analytic.get_secret(secret_name='my_secret')
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['secretName'], 'my_secret')
        self.assertEqual(result, {'secretValue': 'Secret'})

    def test_get_variable_success(self):
        self.mock_adapter.get.return_value = b'binary content'
        result = self.analytic.get_variable(name='my_var')
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertIsNone(kwargs.get('ep_params'))
        self.assertEqual(result, b'binary content')

    def test_get_variable_shared(self):
        self.mock_adapter.get.return_value = b'binary content'
        self.analytic.get_variable(name='my_var', shared=True)
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['shared'], True)

    def test_save_variable_success(self):
        self.mock_adapter.post.return_value = {'resultCode': 0}
        result = self.analytic.save_variable(
            name='my_var',
            value=b'binary data',
            content_md5='abc123'
        )
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_data'], b'binary data')
        self.assertEqual(kwargs['ep_headers']['Content-MD5'], 'abc123')
        self.assertEqual(result, {'resultCode': 0})

    def test_save_variable_without_md5(self):
        self.mock_adapter.post.return_value = {'resultCode': 0}
        self.analytic.save_variable(name='my_var', value=b'binary data')
        args, kwargs = self.mock_adapter.post.call_args
        self.assertIsNone(kwargs.get('ep_headers'))

    def test_delete_variable_success(self):
        self.mock_adapter.delete.return_value = {'resultCode': 0}
        result = self.analytic.delete_variable(name='my_var')
        self.mock_adapter.delete.assert_called_once()
        self.assertEqual(result, {'resultCode': 0})

    def test_save_variables_success(self):
        self.mock_adapter.post.return_value = {'resultCode': 0}
        result = self.analytic.save_variables(
            names=['var1', 'var2'],
            lengths=[10, 20],
            values=b'concatenated data',
            content_md5='abc123'
        )
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['name'], ['var1', 'var2'])
        self.assertEqual(kwargs['ep_params']['length'], [10, 20])
        self.assertEqual(kwargs['ep_data'], b'concatenated data')
        self.assertEqual(kwargs['ep_headers']['Content-MD5'], 'abc123')
        self.assertEqual(result, {'resultCode': 0})

    def test_send_data_message_success(self):
        self.mock_adapter.post.return_value = {'resultCode': 0}
        stream_data = {
            'locations': [34122, 15689],
            'bots': [567, 893],
            'feed': {'key0': 'value0'}
        }
        result = self.analytic.send_data_message(
            address='my_address',
            scope=1,
            stream_data=stream_data
        )
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['address'], 'my_address')
        self.assertEqual(kwargs['ep_params']['scope'], 1)
        self.assertEqual(kwargs['ep_json'], stream_data)
        self.assertEqual(result, {'resultCode': 0})

    def test_submit_data_request_success(self):
        self.mock_adapter.post.return_value = {'resultCode': 0}
        data_requests = [
            {
                'type': 1,
                'key': 'ml_inactivity',
                'deviceId': 'ABC123',
                'startTime': 1446537883000,
                'endTime': 1456537883000
            }
        ]
        result = self.analytic.submit_data_request(data_requests=data_requests)
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_json']['dataRequests'], data_requests)
        self.assertEqual(result, {'resultCode': 0})

    def test_get_location_events_success(self):
        self.mock_adapter.get.return_value = {'events': []}
        result = self.analytic.get_location_events(location_id=123)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertIsNone(kwargs.get('ep_params'))
        self.assertEqual(result, {'events': []})

    def test_get_location_events_with_dates(self):
        self.mock_adapter.get.return_value = {'events': []}
        self.analytic.get_location_events(
            location_id=123,
            start_date='2020-01-01',
            end_date='2020-01-31'
        )
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['startDate'], '2020-01-01')
        self.assertEqual(kwargs['ep_params']['endDate'], '2020-01-31')

    def test_get_call_center_success(self):
        self.mock_adapter.get.return_value = {'callCenter': {'status': 3}}
        result = self.analytic.get_call_center()
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, {'callCenter': {'status': 3}})

    def test_update_call_center_success(self):
        self.mock_adapter.put.return_value = {'resultCode': 0}
        call_center_data = {'callCenter': {'alertStatus': 1}}
        result = self.analytic.update_call_center(call_center_data=call_center_data)
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_json'], call_center_data)
        self.assertEqual(result, {'resultCode': 0})

    def test_get_call_center_alerts_success(self):
        self.mock_adapter.get.return_value = {'callCenterAlerts': []}
        result = self.analytic.get_call_center_alerts()
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, {'callCenterAlerts': []})

    def test_ask_questions_success(self):
        self.mock_adapter.post.return_value = {'questions': [{'id': 1}]}
        questions = [{'key': 'test', 'question': {'en': 'Test?'}}]
        result = self.analytic.ask_questions(questions=questions)
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_json']['questions'], questions)
        self.assertEqual(result, {'questions': [{'id': 1}]})

    def test_get_question_responses_success(self):
        self.mock_adapter.get.return_value = {'questions': []}
        result = self.analytic.get_question_responses()
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertIsNone(kwargs.get('ep_params'))
        self.assertEqual(result, {'questions': []})

    def test_get_question_responses_with_filters(self):
        self.mock_adapter.get.return_value = {'questions': []}
        self.analytic.get_question_responses(key='test', collection_name='urgent', status=2)
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['key'], 'test')
        self.assertEqual(kwargs['ep_params']['collectionName'], 'urgent')
        self.assertEqual(kwargs['ep_params']['status'], 2)

    def test_update_question_response_success(self):
        self.mock_adapter.put.return_value = {'resultCode': 0}
        result = self.analytic.update_question_response(question_id=1, answer='Yes', editable=True)
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_params']['questionId'], 1)
        self.assertEqual(kwargs['ep_json']['answer'], 'Yes')
        self.assertEqual(kwargs['ep_json']['editable'], True)
        self.assertEqual(result, {'resultCode': 0})

    def test_delete_questions_success(self):
        self.mock_adapter.delete.return_value = {'resultCode': 0}
        result = self.analytic.delete_questions(question_id=1)
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(kwargs['ep_params']['questionId'], 1)
        self.assertEqual(result, {'resultCode': 0})

    def test_get_question_collections_success(self):
        self.mock_adapter.get.return_value = {'collections': []}
        result = self.analytic.get_question_collections()
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, {'collections': []})

    def test_set_question_collection_success(self):
        self.mock_adapter.put.return_value = {'resultCode': 0}
        collection = {'name': 'Urgent', 'description': 'Urgent questions'}
        result = self.analytic.set_question_collection(collection=collection)
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_json']['collection'], collection)
        self.assertEqual(result, {'resultCode': 0})

    def test_delete_question_collection_success(self):
        self.mock_adapter.delete.return_value = {'resultCode': 0}
        result = self.analytic.delete_question_collection(name='Urgent')
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(kwargs['ep_params']['name'], 'Urgent')
        self.assertEqual(result, {'resultCode': 0})

    def test_get_tags_success(self):
        self.mock_adapter.get.return_value = {'tags': []}
        result = self.analytic.get_tags()
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, {'tags': []})

    def test_get_tags_with_filters(self):
        self.mock_adapter.get.return_value = {'tags': []}
        self.analytic.get_tags(tag_type=2, id_value='456')
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['type'], 2)
        self.assertEqual(kwargs['ep_params']['id'], '456')

    def test_apply_tags_success(self):
        self.mock_adapter.put.return_value = {'resultCode': 0}
        tags = [{'type': 1, 'tag': 'parent', 'id': '123'}]
        result = self.analytic.apply_tags(tags=tags)
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_json']['tags'], tags)
        self.assertEqual(result, {'resultCode': 0})

    def test_delete_tags_success(self):
        self.mock_adapter.delete.return_value = {'resultCode': 0}
        result = self.analytic.delete_tags(tag_type=1, tag='parent', id_value='123')
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(kwargs['ep_params']['type'], 1)
        self.assertEqual(kwargs['ep_params']['tag'], 'parent')
        self.assertEqual(kwargs['ep_params']['id'], '123')
        self.assertEqual(result, {'resultCode': 0})

    def test_send_notification_success(self):
        self.mock_adapter.post.return_value = {'resultCode': 0}
        notification_data = {'pushMessage': {'content': 'Test'}}
        result = self.analytic.send_notification(category=0, notification_data=notification_data)
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['category'], 0)
        self.assertEqual(kwargs['ep_json'], notification_data)
        self.assertEqual(result, {'resultCode': 0})

    def test_send_location_notification_success(self):
        self.mock_adapter.post.return_value = {'resultCode': 0}
        notification_data = {'pushMessage': {'content': 'Test'}}
        result = self.analytic.send_location_notification(location_id=123, notification_data=notification_data)
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_json'], notification_data)
        self.assertEqual(result, {'resultCode': 0})

    def test_update_location_success(self):
        self.mock_adapter.put.return_value = {'resultCode': 0}
        location_data = {'location': {'name': 'My House'}}
        result = self.analytic.update_location(location_id=123, location_data=location_data)
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_json'], location_data)
        self.assertEqual(result, {'resultCode': 0})

    def test_get_device_parameters_success(self):
        self.mock_adapter.get.return_value = {'parameters': []}
        result = self.analytic.get_device_parameters(device_id='abc123')
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, {'parameters': []})

    def test_set_device_parameters_success(self):
        self.mock_adapter.post.return_value = {'resultCode': 0}
        parameters = [{'name': 'temperature', 'value': 72}]
        result = self.analytic.set_device_parameters(device_id='abc123', parameters=parameters)
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_json']['parameters'], parameters)
        self.assertEqual(result, {'resultCode': 0})

    def test_update_parameters_success(self):
        self.mock_adapter.put.return_value = {'resultCode': 0}
        parameters = [{'deviceId': 'abc123', 'name': 'temperature', 'value': 72}]
        result = self.analytic.update_parameters(parameters=parameters)
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_json']['parameters'], parameters)
        self.assertEqual(result, {'resultCode': 0})

    def test_send_ai_request_success(self):
        self.mock_adapter.post.return_value = {'resultCode': 0, 'answer': 'Hello!'}
        result = self.analytic.send_ai_request(message='Say me hello!')
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(args[0], '/espapi/analytic/ai')
        self.assertIsNone(kwargs['ep_params'])
        self.assertEqual(kwargs['ep_json'], {'message': 'Say me hello!'})
        self.assertEqual(result, {'resultCode': 0, 'answer': 'Hello!'})

    def test_send_ai_request_with_all_parameters(self):
        self.mock_adapter.post.return_value = {'resultCode': 0}
        result = self.analytic.send_ai_request(
            message='Say me hello!',
            conversation_id='conv1',
            request_id='req1',
            location_id=123,
            timeout_ms=5000,
        )
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(args[0], '/espapi/analytic/ai')
        self.assertEqual(kwargs['ep_params']['locationId'], 123)
        self.assertEqual(kwargs['ep_params']['timeout'], 5000)
        self.assertEqual(kwargs['ep_json'], {
            'message': 'Say me hello!',
            'conversationId': 'conv1',
            'requestId': 'req1',
        })
        self.assertEqual(result, {'resultCode': 0})

    def test_send_openai_request_success(self):
        self.mock_adapter.post.return_value = {'resultCode': 0}
        openai_data = {'model': 'gpt-3.5-turbo', 'messages': [{'role': 'user', 'content': 'Hello'}]}
        result = self.analytic.send_openai_request(openai_data=openai_data, key='req1')
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['key'], 'req1')
        self.assertEqual(kwargs['ep_json'], openai_data)
        self.assertEqual(result, {'resultCode': 0})

    def test_send_voice_call_success(self):
        self.mock_adapter.post.return_value = {'callUuid': 'uuid-123'}
        voice_call_data = {'model': {'startStepId': 0, 'steps': []}, 'userId': 123}
        result = self.analytic.send_voice_call(voice_call_data=voice_call_data)
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_json'], voice_call_data)
        self.assertEqual(result, {'callUuid': 'uuid-123'})

    def test_set_voice_call_answer_success(self):
        self.mock_adapter.post.return_value = {'resultCode': 0}
        model = {'startStepId': 0, 'steps': []}
        result = self.analytic.set_voice_call_answer(user_id=123, model=model)
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['userId'], 123)
        self.assertEqual(kwargs['ep_json']['model'], model)
        self.assertEqual(result, {'resultCode': 0})

    def test_delete_voice_call_answer_success(self):
        self.mock_adapter.delete.return_value = {'resultCode': 0}
        result = self.analytic.delete_voice_call_answer(user_id=123)
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(kwargs['ep_params']['userId'], 123)
        self.assertEqual(result, {'resultCode': 0})

    def test_submit_ticket_success(self):
        self.mock_adapter.post.return_value = {'resultCode': 0}
        ticket_data = {'ticket': {'type': 1, 'priority': 2, 'subject': 'Test', 'comment': 'Test comment'}}
        result = self.analytic.submit_ticket(ticket_data=ticket_data)
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_json'], ticket_data)
        self.assertEqual(result, {'resultCode': 0})

    def test_send_fall_feedback_success(self):
        self.mock_adapter.post.return_value = {'resultCode': 0}
        feedback_data = {'deviceId': 'abc123', 'classification': 'TRUE_POSITIVE', 'eventTimestamp': 1234567890}
        result = self.analytic.send_fall_feedback(feedback_data=feedback_data)
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_json'], feedback_data)
        self.assertEqual(result, {'resultCode': 0})

    def test_send_mms_success(self):
        self.mock_adapter.post.return_value = {'resultCode': 0}
        result = self.analytic.send_mms(user_id=123, media_type=1, url='https://example.com/image.jpg', caption='Test')
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['userId'], 123)
        self.assertEqual(kwargs['ep_params']['mediaType'], 1)
        self.assertEqual(kwargs['ep_params']['url'], 'https://example.com/image.jpg')
        self.assertEqual(kwargs['ep_params']['caption'], 'Test')
        self.assertEqual(result, {'resultCode': 0})

    def test_execute_cli_success(self):
        self.mock_adapter.post.return_value = {'resultCode': 0}
        result = self.analytic.execute_cli(json_data='{"id": 123}', initialize='true')
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['json'], '{"id": 123}')
        self.assertEqual(kwargs['ep_params']['initialize'], 'true')
        self.assertEqual(result, {'resultCode': 0})

    def test_get_challenge_participants_success(self):
        self.mock_adapter.get.return_value = {'locations': []}
        result = self.analytic.get_challenge_participants(challenge_id=1)
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, {'locations': []})

    def test_get_challenge_participants_with_filters(self):
        self.mock_adapter.get.return_value = {'locations': []}
        self.analytic.get_challenge_participants(challenge_id=1, status=2, location_id=123, get_devices=True)
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['status'], 2)
        self.assertEqual(kwargs['ep_params']['locationId'], 123)
        self.assertEqual(kwargs['ep_params']['getDevices'], True)

    def test_get_device_parameters_with_historical(self):
        """Test Case ID: TC-Analytic-001
        Title: Get Device Parameters with Historical Query Parameters
        Priority: P1
        """
        self.mock_adapter.get.return_value = {'measures': []}
        result = self.analytic.get_device_parameters(
            device_id='dev1',
            start_date='1446537883000',
            end_date='1446537893000',
            param_name='energy',
            index='0',
            last_rows=100
        )
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/analytic/devices/dev1/parameters')
        self.assertEqual(kwargs['ep_params']['startDate'], '1446537883000')
        self.assertEqual(kwargs['ep_params']['endDate'], '1446537893000')
        self.assertEqual(kwargs['ep_params']['paramName'], 'energy')
        self.assertEqual(kwargs['ep_params']['index'], '0')
        self.assertEqual(kwargs['ep_params']['lastRows'], 100)
        self.assertEqual(result, {'measures': []})

    def test_get_device_parameters_current_only(self):
        """Test Case ID: TC-Analytic-002
        Title: Get Device Parameters Current Measurements Only
        Priority: P1
        """
        self.mock_adapter.get.return_value = {'measures': []}
        result = self.analytic.get_device_parameters(device_id='dev1')
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/analytic/devices/dev1/parameters')
        self.assertIsNone(kwargs.get('ep_params'))
        self.assertEqual(result, {'measures': []})

    def test_inject_device_parameters(self):
        """Test Case ID: TC-Analytic-003
        Title: Inject Device Parameters
        Priority: P1
        """
        self.mock_adapter.post.return_value = {'resultCode': 0}
        params = [
            {'name': 'syn.move', 'index': '0', 'value': '1'},
            {'name': 'syn.sleep', 'value': '0'}
        ]
        result = self.analytic.inject_device_parameters(
            device_id='dev1',
            timestamp=1446537883000,
            params=params
        )
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(args[0], '/espapi/analytic/devices/dev1/parameters')
        self.assertEqual(kwargs['ep_json']['timestamp'], 1446537883000)
        self.assertEqual(kwargs['ep_json']['params'], params)
        self.assertEqual(result, {'resultCode': 0})

    def test_send_device_commands(self):
        """Test Case ID: TC-Analytic-004
        Title: Send Commands to Multiple Devices
        Priority: P1
        """
        self.mock_adapter.put.return_value = {'resultCode': 0, 'devices': []}
        devices = [
            {
                'deviceId': 'ABC123',
                'commandType': 0,
                'commandTimeout': 15000,
                'params': [
                    {'name': 'outletStatus', 'index': '0', 'value': '1'},
                    {'name': 'ppc.lowPowerMode', 'value': '0'}
                ],
                'comment': 'Test command'
            }
        ]
        result = self.analytic.send_device_commands(devices=devices)
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/espapi/analytic/parameters')
        self.assertEqual(kwargs['ep_json']['devices'], devices)
        self.assertEqual(result, {'resultCode': 0, 'devices': []})

    def test_upload_goicon_document(self):
        self.mock_adapter.post.return_value = {'resultCode': 0}
        result = self.analytic.upload_goicon_document(
            file_content=b'%PDF-1.4',
            description='Service plan document',
            category='Service Plans',
            timestamp='2026-01-01T00:00:00Z',
            visible_to_residents=True,
        )
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(args[0], '/espapi/analytic/goicon/documents')
        self.assertEqual(kwargs['ep_params']['description'], 'Service plan document')
        self.assertEqual(kwargs['ep_params']['category'], 'Service Plans')
        self.assertEqual(kwargs['ep_params']['timestamp'], '2026-01-01T00:00:00Z')
        self.assertEqual(kwargs['ep_params']['visibleToResidents'], True)
        self.assertEqual(kwargs['ep_data'], b'%PDF-1.4')
        self.assertEqual(kwargs['ep_headers'], {'Content-Type': 'application/octet-stream'})
        self.assertEqual(result, {'resultCode': 0})

    def test_upload_goicon_document_minimal(self):
        self.mock_adapter.post.return_value = {'resultCode': 0}
        self.analytic.upload_goicon_document(
            file_content=b'%PDF-1.4',
            description='Doc',
            category='Service Plans',
        )
        args, kwargs = self.mock_adapter.post.call_args
        self.assertNotIn('timestamp', kwargs['ep_params'])
        self.assertNotIn('visibleToResidents', kwargs['ep_params'])

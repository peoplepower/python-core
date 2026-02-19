import unittest
from unittest.mock import MagicMock
from caredaily.apis.app import UserCommunication

class TestUserCommunication(unittest.TestCase):
    def setUp(self):
        self.uc = UserCommunication()
        self.mock_adapter = MagicMock()
        self.uc.adapter = self.mock_adapter
        self.mock_adapter._get_headers = MagicMock(return_value={'API_KEY': 'test_key'})

    def test_get_questions(self):
        self.mock_adapter.get.return_value = 'questions-result'
        result = self.uc.get_questions(location_id=1)
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, 'questions-result')

    def test_get_questions_with_filters(self):
        self.mock_adapter.get.return_value = 'questions-result'
        result = self.uc.get_questions(
            location_id=1,
            answer_statuses=[1, 2],
            editable=True,
            collection_name='test',
            question_id=5,
            app_instance_id=10,
            lang='en',
            limit=20
        )
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['locationId'], 1)
        self.assertEqual(kwargs['ep_params']['answerStatus'], [1, 2])
        self.assertEqual(kwargs['ep_params']['editable'], True)

    def test_answer_questions(self):
        self.mock_adapter.put.return_value = 'answer-result'
        result = self.uc.answer_questions(location_id=1, answers={'q': 'a'})
        self.mock_adapter.put.assert_called_once()
        self.assertEqual(result, 'answer-result')

    def test_answer_questions_with_check_if_valid(self):
        self.mock_adapter.put.return_value = 'answer-result'
        result = self.uc.answer_questions(
            location_id=1,
            answers={'q': 'a'},
            check_if_valid=True
        )
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_params']['checkIfValid'], True)
        self.assertIsNotNone(kwargs['ep_headers'])

    def test_get_notification_subscriptions(self):
        self.mock_adapter.get.return_value = {'subscriptions': []}
        result = self.uc.get_notification_subscriptions()
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/notificationSubscriptions')
        self.assertEqual(result, {'subscriptions': []})

    def test_get_notification_subscriptions_with_user_id(self):
        self.mock_adapter.get.return_value = {'subscriptions': []}
        result = self.uc.get_notification_subscriptions(user_id=123)
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['userId'], 123)

    def test_set_notification_subscriptions(self):
        self.mock_adapter.put.return_value = {'updated': True}
        result = self.uc.set_notification_subscriptions(
            notification_type=1,
            email=True,
            push=False,
            sms=True
        )
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/notificationSubscriptions/1')
        self.assertEqual(kwargs['ep_params']['email'], True)
        self.assertEqual(kwargs['ep_params']['push'], False)
        self.assertEqual(kwargs['ep_params']['sms'], True)

    def test_set_notification_subscriptions_with_all_params(self):
        self.mock_adapter.put.return_value = {'updated': True}
        result = self.uc.set_notification_subscriptions(
            notification_type=1,
            location_id=123,
            user_id=456,
            email=True,
            push=True,
            sms=False,
            email_period=3600,
            push_period=1800
        )
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_params']['locationId'], 123)
        self.assertEqual(kwargs['ep_params']['userId'], 456)
        self.assertEqual(kwargs['ep_params']['emailPeriod'], 3600)
        self.assertEqual(kwargs['ep_params']['pushPeriod'], 1800)

    def test_post_push_notification_token(self):
        self.mock_adapter.put.return_value = {'registered': True}
        result = self.uc.post_push_notification_token(
            app_name='test_app',
            token='test_token'
        )
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/notificationToken/test_app/test_token')
        self.assertEqual(result, {'registered': True})

    def test_post_push_notification_token_with_options(self):
        self.mock_adapter.put.return_value = {'registered': True}
        result = self.uc.post_push_notification_token(
            app_name='test_app',
            token='test_token',
            badge=True,
            brand='test_brand'
        )
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_params']['badge'], True)
        self.assertEqual(kwargs['ep_params']['brand'], 'test_brand')

    def test_delete_push_notification_token(self):
        self.mock_adapter.delete.return_value = {'deleted': True}
        result = self.uc.delete_push_notification_token(token='test_token')
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/notificationToken/test_token')
        self.assertEqual(result, {'deleted': True})

    def test_send_notification(self):
        notification_data = {'pushMessage': {'content': 'Test'}}
        self.mock_adapter.post.return_value = {'sent': True}
        result = self.uc.send_notification(notification_data=notification_data)
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_json'], notification_data)
        self.assertEqual(result, {'sent': True})

    def test_send_notification_with_params(self):
        notification_data = {'pushMessage': {'content': 'Test'}}
        self.mock_adapter.post.return_value = {'sent': True}
        result = self.uc.send_notification(
            notification_data=notification_data,
            user_id=1,
            location_id=2,
            organization_id=3
        )
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['userId'], 1)
        self.assertEqual(kwargs['ep_params']['locationId'], 2)
        self.assertEqual(kwargs['ep_params']['organizationId'], 3)

    def test_get_notifications(self):
        self.mock_adapter.get.return_value = {'notifications': []}
        result = self.uc.get_notifications(start_date='2024-01-01')
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['startDate'], '2024-01-01')
        self.assertEqual(result, {'notifications': []})

    def test_get_notifications_with_all_filters(self):
        self.mock_adapter.get.return_value = {'notifications': []}
        result = self.uc.get_notifications(
            start_date='2024-01-01',
            end_date='2024-01-31',
            user_id=1,
            location_id=2,
            source_type=3,
            delivery_type=4,
            notification_type=5
        )
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['endDate'], '2024-01-31')
        self.assertEqual(kwargs['ep_params']['sourceType'], 3)
        self.assertEqual(kwargs['ep_params']['deliveryType'], 4)
        self.assertEqual(kwargs['ep_params']['notificationType'], 5)

    def test_post_support_ticket(self):
        ticket_data = {'ticket': {'type': 1, 'subject': 'Test'}}
        self.mock_adapter.post.return_value = {'ticketId': 1}
        result = self.uc.post_support_ticket(ticket_data=ticket_data)
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_json'], ticket_data)
        self.assertEqual(result, {'ticketId': 1})

    def test_post_support_ticket_with_params(self):
        ticket_data = {'ticket': {'type': 1, 'subject': 'Test'}}
        self.mock_adapter.post.return_value = {'ticketId': 1}
        result = self.uc.post_support_ticket(
            ticket_data=ticket_data,
            user_id=1,
            location_id=2
        )
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['userId'], 1)
        self.assertEqual(kwargs['ep_params']['locationId'], 2)

    def test_post_feedback(self):
        feedback_data = {'feedback': {'type': 1, 'subject': 'Test'}}
        self.mock_adapter.post.return_value = {'feedbackId': 1}
        result = self.uc.post_feedback(feedback_data=feedback_data)
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_json'], feedback_data)
        self.assertEqual(result, {'feedbackId': 1})

    def test_post_feedback_with_params(self):
        feedback_data = {'feedback': {'type': 1, 'subject': 'Test'}}
        self.mock_adapter.post.return_value = {'feedbackId': 1}
        result = self.uc.post_feedback(
            feedback_data=feedback_data,
            user_id=1,
            brand='test_brand'
        )
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['userId'], 1)
        self.assertEqual(kwargs['ep_params']['brand'], 'test_brand')

    def test_get_feedback_by_search(self):
        self.mock_adapter.get.return_value = {'feedbacks': []}
        result = self.uc.get_feedback_by_search(
            app_name='test_app',
            feedback_type=1,
            length=10
        )
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/feedback/test_app/1')
        self.assertEqual(kwargs['ep_params']['length'], 10)
        self.assertEqual(result, {'feedbacks': []})

    def test_get_feedback_by_search_with_filters(self):
        self.mock_adapter.get.return_value = {'feedbacks': []}
        result = self.uc.get_feedback_by_search(
            app_name='test_app',
            feedback_type=1,
            length=10,
            start_pos=0,
            product_id=5,
            product_category=3,
            disabled=False
        )
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['startPos'], 0)
        self.assertEqual(kwargs['ep_params']['productId'], 5)
        self.assertEqual(kwargs['ep_params']['productCategory'], 3)
        self.assertEqual(kwargs['ep_params']['disabled'], False)

    def test_get_specific_feedback(self):
        self.mock_adapter.get.return_value = {'feedback': {}}
        result = self.uc.get_specific_feedback(feedback_id=123)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/feedback/123')
        self.assertEqual(result, {'feedback': {}})

    def test_vote_for_feedback(self):
        self.mock_adapter.put.return_value = {'voted': True}
        result = self.uc.vote_for_feedback(feedback_id=123, rank=1)
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/feedback/123/1')
        self.assertEqual(result, {'voted': True})

    def test_support(self):
        support_data = {'firstName': 'Test', 'email': 'test@example.com'}
        self.mock_adapter.post.return_value = {'ticketId': 1}
        result = self.uc.support(support_data=support_data)
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_json'], support_data)
        self.assertEqual(result, {'ticketId': 1})

    def test_support_with_app_name(self):
        support_data = {'firstName': 'Test', 'email': 'test@example.com'}
        self.mock_adapter.post.return_value = {'ticketId': 1}
        result = self.uc.support(support_data=support_data, app_name='test_app')
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['appName'], 'test_app')

    def test_get_survey_questions(self):
        self.mock_adapter.get.return_value = {'survey': {}}
        result = self.uc.get_survey_questions()
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/surveyQuestions')
        self.assertEqual(result, {'survey': {}})

    def test_answer_survey_questions(self):
        survey_answer = {'question': {'id': 1, 'answerText': 'Answer'}}
        self.mock_adapter.put.return_value = {'result_code': 0}
        result = self.uc.answer_survey_questions(location_id=0, answer_id=1, questions=survey_answer)
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_json'], survey_answer)
        self.assertEqual(result, {'result_code': 0})

    def test_get_message_topics(self):
        self.mock_adapter.get.return_value = {'topics': []}
        result = self.uc.get_message_topics()
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/messageTopics')
        self.assertEqual(result, {'topics': []})

    def test_get_message_topics_with_params(self):
        self.mock_adapter.get.return_value = {'topics': []}
        result = self.uc.get_message_topics(app_id=1, lang='en')
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['appId'], 1)
        self.assertEqual(kwargs['ep_params']['lang'], 'en')

    def test_get_message_topics_with_analytic_key(self):
        self.mock_adapter.get.return_value = {'topics': []}
        result = self.uc.get_message_topics(analytic_key='test_key')
        args, kwargs = self.mock_adapter.get.call_args
        self.assertIsNotNone(kwargs['ep_headers'])

    def test_create_messages(self):
        messages = {'messages': [{'status': 1}]}
        self.mock_adapter.post.return_value = {'messageIds': [1]}
        result = self.uc.create_messages(messages=messages)
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_json'], messages)
        self.assertEqual(result, {'messageIds': [1]})

    def test_create_messages_with_params(self):
        messages = {'messages': [{'status': 1}]}
        self.mock_adapter.post.return_value = {'messageIds': [1]}
        result = self.uc.create_messages(
            messages=messages,
            location_id=123,
            analytic_key='test_key'
        )
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['locationId'], 123)
        self.assertIsNotNone(kwargs['ep_headers'])

    def test_get_messages(self):
        self.mock_adapter.get.return_value = {'messages': []}
        result = self.uc.get_messages(
            location_id=123,
            start_date='2024-01-01'
        )
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['locationId'], 123)
        self.assertEqual(kwargs['ep_params']['startDate'], '2024-01-01')
        self.assertEqual(result, {'messages': []})

    def test_get_messages_with_all_filters(self):
        self.mock_adapter.get.return_value = {'messages': []}
        result = self.uc.get_messages(
            location_id=123,
            start_date='2024-01-01',
            end_date='2024-01-31',
            app_instance_id=10,
            topic_id='topic1',
            read_status=True,
            lang='en'
        )
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['endDate'], '2024-01-31')
        self.assertEqual(kwargs['ep_params']['appInstanceId'], 10)
        self.assertEqual(kwargs['ep_params']['topicId'], 'topic1')
        self.assertEqual(kwargs['ep_params']['readStatus'], True)
        self.assertEqual(kwargs['ep_params']['lang'], 'en')

    def test_update_message_read_status(self):
        self.mock_adapter.put.return_value = {'updated': True}
        result = self.uc.update_message_read_status(
            location_id=123,
            message_id=456,
            read_status=True
        )
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_params']['locationId'], 123)
        self.assertEqual(kwargs['ep_params']['messageId'], 456)
        self.assertEqual(kwargs['ep_params']['readStatus'], True)
        self.assertEqual(result, {'updated': True})

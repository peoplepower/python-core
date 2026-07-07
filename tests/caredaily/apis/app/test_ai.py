import unittest
from unittest.mock import MagicMock

from caredaily.apis.app import AI


class TestAI(unittest.TestCase):
    def setUp(self):
        self.ai = AI()
        self.mock_adapter = MagicMock()
        self.ai.adapter = self.mock_adapter

    def test_send_openai_request(self):
        request_data = {
            'answer': {
                'model': 'gpt-4o',
                'messages': [{'role': 'user', 'content': 'Hello'}],
                'temperature': 0.7,
            }
        }
        self.mock_adapter.post.return_value = 'openai-result'
        result = self.ai.send_openai_request(
            location_id=123,
            openai_path=1,
            request_data=request_data,
            openai_organization='org-abc',
        )
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/openai')
        self.assertEqual(kwargs['ep_params']['locationId'], 123)
        self.assertEqual(kwargs['ep_params']['openAiPath'], 1)
        self.assertEqual(kwargs['ep_params']['openAiOrganization'], 'org-abc')
        self.assertEqual(kwargs['ep_json'], request_data)
        self.assertEqual(result, 'openai-result')

    def test_send_openai_request_no_organization(self):
        self.mock_adapter.post.return_value = 'openai-result'
        self.ai.send_openai_request(location_id=123, openai_path=1, request_data={})
        args, kwargs = self.mock_adapter.post.call_args
        self.assertNotIn('openAiOrganization', kwargs['ep_params'])

    def test_get_openai_token(self):
        self.mock_adapter.get.return_value = 'token-result'
        result = self.ai.get_openai_token(location_id=123, expiry=3600)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/openaiToken')
        self.assertEqual(kwargs['ep_params']['locationId'], 123)
        self.assertEqual(kwargs['ep_params']['expiry'], 3600)
        self.assertEqual(result, 'token-result')


if __name__ == '__main__':
    unittest.main()

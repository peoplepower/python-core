import unittest
from unittest.mock import MagicMock

from caredaily.apis.admin import Challenges


class TestChallenges(unittest.TestCase):
    def setUp(self):
        self.challenges = Challenges()
        self.mock_adapter = MagicMock()
        self.challenges.adapter = self.mock_adapter
        self.mock_adapter._headers = {'ADMIN_KEY': 'admin_key', 'USER_KEY': 'user_key'}
        self.mock_adapter._get_headers = MagicMock(return_value={'API_KEY': 'admin_key'})

    def test_create_challenge_success(self):
        challenge_data = {'challenge': {'name': 'Test Challenge'}}
        self.mock_adapter.post.return_value = {'challengeId': 1}
        result = self.challenges.create_challenge(
            organization_id=123,
            challenge_data=challenge_data
        )
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_json'], challenge_data)
        self.assertEqual(result, {'challengeId': 1})

    def test_create_challenge_with_check_and_parent(self):
        challenge_data = {'challenge': {'name': 'Test Challenge'}}
        self.mock_adapter.post.return_value = {'challengeId': 1}
        self.challenges.create_challenge(
            organization_id=123,
            challenge_data=challenge_data,
            check=True,
            parent_id=5
        )
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['check'], True)
        self.assertEqual(kwargs['ep_params']['parentId'], 5)

    def test_get_challenges_success(self):
        self.mock_adapter.get.return_value = {'challenges': []}
        self.mock_adapter._get_headers = MagicMock(return_value={'API_KEY': 'user_key'})
        result = self.challenges.get_challenges(organization_id=123)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params'], {})
        self.assertEqual(result, {'challenges': []})

    def test_get_challenges_with_all_filters(self):
        self.mock_adapter.get.return_value = {'challenges': []}
        self.mock_adapter._get_headers = MagicMock(return_value={'API_KEY': 'user_key'})
        self.challenges.get_challenges(
            organization_id=123,
            status=1,
            challenge_id=5,
            challenge_type=2,
            search_by='test',
            parent_id=10
        )
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['status'], 1)
        self.assertEqual(kwargs['ep_params']['challengeId'], 5)
        self.assertEqual(kwargs['ep_params']['challengeType'], 2)
        self.assertEqual(kwargs['ep_params']['searchBy'], 'test')
        self.assertEqual(kwargs['ep_params']['parentId'], 10)

    def test_update_challenge_success(self):
        challenge_data = {'challenge': {'name': 'Updated Challenge'}}
        self.mock_adapter.put.return_value = {'status': 'ok'}
        result = self.challenges.update_challenge(
            organization_id=123,
            challenge_id=1,
            challenge_data=challenge_data
        )
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_json'], challenge_data)
        self.assertEqual(result, {'status': 'ok'})

    def test_delete_challenge_success(self):
        self.mock_adapter.delete.return_value = {'status': 'ok'}
        result = self.challenges.delete_challenge(
            organization_id=123,
            challenge_id=1
        )
        self.mock_adapter.delete.assert_called_once()
        self.assertEqual(result, {'status': 'ok'})

    def test_update_challenge_status_success(self):
        self.mock_adapter.put.return_value = {'status': 'ok'}
        result = self.challenges.update_challenge_status(
            organization_id=123,
            challenge_id=1,
            status=1
        )
        self.mock_adapter.put.assert_called_once()
        self.assertEqual(result, {'status': 'ok'})

    def test_get_challenge_participants_success(self):
        self.mock_adapter.get.return_value = {'participants': []}
        self.mock_adapter._get_headers = MagicMock(return_value={'API_KEY': 'user_key'})
        result = self.challenges.get_challenge_participants(
            organization_id=123,
            challenge_id=1
        )
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params'], {})
        self.assertEqual(result, {'participants': []})

    def test_get_challenge_participants_with_filters(self):
        self.mock_adapter.get.return_value = {'participants': []}
        self.mock_adapter._get_headers = MagicMock(return_value={'API_KEY': 'user_key'})
        self.challenges.get_challenge_participants(
            organization_id=123,
            challenge_id=1,
            status=2,
            location_id=10
        )
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['status'], 2)
        self.assertEqual(kwargs['ep_params']['locationId'], 10)

    def test_update_challenge_participant_status_success(self):
        self.mock_adapter.put.return_value = {'resultCode': 0}
        self.mock_adapter._get_headers = MagicMock(return_value={'API_KEY': 'user_key'})
        result = self.challenges.update_challenge_participant_status(
            organization_id=123,
            challenge_id=1,
            status=2,
            location_id=10
        )
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_params']['status'], 2)
        self.assertEqual(kwargs['ep_params']['locationId'], 10)
        self.assertEqual(result, {'resultCode': 0})

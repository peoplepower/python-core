import unittest
from unittest.mock import MagicMock

from caredaily.apis.bot import DeveloperTeams


class TestDeveloperTeams(unittest.TestCase):
    def setUp(self):
        self.teams = DeveloperTeams()
        self.mock_adapter = MagicMock()
        self.teams.adapter = self.mock_adapter

    def test_create_team(self):
        self.mock_adapter.post.return_value = {'teamId': 1}
        result = self.teams.create_team('MyTeam', description='Team description')
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_json']['name'], 'MyTeam')
        self.assertEqual(kwargs['ep_json']['description'], 'Team description')
        self.assertEqual(result, {'teamId': 1})

    def test_create_team_without_description(self):
        self.mock_adapter.post.return_value = {'teamId': 1}
        self.teams.create_team('MyTeam')
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_json']['name'], 'MyTeam')
        self.assertNotIn('description', kwargs['ep_json'])

    def test_add_member(self):
        self.mock_adapter.post.return_value = {'status': 'ok'}
        result = self.teams.add_member('MyTeam', user_id=123, username='user1', tester=True)
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['teamName'], 'MyTeam')
        self.assertEqual(kwargs['ep_params']['userId'], 123)
        self.assertEqual(kwargs['ep_params']['username'], 'user1')
        self.assertEqual(kwargs['ep_params']['tester'], True)
        self.assertEqual(result, {'status': 'ok'})

    def test_add_member_with_user_id_only(self):
        self.mock_adapter.post.return_value = {'status': 'ok'}
        self.teams.add_member('MyTeam', user_id=123)
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['teamName'], 'MyTeam')
        self.assertEqual(kwargs['ep_params']['userId'], 123)
        self.assertNotIn('username', kwargs['ep_params'])
        self.assertNotIn('tester', kwargs['ep_params'])

    def test_add_member_with_username_only(self):
        self.mock_adapter.post.return_value = {'status': 'ok'}
        self.teams.add_member('MyTeam', username='user1')
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['teamName'], 'MyTeam')
        self.assertEqual(kwargs['ep_params']['username'], 'user1')
        self.assertNotIn('userId', kwargs['ep_params'])

    def test_add_member_with_tester_flag(self):
        self.mock_adapter.post.return_value = {'status': 'ok'}
        self.teams.add_member('MyTeam', user_id=123, tester=False)
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['tester'], False)

    def test_remove_member(self):
        self.mock_adapter.delete.return_value = {'status': 'ok'}
        result = self.teams.remove_member('MyTeam', user_id=123, username='user1')
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(kwargs['ep_params']['teamName'], 'MyTeam')
        self.assertEqual(kwargs['ep_params']['userId'], 123)
        self.assertEqual(kwargs['ep_params']['username'], 'user1')
        self.assertEqual(result, {'status': 'ok'})

    def test_remove_member_with_user_id_only(self):
        self.mock_adapter.delete.return_value = {'status': 'ok'}
        self.teams.remove_member('MyTeam', user_id=123)
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(kwargs['ep_params']['teamName'], 'MyTeam')
        self.assertEqual(kwargs['ep_params']['userId'], 123)
        self.assertNotIn('username', kwargs['ep_params'])

    def test_remove_member_with_username_only(self):
        self.mock_adapter.delete.return_value = {'status': 'ok'}
        self.teams.remove_member('MyTeam', username='user1')
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(kwargs['ep_params']['teamName'], 'MyTeam')
        self.assertEqual(kwargs['ep_params']['username'], 'user1')
        self.assertNotIn('userId', kwargs['ep_params'])

    def test_get_teams(self):
        self.mock_adapter.get.return_value = {'teams': []}
        result = self.teams.get_teams(team_name='MyTeam', user_id=123, bundle='com.example.bot')
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['teamName'], 'MyTeam')
        self.assertEqual(kwargs['ep_params']['userId'], 123)
        self.assertEqual(kwargs['ep_params']['bundle'], 'com.example.bot')
        self.assertEqual(result, {'teams': []})

    def test_get_teams_with_team_name_only(self):
        self.mock_adapter.get.return_value = {'teams': []}
        self.teams.get_teams(team_name='MyTeam')
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['teamName'], 'MyTeam')
        self.assertNotIn('userId', kwargs['ep_params'])
        self.assertNotIn('bundle', kwargs['ep_params'])

    def test_get_teams_with_user_id_only(self):
        self.mock_adapter.get.return_value = {'teams': []}
        self.teams.get_teams(user_id=123)
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['userId'], 123)
        self.assertNotIn('teamName', kwargs['ep_params'])
        self.assertNotIn('bundle', kwargs['ep_params'])

    def test_get_teams_with_bundle_only(self):
        self.mock_adapter.get.return_value = {'teams': []}
        self.teams.get_teams(bundle='com.example.bot')
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['bundle'], 'com.example.bot')
        self.assertNotIn('teamName', kwargs['ep_params'])
        self.assertNotIn('userId', kwargs['ep_params'])

    def test_get_teams_minimal(self):
        self.mock_adapter.get.return_value = {'teams': []}
        result = self.teams.get_teams()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params'], {})
        self.assertEqual(result, {'teams': []})

    def test_add_developer_to_team_with_user_id(self):
        """Test add_developer_to_team with user_id"""
        team_name = 'MyTeam'
        user_id = 123
        self.mock_adapter.post.return_value = {'status': 'ok'}
        result = self.teams.add_developer_to_team(team_name=team_name, user_id=user_id)
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(args[0], f'/espapi/cloud/developer/teams/{team_name}')
        self.assertEqual(kwargs['ep_params']['userId'], user_id)
        self.assertNotIn('username', kwargs['ep_params'])
        self.assertEqual(result, {'status': 'ok'})

    def test_add_developer_to_team_with_username(self):
        """Test add_developer_to_team with username"""
        team_name = 'MyTeam'
        username = 'user1'
        self.mock_adapter.post.return_value = {'status': 'ok'}
        result = self.teams.add_developer_to_team(team_name=team_name, username=username)
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['username'], username)
        self.assertNotIn('userId', kwargs['ep_params'])
        self.assertEqual(result, {'status': 'ok'})

    def test_add_developer_to_team_with_tester_true(self):
        """Test add_developer_to_team with tester=True"""
        team_name = 'MyTeam'
        user_id = 123
        tester = True
        self.mock_adapter.post.return_value = {'status': 'ok'}
        result = self.teams.add_developer_to_team(team_name=team_name, user_id=user_id, tester=tester)
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['tester'], tester)
        self.assertEqual(result, {'status': 'ok'})

    def test_add_developer_to_team_with_tester_false(self):
        """Test add_developer_to_team with tester=False"""
        team_name = 'MyTeam'
        user_id = 123
        tester = False
        self.mock_adapter.post.return_value = {'status': 'ok'}
        result = self.teams.add_developer_to_team(team_name=team_name, user_id=user_id, tester=tester)
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['tester'], tester)
        self.assertEqual(result, {'status': 'ok'})

    def test_add_developer_to_team_with_all_params(self):
        """Test add_developer_to_team with all optional parameters"""
        team_name = 'MyTeam'
        user_id = 123
        username = 'user1'
        tester = True
        self.mock_adapter.post.return_value = {'status': 'ok'}
        result = self.teams.add_developer_to_team(
            team_name=team_name,
            user_id=user_id,
            username=username,
            tester=tester
        )
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['userId'], user_id)
        self.assertEqual(kwargs['ep_params']['username'], username)
        self.assertEqual(kwargs['ep_params']['tester'], tester)
        self.assertEqual(result, {'status': 'ok'})

    def test_remove_developer_from_team_with_user_id(self):
        """Test remove_developer_from_team with user_id"""
        team_name = 'MyTeam'
        user_id = 123
        self.mock_adapter.delete.return_value = {'status': 'ok'}
        result = self.teams.remove_developer_from_team(team_name=team_name, user_id=user_id)
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(args[0], f'/espapi/cloud/developer/teams/{team_name}')
        self.assertEqual(kwargs['ep_params']['userId'], user_id)
        self.assertNotIn('username', kwargs['ep_params'])
        self.assertEqual(result, {'status': 'ok'})

    def test_remove_developer_from_team_with_username(self):
        """Test remove_developer_from_team with username"""
        team_name = 'MyTeam'
        username = 'user1'
        self.mock_adapter.delete.return_value = {'status': 'ok'}
        result = self.teams.remove_developer_from_team(team_name=team_name, username=username)
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(kwargs['ep_params']['username'], username)
        self.assertNotIn('userId', kwargs['ep_params'])
        self.assertEqual(result, {'status': 'ok'})

    def test_remove_developer_from_team_with_all_params(self):
        """Test remove_developer_from_team with both user_id and username"""
        team_name = 'MyTeam'
        user_id = 123
        username = 'user1'
        self.mock_adapter.delete.return_value = {'status': 'ok'}
        result = self.teams.remove_developer_from_team(
            team_name=team_name,
            user_id=user_id,
            username=username
        )
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(kwargs['ep_params']['userId'], user_id)
        self.assertEqual(kwargs['ep_params']['username'], username)
        self.assertEqual(result, {'status': 'ok'})

    def test_get_team_secrets(self):
        """Test get_team_secrets"""
        team_name = 'MyTeam'
        self.mock_adapter.get.return_value = {'secrets': ['secret1', 'secret2']}
        result = self.teams.get_team_secrets(team_name=team_name)
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], f'/espapi/cloud/developer/teams/{team_name}/secrets')
        self.assertEqual(result, {'secrets': ['secret1', 'secret2']})

    def test_put_team_secret(self):
        """Test put_team_secret"""
        team_name = 'MyTeam'
        secret_name = 'api_key'
        secret_value = 'secret_value_123'
        self.mock_adapter.put.return_value = {'status': 'ok'}
        result = self.teams.put_team_secret(
            team_name=team_name,
            secret_name=secret_name,
            secret_value=secret_value
        )
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], f'/espapi/cloud/developer/teams/{team_name}/secrets')
        self.assertEqual(kwargs['ep_params']['secretName'], secret_name)
        self.assertEqual(kwargs['ep_json']['secretValue'], secret_value)
        self.assertEqual(result, {'status': 'ok'})

    def test_delete_team_secret(self):
        """Test delete_team_secret"""
        team_name = 'MyTeam'
        secret_name = 'api_key'
        self.mock_adapter.delete.return_value = {'status': 'ok'}
        result = self.teams.delete_team_secret(
            team_name=team_name,
            secret_name=secret_name
        )
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(args[0], f'/espapi/cloud/developer/teams/{team_name}/secrets')
        self.assertEqual(kwargs['ep_params']['secretName'], secret_name)
        self.assertEqual(result, {'status': 'ok'})

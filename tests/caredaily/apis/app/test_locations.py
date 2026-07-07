import unittest
import json
from unittest.mock import MagicMock
from caredaily.apis.app import Locations
from caredaily.models import APIKeyType

class TestLocations(unittest.TestCase):
    def setUp(self):
        self.loc = Locations()
        self.mock_adapter = MagicMock()
        self.loc.adapter = self.mock_adapter
        self.mock_adapter._headers = {}
        self.mock_adapter._get_headers = MagicMock(return_value={'API_KEY': 'test_key'})

    def test_create_location(self):
        location_data = {'name': 'Test Location', 'type': 'residential'}
        self.mock_adapter.post.return_value = 'create-result'
        result = self.loc.create_location(data=location_data)
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(args[0], '/cloud/json/location')
        self.assertEqual(kwargs['ep_json'], json.dumps(location_data))
        self.assertEqual(result, 'create-result')

    def test_update_location(self):
        self.mock_adapter.put.return_value = 'update-location-result'
        result = self.loc.update_location(location_id=1, data={'a': 1}, analytic_key='key')
        self.mock_adapter.put.assert_called_once()
        self.assertEqual(result, 'update-location-result')

    def test_update_location_with_analytic_key(self):
        location_data = {'name': 'Updated Location'}
        self.mock_adapter._get_headers.return_value = {'API_KEY': 'analytic_key'}
        self.mock_adapter.put.return_value = 'update-result'
        result = self.loc.update_location(location_id=1, data=location_data, analytic_key='analytic_key')
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/cloud/json/location/1')
        self.assertEqual(kwargs['ep_json'], json.dumps(location_data))
        self.mock_adapter._get_headers.assert_called_once_with('analytic_key', APIKeyType.ANALYTIC)
        self.assertEqual(result, 'update-result')

    def test_delete_location(self):
        self.mock_adapter.delete.return_value = 'delete-result'
        result = self.loc.delete_location(location_id=1)
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(args[0], '/cloud/json/location/1')
        self.assertEqual(result, 'delete-result')

    def test_put_location_to_organization(self):
        self.mock_adapter.put.return_value = 'put-org-result'
        result = self.loc.put_location_to_organization(location_id=1, organization_id=2)
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/cloud/json/location/1/organization')
        self.assertEqual(kwargs['ep_params']['organizationId'], 2)
        self.assertEqual(result, 'put-org-result')

    def test_post_location_event(self):
        event_data = {'eventType': 'test', 'timestamp': 1234567890}
        self.mock_adapter.post.return_value = 'event-result'
        result = self.loc.post_location_event(location_id=1, event=event_data)
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(args[0], '/cloud/json/location/1/events')
        self.assertEqual(kwargs['ep_json'], json.dumps(event_data))
        self.assertEqual(result, 'event-result')

    def test_get_location_events_history(self):
        self.mock_adapter.get.return_value = 'events-history-result'
        result = self.loc.get_location_events_history(location_id=1, start_date_ms=1000, end_date_ms=2000)
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, 'events-history-result')

    def test_get_location_events_history_partial_params(self):
        self.mock_adapter.get.return_value = 'events-result'
        result = self.loc.get_location_events_history(location_id=1, start_date_ms=1000)
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['startDate'], 1000)
        self.assertNotIn('endDate', kwargs['ep_params'])
        self.assertEqual(result, 'events-result')

    def test_get_location_priorities_history(self):
        self.mock_adapter.get.return_value = 'priorities-result'
        result = self.loc.get_location_priorities_history(location_id=1, start_date_ms=1000, end_date_ms=2000)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/cloud/json/location/1/priorities')
        self.assertEqual(kwargs['ep_params']['startDate'], 1000)
        self.assertEqual(kwargs['ep_params']['endDate'], 2000)
        self.assertEqual(result, 'priorities-result')

    def test_get_countries(self):
        self.mock_adapter.get.return_value = 'countries-result'
        result = self.loc.get_countries(state_id=1)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/cloud/json/countries')
        self.assertEqual(kwargs['ep_params']['stateId'], 1)
        self.assertEqual(result, 'countries-result')

    def test_get_countries_no_state(self):
        self.mock_adapter.get.return_value = 'countries-result'
        result = self.loc.get_countries()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params'], {})
        self.assertEqual(result, 'countries-result')

    def test_get_location_users(self):
        self.mock_adapter.get.return_value = 'users-result'
        result = self.loc.get_location_users(location_id=1)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/cloud/json/location/1/users')
        self.assertEqual(result, 'users-result')

    def test_add_location_users(self):
        users_data = [{'userId': 1, 'locationAccess': 2}]
        self.mock_adapter.post.return_value = 'add-users-result'
        result = self.loc.add_location_users(location_id=1, users=users_data)
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(args[0], '/cloud/json/location/1/users')
        self.assertEqual(kwargs['ep_json'], json.dumps({'users': users_data}))
        self.assertEqual(result, 'add-users-result')

    def test_update_location_user(self):
        self.mock_adapter.put.return_value = 'update-user-result'
        result = self.loc.update_location_user(location_id=1, user_id=2, location_access=3, temporary=True)
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/cloud/json/location/1/users/2')
        self.assertEqual(kwargs['ep_params']['locationAccess'], 3)
        self.assertEqual(kwargs['ep_params']['temporary'], True)
        self.assertEqual(result, 'update-user-result')

    def test_update_location_user_partial_params(self):
        self.mock_adapter.put.return_value = 'update-user-result'
        result = self.loc.update_location_user(location_id=1, user_id=2)
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_params'], {})
        self.assertEqual(result, 'update-user-result')

    def test_delete_location_user(self):
        self.mock_adapter.delete.return_value = 'delete-user-result'
        result = self.loc.delete_location_user(location_id=1, user_id=2)
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(args[0], '/cloud/json/location/1/users/2')
        self.assertEqual(result, 'delete-user-result')

    def test_add_sub_location(self):
        self.mock_adapter.post.return_value = 'add-sub-result'
        result = self.loc.add_sub_location(location_id=1, sub_location_id=2)
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(args[0], '/cloud/json/location/1/subLocations')
        self.assertEqual(kwargs['ep_params']['subLocationId'], 2)
        self.assertEqual(result, 'add-sub-result')

    def test_delete_sub_location(self):
        self.mock_adapter.delete.return_value = 'delete-sub-result'
        result = self.loc.delete_sub_location(location_id=1, sub_location_id=2)
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(args[0], '/cloud/json/location/1/subLocations')
        self.assertEqual(kwargs['ep_params']['subLocationId'], 2)
        self.assertEqual(result, 'delete-sub-result')

    def test_get_location_spaces(self):
        self.mock_adapter.get.return_value = 'spaces-result'
        result = self.loc.get_location_spaces(location_id=1)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/cloud/json/location/1/spaces')
        self.assertEqual(result, 'spaces-result')

    def test_delete_location_space(self):
        self.mock_adapter.delete.return_value = 'delete-space-result'
        result = self.loc.delete_location_space(location_id=1, space_id=2)
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(args[0], '/cloud/json/location/1/spaces')
        self.assertEqual(kwargs['ep_params']['spaceId'], 2)
        self.assertEqual(result, 'delete-space-result')

    def test_get_narratives(self):
        self.mock_adapter.get.return_value = 'narratives-result'
        result = self.loc.get_narratives(location_id=1, row_count=10, narrative_type=1, scope=2)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/cloud/json/locations/1/narratives')
        self.assertEqual(kwargs['ep_params']['rowCount'], 10)
        self.assertEqual(kwargs['ep_params']['narrativeType'], 1)
        self.assertEqual(kwargs['ep_params']['scope'], 2)
        self.assertEqual(result, 'narratives-result')

    def test_get_narratives_with_analytic_key(self):
        self.mock_adapter._get_headers.return_value = {'API_KEY': 'analytic_key'}
        self.mock_adapter.get.return_value = 'narratives-result'
        result = self.loc.get_narratives(location_id=1, row_count=10, analytic_key='key')
        args, kwargs = self.mock_adapter.get.call_args
        self.mock_adapter._get_headers.assert_called_once_with('key', APIKeyType.ANALYTIC)
        self.assertEqual(result, 'narratives-result')

    def test_put_narrative(self):
        narrative_data = {'text': 'Test narrative'}
        self.mock_adapter.put.return_value = 'put-narrative-result'
        result = self.loc.put_narrative(location_id=1, scope=2, narrative=narrative_data, publish=True)
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/cloud/json/locations/1/narratives')
        self.assertEqual(kwargs['ep_json'], json.dumps(narrative_data))
        self.assertEqual(kwargs['ep_params']['scope'], 2)
        self.assertEqual(kwargs['ep_params']['publish'], True)
        self.assertEqual(result, 'put-narrative-result')

    def test_put_narrative_with_analytic_key(self):
        narrative_data = {'text': 'Test'}
        self.mock_adapter._get_headers.return_value = {'API_KEY': 'analytic_key'}
        self.mock_adapter.put.return_value = 'result'
        result = self.loc.put_narrative(location_id=1, scope=2, narrative=narrative_data, analytic_key='key')
        self.mock_adapter._get_headers.assert_called_once_with('key', APIKeyType.ANALYTIC)
        self.assertEqual(result, 'result')

    def test_delete_a_narrative(self):
        self.mock_adapter.delete.return_value = 'delete-narrative-result'
        result = self.loc.delete_a_narrative(location_id=1, scope=2, narrative_id=3, narrative_time_ms=1000)
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(args[0], '/cloud/json/locations/1/narratives')
        self.assertEqual(kwargs['ep_params']['scope'], 2)
        self.assertEqual(kwargs['ep_params']['narrativeId'], 3)
        self.assertEqual(kwargs['ep_params']['narrativeTime'], 1000)
        self.assertEqual(result, 'delete-narrative-result')

    def test_delete_a_narrative_with_analytic_key(self):
        self.mock_adapter._get_headers.return_value = {'API_KEY': 'analytic_key'}
        self.mock_adapter.delete.return_value = 'result'
        result = self.loc.delete_a_narrative(location_id=1, scope=2, narrative_id=3, narrative_time_ms=1000, analytic_key='key')
        self.mock_adapter._get_headers.assert_called_once_with('key', APIKeyType.ANALYTIC)
        self.assertEqual(result, 'result')

    def test_stream_message(self):
        feed_data = {'message': 'test'}
        self.mock_adapter._get_headers.return_value = {'API_KEY': 'test_key'}
        self.mock_adapter.post.return_value = 'stream-result'
        result = self.loc.stream_message(scope='test', address='addr', feed=feed_data, location_id=1)
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(args[0], '/espapi/cloud/appstore/stream')
        self.assertEqual(kwargs['ep_params']['scope'], 'test')
        self.assertEqual(kwargs['ep_params']['address'], 'addr')
        self.assertEqual(kwargs['ep_params']['locationId'], 1)
        self.assertEqual(kwargs['ep_json']['feed'], feed_data)
        self.assertEqual(result, 'stream-result')

    def test_stream_message_with_admin_key(self):
        feed_data = {'message': 'test'}
        self.mock_adapter._headers = {'ADMIN_KEY': 'admin_key'}
        self.mock_adapter._get_headers.return_value = {'API_KEY': 'user_key'}
        self.mock_adapter.post.return_value = 'stream-result'
        result = self.loc.stream_message(scope='test', address='addr', feed=feed_data)
        self.mock_adapter._get_headers.assert_called_with('admin_key', key_type=APIKeyType.USER)
        self.assertEqual(result, 'stream-result')

    def test_get_summary(self):
        self.mock_adapter._get_headers.return_value = {'API_KEY': 'test_key'}
        self.mock_adapter.get.return_value = 'summary-result'
        result = self.loc.get_summary(location_id=1, organization_id=2)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/cloud/appstore/summary')
        self.assertEqual(kwargs['ep_params']['locationId'], 1)
        self.assertEqual(kwargs['ep_params']['organizationId'], 2)
        self.assertEqual(result, 'summary-result')

    def test_get_summary_with_admin_key(self):
        self.mock_adapter._headers = {'ADMIN_KEY': 'admin_key'}
        self.mock_adapter._get_headers.return_value = {'API_KEY': 'user_key'}
        self.mock_adapter.get.return_value = 'summary-result'
        result = self.loc.get_summary(location_id=1)
        self.mock_adapter._get_headers.assert_called_with('admin_key', key_type=APIKeyType.USER)
        self.assertEqual(result, 'summary-result')

    def test_put_state(self):
        state_data = {'value': 'test'}
        self.mock_adapter.put.return_value = 'put-state-result'
        result = self.loc.put_state(location_id=1, name='state_name', state=state_data, overwrite=True)
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/cloud/json/locations/1/state')
        self.assertEqual(kwargs['ep_json'], json.dumps(state_data))
        self.assertEqual(kwargs['ep_params']['name'], 'state_name')
        self.assertEqual(kwargs['ep_params']['overwrite'], True)
        self.assertEqual(result, 'put-state-result')

    def test_get_state(self):
        self.mock_adapter.get.return_value = 'get-state-result'
        result = self.loc.get_state(location_id=1, name='state_name')
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/cloud/json/locations/1/state')
        self.assertEqual(kwargs['ep_params']['name'], 'state_name')
        self.assertEqual(result, 'get-state-result')

    def test_get_state_with_list(self):
        self.mock_adapter.get.return_value = 'get-state-result'
        result = self.loc.get_state(location_id=1, name=['state1', 'state2'])
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['name'], ['state1', 'state2'])
        self.assertEqual(result, 'get-state-result')

    def test_delete_all_location_states(self):
        self.mock_adapter.delete.return_value = 'delete-states-result'
        result = self.loc.delete_all_location_states(location_id=1)
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(args[0], '/cloud/json/locations/1/state')
        self.assertEqual(kwargs['ep_params']['locationId'], 1)
        self.assertEqual(result, 'delete-states-result')

    def test_put_time_state(self):
        state_data = {'value': 'test'}
        self.mock_adapter.put.return_value = 'put-time-state-result'
        result = self.loc.put_time_state(location_id=1, name='state_name', timestamp_ms=1000, state=state_data)
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/cloud/json/locations/1/timeStates')
        self.assertEqual(kwargs['ep_json'], json.dumps(state_data))
        self.assertEqual(kwargs['ep_params']['name'], 'state_name')
        self.assertEqual(kwargs['ep_params']['timestampMs'], 1000)
        self.assertEqual(result, 'put-time-state-result')

    def test_get_time_state(self):
        self.mock_adapter.get.return_value = 'get-time-state-result'
        result = self.loc.get_time_state(location_id=1, start_date_ms=1000, end_date_ms=2000, name='state_name')
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/cloud/json/locations/1/timeStates')
        self.assertEqual(kwargs['ep_params']['startDate'], 1000)
        self.assertEqual(kwargs['ep_params']['endDate'], 2000)
        self.assertEqual(kwargs['ep_params']['name'], 'state_name')
        self.assertEqual(result, 'get-time-state-result')

    def test_get_location_totals(self):
        self.mock_adapter.get.return_value = 'totals-result'
        result = self.loc.get_location_totals(organization_id=1)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/cloud/json/locationTotals')
        self.assertEqual(kwargs['ep_params']['organizationId'], 1)
        self.assertEqual(result, 'totals-result')

    def test_get_location_totals_no_org(self):
        self.mock_adapter.get.return_value = 'totals-result'
        result = self.loc.get_location_totals()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params'], {})
        self.assertEqual(result, 'totals-result')

    def test_get_presence_ids(self):
        self.mock_adapter.get.return_value = 'presence-ids-result'
        result = self.loc.get_presence_ids(location_id=1)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/cloud/json/location/1/presence')
        self.assertEqual(result, 'presence-ids-result')

    def test_add_location_presence(self):
        presence_data = {'presenceId': 1, 'name': 'Home'}
        self.mock_adapter.post.return_value = 'add-presence-result'
        result = self.loc.add_location_presence(location_id=1, presence_data=presence_data)
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(args[0], '/cloud/json/location/1/presence')
        self.assertEqual(kwargs['ep_json'], json.dumps(presence_data))
        self.assertEqual(result, 'add-presence-result')


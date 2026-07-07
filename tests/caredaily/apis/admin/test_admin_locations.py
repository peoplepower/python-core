import unittest
from unittest.mock import MagicMock

from caredaily.apis.admin import Locations


class TestLocations(unittest.TestCase):
    def setUp(self):
        self.locations = Locations()
        self.mock_adapter = MagicMock()
        self.locations.adapter = self.mock_adapter
        self.mock_adapter._headers = {'ADMIN_KEY': 'admin_key'}
        self.mock_adapter._get_headers = MagicMock(return_value={'API_KEY': 'admin_key'})

    def test_get_organization_locations_success(self):
        self.mock_adapter.get.return_value = {'locations': []}
        result = self.locations.get_organization_locations(organization_id=123)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['organizationId'], 123)
        self.assertEqual(result, {'locations': []})

    def test_get_organization_locations_with_filters(self):
        self.mock_adapter.get.return_value = {'locations': []}
        self.locations.get_organization_locations(
            organization_id=123,
            location_id=5,
            sub_type=1,
            external_id='ext123',
            search_by='home*',
            event='test',
            location_type=2,
            exclude_type=3,
            search_tag='tag1',
            search_device_tag='devtag1',
            device_type=10,
            service_plan_id=1,
            state_id=5,
            country_id=1,
            priority_category=2,
            external_user_id='user123',
            user_role=1,
            state_name='temp',
            get_tags=True,
            limit=50
        )
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['organizationId'], 123)
        self.assertEqual(kwargs['ep_params']['locationId'], 5)
        self.assertEqual(kwargs['ep_params']['subType'], 1)
        self.assertEqual(kwargs['ep_params']['externalId'], 'ext123')
        self.assertEqual(kwargs['ep_params']['searchBy'], 'home*')
        self.assertEqual(kwargs['ep_params']['event'], 'test')
        self.assertEqual(kwargs['ep_params']['locationType'], 2)
        self.assertEqual(kwargs['ep_params']['excludeType'], 3)
        self.assertEqual(kwargs['ep_params']['searchTag'], 'tag1')
        self.assertEqual(kwargs['ep_params']['searchDeviceTag'], 'devtag1')
        self.assertEqual(kwargs['ep_params']['deviceType'], 10)
        self.assertEqual(kwargs['ep_params']['servicePlanId'], 1)
        self.assertEqual(kwargs['ep_params']['stateId'], 5)
        self.assertEqual(kwargs['ep_params']['countryId'], 1)
        self.assertEqual(kwargs['ep_params']['priorityCategory'], 2)
        self.assertEqual(kwargs['ep_params']['externalUserId'], 'user123')
        self.assertEqual(kwargs['ep_params']['userRole'], 1)
        self.assertEqual(kwargs['ep_params']['stateName'], 'temp')
        self.assertEqual(kwargs['ep_params']['getTags'], True)
        self.assertEqual(kwargs['ep_params']['limit'], 50)

    def test_create_organization_location_success(self):
        location_data = {'location': {'name': 'Test Location'}}
        self.mock_adapter.post.return_value = {'locationId': 1}
        result = self.locations.create_organization_location(
            organization_id=123,
            location_data=location_data
        )
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_json'], location_data)
        self.assertEqual(result, {'locationId': 1})

    def test_create_organization_location_with_parent_and_user(self):
        location_data = {'location': {'name': 'Test Location'}}
        self.mock_adapter.post.return_value = {'locationId': 1}
        self.locations.create_organization_location(
            organization_id=123,
            location_data=location_data,
            parent_id=10,
            user_id=20
        )
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['parentId'], 10)
        self.assertEqual(kwargs['ep_params']['userId'], 20)

    def test_update_organization_location_success(self):
        location_data = {'location': {'name': 'Updated Location'}}
        self.mock_adapter.put.return_value = {'status': 'ok'}
        result = self.locations.update_organization_location(
            organization_id=123,
            location_id=1,
            location_data=location_data
        )
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_params']['locationId'], 1)
        self.assertEqual(kwargs['ep_json'], location_data)
        self.assertEqual(result, {'status': 'ok'})

    def test_delete_organization_location_success(self):
        self.mock_adapter.delete.return_value = {'status': 'ok'}
        result = self.locations.delete_organization_location(
            organization_id=123,
            location_id=1
        )
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(kwargs['ep_params']['locationId'], 1)
        self.assertEqual(result, {'status': 'ok'})

    def test_add_update_delete_organization_locations_success(self):
        location_ids = [1, 2, 3]
        self.mock_adapter.put.return_value = {'status': 'ok'}
        result = self.locations.add_update_delete_organization_locations(
            organization_id=123,
            location_ids=location_ids,
            notes='Test notes',
            delete=False
        )
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_json']['locationIds'], location_ids)
        self.assertEqual(kwargs['ep_json']['notes'], 'Test notes')
        self.assertEqual(kwargs['ep_json']['delete'], False)
        self.assertEqual(result, {'status': 'ok'})

    def test_add_update_delete_organization_locations_delete(self):
        location_ids = [1, 2]
        self.mock_adapter.put.return_value = {'status': 'ok'}
        self.locations.add_update_delete_organization_locations(
            organization_id=123,
            location_ids=location_ids,
            delete=True
        )
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_json']['delete'], True)
        self.assertNotIn('notes', kwargs['ep_json'])

    def test_add_update_delete_organization_locations_start_date(self):
        self.mock_adapter.put.return_value = {'status': 'ok'}
        result = self.locations.add_update_delete_organization_locations(
            organization_id=123,
            location_ids=[1],
            start_date='2026-01-01'
        )
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/espapi/admin/json/organizations/123/locationStatus')
        self.assertEqual(kwargs['ep_json']['startDate'], '2026-01-01')
        self.assertEqual(result, {'status': 'ok'})
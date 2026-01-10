import unittest
from unittest.mock import MagicMock

from caredaily.apis.admin import Organizations
from caredaily.models import APIKeyType


class TestOrganizations(unittest.TestCase):
    def setUp(self):
        self.org = Organizations()
        self.mock_adapter = MagicMock()
        self.org.adapter = self.mock_adapter

    def test_get_organizations_success(self):
        self.mock_adapter.get.return_value = {'status': 'ok'}
        result = self.org.get_organizations(organization_id=1, domain_name='test.com', name='TestOrg')
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, {'status': 'ok'})

    def test_get_organizations_filters_none(self):
        self.org.get_organizations(organization_id=None, domain_name=None, name=None)
        args, kwargs = self.mock_adapter.get.call_args
        self.assertIn('ep_params', kwargs)
        self.assertEqual(kwargs['ep_params'], {})

    def test_create_organization_success(self):
        organization_data = {'organization': {'name': 'Test Org', 'domain': 'test.com'}}
        self.mock_adapter.post.return_value = {'organizationId': 123}
        self.mock_adapter._headers = {'ADMIN_KEY': 'admin_key'}
        self.mock_adapter._get_headers = MagicMock(return_value={'API_KEY': 'admin_key'})
        result = self.org.create_organization(organization_data, parent_organization_id=1)
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_json'], organization_data)
        self.assertEqual(kwargs['ep_params']['organizationId'], 1)
        self.assertEqual(result, {'organizationId': 123})

    def test_create_organization_no_parent(self):
        organization_data = {'organization': {'name': 'Test Org'}}
        self.mock_adapter.post.return_value = {'organizationId': 123}
        self.mock_adapter._headers = {'ADMIN_KEY': 'admin_key'}
        self.mock_adapter._get_headers = MagicMock(return_value={'API_KEY': 'admin_key'})
        result = self.org.create_organization(organization_data)
        args, kwargs = self.mock_adapter.post.call_args
        self.assertNotIn('organizationId', kwargs['ep_params'])

    def test_edit_organization_success(self):
        organization_data = {'organization': {'name': 'Updated Org'}}
        self.mock_adapter.put.return_value = {'status': 'ok'}
        self.mock_adapter._headers = {'ADMIN_KEY': 'admin_key'}
        self.mock_adapter._get_headers = MagicMock(return_value={'API_KEY': 'admin_key'})
        result = self.org.edit_organization(organization_id=123, organization_data=organization_data)
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_params']['organizationId'], 123)
        self.assertEqual(kwargs['ep_json'], organization_data)
        self.assertEqual(result, {'status': 'ok'})

    def test_delete_organization_success(self):
        self.mock_adapter.delete.return_value = {'status': 'ok'}
        self.mock_adapter._headers = {'ADMIN_KEY': 'admin_key'}
        self.mock_adapter._get_headers = MagicMock(return_value={'API_KEY': 'admin_key'})
        result = self.org.delete_organization(organization_id=123)
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(kwargs['ep_params']['organizationId'], 123)
        self.assertEqual(result, {'status': 'ok'})

    def test_get_organization_totals_success(self):
        self.mock_adapter.get.return_value = {'locationsCount': 5, 'organizationDevices': 10}
        self.mock_adapter._headers = {'ADMIN_KEY': 'admin_key'}
        self.mock_adapter._get_headers = MagicMock(return_value={'API_KEY': 'admin_key'})
        result = self.org.get_organization_totals(organization_id=123, locations=True, user_devices=True)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['locations'], True)
        self.assertEqual(kwargs['ep_params']['userDevices'], True)
        self.assertEqual(result, {'locationsCount': 5, 'organizationDevices': 10})

    def test_get_organization_totals_no_params(self):
        self.mock_adapter.get.return_value = {'locationsCount': 5}
        self.mock_adapter._headers = {'ADMIN_KEY': 'admin_key'}
        self.mock_adapter._get_headers = MagicMock(return_value={'API_KEY': 'admin_key'})
        self.org.get_organization_totals(organization_id=123)
        args, kwargs = self.mock_adapter.get.call_args
        self.assertNotIn('locations', kwargs['ep_params'])
        self.assertNotIn('userDevices', kwargs['ep_params'])

    def test_get_brands_success(self):
        self.mock_adapter.get.return_value = {'brands': [{'name': 'default'}]}
        self.mock_adapter._headers = {'ADMIN_KEY': 'admin_key'}
        self.mock_adapter._get_headers = MagicMock(return_value={'API_KEY': 'admin_key'})
        result = self.org.get_brands()
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, {'brands': [{'name': 'default'}]})

    def test_get_organization_objects_success(self):
        self.mock_adapter.get.return_value = {'organizationObjects': []}
        self.mock_adapter._headers = {'USER_KEY': 'user_key'}
        self.mock_adapter._get_headers = MagicMock(return_value={'API_KEY': 'user_key'})
        result = self.org.get_organization_objects(organization_id=123)
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, {'organizationObjects': []})

    def test_set_organization_properties_success(self):
        org_objects = {'organizationObjects': [{'name': 'backgroundColour', 'value': '777'}]}
        self.mock_adapter.post.return_value = {'resultCode': 0}
        self.mock_adapter._headers = {'ADMIN_KEY': 'admin_key'}
        self.mock_adapter._get_headers = MagicMock(return_value={'API_KEY': 'admin_key'})
        result = self.org.set_organization_properties(organization_id=123, organization_objects=org_objects)
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_json'], org_objects)
        self.assertEqual(result, {'resultCode': 0})

    def test_get_organization_object_success(self):
        self.mock_adapter.get.return_value = b'object content'
        self.mock_adapter._headers = {'ADMIN_KEY': 'admin_key'}
        self.mock_adapter._get_headers = MagicMock(return_value={'API_KEY': 'admin_key'})
        result = self.org.get_organization_object(organization_id=123, object_name='logo')
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, b'object content')

    def test_upload_organization_object_success(self):
        object_data = b'binary data'
        self.mock_adapter.put.return_value = {'resultCode': 0}
        self.mock_adapter._headers = {'ADMIN_KEY': 'admin_key'}
        mock_headers = {'API_KEY': 'admin_key', 'Content-Type': 'image/png'}
        self.mock_adapter._get_headers = MagicMock(return_value={'API_KEY': 'admin_key'})
        result = self.org.upload_organization_object(
            organization_id=123,
            object_name='logo',
            object_data=object_data,
            content_type='image/png',
            private=False
        )
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_data'], object_data)
        self.assertEqual(kwargs['ep_params']['private'], False)
        self.assertEqual(kwargs['ep_headers']['Content-Type'], 'image/png')
        self.assertEqual(result, {'resultCode': 0})

    def test_delete_organization_object_success(self):
        self.mock_adapter.delete.return_value = {'resultCode': 0}
        self.mock_adapter._headers = {'ADMIN_KEY': 'admin_key'}
        self.mock_adapter._get_headers = MagicMock(return_value={'API_KEY': 'admin_key'})
        result = self.org.delete_organization_object(organization_id=123, object_name='logo')
        self.mock_adapter.delete.assert_called_once()
        self.assertEqual(result, {'resultCode': 0})

    def test_get_ehr_facilities_success(self):
        self.mock_adapter.get.return_value = {'facilities': []}
        self.mock_adapter._headers = {'ADMIN_KEY': 'admin_key'}
        self.mock_adapter._get_headers = MagicMock(return_value={'API_KEY': 'admin_key'})
        result = self.org.get_ehr_facilities(organization_id=123)
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, {'facilities': []})

    def test_set_ehr_locations_filter_success(self):
        location_filter = {'locationFilter': [{'room': '102A', 'beds': ['A', 'B']}]}
        self.mock_adapter.put.return_value = {'resultCode': 0}
        self.mock_adapter._headers = {'ADMIN_KEY': 'admin_key'}
        self.mock_adapter._get_headers = MagicMock(return_value={'API_KEY': 'admin_key'})
        result = self.org.set_ehr_locations_filter(
            organization_id=123,
            application_id=1000,
            facility_id='PHHA',
            location_filter=location_filter
        )
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_params']['applicationId'], 1000)
        self.assertEqual(kwargs['ep_params']['facilityId'], 'PHHA')
        self.assertEqual(kwargs['ep_json'], location_filter)
        self.assertEqual(result, {'resultCode': 0})

    def test_delete_ehr_facility_success(self):
        self.mock_adapter.delete.return_value = {'resultCode': 0}
        self.mock_adapter._headers = {'ADMIN_KEY': 'admin_key'}
        self.mock_adapter._get_headers = MagicMock(return_value={'API_KEY': 'admin_key'})
        result = self.org.delete_ehr_facility(organization_id=123, application_id=1000, facility_id='PHHA')
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(kwargs['ep_params']['applicationId'], 1000)
        self.assertEqual(kwargs['ep_params']['facilityId'], 'PHHA')
        self.assertEqual(result, {'resultCode': 0})

    def test_test_organization_notifications_success(self):
        notification_data = {'brand': 'default', 'template': 'account/user_registration.vm', 'language': 'en'}
        self.mock_adapter.post.return_value = b'zip archive data'
        self.mock_adapter._headers = {'ADMIN_KEY': 'admin_key'}
        self.mock_adapter._get_headers = MagicMock(return_value={'API_KEY': 'admin_key'})
        result = self.org.test_organization_notifications(organization_id=123, notification_data=notification_data)
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_json'], notification_data)
        self.assertEqual(result, b'zip archive data')

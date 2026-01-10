import unittest
from unittest.mock import MagicMock
from caredaily.apis.app import SystemAndUserProperties

class TestSystemAndUserProperties(unittest.TestCase):
    def setUp(self):
        self.sup = SystemAndUserProperties()
        self.mock_adapter = MagicMock()
        self.sup.adapter = self.mock_adapter

    def test_get_property(self):
        name = 'test_property'
        self.mock_adapter.get.return_value = 'property-result'
        result = self.sup.get_property(name=name)
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, 'property-result')

    def test_get_user_properties(self):
        user_id = 1
        self.mock_adapter.get.return_value = 'user-properties-result'
        result = self.sup.get_user_properties(user_id=user_id)
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, 'user-properties-result')

    def test_set_user_property(self):
        name = 'test_property'
        value = 'test_value'
        self.mock_adapter.put.return_value = 'set-user-property-result'
        result = self.sup.set_user_property(name=name, value=value)
        self.mock_adapter.put.assert_called_once()
        self.assertEqual(result, 'set-user-property-result')

    def test_set_user_properties(self):
        properties = {'prop1': 'value1', 'prop2': 'value2'}
        self.mock_adapter.put.return_value = 'set-user-properties-result'
        result = self.sup.set_user_properties(properties=properties)
        self.mock_adapter.put.assert_called_once()
        self.assertEqual(result, 'set-user-properties-result')

    def test_get_user_property(self):
        """Test Case ID: TC-SystemAndUserProperties-001
        Title: Get User Property
        Priority: P1
        """
        self.mock_adapter.get.return_value = 'property-value'
        result = self.sup.get_user_property(name='test_property')
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/userProperty/test_property')
        self.assertIsNone(kwargs.get('ep_params'))
        self.assertEqual(result, 'property-value')

    def test_get_user_property_with_user_id(self):
        """Test Case ID: TC-SystemAndUserProperties-002
        Title: Get User Property with User ID
        Priority: P2
        """
        self.mock_adapter.get.return_value = 'property-value'
        result = self.sup.get_user_property(name='test_property', user_id=123)
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['userId'], 123)
        self.assertEqual(result, 'property-value')

    def test_post_user_properties(self):
        """Test Case ID: TC-SystemAndUserProperties-003
        Title: Create User Properties via POST
        Priority: P1
        """
        properties = {'prop1': 'value1', 'prop2': 'value2'}
        self.mock_adapter.post.return_value = {'resultCode': 0}
        result = self.sup.post_user_properties(properties=properties)
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/userProperties')
        self.assertIn('property', kwargs['ep_json'])
        self.assertEqual(result, {'resultCode': 0})

    def test_post_user_properties_with_user_id(self):
        """Test Case ID: TC-SystemAndUserProperties-004
        Title: Create User Properties with User ID
        Priority: P2
        """
        properties = {'prop1': 'value1'}
        self.mock_adapter.post.return_value = {'resultCode': 0}
        result = self.sup.post_user_properties(properties=properties, user_id=123)
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['userId'], 123)
        self.assertEqual(result, {'resultCode': 0})

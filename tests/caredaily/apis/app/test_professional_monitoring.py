import unittest
from unittest.mock import MagicMock
from caredaily.apis.app import ProfessionalMonitoring

class TestProfessionalMonitoring(unittest.TestCase):
    def setUp(self):
        self.pm = ProfessionalMonitoring()
        self.mock_adapter = MagicMock()
        self.pm.adapter = self.mock_adapter

    def test_get_call_center_settings(self):
        location_id = 1
        self.mock_adapter.get.return_value = 'call-center-settings-result'
        result = self.pm.get_call_center_settings(location_id=location_id)
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, 'call-center-settings-result')

    def test_provide_call_center_settings(self):
        location_id = 1
        settings_data = {'settings': {'enabled': True}}
        self.mock_adapter.put.return_value = 'provide-call-center-settings-result'
        result = self.pm.provide_call_center_settings(location_id=location_id, settings_data=settings_data)
        self.mock_adapter.put.assert_called_once()
        self.assertEqual(result, 'provide-call-center-settings-result')

    def test_delete_call_center(self):
        location_id = 1
        self.mock_adapter.delete.return_value = 'delete-call-center-result'
        result = self.pm.delete_call_center(location_id=location_id)
        self.mock_adapter.delete.assert_called_once()
        self.assertEqual(result, 'delete-call-center-result')

    def test_create_call_center_test(self):
        location_id = 1
        self.mock_adapter.post.return_value = 'create-call-center-test-result'
        result = self.pm.create_call_center_test(location_id=location_id)
        self.mock_adapter.post.assert_called_once()
        self.assertEqual(result, 'create-call-center-test-result')

    def test_cancel_call_center_test(self):
        location_id = 1
        self.mock_adapter.delete.return_value = 'cancel-call-center-test-result'
        result = self.pm.cancel_call_center_test(location_id=location_id)
        self.mock_adapter.delete.assert_called_once()
        self.assertEqual(result, 'cancel-call-center-test-result')

    def test_get_call_center_alerts(self):
        location_id = 1
        start_date_ms = 1000
        end_date_ms = 2000
        self.mock_adapter.get.return_value = 'call-center-alerts-result'
        result = self.pm.get_call_center_alerts(location_id=location_id, start_date_ms=start_date_ms, end_date_ms=end_date_ms)
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, 'call-center-alerts-result')

    def test_delete_call_center(self):
        """Test Case ID: TC-ProfessionalMonitoring-001
        Title: Delete Call Center
        Priority: P1
        """
        self.mock_adapter.delete.return_value = {'resultCode': 0}
        result = self.pm.delete_call_center(location_id=123)
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(args[0], '/cloud/json/callCenter')
        self.assertEqual(kwargs['ep_params']['locationId'], 123)
        self.assertEqual(result, {'resultCode': 0})

    def test_delete_call_center_no_location(self):
        """Test Case ID: TC-ProfessionalMonitoring-002
        Title: Delete Call Center without Location ID
        Priority: P2
        """
        self.mock_adapter.delete.return_value = {'resultCode': 0}
        result = self.pm.delete_call_center()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertIsNone(kwargs.get('ep_params'))
        self.assertEqual(result, {'resultCode': 0})

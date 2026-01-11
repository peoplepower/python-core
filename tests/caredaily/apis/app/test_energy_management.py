import unittest
from unittest.mock import MagicMock
from caredaily.apis.app import EnergyManagement

class TestEnergyManagement(unittest.TestCase):
    def setUp(self):
        self.em = EnergyManagement()
        self.mock_adapter = MagicMock()
        self.em.adapter = self.mock_adapter

    def test_get_location_energy_usage(self):
        location_id = 1
        start_date_ms = 1000
        end_date_ms = 2000
        self.mock_adapter.get.return_value = 'location-energy-usage-result'
        result = self.em.get_location_energy_usage(location_id=location_id, start_date_ms=start_date_ms, end_date_ms=end_date_ms)
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, 'location-energy-usage-result')

    def test_get_current_device_energy_usage(self):
        device_id = 'dev1'
        location_id = 1
        self.mock_adapter.get.return_value = 'current-device-energy-usage-result'
        result = self.em.get_current_device_energy_usage(device_id=device_id, location_id=location_id)
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, 'current-device-energy-usage-result')

    def test_get_aggregated_device_energy_usage(self):
        location_id = 1
        start_date_ms = 1000
        end_date_ms = 2000
        self.mock_adapter.get.return_value = 'aggregated-device-energy-usage-result'
        result = self.em.get_aggregated_device_energy_usage(location_id=location_id, start_date_ms=start_date_ms, end_date_ms=end_date_ms)
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, 'aggregated-device-energy-usage-result')

    def test_get_billing_setting(self):
        location_id = 1
        self.mock_adapter.get.return_value = 'billing-setting-result'
        result = self.em.get_billing_setting(location_id=location_id)
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, 'billing-setting-result')

    def test_put_billing_setting(self):
        location_id = 1
        billing_data = {'billing': {'rate': 0.12}}
        self.mock_adapter.put.return_value = 'put-billing-setting-result'
        result = self.em.put_billing_setting(location_id=location_id, billing_data=billing_data)
        self.mock_adapter.put.assert_called_once()
        self.assertEqual(result, 'put-billing-setting-result')

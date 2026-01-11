import unittest
from unittest.mock import MagicMock
from caredaily.apis.app import DeviceMeasurements

class TestDeviceMeasurements(unittest.TestCase):
    def setUp(self):
        self.dm = DeviceMeasurements()
        self.mock_adapter = MagicMock()
        self.dm.adapter = self.mock_adapter

    def test_get_specific_device_parameters(self):
        self.mock_adapter.get.return_value = 'params-result'
        result = self.dm.get_specific_device_parameters(device_id='dev1', location_id=1)
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, 'params-result')

    def test_send_device_command(self):
        self.mock_adapter.put.return_value = 'command-result'
        result = self.dm.send_device_command(device_id='dev1', location_id=1, command={'cmd': 1})
        self.mock_adapter.put.assert_called_once()
        self.assertEqual(result, 'command-result')

    def test_device_readings_history(self):
        self.mock_adapter.get.return_value = 'readings-history-result'
        result = self.dm.device_readings_history(device_id='dev1', start_date_ms=1000, location_id=1)
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, 'readings-history-result')

    def test_last_device_readings(self):
        self.mock_adapter.get.return_value = 'last-readings-result'
        result = self.dm.last_device_readings(device_id='dev1', row_count=5, location_id=1, start_date_ms=1000)
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, 'last-readings-result')

    def test_get_multiple_device_parameters(self):
        self.mock_adapter.get.return_value = {'parameters': []}
        result = self.dm.get_multiple_device_parameters(location_id=123)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/parameters')
        self.assertEqual(kwargs['ep_params']['locationId'], 123)
        self.assertEqual(result, {'parameters': []})

    def test_get_multiple_device_parameters_with_filters(self):
        self.mock_adapter.get.return_value = {'parameters': []}
        result = self.dm.get_multiple_device_parameters(
            location_id=123,
            param_name=['temperature', 'humidity'],
            device_id=['dev1', 'dev2']
        )
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['paramName'], ['temperature', 'humidity'])
        self.assertEqual(kwargs['ep_params']['deviceId'], ['dev1', 'dev2'])

    def test_send_device_command_with_skip_prospects(self):
        self.mock_adapter.put.return_value = {'sent': True}
        result = self.dm.send_device_command(
            device_id='dev1',
            location_id=1,
            command={'cmd': 1},
            skip_prospects=True
        )
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_params']['skipProspects'], True)

    def test_device_readings_history_with_all_params(self):
        self.mock_adapter.get.return_value = {'readings': []}
        result = self.dm.device_readings_history(
            device_id='dev1',
            start_date_ms=1000,
            location_id=1,
            end_date_ms=2000,
            parameter_names=['temp', 'humidity'],
            parameter_index='0',
            range_only=True,
            reduce_noise=True,
            interval=3600,
            aggregation=1,
            sort_order='asc'
        )
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['endDate'], 2000)
        self.assertEqual(kwargs['ep_params']['parameterNames'], ['temp', 'humidity'])
        self.assertEqual(kwargs['ep_params']['rangeOnly'], True)
        self.assertEqual(kwargs['ep_params']['reduceNoise'], True)
        self.assertEqual(kwargs['ep_params']['interval'], 3600)
        self.assertEqual(kwargs['ep_params']['aggregation'], 1)
        self.assertEqual(kwargs['ep_params']['sortOrder'], 'asc')

    def test_last_device_readings_with_all_params(self):
        self.mock_adapter.get.return_value = {'readings': []}
        result = self.dm.last_device_readings(
            device_id='dev1',
            row_count=5,
            location_id=1,
            start_date_ms=1000,
            end_date_ms=2000,
            param_name='temperature',
            index='0',
            reduce_noise=True
        )
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['endDate'], 2000)
        self.assertEqual(kwargs['ep_params']['paramName'], 'temperature')
        self.assertEqual(kwargs['ep_params']['index'], '0')
        self.assertEqual(kwargs['ep_params']['reduceNoise'], True)

    def test_get_device_alerts(self):
        self.mock_adapter.get.return_value = {'alerts': []}
        result = self.dm.get_device_alerts(location_id=123)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/deviceAlerts')
        self.assertEqual(kwargs['ep_params']['locationId'], 123)
        self.assertEqual(result, {'alerts': []})

    def test_get_device_alerts_with_filters(self):
        self.mock_adapter.get.return_value = {'alerts': []}
        result = self.dm.get_device_alerts(
            location_id=123,
            device_id='dev1',
            alert_type=1,
            start_date_ms=1000,
            end_date_ms=2000
        )
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['deviceId'], 'dev1')
        self.assertEqual(kwargs['ep_params']['alertType'], 1)
        self.assertEqual(kwargs['ep_params']['startDate'], 1000)
        self.assertEqual(kwargs['ep_params']['endDate'], 2000)

    def test_submit_data_request(self):
        self.mock_adapter.post.return_value = {'requestId': 1}
        result = self.dm.submit_data_request(
            location_id=123,
            device_id='dev1',
            start_date_ms=1000,
            end_date_ms=2000
        )
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/dataRequests')
        self.assertEqual(kwargs['ep_params']['locationId'], 123)
        self.assertEqual(kwargs['ep_params']['deviceId'], 'dev1')
        self.assertEqual(kwargs['ep_params']['startDate'], 1000)
        self.assertEqual(kwargs['ep_params']['endDate'], 2000)
        self.assertEqual(result, {'requestId': 1})

    def test_submit_data_request_with_params(self):
        self.mock_adapter.post.return_value = {'requestId': 1}
        result = self.dm.submit_data_request(
            location_id=123,
            device_id='dev1',
            start_date_ms=1000,
            end_date_ms=2000,
            param_names=['temp', 'humidity'],
            index='0'
        )
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['paramNames'], ['temp', 'humidity'])
        self.assertEqual(kwargs['ep_params']['index'], '0')

    def test_get_data_requests(self):
        self.mock_adapter.get.return_value = {'requests': []}
        result = self.dm.get_data_requests(location_id=123)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/dataRequests')
        self.assertEqual(kwargs['ep_params']['locationId'], 123)
        self.assertEqual(result, {'requests': []})

    def test_get_data_requests_with_filters(self):
        self.mock_adapter.get.return_value = {'requests': []}
        result = self.dm.get_data_requests(
            location_id=123,
            request_id=1,
            device_id='dev1'
        )
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['requestId'], 1)
        self.assertEqual(kwargs['ep_params']['deviceId'], 'dev1')

    def test_get_units_of_measurement(self):
        self.mock_adapter.get.return_value = {'units': []}
        result = self.dm.get_units_of_measurement()
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/units')
        self.assertEqual(result, {'units': []})

    def test_get_units_of_measurement_with_filters(self):
        self.mock_adapter.get.return_value = {'units': []}
        result = self.dm.get_units_of_measurement(
            param_name='temperature',
            system=0
        )
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['paramName'], 'temperature')
        self.assertEqual(kwargs['ep_params']['system'], 0)

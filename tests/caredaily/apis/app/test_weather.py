import unittest
from unittest.mock import MagicMock
from caredaily.apis.app import Weather

class TestWeather(unittest.TestCase):
    def setUp(self):
        self.weather = Weather()
        self.mock_adapter = MagicMock()
        self.weather.adapter = self.mock_adapter

    def test_get_weather_no_params(self):
        """Test get_weather with only required location_id"""
        location_id = 1
        self.mock_adapter.get.return_value = 'weather-result'
        result = self.weather.get_weather(location_id=location_id)
        self.mock_adapter.get.assert_called_once_with(
            f'/espapi/cloud/json/weather/forecast/location/{location_id}',
            ep_params={}
        )
        self.assertEqual(result, 'weather-result')

    def test_get_weather_with_units(self):
        """Test get_weather with units parameter"""
        location_id = 1
        units = 'm'
        self.mock_adapter.get.return_value = 'weather-result'
        result = self.weather.get_weather(location_id=location_id, units=units)
        self.mock_adapter.get.assert_called_once_with(
            f'/espapi/cloud/json/weather/forecast/location/{location_id}',
            ep_params={'units': units}
        )
        self.assertEqual(result, 'weather-result')

    def test_get_weather_with_hours(self):
        """Test get_weather with hours parameter"""
        location_id = 1
        hours = 48
        self.mock_adapter.get.return_value = 'weather-result'
        result = self.weather.get_weather(location_id=location_id, hours=hours)
        self.mock_adapter.get.assert_called_once_with(
            f'/espapi/cloud/json/weather/forecast/location/{location_id}',
            ep_params={'hours': hours}
        )
        self.assertEqual(result, 'weather-result')

    def test_get_weather_with_all_params(self):
        """Test get_weather with all optional parameters"""
        location_id = 1
        units = 'e'
        hours = 24
        self.mock_adapter.get.return_value = 'weather-result'
        result = self.weather.get_weather(location_id=location_id, units=units, hours=hours)
        self.mock_adapter.get.assert_called_once_with(
            f'/espapi/cloud/json/weather/forecast/location/{location_id}',
            ep_params={'units': units, 'hours': hours}
        )
        self.assertEqual(result, 'weather-result')

    def test_get_weather_current_by_location_no_units(self):
        """Test get_weather_current_by_location without units"""
        location_id = 123
        self.mock_adapter.get.return_value = 'current-weather-result'
        result = self.weather.get_weather_current_by_location(location_id=location_id)
        self.mock_adapter.get.assert_called_once_with(
            f'/espapi/cloud/json/weather/current/location/{location_id}',
            ep_params=None
        )
        self.assertEqual(result, 'current-weather-result')

    def test_get_weather_current_by_location_with_units(self):
        """Test get_weather_current_by_location with units"""
        location_id = 123
        units = 'm'
        self.mock_adapter.get.return_value = 'current-weather-result'
        result = self.weather.get_weather_current_by_location(location_id=location_id, units=units)
        self.mock_adapter.get.assert_called_once_with(
            f'/espapi/cloud/json/weather/current/location/{location_id}',
            ep_params={'units': units}
        )
        self.assertEqual(result, 'current-weather-result')

    def test_get_weather_current_by_geocode_no_units(self):
        """Test get_weather_current_by_geocode without units"""
        latitude = '37.7749'
        longitude = '-122.4194'
        self.mock_adapter.get.return_value = 'geocode-weather-result'
        result = self.weather.get_weather_current_by_geocode(latitude=latitude, longitude=longitude)
        self.mock_adapter.get.assert_called_once_with(
            f'/espapi/cloud/json/weather/current/geocode/{latitude}/{longitude}',
            ep_params=None
        )
        self.assertEqual(result, 'geocode-weather-result')

    def test_get_weather_current_by_geocode_with_units(self):
        """Test get_weather_current_by_geocode with units"""
        latitude = '37.7749'
        longitude = '-122.4194'
        units = 'h'
        self.mock_adapter.get.return_value = 'geocode-weather-result'
        result = self.weather.get_weather_current_by_geocode(
            latitude=latitude, 
            longitude=longitude, 
            units=units
        )
        self.mock_adapter.get.assert_called_once_with(
            f'/espapi/cloud/json/weather/current/geocode/{latitude}/{longitude}',
            ep_params={'units': units}
        )
        self.assertEqual(result, 'geocode-weather-result')

    def test_get_weather_forecast_by_geocode_no_params(self):
        """Test get_weather_forecast_by_geocode with only required parameters"""
        latitude = '40.7128'
        longitude = '-74.0060'
        self.mock_adapter.get.return_value = 'forecast-result'
        result = self.weather.get_weather_forecast_by_geocode(
            latitude=latitude, 
            longitude=longitude
        )
        self.mock_adapter.get.assert_called_once_with(
            f'/espapi/cloud/json/weather/forecast/geocode/{latitude}/{longitude}',
            ep_params=None
        )
        self.assertEqual(result, 'forecast-result')

    def test_get_weather_forecast_by_geocode_with_units(self):
        """Test get_weather_forecast_by_geocode with units"""
        latitude = '40.7128'
        longitude = '-74.0060'
        units = 's'
        self.mock_adapter.get.return_value = 'forecast-result'
        result = self.weather.get_weather_forecast_by_geocode(
            latitude=latitude, 
            longitude=longitude,
            units=units
        )
        self.mock_adapter.get.assert_called_once_with(
            f'/espapi/cloud/json/weather/forecast/geocode/{latitude}/{longitude}',
            ep_params={'units': units}
        )
        self.assertEqual(result, 'forecast-result')

    def test_get_weather_forecast_by_geocode_with_hours(self):
        """Test get_weather_forecast_by_geocode with hours"""
        latitude = '40.7128'
        longitude = '-74.0060'
        hours = 12
        self.mock_adapter.get.return_value = 'forecast-result'
        result = self.weather.get_weather_forecast_by_geocode(
            latitude=latitude, 
            longitude=longitude,
            hours=hours
        )
        self.mock_adapter.get.assert_called_once_with(
            f'/espapi/cloud/json/weather/forecast/geocode/{latitude}/{longitude}',
            ep_params={'hours': hours}
        )
        self.assertEqual(result, 'forecast-result')

    def test_get_weather_forecast_by_geocode_with_organization_id(self):
        """Test get_weather_forecast_by_geocode with organization_id"""
        latitude = '40.7128'
        longitude = '-74.0060'
        organization_id = 456
        self.mock_adapter.get.return_value = 'forecast-result'
        result = self.weather.get_weather_forecast_by_geocode(
            latitude=latitude, 
            longitude=longitude,
            organization_id=organization_id
        )
        self.mock_adapter.get.assert_called_once_with(
            f'/espapi/cloud/json/weather/forecast/geocode/{latitude}/{longitude}',
            ep_params={'organizationId': organization_id}
        )
        self.assertEqual(result, 'forecast-result')

    def test_get_weather_forecast_by_geocode_with_all_params(self):
        """Test get_weather_forecast_by_geocode with all optional parameters"""
        latitude = '40.7128'
        longitude = '-74.0060'
        units = 'm'
        hours = 48
        organization_id = 789
        self.mock_adapter.get.return_value = 'forecast-result'
        result = self.weather.get_weather_forecast_by_geocode(
            latitude=latitude, 
            longitude=longitude,
            units=units,
            hours=hours,
            organization_id=organization_id
        )
        self.mock_adapter.get.assert_called_once_with(
            f'/espapi/cloud/json/weather/forecast/geocode/{latitude}/{longitude}',
            ep_params={
                'units': units,
                'hours': hours,
                'organizationId': organization_id
            }
        )
        self.assertEqual(result, 'forecast-result')

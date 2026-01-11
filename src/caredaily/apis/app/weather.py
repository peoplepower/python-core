# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "requests",
# ]
# ///

import json
from typing import Dict, List, Optional

from ...models import (
    APIKeyType,
    Cloud,
    MQTT,
    Result,
    Server,
    ServerType,
    SignatureAlgorithm,
)
from ..api import API


class Weather(API):
    def get_weather(
        self,
        location_id: int,
        units: str = None,
        hours: int = None,
    ) -> Result:
        """
        Get Weather Forecast for a Location.

        Retrieve weather forecast for a location.

        Args:
            location_id: Location ID (required)
            units: Units for measurements (e = English, m = Metric, h = Hybrid, s = Metric SI)
            hours: Forecast depth in hours (6, 12, 24, 48). Default is 24.

        Returns:
            Result: API response with weather forecast

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Weather/operation/Get%20Forecast%20by%20Location
        """
        params = {
            "units": units,
            "hours": hours,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            f"/espapi/cloud/json/weather/forecast/location/{location_id}",
            ep_params=params,
        )
        return result

    def get_weather_current_by_location(
        self,
        location_id: int,
        units: Optional[str] = None,
    ) -> Result:
        """
        Get Current Weather by Location.

        Retrieve current weather conditions by the location address.

        Args:
            location_id: ID of location (required)
            units: Units for measurements (e = English, m = Metric, h = Hybrid, s = Metric SI)

        Returns:
            Result: API response with current weather data

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Weather/operation/Get%20Current%20Weather%20by%20Location
        """
        params = {}
        if units is not None:
            params["units"] = units
        result: Result = self.adapter.get(
            f"/espapi/cloud/json/weather/current/location/{location_id}",
            ep_params=params if params else None,
        )
        return result

    def get_weather_current_by_geocode(
        self,
        latitude: str,
        longitude: str,
        units: Optional[str] = None,
    ) -> Result:
        """
        Get Current Weather by Geocode.

        Retrieve current weather conditions at certain point by latitude and longitude.

        Args:
            latitude: Latitude (required)
            longitude: Longitude (required)
            units: Units for measurements (e = English, m = Metric, h = Hybrid, s = Metric SI)

        Returns:
            Result: API response with current weather data

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Weather/operation/Get%20Current%20Weather%20by%20Geocode
        """
        params = {}
        if units is not None:
            params["units"] = units
        result: Result = self.adapter.get(
            f"/espapi/cloud/json/weather/current/geocode/{latitude}/{longitude}",
            ep_params=params if params else None,
        )
        return result

    def get_weather_forecast_by_geocode(
        self,
        latitude: str,
        longitude: str,
        units: Optional[str] = None,
        hours: Optional[int] = None,
        organization_id: Optional[int] = None,
    ) -> Result:
        """
        Get Forecast by Geocode.

        Retrieve weather forecast at certain point by latitude and longitude.

        Args:
            latitude: Latitude (required)
            longitude: Longitude (required)
            units: Units for measurements (e = English, m = Metric, h = Hybrid, s = Metric SI)
            hours: Forecast depth in hours (6, 12, 24, 48). Default is 24.
            organization_id: For specific organization. Used by administrator only.

        Returns:
            Result: API response with weather forecast

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Weather/operation/Get%20Forecast%20by%20Geocode
        """
        params = {}
        if units is not None:
            params["units"] = units
        if hours is not None:
            params["hours"] = hours
        if organization_id is not None:
            params["organizationId"] = organization_id
        result: Result = self.adapter.get(
            f"/espapi/cloud/json/weather/forecast/geocode/{latitude}/{longitude}",
            ep_params=params if params else None,
        )
        return result

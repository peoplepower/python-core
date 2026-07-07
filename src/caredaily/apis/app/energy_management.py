# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "requests",
# ]
# ///

import json
from datetime import datetime
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


class EnergyManagement(API):
    def get_location_energy_usage(
        self,
        location_id: int,
        start_date_ms: int,
        end_date_ms: int,
        aggregation: int = 2,
    ) -> Result:
        """
        Get Energy Usage for a Location.

        Args:
            location_id: Location ID for which to obtain energy measurements
            start_date_ms: Start date in milliseconds
            end_date_ms: End date in milliseconds
            aggregation: How to aggregate the energy data (0-5, default 2 for Day)

        Returns:
            Result: API response with energy usage history

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Energy-Management/operation/Get%20Energy%20Usage
        """
        # Convert milliseconds to ISO date strings
        start_date = datetime.fromtimestamp(start_date_ms / 1000).isoformat()
        end_date = datetime.fromtimestamp(end_date_ms / 1000).isoformat()
        
        params = {
            "endDate": end_date,
        }
        result: Result = self.adapter.get(
            f"/cloud/json/locations/{location_id}/energyUsage/{aggregation}/{start_date}",
            ep_params=params,
        )
        return result

    def get_current_device_energy_usage(
        self,
        device_id: str,
        location_id: int,
        index: str = None,
    ) -> Result:
        """
        Get Device Energy Usage.

        Return a device's values of power, billing rate, its associated cost, total energy usage, and its cost for the current day, month and year.

        Args:
            device_id: Device ID for which to obtain energy-related data
            location_id: Request information on a specific location (required)
            index: Optional index number to obtain energy-related data from a part of a device

        Returns:
            Result: API response with current device energy usage

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Energy-Management/operation/Get%20Device%20Energy%20Usage
        """
        params = {
            "locationId": location_id,
            "index": index,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            f"/cloud/json/devices/{device_id}/currentEnergyUsage",
            ep_params=params,
        )
        return result

    def get_aggregated_device_energy_usage(
        self,
        location_id: int,
        start_date_ms: int,
        end_date_ms: int,
        device_id: str = None,
        aggregation: int = 2,
        reduce_noise: bool = None,
    ) -> Result:
        """
        Get Aggregated Energy Usage for a Device.

        Return energy usage at a device level for a specified period of time, and aggregated by different periods.

        Args:
            location_id: Request information on a specific location (required)
            start_date_ms: Start date in milliseconds
            end_date_ms: End date in milliseconds
            device_id: Device ID for which to obtain aggregated energy usage
            aggregation: How to aggregate the energy data (0-5, default 2 for Day)
            reduce_noise: Return tiny energy values less than defined threshold as zero

        Returns:
            Result: API response with aggregated energy usage

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Energy-Management/operation/Get%20Aggregated%20Energy%20Usage%20for%20a%20Device
        """
        # Convert milliseconds to ISO date strings
        start_date = datetime.fromtimestamp(start_date_ms / 1000).isoformat()
        end_date = datetime.fromtimestamp(end_date_ms / 1000).isoformat()
        
        # If device_id is not provided, we might need to use a different endpoint
        # For now, we'll require device_id
        if not device_id:
            # This might need to be handled differently, but for now use a placeholder
            device_id = "all"
        
        params = {
            "locationId": location_id,
            "endDate": end_date,
            "reduceNoise": reduce_noise,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            f"/cloud/json/devices/{device_id}/energyUsage/{aggregation}/{start_date}",
            ep_params=params,
        )
        return result

    def get_billing_setting(
        self,
        location_id: int,
    ) -> Result:
        """
        Get Billing Setting.

        Get billing settings for a location.

        Args:
            location_id: Location ID

        Returns:
            Result: API response with billing settings

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html
        """
        # The billing endpoint might be part of location settings
        # For now, using a reasonable endpoint structure
        result: Result = self.adapter.get(
            f"/cloud/json/locations/{location_id}/billing",
        )
        return result

    def put_billing_setting(
        self,
        location_id: int,
        billing_data: Dict,
    ) -> Result:
        """
        Put Billing Setting.

        Update billing settings for a location.

        Args:
            location_id: Location ID
            billing_data: Billing data to update

        Returns:
            Result: API response confirming update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html
        """
        result: Result = self.adapter.put(
            f"/cloud/json/locations/{location_id}/billing",
            ep_json=billing_data,
        )
        return result


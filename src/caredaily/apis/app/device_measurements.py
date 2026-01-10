# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "requests",
# ]
# ///

import json
from typing import Dict, List

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

class DeviceMeasurements(API):
    """
    Device Measurements API for accessing device parameters, readings, and measurement data.

    This class provides methods to retrieve device parameters, send commands, get historical
    readings, and manage device measurement data.

    Reference:
        https://app.peoplepowerco.com/cloud/apidocs/cloud.html#device-measurements
    """

    def get_specific_device_parameters(
        self,
        device_id: str,
        location_id: int,
        param_name: List[str] = None,
    ):
        """
        Get specific device parameters for a single device.

        Args:
            device_id: Unique device ID
            location_id: Location ID where the device is registered
            param_name: List of parameter names to retrieve

        Returns:
            Result: API response containing device parameters

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Device-Measurements/operation/Get%20Current%20Measurements
        """
        params = {
            "locationId": location_id,
            "paramName": param_name,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.get(
            f"/espapi/cloud/json/devices/{device_id}/parameters",
            ep_params=params,
        )

    def send_device_command(
        self,
        device_id: str,
        location_id: int,
        command: Dict,
        skip_prospects: bool = None,
    ):
        """
        Send a command or parameter update to a device.

        Args:
            device_id: Unique device ID
            location_id: Location ID where the device is registered
            command: Command payload as a dictionary
            skip_prospects: Skip sending to prospect users if True

        Returns:
            Result: API response confirming command was sent

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Device-Measurements/operation/Send%20a%20Command
        """
        params = {"locationId": location_id, "skipProspects": skip_prospects}
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.put(
            f"/espapi/cloud/json/devices/{device_id}/parameters",
            ep_json=json.dumps(command),
            ep_params=params,
        )

    def get_multiple_device_parameters(
        self,
        location_id: int,
        param_name: List[str] = None,
        device_id: List[str] = None,
    ):
        """
        Get parameters for multiple devices at once.

        Args:
            location_id: Location ID where the devices are registered
            param_name: List of parameter names to retrieve
            device_id: List of device IDs to query

        Returns:
            Result: API response containing parameters for multiple devices

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Device-Measurements/operation/Get%20Current%20Measurements
        """
        params = {
            "locationId": location_id,
            "paramName": param_name,
            "deviceId": device_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.get(
            "/espapi/cloud/json/parameters",
            ep_params=params,
        )

    def send_device_commands(
        self,
        location_id: int,
        devices: List[Dict],
    ):
        """
        This API allows to send commands to multiple devices simultaneously.

        This operation is not atomic. It will try to execute all commands in the same order, as they are provided.
        If some command fails, it will execute the next one. The result code is returned for each command.

        Args:
            location_id: Location ID where the device is registered
            devices: List of device command objects, each containing:
                - deviceId: Device ID (required)
                - commandType: Command type (required)
                - commandTimeout: Command timeout in milliseconds (required)
                - params: List of parameter objects, each containing:
                    - name: Parameter name (required)
                    - value: Parameter value (required)
                    - index: Parameter index (optional)
                - comment: Optional comment explaining why this command has been sent

        Returns:
            Result: API response confirming command was sent

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Device-Measurements/operation/Send%20a%20Command
        """
        data = {
            "devices": devices,
        }
        result: Result = self.adapter.put(
            "/espapi/cloud/json/parameters",
            ep_json=data,
        )
        return result

    def device_readings_history(
        self,
        device_id: str,
        start_date_ms: int,
        location_id: int,
        end_date_ms: int = None,
        parameter_names: List[str] = None,
        parameter_index: str = None,
        range_only: bool = None,
        reduce_noise: bool = None,
        interval: int = None,
        aggregation: int = None,
        sort_order: str = None,
    ):
        """
        Get historical device readings within a date range.

        Args:
            device_id: Unique device ID
            start_date_ms: Start timestamp in milliseconds
            location_id: Location ID where the device is registered
            end_date_ms: End timestamp in milliseconds
            parameter_names: List of parameter names to retrieve
            parameter_index: Index of specific parameter
            range_only: Return only min/max range if True
            reduce_noise: Apply noise reduction if True
            interval: Time interval for aggregation in milliseconds
            aggregation: Aggregation type (0=avg, 1=min, 2=max, 3=count)
            sort_order: Sort order ('asc' or 'desc')

        Returns:
            Result: API response containing historical readings

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Device-Measurements/operation/Get%20History%20of%20Measurements
        """
        params = {
            "endDate": end_date_ms,
            "locationId": location_id,
            "parameterNames": parameter_names,
            "parameterIndex": parameter_index,
            "rangeOnly": range_only,
            "reduceNoise": reduce_noise,
            "interval": interval,
            "aggregation": aggregation,
            "sortOrder": sort_order,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.get(
            f"/espapi/cloud/json/devices/{device_id}/parametersByDate/{start_date_ms}",
            ep_params=params,
        )

    def last_device_readings(
        self,
        device_id: str,
        row_count: int,
        location_id: int,
        start_date_ms: int,
        end_date_ms: int = None,
        param_name: str = None,
        index: str = None,
        reduce_noise: bool = None,
    ):
        """
        Get the last N readings from a device.

        Args:
            device_id: Unique device ID
            row_count: Number of readings to retrieve
            location_id: Location ID where the device is registered
            start_date_ms: Start timestamp in milliseconds
            end_date_ms: End timestamp in milliseconds
            param_name: Parameter name to filter by
            index: Index of specific parameter
            reduce_noise: Apply noise reduction if True

        Returns:
            Result: API response containing the last N readings

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Device-Measurements/operation/Get%20the%20Last%20N%20Measurements
        """
        params = {
            "locationId": location_id,
            "startDate": start_date_ms,
            "endDate": end_date_ms,
            "paramName": param_name,
            "index": index,
            "reduceNoise": reduce_noise,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.get(
            f"/espapi/cloud/json/devices/{device_id}/parametersByCount/{row_count}",
            ep_params=params,
        )

    def get_device_alerts(
        self,
        location_id: int,
        device_id: str = None,
        alert_type: int = None,
        start_date_ms: int = None,
        end_date_ms: int = None,
    ):
        """
        Get device alerts for a location.

        Args:
            location_id: Location ID to query alerts for
            device_id: Filter by specific device ID
            alert_type: Filter by alert type
            start_date_ms: Start timestamp in milliseconds
            end_date_ms: End timestamp in milliseconds

        Returns:
            Result: API response containing device alerts

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Device-Measurements/operation/Get%20History%20of%20Alerts
        """
        params = {
            "locationId": location_id,
            "deviceId": device_id,
            "alertType": alert_type,
            "startDate": start_date_ms,
            "endDate": end_date_ms,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.get(
            "/espapi/cloud/json/deviceAlerts",
            ep_params=params,
        )

    def get_alerts(
        self,
        location_id: int,
        start_date: str,
        device_id: str = None,
        alert_type: str = None,
        end_date: str = None,
    ) -> Result:
        """
        Get History of Device Alerts.

        Retrieve history of device alerts for a location.

        Args:
            location_id: Location ID (required)
            start_date: Start date to begin receiving alerts, e.g., 2014-08-01T12:00:00-08:00 (required)
            device_id: Device ID for which to get a history of alerts
            alert_type: Retrieve only alerts of this type
            end_date: End date to stop receiving alerts, e.g., 2014-08-01T13:00:00-08:00. Default is the current date.

        Returns:
            Result: API response with device alerts history

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Device-Measurements/operation/Get%20History%20of%20Alerts
        """
        params = {
            "locationId": location_id,
            "startDate": start_date,
        }
        if device_id is not None:
            params["deviceId"] = device_id
        if alert_type is not None:
            params["alertType"] = alert_type
        if end_date is not None:
            params["endDate"] = end_date
        result: Result = self.adapter.get(
            "/espapi/cloud/json/alerts",
            ep_params=params,
        )
        return result

    def submit_data_request(
        self,
        location_id: int,
        device_id: str,
        start_date_ms: int,
        end_date_ms: int,
        param_names: List[str] = None,
        index: str = None,
    ):
        """
        Submit a request to retrieve device data asynchronously.

        Args:
            location_id: Location ID where the device is registered
            device_id: Unique device ID
            start_date_ms: Start timestamp in milliseconds
            end_date_ms: End timestamp in milliseconds
            param_names: List of parameter names to retrieve
            index: Index of specific parameter

        Returns:
            Result: API response with data request ID

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Device-Measurements/operation/Submit%20Data%20Request
        """
        params = {
            "locationId": location_id,
            "deviceId": device_id,
            "startDate": start_date_ms,
            "endDate": end_date_ms,
            "paramNames": param_names,
            "index": index,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.post(
            "/espapi/cloud/json/dataRequests",
            ep_params=params,
        )

    def get_data_requests(
        self,
        location_id: int,
        request_id: int = None,
        device_id: str = None,
    ):
        """
        Get status and results of data requests.

        Args:
            location_id: Location ID
            request_id: Specific request ID to retrieve
            device_id: Filter by device ID

        Returns:
            Result: API response containing data request status and results

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Device-Measurements/operation/Get%20Requested%20Data
        """
        params = {
            "locationId": location_id,
            "requestId": request_id,
            "deviceId": device_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.get(
            "/espapi/cloud/json/dataRequests",
            ep_params=params,
        )

    def get_units_of_measurement(
        self,
        param_name: str = None,
        system: int = None,
    ):
        """
        Get available units of measurement for device parameters.

        Args:
            param_name: Filter by specific parameter name
            system: Measurement system (0=metric, 1=imperial)

        Returns:
            Result: API response containing units of measurement

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Device-Measurements/operation/Get%20Units%20of%20Measurement
        """
        params = {
            "paramName": param_name,
            "system": system,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.get(
            "/espapi/cloud/json/units",
            ep_params=params,
        )


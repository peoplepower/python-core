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


class Devices(API):
    """
    Devices API for managing devices and device operations.

    This class provides comprehensive methods for device operations including
    registration, retrieval, updates, deletion, properties management, and device-specific operations.

    Reference:
        https://app.peoplepowerco.com/cloud/apidocs/cloud.html#devices
    """

    def register_device(
        self,
        device_id: str,
        location_id: int,
        device_type: int,
        description: str = None,
        model_id: str = None,
        start_date_ms: int = None,
        goal_id: int = None,
        new_device: bool = None,
        user_id: int = None,
    ):
        """
        Register a new device to a location.

        Args:
            device_id: Unique device identifier
            location_id: Location ID to register the device to
            device_type: Device type identifier
            description: Optional device description
            model_id: Optional device model identifier
            start_date_ms: Start date in milliseconds since epoch
            goal_id: Optional goal ID for the device
            new_device: Whether this is a new device
            user_id: Optional user ID (requires admin permissions)

        Returns:
            Result: API response with device registration result

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#register-a-device
        """
        params = {
            "locationId": location_id,
            "deviceType": device_type,
            "desc": description,
            "modelId": model_id,
            "startDate": start_date_ms,
            "goalId": goal_id,
            "newDevice": new_device,
            "userId": user_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.post(
            f"/cloud/json/devices/{device_id}",
            ep_params=params,
        )
        return result

    def get_devices(
        self,
        location_id: int,
        user_id: int = None,
        check_persistent: bool = None,
        space_id: int = None,
        get_tags: bool = None,
        prospect: bool = None,
    ):
        """
        Get list of devices for a location.

        Args:
            location_id: Location ID to get devices for
            user_id: Optional user ID (requires admin permissions)
            check_persistent: Check if devices are persistent
            space_id: Filter by space ID
            get_tags: Include device tags in response
            prospect: Include prospect devices

        Returns:
            Result: API response containing list of devices with their details

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Devices/operation/Get%20Devices
        """
        params = {
            "locationId": location_id,
            "userId": user_id,
            "checkPersistent": check_persistent,
            "spaceId": space_id,
            "getTags": get_tags,
            "prospect": prospect,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/cloud/json/devices",
            ep_params=params,
        )
        return result

    def delete_multiple_devices(
        self,
        location_id: int,
        device_ids: List[str],
        clear_measurements: bool = None,
    ):
        """
        Delete multiple devices from a location.

        Args:
            location_id: Location ID containing the devices
            device_ids: List of device IDs to delete
            clear_measurements: Whether to clear device measurements

        Returns:
            Result: API response confirming deletions

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Devices/operation/Delete%20Multiple%20Devices
        """
        params = {
            "locationId": location_id,
            "deviceId": device_ids,
            "clearMeasurements": clear_measurements,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.delete(
            "/cloud/json/devices",
            ep_params=params,
        )
        return result

    def get_device(
        self,
        device_id: str,
        location_id: int,
        check_connected: bool = None,
    ):
        """
        Get details of a specific device.

        Args:
            device_id: Device ID to retrieve
            location_id: Location ID containing the device
            check_connected: Check if device is currently connected

        Returns:
            Result: API response containing device details including
                   configuration, status, and metadata

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Devices/operation/Get%20Device
        """
        params = {
            "locationId": location_id,
            "checkConnected": check_connected,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            f"/cloud/json/devices/{device_id}",
            ep_params=params,
        )
        return result

    def get_device_services(
        self,
        device_id: str,
        location_id: int,
    ):
        """
        Get services available for a specific device.

        Args:
            device_id: Device ID to get services for
            location_id: Location ID containing the device

        Returns:
            Result: API response containing available device services

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Devices/operation/Get%20Device%20Services
        """
        params = {
            "locationId": location_id,
        }
        result: Result = self.adapter.get(
            f"/cloud/json/devices/{device_id}/services",
            ep_params=params,
        )
        return result

    def update_device(
        self,
        device_id: str,
        location_id: int,
        description: str = None,
        goal_id: int = None,
        spaces: List[Dict] = None,
    ):
        """
        Update device attributes.

        Args:
            device_id: Device ID to update
            location_id: Location ID containing the device
            description: New device description
            goal_id: New goal ID for the device
            spaces: List of space associations

        Returns:
            Result: API response confirming update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Devices/operation/Update%20Device
        """
        params = {
            "locationId": location_id,
            "desc": description,
            "goalId": goal_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        body = None
        if spaces is not None:
            body = {"spaces": spaces}
        result: Result = self.adapter.put(
            f"/cloud/json/devices/{device_id}",
            ep_params=params,
            ep_json=json.dumps(body) if body else None,
        )
        return result

    def delete_device(
        self,
        device_id: str,
        location_id: int,
        clear_measurements: bool = None,
    ):
        """
        Remove a device from a specific location.

        Args:
            device_id: Device ID to remove
            location_id: Location ID containing the device
            clear_measurements: Whether to clear device measurements

        Returns:
            Result: API response confirming removal

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Devices/operation/Delete%20Device
        """
        params = {
            "locationId": location_id,
            "clearMeasurements": clear_measurements,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.delete(
            f"/cloud/json/devices/{device_id}",
            ep_params=params,
        )
        return result

    def get_device_sim_card(
        self,
        device_id: str,
        location_id: int,
    ):
        """
        Get SIM card information for a device.

        Args:
            device_id: Device ID to get SIM card info for
            location_id: Location ID containing the device

        Returns:
            Result: API response containing SIM card information

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Devices/operation/Get%20Device%20SIM%20Card
        """
        params = {
            "locationId": location_id,
        }
        result: Result = self.adapter.get(
            f"/cloud/json/devices/{device_id}/simCard",
            ep_params=params,
        )
        return result

    def copy_device_simulator(
        self,
        device_id: str,
        location_id: int,
        new_device_id: str,
    ):
        """
        Copy device simulator configuration to a new device.

        Args:
            device_id: Source device ID to copy from
            location_id: Location ID containing the device
            new_device_id: New device ID to copy to

        Returns:
            Result: API response confirming copy operation

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Devices/operation/Copy%20Device%20Simulator
        """
        params = {
            "locationId": location_id,
            "newDeviceId": new_device_id,
        }
        result: Result = self.adapter.post(
            f"/cloud/json/devices/{device_id}/simulator",
            ep_params=params,
        )
        return result

    def get_device_activation_info(
        self,
        device_id: str,
        location_id: int = None,
    ):
        """
        Get device activation information.

        Args:
            device_id: Device ID to get activation info for
            location_id: Optional location ID

        Returns:
            Result: API response containing device activation information

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Devices/operation/Get%20Device%20Activation%20Information
        """
        params = {
            "locationId": location_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            f"/cloud/json/devices/{device_id}/activation",
            ep_params=params,
        )
        return result

    def get_device_properties(
        self,
        device_id: str,
        location_id: int,
        name: str = None,
        index: str = None,
    ):
        """
        Get device properties.

        Args:
            device_id: Device ID to get properties for
            location_id: Location ID containing the device
            name: Optional property name filter
            index: Optional property index filter

        Returns:
            Result: API response containing device properties

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Devices/operation/Get%20Device%20Properties
        """
        params = {
            "locationId": location_id,
            "name": name,
            "index": index,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            f"/cloud/json/devices/{device_id}/properties",
            ep_params=params,
        )
        return result

    def set_device_properties(
        self,
        device_id: str,
        location_id: int,
        properties: List[Dict],
    ):
        """
        Set device properties.

        Args:
            device_id: Device ID to set properties for
            location_id: Location ID containing the device
            properties: List of property dictionaries with name, value, and optional index

        Returns:
            Result: API response confirming property updates

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Devices/operation/Set%20Device%20Properties
        """
        params = {
            "locationId": location_id,
        }
        body = {"properties": properties}
        result: Result = self.adapter.put(
            f"/cloud/json/devices/{device_id}/properties",
            ep_params=params,
            ep_json=json.dumps(body),
        )
        return result

    def delete_device_property(
        self,
        device_id: str,
        location_id: int,
        name: str,
        index: str = None,
    ):
        """
        Delete a device property.

        Args:
            device_id: Device ID to delete property from
            location_id: Location ID containing the device
            name: Property name to delete
            index: Optional property index

        Returns:
            Result: API response confirming property deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Devices/operation/Delete%20Device%20Property
        """
        params = {
            "locationId": location_id,
            "name": name,
            "index": index,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.delete(
            f"/cloud/json/devices/{device_id}/properties",
            ep_params=params,
        )
        return result

    def link_device_to_space(
        self,
        device_id: str,
        location_id: int,
        space_id: int,
    ):
        """
        Link a device to a space.

        Args:
            device_id: Device ID to link
            location_id: Location ID containing the device
            space_id: Space ID to link to

        Returns:
            Result: API response confirming link

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Devices/operation/Link%20Device%20to%20Space
        """
        params = {
            "locationId": location_id,
            "spaceId": space_id,
        }
        result: Result = self.adapter.post(
            f"/cloud/json/devices/{device_id}/spaces",
            ep_params=params,
        )
        return result

    def unlink_device_from_space(
        self,
        device_id: str,
        location_id: int,
        space_id: int,
    ):
        """
        Unlink a device from a space.

        Args:
            device_id: Device ID to unlink
            location_id: Location ID containing the device
            space_id: Space ID to unlink from

        Returns:
            Result: API response confirming unlink

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Devices/operation/Unlink%20Device%20from%20Space
        """
        params = {
            "locationId": location_id,
            "spaceId": space_id,
        }
        result: Result = self.adapter.delete(
            f"/cloud/json/devices/{device_id}/spaces",
            ep_params=params,
        )
        return result

    def get_firmware_update_jobs(
        self,
        device_id: str,
        location_id: int,
    ):
        """
        Get firmware update jobs for a device.

        Args:
            device_id: Device ID to get firmware jobs for
            location_id: Location ID containing the device

        Returns:
            Result: API response containing firmware update jobs

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Devices/operation/Get%20Firmware%20Update%20Jobs
        """
        params = {
            "locationId": location_id,
        }
        result: Result = self.adapter.get(
            f"/cloud/json/devices/{device_id}/firmware",
            ep_params=params,
        )
        return result

    def set_firmware_update_status(
        self,
        device_id: str,
        location_id: int,
        status: int,
        job_id: int = None,
    ):
        """
        Set firmware update status for a device.

        Args:
            device_id: Device ID to set firmware status for
            location_id: Location ID containing the device
            status: Firmware update status code
            job_id: Optional firmware job ID

        Returns:
            Result: API response confirming status update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Devices/operation/Set%20Firmware%20Update%20Status
        """
        params = {
            "locationId": location_id,
            "status": status,
            "jobId": job_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.put(
            f"/cloud/json/devices/{device_id}/firmware",
            ep_params=params,
        )
        return result

    def get_firmware_jobs(
        self,
        device_id: str = None,
        index: str = None,
        firmware: str = None,
        user_id: int = None,
    ) -> Result:
        """
        Get Firmware Jobs.

        A user can approve or decline an update of his devices with new firmware.

        Firmware update job statuses:
        - 1: Available
        - 2: Approved
        - 3: Decline
        - 4: Started

        This API allows to retrieve a list of available firmware updates for user devices.

        Args:
            device_id: Optional filter by device ID
            index: Check update for specific device part
            firmware: Current device firmware version
            user_id: Device owner ID for access by an administrator

        Returns:
            Result: API response with firmware update jobs

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Devices/operation/Get%20Firmware%20Jobs
        """
        params = {}
        if device_id is not None:
            params["deviceId"] = device_id
        if index is not None:
            params["index"] = index
        if firmware is not None:
            params["firmware"] = firmware
        if user_id is not None:
            params["userId"] = user_id
        result: Result = self.adapter.get(
            "/cloud/json/fwupdate",
            ep_params=params if params else None,
        )
        return result

    def set_firmware_update_status_v2(
        self,
        device_id: str,
        status: int,
        index: str = None,
        start_date: str = None,
        user_id: int = None,
    ) -> Result:
        """
        Set Firmware Update Status.

        Approve or decline a not forced firmware update job.
        The user can schedule the update after specific date and time.

        Args:
            device_id: Device ID (required)
            status: New job status: 2 - approved, 3 - declined (required)
            index: Update firmware of specific device part
            start_date: Firmware update start date
            user_id: Device owner ID for access by an administrator

        Returns:
            Result: API response confirming status update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Devices/operation/Set%20Firmware%20Update%20Status
        """
        params = {
            "deviceId": device_id,
            "status": status,
        }
        if index is not None:
            params["index"] = index
        if start_date is not None:
            params["startDate"] = start_date
        if user_id is not None:
            params["userId"] = user_id
        result: Result = self.adapter.put(
            "/cloud/json/fwupdate",
            ep_params=params,
        )
        return result

    def get_device_logs(
        self,
        device_id: str,
        location_id: int,
        start_date_ms: int = None,
        end_date_ms: int = None,
    ):
        """
        Get device logs.

        Args:
            device_id: Device ID to get logs for
            location_id: Location ID containing the device
            start_date_ms: Start date in milliseconds since epoch
            end_date_ms: End date in milliseconds since epoch

        Returns:
            Result: API response containing device logs

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Devices/operation/Get%20Device%20Logs
        """
        params = {
            "locationId": location_id,
            "startDate": start_date_ms,
            "endDate": end_date_ms,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            f"/cloud/json/devices/{device_id}/logs",
            ep_params=params,
        )
        return result

    def get_device_logs_list(
        self,
        location_id: int,
        device_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Result:
        """
        Get Device Logs.

        Returns a list of device log files stored in the system.

        Args:
            location_id: Request device on a specific location (required)
            device_id: Device ID filter
            start_date: Limit response by date, 30 days in the past maximum
            end_date: Limit response by date

        Returns:
            Result: API response containing list of device log files

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Devices/operation/Get%20Device%20Logs
        """
        params = {
            "locationId": location_id,
        }
        if device_id is not None:
            params["deviceId"] = device_id
        if start_date is not None:
            params["startDate"] = start_date
        if end_date is not None:
            params["endDate"] = end_date
        result: Result = self.adapter.get(
            "/cloud/json/deviceLogs",
            ep_params=params,
        )
        return result

    def get_device_log_content_url(
        self,
        location_id: int,
        device_id: str,
        log_date: str,
    ) -> Result:
        """
        Get Device Log Content.

        This API returns a temporary URL to download log's content.

        Args:
            location_id: Request device on a specific location (required)
            device_id: Device ID (required)
            log_date: Log date (required)

        Returns:
            Result: API response with temporary URL to download log content

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Devices/operation/Get%20Device%20Log%20Content
        """
        params = {
            "locationId": location_id,
            "deviceId": device_id,
            "logDate": log_date,
        }
        result: Result = self.adapter.get(
            "/cloud/json/deviceLogContent",
            ep_params=params,
        )
        return result

    def get_preregistered_device(
        self,
        device_id: str,
    ) -> Result:
        """
        Get pre-registered device by ID.

        This API returns device type and model, if this information is pre-registered in the cloud database.

        Args:
            device_id: Device ID (required)

        Returns:
            Result: API response with device details

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Devices/operation/Get%20pre-registered%20device
        """
        result: Result = self.adapter.get(
            f"/cloud/json/preregistered/{device_id}",
        )
        return result

    def get_device_log_content(
        self,
        device_id: str,
        location_id: int,
        log_id: int,
    ):
        """
        Get specific device log content.

        Args:
            device_id: Device ID to get log content for
            location_id: Location ID containing the device
            log_id: Log ID to retrieve

        Returns:
            Result: API response containing log content

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Devices/operation/Get%20Device%20Log%20Content
        """
        params = {
            "locationId": location_id,
            "logId": log_id,
        }
        result: Result = self.adapter.get(
            f"/cloud/json/devices/{device_id}/logContent",
            ep_params=params,
        )
        return result

    def upload_sensitivity_map(
        self,
        device_id: str,
        location_id: int,
        sensitivity_map: str,
    ):
        """
        Upload sensitivity map for a device.

        Args:
            device_id: Device ID to upload sensitivity map for
            location_id: Location ID containing the device
            sensitivity_map: Sensitivity map data

        Returns:
            Result: API response confirming upload

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Devices/operation/Upload%20Sensitivity%20Map
        """
        params = {
            "locationId": location_id,
        }
        body = {"sensitivityMap": sensitivity_map}
        result: Result = self.adapter.post(
            f"/cloud/json/devices/{device_id}/sensitivityMap",
            ep_params=params,
            ep_json=json.dumps(body),
        )
        return result

    def delete_sensitivity_map(
        self,
        device_id: str,
        location_id: int,
    ):
        """
        Delete sensitivity map for a device.

        Args:
            device_id: Device ID to delete sensitivity map for
            location_id: Location ID containing the device

        Returns:
            Result: API response confirming deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Devices/operation/Delete%20Sensitivity%20Map
        """
        params = {
            "locationId": location_id,
        }
        result: Result = self.adapter.delete(
            f"/cloud/json/devices/{device_id}/sensitivityMap",
            ep_params=params,
        )
        return result

    def register_device_voip_account(
        self,
        device_id: str,
        location_id: int,
        voip_account: str,
        voip_password: str,
        voip_server: str = None,
        voip_port: int = None,
    ):
        """
        Register a VoIP account for a device.

        Args:
            device_id: Device ID to register VoIP account for
            location_id: Location ID containing the device
            voip_account: VoIP account username
            voip_password: VoIP account password
            voip_server: Optional VoIP server address
            voip_port: Optional VoIP server port

        Returns:
            Result: API response confirming VoIP registration

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Devices/operation/Register%20VoIP%20account
        """
        params = {
            "locationId": location_id,
        }
        body = {
            "account": voip_account,
            "password": voip_password,
        }
        if voip_server is not None:
            body["server"] = voip_server
        if voip_port is not None:
            body["port"] = voip_port
        result: Result = self.adapter.post(
            f"/cloud/json/devices/{device_id}/voip",
            ep_params=params,
            ep_json=json.dumps(body),
        )
        return result

    def remove_device_voip_registration(
        self,
        device_id: str,
        location_id: int,
    ):
        """
        Remove VoIP registration for a device.

        Args:
            device_id: Device ID to remove VoIP registration for
            location_id: Location ID containing the device

        Returns:
            Result: API response confirming VoIP removal

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Devices/operation/Remove%20VoIP%20registration
        """
        params = {
            "locationId": location_id,
        }
        result: Result = self.adapter.delete(
            f"/cloud/json/devices/{device_id}/voip",
            ep_params=params,
        )
        return result

    def make_device_voip_call(
        self,
        device_id: str,
        location_id: int,
        callee: str,
        call_type: str = None,
    ):
        """
        Make a VoIP call from a device.

        Args:
            device_id: Device ID to make call from
            location_id: Location ID containing the device
            callee: Callee phone number or SIP address
            call_type: Optional call type (e.g., 'audio', 'video')

        Returns:
            Result: API response confirming call initiation

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Devices/operation/Make%20VoIP%20Call
        """
        params = {
            "locationId": location_id,
        }
        body = {
            "callee": callee,
        }
        if call_type is not None:
            body["type"] = call_type
        result: Result = self.adapter.put(
            f"/cloud/json/devices/{device_id}/voipCall",
            ep_params=params,
            ep_json=json.dumps(body),
        )
        return result

    def hangup_device_voip_call(
        self,
        device_id: str,
        location_id: int,
    ):
        """
        Hang up an active VoIP call for a device.

        Args:
            device_id: Device ID to hang up call for
            location_id: Location ID containing the device

        Returns:
            Result: API response confirming call hangup

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Devices/operation/Hagn%20Up%20VoIP%20Call
        """
        params = {
            "locationId": location_id,
        }
        result: Result = self.adapter.delete(
            f"/cloud/json/devices/{device_id}/voipCall",
            ep_params=params,
        )
        return result

    def register_device_v2(
        self,
        device_data: Dict,
        auth_token: bool = None,
        start_date: str = None,
    ) -> Result:
        """
        Register a Device.

        Registration response will describe how the device should connect to the cloud server instance.

        Args:
            device_data: Device data as JSON object with 'device' key containing:
                - deviceId: Device ID (required, max 50 chars, no '/', '%', '#', '+')
                - deviceType: Device type (required)
                - locationId: Location ID (required)
                - desc: Device description (optional)
                - modelId: Device model ID (optional)
                - goalId: Goal ID (optional)
            auth_token: Request an authentication token for bi-directional authentication
            start_date: Start date in milliseconds or ISO 8601 format

        Returns:
            Result: API response with device registration result and connection details

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Devices/operation/Register%20a%20Device
        """
        params = {}
        if auth_token is not None:
            params["authToken"] = auth_token
        if start_date is not None:
            params["startDate"] = start_date
        result: Result = self.adapter.post(
            "/cloud/json/devices",
            ep_params=params if params else None,
            ep_json=device_data,
        )
        return result

    def update_location_device(
        self,
        location_id: int,
        device_id: str,
        device_data: Dict,
    ) -> Result:
        """
        Update Device.

        Update the device nickname / description, the device goal, the `newDevice` flag,
        the device model ID, the user ID, or move the device to another location.

        Args:
            location_id: Location ID that contains the device (required)
            device_id: Device ID to update (required)
            device_data: Device data as JSON object with 'device' key

        Returns:
            Result: API response confirming update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Devices/operation/Update%20Device
        """
        params = {
            "postId": location_id,  # Note: API spec shows postId but should be locationId
        }
        result: Result = self.adapter.put(
            f"/cloud/json/locations/{location_id}/devices/{device_id}",
            ep_json=device_data,
        )
        return result

    def delete_location_device(
        self,
        location_id: int,
        device_id: str,
    ) -> Result:
        """
        Delete Device from Location.

        Args:
            location_id: Location ID (required)
            device_id: Device ID (required)

        Returns:
            Result: API response confirming deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Devices/operation/Delete%20Device
        """
        result: Result = self.adapter.delete(
            f"/cloud/json/locations/{location_id}/devices/{device_id}",
        )
        return result

    def activate_device_sim_card(
        self,
        location_id: int,
        device_id: str,
        sim_card_data: Dict,
    ) -> Result:
        """
        Activate Sim Card.

        Using this API an administrator can manually activate or deactivate device SIM cards.

        Args:
            location_id: Location ID (required)
            device_id: Device ID (required)
            sim_card_data: SIM card data as JSON object

        Returns:
            Result: API response confirming SIM card activation/deactivation

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Devices/operation/Activate%20Sim%20Card
        """
        result: Result = self.adapter.put(
            f"/cloud/json/locations/{location_id}/devices/{device_id}/simCard",
            ep_json=sim_card_data,
        )
        return result

    def create_device_simulated_copy(
        self,
        location_id: int,
        device_id: str,
        simulated_location_id: int = None,
    ) -> Result:
        """
        Create Device Simulated Copy.

        Using this API an administrator can set a device as a source simulator and register
        another simulated device on a required location.

        Args:
            location_id: Location ID that contains the source device (required)
            device_id: Device ID acting as a source (required)
            simulated_location_id: Location ID where a simulated device will be registered

        Returns:
            Result: API response with simulated device ID

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Devices/operation/Create%20Device%20Simulated%20Copy
        """
        params = {}
        if simulated_location_id is not None:
            params["simulatedLocationId"] = simulated_location_id
        result: Result = self.adapter.post(
            f"/cloud/json/locations/{location_id}/devices/{device_id}/copySimulator",
            ep_params=params if params else None,
        )
        return result

    def link_device_space(
        self,
        location_id: int,
        device_id: str,
        space_id: int,
    ) -> Result:
        """
        Link Device Space.

        Link a device to a space within a location.

        Args:
            location_id: Location ID (required)
            device_id: Device ID (required)
            space_id: Space ID (required)

        Returns:
            Result: API response confirming link

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Devices/operation/Link%20Device%20Space
        """
        result: Result = self.adapter.put(
            f"/cloud/json/locations/{location_id}/devices/{device_id}/spaces/{space_id}",
        )
        return result

    def unlink_device_space(
        self,
        location_id: int,
        device_id: str,
        space_id: int,
    ) -> Result:
        """
        Unlink Device Space.

        Unlink a device from a space within a location.

        Args:
            location_id: Location ID (required)
            device_id: Device ID (required)
            space_id: Space ID (required)

        Returns:
            Result: API response confirming unlink

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Devices/operation/Unlink%20Device%20Space
        """
        result: Result = self.adapter.delete(
            f"/cloud/json/locations/{location_id}/devices/{device_id}/spaces/{space_id}",
        )
        return result

    def get_device_activation(
        self,
        location_id: int,
        device_type: int,
    ) -> Result:
        """
        Get Device Activation.

        Get device activation information for a location and device type.

        Args:
            location_id: Location ID (required)
            device_type: Device type (required)

        Returns:
            Result: API response with device activation information

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Devices/operation/Get%20Device%20Activation
        """
        result: Result = self.adapter.get(
            f"/cloud/json/locations/{location_id}/deviceActivation/{device_type}",
        )
        return result

    def set_device_properties_v2(
        self,
        device_id: str,
        properties: List[Dict],
    ) -> Result:
        """
        Set Device Properties.

        Set properties for a device.

        Args:
            device_id: Device ID (required)
            properties: List of property objects, each containing:
                - name: Property name
                - value: Property value
                - index: Optional property index

        Returns:
            Result: API response confirming properties set

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Devices/operation/Set%20Device%20Properties
        """
        data = {
            "properties": properties,
        }
        result: Result = self.adapter.post(
            f"/cloud/json/devices/{device_id}/properties",
            ep_json=data,
        )
        return result
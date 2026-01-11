# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "requests",
# ]
# ///

from typing import Dict, Optional

from ..api import API

from ...models import (
    Result,
)


class Firmware(API):
    """
    Firmware API for managing firmware versions, update jobs, and firmware groups.

    This class provides methods to manage firmware versions, create and manage firmware update jobs,
    and configure firmware groups for devices.

    Reference:
        https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Firmware
    """

    def get_firmware_versions(
        self,
        device_type: int,
    ) -> Result:
        """
        Get existing FW update versions by device type.

        Args:
            device_type: Device type

        Returns:
            Result: API response with firmware versions data

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Firmware/operation/Get%20Firmware%20Versions
        """
        params = {
            "deviceType": device_type,
        }
        result: Result = self.adapter.get(
            "/espapi/admin/json/fwversion",
            ep_params=params,
            ep_headers=self.adapter._get_headers(
                {"API_KEY": self.adapter._headers.get("ADMIN_KEY")}
            ),
        )
        return result

    def upload_firmware_version(
        self,
        device_type: int,
        firmware: str,
        file_name: str,
        check_sum: str,
        index: Optional[str] = None,
    ) -> Result:
        """
        Upload a new FW version (binary file, version number, check sum, device type, part index).
        Return the version ID.

        Args:
            device_type: Device type
            firmware: Version number
            file_name: File name
            check_sum: Hash value of the file to upload
            index: Part index

        Returns:
            Result: API response with versionId

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Firmware/operation/Upload%20Firmware%20Version
        """
        params = {
            "deviceType": device_type,
            "firmware": firmware,
            "fileName": file_name,
            "checkSum": check_sum,
        }
        if index is not None:
            params["index"] = index
        result: Result = self.adapter.post(
            "/espapi/admin/json/fwversion",
            ep_params=params,
            ep_headers=self.adapter._get_headers(
                {"API_KEY": self.adapter._headers.get("ADMIN_KEY")}
            ),
        )
        return result

    def delete_firmware_version(
        self,
        version_id: int,
    ) -> Result:
        """
        Delete existing FW version.

        Args:
            version_id: Firmware version ID

        Returns:
            Result: API response confirming deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Firmware/operation/Delete%20Firmware%20Versions
        """
        params = {
            "versionId": version_id,
        }
        result: Result = self.adapter.delete(
            "/espapi/admin/json/fwversion",
            ep_params=params,
            ep_headers=self.adapter._get_headers(
                {"API_KEY": self.adapter._headers.get("ADMIN_KEY")}
            ),
        )
        return result

    def get_firmware_groups(
        self,
        organization_id: Optional[int] = None,
    ) -> Result:
        """
        Get firmware groups.

        Args:
            organization_id: Organization ID filter

        Returns:
            Result: API response with firmware groups data

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Firmware/operation/Get%20Firmware%20Groups
        """
        params = {}
        if organization_id is not None:
            params["organizationId"] = organization_id
        result: Result = self.adapter.get(
            "/espapi/admin/json/fwgroup",
            ep_params=params if params else None,
            ep_headers=self.adapter._get_headers(
                {"API_KEY": self.adapter._headers.get("ADMIN_KEY")}
            ),
        )
        return result

    def update_firmware_group_for_device(
        self,
        device_id: str,
        group_id: Optional[int] = None,
    ) -> Result:
        """
        Update or clear the FW update group ID for a specific device instance.

        Args:
            device_id: Device instance ID
            group_id: Firmware group ID (optional, to clear the group)

        Returns:
            Result: API response confirming update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Firmware/operation/Update%20Firmware%20Group%20for%20Device
        """
        params = {
            "deviceId": device_id,
        }
        if group_id is not None:
            params["groupId"] = group_id
        result: Result = self.adapter.put(
            "/espapi/admin/json/fwgroup",
            ep_params=params,
            ep_headers=self.adapter._get_headers(
                {"API_KEY": self.adapter._headers.get("ADMIN_KEY")}
            ),
        )
        return result

    def get_firmware_update_jobs(
        self,
        device_type: int,
        group_id: Optional[int] = None,
    ) -> Result:
        """
        Get active FW update jobs. Normally, no more than one job could exist.

        Args:
            device_type: Device type
            group_id: Firmware group ID

        Returns:
            Result: API response with firmware update jobs data

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Firmware/operation/Get%20Update%20Jobs
        """
        params = {
            "deviceType": device_type,
        }
        if group_id is not None:
            params["groupId"] = group_id
        result: Result = self.adapter.get(
            "/espapi/admin/json/fwjobs",
            ep_params=params,
            ep_headers=self.adapter._get_headers(
                {"API_KEY": self.adapter._headers.get("ADMIN_KEY")}
            ),
        )
        return result

    def create_firmware_update_job(
        self,
        version_id: int,
        forced: Optional[bool] = None,
        group_id: Optional[int] = None,
    ) -> Result:
        """
        Create a new FW update job by version ID, FW group ID.
        Previous active job will be deleted.

        Args:
            version_id: Firmware version ID
            forced: Force the update job
            group_id: Firmware group ID

        Returns:
            Result: API response with jobId

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Firmware/operation/Create%20Update%20Job
        """
        params = {
            "versionId": version_id,
        }
        if forced is not None:
            params["forced"] = forced
        if group_id is not None:
            params["groupId"] = group_id
        result: Result = self.adapter.post(
            "/espapi/admin/json/fwjobs",
            ep_params=params,
            ep_headers=self.adapter._get_headers(
                {"API_KEY": self.adapter._headers.get("ADMIN_KEY")}
            ),
        )
        return result

    def delete_firmware_update_job(
        self,
        job_id: int,
    ) -> Result:
        """
        Delete existing FW update job.

        Args:
            job_id: Job ID

        Returns:
            Result: API response confirming deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Firmware/operation/Delete%20Update%20Job
        """
        params = {
            "jobId": job_id,
        }
        result: Result = self.adapter.delete(
            "/espapi/admin/json/fwjobs",
            ep_params=params,
            ep_headers=self.adapter._get_headers(
                {"API_KEY": self.adapter._headers.get("ADMIN_KEY")}
            ),
        )
        return result

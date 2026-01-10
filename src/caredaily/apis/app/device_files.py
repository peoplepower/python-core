# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "requests",
# ]
# ///

from typing import Dict

from ...models import Result
from ..api import API


class DeviceFiles(API):
    def upload_file(
        self,
        device_id: str,
        location_id: int,
        file_data: Dict = None,
        proxy_id: str = None,
        ext: str = None,
        expected_size: int = None,
        timestamp: str = None,
        timesec: str = None,
        duration: int = None,
        rotate: int = None,
        file_id: int = None,
        thumbnail: bool = None,
        incomplete: bool = None,
        upload_url: bool = None,
        file_type: int = None,
    ) -> Result:
        """
        Upload New Device File.

        The "Content-Type" header must be like `video/*`, `image/*`, `audio/*`, `text/plain` or `application/octet-stream`.

        Args:
            device_id: Device ID of the device that generated this file
            location_id: Location ID (used for proxyId if not provided)
            file_data: File data to upload
            proxy_id: Device ID of the proxy that this file is being uploaded through
            ext: File extension (For example, `mp4` or `png`)
            expected_size: Expected total size in bytes, if available
            timestamp: File creation time on the device in milliseconds
            timesec: File creation time on the device in seconds
            duration: Duration of the video in seconds, for reporting to the UI
            rotate: Rotation in degrees
            file_id: Existing file ID to replace the content and properties
            thumbnail: true - the content is a thumbnail image and the file content will be uploaded later
            incomplete: true - This file content will be added or replaced or extended later
            upload_url: true - Generate upload URL's for file's content and thumbnail
            file_type: File type

        Returns:
            Result: API response with file reference

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Device-Files/operation/Upload%20Device%20File
        """
        params = {
            "proxyId": proxy_id or device_id,
            "deviceId": device_id,
            "ext": ext,
            "expectedSize": expected_size,
            "timestamp": timestamp,
            "timesec": timesec,
            "duration": duration,
            "rotate": rotate,
            "fileId": file_id,
            "thumbnail": thumbnail,
            "incomplete": incomplete,
            "uploadUrl": upload_url,
            "type": file_type,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.post(
            "/espapi/cloud/json/files",
            ep_params=params,
            ep_json=file_data if file_data else None,
        )
        return result

    def get_files(
        self,
        device_id: str,
        location_id: int,
        file_type: int = None,
        owners: int = None,
        owner_id: int = None,
        device_description: str = None,
        start_date: str = None,
        end_date: str = None,
    ) -> Result:
        """
        Get Device Files.

        Return a list of the user's files, and any files that have been shared with this user by other users.

        Args:
            device_id: Camera device ID to filter files by the specific camera
            location_id: Files location ID (required)
            file_type: Type of file to obtain in the list
            owners: Filter files by owners bitmap (1 - only own files, 2 - only shared files, 3 - own and shared, 4 - own deleted files)
            owner_id: User ID to filter files by the specific owner
            device_description: Camera device description to filter files by the specific camera
            start_date: Optional start date to start the list of files
            end_date: Optional end date to end the list of files

        Returns:
            Result: API response with list of files

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Device-Files/operation/Get%20Device%20Files
        """
        params = {
            "locationId": location_id,
            "type": file_type,
            "owners": owners,
            "ownerId": owner_id,
            "deviceId": device_id,
            "deviceDescription": device_description,
            "startDate": start_date,
            "endDate": end_date,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/espapi/cloud/json/files",
            ep_params=params,
        )
        return result

    def delete_all_files(
        self,
        device_id: str,
        location_id: int,
    ) -> Result:
        """
        Delete All Device Files.

        This action will delete all files on the location that are not marked as favorite.

        Args:
            device_id: Device ID (for context, but locationId is the key parameter)
            location_id: Files location ID (required)

        Returns:
            Result: API response confirming deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Device-Files/operation/Delete%20All%20Device%20Files
        """
        params = {
            "locationId": location_id,
        }
        result: Result = self.adapter.delete(
            "/espapi/cloud/json/files",
            ep_params=params,
        )
        return result

    def upload_a_binary_files_parts_or_thumbnail(
        self,
        file_id: int,
        proxy_id: str,
        file_data: Dict = None,
        thumbnail: bool = None,
        incomplete: bool = None,
        index: int = None,
    ) -> Result:
        """
        Upload Device File Fragment.

        Allow to add a fragment to the content of the existing file or upload a thumbnail.
        Content-Type and PPCAuthorization must be set the same way as in uploading a new file.

        Args:
            file_id: Existing file ID
            proxy_id: Device ID of the proxy that this file is being uploaded through
            file_data: File fragment data to upload
            thumbnail: true - the content is a thumbnail image
            incomplete: true - The file will be extended later, false - This file is complete
            index: Fragment index starting from 0 to identify unique file fragment

        Returns:
            Result: API response with file reference

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Device-Files/operation/Upload%20Device%20File%20Fragment
        """
        params = {
            "proxyId": proxy_id,
            "thumbnail": thumbnail,
            "incomplete": incomplete,
            "index": index,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.post(
            f"/espapi/cloud/json/files/{file_id}",
            ep_params=params,
            ep_json=file_data if file_data else None,
        )
        return result

    def get_last_n_files(
        self,
        count: int,
        location_id: int,
        start_date: str = None,
        end_date: str = None,
        file_type: int = None,
        device_id: str = None,
        device_description: str = None,
    ) -> Result:
        """
        Get Last Device Files.

        Return a list of last N the user's files before specific date.

        Args:
            count: Maximum number of files to return
            location_id: Files location ID (required)
            start_date: Optional start date to start the list of files
            end_date: Optional end date to end the list of files, default is the current date
            file_type: Type of file to obtain in the list
            device_id: Camera device ID to filter files by the specific camera
            device_description: Camera device description to filter files by the specific camera

        Returns:
            Result: API response with list of files

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Device-Files/operation/Get%20Last%20Device%20Files
        """
        params = {
            "locationId": location_id,
            "startDate": start_date,
            "endDate": end_date,
            "type": file_type,
            "deviceId": device_id,
            "deviceDescription": device_description,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            f"/espapi/cloud/json/filesByCount/{count}",
            ep_params=params,
        )
        return result

    def get_file_download_urls(
        self,
        file_id: int,
        location_id: int,
        content: bool = None,
        thumbnail: bool = None,
        expiration: int = None,
    ) -> Result:
        """
        Get Device File Download URLs.

        A client can request temporary download URLs to get file and thumbnail
        content directly from S3 instead of copying it through the server.

        Args:
            file_id: File ID to download
            location_id: File location ID (required)
            content: Request file content URL
            thumbnail: Request thumbnail content URL
            expiration: URL's expiration in milliseconds since the current time

        Returns:
            Result: API response with download URLs

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Device-Files/operation/Get%20Device%20File%20Download%20URL
        """
        params = {
            "locationId": location_id,
            "content": content,
            "thumbnail": thumbnail,
            "expiration": expiration,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            f"/espapi/cloud/json/files/{file_id}/url",
            ep_params=params,
        )
        return result

    def download_file(
        self,
        file_id: int,
        location_id: int = None,
        user_id: int = None,
        thumbnail: bool = None,
        attach: bool = None,
        range_header: str = None,
    ) -> Result:
        """
        Download Device File.

        Download the file content or thumbnail. Supports range requests for partial content.

        Args:
            file_id: File ID to download
            location_id: File location ID
            user_id: User ID (optional)
            thumbnail: true - Download the thumbnail for this file, false - Download the actual file
            attach: Whether to download as attachment
            range_header: Data range header (e.g., "bytes=10240-20479")

        Returns:
            Result: API response with file content

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Device-Files/operation/Download%20Device%20File
        """
        params = {
            "locationId": location_id,
            "userId": user_id,
            "thumbnail": thumbnail,
            "attach": attach,
        }
        params = {k: v for k, v in params.items() if v is not None}
        headers = None
        if range_header:
            headers = {"Range": range_header}
        result: Result = self.adapter.get(
            f"/espapi/cloud/json/files/{file_id}",
            ep_params=params,
            ep_headers=headers,
        )
        return result

    def update_file(
        self,
        file_id: int,
        location_id: int,
        file_data: Dict = None,
        proxy_id: str = None,
        incomplete: bool = None,
        recover: bool = None,
        pure: bool = None,
    ) -> Result:
        """
        Update Device File Attributes.

        Update the file's attributes to declare, if the file has been viewed or not,
        if it's a favourite file and shouldn't be auto-deleted, and whether the file is available for public access.
        The file publisher (camera) can update it as completed.
        Also, this API can be used to recover deleted files.

        Args:
            file_id: File ID to update
            location_id: File location ID (required)
            file_data: File data as JSON object with 'file' key containing attributes (viewed, favourite, publicAccess)
            proxy_id: Device ID of the proxy that this file is being uploaded through
            incomplete: Set it to false for updating the file as completed
            recover: Set it to true to recover a deleted file
            pure: true - the server will not make any modification of the file content

        Returns:
            Result: API response confirming update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Device-Files/operation/Update%20Device%20File%20Attributes
        """
        params = {
            "locationId": location_id,
            "proxyId": proxy_id,
            "incomplete": incomplete,
            "recover": recover,
            "pure": pure,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.put(
            f"/espapi/cloud/json/files/{file_id}",
            ep_params=params,
            ep_json=file_data if file_data else None,
        )
        return result

    def delete_single_file(
        self,
        file_id: int,
        location_id: int,
    ) -> Result:
        """
        Delete Single Device File.

        Args:
            file_id: File ID to delete
            location_id: File location ID (required)

        Returns:
            Result: API response confirming deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Device-Files/operation/Delete%20Device%20%20File
        """
        params = {
            "locationId": location_id,
        }
        result: Result = self.adapter.delete(
            f"/espapi/cloud/json/files/{file_id}",
            ep_params=params,
        )
        return result

    def get_files_summary(
        self,
        aggregation: int,
        location_id: int,
        start_date: str = None,
        end_date: str = None,
        owners: int = None,
        details: bool = None,
    ) -> Result:
        """
        Get Summary of Device Files.

        Users can collect a massive list of files. This API helps describe what files exist
        on the server, so the user can drill into the data without downloading everything all at once.

        Aggregation:
        - 1: hour
        - 2: day
        - 3: month

        Args:
            aggregation: The duration of time across which to aggregate summary information
            location_id: Files location ID (required)
            start_date: Optional start date to start the list of files
            end_date: Optional end date to end the list of files
            owners: Filter files by owners bitmap (1 - only own files, 2 - only shared files, 3 - own and shared)
            details: Include detailed file information in summary

        Returns:
            Result: API response with files summary

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Device-Files/operation/Get%20Summary%20of%20Device%20Files
        """
        params = {
            "locationId": location_id,
            "startDate": start_date,
            "endDate": end_date,
            "owners": owners,
            "details": details,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            f"/espapi/cloud/json/filesSummary/{aggregation}",
            ep_params=params,
        )
        return result

    def get_file_info(
        self,
        file_id: int,
        location_id: int,
    ) -> Result:
        """
        Get Device File Information.

        For public files the API key header is optional.

        Args:
            file_id: File ID of the file for which to retrieve information
            location_id: File location ID (required)

        Returns:
            Result: API response with file information

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Device-Files/operation/Get%20Device%20File%20Information
        """
        params = {
            "locationId": location_id,
        }
        result: Result = self.adapter.get(
            f"/espapi/cloud/json/filesInfo/{file_id}",
            ep_params=params,
        )
        return result

    def get_file_devices(
        self,
        location_id: int,
    ) -> Result:
        """
        Get File Devices.

        Return all combinations of device IDs and device descriptions from existing user files.

        Args:
            location_id: Location ID (required)

        Returns:
            Result: API response with list of devices

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Device-Files/operation/Get%20File%20Devices
        """
        params = {
            "locationId": location_id,
        }
        result: Result = self.adapter.get(
            "/espapi/cloud/json/fileDevices",
            ep_params=params,
        )
        return result

    def apply_file_tags(
        self,
        file_id: int,
        tags: Dict,
    ) -> Result:
        """
        Apply File Tags.

        Args:
            file_id: File ID to apply tags to
            tags: Tags data as JSON object

        Returns:
            Result: API response confirming tags application

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Device-Files
        """
        result: Result = self.adapter.put(
            f"/espapi/cloud/json/files/{file_id}/tags",
            ep_json=tags if tags else None,
        )
        return result

    def delete_file_tags(
        self,
        file_id: int,
        tags: Dict = None,
    ) -> Result:
        """
        Delete File Tags.

        Args:
            file_id: File ID to delete tags from
            tags: Tags data as JSON object (optional, if not provided all tags are deleted)

        Returns:
            Result: API response confirming tags deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Device-Files
        """
        result: Result = self.adapter.delete(
            f"/espapi/cloud/json/files/{file_id}/tags",
            ep_json=tags if tags else None,
        )
        return result

    def report_file(
        self,
        file_id: int,
        report_type: str = "abuse",
    ) -> Result:
        """
        Report File Abuse.

        The API Key should only be used if a user is logged in and reporting abuse.
        If the user is not logged into the system and is instead browsing publicly,
        then you do not have to include an API key in the header.

        Args:
            file_id: File ID to report
            report_type: Type of report (typically "abuse", but may be changed to trigger different email template)

        Returns:
            Result: API response confirming report

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Device-Files/operation/Report%20Device%20File%20Abuse
        """
        result: Result = self.adapter.put(
            f"/espapi/cloud/json/files/{file_id}/report/{report_type}",
        )
        return result

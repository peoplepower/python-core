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


class AppFiles(API):
    def upload_file_content(
        self,
        file_content: bytes = None,
        content_type: str = "application/octet-stream",
        file_id: int = None,
        file_type: int = None,
        user_id: int = None,
        location_id: int = None,
        device_id: str = None,
        name: str = None,
        public_access: bool = None,
    ) -> Result:
        """
        Upload Application File Content.

        The "Content-Type" header must be like `image/*`, `video/*`, `audio/*` or `application/octet-stream`.

        Args:
            file_content: File content to upload (binary data)
            content_type: Content-Type header value (e.g., 'image/jpeg', 'video/mp4', 'audio/mp3', 'application/octet-stream')
            file_id: Existing file ID to replace the content and properties
            file_type: File type (required)
            user_id: User ID associated with this file
            location_id: Location ID associated with this file
            device_id: Device ID associated with this file
            name: File name
            public_access: Publicly available file

        Returns:
            Result: API response with file ID

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Application-Files/operation/Upload%20App%20File%20Content
        """
        params = {
            "fileId": file_id,
            "type": file_type,
            "userId": user_id,
            "locationId": location_id,
            "deviceId": device_id,
            "name": name,
            "publicAccess": public_access,
        }
        params = {k: v for k, v in params.items() if v is not None}
        headers = {"Content-Type": content_type} if file_content else None
        result: Result = self.adapter.post(
            "/cloud/json/appfiles",
            ep_params=params,
            ep_data=file_content if file_content else None,
            ep_headers=headers,
        )
        return result

    def get_files(
        self,
        file_id: int = None,
        file_type: int = None,
        user_id: int = None,
        location_id: int = None,
        device_id: str = None,
        name: str = None,
    ) -> Result:
        """
        Get Application Files.

        Return a list of the user's files filtered by query parameters.

        Args:
            file_id: File ID filter
            file_type: File type
            user_id: User ID associated with this file
            location_id: Location ID associated with this file
            device_id: Device ID associated with this file
            name: File name

        Returns:
            Result: API response with list of files

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Application-Files/operation/Get%20App%20Files
        """
        params = {
            "fileId": file_id,
            "type": file_type,
            "userId": user_id,
            "locationId": location_id,
            "deviceId": device_id,
            "name": name,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/cloud/json/appfiles",
            ep_params=params,
        )
        return result

    def download_file(
        self,
        file_id: int,
        user_id: int = None,
        location_id: int = None,
        attach: bool = None,
    ) -> Result:
        """
        Download Application File.

        The `Range` HTTP Header is optional, and will only return a chunk of the total content.

        Args:
            file_id: File ID to download (required)
            user_id: User ID to download the file as an administrator
            location_id: Location ID to download the file as an administrator
            attach: Download the file content as an attachments with the Content-Disposition header

        Returns:
            Result: API response with file content

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Application-Files/operation/Download%20App%20File
        """
        params = {
            "userId": user_id,
            "locationId": location_id,
            "attach": attach,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            f"/cloud/json/appfiles/{file_id}",
            ep_params=params,
        )
        return result

    def delete_file(
        self,
        file_id: int,
        user_id: int = None,
        location_id: int = None,
    ) -> Result:
        """
        Delete Application File.

        Args:
            file_id: File ID to delete (required)
            user_id: User ID to delete the file as an administrator
            location_id: Location ID to delete the file as an administrator

        Returns:
            Result: API response confirming deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Application-Files/operation/Delete%20App%20File
        """
        params = {
            "userId": user_id,
            "locationId": location_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.delete(
            f"/cloud/json/appfiles/{file_id}",
            ep_params=params,
        )
        return result

    def get_file_url(
        self,
        file_id: int,
    ) -> Result:
        """
        Get Application File URL.

        Get a pre-signed URL to download the application file.

        Args:
            file_id: File ID (required)

        Returns:
            Result: API response with file URL

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Application-Files/operation/Get%20App%20File%20URL
        """
        result: Result = self.adapter.get(
            f"/cloud/json/appfiles/{file_id}/url",
        )
        return result

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


class CloudConnectivity(API):
    """
    Cloud Connectivity API for accessing CareDaily cloud infrastructure information.

    This class provides methods to check availability, retrieve version information,
    and access cloud/server settings for devices and applications.
    """
    def check_availability(self):
        result = self.adapter.get(
            "/espapi/watch", ep_headers={"Content-Type": "text/plain"}
        )
        return result

    def get_version(self, version: bool = None, json_format: bool = None):
        params = {
            "version": "true" if version else None,
            "json": "true" if json_format else None,
        }
        params = {k: v for k, v in params.items() if v is not None}
        headers = self.adapter._get_headers()
        if version:
            headers["Content-Type"] = "text/html"
        elif json_format:
            headers["Content-Type"] = "application/json"
        else:
            headers["Content-Type"] = "application/xml"
        result = self.adapter.get(
            "/espapi/version", 
            ep_params=params, 
            ep_headers=headers
        )
        return result

    def get_cloud_settings(
        self, device_id: str = None, connected: bool = None, version: str = None
    ):
        params = {
            "device_id": device_id,
            "connected": connected,
            "version": version,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/cloud/json/settings", ep_params=params
        )
        return result

    def get_server_settings(
        self,
        server_type: ServerType = ServerType.RESTFUL,
        crtTag: bool = None,
        deviceId: str = None,
        connected: bool = None,
        brand: str = None,
        appName: str = None,
    ):
        # deviceId, connected and appName were removed from the API spec in v61
        # (streaming server type removed); kept here for backward compatibility.
        params = {
            "crtTag": crtTag,
            "deviceId": deviceId,
            "connected": connected,
            "brand": brand,
            "appName": appName,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/cloud/json/settingsServer/{type}".format(type=server_type.value), ep_params=params
        )
        return result

    def get_server_settings_url(
        self,
        server_type: ServerType = ServerType.RESTFUL,
        device_id: str = None,
        connected: bool = None,
        ssl: bool = None,
        brand: str = None,
        appName: str = None,
    ):
        # deviceId, connected and appName were removed from the API spec in v61
        # (streaming server type removed); kept here for backward compatibility.
        params = {
            "type": server_type.value,
            "deviceId": device_id,
            "connected": connected,
            "ssl": ssl,
            "brand": brand,
            "appName": appName,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/cloud/json/settingsServer", ep_params=params
        )
        return result
    
    def get_cloud_instances(
            self, 
            device_id: str
        ):
        params = {
            "deviceId": device_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/cloud/json/settingsCloud", ep_params=params
        )
        return result
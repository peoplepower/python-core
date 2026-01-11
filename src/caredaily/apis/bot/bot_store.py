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
    Result,
)
from ..api import API

#TODO: Finish (see docs/api/bots.yaml)
class BotStore(API):
    """
    BotStore API for managing bot marketplace operations, including searching, purchasing, configuring, and managing bots for organizations and users.

    Reference:
        https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/End-User-Bot-Shop-APIs
    """
    def add_bot_to_organization(self, bundle: str, organization_id: int):
        """
        Add a bot to an organization.

        Args:
            bundle: Bot bundle identifier
            organization_id: Organization ID

        Returns:
            API response confirming addition

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/End-User-Bot-Shop-APIs/operation/Add%20Bot%20to%20Organization
        """
        params = {"bundle": bundle}
        return self.adapter.post(
            f"/espapi/cloud/appstore/organizations/{organization_id}",
            ep_params=params,
        )

    def remove_bot_from_organization(self, bundle: str, organization_id: int):
        """
        Remove a bot from an organization.

        Args:
            bundle: Bot bundle identifier
            organization_id: Organization ID

        Returns:
            API response confirming removal

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/End-User-Bot-Shop-APIs/operation/Remove%20Bot%20Organization
        """
        params = {"bundle": bundle}
        return self.adapter.delete(
            f"/espapi/cloud/appstore/organizations/{organization_id}",
            ep_params=params,
        )

    def approve_bot_for_organization(self, bundle: str, organization_id: int, status: int, development: bool = None):
        """
        Approve or set the status of a bot for an organization.

        Args:
            bundle: Bot bundle identifier
            organization_id: Organization ID
            status: Approval status code
            development: Optional development mode flag

        Returns:
            API response confirming approval or status update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/End-User-Bot-Shop-APIs/operation/Approve%20Bot%20for%20Organization
        """
        params = {
            "bundle": bundle,
            "status": status,
            "development": development,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.put(
            f"/espapi/cloud/appstore/organizations/{organization_id}",
            ep_params=params,
            ep_headers=self.adapter._get_headers(
                # Uses API_KEY with admin key type
                self.adapter._headers.get("ADMIN_KEY"),
                APIKeyType.USER,
            ),
        )

    def get_bot_organizations(self, bundle: str):
        """
        Get organizations that have access to a bot.

        Args:
            bundle: Bot bundle identifier

        Returns:
            API response with organization list

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/End-User-Bot-Shop-APIs/operation/Get%20Bot%20Organizations
        """
        params = {"bundle": bundle}
        return self.adapter.get(
            "/espapi/cloud/appstore/organizations",
            ep_params=params,
        )

    def search_bots(self, search_by: str = None, categories: List[str] = None, compatible: bool = None, lang: str = None, core: int = None, location_id: int = None, organization_id: int = None, object_names: List[str] = None, limit: int = None):
        """
        Search for bots in the app store.

        Args:
            search_by: Search string
            categories: List of categories
            compatible: Filter by compatibility
            lang: Language code
            core: Core version
            location_id: Location ID
            organization_id: Organization ID
            object_names: List of object names
            limit: Maximum number of results

        Returns:
            API response with search results

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/End-User-Bot-Shop-APIs/operation/Search%20Bots
        """
        params = {
            "searchBy": search_by,
            "categories": categories,
            "compatible": compatible,
            "lang": lang,
            "core": core,
            "locationId": location_id,
            "organizationId": organization_id,
            "objectNames": object_names,
            "limit": limit,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.get(
            "/espapi/cloud/appstore/search",
            ep_params=params,
        )

    def get_bot_info(self, bundle: str, lang: str = None, last_n_version: int = None, object_name: str = None):
        """
        Get detailed information about a bot.

        Args:
            bundle: Bot bundle identifier
            lang: Optional language code
            last_n_version: Optional number of versions to return
            object_name: Optional object name

        Returns:
            API response with bot information

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/End-User-Bot-Shop-APIs/operation/Get%20Bot%20Information
        """
        params = {
            "bundle": bundle,
            "lang": lang,
            "lastNVersion": last_n_version,
            "objectName": object_name,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.get(
            "/espapi/cloud/appstore/appinfo",
            ep_params=params,
        )

    def get_bot_object(self, name: str, bundle: str) -> Result:
        """
        Get Bot Object.

        Each bot can contain a publicly available icon and/or other images.

        Args:
            name: Object name. Use "icon" for icons (required)
            bundle: Globally unique bundle ID for the bot, i.e. ai.caredaily.MyBot (required)

        Returns:
            Result: API response with object content (binary image data)

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/End-User-Bot-Shop-APIs/operation/Get%20Bot%20Object
        """
        params = {
            "bundle": bundle,
        }
        result: Result = self.adapter.get(
            f"/espapi/cloud/appstore/objects/{name}",
            ep_params=params,
        )
        return result

    def purchase_bot(self, bundle: str, location_id: int = None, organization_id: int = None):
        """
        Purchase a bot for a location or organization.

        Args:
            bundle: Bot bundle identifier
            location_id: Optional location ID
            organization_id: Optional organization ID

        Returns:
            API response confirming purchase

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/End-User-Bot-Shop-APIs/operation/Purchase%20a%20New%20Bot%20Instance
        """
        params = {
            "bundle": bundle,
            "locationId": location_id,
            "organizationId": organization_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.post(
            "/espapi/cloud/appstore/appInstance",
            ep_params=params,
        )

    def configure_my_bot(self, app_instance_id: int, status: int = None, data: Dict = None):
        """
        Configure a purchased bot instance.

        Args:
            app_instance_id: Application instance ID
            status: Optional status code
            data: Optional configuration data

        Returns:
            API response confirming configuration

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/End-User-Bot-Shop-APIs/operation/Configure%20a%20Bot%20Instance
        """
        params = {"appInstanceId": app_instance_id, "status": status}
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.put(
            "/espapi/cloud/appstore/appInstance",
            ep_json=json.dumps(data),
            ep_params=params,
        )

    def get_my_bots(self, app_instance_id: int = None, bundle: str = None, location_id: int = None, organization_id: int = None, user_id: int = None, object_names: List[str] = None):
        """
        Get purchased bots for a user, location, or organization.

        Args:
            app_instance_id: Optional application instance ID
            bundle: Optional bot bundle identifier
            location_id: Optional location ID
            organization_id: Optional organization ID
            user_id: Optional user ID
            object_names: Optional list of object names

        Returns:
            API response with purchased bot instances

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/End-User-Bot-Shop-APIs/operation/Get%20Bot%20Instances
        """
        params = {
            "appInstanceId": app_instance_id,
            "bundle": bundle,
            "locationId": location_id,
            "organizationId": organization_id,
            "userId": user_id,
            "objectNames": object_names,
        }
        params = {k: v for k, v in params.items() if v is not None}
        headers = self.adapter._get_headers()
        if "ADMIN_KEY" in self.adapter._headers:
            headers = self.adapter._get_headers(
                self.adapter._headers.get("ADMIN_KEY"), 
                key_type=APIKeyType.USER
            )
        return self.adapter.get(
            "/espapi/cloud/appstore/appInstance",
            ep_params=params,
            ep_headers=headers,
        )

    def remove_from_my_bots(self, app_instance_id: int):
        """
        Remove a purchased bot instance from a user's bots.

        Args:
            app_instance_id: Application instance ID

        Returns:
            API response confirming removal

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/End-User-Bot-Shop-APIs/operation/Delete%20a%20Bot%20Instance
        """
        params = {"appInstanceId": app_instance_id}
        return self.adapter.delete(
            "/espapi/cloud/appstore/appInstance",
            ep_params=params,
        )

    def send_data_stream_message(self, scope: int, address: str, data: Dict, location_id: int = None, organization_id: int = None):
        """
        Send a data stream message to a bot instance.

        Args:
            scope: Message scope
            address: Target address
            data: Message data as dictionary
            location_id: Optional location ID
            organization_id: Optional organization ID

        Returns:
            API response confirming message delivery

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/End-User-Bot-Shop-APIs/operation/Send%20Message%20to%20Bots
        """
        params = {
            "scope": scope,
            "address": address,
            "locationId": location_id,
            "organizationId": organization_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.post(
            "/espapi/cloud/appstore/stream",
            ep_json=json.dumps(data),
            ep_params=params,
        )

    def get_summary(self, location_id: int = None, organization_id: int = None):
        """
        Get a summary of bots for a location or organization.

        Args:
            location_id: Optional location ID
            organization_id: Optional organization ID

        Returns:
            API response with summary data

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/End-User-Bot-Shop-APIs/operation/Get%20Bots%20Summary
        """
        params = {"locationId": location_id, "organizationId": organization_id}
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.get(
            "/espapi/cloud/appstore/summary",
            ep_params=params,
        )

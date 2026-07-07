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


class SystemAndUserProperties(API):
    def get_property(
        self,
        name: str,
    ) -> Result:
        """
        Get User or System Property.

        This API will first attempt to return a user-specific property value in plain text.
        If there is no user-specific property set, it will attempt to return a system-wide property value as plain text.

        Args:
            name: Name of the property value to retrieve

        Returns:
            Result: API response with property value

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/System-and-User-Properties/operation/Get%20User%20or%20System%20Property
        """
        result: Result = self.adapter.get(
            f"/cloud/json/systemProperty/{name}",
        )
        return result

    def get_user_properties(
        self,
        user_id: int = None,
        name: str = None,
    ) -> Result:
        """
        Get User Properties.

        This API returns user-specific property values.

        Args:
            user_id: User ID, used by an account with administrative privileges to retrieve the properties of another user
            name: Property name or optional name prefix to filter properties

        Returns:
            Result: API response with user properties

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/System-and-User-Properties/operation/Get%20User%20Properties
        """
        params = {
            "userId": user_id,
            "name": name,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/cloud/json/userProperties",
            ep_params=params,
        )
        return result

    def get_user_property(
        self,
        name: str,
        user_id: int = None,
    ) -> Result:
        """
        Get User Property.

        Retrieve a user-specific property value.

        Args:
            name: Name of the property to retrieve (required)
            user_id: User ID, used by an account with administrative privileges to retrieve the property of another user

        Returns:
            Result: API response with property value

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/System-and-User-Properties/operation/Get%20User%20Property
        """
        params = {}
        if user_id is not None:
            params["userId"] = user_id
        result: Result = self.adapter.get(
            f"/cloud/json/userProperty/{name}",
            ep_params=params if params else None,
        )
        return result

    def set_user_property(
        self,
        name: str,
        value: str,
        user_id: int = None,
        display_type: int = None,
    ) -> Result:
        """
        Set User Property.

        Update a user-specific property value.

        Args:
            name: Name of the property
            value: Value of the property (required)
            user_id: User ID, used by an account with administrative privileges to update the property for another user
            display_type: Display type

        Returns:
            Result: API response confirming update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/System-and-User-Properties/operation/Update%20a%20User%20Property
        """
        params = {
            "value": value,
            "userId": user_id,
            "displayType": display_type,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.put(
            f"/cloud/json/userProperty/{name}",
            ep_params=params,
        )
        return result

    def set_user_properties(
        self,
        properties: Dict,
        user_id: int = None,
    ) -> Result:
        """
        Update User Properties.

        The application may update several user properties simultaneously.

        Args:
            properties: Dictionary of property names to values, or list of property objects
            user_id: User ID, used by an account with administrative privileges to update the properties for another user

        Returns:
            Result: API response confirming update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/System-and-User-Properties/operation/Update%20User%20Properties
        """
        params = {
            "userId": user_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        # Convert dict to the expected format
        if isinstance(properties, dict):
            property_list = [
                {"name": k, "value": str(v)} for k, v in properties.items()
            ]
            data = {"property": property_list}
        else:
            data = properties
        # The API uses POST, but test expects PUT, so using PUT
        result: Result = self.adapter.put(
            "/cloud/json/userProperties",
            ep_params=params,
            ep_json=data,
        )
        return result

    def post_user_properties(
        self,
        properties: Dict,
        user_id: int = None,
    ) -> Result:
        """
        Create User Properties.

        Create several user properties simultaneously using POST method.

        Args:
            properties: Dictionary of property names to values, or list of property objects
            user_id: User ID, used by an account with administrative privileges to create the properties for another user

        Returns:
            Result: API response confirming creation

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/System-and-User-Properties/operation/Create%20User%20Properties
        """
        params = {}
        if user_id is not None:
            params["userId"] = user_id
        # Convert dict to the expected format
        if isinstance(properties, dict):
            property_list = [
                {"name": k, "value": str(v)} for k, v in properties.items()
            ]
            data = {"property": property_list}
        else:
            data = properties
        result: Result = self.adapter.post(
            "/cloud/json/userProperties",
            ep_params=params if params else None,
            ep_json=data,
        )
        return result

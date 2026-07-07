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


class CloudsIntegration(API):
    def get_3rd_party_clouds(self) -> Result:
        """
        Get Third-Party Clouds.

        This API returns a list of supported third-party clouds/applications, where a user may obtain authorization.

        Returns:
            Result: API response with list of third-party clouds/applications

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Clouds-Integration/operation/Get%20Third-Party%20Clouds
        """
        result: Result = self.adapter.get("/espapi/cloud/json/authorize")
        return result

    def access_3rd_party_cloud(
        self,
        cloud_id: str,
        credentials: Dict = None,
        location_id: int = None,
        scope: str = None,
        brand: str = None,
    ) -> Result:
        """
        Access a Third-Party Cloud.

        This URL is meant to be loaded in a web view.
        It will redirect a user to the third party application web page for authenticating and authorizing access.

        Args:
            cloud_id: Application/Cloud ID
            credentials: Credentials data for accessing the cloud
            location_id: Location ID where the 3rd party devices and services will be linked
            scope: OAuth2 scope
            brand: Force forwarding user to a specific branded page

        Returns:
            Result: API response

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Clouds-Integration/operation/Access%20a%20Third-Party%20Cloud
        """
        params = {
            "locationId": location_id,
            "scope": scope,
            "brand": brand,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.post(
            f"/espapi/auth/authorize/{cloud_id}",
            ep_params=params,
            ep_json=credentials if credentials else None,
        )
        return result

    def authorize_3rd_party_cloud(
        self,
        app_id: int,
        location_id: int,
        scope: Optional[str] = None,
        brand: Optional[str] = None,
    ) -> Result:
        """
        Access a Third-Party Cloud.

        This URL is meant to be loaded in a web view.
        It will redirect a user to the third party application web page for authenticating and authorizing access
        to user's data in the external application.

        Args:
            app_id: Application ID (required)
            location_id: Location ID where the 3rd party devices and services will be linked (required)
            scope: OAuth2 scope
            brand: Brand

        Returns:
            Result: API response with redirect URL

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Clouds-Integration/operation/Access%20a%20Third-Party%20Cloud
        """
        params = {
            "locationId": location_id,
        }
        if scope is not None:
            params["scope"] = scope
        if brand is not None:
            params["brand"] = brand
        result: Result = self.adapter.get(
            f"/espapi/auth/authorize/{app_id}",
            ep_params=params,
        )
        return result

    def approve_oauth_authorization(
        self,
        approved: bool,
        client_id: str,
        state: Optional[str] = None,
        location_id: Optional[int] = None,
    ) -> Result:
        """
        Approve or Deny Authorization.

        Allow a user to approve or deny an authorization request from the third-party application.
        The user can choose the location to access.
        The user will be redirected to the external application web page.

        Args:
            approved: true - The third-party app is approved, false - The third-party app is not approved (required)
            client_id: The third-party client identifier (required)
            state: OAuth state parameter
            location_id: Location ID to access

        Returns:
            Result: API response with redirect information

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Clouds-Integration/operation/Approve%20or%20Deny%20Authorization
        """
        params = {
            "client_id": client_id,
        }
        if state is not None:
            params["state"] = state
        if location_id is not None:
            params["locationId"] = location_id
        result: Result = self.adapter.get(
            "/espapi/oauth/approve/{approved}".format(approved="true" if approved else "false"),
            ep_params=params,
        )
        return result

    def revoke_access_to_3rd_party_cloud(
        self,
        cloud_id: str,
        location_id: int = None,
    ) -> Result:
        """
        Revoke Access to a Third-Party Cloud.

        The user may revoke authorization for the Care Daily AI Platform to access the user's data on a third-party host.
        This operation will delete all corresponding access and refresh tokens.

        Args:
            cloud_id: The authorization ID to revoke access to
            location_id: Location ID to revoke access

        Returns:
            Result: API response confirming revocation

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Clouds-Integration/operation/Revoke%20Access%20to%20a%20Third-Party%20Cloud
        """
        params = {
            "locationId": location_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.delete(
            f"/espapi/cloud/json/authorizations/{cloud_id}",
            ep_params=params,
        )
        return result

    def authorize_3rd_party_client(
        self,
        client_data: Dict,
        brand: str = None,
    ) -> Result:
        """
        Authorize a Third-Party Application.

        OAuth allows the Care Daily AI Platform to act as a client or a host for a third-party application.
        As a host, the Care Daily AI Platform provides authorization information to third party applications using the OAuth 2.0 open standard.

        Args:
            client_data: Client authorization data including client_id, response_type, state, etc.
            brand: Brand

        Returns:
            Result: API response

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Clouds-Integration/operation/Authorize%20a%20Third-Party%20Application
        """
        params = {
            "brand": brand,
        }
        params = {k: v for k, v in params.items() if v is not None}
        # Merge client_data into params
        if client_data:
            params.update(client_data)
        result: Result = self.adapter.post(
            "/espapi/oauth/authorize",
            ep_params=params,
        )
        return result

    def authorize_3rd_party_client_get(
        self,
        brand: str,
        client_id: str,
        response_type: str,
        state: Optional[str] = None,
        redirect_uri: Optional[str] = None,
        scope: Optional[str] = None,
    ) -> Result:
        """
        Authorize a Third-Party Application.

        This endpoint begins the process of authorizing a third-party application (the client) to access the user's data.
        The client has to redirect the user to this HTTP GET URL.

        Args:
            brand: Brand (required)
            client_id: The third-party client identifier (required)
            response_type: The OAuth 2.0 response type (required)
            state: The third-party client state
            redirect_uri: The callback URL
            scope: OAuth2 scope

        Returns:
            Result: API response with redirect URL

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Clouds-Integration/operation/Authorize%20a%20Third-Party%20Application
        """
        params = {
            "client_id": client_id,
            "response_type": response_type,
        }
        if state is not None:
            params["state"] = state
        if redirect_uri is not None:
            params["redirect_uri"] = redirect_uri
        if scope is not None:
            params["scope"] = scope
        result: Result = self.adapter.get(
            f"/espapi/oauth/authorize/{brand}",
            ep_params=params,
        )
        return result

    def approve_or_deny_client_authorization(
        self,
        client_id: str,
        approve: bool,
        state: str = None,
        response_type: str = None,
        location_id: int = None,
        brand: str = None,
    ) -> Result:
        """
        Approve or Deny Authorization.

        Allow a user to approve or deny an authorization request from the third-party application.

        Args:
            client_id: The third-party client identifier (required)
            approve: true - The third-party app is approved, false - The third-party app is not approved (required)
            state: The third-party client state
            response_type: The OAuth 2.0 response type (required)
            location_id: Location ID, where the third-party app is going to have access
            brand: Brand

        Returns:
            Result: API response

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Clouds-Integration/operation/Approve%20or%20Deny%20Authorization
        """
        params = {
            "client_id": client_id,
            "state": state,
            "response_type": response_type,
            "locationId": location_id,
            "brand": brand,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.post(
            "/espapi/oauth/approve/{approved}".format(approved="true" if approve else "false"),
            ep_params=params,
        )
        return result

    def approve_or_deny_authorization_get(
        self,
        approved: bool,
        client_id: str,
        state: Optional[str] = None,
        response_type: Optional[str] = None,
        location_id: Optional[int] = None,
        brand: Optional[str] = None,
    ) -> Result:
        """
        Approve or Deny Authorization.

        Allow a user to approve or deny an authorization request from the third-party application.
        The user can choose the location to access.

        Args:
            approved: true - The third-party app is approved, false - The third-party app is not approved (required)
            client_id: The third-party client identifier (required)
            state: The third-party client state
            response_type: The OAuth 2.0 response type
            location_id: Location ID, where the third-party app is going to have access
            brand: Brand

        Returns:
            Result: API response with redirect URL

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Clouds-Integration/operation/Approve%20or%20Deny%20Authorization
        """
        params = {
            "client_id": client_id,
        }
        if state is not None:
            params["state"] = state
        if response_type is not None:
            params["response_type"] = response_type
        if location_id is not None:
            params["locationId"] = location_id
        if brand is not None:
            params["brand"] = brand
        result: Result = self.adapter.get(
            "/espapi/oauth/approve/{approved}".format(approved="true" if approved else "false"),
            ep_params=params,
        )
        return result

    def get_access_token(
        self,
        client_id: str,
        code: str = None,
        refresh_token: str = None,
        client_secret: str = None,
    ) -> Result:
        """
        Get Access Token.

        This API uses an authorization code or a previously generated refresh token to grant new access to the Care Daily AI Platform.
        It returns a new access token, a token type, expiration time, and a refresh token.

        Args:
            client_id: The client ID (required)
            code: The authorization code
            refresh_token: A refresh token previously received from getting an access token with an authorization code
            client_secret: The client secret

        Returns:
            Result: API response with access token

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Clouds-Integration/operation/Get%20Access%20Token
        """
        params = {
            "client_id": client_id,
            "code": code,
            "refresh_token": refresh_token,
            "client_secret": client_secret,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/espapi/oauth/token",
            ep_params=params,
        )
        return result

    def get_access_token_post(
        self,
        client_id: str,
        code: Optional[str] = None,
        refresh_token: Optional[str] = None,
        client_secret: Optional[str] = None,
        grant_type: Optional[str] = None,
    ) -> Result:
        """
        Get Access Token.

        This API uses an authorization code or a previously generated refresh token to grant new access to the Care Daily AI Platform.
        It returns a new access token, a token type, expiration time, and a refresh token.

        All parameters should be sent in the `application/x-www-form-urlencoded` format. However, query parameters are supported as well.

        Args:
            client_id: The client ID (required)
            code: The authorization code
            refresh_token: A refresh token previously received from getting an access token with an authorization code
            client_secret: The client secret
            grant_type: The grant type (not used when authorization code or refresh token are provided, otherwise only "client_credentials" is supported)

        Returns:
            Result: API response with access token

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Clouds-Integration/operation/Get%20Access%20Token
        """
        params = {
            "client_id": client_id,
        }
        if code is not None:
            params["code"] = code
        if refresh_token is not None:
            params["refresh_token"] = refresh_token
        if client_secret is not None:
            params["client_secret"] = client_secret
        if grant_type is not None:
            params["grant_type"] = grant_type
        result: Result = self.adapter.post(
            "/espapi/oauth/token",
            ep_params=params,
        )
        return result

    def update_oauth_client(
        self,
        client_id: str,
        client_data: Dict,
        location_id: int = None,
    ) -> Result:
        """
        Update OAuth Client.

        Args:
            client_id: The Client ID (required)
            client_data: Client data including devices array
            location_id: Access to devices on specific location

        Returns:
            Result: API response

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Clouds-Integration/operation/Update%20OAuth%20Client
        """
        params = {
            "clientId": client_id,
            "locationId": location_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.put(
            "/espapi/cloud/json/authClient",
            ep_params=params,
            ep_json=client_data if client_data else None,
        )
        return result

    def create_oauth_client(
        self,
        client_data: Dict,
        location_id: int = None,
    ) -> Result:
        """
        Update OAuth Client.

        Create or update an OAuth client.

        Args:
            client_data: Client data including devices array
            location_id: Access to devices on specific location

        Returns:
            Result: API response

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Clouds-Integration/operation/Update%20OAuth%20Client
        """
        params = {}
        if location_id is not None:
            params["locationId"] = location_id
        result: Result = self.adapter.post(
            "/espapi/cloud/json/authClient",
            ep_params=params if params else None,
            ep_json=client_data,
        )
        return result

    def revoke_oauth_client(
        self,
        client_id: str,
        user_id: int = None,
        location_id: int = None,
    ) -> Result:
        """
        Revoke OAuth Client.

        The user may revoke authorization for a third party to access the user's data on the Care Daily AI Platform.
        This operation will delete all corresponding access and refresh tokens.

        Args:
            client_id: The Client ID to revoke or authorization for all clients will be revoked (required)
            user_id: Administrators may revoke access to third-party clients on behalf of a user
            location_id: Revoke authorization for specific location

        Returns:
            Result: API response confirming revocation

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Clouds-Integration/operation/Revoke%20OAuth%20Client
        """
        params = {
            "clientId": client_id,
            "userId": user_id,
            "locationId": location_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.delete(
            "/espapi/cloud/json/authClient",
            ep_params=params,
        )
        return result

    def get_commissioning_config(
        self,
        application_id: int,
    ) -> Result:
        """
        Get Commissioning Configuration from Third-Party Cloud.

        Retrieve the commissioning configuration profiles for a third-party cloud
        application. This API does not require authentication.

        Args:
            application_id: Application/Cloud ID

        Returns:
            Result: API response with commissioning configuration profiles

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Clouds-Integration/operation/Commissioning%20Configuration
        """
        params = {
            "applicationId": application_id,
        }
        result: Result = self.adapter.get(
            "/espapi/cloud/json/commissioningConfig",
            ep_params=params,
        )
        return result

    def start_commissioning_session(
        self,
        location_id: int,
        application_id: int,
        auth_id: int = None,
        params_data: Dict = None,
    ) -> Result:
        """
        Start Commissioning Session for Third-Party Cloud.

        Args:
            location_id: Location ID where the third-party devices will be linked
            application_id: Application/Cloud ID
            auth_id: Existing authorization ID
            params_data: Commissioning parameters as key-value pairs

        Returns:
            Result: API response with the commissioning session (authId and value)

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Clouds-Integration/operation/Commissioning%20Session
        """
        params = {
            "locationId": location_id,
            "applicationId": application_id,
            "authId": auth_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        data = {"params": params_data} if params_data else None
        result: Result = self.adapter.post(
            "/espapi/cloud/json/commissioning",
            ep_params=params,
            ep_json=data,
        )
        return result

    def discover_devices(
        self,
        auth_id: int,
        location_id: int,
    ) -> Result:
        """
        Discover devices from Third-Party Cloud.

        Trigger device discovery for an existing third-party cloud authorization.

        Args:
            auth_id: Authorization ID
            location_id: Location ID where the discovered devices will be linked

        Returns:
            Result: API response confirming discovery started

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Clouds-Integration/operation/Discover%20devices%20from%20Third-Party%20Cloud
        """
        params = {
            "locationId": location_id,
        }
        result: Result = self.adapter.put(
            f"/espapi/cloud/json/authorizations/{auth_id}/discover",
            ep_params=params,
        )
        return result

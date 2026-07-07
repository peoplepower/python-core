# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "requests",
# ]
# ///

import json

from ...models import (
    APIKeyType,
    Result,
    SignatureAlgorithm,
)
from ..api import API


class Authentication(API):
    """
    Cloud Connectivity API for accessing CareDaily cloud infrastructure information.

    This class provides methods to check availability, retrieve version information,
    and access cloud/server settings for devices and applications.
    """
    def login_by_username(
        self,
        username: str,
        password: str = None,
        passcode: str = None,
        expiry: int = None,
        key_type: APIKeyType = None,
        app_name: str = None,
        brand: str = None,
        client_id: str = None,
        pref_delivery_type: int = None,
        sms_prefix: str = None,
        app_hash: str = None,
        totp: bool = None,
        sign: bool = None,
        sign_algorithm: SignatureAlgorithm = None,
    ):
        """
        Login with username and password to obtain an API key.

        Args:
            username: Username, phone number with country code, or email
            password: User password (sent in header)
            passcode: One-time passcode for additional verification
            expiry: Key expiry time in milliseconds
            key_type: Type of API key to generate
            app_name: Application name
            brand: Brand name
            client_id: OAuth client ID
            pref_delivery_type: Preferred delivery type for passcode
            sms_prefix: SMS prefix message
            app_hash: Application hash for Android SMS API
            totp: Enable TOTP verification
            sign: Enable request signing
            sign_algorithm: Signature algorithm to use

        Returns:
            Result: API response with API key and user information

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Authentication/operation/Login%20by%20Username
        """
        params = {
            "username": username,
            "expiry": expiry,
            "keyType": key_type.value if key_type else None,
            "appName": app_name,
            "brand": brand,
            "clientId": client_id,
            "prefDeliveryType": pref_delivery_type,
            "smsPrefix": sms_prefix,
            "appHash": app_hash,
            "totp": totp,
            "sign": sign,
            "signAlgorithm": sign_algorithm.value if sign_algorithm else None,
        }
        params = {k: v for k, v in params.items() if v is not None}
        headers = {
            "PASSWORD": password,
            "passcode": passcode,
        }
        headers = {k: v for k, v in headers.items() if v is not None}
        result: Result = self.adapter.get(
            "/cloud/json/login", ep_params=params, ep_headers=headers
        )
        return result

    def send_passcode(
        self,
        username: str,
        pref_delivery_type: int = None,
        brand: str = None,
        prefix: str = None,
        app_hash: str = None,
    ):
        """
        Send a passcode to a user for authentication.

        Args:
            username: Username, phone number with country code or email
            pref_delivery_type: Preferred delivery type (SMS or email)
            brand: Brand name
            prefix: SMS prefix message
            app_hash: Application hash for Android SMS API

        Returns:
            Result: API response with result code and message

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Authentication/operation/Send%20Passcode
        """
        params = {
            "username": username,
            "prefDeliveryType": pref_delivery_type,
            "brand": brand,
            "prefix": prefix,
            "appHash": app_hash,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/cloud/json/passcode", ep_params=params
        )
        return result

    def login_by_key(
        self,
        key: str,
        passcode: str = None,
        key_type: APIKeyType = None,
        expiry: int = None,
        pref_delivery_type: int = None,
        brand: str = None,
        client_id: str = None,
    ):
        """
        Login using an existing API key.

        Args:
            key: API key to authenticate with
            passcode: Optional passcode for additional verification
            key_type: Type of API key to generate
            expiry: Key expiry time in milliseconds
            pref_delivery_type: Preferred delivery type for passcode
            brand: Brand name
            client_id: OAuth client ID

        Returns:
            Result: API response with new key information

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Authentication/operation/Login%20by%20Key
        """
        params = {
            "keyType": key_type.value if key_type else None,
            "expiry": expiry,
            "prefDeliveryType": pref_delivery_type,
            "brand": brand,
            "clientId": client_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        headers = {
            "API_KEY": key,
            "passcode": passcode,
        }
        headers = {k: v for k, v in headers.items() if v is not None}
        result: Result = self.adapter.get(
            "/cloud/json/loginByKey", ep_params=params, ep_headers=headers
        )
        return result

    def logout(self):
        """
        Logout and invalidate the current API key.

        Returns:
            Result: API response confirming logout

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Authentication/operation/Logout
        """
        result: Result = self.adapter.get("/cloud/json/logout")
        return result

    def _user_key_headers(self):
        """
        Headers for endpoints authenticated with the user API key.

        If the adapter is configured with an admin key, map it into the
        API_KEY header expected by app endpoints; otherwise keep the
        adapter's default headers.
        """
        admin_key = self.adapter._headers.get("ADMIN_KEY")
        if admin_key:
            headers = self.adapter._get_headers(
                api_key=admin_key,
                key_type=APIKeyType.USER,
            )
            # Suppress the adapter's base ADMIN_KEY header so the request
            # carries a single auth header (requests drops None values).
            headers["ADMIN_KEY"] = None
            return headers
        return None

    def create_totp_factor(
        self,
        name: str = None,
        issuer: str = None,
    ):
        """
        Create a new TOTP (Time-based One-Time Password) secret for two-factor authentication.

        Args:
            name: Name identifier for this TOTP factor
            issuer: Issuer name (typically the app or service name)

        Returns:
            Result: API response with TOTP secret and QR code URL

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Authentication/operation/Create%20TOTP%20Secret
        """
        params = {
            "name": name,
            "issuer": issuer,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.post(
            "/cloud/json/totp", 
            ep_params=params,
            ep_headers=self._user_key_headers()
        )
        return result

    def confirm_totp_factor(
        self,
        name: str,
        code: str,
    ):
        """
        Confirm and activate a TOTP factor by verifying a code.

        Args:
            name: Name of the TOTP factor to confirm
            code: TOTP code to verify

        Returns:
            Result: API response confirming activation

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Authentication/operation/Confirm%20TOTP%20Secret
        """
        params = {
            "name": name,
            "code": code,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.put(
            "/cloud/json/totp", 
            ep_params=params,
            ep_headers=self._user_key_headers()
        )
        return result

    def get_totp_factors(self):
        """
        Get all TOTP factors configured for the current user.

        Returns:
            Result: API response with list of TOTP factors

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Authentication/operation/Get%20TOTP%20Factors
        """
        result: Result = self.adapter.get(
            "/cloud/json/totp",
            ep_headers=self._user_key_headers()
        )
        return result

    def delete_totp_factor(
        self,
        name: str,
    ):
        """
        Delete a TOTP factor.

        Args:
            name: Name of the TOTP factor to delete

        Returns:
            Result: API response confirming deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Authentication/operation/Delete%20TOTP%20Factor
        """
        params = {
            "name": name,
        }
        result: Result = self.adapter.delete(
            "/cloud/json/totp", 
            ep_params=params,
            ep_headers=self._user_key_headers()
        )
        return result

    def get_private_key(
        self,
        app_name: str = None,
        end_user: bool = None,
    ):
        """
        Get a private signature key for request signing.

        Since API v61 this endpoint is authenticated with the user API key.

        Args:
            app_name: Application name
            end_user: Request a key for the end-user 1st step signature login

        Returns:
            Result: API response with private key

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Authentication/operation/Get%20Signature%20Private%20Key
        """
        params = {
            "appName": app_name,
            "endUser": end_user,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/cloud/json/signatureKey",
            ep_params=params,
            ep_headers=self._user_key_headers(),
        )
        return result

    def put_public_key(
        self,
        app_name: str,
        public_key: str,
        end_user: bool = None,
    ):
        """
        Upload a public key for request signature verification.

        Since API v61 this endpoint is authenticated with the user API key.

        Args:
            app_name: Application name
            public_key: Public key in PEM format
            end_user: Register the key for the end-user 1st step signature login

        Returns:
            Result: API response confirming upload

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Authentication/operation/Put%20Signature%20Public%20Key
        """
        params = {
            "appName": app_name,
            "endUser": end_user,
        }
        params = {k: v for k, v in params.items() if v is not None}
        data = {
            "publicKey": public_key,
        }
        result: Result = self.adapter.put(
            "/cloud/json/signatureKey",
            ep_params=params,
            ep_data=json.dumps(data),
            ep_headers=self._user_key_headers(),
        )
        return result

    def get_operation_token(
        self,
        token_type: int = None,
    ):
        """
        Get an operation token for specific operations.

        Args:
            token_type: Type of operation token to generate

        Returns:
            Result: API response with operation token

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Authentication/operation/Get%20Operation%20Token
        """
        params = {
            "type": token_type,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/cloud/json/token", ep_params=params
        )
        return result

    def get_auth_token(
        self,
        token_type: int,
        expiry: int,
        location_id: int = None,
    ):
        """
        Generate authorization tokens for use in other services.

        Token Types:
            7: Location token for MCP Server (requires location_id parameter)

        Args:
            token_type: Requested token type (required)
            expiry: Token expiry time from now in seconds (required)
            location_id: Location ID (required for token type 7)

        Returns:
            Result: API response with authorization token

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Authentication/operation/Get%20Auth%20Token
        """
        params = {
            "tokenType": token_type,
            "expiry": expiry,
            "locationId": location_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/cloud/json/authToken", ep_params=params
        )
        return result

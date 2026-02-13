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
            "/espapi/cloud/json/login", ep_params=params, ep_headers=headers
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
            "/espapi/cloud/json/passcode", ep_params=params
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
            "/espapi/cloud/json/loginByKey", ep_params=params, ep_headers=headers
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
        result: Result = self.adapter.get("/espapi/cloud/json/logout")
        return result

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
            "/espapi/cloud/json/totp", 
            ep_params=params,
            ep_headers=self.adapter._get_headers(
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            )
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
            "/espapi/cloud/json/totp", 
            ep_params=params,
            ep_headers=self.adapter._get_headers(
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            )
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
            "/espapi/cloud/json/totp",
            ep_headers=self.adapter._get_headers(
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            )
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
            "/espapi/cloud/json/totp", 
            ep_params=params,
            ep_headers=self.adapter._get_headers(
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            )
        )
        return result

    def get_private_key(
        self,
        app_name: str = None,
    ):
        """
        Get a private signature key for request signing.

        Args:
            app_name: Application name

        Returns:
            Result: API response with private key

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Authentication/operation/Get%20Private%20Key
        """
        params = {
            "appName": app_name,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/espapi/cloud/json/signatureKey", 
            ep_params=params,
            ep_headers=self.adapter._get_headers(
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            )
        )
        return result

    def put_public_key(
        self,
        app_name: str,
        public_key: str,
    ):
        """
        Upload a public key for request signature verification.

        Args:
            app_name: Application name
            public_key: Public key in PEM format

        Returns:
            Result: API response confirming upload

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Authentication/operation/Put%20Public%20Key
        """
        params = {
            "appName": app_name,
        }
        data = {
            "publicKey": public_key,
        }
        result: Result = self.adapter.put(
            "/espapi/cloud/json/signatureKey", 
            ep_params=params,
            ep_data=json.dumps(data),
            ep_headers=self.adapter._get_headers(
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            )
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
            "/espapi/cloud/json/token", ep_params=params
        )
        return result

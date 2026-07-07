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

class UserAccounts(API):
    """
    User Accounts API for managing user accounts and profiles.

    This class provides comprehensive methods for user account operations including
    registration, profile management, verification, password management, and user metadata.
    """

    def create_user_account(
        self,
        username: str,
        password: str = None,
        email: str = None,
        community_name: str = None,
        location_id: int = None,
        organization_id: int = None,
        user_id: int = None,
        forward: str = None,
    ):
        """
        Create a new user account.

        Args:
            username: Username for the new account
            password: Password for the new account (sent in header)
            email: Email address (can be same as username)
            community_name: Community or application name
            location_id: Optional location ID to associate with the user
            organization_id: Optional organization ID
            user_id: Optional user ID to update existing user
            forward: Forward URL after registration

        Returns:
            Result: API response with user creation result

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#create-user-account
        """
        params = {
            "username": username,
            "email": email,
            "communityName": community_name,
            "locationId": location_id,
            "organizationId": organization_id,
            "userId": user_id,
            "forward": forward,
        }
        params = {k: v for k, v in params.items() if v is not None}
        headers = {}
        if password:
            headers["PASSWORD"] = password
        headers = {k: v for k, v in headers.items() if v is not None}
        result: Result = self.adapter.post(
            "/cloud/json/user",
            ep_params=params,
            ep_headers=headers if headers else None,
        )
        return result

    def get_user_information(
        self,
        user_id: int = None,
        organization_id: int = None,
    ):
        """
        Get user information for the current user or a specific user.

        Args:
            user_id: Optional user ID to get information for (requires admin permissions)
            organization_id: Optional organization ID filter

        Returns:
            Result: API response containing user information including profile,
                   preferences, locations, and account status

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#get-user-information
        """
        params = {
            "userId": user_id,
            "organizationId": organization_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/cloud/json/user", ep_params=params
        )
        return result

    def update_user(
        self,
        email: str = None,
        username: str = None,
        alt_username: str = None,
        language: str = None,
        phone: str = None,
        first_name: str = None,
        last_name: str = None,
        pronoun: int = None,
        user_id: int = None,
    ):
        """
        Update user profile information.

        Args:
            email: New email address
            username: New username
            alt_username: Alternative username
            language: Preferred language code
            phone: Phone number with country code
            first_name: User's first name
            last_name: User's last name
            pronoun: Pronoun preference ID
            user_id: User ID to update (requires admin permissions)

        Returns:
            Result: API response with update result

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#update-user
        """
        params = {
            "email": email,
            "username": username,
            "altUsername": alt_username,
            "language": language,
            "phone": phone,
            "firstName": first_name,
            "lastName": last_name,
            "pronoun": pronoun,
            "userId": user_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.put(
            "/cloud/json/user", ep_params=params
        )
        return result

    def delete_user(
        self,
        user_id: int = None,
        send_email: bool = None,
    ):
        """
        Delete a user account.

        This operation will permanently delete the user account and all associated data.

        Args:
            user_id: User ID to delete (requires admin permissions)
            send_email: Whether to send confirmation email

        Returns:
            Result: API response confirming deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#delete-user
        """
        params = {
            "userId": user_id,
            "sendEmail": send_email,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.delete(
            "/cloud/json/user", ep_params=params
        )
        return result

    def get_pronouns(self):
        """
        Get list of available pronouns.

        Returns:
            Result: API response containing available pronoun options

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#get-pronouns
        """
        result: Result = self.adapter.get("/cloud/json/pronouns")
        return result

    def send_verification_message(
        self,
        type: int = None,
        brand: str = None,
    ):
        """
        Send a verification message to the user's email or phone.

        Args:
            type: Verification type (1=email, 2=SMS)
            brand: Brand name for message customization

        Returns:
            Result: API response indicating message was sent

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#send-verification-message
        """
        params = {
            "type": type,
            "brand": brand,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/cloud/json/emailVerificationMessage", ep_params=params
        )
        return result

    def provide_verification_code(
        self,
        code: str,
        type: int = None,
    ):
        """
        Provide verification code to verify email or phone.

        Args:
            code: Verification code received by user
            type: Verification type (1=email, 2=SMS)

        Returns:
            Result: API response confirming verification

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#provide-verification-code
        """
        params = {
            "code": code,
            "type": type,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.put(
            "/cloud/json/emailVerificationMessage", ep_params=params
        )
        return result

    def get_new_password(
        self,
        username: str,
        brand: str = None,
    ) -> Result:
        """
        Recover Password.

        If a user forgot his password or does not have one, this API can be used to recover user's password.

        The API will send an email to the user containing a temporary link, which is valid for the next hour,
        to the reset password page. When the user clicks on that link the web page is launched.
        After verification of token, the page shall allow the user to set a new password.
        The user must have a valid email address.

        Args:
            username: The username, which is typically the user's email address (required)
            brand: A parameter identifying a customer's specific email template

        Returns:
            Result: API response confirming password recovery email sent

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/User-Accounts/operation/Recover%20Password
        """
        params = {
            "username": username,
        }
        if brand is not None:
            params["brand"] = brand
        result: Result = self.adapter.get(
            "/cloud/json/newPassword",
            ep_params=params,
        )
        return result

    def put_new_password(
        self,
        new_password: str,
        old_password: str = None,
        passcode: str = None,
        user_id: int = None,
        brand: str = None,
        strong_password: bool = None,
        keep_key_version: bool = None,
    ):
        """
        Update user password.

        The app calls this API to submit a new password, if the user has the password already.

        To change the password an end users must provide either a temporary API key sent by email
        after calling the recover password API or a regular user API key and the old password together.

        Args:
            new_password: New password to set (sent in header)
            old_password: Current password for verification (sent in header)
            passcode: Optional passcode for additional verification
            user_id: User ID to update (requires admin permissions)
            brand: A parameter identifying a customer's specific notification template
            strong_password: Check if the password is strong
            keep_key_version: Keep the current user API key version to keep previously generated API keys active

        Returns:
            Result: API response confirming password change

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/User-Accounts/operation/Update%20Password
        """
        params = {}
        if user_id is not None:
            params["userId"] = user_id
        if brand is not None:
            params["brand"] = brand
        if strong_password is not None:
            params["strongPassword"] = strong_password
        if keep_key_version is not None:
            params["keepKeyVersion"] = keep_key_version
        params = {k: v for k, v in params.items() if v is not None}
        headers = {
            "NEW_PASSWORD": new_password,
            "PASSWORD": old_password,
            "passcode": passcode,
        }
        headers = {k: v for k, v in headers.items() if v is not None}
        data = {}
        if old_password:
            data["oldPassword"] = old_password
        if new_password:
            data["newPassword"] = new_password
        result: Result = self.adapter.put(
            "/cloud/json/newPassword",
            ep_params=params if params else None,
            ep_headers=headers if headers else None,
            ep_json=data if data else None,
        )
        return result

    def recover_password(
        self,
        username: str = None,
        email: str = None,
        brand: str = None,
        app_name: str = None,
    ):
        """
        Initiate password recovery process.

        Sends a password reset link to the user's email.

        Args:
            username: Username or phone number
            email: Email address
            brand: Brand name for email customization
            app_name: Application name

        Returns:
            Result: API response confirming recovery email sent

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#recover-password
        """
        params = {
            "username": username,
            "email": email,
            "brand": brand,
            "appName": app_name,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.post(
            "/cloud/json/recoverPassword", ep_params=params
        )
        return result

    def reset_user_badges(
        self,
        user_id: int = None,
    ):
        """
        Reset user badges.

        Args:
            user_id: User ID (requires admin permissions if different from current user)

        Returns:
            Result: API response confirming badge reset

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#reset-user-badges
        """
        params = {
            "userId": user_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.put(
            "/cloud/json/userBadges", ep_params=params
        )
        return result

    def reset_badges(
        self,
        badge_type: int = None,
    ) -> Result:
        """
        Reset Badges.

        A badge is a red number that appears over an app's icon, indicating to the user that the app has something new to share.
        It is the app's responsibility to clear its own local badges, and to alert the server to reset the badge counter when the user finally responds.

        Badge types:
        - 1: Reset message badges
        - 2: Reset challenge badges
        - 3: Motion detection device alert
        - 6: Community

        Args:
            badge_type: Badge type to reset. If not provided, all badge counts will be reset.

        Returns:
            Result: API response confirming badge reset

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/User-Accounts/operation/Reset%20Badges
        """
        params = {}
        if badge_type is not None:
            params["type"] = badge_type
        result: Result = self.adapter.put(
            "/cloud/json/badges",
            ep_params=params if params else None,
        )
        return result

    def get_terms_of_service(
        self,
        signature_id: int = None,
    ):
        """
        Get terms of service.

        Args:
            signature_id: Optional signature ID to retrieve specific version

        Returns:
            Result: API response containing terms of service text and metadata

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#get-terms-of-service
        """
        params = {
            "signatureId": signature_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/cloud/json/termsOfServices", ep_params=params
        )
        return result

    def put_terms_of_service(
        self,
        signature_id: int,
    ):
        """
        Sign terms of service.

        Args:
            signature_id: Terms of service signature ID to accept

        Returns:
            Result: API response confirming acceptance

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#put-terms-of-service
        """
        result: Result = self.adapter.put(
            f"/cloud/json/termsOfServices/{signature_id}"
        )
        return result

    def put_user_tag(
        self,
        tag: str,
    ):
        """
        Apply a tag to the user account.

        Args:
            tag: Tag name to apply

        Returns:
            Result: API response confirming tag was applied

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#put-user-tag
        """
        result: Result = self.adapter.put(f"/cloud/json/usertags/{tag}")
        return result

    def delete_user_tag(
        self,
        tag: str,
    ):
        """
        Delete a tag from the user account.

        Args:
            tag: Tag name to remove

        Returns:
            Result: API response confirming tag was removed

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#delete-user-tag
        """
        result: Result = self.adapter.delete(f"/cloud/json/usertags/{tag}")
        return result

    def put_user_code(
        self,
        name: str,
        code: str = None,
        location_id: int = None,
        type: int = None,
        device_id: str = None,
        set_expiry: bool = None,
        verify: bool = None,
    ):
        """
        Create or update a user code.

        User codes are used for various purposes like device pairing, access codes, etc.

        Args:
            name: Code name/identifier
            code: The actual code value
            location_id: Optional location ID to associate with the code
            type: Code type identifier
            device_id: Optional device ID to associate with the code
            set_expiry: Whether to set an expiration time
            verify: Whether to verify the code immediately

        Returns:
            Result: API response with code creation/update result

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#put-user-code
        """
        params = {
            "name": name,
            "code": code,
            "locationId": location_id,
            "type": type,
            "deviceId": device_id,
            "setExpiry": set_expiry,
            "verify": verify,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.put(
            "/cloud/json/userCodes", ep_params=params
        )
        return result

    def get_user_codes(self):
        """
        Get all user codes for the current user.

        Returns:
            Result: API response containing list of user codes with their properties

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#get-user-codes
        """
        result: Result = self.adapter.get("/cloud/json/userCodes")
        return result

    def delete_user_code(
        self,
        name: str,
        location_id: int = None,
    ):
        """
        Delete a user code.

        Args:
            name: Code name to delete
            location_id: Optional location ID to scope the deletion

        Returns:
            Result: API response confirming code deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#delete-user-code
        """
        params = {
            "name": name,
            "locationId": location_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.delete(
            "/cloud/json/userCodes", ep_params=params
        )
        return result


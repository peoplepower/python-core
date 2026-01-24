# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "requests",
# ]
# ///

from typing import Dict

from ..api import API

from ...models import (
    APIKeyType,
    Result,
)


class Challenges(API):
    """
    Challenges API for managing organization challenges and participant operations.

    This class provides methods to create, retrieve, update, delete, and manage the status of challenges, as well as retrieve challenge participants.
    Supports filtering, template-based creation, and status management for community engagement challenges.

    Reference:
        https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Challenges
    """
    def create_challenge(
        self,
        organization_id: int,
        challenge_data: Dict,
        check: bool = None,
        parent_id: int = None,
    ) -> Result:
        """
        Create a challenge from scratch or from a template.

        In a community social network setting, an Engagement Manager may issue challenges
        to the community, to help achieve the overall goals of the community.

        Args:
            organization_id: Organization ID to create this challenge for
            challenge_data: Challenge data as JSON object with 'challenge' key
            check: True - Check if an active challenge already exists without creating one.
                   False - Do not check, just create it (default)
            parent_id: Challenge or template ID to copy settings from

        Returns:
            Result: API response with challengeId

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Challenges/operation/Create%20a%20Challenge
        """
        params = {
            "check": check,
            "parentId": parent_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.post(
            f"/espapi/admin/json/organizations/{organization_id}/challenges",
            ep_params=params,
            ep_json=challenge_data if challenge_data else None,
            ep_headers=self.adapter._get_headers(
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            ),
        )
        return result

    def get_challenges(
        self,
        organization_id: int,
        status: int = None,
        challenge_id: int = None,
        challenge_type: int = None,
        search_by: str = None,
        parent_id: int = None,
    ) -> Result:
        """
        View a list of challenges selected by their parameters.
        Only admins can see the templates in the search results.

        Args:
            organization_id: Organization ID to retrieve challenges for
            status: Optional status filter (0=Inactive, 1=Active, 2=Completed)
            challenge_id: Retrieve only this challenge
            challenge_type: Filter response by challenge types
            search_by: Search by name
            parent_id: Template ID to filter by

        Returns:
            Result: API response with challenges data

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Challenges/operation/Get%20Challenges
        """
        params = {
            "status": status,
            "challengeId": challenge_id,
            "challengeType": challenge_type,
            "searchBy": search_by,
            "parentId": parent_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            f"/espapi/admin/json/organizations/{organization_id}/challenges",
            ep_params=params,
            ep_headers=self.adapter._get_headers(
                {"API_KEY": self.adapter._headers.get("USER_KEY")}
            ),
        )
        return result

    def update_challenge(
        self,
        organization_id: int,
        challenge_id: int,
        challenge_data: Dict,
    ) -> Result:
        """
        Update a challenge.

        An administrator can modify all template fields except 'template' and 'challengeType'.

        Args:
            organization_id: Organization ID to update a challenge within
            challenge_id: Challenge ID to update
            challenge_data: Challenge data as JSON object with 'challenge' key

        Returns:
            Result: API response confirming update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Challenges/operation/Update%20a%20Challenge
        """
        result: Result = self.adapter.put(
            f"/espapi/admin/json/organizations/{organization_id}/challenges/{challenge_id}",
            ep_json=challenge_data if challenge_data else None,
            ep_headers=self.adapter._get_headers(
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            ),
        )
        return result

    def delete_challenge(
        self,
        organization_id: int,
        challenge_id: int,
    ) -> Result:
        """
        Delete a challenge.

        Args:
            organization_id: Organization ID
            challenge_id: Challenge ID to delete

        Returns:
            Result: API response confirming deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Challenges/operation/Delete%20a%20Challenge
        """
        result: Result = self.adapter.delete(
            f"/espapi/admin/json/organizations/{organization_id}/challenges/{challenge_id}",
            ep_headers=self.adapter._get_headers(
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            ),
        )
        return result

    def update_challenge_status(
        self,
        organization_id: int,
        challenge_id: int,
        status: int,
    ) -> Result:
        """
        Update challenge status.

        Args:
            organization_id: Organization ID to update
            challenge_id: Challenge ID to update
            status: New status (0=Inactive, 1=Active)

        Returns:
            Result: API response confirming status update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Challenges/operation/Update%20Challenge%20Status
        """
        result: Result = self.adapter.put(
            f"/espapi/admin/json/organizations/{organization_id}/challenges/{challenge_id}/status/{status}",
            ep_headers=self.adapter._get_headers(
                api_key=self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER
            ),
        )
        return result

    def get_challenge_participants(
        self,
        organization_id: int,
        challenge_id: int,
        status: int = None,
        location_id: int = None,
    ) -> Result:
        """
        Return invitational challenge participants.

        Only approved members of the given organization and the challenge participants
        can call this API.

        Participation statuses:
        - 1: Not responded
        - 2: Opt-In
        - 3: Opt-Out

        Args:
            organization_id: Organization ID
            challenge_id: Challenge ID to obtain winners for
            status: Participation status filter
            location_id: Filter the response by location ID

        Returns:
            Result: API response with participants data

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Challenges/operation/Get%20Participants
        """
        params = {
            "status": status,
            "locationId": location_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            f"/espapi/admin/json/organizations/{organization_id}/challenges/{challenge_id}/participants",
            ep_params=params,
            ep_headers=self.adapter._get_headers(
                {"API_KEY": self.adapter._headers.get("USER_KEY")}
            ),
        )
        return result

    def update_challenge_participant_status(
        self,
        organization_id: int,
        challenge_id: int,
        status: int,
        location_id: int,
    ) -> Result:
        """
        Update participation status to Opt-In or Opt-Out.

        Only approved members of the given organization and the challenge participants
        can update their participation status.

        Args:
            organization_id: Organization ID
            challenge_id: Challenge ID
            status: New participation status (2=Opt-In, 3=Opt-Out)
            location_id: Location ID

        Returns:
            Result: API response confirming status update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/admin.html#tag/Challenges/operation/Update%20Status
        """
        params = {
            "status": status,
            "locationId": location_id,
        }
        result: Result = self.adapter.put(
            f"/espapi/admin/json/organizations/{organization_id}/challenges/{challenge_id}/participants",
            ep_params=params,
            ep_headers=self.adapter._get_headers(
                {"API_KEY": self.adapter._headers.get("USER_KEY")}
            ),
        )
        return result

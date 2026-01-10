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
    Runtime,
)
from ..api import API


class DeveloperTeams(API):
    def create_team(self, team_name: str, description: str = None):
        """
        Create a new developer team.

        Args:
            team_name: Name of the team to create.
            description: Optional description of the team.

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Developer-Teams/operation/Create%20Team
        """
        data = {
            "name": team_name,
            "description": description,
        }
        data = {k: v for k, v in data.items() if v is not None}
        return self.adapter.post(
            "/espapi/cloud/developer/teams",
            ep_json=data,
        )

    def add_member(self, team_name: str, user_id: int = None, username: str = None, tester: bool = None):
        """
        Add a member to a developer team.

        Args:
            team_name: Name of the team to add the member to.
            user_id: Optional user ID of the member.
            username: Optional username of the member.
            tester: Optional flag to add as tester.

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Developer-Teams/operation/Add%20Member
        """
        params = {
            "teamName": team_name,
            "userId": user_id,
            "username": username,
            "tester": tester,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.post(
            "/espapi/cloud/developer/teams/members",
            ep_params=params,
        )

    def remove_member(self, team_name: str, user_id: int = None, username: str = None):
        """
        Remove a member from a developer team.

        Args:
            team_name: Name of the team to remove the member from.
            user_id: Optional user ID of the member.
            username: Optional username of the member.

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Developer-Teams/operation/Remove%20Member
        """
        params = {
            "teamName": team_name,
            "userId": user_id,
            "username": username,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.delete(
            "/espapi/cloud/developer/teams/members",
            ep_params=params,
        )

    def get_teams(self, team_name: str = None, user_id: int = None, bundle: str = None):
        """
        Get developer teams, optionally filtered by team name, user, or bundle.

        Args:
            team_name: Optional name of the team to filter.
            user_id: Optional user ID to filter teams by membership.
            bundle: Optional bot bundle identifier to filter teams.

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Developer-Teams/operation/Get%20Teams
        """
        params = {
            "teamName": team_name,
            "userId": user_id,
            "bundle": bundle,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.get(
            "/espapi/cloud/developer/teams",
            ep_params=params,
        )

    def add_developer_to_team(
        self,
        team_name: str,
        user_id: int = None,
        username: str = None,
        tester: bool = None,
    ):
        """
        Add a Developer.

        Any team member (except of testers) can add a new member of that team.
        System configuration administrators can add any user to any development team.

        Args:
            team_name: Existing developer team name (required)
            user_id: User ID to include to the team (either username or user ID is required)
            username: User to include to the team (either username or user ID is required)
            tester: Add beta-tester. Default is 'false' (developer).

        Returns:
            API response confirming addition

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Developer-Teams/operation/Add%20a%20Developer
        """
        params = {}
        if user_id is not None:
            params["userId"] = user_id
        if username is not None:
            params["username"] = username
        if tester is not None:
            params["tester"] = tester
        return self.adapter.post(
            f"/espapi/cloud/developer/teams/{team_name}",
            ep_params=params if params else None,
        )

    def remove_developer_from_team(
        self,
        team_name: str,
        user_id: int = None,
        username: str = None,
    ):
        """
        Remove a Developer.

        Any member (except of testers) of existing team can remove any other member of that team.
        System configuration administrators can remove any member of any team.

        Args:
            team_name: Existing developer team name (required)
            user_id: User ID to remove from the team (either username or user ID is required)
            username: User to remove from the team (either username or user ID is required)

        Returns:
            API response confirming removal

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Developer-Teams/operation/Remove%20a%20Developer
        """
        params = {}
        if user_id is not None:
            params["userId"] = user_id
        if username is not None:
            params["username"] = username
        return self.adapter.delete(
            f"/espapi/cloud/developer/teams/{team_name}",
            ep_params=params if params else None,
        )

    def get_team_secrets(self, team_name: str):
        """
        Get Developers Team Secret Names.

        List all existing secret names.

        Args:
            team_name: Developer team name (required)

        Returns:
            API response with list of secret names

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Developer-Teams/operation/Get%20Developers%20Team%20Secret%20Names
        """
        return self.adapter.get(
            f"/espapi/cloud/developer/teams/{team_name}/secrets",
        )

    def put_team_secret(
        self,
        team_name: str,
        secret_name: str,
        secret_value: str,
    ):
        """
        Put a Developers Team Secret.

        Create or update a developers team named secret value.
        The value will be stored encrypted and be available for team bot instances.

        Args:
            team_name: Developer team name (required)
            secret_name: Secret value name, maximum 50 characters (required)
            secret_value: Secret value to store (required)

        Returns:
            API response confirming secret creation/update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Developer-Teams/operation/Put%20a%20Developers%20Team%20Secret
        """
        params = {
            "secretName": secret_name,
        }
        data = {
            "secretValue": secret_value,
        }
        return self.adapter.put(
            f"/espapi/cloud/developer/teams/{team_name}/secrets",
            ep_params=params,
            ep_json=data,
        )

    def delete_team_secret(
        self,
        team_name: str,
        secret_name: str,
    ):
        """
        Delete a Developers Team Secret.

        Delete a developers team named secret value.

        Args:
            team_name: Developer team name (required)
            secret_name: Secret value name to delete (required)

        Returns:
            API response confirming secret deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Developer-Teams/operation/Delete%20a%20Developers%20Team%20Secret
        """
        params = {
            "secretName": secret_name,
        }
        return self.adapter.delete(
            f"/espapi/cloud/developer/teams/{team_name}/secrets",
            ep_params=params,
        )
# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "requests",
# ]
# ///

from typing import Dict, List

from ...models import Result
from ..api import API


class Rules(API):
    def get_conditions_and_actions(
        self,
        location_id: int,
        version: int = None,
    ) -> Result:
        """
        Get Rule Phrases.

        Get possible rule triggers, states, and actions.

        Args:
            location_id: Location ID (required)
            version: Rules implementation version

        Returns:
            Result: API response with triggers, states, and actions

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Rules-Engine/operation/Get%20Rule%20Phrases
        """
        params = {
            "locationId": location_id,
            "version": version,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/espapi/cloud/json/ruleConditions",
            ep_params=params,
        )
        return result

    def create_update_rule(
        self,
        rule_data: Dict,
        location_id: int = None,
        rule_id: int = None,
    ) -> Result:
        """
        Create or Update a Rule.

        When creating a rule, specify a single trigger, one or more states, and one or more actions.

        Args:
            rule_data: Rule data including trigger, states, and actions
            location_id: Location ID (required for create, required for update)
            rule_id: Rule ID to update (if provided, will update instead of create)

        Returns:
            Result: API response with created/updated rule

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Rules-Engine/operation/Create%20a%20Rule
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Rules-Engine/operation/Update%20a%20Rule
        """
        # Check if rule_data contains an ID to determine if it's an update
        if rule_id is None and isinstance(rule_data, dict):
            rule = rule_data.get("rule", {})
            if isinstance(rule, dict):
                rule_id = rule.get("id")

        if rule_id:
            # Update existing rule
            params = {
                "locationId": location_id,
            }
            params = {k: v for k, v in params.items() if v is not None}
            result: Result = self.adapter.put(
                f"/espapi/cloud/json/rules/{rule_id}",
                ep_params=params,
                ep_json=rule_data,
            )
        else:
            # Create new rule
            params = {
                "locationId": location_id,
            }
            params = {k: v for k, v in params.items() if v is not None}
            result: Result = self.adapter.post(
                "/espapi/cloud/json/rules",
                ep_params=params,
                ep_json=rule_data,
            )
        return result

    def get_rules(
        self,
        location_id: int,
        rule_id: str = None,
        device_id: str = None,
        details: bool = None,
    ) -> Result:
        """
        Get Rules.

        This API will allow you to filter the list of rules by criteria.

        Args:
            location_id: Location ID (required)
            rule_id: Only return this rule
            device_id: Only return rules for the given device ID
            details: Return details for this rule, including all the triggers, states, and actions

        Returns:
            Result: API response with list of rules

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Rules-Engine/operation/Get%20Rules
        """
        params = {
            "locationId": location_id,
            "ruleId": rule_id,
            "deviceId": device_id,
            "details": details,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/espapi/cloud/json/rules",
            ep_params=params,
        )
        return result

    def delete_rules(
        self,
        location_id: int,
        rule_ids: List[int] = None,
        status: int = None,
        device_type: int = None,
        device_id: str = None,
        default: bool = None,
        hidden: bool = None,
    ) -> Result:
        """
        Delete Rules by Criteria.

        Delete all rules matching to selection criteria.

        Args:
            location_id: Location ID (required)
            rule_ids: Rule ID's. Multiple values are supported.
            status: Rules status
            device_type: Delete rules containing devices of these types. Multiple values are supported.
            device_id: Delete rules containing these devices. Multiple values are supported.
            default: If set, delete only default or non-default rules.
            hidden: If set, delete only hidden or non-hidden rules.

        Returns:
            Result: API response confirming deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Rules-Engine/operation/Delete%20Rules%20by%20Criteria
        """
        params = {
            "locationId": location_id,
            "status": status,
            "deviceType": device_type,
            "deviceId": device_id,
            "default": default,
            "hidden": hidden,
        }
        # Handle multiple rule IDs - the API accepts multiple ruleId query parameters
        # We'll pass them as a list and let the adapter handle it
        if rule_ids:
            # For multiple rule IDs, we might need to pass them as comma-separated or multiple params
            # The adapter should handle list values appropriately
            params["ruleId"] = rule_ids
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.delete(
            "/espapi/cloud/json/rules",
            ep_params=params,
        )
        return result

    def update_rule_attrs(
        self,
        rule_id: int,
        attrs: Dict,
        location_id: int,
    ) -> Result:
        """
        Update Rule Attributes.

        Update the second name or status of the rule.

        Args:
            rule_id: Rule ID to update (required)
            attrs: Attributes to update (dict containing rule with name and/or status)
            location_id: Location ID (required)

        Returns:
            Result: API response with update result

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Rules-Engine/operation/Update%20a%20Rule%20Attribute
        """
        params = {
            "locationId": location_id,
        }
        result: Result = self.adapter.put(
            f"/espapi/cloud/json/rules/{rule_id}/attrs",
            ep_params=params,
            ep_json=attrs,
        )
        return result

    def delete_rule(
        self,
        rule_id: int,
        location_id: int,
    ) -> Result:
        """
        Delete a Rule.

        Delete a single rule by its ID.

        Args:
            rule_id: Rule ID to delete (required)
            location_id: Location ID (required)

        Returns:
            Result: API response confirming deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Rules-Engine/operation/Delete%20a%20Rule
        """
        params = {
            "locationId": location_id,
        }
        result: Result = self.adapter.delete(
            f"/espapi/cloud/json/rules/{rule_id}",
            ep_params=params,
        )
        return result

    def update_rules_status(
        self,
        status: int,
        location_id: int,
        rule_ids: List[int] = None,
        device_type: int = None,
        device_id: str = None,
        default: bool = None,
        hidden: bool = None,
    ) -> Result:
        """
        Update Rules Status.

        Update status of all rules matching to selection criteria.
        The API returns ID's of updated rules.

        Args:
            status: New rules status (required)
            location_id: Location ID (required)
            rule_ids: Rule ID's to update. Multiple values are supported.
            device_type: Update rules containing devices of these types. Multiple values are supported.
            device_id: Update rules containing these devices. Multiple values are supported.
            default: If set, update only default or non-default rules.
            hidden: If set, update only hidden or non-hidden rules.

        Returns:
            Result: API response with update result and list of updated rule IDs

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Rules-Engine/operation/Update%20Rules%20Status
        """
        params = {
            "locationId": location_id,
            "deviceType": device_type,
            "deviceId": device_id,
            "default": default,
            "hidden": hidden,
        }
        # Handle multiple rule IDs
        if rule_ids:
            params["ruleId"] = rule_ids
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.put(
            f"/espapi/cloud/json/rulesStatus/{status}",
            ep_params=params,
        )
        return result

    def create_default_rules(
        self,
        location_id: int,
        device_id: str = None,
    ) -> Result:
        """
        Create Default Rules for a Device.

        Creates all the default rules, if they do not already exist, for an individual device
        or for all the user's devices.

        Args:
            location_id: Location ID (required)
            device_id: Specific device ID to create default rules for (optional)

        Returns:
            Result: API response with creation result

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Rules-Engine/operation/Create%20Default%20Rules%20for%20a%20Device
        """
        params = {
            "locationId": location_id,
            "deviceId": device_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.post(
            "/espapi/cloud/json/rulesCreateDefault",
            ep_params=params,
        )
        return result

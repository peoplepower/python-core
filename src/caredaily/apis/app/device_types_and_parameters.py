# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "requests",
# ]
# ///

from typing import Dict, List, Optional

from ...models import Result
from ..api import API


class DeviceTypesAndParameters(API):
    """
    Device Types and Parameters API for managing device types, parameters, rules, goals, models, media, and stories.

    This class provides methods to manage device types, their attributes, parameters, default rules,
    device goals, models, media, and stories.

    Reference:
        https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Products-Management
    """

    def get_device_types(
        self,
        device_type: int = None,
        attribute_name: str = None,
        attribute_value: str = None,
        own: bool = None,
        simple: bool = None,
        organization_id: int = None,
    ) -> Result:
        """
        Get Device Types.

        Retrieve device types with optional filtering.

        Args:
            device_type: Filter by device type ID
            attribute_name: Filter by attribute name
            attribute_value: Filter by attribute value
            own: Filter by own device types
            simple: Return simplified device type information
            organization_id: Filter by organization ID

        Returns:
            Result: API response with device types list

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Products-Management
        """
        params = {
            "deviceType": device_type,
            "attributeName": attribute_name,
            "attributeValue": attribute_value,
            "own": own,
            "simple": simple,
            "organizationId": organization_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/cloud/json/deviceTypes",
            ep_params=params,
        )
        return result

    def get_device_type_attributes(
        self,
        device_type: int = None,
    ) -> Result:
        """
        Get Device Type Attributes.

        Each device type can have a set of attributes associated with it, to optimize its performance on the Care Daily AI Platform.
        This API will provide access to every supported attribute and attribute values.

        Args:
            device_type: Device type ID to filter attributes (optional)

        Returns:
            Result: API response with device type attributes

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Products-Management/operation/Get%20Device%20Type%20Attributes
        """
        params = {
            "deviceType": device_type,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/cloud/json/deviceTypeAttrs",
            ep_params=params,
        )
        return result

    def create_update_device_type(
        self,
        device_type_data: Dict,
    ) -> Result:
        """
        Create or Update Device Type.

        Each device type is created with a default name and a set of attributes to define the behavior of the device type.
        If the device type data contains an ID, it will update an existing device type.

        Args:
            device_type_data: Device type data including name and attributes

        Returns:
            Result: API response

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Products-Management/operation/Create%20Device%20Type
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Products-Management/operation/Update%20Device%20Type
        """
        # Check if device_type_data contains an ID to determine if it's an update
        device_type_id = None
        if isinstance(device_type_data, dict):
            device_type = device_type_data.get("deviceType", {})
            if isinstance(device_type, dict):
                device_type_id = device_type.get("id")

        if device_type_id:
            # Update existing device type
            result: Result = self.adapter.put(
                f"/cloud/json/deviceType/{device_type_id}",
                ep_json=device_type_data,
            )
        else:
            # Create new device type
            result: Result = self.adapter.post(
                "/cloud/json/deviceTypes",
                ep_json=device_type_data,
            )
        return result

    def create_device_type(
        self,
        device_type_data: Dict,
    ) -> Result:
        """
        Create Device Type.

        Each device type is created with a default name and a set of attributes to define the behavior of the device type.

        Args:
            device_type_data: Device type data as JSON object with 'deviceType' key containing:
                - name: Device type name
                - attr: List of attribute objects with 'name' and 'content'

        Returns:
            Result: API response with created device type

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Products-Management/operation/Create%20Device%20Type
        """
        result: Result = self.adapter.post(
            "/cloud/json/deviceType",
            ep_json=device_type_data,
        )
        return result

    def get_device_parameters(
        self,
        param_name: str = None,
    ) -> Result:
        """
        Get Device Parameters.

        A parameter is an individual stream of data between a device and the Care Daily AI Platform.
        The Care Daily AI Platform has a single namespace for parameters.
        Each parameter name must contain no spaces, and include a prefix that is separated
        from the rest of the name by a period ('.').

        Args:
            param_name: Get a specific parameter by name

        Returns:
            Result: API response with device parameters

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Products-Management/operation/Get%20Parameters
        """
        params = {
            "paramName": param_name,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/cloud/json/deviceParameters",
            ep_params=params,
        )
        return result

    def post_device_parameter(
        self,
        parameter_data: Dict,
    ) -> Result:
        """
        Create and Update a Parameter.

        A normal developer can update only their own parameters.
        A system administrator can edit any parameter.

        Args:
            parameter_data: Parameter data as JSON object with 'deviceParam' key

        Returns:
            Result: API response confirming parameter creation/update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Products-Management/operation/Create%20and%20Update%20a%20Parameter
        """
        result: Result = self.adapter.post(
            "/cloud/json/deviceParameters",
            ep_json=parameter_data if parameter_data else None,
        )
        return result

    def delete_device_parameter(
        self,
        parameter_name: str,
    ) -> Result:
        """
        Delete a Parameter.

        A normal developer can delete only their own parameters.
        A system administrator can delete any parameter.

        Args:
            parameter_name: Name of your parameter to delete

        Returns:
            Result: API response confirming deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Products-Management/operation/Delete%20a%20Parameter
        """
        result: Result = self.adapter.delete(
            f"/cloud/json/deviceParameters/{parameter_name}",
        )
        return result

    def put_device_parameter(
        self,
        parameter_name: str,
        parameter_data: Dict,
    ) -> Result:
        """
        Update a Parameter.

        A normal developer can update only their own parameters.
        A system administrator can edit any parameter.

        Args:
            parameter_name: Name of the parameter to update
            parameter_data: Parameter data as JSON object with 'deviceParam' key

        Returns:
            Result: API response confirming update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Products-Management
        """
        result: Result = self.adapter.put(
            f"/cloud/json/deviceParameters/{parameter_name}",
            ep_json=parameter_data if parameter_data else None,
        )
        return result

    def get_default_rules(
        self,
        device_type: int,
        details: bool = None,
    ) -> Result:
        """
        Get Device Type Default Rules.

        This API will allow you to get default rules by device type ID.
        You must be the owner of the device type in order to retrieve them.

        Args:
            device_type: The device type ID
            details: true - Return details for these rules, including all the triggers, states, and actions.
                    false - Only return the high level information about the rule, default

        Returns:
            Result: API response with default rules

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Products-Management/operation/Get%20Default%20Rules
        """
        params = {
            "details": details,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            f"/cloud/json/deviceType/{device_type}/rules",
            ep_params=params,
        )
        return result

    def add_default_rule(
        self,
        device_type: int,
        rule_id: int,
        hidden: bool = None,
    ) -> Result:
        """
        Add Default Rule.

        Assign a rule as default for a specific device type.
        When a user register a new device of this type, the system will automatically
        create a new rule based on this default rule.
        You must be the owner of the device type and the rule.
        The rule cannot be deleted after that.

        Args:
            device_type: The device type ID
            rule_id: The rule ID
            hidden: true - A new generated rule will be hidden and a user will not see it.
                   false - A user will see this rule in the list, default

        Returns:
            Result: API response confirming rule addition

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Products-Management/operation/Add%20Default%20Rule
        """
        params = {
            "hidden": hidden,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.post(
            f"/cloud/json/deviceType/{device_type}/rules/{rule_id}",
            ep_params=params,
        )
        return result

    def delete_default_rule(
        self,
        device_type: int,
        rule_id: int,
    ) -> Result:
        """
        Delete Default Rule.

        Delete an association of the default rule and the specific device type.
        You must be the owner of the device type and the rule.

        Args:
            device_type: The device type ID
            rule_id: The rule ID

        Returns:
            Result: API response confirming deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Products-Management/operation/Delete%20Default%20Rule
        """
        result: Result = self.adapter.delete(
            f"/cloud/json/deviceType/{device_type}/rules/{rule_id}",
        )
        return result

    def get_device_goals_by_types(
        self,
        type_ids: str = None,
        device_type: int = None,
        app_name: str = None,
    ) -> Result:
        """
        Get Device Goals by Type.

        Retrieve device goals by device type.
        Device goals provide possible device usage scenarios.
        Depending on chosen device goal the Care Daily AI Platform assign default rules
        and suggest device installation.

        Args:
            type_ids: Comma-separated list of device type IDs
            device_type: Single device type ID (alternative to typeIds)
            app_name: Specific app name

        Returns:
            Result: API response with device goals

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Products-Management/operation/Get%20Device%20Goals%20by%20Type
        """
        params = {
            "typeIds": type_ids,
            "appName": app_name,
        }
        params = {k: v for k, v in params.items() if v is not None}
        if device_type:
            result: Result = self.adapter.get(
                f"/cloud/json/deviceType/{device_type}/goals",
                ep_params=params,
            )
        else:
            result: Result = self.adapter.get(
                "/cloud/json/deviceGoals",
                ep_params=params,
            )
        return result

    def get_device_goal_installation_instruction(
        self,
        goal_id: int,
    ) -> Result:
        """
        Get Installation Instructions.

        Get device installation instructions by goal ID.

        Args:
            goal_id: The device goal ID

        Returns:
            Result: API response with installation instructions

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Products-Management/operation/Get%20Installation%20Instructions
        """
        result: Result = self.adapter.get(
            f"/cloud/json/goals/{goal_id}/installation",
        )
        return result

    def put_device_media(
        self,
        media_data: Dict,
    ) -> Result:
        """
        Put Device Media.

        Create or update device type media.

        Args:
            media_data: Media data as JSON object

        Returns:
            Result: API response confirming media update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Products-Management
        """
        result: Result = self.adapter.put(
            "/cloud/json/deviceMedia",
            ep_json=media_data if media_data else None,
        )
        return result

    def get_media(
        self,
        device_type: int = None,
        media_id: int = None,
    ) -> Result:
        """
        Get Media.

        Retrieve device type media.

        Args:
            device_type: Filter by device type ID
            media_id: Filter by specific media ID

        Returns:
            Result: API response with media list

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Products-Management
        """
        params = {
            "deviceType": device_type,
            "mediaId": media_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/cloud/json/deviceMedia",
            ep_params=params,
        )
        return result

    def get_available_media(
        self,
        media_id: str = None,
    ) -> Result:
        """
        Get Media.

        Get available medias.

        Media Types:
        - 1: video
        - 2: image
        - 3: audio
        - 6: text document

        Args:
            media_id: Search by ID

        Returns:
            Result: API response with available media list

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Products-Management/operation/Get%20Media
        """
        params = {}
        if media_id is not None:
            params["mediaId"] = media_id
        result: Result = self.adapter.get(
            "/cloud/json/media",
            ep_params=params if params else None,
        )
        return result

    def put_media(
        self,
        media_data: Dict,
    ) -> Result:
        """
        Put Media.

        Create or update media.

        Args:
            media_data: Media data as JSON object

        Returns:
            Result: API response confirming media update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Products-Management/operation/Put%20Media
        """
        result: Result = self.adapter.put(
            "/cloud/json/media",
            ep_json=media_data if media_data else None,
        )
        return result

    def delete_media_collection(
        self,
        media_ids: Optional[List[int]] = None,
    ) -> Result:
        """
        Delete Media.

        Delete media at the collection level.

        Args:
            media_ids: List of media IDs to delete (optional, if not provided deletes all)

        Returns:
            Result: API response confirming deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Products-Management/operation/Delete%20Media
        """
        params = {}
        if media_ids is not None:
            params["mediaId"] = media_ids
        result: Result = self.adapter.delete(
            "/cloud/json/media",
            ep_params=params if params else None,
        )
        return result

    def delete_media(
        self,
        media_id: int,
    ) -> Result:
        """
        Delete Media.

        Delete device type media.

        Args:
            media_id: Media ID to delete

        Returns:
            Result: API response confirming deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Products-Management
        """
        result: Result = self.adapter.delete(
            f"/cloud/json/deviceMedia/{media_id}",
        )
        return result

    def put_device_models(
        self,
        models_data: Dict,
    ) -> Result:
        """
        Put Device Models.

        Create or update device models.

        Args:
            models_data: Device models data as JSON object

        Returns:
            Result: API response confirming models update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Products-Management
        """
        result: Result = self.adapter.put(
            "/cloud/json/deviceModels",
            ep_json=models_data if models_data else None,
        )
        return result

    def get_device_models(
        self,
        device_type: int = None,
        model_id: str = None,
    ) -> Result:
        """
        Get Device Models.

        Retrieve device models.

        Args:
            device_type: Filter by device type ID
            model_id: Filter by specific model ID

        Returns:
            Result: API response with device models list

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Products-Management
        """
        params = {
            "deviceType": device_type,
            "modelId": model_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/cloud/json/deviceModels",
            ep_params=params,
        )
        return result

    def delete_device_model_data(
        self,
        model_id: str,
    ) -> Result:
        """
        Delete Device Model Data.

        Delete a device model.

        Args:
            model_id: Model ID to delete

        Returns:
            Result: API response confirming deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Products-Management
        """
        result: Result = self.adapter.delete(
            f"/cloud/json/deviceModels/{model_id}",
        )
        return result

    def delete_device_model(
        self,
        model_id: str,
    ) -> Result:
        """
        Delete Device Model.

        Delete a device model by ID.

        Args:
            model_id: Model ID to delete (required)

        Returns:
            Result: API response confirming deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Products-Management/operation/Delete%20Device%20Model
        """
        params = {
            "modelId": model_id,
        }
        result: Result = self.adapter.delete(
            "/cloud/json/devicemodels",
            ep_params=params,
        )
        return result

    def get_stories(
        self,
        device_type: int = None,
        story_id: int = None,
    ) -> Result:
        """
        Get Stories.

        Retrieve device type stories.

        Args:
            device_type: Filter by device type ID
            story_id: Filter by specific story ID

        Returns:
            Result: API response with stories list

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Products-Management
        """
        params = {
            "deviceType": device_type,
            "storyId": story_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/cloud/json/deviceStories",
            ep_params=params,
        )
        return result

    def get_stories_collection(
        self,
        story_type: int = None,
        lang: str = None,
    ) -> Result:
        """
        Get Stories.

        Retrieve stories from the stories collection.

        Args:
            story_type: Filter by story type
            lang: Filter by language

        Returns:
            Result: API response with stories list

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Products-Management/operation/Get%20Stories
        """
        params = {}
        if story_type is not None:
            params["storyType"] = story_type
        if lang is not None:
            params["lang"] = lang
        result: Result = self.adapter.get(
            "/cloud/json/stories",
            ep_params=params if params else None,
        )
        return result

    def put_stories_collection(
        self,
        stories_data: Dict,
    ) -> Result:
        """
        Put Stories.

        Insert new stories or update existing stories in the stories collection.

        Args:
            stories_data: Stories data as JSON object with 'stories' array

        Returns:
            Result: API response confirming stories update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Products-Management/operation/Put%20Stories
        """
        result: Result = self.adapter.put(
            "/cloud/json/stories",
            ep_json=stories_data if stories_data else None,
        )
        return result

    def delete_stories_collection(
        self,
        story_ids: Optional[List[int]] = None,
    ) -> Result:
        """
        Delete Stories.

        Delete stories from the stories collection.

        Args:
            story_ids: List of story IDs to delete (optional, if not provided deletes all)

        Returns:
            Result: API response confirming deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Products-Management/operation/Delete%20Stories
        """
        params = {}
        if story_ids is not None:
            params["storyId"] = story_ids
        result: Result = self.adapter.delete(
            "/cloud/json/stories",
            ep_params=params if params else None,
        )
        return result

    def put_stories(
        self,
        stories_data: Dict,
    ) -> Result:
        """
        Put Stories.

        Create or update device type stories.

        Args:
            stories_data: Stories data as JSON object

        Returns:
            Result: API response confirming stories update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Products-Management
        """
        result: Result = self.adapter.put(
            "/cloud/json/deviceStories",
            ep_json=stories_data if stories_data else None,
        )
        return result

    def delete_story(
        self,
        story_id: int,
    ) -> Result:
        """
        Delete Story.

        Delete a device type story.

        Args:
            story_id: Story ID to delete

        Returns:
            Result: API response confirming deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Products-Management
        """
        result: Result = self.adapter.delete(
            f"/cloud/json/deviceStories/{story_id}",
        )
        return result

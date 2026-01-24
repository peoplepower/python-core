# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "requests",
# ]
# ///

import json
from typing import Dict, List


from ..api import API

# TODO: Finish (see docs/api/bots.yaml)
class BotDeveloper(API):
    """
    BotDeveloper API for managing bot applications, versions, code uploads, statistics, and execution logs.

    This class provides methods to create, update, and retrieve bot apps and versions, upload code and objects, manage parameters and status, set message topics, and access execution and logging information for bots.

    Reference:
        https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Development
    """
    def create_update_bot(
        self,
        bundle: str,
        data: Dict,
        developer_team: str = None,
    ):
        """
        Create or update a bot application.

        Args:
            bundle: Bot bundle identifier
            data: Bot application data as a dictionary
            developer_team: Optional developer team name

        Returns:
            API response with bot application details

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Development/operation/Create%20or%20Update%20Bot
        """
        params = {"bundle": bundle, "developerTeam": developer_team}
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.put(
            "/espapi/cloud/developer/apps",
            ep_json=data,
            ep_params=params,
        )

    def create_update_bot_version(
        self,
        bundle: str,
        status: int = None,
        version: str = None,
        data: Dict = None,
    ):
        """
        Create or update a bot application version.

        Args:
            bundle: Bot bundle identifier
            status: Optional status code
            version: Optional version string
            data: Bot version data as a dictionary

        Returns:
            API response with bot version details

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Development/operation/Update%20the%20Latest%20Version
        """
        params = {"bundle": bundle, "status": status, "version": version}
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.put(
            "/espapi/cloud/developer/versions",
            ep_json=data,
            ep_params=params,
        )

    def upload_bot_code(
        self,
        data,
        content_type: str,
        bundle: str = None,
        runtime: int = None,
        source: bool = True,
        a_sync: bool = True,
        memory: int = None,
        timeout: int = None,
    ):
        """
        Upload bot code package for a bot application.

        Args:
            data: Code file data (bytes or file-like)
            content_type: MIME type of the code file
            bundle: Optional bot bundle identifier
            runtime: Optional runtime environment identifier
            source: Whether this is source code (default True)
            a_sync: Whether to upload asynchronously (default True)
            memory: Optional memory allocation
            timeout: Optional timeout in seconds

        Returns:
            API response with upload status or request ID

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Development/operation/Upload%20Bot%20Code
        """
        params = {
            "bundle": bundle,
            "runtime": runtime,
            "source": source,
            "async": a_sync,
            "memory": memory,
            "timeout": timeout,
        }
        params = {k: v for k, v in params.items() if v is not None}
        headers = {"Content-Type": content_type}
        return self.adapter.post(
            "/espapi/cloud/developer/upload",
            ep_data=data,
            ep_params=params,
            ep_headers=headers,
        )

    def get_upload_bot_code_result(
        self,
        request_id: str,
    ):
        """
        Get the result of a bot code upload operation by request ID.

        Args:
            request_id: Upload request identifier

        Returns:
            API response with upload result

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Development/operation/Get%20Code%20Upload%20Result
        """
        return self.adapter.get(
            f"/espapi/cloud/developer/upload/{request_id}",
        )

    def update_bot_parameters(
        self,
        bundle: str,
        memory: int,
        timeout: int,
        development: bool = None,
    ):
        """
        Update bot application parameters such as memory and timeout.

        Args:
            bundle: Bot bundle identifier
            memory: Memory allocation
            timeout: Timeout in seconds
            development: Optional development mode flag

        Returns:
            API response confirming parameter update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Development/operation/Update%20Bot%20Parameters

        @deprecated: Remove
        """
        params = {
            "memory": memory,
            "timeout": timeout,
            "development": development,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.put(
            "/espapi/cloud/developer/botParams/{}".format(bundle),
            ep_params=params,
        )

    def set_bot_version_status(
        self,
        bundle: str,
        status: int,
    ):
        """
        Set the status of a bot application version.

        Args:
            bundle: Bot bundle identifier
            status: Status code to set

        Returns:
            API response confirming status update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Development/operation/Update%20Version%20Status
        """
        params = {"bundle": bundle, "status": status}
        return self.adapter.put(
            "/espapi/cloud/developer/versionStatus",
            ep_params=params,
        )

    def get_bots(
        self,
        bundle: str = None
    ):
        """
        Retrieve a list of bot applications or a specific bot by bundle.

        Args:
            bundle: Optional bot bundle identifier

        Returns:
            API response with bot application(s) details

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Development/operation/Get%20Developer%20Bots
        """
        params = {"bundle": bundle}
        params = {k: v for k, v in params.items() if v is not None}
        headers = self.adapter._get_headers()
        print("Headers:", headers)
        return self.adapter.get("/espapi/cloud/developer/apps", ep_params=params)

    def get_bot_versions(
        self,
        bundle: str,
        statuses: List[str] = None,
        version: str = None,
    ):
        """
        Retrieve versions of a bot application.

        Args:
            bundle: Bot bundle identifier
            statuses: Optional list of status strings
            version: Optional version string

        Returns:
            API response with bot version(s) details

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Development/operation/Get%20Bot%20Versions
        """
        params = {"bundle": bundle, "status": statuses, "version": version}
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.get("/espapi/cloud/developer/versions", ep_params=params)

    def delete_bot_versions(
        self,
        bundle: str,
    ):
        """
        Delete Bot Versions.

        Archive active bot versions, delete bot instances.

        Args:
            bundle: Bot bundle ID (required)

        Returns:
            API response confirming deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Development/operation/Delete%20Bot%20Versions
        """
        params = {"bundle": bundle}
        return self.adapter.delete(
            "/espapi/cloud/developer/versions",
            ep_params=params,
        )

    def get_bot_statistics(
        self,
        bundle: str,
    ):
        """
        Retrieve statistics for a bot application.

        Args:
            bundle: Bot bundle identifier

        Returns:
            API response with bot statistics

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Execution-Statistics-and-Logs/operation/Get%20Bot%20Statistics
        """
        params = {"bundle": bundle}
        return self.adapter.get(
            "/espapi/cloud/developer/stats",
            ep_params=params,
        )

    def upload_bot_object(
        self,
        name: str,
        bundle: str,
        data,
        content_type: str = "image/png",
    ):
        """
        Upload an object (e.g., image) for a bot application.

        Each bot can contain a publicly available icon and/or other images.
        These will be displayed in the Bot Shop.

        For all images and icons, the PNG format is recommended. You should avoid using interlaced PNGs.
        The standard bit depth for icons and images is 24 bits.
        The standard size for icons is 1024 x 1024 px.

        Args:
            name: Object name. Use "icon" for icons (required)
            bundle: Globally unique bundle ID for the bot, i.e. ai.caredaily.MyBot (required)
            data: Object data (bytes or file-like) - binary image data
            content_type: MIME type of the object (default 'image/png')

        Returns:
            API response with upload status

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Development/operation/Upload%20Bot%20Object
        """
        params = {"bundle": bundle}
        headers = {"Content-Type": content_type}
        return self.adapter.put(
            f"/espapi/cloud/developer/objects/{name}",
            ep_data=data,
            ep_params=params,
            ep_headers=headers,
        )

    def set_message_topics(
        self,
        bundle: str,
        topics: Dict,
    ):
        """
        Set message topics for a bot application.

        Args:
            bundle: Bot bundle identifier
            topics: Dictionary of message topics

        Returns:
            API response confirming topics update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Development/operation/Update%20Message%20Topics
        """
        params = {"bundle": bundle}
        return self.adapter.put(
            "/espapi/cloud/developer/messageTopics",
            ep_json=json.dumps(topics),
            ep_params=params,
        )

    def get_execution_history(
        self,
        start_date_ms: int,
        end_date_ms: int,
        bundle: str = None,
        developer: bool = None,
        app_instance_id: int = None,
        flow: int = None,
        trigger: int = None,
        errors_only: bool = None,
        row_count: int = None,
        sort_order: str = None,
    ):
        """
        Retrieve execution history for bot applications or instances.

        Args:
            start_date_ms: Start date in milliseconds since epoch
            end_date_ms: End date in milliseconds since epoch
            bundle: Optional bot bundle identifier
            developer: Optional developer mode flag
            app_instance_id: Optional application instance ID
            flow: Optional flow identifier
            trigger: Optional trigger identifier
            errors_only: Optional flag to filter errors only
            row_count: Optional number of rows to return
            sort_order: Optional sort order

        Returns:
            API response with execution history

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Development/operation/Get%20Execution%20History
        """
        params = {
            "startDate": start_date_ms,
            "endDate": end_date_ms,
            "bundle": bundle,
            "developer": developer,
            "appInstanceId": app_instance_id,
            "flow": flow,
            "trigger": trigger,
            "errorsOnly": errors_only,
            "rowCount": row_count,
            "sortOrder": sort_order,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.get(
            "/espapi/cloud/developer/executionHistory",
            ep_params=params,
        )

    def get_execution_info(
        self,
        app_instance_id: int,
        flow: int,
        request_date_ms: int,
    ):
        """
        Retrieve detailed execution information for a specific bot instance execution.

        Args:
            app_instance_id: Application instance ID
            flow: Flow identifier
            request_date_ms: Request date in milliseconds since epoch

        Returns:
            API response with execution information

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Execution-Statistics-and-Logs/operation/Get%20Execution%20Info
        """
        params = {
            "appInstanceId": app_instance_id,
            "flow": flow,
            "requestDate": request_date_ms,
        }
        return self.adapter.get(
            "/espapi/cloud/developer/executionInfo",
            ep_params=params,
        )

    def manage_bot_instance_logging(
        self,
        app_instance_id: int,
        flow: int,
        status: int,
        end_date_ms: int = None,
    ):
        """
        Enable, disable, or update logging for a bot instance.

        Args:
            app_instance_id: Application instance ID
            flow: Flow identifier
            status: Logging status code
            end_date_ms: Optional end date in milliseconds since epoch

        Returns:
            API response confirming logging status update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Execution-Statistics-and-Logs/operation/Enable/Disable%20CloudWatch%20Logging
        """
        params = {
            "appInstanceId": app_instance_id,
            "flow": flow,
            "status": status,
            "endDate": end_date_ms,  # TODO:  ISO 8601
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.put(
            "/espapi/cloud/developer/cloudwatchlog",
            ep_params=params,
        )

    def describe_bot_instance_logging(
        self,
        app_instance_id: int,
        flow: int,
    ):
        """
        Retrieve logging configuration for a bot instance.

        Args:
            app_instance_id: Application instance ID
            flow: Flow identifier

        Returns:
            API response with logging configuration

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Execution-Statistics-and-Logs/operation/Get%20CloudWatch%20Log%20Info
        """
        params = {"appInstanceId": app_instance_id, "flow": flow}
        return self.adapter.get(
            "/espapi/cloud/developer/cloudwatchlog",
            ep_params=params,
        )

    def export_bot_instance_log(
        self,
        app_instance_id: int,
        flow: int,
        start_date_ms: int,
        end_date_ms: int = None,
    ):
        """
        Export logs for a bot instance within a date range.

        Args:
            app_instance_id: Application instance ID
            flow: Flow identifier
            start_date_ms: Start date in milliseconds since epoch
            end_date_ms: Optional end date in milliseconds since epoch

        Returns:
            API response with export task information

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Execution-Statistics-and-Logs/operation/Create%20an%20export%20task
        """
        params = {
            "appInstanceId": app_instance_id,
            "flow": flow,
            "startDate": start_date_ms,
            "endDate": end_date_ms,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.post(
            "/espapi/cloud/developer/cloudwatchlog/export",
            ep_params=params,
        )

    def get_exported_bot_instance_log(
        self,
        task_id: str,
    ):
        """
        Retrieve exported logs for a bot instance by task ID.

        Args:
            task_id: Export task identifier

        Returns:
            API response with exported log data

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Execution-Statistics-and-Logs/operation/Get%20Export%20Status
        """
        params = {"taskId": task_id}
        return self.adapter.get(
            "/espapi/cloud/developer/cloudwatchlog/export",
            ep_params=params,
        )

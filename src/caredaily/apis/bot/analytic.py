# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "requests",
# ]
# ///

from typing import Dict, List, Optional

from ..api import API

from ...models import (
    Result,
)


class Analytic(API):
    """
    Analytic API for bot server operations and bot management.

    This class provides methods for bot execution, variables management, data requests,
    and other bot server operations. These are bot-level APIs that operate on bot instances,
    distinct from location-level APIs.

    Reference:
        https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Server-APIs
    """

    def get_app_key(
        self,
        app_instance_id: int,
    ) -> Result:
        """
        Get Bot Key.

        For authentication all bot API's require an API key generated specifically for running the bot.
        Each bot will receive the key inside the input parameter.

        However, it can be useful to call bot APIs manually.
        This API allows to obtain analytic API key using existing user API key for limited time.

        Args:
            app_instance_id: Bot instance ID (required)

        Returns:
            Result: API response with bot key and expiry

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Server-APIs/operation/Get%20Bot%20Key
        """
        params = {
            "appInstanceId": app_instance_id,
        }
        result: Result = self.adapter.get(
            "/espapi/analytic/appkey",
            ep_params=params,
        )
        return result

    def start_execution(
        self,
        start_key: int,
        aws_request_id: Optional[str] = None,
        log_stream_name: Optional[str] = None,
    ) -> Result:
        """
        Start Execution.

        Bots must always notify the server about they have started running.
        This is necessary in order to avoid parallel execution of the same bot instance.

        Args:
            start_key: Unique identifier of the launch (required)
            aws_request_id: The property 'aws_request_id' of the context object
            log_stream_name: The property 'log_stream_name' of the context object

        Returns:
            Result: API response with execution start result

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Server-APIs/operation/Start%20Execution
        """
        params = {
            "startKey": start_key,
        }
        if aws_request_id is not None:
            params["awsRequestId"] = aws_request_id
        if log_stream_name is not None:
            params["logStreamName"] = log_stream_name
        result: Result = self.adapter.post(
            "/espapi/analytic/start",
            ep_params=params,
        )
        return result

    def request_execution(
        self,
        in_seconds: Optional[int] = None,
        at_timestamp: Optional[int] = None,
    ) -> Result:
        """
        Request Execution.

        Bots can request to execute themselves again in N seconds, without external triggers.
        In the BotEngine, this is transformed into a Timer system that multiplexes this single timer.

        Args:
            in_seconds: Execute in N seconds
            at_timestamp: Execute at a unix timestamp in milliseconds

        Returns:
            Result: API response with scheduled execution time

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Server-APIs/operation/Request%20Execution
        """
        params = {}
        if in_seconds is not None:
            params["in"] = in_seconds
        if at_timestamp is not None:
            params["at"] = at_timestamp
        result: Result = self.adapter.put(
            "/espapi/analytic/execute",
            ep_params=params if params else None,
        )
        return result

    def cancel_execution(
        self,
    ) -> Result:
        """
        Cancel Execution.

        Cancel the scheduled one-time execution.

        Returns:
            Result: API response confirming cancellation

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Server-APIs/operation/Cancel%20Execution
        """
        result: Result = self.adapter.delete(
            "/espapi/analytic/execute",
        )
        return result

    def get_secret(
        self,
        secret_name: str,
    ) -> Result:
        """
        Get Secret Value.

        A bot instance can request a secret value defined by the developers team.

        Args:
            secret_name: Secret value name (required)

        Returns:
            Result: API response with secret value

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Server-APIs/operation/Get%20Secret%20Value
        """
        params = {
            "secretName": secret_name,
        }
        result: Result = self.adapter.get(
            "/espapi/analytic/secrets",
            ep_params=params,
        )
        return result

    def get_variable(
        self,
        name: str,
        shared: Optional[bool] = None,
    ) -> Result:
        """
        Get a Variable.

        Variables are to an instance of a bot, as user properties are to an instance of a user.
        Variables could have binary values up to 16M.

        Args:
            name: Name of the variable to return (required)
            shared: Shared variable

        Returns:
            Result: API response with variable value (or 204 if variable doesn't exist)

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Server-APIs/operation/Get%20a%20Variable
        """
        params = {}
        if shared is not None:
            params["shared"] = shared
        result: Result = self.adapter.get(
            f"/espapi/analytic/variables/{name}",
            ep_params=params if params else None,
        )
        return result

    def save_variable(
        self,
        name: str,
        value: bytes,
        content_md5: Optional[str] = None,
        shared: Optional[bool] = None,
    ) -> Result:
        """
        Save a Variable.

        The API saves the value of specified variable.
        If the variable doesn't yet exist it will be created.
        If the value to save is empty then this variable will be removed.

        Args:
            name: Name of the variable to save (required)
            value: Variable value as bytes
            content_md5: MD5 digest of the variable value in hex format
            shared: Shared variable

        Returns:
            Result: API response confirming save

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Server-APIs/operation/Save%20a%20Variable
        """
        params = {}
        if shared is not None:
            params["shared"] = shared
        headers = {}
        if content_md5 is not None:
            headers["Content-MD5"] = content_md5
        result: Result = self.adapter.post(
            f"/espapi/analytic/variables/{name}",
            ep_params=params if params else None,
            ep_data=value,
            ep_headers=headers if headers else None,
        )
        return result

    def delete_variable(
        self,
        name: str,
        shared: Optional[bool] = None,
    ) -> Result:
        """
        Delete a Variable.

        The API deletes the specified variable, if any.

        Args:
            name: Name of the variable to delete (required)
            shared: Shared variable

        Returns:
            Result: API response confirming deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Server-APIs/operation/Delete%20a%20Variable
        """
        params = {}
        if shared is not None:
            params["shared"] = shared
        result: Result = self.adapter.delete(
            f"/espapi/analytic/variables/{name}",
            ep_params=params if params else None,
        )
        return result

    def save_variables(
        self,
        names: List[str],
        lengths: List[int],
        values: bytes,
        content_md5: Optional[str] = None,
    ) -> Result:
        """
        Save Variables.

        This API allows to put multiple variables in one API call.
        The API saves values of specified variables concatenated in the request body.

        Args:
            names: Names of variables to save (required)
            lengths: Lengths of variable values (required)
            values: Concatenated variable values as bytes
            content_md5: MD5 digest of the variables content in hex format

        Returns:
            Result: API response confirming save

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Server-APIs/operation/Save%20Variables
        """
        params = {
            "name": names,
            "length": lengths,
        }
        headers = {}
        if content_md5 is not None:
            headers["Content-MD5"] = content_md5
        result: Result = self.adapter.post(
            "/espapi/analytic/variables",
            ep_params=params,
            ep_data=values,
            ep_headers=headers if headers else None,
        )
        return result

    def send_data_message(
        self,
        address: str,
        scope: int,
        stream_data: Dict,
    ) -> Result:
        """
        Send Data Message.

        A bot can send a message to other bots.
        The message can be sent to bots subscribed on the specific data stream address.

        Args:
            address: Data stream address (required)
            scope: Bitmask to feed location and/or organization bots (1=location, 2=organization)
            stream_data: Stream data containing:
                - locations: List of location IDs to send message to
                - bots: List of bot instance IDs to send message to
                - feed: Flexible data structure message

        Returns:
            Result: API response confirming message sent

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Server-APIs/operation/Send%20Data%20Message
        """
        params = {
            "address": address,
            "scope": scope,
        }
        result: Result = self.adapter.post(
            "/espapi/analytic/stream",
            ep_params=params,
            ep_json=stream_data,
        )
        return result

    def submit_data_request(
        self,
        data_requests: List[Dict],
    ) -> Result:
        """
        Submit Data Request.

        Selecting large amount of data from the database can take significant time.
        To avoid this long waiting period a bot can submit requests for all data to the server asynchronously.

        Args:
            data_requests: List of data request objects, each containing:
                - type: Data type (1=Device parameters, 2=Device activities, etc.)
                - key: Optional request key
                - deviceId: Device ID (required for types 1,2,8,9)
                - startTime: Period start time in milliseconds
                - endTime: Period end time in milliseconds
                - paramNames: Device parameter names (optional for type 1)
                - index: Device part index (optional for type 1)
                - organizationId: Organization ID (required for types 3,6)
                - ordered: Order data by timestamp (optional)
                - compression: Data compression type (optional)

        Returns:
            Result: API response with data request submission result

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Server-APIs/operation/Submit%20Data%20Request
        """
        data = {
            "dataRequests": data_requests,
        }
        result: Result = self.adapter.post(
            "/espapi/analytic/dataRequests",
            ep_json=data,
        )
        return result

    def get_location_events(
        self,
        location_id: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Result:
        """
        Location Scenes History.

        Return location change schemes history in backward order (latest first).

        Args:
            location_id: The Location ID for which to trigger an event (required)
            start_date: Start date to begin receiving data
            end_date: End date to stop receiving data

        Returns:
            Result: API response with location events history

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Location-APIs/operation/Location%20Scenes%20History
        """
        params = {}
        if start_date is not None:
            params["startDate"] = start_date
        if end_date is not None:
            params["endDate"] = end_date
        result: Result = self.adapter.get(
            f"/espapi/analytic/location/{location_id}/events",
            ep_params=params if params else None,
        )
        return result

    def get_call_center(
        self,
    ) -> Result:
        """
        Get Call Center.

        A bot can check the current call center service status and send an alert, if the service is available.

        Returns:
            Result: API response with call center status and alert information

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Professional-Monitoring-APIs/operation/Get%20Call%20Center
        """
        result: Result = self.adapter.get(
            "/espapi/analytic/callCenter",
        )
        return result

    def update_call_center(
        self,
        call_center_data: Dict,
    ) -> Result:
        """
        Update Call Center.

        Update call center alert status. The API can raise an alert by setting the alert status.

        Args:
            call_center_data: Call center data containing:
                - alertStatus: To raise an alert set it to 1 (raised)

        Returns:
            Result: API response confirming update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Professional-Monitoring-APIs/operation/Update%20Call%20Center
        """
        result: Result = self.adapter.put(
            "/espapi/analytic/callCenter",
            ep_json=call_center_data,
        )
        return result

    def get_call_center_alerts(
        self,
    ) -> Result:
        """
        Get Call Center Alerts.

        Retrieve history of call center alerts.

        Returns:
            Result: API response with call center alerts history

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Professional-Monitoring-APIs/operation/Get%20Call%20Center%20Alerts
        """
        result: Result = self.adapter.get(
            "/espapi/analytic/callCenterAlerts",
        )
        return result

    def ask_questions(
        self,
        questions: List[Dict],
    ) -> Result:
        """
        Ask Questions.

        Create questions for users to answer.

        Args:
            questions: List of question objects, each containing:
                - key: Unique key for the bot to reference this question
                - collectionName: Collection name
                - description: Question description
                - editable: Whether the question is editable
                - question: Multilingual question text map
                - placeholder: Multilingual placeholder text map
                - deviceId: Optional device ID
                - icon: Optional icon name
                - iconFont: Icon font
                - displayType: Display type
                - defaultAnswer: Default answer value
                - answerFormat: Answer format regex
                - slider: Slider configuration object
                - sectionTitle: Multilingual section title map
                - sectionId: Section ID
                - questionWeight: Question weight
                - responseType: Response type
                - responseOptions: List of response option objects

        Returns:
            Result: API response with created questions

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Question-APIs/operation/Ask%20Questions
        """
        data = {
            "questions": questions,
        }
        result: Result = self.adapter.post(
            "/espapi/analytic/questions",
            ep_json=data,
        )
        return result

    def get_question_responses(
        self,
        key: Optional[str] = None,
        collection_name: Optional[str] = None,
        status: Optional[int] = None,
    ) -> Result:
        """
        Get Question Responses.

        Retrieve question responses. Questions that have a timestamp have been explicitly answered by the user.

        Args:
            key: Question key filter
            collection_name: Collection name filter
            status: Answer status filter (multiple values supported)

        Returns:
            Result: API response with question responses and collections

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Question-APIs/operation/Get%20Question%20Responses
        """
        params = {}
        if key is not None:
            params["key"] = key
        if collection_name is not None:
            params["collectionName"] = collection_name
        if status is not None:
            params["status"] = status
        result: Result = self.adapter.get(
            "/espapi/analytic/questions",
            ep_params=params if params else None,
        )
        return result

    def update_question_response(
        self,
        question_id: int,
        answer: Optional[str] = None,
        editable: Optional[bool] = None,
    ) -> Result:
        """
        Update Response.

        Updates the answer and/or the 'editable' flag of the question.

        Args:
            question_id: Question ID to update (required)
            answer: New answer value
            editable: Whether the question is editable

        Returns:
            Result: API response confirming update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Question-APIs/operation/Update%20Response
        """
        params = {
            "questionId": question_id,
        }
        data = {}
        if answer is not None:
            data["answer"] = answer
        if editable is not None:
            data["editable"] = editable
        result: Result = self.adapter.put(
            "/espapi/analytic/questions",
            ep_params=params,
            ep_json=data if data else None,
        )
        return result

    def delete_questions(
        self,
        question_id: int,
    ) -> Result:
        """
        Delete Questions.

        Delete questions by ID. Multiple question IDs are supported.

        Args:
            question_id: Question ID to delete (multiple values supported)

        Returns:
            Result: API response confirming deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Question-APIs/operation/Delete%20Questions
        """
        params = {
            "questionId": question_id,
        }
        result: Result = self.adapter.delete(
            "/espapi/analytic/questions",
            ep_params=params,
        )
        return result

    def get_question_collections(
        self,
        name: Optional[str] = None,
    ) -> Result:
        """
        Get Question Collections.

        Return all or specified question collections.

        Args:
            name: Collection name filter

        Returns:
            Result: API response with question collections

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Question-APIs/operation/Get%20Question%20Collections
        """
        params = {}
        if name is not None:
            params["name"] = name
        result: Result = self.adapter.get(
            "/espapi/analytic/questions/collections",
            ep_params=params if params else None,
        )
        return result

    def set_question_collection(
        self,
        collection: Dict,
    ) -> Result:
        """
        Set Questions Collection.

        Create a new or update an existing questions collection.

        Args:
            collection: Collection object containing:
                - name: Collection name
                - mlName: Multilingual name map
                - description: Collection description
                - mlDescription: Multilingual description map
                - icon: Icon name
                - iconFont: Icon font
                - media: Media name
                - mediaContentType: Media content type
                - weight: Collection weight

        Returns:
            Result: API response confirming collection creation/update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Question-APIs/operation/Set%20Questions%20Collection
        """
        data = {
            "collection": collection,
        }
        result: Result = self.adapter.put(
            "/espapi/analytic/questions/collections",
            ep_json=data,
        )
        return result

    def delete_question_collection(
        self,
        name: str,
    ) -> Result:
        """
        Delete Question Collection.

        Remove the binding to the specified collection for all questions asked by the bot instance
        (does not delete the questions).

        Args:
            name: Collection name (required)

        Returns:
            Result: API response confirming deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Question-APIs/operation/Delete%20Question%20Collection
        """
        params = {
            "name": name,
        }
        result: Result = self.adapter.delete(
            "/espapi/analytic/questions/collections",
            ep_params=params,
        )
        return result

    def get_tags(
        self,
        tag_type: Optional[int] = None,
        id_value: Optional[str] = None,
    ) -> Result:
        """
        Get Tags.

        Return the list of tags that this bot has given to the user's entities.
        If the entity ID argument is passed in, then we return tags for that entity that were previously set by this bot.

        Args:
            tag_type: Tag type filter (1=User, 2=Location, 3=Device)
            id_value: Retrieve tags set by this bot from a specific entity ID

        Returns:
            Result: API response with tags data

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Tag-APIs/operation/Get%20Tags
        """
        params = {}
        if tag_type is not None:
            params["type"] = tag_type
        if id_value is not None:
            params["id"] = id_value
        result: Result = self.adapter.get(
            "/espapi/analytic/tags",
            ep_params=params if params else None,
        )
        return result

    def apply_tags(
        self,
        tags: List[Dict],
    ) -> Result:
        """
        Apply Tags.

        Apply bot tags for locations, users, and devices.

        Args:
            tags: List of tag objects, each containing:
                - type: Tag type (1=User, 2=Location, 3=Device)
                - tag: Tag value (required)
                - id: Location, device, or user ID (required)
                - category: Location tag category (optional)
                - priority: Location tag priority (optional)

        Returns:
            Result: API response confirming tags applied

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Tag-APIs/operation/Apply%20Tags
        """
        data = {
            "tags": tags,
        }
        result: Result = self.adapter.put(
            "/espapi/analytic/tags",
            ep_json=data,
        )
        return result

    def delete_tags(
        self,
        tag_type: int,
        tag: str,
        id_value: Optional[str] = None,
    ) -> Result:
        """
        Delete Tags.

        Delete bot tags for users, locations, and devices.

        Args:
            tag_type: Tag type filter (1=User, 2=Location, 3=Device) (required)
            tag: Tag value (required)
            id_value: The entity ID to remove the tag from, optional for location tags

        Returns:
            Result: API response confirming tags deleted

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Tag-APIs/operation/Delete%20Tags
        """
        params = {
            "type": tag_type,
            "tag": tag,
        }
        if id_value is not None:
            params["id"] = id_value
        result: Result = self.adapter.delete(
            "/espapi/analytic/tags",
            ep_params=params,
        )
        return result

    def send_notification(
        self,
        category: int,
        notification_data: Dict,
    ) -> Result:
        """
        Send a Notification.

        Sends an arbitrary push notification or email or sms to the user.

        Args:
            category: Bot communication categories, where to send notifications (required).
                     Multiple values are supported:
                     - 0 = Location Users
                     - 1 = Specific Address
                     - 2 = Organization Users
            notification_data: Notification data containing:
                - brand: Notification brand
                - botNotificationId: Bot notification ID to select organization notification groups
                - users: List of user IDs (for organizational bots)
                - userCategories: List of user categories
                - pushMessage: Push message object
                - emailMessage: Email message object
                - smsMessage: SMS message object
                - attachments: List of attachment objects

        Returns:
            Result: API response with notification result

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Notification-APIs/operation/Send%20a%20Notification
        """
        params = {
            "category": category,
        }
        result: Result = self.adapter.post(
            "/espapi/analytic/notifications",
            ep_params=params,
            ep_json=notification_data,
        )
        return result

    def send_location_notification(
        self,
        location_id: int,
        notification_data: Dict,
    ) -> Result:
        """
        Send a Location Notification.

        Send a notification to users at a specific location.

        Args:
            location_id: Location ID (required)
            notification_data: Notification data (same as send_notification)

        Returns:
            Result: API response with notification result

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Notification-APIs/operation/Send%20a%20Location%20Notification
        """
        result: Result = self.adapter.post(
            f"/espapi/analytic/location/{location_id}/notifications",
            ep_json=notification_data,
        )
        return result

    def update_location(
        self,
        location_id: int,
        location_data: Dict,
    ) -> Result:
        """
        Edit Location.

        Update location information. This API is similar to the cloud update location API.

        Args:
            location_id: Location ID to update (required)
            location_data: Location data as JSON object with 'location' key

        Returns:
            Result: API response confirming update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Location-APIs/operation/Edit%20Location
        """
        result: Result = self.adapter.put(
            f"/espapi/analytic/location/{location_id}",
            ep_json=location_data,
        )
        return result

    def get_device_parameters(
        self,
        device_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        param_name: Optional[str] = None,
        index: Optional[str] = None,
        last_rows: Optional[int] = None,
    ) -> Result:
        """
        Get Current or Historical Parameters.

        Historical measurements should never be accessed directly by a user's bot.
        For large data values and machine learning bot should submit an asynchronous data request.

        But we do make the historical measurement API available for the Python BotEngine Framework
        to fast-forward through months of data when a bot is initialized.

        By leaving the start_date, end_date, or last_rows empty, this API call will return only
        the current measurements.

        Args:
            device_id: Device ID to extract parameters from (required)
            start_date: Start time in milliseconds to begin receiving measurements.
                       If not set, only latest measurements will be returned.
            end_date: End time in milliseconds to stop receiving measurements, default is the current time
            param_name: One or more parameter names
            index: Only obtain measurements for parameters with this index number
            last_rows: Receive only last N measurements

        Returns:
            Result: API response with device parameters

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Device-APIs/operation/Get%20Current%20or%20Historical%20Parameters
        """
        params = {}
        if start_date is not None:
            params["startDate"] = start_date
        if end_date is not None:
            params["endDate"] = end_date
        if param_name is not None:
            params["paramName"] = param_name
        if index is not None:
            params["index"] = index
        if last_rows is not None:
            params["lastRows"] = last_rows
        result: Result = self.adapter.get(
            f"/espapi/analytic/devices/{device_id}/parameters",
            ep_params=params if params else None,
        )
        return result

    def set_device_parameters(
        self,
        device_id: str,
        parameters: List[Dict],
    ) -> Result:
        """
        Set Device Parameters.

        Update device parameters.

        Args:
            device_id: Device ID (required)
            parameters: List of parameter objects, each containing:
                - name: Parameter name
                - value: Parameter value
                - unit: Parameter unit (optional)
                - index: Parameter index (optional)

        Returns:
            Result: API response confirming parameters set

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Device-APIs/operation/Set%20Device%20Parameters
        """
        data = {
            "parameters": parameters,
        }
        result: Result = self.adapter.post(
            f"/espapi/analytic/devices/{device_id}/parameters",
            ep_json=data,
        )
        return result

    def inject_device_parameters(
        self,
        device_id: str,
        timestamp: int,
        params: List[Dict],
    ) -> Result:
        """
        Inject Device Parameters.

        Synthetic device parameters (not provided by real devices) can be injected to parameters history.

        Args:
            device_id: Device ID for which to inject parameters (required)
            timestamp: Timestamp in milliseconds for the parameters
            params: List of parameter objects, each containing:
                - name: Parameter name (required)
                - value: Parameter value (required)
                - index: Parameter index (optional)

        Returns:
            Result: API response confirming parameters injected

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Device-APIs/operation/Inject%20Device%20Parameters
        """
        data = {
            "timestamp": timestamp,
            "params": params,
        }
        result: Result = self.adapter.post(
            f"/espapi/analytic/devices/{device_id}/parameters",
            ep_json=data,
        )
        return result

    def send_device_commands(
        self,
        devices: List[Dict],
    ) -> Result:
        """
        Send Commands.

        This API allows to send commands to multiple devices simultaneously.

        This operation is not atomic. It will try to execute all commands in the same order,
        as they are provided. If some command fails, it will execute the next one.
        The result code is returned for each command.

        Args:
            devices: List of device command objects, each containing:
                - deviceId: Device ID (required)
                - commandType: Command type (required)
                - commandTimeout: Command timeout in milliseconds (required)
                - params: List of parameter objects, each containing:
                    - name: Parameter name (required)
                    - value: Parameter value (required)
                    - index: Parameter index (optional)
                - comment: Optional comment explaining why this command has been sent

        Returns:
            Result: API response with result code for each command

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Device-APIs/operation/Send%20Commands
        """
        data = {
            "devices": devices,
        }
        result: Result = self.adapter.put(
            "/espapi/analytic/parameters",
            ep_json=data,
        )
        return result

    def update_parameters(
        self,
        parameters: List[Dict],
    ) -> Result:
        """
        Update Parameters.

        Update multiple device parameters across devices.

        Args:
            parameters: List of parameter objects, each containing:
                - deviceId: Device ID
                - name: Parameter name
                - value: Parameter value
                - unit: Parameter unit (optional)
                - index: Parameter index (optional)

        Returns:
            Result: API response confirming parameters updated

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Device-APIs/operation/Update%20Parameters
        """
        data = {
            "parameters": parameters,
        }
        result: Result = self.adapter.put(
            "/espapi/analytic/parameters",
            ep_json=data,
        )
        return result

    def send_ai_request(
        self,
        model_name: str,
        ai_data: Dict,
        key: Optional[str] = None,
    ) -> Result:
        """
        Send a request to a model.

        Send asynchronous request to an AI model to obtain a model response.
        Bots can interact asynchronously with registered AI applications using this API.

        Args:
            model_name: Unique name of the model installed in the cloud (required)
            ai_data: AI request data containing:
                - text: Simple completion text (for LLama)
                - chat: List of chat messages (for LLama chat completion)
                - phrases: List of phrases for scoring (for SetFit)
                - params: Optional parameters object (temperature, top_p, etc.)
            key: A reference to the request that will be sent to the bot along with the response

        Returns:
            Result: API response confirming request sent

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-AI-APIs/operation/Send%20a%20request%20to%20a%20model
        """
        params = {
            "name": model_name,
        }
        if key is not None:
            params["key"] = key
        result: Result = self.adapter.post(
            "/espapi/analytic/ai",
            ep_params=params,
            ep_json=ai_data,
        )
        return result

    def send_openai_request(
        self,
        openai_data: Dict,
        key: Optional[str] = None,
        openai_organization: Optional[str] = None,
    ) -> Result:
        """
        Send a request for chat completion.

        Send asynchronous request to Open AI API to obtain a model response for the given chat conversation.

        Args:
            openai_data: OpenAI request data containing:
                - model: Model name (e.g., 'gpt-3.5-turbo')
                - messages: List of message objects with 'role' and 'content'
                - temperature: Optional temperature parameter
            key: A reference to the request that will be sent to the bot along with the response from ChatGPT
            openai_organization: An organization which will be used (charged) for an Open AI API request

        Returns:
            Result: API response confirming request sent

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-AI-APIs/operation/Send%20a%20request%20for%20chat%20completion
        """
        params = {}
        if key is not None:
            params["key"] = key
        if openai_organization is not None:
            params["openAiOrganization"] = openai_organization
        result: Result = self.adapter.post(
            "/espapi/analytic/openai",
            ep_params=params if params else None,
            ep_json=openai_data,
        )
        return result

    def upload_goicon_document(
        self,
        file_content: bytes,
        description: str,
        category: str,
        timestamp: Optional[str] = None,
        visible_to_residents: Optional[bool] = None,
    ) -> Result:
        """
        Upload GoIcon Document.

        Upload a PDF document to a GoIcon resident associated with the bot's location.
        The system resolves the GoIcon resident from a cached GoIcon resident ID or,
        if not found, from the MooringsPark external user ID.

        Args:
            file_content: PDF document content (binary data)
            description: Document description
            category: Document category (e.g., "Service Plans")
            timestamp: Document timestamp, epoch milliseconds or ISO-8601 date-time
            visible_to_residents: Whether the document is visible to residents in GoIcon

        Returns:
            Result: API response confirming upload

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Server-APIs/operation/Upload%20GoIcon%20Document
        """
        params = {
            "description": description,
            "category": category,
            "timestamp": timestamp,
            "visibleToResidents": visible_to_residents,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.post(
            "/espapi/analytic/goicon/documents",
            ep_params=params,
            ep_data=file_content,
            ep_headers={"Content-Type": "application/octet-stream"},
        )
        return result

    def send_voice_call(
        self,
        voice_call_data: Dict,
    ) -> Result:
        """
        Outbound Voice Call.

        This API initiates outbound voice call.

        Args:
            voice_call_data: Voice call data containing:
                - model: Voice call model with settings, startStepId, and steps
                - userId: User ID to call
                - phoneNumber: Phone number to call (optional)

        Returns:
            Result: API response with call UUID

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Notification-APIs/operation/Outbound%20Voice%20Call
        """
        result: Result = self.adapter.post(
            "/espapi/analytic/voiceCall",
            ep_json=voice_call_data,
        )
        return result

    def set_voice_call_answer(
        self,
        user_id: int,
        model: Dict,
    ) -> Result:
        """
        Set Inbound Voice Call Model.

        When a user makes an inbound voice call, the cloud generates an answer scenario
        based on an existing Outbound Voice Call Model without triggering bots.

        Args:
            user_id: User ID, support for multiple values (required)
            model: Voice call model with settings, startStepId, and steps

        Returns:
            Result: API response confirming model set

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Notification-APIs/operation/Set%20Inbound%20Voice%20Call%20Model
        """
        params = {
            "userId": user_id,
        }
        data = {
            "model": model,
        }
        result: Result = self.adapter.post(
            "/espapi/analytic/voiceCallAnswer",
            ep_params=params,
            ep_json=data,
        )
        return result

    def delete_voice_call_answer(
        self,
        user_id: int,
    ) -> Result:
        """
        Delete Inbound Voice Call Model.

        Remove the inbound voice call model for a user.

        Args:
            user_id: User ID (required)

        Returns:
            Result: API response confirming deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Notification-APIs/operation/Delete%20Inbound%20Voice%20Call%20Model
        """
        params = {
            "userId": user_id,
        }
        result: Result = self.adapter.delete(
            "/espapi/analytic/voiceCallAnswer",
            ep_params=params,
        )
        return result

    def submit_ticket(
        self,
        ticket_data: Dict,
    ) -> Result:
        """
        Submit Ticket.

        Publish a ticket to Zendesk.

        Args:
            ticket_data: Ticket data containing:
                - brand: Brand name
                - lang: Language code
                - template: Template name
                - userId: User ID
                - ticket: Ticket object with:
                    - type: Ticket type (1=Problem, 2=Incident, 3=Question, 4=Task)
                    - priority: Ticket priority (1=Low, 2=Normal, 3=High, 4=Urgent)
                    - subject: Ticket subject
                    - comment: Ticket comment
                    - data: Optional data map
                    - customFields: List of custom field objects

        Returns:
            Result: API response confirming ticket submission

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Notification-APIs/operation/Submit%20Ticket
        """
        result: Result = self.adapter.post(
            "/espapi/analytic/ticket",
            ep_json=ticket_data,
        )
        return result

    def send_fall_feedback(
        self,
        feedback_data: Dict,
    ) -> Result:
        """
        Send Fall Event Feedback.

        Send feedback regarding fall events.

        Args:
            feedback_data: Feedback data containing:
                - deviceId: Device ID
                - classification: Fall event classification (TRUE_POSITIVE, FALSE_POSITIVE, FALSE_NEGATIVE, TEST_FALL)
                - eventTimestamp: Event timestamp in milliseconds
                - comment: Optional comment

        Returns:
            Result: API response confirming feedback sent

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Device-APIs/operation/Send%20Fall%20Event%20Feedback
        """
        result: Result = self.adapter.post(
            "/espapi/analytic/fallFeedback",
            ep_json=feedback_data,
        )
        return result

    def send_mms(
        self,
        user_id: int,
        media_type: int,
        url: str,
        caption: Optional[str] = None,
    ) -> Result:
        """
        Send MMS.

        Send an image or audio content to the user's phone.

        Args:
            user_id: User ID, multiple values supported (required)
            media_type: Media type (1=image, 2=audio) (required)
            url: Static media URL (required)
            caption: Additional text to accompany the media file

        Returns:
            Result: API response confirming MMS sent

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Notification-APIs/operation/Send%20MMS
        """
        params = {
            "userId": user_id,
            "mediaType": media_type,
            "url": url,
        }
        if caption is not None:
            params["caption"] = caption
        result: Result = self.adapter.post(
            "/espapi/analytic/mms",
            ep_params=params,
        )
        return result

    def execute_cli(
        self,
        json_data: str,
        initialize: Optional[str] = None,
        cli_data: Optional[Dict] = None,
    ) -> Result:
        """
        Cloud Execution.

        The cloud is expected to run the bot from the command line.
        This API provides bot execution data for command line execution.

        Args:
            json_data: The JSON that would be passed to the bot over the command line (required)
            initialize: Include this option if this bot instance should be initialized
            cli_data: CLI execution data (optional)

        Returns:
            Result: API response with execution data

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bots-Execution/operation/Cloud%20Execution
        """
        params = {
            "json": json_data,
        }
        if initialize is not None:
            params["initialize"] = initialize
        result: Result = self.adapter.post(
            "/espapi/cli",
            ep_params=params,
            ep_json=cli_data,
        )
        return result

    def get_challenge_participants(
        self,
        challenge_id: int,
        status: Optional[int] = None,
        location_id: Optional[int] = None,
        get_devices: Optional[bool] = None,
        device_category: Optional[int] = None,
    ) -> Result:
        """
        Get Participants.

        Return invitational challenge participants.

        Args:
            challenge_id: Challenge ID to obtain participants for (required)
            status: Participation status filter
            location_id: Filter the response by location ID
            get_devices: Return devices as well
            device_category: Filter devices by a type category

        Returns:
            Result: API response with challenge participants

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/bots.html#tag/Bot-Challenge-APIs/operation/Get%20Participants
        """
        params = {}
        if status is not None:
            params["status"] = status
        if location_id is not None:
            params["locationId"] = location_id
        if get_devices is not None:
            params["getDevices"] = get_devices
        if device_category is not None:
            params["deviceCategory"] = device_category
        result: Result = self.adapter.get(
            f"/espapi/analytic/admin/challenges/{challenge_id}/participants",
            ep_params=params if params else None,
        )
        return result

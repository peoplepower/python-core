# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "requests",
# ]
# ///

import json
from typing import Dict, List, Optional

from ...models import APIKeyType, Result
from ..api import API


class UserCommunication(API):
    def get_notification_subscriptions(
        self,
        user_id: int = None,
    ) -> Result:
        """
        Get Notification Subscriptions.

        A user may subscribe or unsubscribe from certain types of push and email notifications,
        or set boundaries on how many notifications their account can receive within a specified amount of time.

        Args:
            user_id: User ID for bots and administrators

        Returns:
            Result: API response with notification subscriptions

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/User-Communications/operation/Get%20Notification%20Subscriptions
        """
        params = {
            "userId": user_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/espapi/cloud/json/notificationSubscriptions",
            ep_params=params,
        )
        return result

    def set_notification_subscriptions(
        self,
        notification_type: int,
        location_id: int = None,
        user_id: int = None,
        email: bool = None,
        push: bool = None,
        sms: bool = None,
        email_period: int = None,
        push_period: int = None,
    ) -> Result:
        """
        Set Notification Subscriptions.

        Set notification subscription preferences for a specific notification type.

        Args:
            notification_type: Type of notification (required)
            location_id: Location ID
            user_id: User ID for bots and administrators
            email: Email notifications enabled (true/false)
            push: Push notifications enabled (true/false)
            sms: SMS notifications enabled (true/false)
            email_period: Minimum number of seconds between email notifications
            push_period: Minimum number of seconds between push notifications

        Returns:
            Result: API response confirming update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/User-Communications/operation/Set%20Notification%20Subscriptions
        """
        params = {
            "userId": user_id,
            "locationId": location_id,
            "email": email,
            "push": push,
            "sms": sms,
            "emailPeriod": email_period,
            "pushPeriod": push_period,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.put(
            f"/espapi/cloud/json/notificationSubscriptions/{notification_type}",
            ep_params=params,
        )
        return result

    def post_push_notification_token(
        self,
        app_name: str,
        token: str,
        badge: bool = None,
        brand: str = None,
    ) -> Result:
        """
        Register App for Push Notifications.

        Register an app and token for push notifications.

        Args:
            app_name: Unique App Name to register for push notifications (required)
            token: The iOS notification token or the Android device registration ID (required)
            badge: This app supports badge icons (true/false)
            brand: If set, the app will not receive notifications addressed to different brands

        Returns:
            Result: API response confirming registration

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/User-Communications/operation/Register%20App%20for%20Push%20Notifications
        """
        params = {
            "badge": badge,
            "brand": brand,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.put(
            f"/espapi/cloud/json/notificationToken/{app_name}/{token}",
            ep_params=params,
        )
        return result

    def delete_push_notification_token(
        self,
        token: str,
    ) -> Result:
        """
        Unregister App for Push Notifications.

        Unregister a push notification token.

        Args:
            token: The iOS notification token or the Android device registration ID (required)

        Returns:
            Result: API response confirming unregistration

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/User-Communications/operation/Unregister%20App%20for%20Push%20Notifications
        """
        result: Result = self.adapter.delete(
            f"/espapi/cloud/json/notificationToken/{token}",
        )
        return result

    def send_notification(
        self,
        notification_data: Dict,
        user_id: int = None,
        location_id: int = None,
        organization_id: int = None,
    ) -> Result:
        """
        Send a Notification.

        Sends an arbitrary push notification or email to the user.
        If you're sending an email, you may include a subject and specify whether the email is in HTML format or plain text.
        Push notification messages are limited by the standard push notification payload size.

        Args:
            notification_data: Notification data including brand, userCategories, users, language,
                             pushMessage, emailMessage, smsMessage, deviceMessage (required)
            user_id: Send a notification to this user by an administrator
            location_id: Send a notification to users on this location
            organization_id: Use templates of specific organization

        Returns:
            Result: API response confirming notification sent

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/User-Communications/operation/Send%20a%20Notification
        """
        params = {
            "userId": user_id,
            "locationId": location_id,
            "organizationId": organization_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.post(
            "/espapi/cloud/json/notifications",
            ep_json=notification_data,
            ep_params=params,
        )
        return result

    def get_notifications(
        self,
        start_date: str,
        user_id: int = None,
        end_date: str = None,
        location_id: int = None,
        source_type: int = None,
        delivery_type: int = None,
        notification_type: int = None,
    ) -> Result:
        """
        Get Notifications.

        Get notification history.

        Args:
            start_date: Start date to select notifications (required)
            user_id: Get notifications for this user by an administrator
            end_date: End date to select notifications. Default is the current date.
            location_id: Get notifications related to this location
            source_type: Filter by source type
            delivery_type: Filter by delivery type
            notification_type: Filter by notification type

        Returns:
            Result: API response with notification history

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/User-Communications/operation/Get%20Notifications
        """
        params = {
            "userId": user_id,
            "startDate": start_date,
            "endDate": end_date,
            "locationId": location_id,
            "sourceType": source_type,
            "deliveryType": delivery_type,
            "notificationType": notification_type,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/espapi/cloud/json/notifications",
            ep_params=params,
        )
        return result

    def post_support_ticket(
        self,
        ticket_data: Dict,
        user_id: int = None,
        location_id: int = None,
    ) -> Result:
        """
        Post Support Ticket.

        Create a support ticket.

        Args:
            ticket_data: Ticket data including brand, lang, ticket with type, priority, subject,
                        comment, customFields (required)
            user_id: Request support for this user by an administrator
            location_id: Request support for this location

        Returns:
            Result: API response confirming ticket creation

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/User-Communications/operation/Post%20Support%20Ticket
        """
        params = {
            "userId": user_id,
            "locationId": location_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.post(
            "/espapi/cloud/json/ticket",
            ep_json=ticket_data,
            ep_params=params,
        )
        return result

    def post_feedback(
        self,
        feedback_data: Dict,
        user_id: int = None,
        brand: str = None,
    ) -> Result:
        """
        Post Crowd Feedback.

        Crowd feedback is first delivered to a support email for moderation.
        If the feedback is unique, then the support staff will make it public for other users to vote on.

        Args:
            feedback_data: Feedback data including feedback object with appName, appVersion, type,
                          subject, email, deviceId, deviceModel, deviceOs, productId,
                          productCategory, viewer, description (required)
            user_id: Send a feedback for this user by an administrator
            brand: Application brand

        Returns:
            Result: API response with created feedback ID and ticket information

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/User-Communications/operation/Post%20Crowd%20Feedback
        """
        params = {
            "userId": user_id,
            "brand": brand,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.post(
            "/espapi/cloud/json/feedback",
            ep_json=feedback_data,
            ep_params=params,
        )
        return result

    def get_feedback_by_search(
        self,
        app_name: str,
        feedback_type: int,
        length: int,
        start_pos: int = None,
        product_id: int = None,
        product_category: int = None,
        disabled: bool = None,
    ) -> Result:
        """
        Get Crowd Feedback by Searching.

        Search for feedback items by app name and type.

        Args:
            app_name: Unique name / identifier of the app or product (required)
            feedback_type: 1 - New feature request, 2 - Problem report (required)
            length: Number of records to return (required)
            start_pos: Index of the first record to be returned
            product_id: Filter the response by product ID. Multiple values supported.
            product_category: Filter the response by product category. Multiple values supported.
            disabled: Return not enabled feedbacks as well

        Returns:
            Result: API response with list of feedback items

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/User-Communications/operation/Get%20Crowd%20Feedback%20by%20Searching
        """
        params = {
            "startPos": start_pos,
            "length": length,
            "productId": product_id,
            "productCategory": product_category,
            "disabled": disabled,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            f"/espapi/cloud/json/feedback/{app_name}/{feedback_type}",
            ep_params=params,
        )
        return result

    def get_specific_feedback(
        self,
        feedback_id: int,
    ) -> Result:
        """
        Get Specific Crowd Feedback.

        Get a specific feedback item by ID.

        Args:
            feedback_id: Specific feedback ID (required)

        Returns:
            Result: API response with feedback item

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/User-Communications/operation/Get%20Specific%20Crowd%20Feedback
        """
        result: Result = self.adapter.get(
            f"/espapi/cloud/json/feedback/{feedback_id}",
        )
        return result

    def vote_for_feedback(
        self,
        feedback_id: int,
        rank: int,
    ) -> Result:
        """
        Vote for Feedback.

        Vote for or remove a vote from a feedback item.

        Args:
            feedback_id: Feedback ID to vote on (required)
            rank: 1 to cast a vote, 0 to remove a vote (required)

        Returns:
            Result: API response confirming vote

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/User-Communications/operation/Vote%20for%20Feedback
        """
        result: Result = self.adapter.put(
            f"/espapi/cloud/json/feedback/{feedback_id}/{rank}",
        )
        return result

    def support(
        self,
        support_data: Dict,
        app_name: str = None,
    ) -> Result:
        """
        Request Support.

        Submit a support request. If a ticket has been created in a support cloud,
        then the API returns the ticket ID and the brand name.

        Args:
            support_data: Support request data including firstName, lastName, email, subject,
                         text, subscribe (required)
            app_name: App name to forward the support request

        Returns:
            Result: API response with ticket ID and brand information

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/User-Communications/operation/Request%20Support
        """
        params = {
            "appName": app_name,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.post(
            "/espapi/cloud/json/support",
            ep_json=support_data,
            ep_params=params,
        )
        return result

    def get_questions(
        self,
        location_id: int,
        answer_statuses: List[int] = None,
        editable: bool = None,
        collection_name: str = None,
        question_id: int = None,
        app_instance_id: int = None,
        lang: str = None,
        limit: int = None,
    ) -> Result:
        """
        Get Questions.

        Questions enable bidirectional conversations to take place between the users' location
        and data analytics services. Questions enable the user to add context to the data.

        Args:
            location_id: Location ID to get questions (required)
            answer_statuses: Return questions with requested answer statuses.
                           By default questions with statuses 2 and 3 are returned.
                           Multiple values are supported.
            editable: Filter answered questions:
                     true - return only editable answered questions,
                     false - return only not editable answered questions,
                     otherwise return all answered questions.
            collection_name: Questions collection name filter
            question_id: Extract a specific question ID
            app_instance_id: Only retrieve questions for a specific bot
            lang: Questions text language. If not set, user's or default language will be used.
            limit: Maximum number of questions to return. The default is unlimited.

        Returns:
            Result: API response with list of questions

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/User-Communications/operation/Get%20Questions
        """
        params = {
            "locationId": location_id,
            "answerStatus": answer_statuses,
            "editable": editable,
            "collectionName": collection_name,
            "questionId": question_id,
            "appInstanceId": app_instance_id,
            "lang": lang,
            "limit": limit,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/espapi/cloud/json/questions",
            ep_params=params,
        )
        return result

    def answer_questions(
        self,
        location_id: int,
        answers: Dict,
        check_if_valid: bool = None,
    ) -> Result:
        """
        Answer Questions.

        After answering a question, if the question is aggregated publicly then the user
        should also see how other people voted.

        Args:
            location_id: Location ID to answer questions (required)
            answers: Answers data including questions array with id, answer, answerStatus (required)
            check_if_valid: Check if the answers are valid

        Returns:
            Result: API response with answered questions

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/User-Communications/operation/Answer%20Questions
        """
        params = {
            "locationId": location_id,
            "checkIfValid": check_if_valid,
        }
        params = {k: v for k, v in params.items() if v is not None}
        headers = None
        if check_if_valid:
            headers = {"Content-Type": "application/json"}
        result: Result = self.adapter.put(
            "/espapi/cloud/json/questions",
            ep_json=answers,
            ep_params=params,
            ep_headers=headers,
        )
        return result

    def get_message_topics(
        self,
        app_id: int = None,
        lang: str = None,
        analytic_key: str = None,
    ) -> Result:
        """
        Get Message Topics.

        Get available message topics for bots.

        Args:
            app_id: Bot ID
            lang: Preferred content language
            analytic_key: Analytic API key for authentication

        Returns:
            Result: API response with message topics

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/User-Communications/operation/Get%20Message%20Topics
        """
        params = {
            "appId": app_id,
            "lang": lang,
        }
        params = {k: v for k, v in params.items() if v is not None}
        headers = None
        if analytic_key:
            headers = self.adapter._get_headers(analytic_key, APIKeyType.ANALYTIC)
        result: Result = self.adapter.get(
            "/espapi/cloud/json/messageTopics",
            ep_params=params,
            ep_headers=headers,
        )
        return result

    def create_messages(
        self,
        messages: Dict,
        location_id: int = None,
        analytic_key: str = None,
    ) -> Result:
        """
        Create Messages.

        Message APIs allow to create, schedule, and retrieve messages from AI bots to location users.

        Args:
            messages: Messages data including messages array with status, originalMessageId, topicId,
                     scheduleType, contentKey, contents, questionId, mediaUrl, etc. (required)
            location_id: Location ID, when created by a user
            analytic_key: Analytic API key for authentication

        Returns:
            Result: API response with created message IDs

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/User-Communications/operation/Create%20Messages
        """
        params = {
            "locationId": location_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        headers = None
        if analytic_key:
            headers = self.adapter._get_headers(analytic_key, APIKeyType.ANALYTIC)
        result: Result = self.adapter.post(
            "/espapi/cloud/json/messages",
            ep_json=messages,
            ep_params=params,
            ep_headers=headers,
        )
        return result

    def update_messages(
        self,
        location_id: int,
        messages: Dict,
    ) -> Result:
        """
        Update Messages.

        Update messages for a location.
        """
        params = {
            "locationId": location_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.put(
            "/espapi/cloud/json/messages",
            ep_json=messages,
            ep_params=params,
        )
        return result

    def get_messages(
        self,
        location_id: int,
        start_date: str,
        end_date: str = None,
        app_instance_id: int = None,
        topic_id: str = None,
        read_status: bool = None,
        lang: str = None,
    ) -> Result:
        """
        Get Messages.

        Retrieve messages for a location.

        Args:
            location_id: Location ID (required)
            start_date: Start date to filter by delivery date (required)
            end_date: End date to filter by delivery date
            app_instance_id: Bot instance ID
            topic_id: Filter by topic
            read_status: Filter read or unread messages
            lang: Preferred message content language

        Returns:
            Result: API response with messages

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/User-Communications/operation/Get%20Messages
        """
        params = {
            "locationId": location_id,
            "startDate": start_date,
            "endDate": end_date,
            "appInstanceId": app_instance_id,
            "topicId": topic_id,
            "readStatus": read_status,
            "lang": lang,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/espapi/cloud/json/messages",
            ep_params=params,
        )
        return result

    def update_message_read_status(
        self,
        location_id: int,
        message_id: int,
        read_status: bool,
    ) -> Result:
        """
        Update Message Read Status.

        A user can mark a message as read or unread.

        Args:
            location_id: Location ID (required)
            message_id: Message ID (required)
            read_status: Read status (required)

        Returns:
            Result: API response confirming status update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/User-Communications/operation/Update%20Message%20Read%20Status
        """
        params = {
            "locationId": location_id,
            "messageId": message_id,
            "readStatus": read_status,
        }
        result: Result = self.adapter.put(
            "/espapi/cloud/json/messageRead",
            ep_params=params,
        )
        return result

    def get_survey_answers(
        self,
        location_id: int,
        user_id: int = None,
        survey_key: str = None,
        status: int = None,
        start_date: str = None,
        end_date: str = None,
    ) -> Result:
        """
        Get Survey Answers.

        Returns history of survey answers.

        Args:
            location_id: Location ID (required)
            user_id: User ID filter
            survey_key: Survey filter
            status: Survey answer status filter (0 - Open, 1 - Closed)
            start_date: Answers start date
            end_date: Answers end date

        Returns:
            Result: API response with survey answers history

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Questions/operation/Get%20Survey%20Answers
        """
        params = {
            "locationId": location_id,
            "userId": user_id,
            "surveyKey": survey_key,
            "status": status,
            "startDate": start_date,
            "endDate": end_date,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/espapi/cloud/json/surveyAnswers",
            ep_params=params,
        )
        return result

    def start_answering_survey(
        self,
        location_id: int,
        survey_key: str,
        user_id: int,
        answer_id: int = None,
        pre_answer_id: int = None,
        send_to_user: bool = None,
        notification_category: int = None,
        questions: List[Dict] = None,
        notification_model: Dict = None,
    ) -> Result:
        """
        Start Answering Survey.

        Initiates a survey answering. This API creates a new survey answer record for the
        requested user or returns an existing answer record.

        A user or a bot can submit answers to some survey questions in this request.
        Also question answers can be copied from a previously submitted survey by ID.

        The API can send an email to a user or to an organization notification users with
        a link to answer the survey or to view the existing answers, if the sendToUser or
        the notificationCategory parameters are provided.

        The API returns the answer record with an authentication token and a URL to answer
        the survey for the user or view the previous answers.

        Args:
            location_id: Answer a survey for this location (required)
            survey_key: Key of the survey to answer (required)
            user_id: Answer a survey for this user (required)
            answer_id: An existing answer record ID to recreate previous API response and action
            pre_answer_id: Copy question answers from this answer record
            send_to_user: Send the email directly to the location users
            notification_category: Send the email to organization notification user with this category
            questions: Optional answers to the survey questions (list of dicts with questionKey and answer)
            notification_model: Additional notification template parameters as a string map

        Returns:
            Result: API response with answer record, token, and survey URL

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Questions/operation/Start%20Answering%20Survey
        """
        params = {
            "locationId": location_id,
            "surveyKey": survey_key,
            "userId": user_id,
            "answerId": answer_id,
            "preAnswerId": pre_answer_id,
            "sendToUser": send_to_user,
            "notificationCategory": notification_category,
        }
        params = {k: v for k, v in params.items() if v is not None}
        body = {}
        if questions is not None:
            body["questions"] = questions
        if notification_model is not None:
            body["notificationModel"] = notification_model
        result: Result = self.adapter.post(
            "/espapi/cloud/json/surveyAnswers",
            ep_params=params,
            ep_json=body if body else None,
        )
        return result

    def get_survey_questions(
        self,
        location_id: int = None,
        answer_id: int = None,
    ) -> Result:
        """
        Get Survey Questions.

        Return open organization survey details, sections, questions, and previously submitted answers.

        The request can be authenticated either by a survey answer token (Bearer JWT) or by a user or bot API key.

        Args:
            location_id: Location ID when a user or a bot is authenticated
            answer_id: Answer ID when a user or a bot is authenticated

        Returns:
            Result: API response with survey questions

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Questions/operation/Get%20Survey%20Questions
        """
        params = {
            "locationId": location_id,
            "answerId": answer_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/espapi/cloud/json/surveyQuestions",
            ep_params=params,
        )
        return result

    def answer_survey_questions(
        self,
        questions: Dict,
        location_id: int = None,
        answer_id: int = None,
        status: int = None,
    ) -> Result:
        """
        Answer Survey Questions.

        Put survey answers to the latest open survey response.
        A user can submit a portion of answers in one API call. Some of answers can overwrite previous.

        The API checks, if the survey is not answered yet by the user (within configured date interval).

        An optional parameter `status` is used to finalize the latest survey response.
        In this case the API checks that all questions answered and triggers bots.

        The request can be authenticated either by a survey answer token (Bearer JWT) or by a user or bot API key.

        Args:
            questions: Questions data including questions array with questionKey and answer (required)
            location_id: Location ID when a user or a bot is authenticated
            answer_id: Answer ID when a user or a bot is authenticated
            status: Change survey response status: 1 - close

        Returns:
            Result: API response confirming answers submitted

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Questions/operation/Answer%20Survey%20Questions
        """
        params = {
            "locationId": location_id,
            "answerId": answer_id,
            "status": status,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.put(
            "/espapi/cloud/json/surveyQuestions",
            ep_json=questions,
            ep_params=params if params else None,
        )
        return result

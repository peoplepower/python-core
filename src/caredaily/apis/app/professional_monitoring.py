# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "requests",
# ]
# ///

import json
from datetime import datetime
from typing import Dict, List, Optional

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


class ProfessionalMonitoring(API):
    def get_call_center_settings(
        self,
        location_id: int,
    ) -> Result:
        """
        Get Call Center.

        Retrieve call center service statuses.

        Args:
            location_id: Location ID (required)

        Returns:
            Result: API response with call center settings

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Professional-Monitoring/operation/Get%20Call%20Center
        """
        params = {
            "locationId": location_id,
        }
        result: Result = self.adapter.get(
            "/cloud/json/callCenter",
            ep_params=params,
        )
        return result

    def provide_call_center_settings(
        self,
        location_id: int,
        settings_data: Dict,
    ) -> Result:
        """
        Update Call Center.

        Update user's call center record.

        Args:
            location_id: Location ID (required)
            settings_data: Call center settings data

        Returns:
            Result: API response

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Professional-Monitoring/operation/Update%20Call%20Center
        """
        params = {
            "locationId": location_id,
        }
        result: Result = self.adapter.put(
            "/cloud/json/callCenter",
            ep_params=params,
            ep_json=settings_data,
        )
        return result

    def delete_call_center(
        self,
        location_id: int = None,
    ) -> Result:
        """
        Delete Call Center.

        Delete call center registration.

        Args:
            location_id: Location ID

        Returns:
            Result: API response confirming deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Professional-Monitoring/operation/Delete%20Call%20Center
        """
        params = {}
        if location_id is not None:
            params["locationId"] = location_id
        result: Result = self.adapter.delete(
            "/cloud/json/callCenter",
            ep_params=params if params else None,
        )
        return result

    def create_call_center_test(
        self,
        location_id: int,
        start_date: str = None,
        end_date: str = None,
        comment: str = None,
    ) -> Result:
        """
        Create Call Center Test.

        Create a test period for a call center account from optional startDate to endDate.

        Args:
            location_id: Location ID (required)
            start_date: Start date for the test
            end_date: End date for the test
            comment: Comment for the test

        Returns:
            Result: API response

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Professional-Monitoring/operation/Create%20Call%20Center%20Test
        """
        params = {
            "locationId": location_id,
        }
        test_data = {
            "startDate": start_date,
            "endDate": end_date,
            "comment": comment,
        }
        test_data = {k: v for k, v in test_data.items() if v is not None}
        result: Result = self.adapter.post(
            "/cloud/json/callCenterTest",
            ep_params=params,
            ep_json=test_data if test_data else None,
        )
        return result

    def cancel_call_center_test(
        self,
        location_id: int,
        test_id: int = None,
    ) -> Result:
        """
        Cancel Call Center Test.

        Cancel a specific test or all active tests.

        Args:
            location_id: Location ID (required)
            test_id: Test ID

        Returns:
            Result: API response

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Professional-Monitoring/operation/Cancel%20Call%20Center%20Test
        """
        params = {
            "locationId": location_id,
            "testId": test_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.delete(
            "/cloud/json/callCenterTest",
            ep_params=params,
        )
        return result

    def get_call_center_alerts(
        self,
        location_id: int,
        start_date_ms: int = None,
        end_date_ms: int = None,
    ) -> Result:
        """
        Get Call Center Alerts.

        Get call center alerts for a location.

        Args:
            location_id: Location ID (required)
            start_date_ms: Start date in milliseconds
            end_date_ms: End date in milliseconds

        Returns:
            Result: API response with call center alerts

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Professional-Monitoring/operation/Get%20Call%20Center%20Alerts
        """
        params = {
            "locationId": location_id,
        }
        # Convert milliseconds to ISO date strings if provided
        if start_date_ms:
            start_date = datetime.fromtimestamp(start_date_ms / 1000).isoformat()
            params["startDate"] = start_date
        if end_date_ms:
            end_date = datetime.fromtimestamp(end_date_ms / 1000).isoformat()
            params["endDate"] = end_date
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/cloud/json/callCenterAlerts",
            ep_params=params,
        )
        return result

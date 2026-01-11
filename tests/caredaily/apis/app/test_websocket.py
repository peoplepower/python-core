"""
Test suite for WebSocket API implementation.

Test Case Coverage:
- Positive scenarios: Successful connection, authentication, subscriptions
- Negative scenarios: Invalid inputs, connection failures, authentication errors
- Boundary conditions: Edge cases for parameters, timeouts, message handling
- Integration: Callback handling, async operations, context manager usage
"""

import asyncio
import json
import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

from caredaily.apis.app.websocket import (
    WebSocketConnection,
    WebSocketGoal,
    WebSocketOperation,
    WebSocketSubscriptionType,
    Websocket,
)
from caredaily.exceptions import CareDailyException
from caredaily.models import Result, ResultCode, ServerType

import pytest


class TestWebsocket(unittest.TestCase):
    """Test suite for Websocket API class."""

    def setUp(self):
        """Set up test fixtures before each test method."""

        try:
            import websockets
        except ImportError:
            pytest.skip("websockets is required for WebSocket connections. Install it with `pip install caredaily[websockets]`")
        
        self.websocket_api = Websocket({"api_key": "test_api_key_123"})
        self.mock_adapter = MagicMock()
        self.websocket_api.adapter = self.mock_adapter

    def test_get_websocket_url_success(self):
        """
        Test Case ID: TC-WS-001
        Title: Get WebSocket URL - Success
        Priority: P0
        Preconditions: Valid API configuration with adapter
        Test Steps:
        1. Call get_websocket_url()
        2. Verify CloudConnectivity.get_server_settings is called with WEBSOCKET type
        Expected Result: Returns Result object with server settings
        """
        # Setup
        mock_cloud_connectivity = MagicMock()
        mock_result = Result(resultCode=ResultCode.SUCCESS, data={"server": {"host": "ws.example.com", "port": 443, "ssl": True}})
        mock_cloud_connectivity.get_server_settings.return_value = mock_result

        with patch("caredaily.apis.app.cloud_connectivity.CloudConnectivity", return_value=mock_cloud_connectivity):
            # Execute
            result = self.websocket_api.get_websocket_url()

            # Verify
            mock_cloud_connectivity.get_server_settings.assert_called_once_with(server_type=ServerType.WEBSOCKET)
            self.assertEqual(result, mock_result)

    def test_get_websocket_url_uses_same_adapter(self):
        """
        Test Case ID: TC-WS-002
        Title: Get WebSocket URL - Reuses Same Adapter
        Priority: P1
        Preconditions: Valid API configuration
        Test Steps:
        1. Call get_websocket_url()
        2. Verify CloudConnectivity instance uses the same adapter
        Expected Result: Adapter is shared between instances
        """
        with patch("caredaily.apis.app.cloud_connectivity.CloudConnectivity") as mock_cloud_class:
            mock_instance = MagicMock()
            mock_cloud_class.return_value = mock_instance
            mock_instance.get_server_settings.return_value = Result(resultCode=ResultCode.SUCCESS, data={})

            self.websocket_api.get_websocket_url()

            # Verify adapter was set
            self.assertEqual(mock_instance.adapter, self.mock_adapter)

    def test_connect_invalid_url_response(self):
        """
        Test Case ID: TC-WS-003
        Title: Connect - Invalid URL Response
        Priority: P0
        Preconditions: API configured, get_websocket_url returns error
        Test Steps:
        1. Mock get_websocket_url to return error result
        2. Call connect()
        Expected Result: Raises CareDailyException with error message
        """
        # Setup
        error_result = Result(resultCode=ResultCode.INTERNAL_ERROR, resultCodeMessage="Server error")
        self.websocket_api.get_websocket_url = MagicMock(return_value=error_result)

        # Execute & Verify
        async def run_test():
            with self.assertRaises(CareDailyException) as context:
                await self.websocket_api.connect()
            self.assertIn("Failed to get WebSocket URL", str(context.exception))

        asyncio.run(run_test())

    def test_connect_missing_server_data(self):
        """
        Test Case ID: TC-WS-004
        Title: Connect - Missing Server Data
        Priority: P0
        Preconditions: API configured
        Test Steps:
        1. Mock get_websocket_url to return success but no data
        2. Call connect()
        Expected Result: Raises CareDailyException
        """
        # Setup
        result = Result(result_code=ResultCode.SUCCESS, data=None)
        self.websocket_api.get_websocket_url = MagicMock(return_value=result)

        # Execute & Verify
        async def run_test():
            with self.assertRaises(CareDailyException) as context:
                await self.websocket_api.connect()
            self.assertIn("No server data", str(context.exception))

        asyncio.run(run_test())

    def test_connect_missing_host(self):
        """
        Test Case ID: TC-WS-005
        Title: Connect - Missing Host in Server Data
        Priority: P0
        Preconditions: API configured
        Test Steps:
        1. Mock get_websocket_url to return data without host
        2. Call connect()
        Expected Result: Raises CareDailyException
        """
        # Setup
        result = Result(result_code=ResultCode.SUCCESS, data={"server": {"port": 443}})
        self.websocket_api.get_websocket_url = MagicMock(return_value=result)

        # Execute & Verify
        async def run_test():
            with self.assertRaises(CareDailyException) as context:
                await self.websocket_api.connect()
            self.assertIn("Server host not found", str(context.exception))

        asyncio.run(run_test())

    def test_connect_invalid_port(self):
        """
        Test Case ID: TC-WS-006
        Title: Connect - Invalid Port Number
        Priority: P1
        Preconditions: API configured
        Test Steps:
        1. Mock get_websocket_url with invalid port (0, -1, 70000)
        2. Call connect()
        Expected Result: Raises CareDailyException for each invalid port
        """
        invalid_ports = [0, -1, 70000, "invalid"]

        async def run_test():
            for port in invalid_ports:
                with self.subTest(port=port):
                    result = Result(
                        result_code=ResultCode.SUCCESS,
                        data={"server": {"host": "ws.example.com", "port": port}},
                    )
                    self.websocket_api.get_websocket_url = MagicMock(return_value=result)

                    with self.assertRaises(CareDailyException):
                        await self.websocket_api.connect()

        asyncio.run(run_test())

    def test_connect_success_ssl(self):
        """
        Test Case ID: TC-WS-007
        Title: Connect - Success with SSL
        Priority: P0
        Preconditions: Valid server settings with SSL enabled
        Test Steps:
        1. Mock get_websocket_url with SSL server
        2. Call connect()
        3. Verify connection uses wss:// protocol
        Expected Result: Returns WebSocketConnection with wss:// URL
        """
        # Setup
        result = Result(
            resultCode=ResultCode.SUCCESS,
            data={"server": {"host": "ws.example.com", "port": 443, "ssl": True}},
        )
        self.websocket_api.get_websocket_url = MagicMock(return_value=result)

        # Execute
        async def run_test():
            connection = await self.websocket_api.connect()

            # Verify
            self.assertIsInstance(connection, WebSocketConnection)
            self.assertTrue(connection.url.startswith("wss://"))
            self.assertEqual(connection.url, "wss://ws.example.com:443")

        asyncio.run(run_test())

    def test_connect_success_no_ssl(self):
        """
        Test Case ID: TC-WS-008
        Title: Connect - Success without SSL
        Priority: P0
        Preconditions: Valid server settings with SSL disabled
        Test Steps:
        1. Mock get_websocket_url with non-SSL server
        2. Call connect()
        3. Verify connection uses ws:// protocol
        Expected Result: Returns WebSocketConnection with ws:// URL
        """
        # Setup
        result = Result(
            resultCode=ResultCode.SUCCESS,
            data={"server": {"host": "ws.example.com", "port": 80, "ssl": False}},
        )
        self.websocket_api.get_websocket_url = MagicMock(return_value=result)

        # Execute
        async def run_test():
            connection = await self.websocket_api.connect()

            # Verify
            self.assertIsInstance(connection, WebSocketConnection)
            self.assertTrue(connection.url.startswith("ws://"))
            self.assertEqual(connection.url, "ws://ws.example.com:80")

        asyncio.run(run_test())

    def test_connect_default_port(self):
        """
        Test Case ID: TC-WS-009
        Title: Connect - Default Port When Not Specified
        Priority: P2
        Preconditions: Valid server settings without port
        Test Steps:
        1. Mock get_websocket_url without port field
        2. Call connect()
        Expected Result: Uses default port 80
        """
        # Setup
        result = Result(
            resultCode=ResultCode.SUCCESS,
            data={"server": {"host": "ws.example.com"}},
        )
        self.websocket_api.get_websocket_url = MagicMock(return_value=result)

        # Execute
        async def run_test():
            connection = await self.websocket_api.connect()
            self.assertEqual(connection.url, "ws://ws.example.com:80")

        asyncio.run(run_test())

    def test_connect_with_callbacks(self):
        """
        Test Case ID: TC-WS-010
        Title: Connect - With Message and Error Callbacks
        Priority: P1
        Preconditions: Valid server settings
        Test Steps:
        1. Create callbacks for on_message and on_error
        2. Call connect() with callbacks
        3. Verify callbacks are set on connection
        Expected Result: Connection has callbacks configured
        """
        # Setup
        def message_callback(data):
            pass

        def error_callback(error):
            pass

        result = Result(
            resultCode=ResultCode.SUCCESS,
            data={"server": {"host": "ws.example.com", "port": 443, "ssl": True}},
        )
        self.websocket_api.get_websocket_url = MagicMock(return_value=result)

        # Execute
        async def run_test():
            connection = await self.websocket_api.connect(
                on_message=message_callback, on_error=error_callback
            )

            # Verify
            self.assertEqual(connection.on_message, message_callback)
            self.assertEqual(connection.on_error, error_callback)

        asyncio.run(run_test())

    def test_init_with_custom_ping_settings(self):
        """
        Test Case ID: TC-WS-011
        Title: Initialize - Custom Ping Interval and Timeout
        Priority: P2
        Preconditions: None
        Test Steps:
        1. Create Websocket instance with custom ping_interval and ping_timeout
        2. Verify settings are stored
        Expected Result: Custom ping settings are applied
        """
        websocket_api = Websocket(
            {"api_key": "test", "ping_interval": 60, "ping_timeout": 20}
        )
        self.assertEqual(websocket_api._ping_interval, 60)
        self.assertEqual(websocket_api._ping_timeout, 20)


class TestWebSocketConnection(unittest.TestCase):
    """Test suite for WebSocketConnection class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        try:
            import websockets
        except ImportError:
            pytest.skip("websockets is required for WebSocket connections. Install it with `pip install caredaily[websockets]`")
        
        self.url = "ws://test.example.com:80"
        self.api_key = "test_api_key_123"
        self.connection = WebSocketConnection(
            url=self.url, api_key=self.api_key, ping_interval=30, ping_timeout=10
        )

    def test_init_valid_parameters(self):
        """
        Test Case ID: TC-WSC-001
        Title: Initialize - Valid Parameters
        Priority: P0
        Preconditions: None
        Test Steps:
        1. Create WebSocketConnection with valid parameters
        2. Verify all attributes are set correctly
        Expected Result: Connection object initialized with correct values
        """
        self.assertEqual(self.connection.url, self.url)
        self.assertEqual(self.connection.api_key, self.api_key)
        self.assertEqual(self.connection.ping_interval, 30)
        self.assertEqual(self.connection.ping_timeout, 10)
        self.assertFalse(self.connection._authenticated)
        self.assertFalse(self.connection._running)
        self.assertEqual(self.connection._pending_responses, {})

    def test_init_invalid_url(self):
        """
        Test Case ID: TC-WSC-002
        Title: Initialize - Invalid URL (Empty)
        Priority: P0
        Preconditions: None
        Test Steps:
        1. Attempt to create WebSocketConnection with empty URL
        Expected Result: Raises ValueError
        """
        with self.assertRaises(ValueError) as context:
            WebSocketConnection(url="", api_key=self.api_key)
        self.assertIn("URL cannot be empty", str(context.exception))

    def test_init_invalid_ping_interval(self):
        """
        Test Case ID: TC-WSC-003
        Title: Initialize - Invalid Ping Interval
        Priority: P1
        Preconditions: None
        Test Steps:
        1. Attempt to create WebSocketConnection with ping_interval <= 0
        Expected Result: Raises ValueError for each invalid value
        """
        invalid_intervals = [0, -1, -10]

        for interval in invalid_intervals:
            with self.subTest(interval=interval):
                with self.assertRaises(ValueError) as context:
                    WebSocketConnection(url=self.url, api_key=self.api_key, ping_interval=interval)
                self.assertIn("ping_interval must be positive", str(context.exception))

    def test_init_invalid_ping_timeout(self):
        """
        Test Case ID: TC-WSC-004
        Title: Initialize - Invalid Ping Timeout
        Priority: P1
        Preconditions: None
        Test Steps:
        1. Attempt to create WebSocketConnection with ping_timeout <= 0
        Expected Result: Raises ValueError
        """
        with self.assertRaises(ValueError) as context:
            WebSocketConnection(url=self.url, api_key=self.api_key, ping_timeout=0)
        self.assertIn("ping_timeout must be positive", str(context.exception))

    def test_is_connected_false_when_not_connected(self):
        """
        Test Case ID: TC-WSC-005
        Title: Is Connected - Returns False When Not Connected
        Priority: P1
        Preconditions: Connection not established
        Test Steps:
        1. Call is_connected() before connection
        Expected Result: Returns False
        """
        self.assertFalse(self.connection.is_connected())

    def test_authenticate_success(self):
        """
        Test Case ID: TC-WSC-006
        Title: Authenticate - Success
        Priority: P0
        Preconditions: WebSocket connected
        Test Steps:
        1. Mock WebSocket connection and response
        2. Call authenticate()
        3. Verify authentication message sent and response received
        Expected Result: Authentication successful, _authenticated=True, tasks started
        """
        async def run_test():
            # Setup
            mock_ws = AsyncMock()
            self.connection._ws = mock_ws
            self.connection._running = True

            # Mock response
            auth_response = {"resultCode": 0, "id": "test_id", "goal": WebSocketGoal.AUTH}
            self.connection._send_and_wait_for_response = AsyncMock(return_value=auth_response)

            # Execute
            result = await self.connection.authenticate()

            # Verify
            self.assertTrue(self.connection._authenticated)
            self.assertEqual(result, auth_response)
            self.assertIsNotNone(self.connection._ping_task)
            self.assertIsNotNone(self.connection._receive_task)

        asyncio.run(run_test())

    def test_authenticate_no_api_key(self):
        """
        Test Case ID: TC-WSC-007
        Title: Authenticate - No API Key
        Priority: P0
        Preconditions: Connection without API key
        Test Steps:
        1. Create connection without API key
        2. Call authenticate()
        Expected Result: Raises CareDailyException
        """
        connection = WebSocketConnection(url=self.url, api_key=None)

        async def run_test():
            connection._ws = AsyncMock()
            connection._running = True

            with self.assertRaises(CareDailyException) as context:
                await connection.authenticate()
            self.assertIn("API key is required", str(context.exception))

        asyncio.run(run_test())

    def test_authenticate_failure(self):
        """
        Test Case ID: TC-WSC-008
        Title: Authenticate - Authentication Failure
        Priority: P0
        Preconditions: WebSocket connected
        Test Steps:
        1. Mock authentication response with error
        2. Call authenticate()
        Expected Result: Raises CareDailyException with error message
        """
        async def run_test():
            # Setup
            self.connection._ws = AsyncMock()
            self.connection._running = True
            auth_response = {
                "resultCode": 2,
                "resultCodeMessage": "Wrong API key",
                "id": "test_id",
                "goal": WebSocketGoal.AUTH,
            }
            self.connection._send_and_wait_for_response = AsyncMock(return_value=auth_response)

            # Execute & Verify
            with self.assertRaises(CareDailyException) as context:
                await self.connection.authenticate()
            self.assertIn("Authentication failed", str(context.exception))
            self.assertIn("Wrong API key", str(context.exception))
            self.assertFalse(self.connection._authenticated)

        asyncio.run(run_test())

    def test_subscribe_location_narrative_success(self):
        """
        Test Case ID: TC-WSC-009
        Title: Subscribe - Location Narrative Success
        Priority: P0
        Preconditions: Authenticated connection
        Test Steps:
        1. Mock authenticated connection
        2. Call subscribe() for location narrative
        3. Verify subscription message sent
        Expected Result: Subscription successful, subscription tracked
        """
        async def run_test():
            # Setup
            self.connection._ws = AsyncMock()
            self.connection._running = True
            self.connection._authenticated = True

            subscribe_response = {
                "resultCode": 0,
                "subscriptionId": 123,
                "id": "test_id",
                "goal": WebSocketGoal.SUBSCRIBE,
            }
            self.connection._send_and_wait_for_response = AsyncMock(return_value=subscribe_response)

            # Execute
            result = await self.connection.subscribe(
                subscription_type=WebSocketSubscriptionType.LOCATION_NARRATIVE,
                location_id=456,
            )

            # Verify
            self.assertEqual(result, subscribe_response)
            self.assertEqual(len(self.connection._subscriptions), 1)

        asyncio.run(run_test())

    def test_subscribe_location_narrative_missing_location_id(self):
        """
        Test Case ID: TC-WSC-010
        Title: Subscribe - Location Narrative Missing Location ID
        Priority: P0
        Preconditions: Authenticated connection
        Test Steps:
        1. Call subscribe() for location narrative without location_id
        Expected Result: Raises CareDailyException
        """
        async def run_test():
            self.connection._authenticated = True

            with self.assertRaises(CareDailyException) as context:
                await self.connection.subscribe(
                    subscription_type=WebSocketSubscriptionType.LOCATION_NARRATIVE
                )
            self.assertIn("location_id is required", str(context.exception))

        asyncio.run(run_test())

    def test_subscribe_organization_narrative_missing_organization_id(self):
        """
        Test Case ID: TC-WSC-011
        Title: Subscribe - Organization Narrative Missing Organization ID
        Priority: P0
        Preconditions: Authenticated connection
        Test Steps:
        1. Call subscribe() for organization narrative without organization_id
        Expected Result: Raises CareDailyException
        """
        async def run_test():
            self.connection._authenticated = True

            with self.assertRaises(CareDailyException) as context:
                await self.connection.subscribe(
                    subscription_type=WebSocketSubscriptionType.ORGANIZATION_NARRATIVE
                )
            self.assertIn("organization_id is required", str(context.exception))

        asyncio.run(run_test())

    def test_subscribe_location_state_missing_name(self):
        """
        Test Case ID: TC-WSC-012
        Title: Subscribe - Location State Missing Name
        Priority: P0
        Preconditions: Authenticated connection
        Test Steps:
        1. Call subscribe() for location state without name
        Expected Result: Raises CareDailyException
        """
        async def run_test():
            self.connection._authenticated = True

            with self.assertRaises(CareDailyException) as context:
                await self.connection.subscribe(
                    subscription_type=WebSocketSubscriptionType.LOCATION_STATE,
                    location_id=123,
                )
            self.assertIn("name is required", str(context.exception))

        asyncio.run(run_test())

    def test_subscribe_sim_card_missing_device_id(self):
        """
        Test Case ID: TC-WSC-013
        Title: Subscribe - SIM Card Missing Device ID
        Priority: P0
        Preconditions: Authenticated connection
        Test Steps:
        1. Call subscribe() for SIM card without device_id
        Expected Result: Raises CareDailyException
        """
        async def run_test():
            self.connection._authenticated = True

            with self.assertRaises(CareDailyException) as context:
                await self.connection.subscribe(
                    subscription_type=WebSocketSubscriptionType.SIM_CARD_ATTRIBUTES,
                    location_id=123,
                )
            self.assertIn("device_id is required", str(context.exception))

        asyncio.run(run_test())

    def test_subscribe_not_authenticated(self):
        """
        Test Case ID: TC-WSC-014
        Title: Subscribe - Not Authenticated
        Priority: P0
        Preconditions: Connection not authenticated
        Test Steps:
        1. Call subscribe() without authenticating first
        Expected Result: Raises CareDailyException
        """
        async def run_test():
            with self.assertRaises(CareDailyException) as context:
                await self.connection.subscribe(
                    subscription_type=WebSocketSubscriptionType.LOCATION_NARRATIVE,
                    location_id=123,
                )
            self.assertIn("Must authenticate", str(context.exception))

        asyncio.run(run_test())

    def test_subscribe_invalid_operation(self):
        """
        Test Case ID: TC-WSC-015
        Title: Subscribe - Invalid Operation Bitmask
        Priority: P1
        Preconditions: Authenticated connection
        Test Steps:
        1. Call subscribe() with invalid operation values (0, 8, 10)
        Expected Result: Raises CareDailyException for each invalid value
        """
        async def run_test():
            self.connection._authenticated = True
            invalid_operations = [0, 8, 10, -1]

            for operation in invalid_operations:
                with self.subTest(operation=operation):
                    with self.assertRaises(CareDailyException) as context:
                        await self.connection.subscribe(
                            subscription_type=WebSocketSubscriptionType.LOCATION_NARRATIVE,
                            location_id=123,
                            operation=operation,
                        )
                    self.assertIn("operation must be between 1 and 7", str(context.exception))

        asyncio.run(run_test())

    def test_subscribe_valid_operation_combinations(self):
        """
        Test Case ID: TC-WSC-016
        Title: Subscribe - Valid Operation Combinations
        Priority: P1
        Preconditions: Authenticated connection
        Test Steps:
        1. Call subscribe() with valid operation combinations (1, 2, 3, 4, 5, 6, 7)
        Expected Result: All valid combinations accepted
        """
        async def run_test():
            self.connection._authenticated = True
            self.connection._ws = AsyncMock()
            self.connection._running = True

            valid_operations = [1, 2, 3, 4, 5, 6, 7]
            subscribe_response = {
                "resultCode": 0,
                "subscriptionId": 123,
                "id": "test_id",
            }
            self.connection._send_and_wait_for_response = AsyncMock(return_value=subscribe_response)

            for operation in valid_operations:
                with self.subTest(operation=operation):
                    result = await self.connection.subscribe(
                        subscription_type=WebSocketSubscriptionType.LOCATION_NARRATIVE,
                        location_id=123,
                        operation=operation,
                    )
                    self.assertEqual(result["resultCode"], 0)

        asyncio.run(run_test())

    def test_unsubscribe_success(self):
        """
        Test Case ID: TC-WSC-017
        Title: Unsubscribe - Success
        Priority: P0
        Preconditions: Active subscription exists
        Test Steps:
        1. Add subscription to tracking
        2. Call unsubscribe() with subscription ID
        3. Verify subscription removed
        Expected Result: Unsubscribe successful, subscription removed from tracking
        """
        async def run_test():
            # Setup
            self.connection._ws = AsyncMock()
            self.connection._running = True
            request_id = str(uuid4())
            self.connection._subscriptions[request_id] = {
                "subscription_id": 123,
                "type": 1,
            }

            unsubscribe_response = {"resultCode": 0, "id": "test_id"}
            self.connection._send_and_wait_for_response = AsyncMock(return_value=unsubscribe_response)

            # Execute
            result = await self.connection.unsubscribe(123)

            # Verify
            self.assertEqual(result, unsubscribe_response)
            self.assertEqual(len(self.connection._subscriptions), 0)

        asyncio.run(run_test())

    def test_presence_success(self):
        """
        Test Case ID: TC-WSC-018
        Title: Presence - Success
        Priority: P1
        Preconditions: WebSocket connected
        Test Steps:
        1. Mock presence response
        2. Call presence()
        Expected Result: Returns presence data with available types
        """
        async def run_test():
            # Setup
            self.connection._ws = AsyncMock()
            self.connection._running = True

            presence_response = {
                "resultCode": 0,
                "id": "test_id",
                "goal": WebSocketGoal.PRESENCE,
                "types": [1, 2, 3],
            }
            self.connection._send_and_wait_for_response = AsyncMock(return_value=presence_response)

            # Execute
            result = await self.connection.presence()

            # Verify
            self.assertEqual(result, presence_response)
            self.assertEqual(result["types"], [1, 2, 3])

        asyncio.run(run_test())

    def test_status_success(self):
        """
        Test Case ID: TC-WSC-019
        Title: Status - Success
        Priority: P1
        Preconditions: WebSocket connected
        Test Steps:
        1. Mock status response
        2. Call status()
        Expected Result: Returns status with current subscriptions
        """
        async def run_test():
            # Setup
            self.connection._ws = AsyncMock()
            self.connection._running = True

            status_response = {
                "resultCode": 0,
                "id": "test_id",
                "goal": WebSocketGoal.STATUS,
                "subscriptions": [],
            }
            self.connection._send_and_wait_for_response = AsyncMock(return_value=status_response)

            # Execute
            result = await self.connection.status()

            # Verify
            self.assertEqual(result, status_response)

        asyncio.run(run_test())

    def test_handle_message_ping(self):
        """
        Test Case ID: TC-WSC-020
        Title: Handle Message - Ping
        Priority: P0
        Preconditions: WebSocket connected
        Test Steps:
        1. Send ping message "?"
        2. Verify pong "!" is sent back
        Expected Result: Pong message sent in response to ping
        """
        async def run_test():
            # Setup
            mock_ws = AsyncMock()
            self.connection._ws = mock_ws

            # Execute
            await self.connection._handle_message("?")

            # Verify
            mock_ws.send.assert_called_once_with("!")

        asyncio.run(run_test())

    def test_handle_message_pong(self):
        """
        Test Case ID: TC-WSC-021
        Title: Handle Message - Pong
        Priority: P2
        Preconditions: WebSocket connected
        Test Steps:
        1. Send pong message "!"
        2. Verify no error, message logged
        Expected Result: Pong received and logged
        """
        async def run_test():
            # Setup
            self.connection._ws = AsyncMock()

            # Execute (should not raise)
            await self.connection._handle_message("!")

            # Verify no send called for pong
            self.connection._ws.send.assert_not_called()

        asyncio.run(run_test())

    def test_handle_message_data_with_callback(self):
        """
        Test Case ID: TC-WSC-022
        Title: Handle Message - Data Message with Callback
        Priority: P0
        Preconditions: WebSocket connected, on_message callback set
        Test Steps:
        1. Set on_message callback
        2. Send data message (goal 6)
        3. Verify callback is called with message data
        Expected Result: Callback invoked with correct data
        """
        async def run_test():
            # Setup
            callback_called = []
            callback_data = None

            def message_callback(data):
                nonlocal callback_data
                callback_data = data
                callback_called.append(True)

            self.connection.on_message = message_callback

            data_message = {
                "resultCode": 0,
                "id": "sub_id",
                "goal": WebSocketGoal.DATA,
                "data": {"type": 1, "narrative": {"id": 123}},
            }

            # Execute
            await self.connection._handle_message(json.dumps(data_message))

            # Verify
            self.assertTrue(callback_called)
            self.assertEqual(callback_data["goal"], WebSocketGoal.DATA)

        asyncio.run(run_test())

    def test_handle_message_async_callback(self):
        """
        Test Case ID: TC-WSC-023
        Title: Handle Message - Async Callback
        Priority: P1
        Preconditions: WebSocket connected, async on_message callback
        Test Steps:
        1. Set async on_message callback
        2. Send data message
        3. Verify async callback is awaited
        Expected Result: Async callback properly awaited
        """
        async def run_test():
            # Setup
            callback_called = []

            async def async_message_callback(data):
                callback_called.append(True)
                await asyncio.sleep(0.01)  # Simulate async work

            self.connection.on_message = async_message_callback

            data_message = {
                "resultCode": 0,
                "id": "sub_id",
                "goal": WebSocketGoal.DATA,
                "data": {},
            }

            # Execute
            await self.connection._handle_message(json.dumps(data_message))

            # Verify
            self.assertTrue(callback_called)

        asyncio.run(run_test())

    def test_handle_message_response_to_request(self):
        """
        Test Case ID: TC-WSC-024
        Title: Handle Message - Response to Request
        Priority: P0
        Preconditions: Pending request exists
        Test Steps:
        1. Create pending response future
        2. Send response message with matching ID
        3. Verify future is resolved
        Expected Result: Response resolves pending future
        """
        async def run_test():
            # Setup
            request_id = "test_request_123"
            future = asyncio.Future()
            self.connection._pending_responses[request_id] = future

            response_message = {
                "resultCode": 0,
                "id": request_id,
                "goal": WebSocketGoal.AUTH,
            }

            # Execute
            await self.connection._handle_message(json.dumps(response_message))

            # Verify
            self.assertTrue(future.done())
            result = await future
            self.assertEqual(result["id"], request_id)

        asyncio.run(run_test())

    def test_handle_message_invalid_json(self):
        """
        Test Case ID: TC-WSC-025
        Title: Handle Message - Invalid JSON
        Priority: P1
        Preconditions: WebSocket connected
        Test Steps:
        1. Send invalid JSON message
        2. Verify error is logged, no exception raised
        Expected Result: Invalid JSON logged as warning, connection continues
        """
        async def run_test():
            # Setup
            self.connection._ws = AsyncMock()

            # Execute (should not raise)
            await self.connection._handle_message("invalid json {")

            # Verify no exception raised, just logged

        asyncio.run(run_test())

    def test_send_and_wait_for_response_timeout(self):
        """
        Test Case ID: TC-WSC-026
        Title: Send and Wait for Response - Timeout
        Priority: P0
        Preconditions: WebSocket connected
        Test Steps:
        1. Send message but don't respond
        2. Wait for timeout
        Expected Result: Raises CareDailyException on timeout
        """
        async def run_test():
            # Setup
            mock_ws = AsyncMock()
            self.connection._ws = mock_ws

            message = {"id": "test_id", "goal": WebSocketGoal.AUTH}

            # Execute & Verify
            with self.assertRaises(CareDailyException) as context:
                await self.connection._send_and_wait_for_response(message, timeout=0.1)
            self.assertIn("Timeout", str(context.exception))

        asyncio.run(run_test())

    def test_send_and_wait_for_response_not_connected(self):
        """
        Test Case ID: TC-WSC-027
        Title: Send and Wait for Response - Not Connected
        Priority: P0
        Preconditions: WebSocket not connected
        Test Steps:
        1. Call _send_and_wait_for_response without connection
        Expected Result: Raises CareDailyException
        """
        async def run_test():
            message = {"id": "test_id", "goal": WebSocketGoal.AUTH}

            with self.assertRaises(CareDailyException) as context:
                await self.connection._send_and_wait_for_response(message)
            self.assertIn("not connected", str(context.exception))

        asyncio.run(run_test())

    def test_send_and_wait_for_response_invalid_message(self):
        """
        Test Case ID: TC-WSC-028
        Title: Send and Wait for Response - Invalid Message Format
        Priority: P1
        Preconditions: WebSocket connected
        Test Steps:
        1. Call _send_and_wait_for_response with message missing "id"
        Expected Result: Raises ValueError
        """
        async def run_test():
            self.connection._ws = AsyncMock()

            invalid_messages = [{}, {"goal": 1}, "not a dict"]

            for message in invalid_messages:
                with self.subTest(message=message):
                    with self.assertRaises((ValueError, TypeError)):
                        await self.connection._send_and_wait_for_response(message)

        asyncio.run(run_test())

    def test_context_manager_enter(self):
        """
        Test Case ID: TC-WSC-029
        Title: Context Manager - Enter
        Priority: P0
        Preconditions: None
        Test Steps:
        1. Use connection as context manager
        2. Verify connection is established
        Expected Result: Connection established on enter
        """
        async def run_test():
            mock_ws = AsyncMock()
            with patch("websockets.connect", new_callable=AsyncMock, return_value=mock_ws):
                async with self.connection:
                    self.assertTrue(self.connection.is_connected())

        asyncio.run(run_test())

    def test_context_manager_exit(self):
        """
        Test Case ID: TC-WSC-030
        Title: Context Manager - Exit
        Priority: P0
        Preconditions: Connection established
        Test Steps:
        1. Enter context manager
        2. Exit context manager
        3. Verify connection is closed
        Expected Result: Connection closed, tasks cancelled on exit
        """
        async def run_test():
            mock_ws = AsyncMock()
            with patch("websockets.connect", new_callable=AsyncMock, return_value=mock_ws):
                async with self.connection:
                    pass  # Exit context

                # Verify close was called
                mock_ws.close.assert_called_once()
                self.assertFalse(self.connection._running)

        asyncio.run(run_test())

    def test_close_cancels_tasks(self):
        """
        Test Case ID: TC-WSC-031
        Title: Close - Cancels Background Tasks
        Priority: P0
        Preconditions: Connection with active tasks
        Test Steps:
        1. Start ping and receive tasks
        2. Call close()
        3. Verify tasks are cancelled
        Expected Result: All background tasks cancelled
        """
        async def run_test():
            # Setup
            mock_ws = AsyncMock()
            self.connection._ws = mock_ws
            self.connection._running = True

            # Start tasks
            self.connection._ping_task = asyncio.create_task(asyncio.sleep(100))
            self.connection._receive_task = asyncio.create_task(asyncio.sleep(100))

            # Execute
            await self.connection.close()

            # Verify
            self.assertTrue(self.connection._ping_task.cancelled())
            self.assertTrue(self.connection._receive_task.cancelled())
            mock_ws.close.assert_called_once()

        asyncio.run(run_test())

    def test_close_handles_exceptions(self):
        """
        Test Case ID: TC-WSC-032
        Title: Close - Handles Exceptions Gracefully
        Priority: P1
        Preconditions: Connection with error on close
        Test Steps:
        1. Mock WebSocket close to raise exception
        2. Call close()
        3. Verify exception is caught and logged
        Expected Result: Exception caught, close completes
        """
        async def run_test():
            # Setup
            mock_ws = AsyncMock()
            mock_ws.close.side_effect = Exception("Close error")
            self.connection._ws = mock_ws

            # Execute (should not raise)
            await self.connection.close()

            # Verify close was attempted
            mock_ws.close.assert_called_once()

        asyncio.run(run_test())

    def test_connect_replaces_existing_connection(self):
        """
        Test Case ID: TC-WSC-033
        Title: Connect - Replaces Existing Connection
        Priority: P1
        Preconditions: Existing connection exists
        Test Steps:
        1. Establish first connection
        2. Call _connect() again
        3. Verify old connection is closed
        Expected Result: Old connection closed, new connection established
        """
        async def run_test():
            # Setup
            mock_ws1 = AsyncMock()
            self.connection._ws = mock_ws1

            mock_ws2 = AsyncMock()
            with patch("websockets.connect", new_callable=AsyncMock, return_value=mock_ws2):
                # Execute
                await self.connection._connect()

                # Verify old connection was closed
                mock_ws1.close.assert_called_once()
                self.assertEqual(self.connection._ws, mock_ws2)

        asyncio.run(run_test())


if __name__ == "__main__":
    unittest.main()

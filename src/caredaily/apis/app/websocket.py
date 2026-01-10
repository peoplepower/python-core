# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "requests",
#   "websockets>=12.0",
# ]
# ///

import asyncio
import json
import logging
from enum import IntEnum
from typing import Awaitable, Callable, Dict, Optional, Union
from uuid import uuid4

from ...exceptions import CareDailyException
from ...models import Result, ResultCode, ServerType
from ..api import API


class WebSocketGoal(IntEnum):
    """WebSocket message goals."""
    AUTH = 1
    PRESENCE = 2
    SUBSCRIBE = 3
    UNSUBSCRIBE = 4
    STATUS = 5
    DATA = 6


class WebSocketSubscriptionType(IntEnum):
    """WebSocket subscription types."""
    LOCATION_NARRATIVE = 1
    ORGANIZATION_NARRATIVE = 2
    LOCATION_STATE = 3
    DEVICE_PARAMETERS = 6
    SIM_CARD_ATTRIBUTES = 8


class WebSocketOperation(IntEnum):
    """WebSocket operation types (bitmask)."""
    CREATE = 1
    UPDATE = 2
    DELETE = 4


class Websocket(API):
    """
    WebSocket API for streaming real-time data from the CareDaily platform.
    
    This class provides methods to establish websocket connections,
    authenticate, subscribe to data streams, and receive real-time updates
    for narratives, device parameters, location state, and SIM card attributes.
    
    Reference:
        https://github.com/CareDailyAI/docs/blob/main/platform_apis/websockets.md
    """

    def __init__(self, config: Dict = {}):
        super().__init__(config)
        self._logger = config.get("logger") or logging.getLogger(__name__)
        self._ping_interval = config.get("ping_interval", 30)  # seconds
        self._ping_timeout = config.get("ping_timeout", 10)  # seconds
        self._api_key = config.get("api_key")

    def get_websocket_url(self) -> Result:
        """
        Get the WebSocket server URL and connection settings.
        
        Each time the client starts a new WebSocket session, it must obtain
        its WebSocket API server connection settings by calling this method.
        
        Returns:
            Result: API response containing server host, port, SSL settings, etc.
            
        Reference:
            https://github.com/CareDailyAI/docs/blob/main/platform_apis/websockets.md#get-the-websocket-url
        """
        from ..app.cloud_connectivity import CloudConnectivity

        # Create CloudConnectivity instance with empty config to reuse the same adapter
        # The adapter is already initialized with the correct config in the base API class
        cloud_connectivity = CloudConnectivity({})
        # Replace the adapter to use the same one as this instance
        cloud_connectivity.adapter = self.adapter
        return cloud_connectivity.get_server_settings(
            server_type=ServerType.WEBSOCKET
        )

    async def connect(
        self,
        on_message: Optional[Callable[[Dict], Union[None, Awaitable[None]]]] = None,
        on_error: Optional[Callable[[Exception], Union[None, Awaitable[None]]]] = None,
    ) -> "WebSocketConnection":
        """
        Establish a WebSocket connection to the CareDaily platform.
        
        Args:
            on_message: Optional callback function called when data messages are received.
                       The function receives a dict with the message data. Can be sync or async.
            on_error: Optional callback function called when errors occur.
                     The function receives the Exception object. Can be sync or async.
        
        Returns:
            WebSocketConnection: An async context manager for the WebSocket connection.
                The connection is established automatically when entering the context manager.
                You must call authenticate() after entering the context.
            
        Example:
            ```python
            from caredaily.apis.app.websocket import WebSocketSubscriptionType
            
            async with websocket_client.connect(on_message=handle_message) as ws:
                await ws.authenticate()
                await ws.subscribe(
                    subscription_type=WebSocketSubscriptionType.LOCATION_NARRATIVE,
                    location_id=123
                )
                await asyncio.sleep(60)  # Keep connection alive
            ```
        """
        # Get WebSocket server settings
        result = self.get_websocket_url()
        if result.result_code is not None and result.result_code != ResultCode.SUCCESS:
            raise CareDailyException(
                f"Failed to get WebSocket URL: {result.result_code_message}"
            )

        server_data = result.data
        if not server_data:
            raise CareDailyException("No server data returned from get_websocket_url()")
        
        server = server_data.get("server") or server_data

        host = server.get("host")
        if not host:
            raise CareDailyException("Server host not found in WebSocket server settings")
        
        port = server.get("port", 80)
        if not isinstance(port, int) or port < 1 or port > 65535:
            raise CareDailyException(f"Invalid port number: {port}")
        
        ssl = server.get("ssl", False)
        protocol = "wss" if ssl else "ws"
        url = f"{protocol}://{host}:{port}"

        self._logger.debug(f"Connecting to WebSocket: {url}")

        # Get API key from headers if not in config
        api_key = self._api_key or self.adapter._headers.get("API_KEY")  # noqa: SLF001

        connection = WebSocketConnection(
            url=url,
            api_key=api_key,
            ping_interval=self._ping_interval,
            ping_timeout=self._ping_timeout,
            on_message=on_message,
            on_error=on_error,
            logger=self._logger,
        )

        # Connection will be established when used as context manager or manually
        return connection


class WebSocketConnection:
    """
    Represents an active WebSocket connection to the CareDaily platform.
    
    This class handles authentication, subscriptions, ping/pong, and message
    routing. It should be used as an async context manager.
    """

    PING_MESSAGE = "?"
    PONG_MESSAGE = "!"

    def __init__(
        self,
        url: str,
        api_key: Optional[str],
        ping_interval: int = 30,
        ping_timeout: int = 10,
        on_message: Optional[Callable[[Dict], Union[None, Awaitable[None]]]] = None,
        on_error: Optional[Callable[[Exception], Union[None, Awaitable[None]]]] = None,
        logger: Optional[logging.Logger] = None,
    ):
        try:
            import websockets
        except ImportError:
            raise ImportError("websockets is required for WebSocket connections. Install it with `pip install caredaily[websockets]`")
        
        if not url:
            raise ValueError("WebSocket URL cannot be empty")
        if ping_interval <= 0:
            raise ValueError("ping_interval must be positive")
        if ping_timeout <= 0:
            raise ValueError("ping_timeout must be positive")
        
        self.url = url
        self.api_key = api_key
        self.ping_interval = ping_interval
        self.ping_timeout = ping_timeout
        self.on_message = on_message
        self.on_error = on_error
        self.logger = logger or logging.getLogger(__name__)
        self._ws: Optional[websockets.WebSocketClientProtocol] = None
        self._subscriptions: Dict[str, Dict] = {}
        self._authenticated = False
        self._running = False
        self._ping_task: Optional[asyncio.Task] = None
        self._receive_task: Optional[asyncio.Task] = None
        self._pending_responses: Dict[str, asyncio.Future] = {}

    async def _call_callback(self, callback: Optional[Callable], *args):
        """
        Helper method to call a callback (sync or async) safely.
        
        Args:
            callback: The callback function to call (can be None, sync, or async)
            *args: Arguments to pass to the callback
        """
        if not callback:
            return
        
        try:
            result = callback(*args)
            # Handle async callbacks
            if asyncio.iscoroutine(result):
                await result
        except Exception as e:
            self.logger.error(f"Error in callback: {e}")

    async def _connect(self):
        """
        Internal method to establish the WebSocket connection.
        
        Raises:
            CareDailyException: If connection fails
        """
        try:
            import websockets
        except ImportError:
            raise ImportError("websockets is required for WebSocket connections. Install it with `pip install caredaily[websockets]`")
        
        if self._ws:
            self.logger.warning("WebSocket already connected, closing existing connection")
            try:
                await self._ws.close()
            except Exception:
                pass
        
        try:
            self._ws = await websockets.connect(
                self.url,
                ping_interval=None,  # We handle ping/pong manually
                close_timeout=self.ping_timeout,
            )
            self._running = True
            self.logger.debug("WebSocket connected")
        except websockets.exceptions.InvalidURI as e:
            error_msg = f"Invalid WebSocket URL: {self.url}"
            self.logger.error(error_msg)
            await self._call_callback(self.on_error, e)
            raise CareDailyException(error_msg) from e
        except Exception as e:
            error_msg = f"Failed to connect to WebSocket: {e}"
            self.logger.error(error_msg)
            await self._call_callback(self.on_error, e)
            raise CareDailyException(error_msg) from e

    async def __aenter__(self):
        """
        Async context manager entry.
        
        Establishes the WebSocket connection if not already connected.
        """
        if not self._ws or not self._running:
            await self._connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Async context manager exit.
        
        Ensures the WebSocket connection is properly closed.
        """
        await self.close()

    def is_connected(self) -> bool:
        """
        Check if the WebSocket is currently connected.
        
        Returns:
            bool: True if connected and running, False otherwise
        """
        return self._ws is not None and self._running

    async def authenticate(self) -> Dict:
        """
        Authenticate the WebSocket session using the API key.
        
        Returns:
            Dict: Authentication response with resultCode.
            
        Reference:
            https://github.com/CareDailyAI/docs/blob/main/platform_apis/websockets.md#authenticate
        """
        if not self.api_key:
            raise CareDailyException("API key is required for authentication")

        request_id = str(uuid4())
        message = {
            "goal": WebSocketGoal.AUTH,
            "id": request_id,
            "key": self.api_key,
        }

        response = await self._send_and_wait_for_response(message)
        
        if response.get("resultCode") == 0:
            self._authenticated = True
            self.logger.debug("WebSocket authenticated")
            # Start ping task and receive task after authentication
            self._ping_task = asyncio.create_task(self._ping_loop())
            self._receive_task = asyncio.create_task(self._receive_loop())
        else:
            error_msg = response.get("resultCodeMessage", "Authentication failed")
            raise CareDailyException(f"Authentication failed: {error_msg}")

        return response

    async def presence(self) -> Dict:
        """
        Check what WebSocket data subscriptions are available.
        
        Returns:
            Dict: Presence response with available subscription types.
            
        Reference:
            https://github.com/CareDailyAI/docs/blob/main/platform_apis/websockets.md#presence
        """
        request_id = str(uuid4())
        message = {
            "goal": WebSocketGoal.PRESENCE,
            "id": request_id,
        }

        return await self._send_and_wait_for_response(message)

    async def status(self) -> Dict:
        """
        Get the current status of WebSocket data subscriptions.
        
        Returns:
            Dict: Status response with current subscriptions.
            
        Reference:
            https://github.com/CareDailyAI/docs/blob/main/platform_apis/websockets.md#status
        """
        request_id = str(uuid4())
        message = {
            "goal": WebSocketGoal.STATUS,
            "id": request_id,
        }

        return await self._send_and_wait_for_response(message)

    async def subscribe(
        self,
        subscription_type: WebSocketSubscriptionType,
        operation: int = 7,  # Default: CREATE (1) + UPDATE (2) + DELETE (4)
        location_id: Optional[int] = None,
        organization_id: Optional[int] = None,
        group_id: Optional[int] = None,
        priority: Optional[int] = None,
        priority_to: Optional[int] = None,
        name: Optional[str] = None,  # For location state subscriptions
        device_id: Optional[str] = None,  # For device/SIM subscriptions
    ) -> Dict:
        """
        Subscribe to WebSocket data streams.
        
        Args:
            subscription_type: Type of subscription (use WebSocketSubscriptionType enum)
            operation: Operation bitmask (CREATE=1, UPDATE=2, DELETE=4, or combinations)
            location_id: Location ID (required for location narratives, optional for org narratives)
            organization_id: Organization ID (required for organization narratives)
            group_id: Optional group ID filter
            priority: Optional priority filter
            priority_to: Optional priority range filter
            name: Variable name for location state subscriptions (type 3)
            device_id: Device ID for device parameters (type 6) or SIM card (type 8)
        
        Returns:
            Dict: Subscription response with subscriptionId.
            
        Raises:
            CareDailyException: If required parameters are missing or invalid.
            
        Reference:
            https://github.com/CareDailyAI/docs/blob/main/platform_apis/websockets.md#subscribe
        """
        if not self._authenticated:
            raise CareDailyException("Must authenticate before subscribing")
        
        # Validate subscription type requirements
        sub_type_value = subscription_type.value if isinstance(subscription_type, WebSocketSubscriptionType) else subscription_type
        
        if sub_type_value == WebSocketSubscriptionType.LOCATION_NARRATIVE and location_id is None:
            raise CareDailyException("location_id is required for location narrative subscriptions")
        if sub_type_value == WebSocketSubscriptionType.ORGANIZATION_NARRATIVE and organization_id is None:
            raise CareDailyException("organization_id is required for organization narrative subscriptions")
        if sub_type_value == WebSocketSubscriptionType.LOCATION_STATE:
            if location_id is None:
                raise CareDailyException("location_id is required for location state subscriptions")
            if name is None:
                raise CareDailyException("name is required for location state subscriptions")
        if sub_type_value == WebSocketSubscriptionType.DEVICE_PARAMETERS and location_id is None:
            raise CareDailyException("location_id is required for device parameter subscriptions")
        if sub_type_value == WebSocketSubscriptionType.SIM_CARD_ATTRIBUTES:
            if location_id is None:
                raise CareDailyException("location_id is required for SIM card subscriptions")
            if device_id is None:
                raise CareDailyException("device_id is required for SIM card subscriptions")
        
        # Validate operation bitmask
        if operation < 1 or operation > 7:
            raise CareDailyException("operation must be between 1 and 7 (bitmask of CREATE=1, UPDATE=2, DELETE=4)")
        
        request_id = str(uuid4())
        subscription = {
            "type": sub_type_value,
            "operation": operation,
        }

        if location_id is not None:
            subscription["locationId"] = location_id
        if organization_id is not None:
            subscription["organizationId"] = organization_id
        if group_id is not None:
            subscription["groupId"] = group_id
        if priority is not None:
            subscription["priority"] = priority
        if priority_to is not None:
            subscription["priorityTo"] = priority_to
        if name is not None:
            subscription["name"] = name
        if device_id is not None:
            subscription["deviceId"] = device_id

        message = {
            "goal": WebSocketGoal.SUBSCRIBE,
            "id": request_id,
            "subscription": subscription,
        }

        response = await self._send_and_wait_for_response(message)
        
        if response.get("resultCode") == 0:
            subscription_id = response.get("subscriptionId")
            self._subscriptions[request_id] = {
                "subscription_id": subscription_id,
                **subscription,
            }
            self.logger.debug(f"Subscribed: {subscription_id}")

        return response

    async def unsubscribe(self, subscription_id: int) -> Dict:
        """
        Unsubscribe from a WebSocket data stream.
        
        Args:
            subscription_id: The subscription ID returned from subscribe().
        
        Returns:
            Dict: Unsubscribe response.
            
        Reference:
            https://github.com/CareDailyAI/docs/blob/main/platform_apis/websockets.md#unsubscribe
        """
        request_id = str(uuid4())
        message = {
            "goal": WebSocketGoal.UNSUBSCRIBE,
            "id": request_id,
            "subscription": {
                "id": subscription_id,
            },
        }

        response = await self._send_and_wait_for_response(message)
        
        # Remove subscription from tracking
        for req_id, sub in list(self._subscriptions.items()):
            if sub.get("subscription_id") == subscription_id:
                del self._subscriptions[req_id]
                break

        return response

    async def _send_and_wait_for_response(self, message: Dict, timeout: float = 10.0) -> Dict:
        """
        Send a message and wait for the corresponding response.
        
        Args:
            message: The message dict to send (must contain "id" field)
            timeout: Maximum time to wait for response in seconds
            
        Returns:
            Dict: The response message from the server
            
        Raises:
            CareDailyException: If WebSocket is not connected or timeout occurs
        """
        if not self._ws:
            raise CareDailyException("WebSocket not connected")
        
        if not isinstance(message, dict) or "id" not in message:
            raise ValueError("Message must be a dict with an 'id' field")

        request_id = message["id"]
        future = asyncio.Future()
        self._pending_responses[request_id] = future

        try:
            await self._ws.send(json.dumps(message))
            self.logger.debug(f"Sent: {message}")

            response = await asyncio.wait_for(future, timeout=timeout)
            return response
        except asyncio.TimeoutError:
            self._pending_responses.pop(request_id, None)
            raise CareDailyException(f"Timeout waiting for response to {request_id}")
        except Exception as e:
            self._pending_responses.pop(request_id, None)
            raise CareDailyException(f"Error sending message: {e}")

    async def _ping_loop(self):
        """Periodically send ping messages to keep the connection alive."""
        try:
            while self._running and self._ws:
                await asyncio.sleep(self.ping_interval)
                if self._ws and self._running:
                    try:
                        await self._ws.send(self.PING_MESSAGE)
                        self.logger.debug("Sent ping")
                    except Exception as e:
                        self.logger.error(f"Error sending ping: {e}")
                        await self._call_callback(self.on_error, e)
                        break
        except asyncio.CancelledError:
            pass
        except Exception as e:
            self.logger.error(f"Ping loop error: {e}")
            await self._call_callback(self.on_error, e)

    async def _receive_loop(self):
        """Continuously receive and process messages from the WebSocket."""
        try:
            import websockets
        except ImportError:
            raise ImportError("websockets is required for WebSocket connections. Install it with `pip install caredaily[websockets]`")
        
        try:
            while self._running and self._ws:
                try:
                    message = await asyncio.wait_for(
                        self._ws.recv(), timeout=self.ping_timeout + 5
                    )
                    await self._handle_message(message)
                except asyncio.TimeoutError:
                    # Timeout is normal, continue receiving
                    continue
                except websockets.exceptions.ConnectionClosed:
                    self.logger.warning("WebSocket connection closed")
                    break
                except Exception as e:
                    self.logger.error(f"Error receiving message: {e}")
                    await self._call_callback(self.on_error, e)
                    break
        except asyncio.CancelledError:
            pass
        except Exception as e:
            self.logger.error(f"Receive loop error: {e}")
            await self._call_callback(self.on_error, e)

    async def _handle_message(self, message: str):
        """Handle incoming WebSocket messages."""
        # Handle ping/pong
        if message == self.PING_MESSAGE:
            if self._ws:
                await self._ws.send(self.PONG_MESSAGE)
                self.logger.debug("Received ping, sent pong")
            return
        elif message == self.PONG_MESSAGE:
            self.logger.debug("Received pong")
            return

        # Handle JSON messages
        try:
            data = json.loads(message)
            self.logger.debug(f"Received: {data}")

            goal = data.get("goal")
            request_id = data.get("id")

            # Handle responses to our requests
            if request_id and request_id in self._pending_responses:
                future = self._pending_responses.pop(request_id)
                if future and not future.done():
                    future.set_result(data)
                    return

            # Handle data messages (goal 6)
            if goal == WebSocketGoal.DATA:
                if self.on_message:
                    try:
                        result = self.on_message(data)
                        # Handle async callbacks
                        if asyncio.iscoroutine(result):
                            await result
                    except Exception as e:
                        self.logger.error(f"Error in on_message callback: {e}")
                        await self._call_callback(self.on_error, e)

        except json.JSONDecodeError:
            self.logger.warning(f"Failed to parse message as JSON: {message[:100]}")

    async def close(self):
        """Close the WebSocket connection."""
        self._running = False

        if self._ping_task:
            self._ping_task.cancel()
            try:
                await self._ping_task
            except asyncio.CancelledError:
                pass

        if self._receive_task:
            self._receive_task.cancel()
            try:
                await self._receive_task
            except asyncio.CancelledError:
                pass

        if self._ws:
            try:
                await self._ws.close()
            except Exception as exc:
                self.logger.error(f"Error closing WebSocket: {exc}")

        self.logger.debug("WebSocket connection closed")
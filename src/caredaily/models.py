# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "pydantic",
# ///

from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field, ConfigDict


class ResultCode(Enum):
    # Success
    SUCCESS = 0
    # Internal error
    INTERNAL_ERROR = 1
    # Wrong API key
    WRONG_API_KEY = 2
    # Wrong device ID or device has not been found
    WRONG_DEVICE_ID = 4
    # Device proxy (gateway) has not been found
    DEVICE_PROXY_NOT_FOUND = 5
    # Object not found
    OBJECT_NOT_FOUND = 6
    # Access denied
    ACCESS_DENIED = 7
    # Wrong parameter value
    WRONG_PARAMETER_VALUE = 8
    # Missed mandatory parameter value
    MISSING_MANDATORY_PARAMETER = 9
    # No available device resources to complete operation
    NO_AVAILABLE_RESOURCES = 10
    # Not enough free files space
    NOT_ENOUGH_SPACE = 11
    # Invalid username or wrong password
    INVALID_CREDENTIALS = 12
    # Error in parsing of input data
    PARSING_ERROR = 14
    # Missing required paid service for this operation
    MISSING_REQUIRED_SERVICE = 15
    # User account is locked out
    ACCOUNT_LOCKED = 16
    # A passcode, which has been sent to the user, is required to sign in
    PASSCODE_REQUIRED = 17
    # Wrong schedule format
    WRONG_SCHEDULE_FORMAT = 18
    # Operation is temporary locked
    OPERATION_TEMPORARILY_LOCKED = 19
    # Duplicate user name
    DUPLICATE_USERNAME = 20
    # Device is offline or disconnected
    DEVICE_OFFLINE = 21
    # Device is under different location
    DEVICE_DIFFERENT_LOCATION = 22
    # Rule generation error
    RULE_GENERATION_ERROR = 23
    # The 2'nd step is required to complete the operation
    STEP_REQUIRED = 24
    # Child object found
    CHILD_OBJECT_FOUND = 25
    # Duplicate entity or property
    DUPLICATE_ENTITY = 26
    # Server is busy or overloaded and cannot complete the request in reasonable time
    SERVER_BUSY = 27
    # Requested API method not found
    API_METHOD_NOT_FOUND = 29
    # Service is temporary unavailable
    SERVICE_UNAVAILABLE = 30
    # Unknown OAuth client
    UNKNOWN_OAUTH_CLIENT = 31
    # External application error response
    EXTERNAL_APPLICATION_ERROR = 32
    # Wrong operation token
    WRONG_OPERATION_TOKEN = 33
    # Cannot modify external resources
    CANNOT_MODIFY_EXTERNAL_RESOURCE = 34
    # Wrong phone number
    WRONG_PHONE_NUMBER = 35
    # Operation canceled
    OPERATION_CANCELED = 36
    # Cannot authorize user on external resource or cloud
    CANNOT_AUTHORIZE_EXTERNAL = 37
    # Requested resource is not available
    RESOURCE_NOT_AVAILABLE = 38
    # Device not found on external cloud
    DEVICE_NOT_FOUND_CLOUD = 39
    # Request not allowed in the current state of the resource
    REQUEST_NOT_ALLOWED = 40
    # Request has not been completed. It is not an error, just nothing to do.
    NO_ACTION_REQUIRED = 41
    # Cannot connect to an external resource
    CANNOT_CONNECT_EXTERNAL_RESOURCE = 42
    # Too often API calls
    TOO_MANY_API_CALLS = 44
    # The communication channel is not authenticated
    CHANNEL_NOT_AUTHENTICATED = 45
    # The password is not strong enough
    WEAK_PASSWORD = 46


class Result(BaseModel):
    # Integer result code
    result_code: Optional[ResultCode] = Field(None, alias="resultCode")
    # Common result code description
    result_code_desc: Optional[str] = Field(None, alias="resultCodeDesc")
    # Specific and user friendly error message describing the problem
    result_code_message: Optional[str] = Field(None, alias="resultCodeMessage")
    # Current user API key expiry
    key_expire: Optional[str] = Field(None, alias="keyExpire")
    # Current user API key expiry in milliseconds
    key_expire_ms: Optional[int] = Field(None, alias="keyExpireMs")
    key_type: Optional[int] = Field(None, alias="keyType")  # Current user API key type
    # Time in milliseconds until the requested operation is locked
    lock_time: Optional[int] = Field(None, alias="lockTime")
    # Relative lock time in milliseconds from the current time
    lock_timeout: Optional[int] = Field(None, alias="lockTimeout")
    # Found child object type
    child_type: Optional[str] = Field(None, alias="childType")
    # Found child object ID's
    child_objects: Optional[List] = Field(None, alias="childObjects")
    # Sorted collection size
    collection_total_size: Optional[int] = Field(None, alias="collectionTotalSize")
    # Data object
    data: Optional[Dict] = None  # Any additional data


class APIKeyType(Enum):
    # end user
    USER = 0
    # administrator
    ADMIN = 11
    # OAuth 2.0 access token
    ACCESS_TOKEN = 13
    # OAuth 2.0 refresh token
    REFRESH_TOKEN = 14
    # service
    SERVICE = 15
    # analytic
    ANALYTIC = 16

class Runtime(Enum):
    Python3_8 = 2
    Python3_9 = 3
    Python3_10 = 4
    Python3_11 = 5
    Python3_12 = 6
    Python3_13 = 7


class ServerType(Enum):
    # restful API
    RESTFUL = "appapi"
    # websockets API
    WEBSOCKET = "wsapi"
    # device IO API
    DEVICEIO = "deviceio"
    # MQTT
    MQTT = "mqtt"
    # streaming API
    STREAMING = "streaming"
    # web UI app
    WEBAPP = "webapp"

class SignatureAlgorithm(Enum):
    # The RSA signature algorithm, which does not use a digesting algorithm before performing the RSA operation.
    NONEwithRSA = "NONEwithRSA"
    # The MD2/MD5 with RSA Encryption signature algorithm, which uses the MD2/MD5 digest algorithm and RSA to create and verify RSA digital signatures
    MD2withRSA = "MD2withRSA"
    MD5withRSA = "MD5withRSA"	
    # The signature algorithm with SHA-* and the RSA encryption algorithm
    SHA1withRSA = "SHA1withRSA"
    SHA224withRSA = "SHA224withRSA"
    SHA256withRSA = "SHA256withRSA"
    SHA384withRSA = "SHA384withRSA"
    SHA512withRSA = "SHA512withRSA"	

class Server(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    # Server Type
    type: Optional[ServerType] = None
    # Server Host
    host: Optional[str] = None
    # Default Port
    port: Optional[int] = None
    # SSL flag
    ssl: Optional[bool] = None
    # Server brand	For web UI apps
    brand: Optional[str] = None
    # Server version	Optional
    version: Optional[int] = None
    # TLS version	Optional
    tlsversion: Optional[int] = None


class MQTT(BaseModel):
    cacrt: Optional[str] = None
    crt: Optional[str] = None
    key: Optional[str] = None
    client_id: Optional[str] = Field(None, alias="clientId")
    qos: Optional[int] = None
    topic_prefix: Optional[str] = Field(None, alias="topicPrefix")


class TimeZone(BaseModel):
    # Daylight saving time flag
    dst: Optional[bool] = None
    # Timezone ID
    id: Optional[str] = None
    # Timezone name
    name: Optional[str] = None
    # Timezone offset
    offset: Optional[int] = None


class Cloud(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    # Current server time
    current_time: Optional[str] = Field(None, alias="currentTime")
    # Current server time in milliseconds
    current_time_ms: Optional[int] = Field(None, alias="currentTimeMs")
    # Default timezone
    default_timezone: Optional[TimeZone] = Field(None, alias="defaultTimezone")
    # Cloud name
    name: Optional[str] = None
    # List of servers
    servers: Optional[List[Server]] = Field(None, alias="servers")
    # Type of cloud
    type: Optional[int] = None
    # Cloud version
    version: Optional[int] = None

class PythonRuntime(Enum):
    PYTHON_3_8 = 2
    PYTHON_3_9 = 3
    PYTHON_3_10 = 4
    PYTHON_3_11 = 5
    PYTHON_3_12 = 6
    PYTHON_3_13 = 7
    # PYTHON_3_14 = 8
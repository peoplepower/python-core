# CareDaily APIs

This directory contains Python client implementations for interfacing with the CareDaily cloud platform APIs. The APIs are organized by functional domain and provide comprehensive access to authentication, device management, user accounts, administrative functions, bot development, and service integrations.

## Directory Structure

```
src/caredaily/apis/
├── api.py                 # Base API class with RestAdapter
├── __init__.py            # Public API exports
├── app/                   # Application-level APIs
├── admin/                 # Administrative APIs (require admin privileges)
└── bot/                   # Bot development and marketplace APIs
```

## Available APIs

### Application APIs (`app/`)

Application-level APIs for standard user operations:

- **AppFiles** - Application file management
- **Authentication** - User authentication and session management
- **CloudConnectivity** - Cloud connectivity operations
- **CloudsIntegration** - Multi-cloud integration management
- **Community** - Community features
- **DeviceFiles** - Device file management
- **DeviceMeasurements** - Device measurement data access
- **Devices** - Device management and control
- **DeviceTypesAndParameters** - Device type definitions and parameters
- **EnergyManagement** - Energy monitoring and management
- **Locations** - Location management
- **PaidServices** - Paid service subscriptions
- **ProfessionalMonitoring** - Professional monitoring services
- **RAG** - Retrieval-Augmented Generation APIs
- **Rules** - Rule engine and automation
- **SystemAndUserProperties** - System and user property management
- **UserAccounts** - User account management
- **UserCommunication** - User messaging and communication
- **Weather** - Weather data integration
- **Websocket** - WebSocket connections and real-time updates

### Administrative APIs (`admin/`)

Administrative APIs requiring admin privileges:

- **Billing** - Billing and subscription management
- **Challenges** - Challenge management
- **Devices** (AdminDevices) - Administrative device management
- **Firmware** - Firmware management and updates
- **Groups** - Organization group management
- **Locations** (AdminLocations) - Administrative location management
- **Narratives** - Narrative management
- **Organizations** - Organization management
- **Reports** - Report generation and access
- **System** - System administration
- **Tags** (AdminTags) - Tag management
- **UserGroups** - User group management
- **Users** - User administration

### Bot APIs (`bot/`)

Bot development and marketplace APIs:

- **Analytic** - Bot analytics and metrics
- **BotDeveloper** - Bot development tools
- **BotStore** - Bot marketplace and store operations
- **DeveloperTeams** - Developer team management
- **Execution** - Bot execution and runtime APIs

## Architecture Overview

### Base API Class

All API classes inherit from the `API` base class (src/caredaily/apis/api.py:13), which provides:

- **RestAdapter**: HTTP client wrapper for making API requests
- **Configuration**: Centralized configuration for hostname, API keys, SSL, and proxies
- **Authentication**: Automatic header management for API keys

```python
from caredaily.apis import API

# Initialize with configuration
config = {
    "hostname": "https://app.peoplepowerco.com",
    "api_key": "your-api-key-here",
    "key_type": "user",  # or "admin", "device"
    "ssl_verify": True,
    "proxies": None,
    "logger": None,
}

api = API(config)
```

## API Response Format

All API methods return a `Result` object with the following structure:

```python
class Result:
    result_code: Optional[ResultCode]       # Integer result code
    result_code_desc: Optional[str]         # Common result code description
    result_code_message: Optional[str]      # Specific and user friendly error message describing the problem
    key_expire: Optional[str]               # Current user API key expiry
    key_expire_ms: Optional[int]            # Current user API key expiry in milliseconds
    key_type: Optional[int]                 # Current user API key type
    lock_time: Optional[int]                # Time in milliseconds until the requested operation is locked
    lock_timeout: Optional[int]             # Relative lock time in milliseconds from the current time
    child_type: Optional[str]               # Found child object type
    child_objects: Optional[List]           # Found child object ID's
    collection_total_size: Optional[int]    # Sorted collection size
    data: Optional[Dict]                    # Data object
```

## Documentation References

Each API method includes a reference link to the official documentation:

```python
def login_by_username(self, username: str, password: str = None, ...):
    """
    Login with username and password to obtain an API key.

    Reference:
        https://app.peoplepowerco.com/cloud/apidocs/cloud.html#login-by-username
    """
```

## Testing and Development

### Running Examples

See individual API files for comprehensive method documentation and parameter details. Each method includes:
- Parameter descriptions with types
- Return value documentation
- Reference links to official API documentation
- Implementation examples in docstrings

## Best Practices for Agents

1. **Initialize Once**: Create API instances with configuration and reuse them
2. **Handle Errors**: Always check `result.result_code` before accessing `result.data`
3. **Secure Credentials**: Never hardcode API keys or passwords
4. **Use Type Hints**: Leverage Python type hints for better IDE support
5. **Check Permissions**: Ensure API key has appropriate permissions for operations
6. **Follow REST Conventions**: Use appropriate HTTP methods (GET, POST, PUT, DELETE)
7. **Cache When Possible**: Cache location IDs, device IDs, and other stable data
8. **Rate Limiting**: Be mindful of API rate limits in production

## Support and Additional Resources

- Official API Documentation: 
    - Cloud APIs:
        - [html](https://app.peoplepowerco.com/cloud/apidocs/cloud.html)
        - [yaml](https://app.peoplepowerco.com/cloud/apidocs/yaml/cloud.yaml)
    - Admin APIs:
        - [html](https://app.peoplepowerco.com/cloud/apidocs/admin.html)
        - [yaml](https://app.peoplepowerco.com/cloud/apidocs/yaml/admin.yaml)
    - Bot APIs:
        - [html](https://app.peoplepowerco.com/cloud/apidocs/bots.html)
        - [yaml](https://app.peoplepowerco.com/cloud/apidocs/yaml/bots.yaml)
- Model Definitions: `src/caredaily/models.py`
- HTTP Adapter: `src/caredaily/http.py`

## Contributing

When adding new API methods:
1. Inherit from the `API` base class
2. Use type hints for all parameters and return values
3. Document all parameters in docstrings
4. Include reference links to official documentation
5. Filter out `None` values from parameter dictionaries
6. Return the `Result` object from the adapter call 

Example template:

```python
def new_method(
    self,
    required_param: str,
    optional_param: int = None,
    optional_json: dict = None,
    optional_data = None,
    optional_headers: dict = None,
):
    """
    Brief description of what this method does.

    Args:
        required_param: Description of required parameter
        optional_param: Description of optional parameter
        optional_json: Description of optional json data
        optional_data: Description of optional data
        optional_header: Description of optional headers

    Returns:
        Result: API response with result data

    Reference:
        https://app.peoplepowerco.com/cloud/apidocs/path#anchor
    """
    params = {
        "requiredParam": required_param,
        "optionalParam": optional_param,
    }
    params = {k: v for k, v in params.items() if v is not None}
    result: Result = self.adapter.get(
        "/espapi/cloud/json/endpoint",
        ep_params=params,
        ep_json=json.dumps(optional_json) if optional_json else None,
        ep_data=optional_data if optional_data else None,
        ep_headers=optional_headers if optional_headers else None,
    )
    return result
```

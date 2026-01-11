# Integration Testing Guide

This document describes how to set up and run integration tests for the `caredaily` Python SDK.

## Overview

Integration tests verify that the SDK works correctly with the live CareDaily API. Unlike unit tests (which mock API responses), integration tests make actual HTTP requests to the API and require valid API keys.

## Prerequisites

To run integration tests, you need:

1. **Valid API Keys**: At least one of the following:
   - App API key (`CAREDAILY_API_KEY`)
   - Admin API key (`CAREDAILY_ADMIN_KEY`)

2. **Configuration**: Properly configured CareDaily credentials and configuration files (see [Configuration](#configuration) section)

3. **Network Access**: Ability to connect to the CareDaily API hostname

## Configuration

### Environment Variables

Integration tests use environment variables to configure API keys and settings:

```bash
# Required: At least one API key
export CAREDAILY_API_KEY="your-app-api-key"
export CAREDAILY_ADMIN_KEY="your-admin-api-key"  # Optional

# Optional: Profile and hostname configuration
export CAREDAILY_PROFILE="profile-name"          # Use specific profile
export CAREDAILY_HOSTNAME="api.example.com"      # Override hostname
```

### Configuration Files

The SDK also supports configuration via files in `~/.caredaily/`:

- `~/.caredaily/config`: Contains hostname, SSL settings, and other configuration
- `~/.caredaily/credentials`: Contains API keys and key types

See the main README.md for detailed configuration instructions.

## Running Integration Tests

### Run All Integration Tests

```bash
# Run all integration tests (skipped if no API keys found)
pytest tests/integration/ -v -m integration

# Run with markers for specific API key types
pytest tests/integration/ -v -m "integration and requires_api_key"
pytest tests/integration/ -v -m "integration and requires_admin_key"
```

### Run Specific Test Files

```bash
# Test App APIs only
pytest tests/integration/test_app_apis.py -v

# Test Admin APIs only
pytest tests/integration/test_admin_apis.py -v

# Test Bot APIs only
pytest tests/integration/test_bot_apis.py -v

# Test CLI commands
pytest tests/integration/test_cli_live.py -v
```

### Skip Integration Tests

Integration tests are automatically skipped if:
- No API keys are found in environment variables or configuration
- Client initialization fails due to configuration errors

To exclude integration tests from a test run:

```bash
# Run unit tests only (exclude integration)
pytest tests/ -v -m "not integration"
```

## Test Organization

Integration tests are organized by API category:

- **`test_app_apis.py`**: Tests for App API endpoints (requires App API key)
  - Cloud Connectivity: `check_availability()`, `get_version()`, `get_cloud_settings()`
  - Authentication: `logout()`, `get_totp_factors()`
  - User Information: `get_user_information()`
  - Devices: `get_devices()`, `get_device_types()`

- **`test_admin_apis.py`**: Tests for Admin API endpoints (requires Admin API key)
  - System: `get_system_status()`
  - Organizations: `get_organizations()`, `get_organization_totals()`, `get_brands()`

- **`test_bot_apis.py`**: Tests for Bot API endpoints (requires App API key)
  - Basic smoke tests to verify bot key configuration

- **`test_cli_live.py`**: Tests for CLI commands
  - `caredaily ping`
  - `caredaily cloud-connectivity --check-availability`
  - `caredaily cloud-connectivity --version`
  - Help command

## Test Design Principles

### Read-Only Operations

Integration tests focus on **read-only operations** that don't modify data:

- ✅ `get_*` methods that retrieve data
- ✅ `check_availability()` and status checks
- ✅ Information queries

- ❌ `create_*`, `update_*`, `delete_*` methods (avoid modifying production data)

### Error Handling

Tests handle various error scenarios:

- **Network errors**: Connection failures, timeouts
- **Authentication errors**: Invalid API keys, expired tokens
- **API errors**: Server errors, rate limiting
- **Configuration errors**: Missing or invalid configuration

### Test Isolation

Each test is independent and doesn't rely on data created by other tests. Tests use:

- Read-only operations
- No shared state between tests
- Proper cleanup (where needed)

## Pytest Markers

Integration tests use several pytest markers:

- **`@pytest.mark.integration`**: Marks a test as an integration test
- **`@pytest.mark.network`**: Marks tests that make network calls
- **`@pytest.mark.requires_api_key`**: Requires App API key
- **`@pytest.mark.requires_admin_key`**: Requires Admin API key

Use markers to filter tests:

```bash
# Run only tests that require API key
pytest -m "integration and requires_api_key" -v

# Run all network tests
pytest -m network -v

# Skip integration tests in CI/CD (unless keys available)
pytest -m "not integration" -v
```

## Fixtures

The `conftest.py` file provides several fixtures:

### `live_client`

Creates a `CareDaily` client instance using environment variables or configuration files:

```python
def test_example(live_client):
    api = live_client.app_api(CloudConnectivity)
    result = api.check_availability()
    assert result is not None
```

### `has_api_key`, `has_admin_key`

Boolean fixtures indicating whether specific API keys are available:

```python
def test_example(live_client, has_api_key):
    if not has_api_key:
        pytest.skip("App API key not available")
    # ... test code
```

## Troubleshooting

### Tests Are Skipped

If tests are skipped with "No API keys found":

1. Check environment variables: `echo $CAREDAILY_API_KEY`
2. Verify configuration files exist: `ls ~/.caredaily/`
3. Check credentials file format: `cat ~/.caredaily/credentials`

### Configuration Errors

If you see "Configuration file is missing 'default' section":

1. Ensure `~/.caredaily/config` exists and has a `[default]` section
2. Ensure `~/.caredaily/credentials` exists and has a `[default]` section
3. Check file permissions: `ls -la ~/.caredaily/`

### Network Errors

If you see connection errors:

1. Verify network connectivity: `ping api.peoplepowerco.com`
2. Check hostname in configuration
3. Verify SSL settings (`ssl_verify` in config file)
4. Check for firewall or proxy issues

### Authentication Errors

If API calls return authentication errors:

1. Verify API key is valid and not expired
2. Check key type matches the API being called (App/Admin/Bot)
3. Ensure key has necessary permissions for the operations being tested

## Best Practices

1. **Use Read-Only Operations**: Avoid modifying production data in tests
2. **Test Critical Paths**: Focus on high-value endpoints used by most users
3. **Handle Errors Gracefully**: Tests should handle network issues, authentication failures, etc.
4. **Document Test Requirements**: Use docstrings and markers to clarify what each test needs
5. **Keep Tests Fast**: Integration tests are slower than unit tests; keep them focused
6. **Skip When Appropriate**: Don't fail the test suite if API keys aren't available

## CI/CD Integration

In CI/CD pipelines:

1. **Optional Integration Tests**: Mark integration tests as optional/allowed to fail if API keys aren't available
2. **Secret Management**: Store API keys securely (e.g., GitHub Secrets, environment variables)
3. **Conditional Execution**: Only run integration tests on specific branches or with explicit flags
4. **Test Isolation**: Use separate test accounts/keys to avoid affecting production

Example GitHub Actions workflow:

```yaml
- name: Run Integration Tests
  if: env.CAREDAILY_API_KEY != ''
  env:
    CAREDAILY_API_KEY: ${{ secrets.CAREDAILY_API_KEY }}
  run: pytest tests/integration/ -v -m integration
  continue-on-error: true  # Don't fail build if integration tests fail
```

## Contributing

When adding new integration tests:

1. Use appropriate markers (`@pytest.mark.integration`, `@pytest.mark.network`)
2. Add skip conditions for missing API keys
3. Focus on read-only operations
4. Include clear docstrings explaining what is being tested
5. Handle errors gracefully with appropriate assertions or skips
6. Update this documentation if adding new test categories or patterns

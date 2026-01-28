"""Pytest configuration and fixtures for integration tests.

This module provides fixtures and configuration for integration tests
that require live API keys and make actual API calls.
"""
import os
import shutil
from pathlib import Path
import tempfile
from typing import Optional

import pytest
from dotenv import load_dotenv

from caredaily import CareDaily
from caredaily.models import APIKeyType
from caredaily.exceptions import CareDailyException

# Load environment variables from .env file in the project root
# This allows tests to use API keys from .env without exporting them
project_root = Path(__file__).parent.parent 
env_file = project_root / ".test_env"
if env_file.exists():
    load_dotenv(env_file)

_TEMP_HOME: Optional[str] = None


def _write_test_config(temp_home: str) -> None:
    """Write ~/.caredaily/config and ~/.caredaily/credentials under temp_home."""
    api_key = os.environ.get("CAREDAILY_API_KEY") or ""
    admin_key = os.environ.get("CAREDAILY_ADMIN_KEY")
    hostname = os.environ.get("CAREDAILY_HOSTNAME") or "app.peoplepowerco.com"

    caredaily_dir = os.path.join(temp_home, ".caredaily")
    os.makedirs(caredaily_dir, exist_ok=True)

    config_path = os.path.join(caredaily_dir, "config")
    credentials_path = os.path.join(caredaily_dir, "credentials")

    # CareDaily expects:
    # - config profiles named: [profile <name>]
    # - credentials profiles named: [<name>]
    with open(config_path, "w") as f:
        f.write(
            "[default]\n"
            f"hostname = {hostname}\n"
            "ssl_verify = true\n"
            "proxies = \n"
            f"core_path = {temp_home}\n"
            f"private_path = {temp_home}\n"
            "\n"
        )
        if admin_key:
            f.write(
                "[profile admin]\n"
                f"hostname = {hostname}\n"
                "ssl_verify = true\n"
                "proxies = \n"
                f"core_path = {temp_home}\n"
                f"private_path = {temp_home}\n"
                "\n"
            )

    with open(credentials_path, "w") as f:
        f.write(
            "[default]\n"
            f"key = {api_key}\n"
            "key_expire_ms = \n"
            f"key_type = {APIKeyType.USER.value}\n"
            "\n"
        )
        if admin_key:
            f.write(
                "[admin]\n"
                f"key = {admin_key}\n"
                "key_expire_ms = \n"
                f"key_type = {APIKeyType.ADMIN.value}\n"
                "\n"
            )


def pytest_sessionstart(session):
    """Create a temp HOME/UserProfile before any tests run."""
    global _TEMP_HOME

    # Create under project root to avoid permission issues.
    base_dir = str(project_root)
    _TEMP_HOME = tempfile.mkdtemp(prefix=".integration_test_", dir=base_dir)

    os.environ["CAREDAILY_INTEGRATION_PATH"] = _TEMP_HOME
    _write_test_config(_TEMP_HOME)

def pytest_sessionfinish(session, exitstatus):
    """Clean up the temp HOME/UserProfile after all tests run."""
    global _TEMP_HOME
    if _TEMP_HOME:
        shutil.rmtree(_TEMP_HOME)


def pytest_configure(config):
    """Register custom markers for integration tests."""
    config.addinivalue_line("markers", "integration: marks tests as integration tests (requires live API keys)")
    config.addinivalue_line("markers", "requires_api_key: marks tests that require App API key")
    config.addinivalue_line("markers", "requires_admin_key: marks tests that require Admin API key")
    config.addinivalue_line("markers", "network: marks tests that make network calls (may fail due to network issues)")


@pytest.fixture(scope="session")
def app_client():
    """Create a CareDaily client instance configured for App API operations.
    
    This fixture uses the default profile which contains the App API key.
    Use this fixture for tests that need to call App API endpoints.
    
    Returns:
        CareDaily: Configured client instance with App API key
        
    Raises:
        pytest.skip: If App API key is not available or configuration fails
    """
    # return CareDaily(raise_errors=True)
    try:
        return CareDaily(raise_errors=True)
    except CareDailyException as e:
        pytest.skip(f"Failed to create App API client: {e}")
    except Exception as e:
        pytest.skip(f"Failed to create App API client (unexpected error): {e}")


@pytest.fixture(scope="session")
def admin_client():
    """Create a CareDaily client instance configured for Admin API operations.
    
    This fixture uses the 'admin' profile which contains the Admin API key.
    Use this fixture for tests that need to call Admin API endpoints.
    
    Returns:
        CareDaily: Configured client instance with Admin API key
        
    Raises:
        pytest.skip: If Admin API key is not available or configuration fails
    """
    # return CareDaily(profile="admin", raise_errors=True)
    try:
        return CareDaily(profile="admin", raise_errors=True)
    except CareDailyException as e:
        pytest.skip(f"Failed to create Admin API client: {e}")
    except Exception as e:
        pytest.skip(f"Failed to create Admin API client (unexpected error): {e}")


@pytest.fixture(scope="session")
def has_api_key():
    """Check if App API key is available."""
    return os.environ.get("CAREDAILY_API_KEY") is not None


@pytest.fixture(scope="session")
def has_admin_key():
    """Check if Admin API key is available."""
    return os.environ.get("CAREDAILY_ADMIN_KEY") is not None


def handle_network_error(test_func):
    """Decorator to handle network errors gracefully in integration tests.
    
    This decorator catches network-related exceptions and provides
    meaningful error messages for debugging.
    """
    def wrapper(*args, **kwargs):
        try:
            return test_func(*args, **kwargs)
        except ConnectionError as e:
            pytest.skip(f"Network connection error: {e}. Check your internet connection and API hostname.")
        except TimeoutError as e:
            pytest.skip(f"Request timeout: {e}. The API may be slow or unavailable.")
        except CareDailyException as e:
            # Re-raise CareDaily exceptions as they contain useful error information
            raise
        except Exception as e:
            # For other exceptions, fail the test but provide context
            pytest.fail(f"Unexpected error during integration test: {e}")
    return wrapper

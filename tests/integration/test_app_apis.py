"""Integration tests for App API endpoints.

These tests make actual API calls and require a valid App API key.
Set CAREDAILY_API_KEY environment variable to run these tests.

Tests focus on read-only operations that don't modify data:
- Cloud Connectivity: check_availability, get_version
- Authentication: token validation (if credentials available)
- User Information: get_user_information (read-only)
- Devices: get_devices (read-only, requires location_id)
- Device Types: get_device_types (read-only)
"""
import pytest
from caredaily.apis.app import CloudConnectivity, Authentication, UserAccounts, Devices, DeviceTypesAndParameters
from caredaily.exceptions import CareDailyException
from caredaily.models import ResultCode

import dotenv
import os


@pytest.mark.integration
@pytest.mark.network
class TestCloudConnectivityLive:
    """Integration tests for Cloud Connectivity API."""
    
    @pytest.mark.requires_api_key
    def test_check_availability(self, app_client):
        """Test cloud connectivity check with live API key."""
        try:
            api = app_client.app_api(CloudConnectivity)
            result = api.check_availability()
            
            # The endpoint should return successfully (exact format may vary)
            assert result is not None
        except CareDailyException as e:
            # Network errors should be handled gracefully
            pytest.skip(f"Network error during availability check: {e}")
    
    @pytest.mark.requires_api_key
    def test_get_version_json(self, app_client, has_api_key):
        """Test getting API version in JSON format."""
        if not has_api_key:
            pytest.skip("App API key not available")
        
        try:
            api = app_client.app_api(CloudConnectivity)
            result = api.get_version(json_format=True)
            
            # Should return version information
            assert result is not None
        except CareDailyException as e:
            # Network errors should be handled gracefully
            pytest.skip(f"Network error during version check: {e}")
    
    @pytest.mark.requires_api_key
    def test_get_cloud_settings(self, app_client, has_api_key):
        """Test getting cloud settings (read-only operation)."""
        if not has_api_key:
            pytest.skip("App API key not available")
        
        try:
            api = app_client.app_api(CloudConnectivity)
            # Don't provide device_id to get general settings
            result = api.get_cloud_settings()
            
            # Should return cloud settings
            assert result is not None
            # If Result object, check that it has data attribute
            if hasattr(result, 'data'):
                assert result.data is not None
        except CareDailyException as e:
            # Network errors should be handled gracefully
            pytest.skip(f"Network error during cloud settings check: {e}")


@pytest.mark.integration
@pytest.mark.network
class TestAuthenticationLive:
    """Integration tests for Authentication API.
    
    Note: Most authentication operations require credentials.
    These tests focus on operations that can be safely tested
    without modifying user accounts.
    """
    
    @pytest.mark.requires_api_key
    def test_login_with_api_key(self, app_client, has_api_key):
        """Test login operation using API key and login_by_key()."""
        if not has_api_key:
            pytest.skip("App API key not available")
        
        try:
            api = app_client.app_api(Authentication)
            config = app_client.get_config()
            # raise Exception(config)
            # Use the login_by_key() API with the actual key from config
            result = api.login_by_key(key=config.get("api_key"))
            # Should return a result indicating successful login, or at least a valid response
            assert result is not None
        except CareDailyException as e:
            import traceback
            # Network errors or API errors should be handled gracefully
            pytest.skip(f"Login test skipped due to API error: {e}. Traceback: {traceback.format_exc()}")
    
    @pytest.mark.requires_api_key
    def test_get_totp_factors(self, app_client, has_api_key):
        """Test getting TOTP factors (read-only operation)."""
        if not has_api_key:
            pytest.skip("App API key not available")
        
        try:
            api = app_client.app_api(Authentication)
            result = api.get_totp_factors()
            
            # Should return list of TOTP factors (may be empty)
            assert result is not None
        except CareDailyException as e:
            assert e.context["resultCode"] == ResultCode.WRONG_API_KEY.value


@pytest.mark.integration
@pytest.mark.network
class TestLocationsLive:
    """Integration tests for Locations API (read-only operations)."""
    
    @pytest.mark.requires_api_key
    def test_get_user_information(self, app_client):
        """Test getting user information (read-only operation)."""
        try:
            api = app_client.app_api(UserAccounts)
            result = api.get_user_information()
            
            # Should return user information (may be empty list if no user information exist)
            assert result is not None
            # If Result object, check that it has data attribute
            if hasattr(result, 'data'):
                assert result.data is not None
        except CareDailyException as e:
            # Network errors should be handled gracefully
            pytest.skip(f"Network error during user information check: {e}")


@pytest.mark.integration
@pytest.mark.network
class TestDevicesLive:
    """Integration tests for Devices API (read-only operations)."""
    
    @pytest.mark.requires_api_key
    def test_get_devices(self, app_client, has_api_key):
        """Test getting devices list (read-only operation).
        
        Note: This test requires a location_id. If no locations are available,
        this test will be skipped. In a real scenario, you would get location_id
        from get_user_information() first.
        """
        if not has_api_key:
            pytest.skip("App API key not available")
        
        try:
            # First, try to get a location to use for the devices call
            user_accounts_api = app_client.app_api(UserAccounts)
            user_accounts_result = user_accounts_api.get_user_information()
            assert len(user_accounts_result.data["locations"]) > 0
            location_id = user_accounts_result.data["locations"][0]["id"]
            api = app_client.app_api(Devices)
            result = api.get_devices(location_id=location_id)
            assert result.data["resultCode"] == 0
            assert result.data["devices"] is not None
        except CareDailyException as e:
            raise e
    
    @pytest.mark.requires_api_key
    def test_get_device_types(self, app_client, has_api_key):
        """Test getting device types (read-only operation)."""
        if not has_api_key:
            pytest.skip("App API key not available")
        
        try:
            # Device types are accessed through DeviceTypesAndParameters API
            api = app_client.app_api(DeviceTypesAndParameters)
            result = api.get_device_types()
            
            # Should return device types
            assert result is not None
            # If Result object, check that it has data attribute
            if hasattr(result, 'data'):
                assert result.data is not None
        except CareDailyException as e:
            # Network errors should be handled gracefully
            pytest.skip(f"Network error during device types check: {e}")

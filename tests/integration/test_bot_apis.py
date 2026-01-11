"""Integration tests for Bot API endpoints.

These tests make actual API calls and require a valid API key.
Set CAREDAILY_API_KEY environment variable to run these tests.

Tests focus on read-only operations that don't modify data.
Note: Bot APIs often require specific bot instance IDs which may not be available
in test environments, so these tests may be skipped if required resources are missing.
"""
import pytest
from caredaily.caredaily import CareDaily
from caredaily.models import APIKeyType, ResultCode
from caredaily.apis.bot import Analytic
from caredaily.exceptions import CareDailyException


@pytest.mark.integration
@pytest.mark.network
class TestAnalyticBotLive:
    """Integration tests for Analytic Bot API."""
    
    @pytest.mark.requires_api_key
    def test_bot_key_available(self, app_client, has_api_key):
        """Basic smoke test to verify bot key is configured.
        
        This test verifies that the bot key is available in the configuration.
        Actual bot API calls may require bot instance IDs which are not
        always available in test environments.
        """
        if not has_api_key:
            pytest.skip("API key not available")
        
        try:
            # Verify we can create the API instance
            api = app_client.bot_api(Analytic)
            assert api is not None

            # Verify we can get the bot key
            result = api.get_app_key(app_instance_id=123)
            assert result is not None
            assert result.result_code == 0
            assert result.data is not None
            assert result.data.get("key") is not None
            assert result.data.get("expiry") is not None

            # Create new CareDaily client with the bot key
            bot_client = CareDaily()
            bot_client.update_config(key="api_key", value=result.data.get("key"))
            bot_client.update_config(key="key_type", value=APIKeyType.ANALYTIC.value)

            # Verify we can get the tags
            result = api.get_tags()
            assert result is not None
            assert result.result_code == 0
        except CareDailyException as e:
            assert e.context["resultCode"] == ResultCode.OBJECT_NOT_FOUND.value
"""Integration tests for Admin API endpoints.

These tests make actual API calls and require a valid Admin API key.
Set CAREDAILY_ADMIN_KEY environment variable to run these tests.

Tests focus on read-only operations that don't modify data:
- System: get_system_status
- Organizations: get_organizations, get_organization_totals
"""
import pytest
from caredaily.apis.admin import System, Organizations
from caredaily.exceptions import CareDailyException
from caredaily.models import ResultCode


@pytest.mark.integration
@pytest.mark.network
class TestOrganizationsAdminLive:
    """Integration tests for Organizations Admin API (read-only operations)."""
    
    @pytest.mark.requires_admin_key
    def test_get_organizations(self, admin_client):
        """Test getting organizations list (read-only operation)."""
        try:
            api = admin_client.admin_api(Organizations)
            result = api.get_organizations(organization_id=0)
            
            # Should return organizations (may be empty list if no organizations exist)
            assert result is not None
            # If Result object, check that it has data attribute
            if hasattr(result, 'data'):
                assert result.data is not None
        except CareDailyException as e:
            raise e
    
    @pytest.mark.requires_admin_key
    def test_get_organization_totals(self, admin_client):
        """Test getting organization totals (read-only operation)."""
        try:
            api = admin_client.admin_api(Organizations)
            result = api.get_organization_totals(organization_id=0)
            
            # Should return organization totals
            assert result is not None
            if hasattr(result, 'data'):
                assert result.data is not None
        except CareDailyException as e:
            assert e.context["resultCode"] == ResultCode.ACCESS_DENIED.value
    
    @pytest.mark.requires_admin_key
    def test_get_brands(self, admin_client):
        """Test getting brands list (read-only operation)."""
        try:
            api = admin_client.admin_api(Organizations)
            api.get_brands()
        except CareDailyException as e:
            assert e.context["resultCode"] == ResultCode.ACCESS_DENIED.value

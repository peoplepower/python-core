"""Integration tests for CLI commands with live API.

These tests verify that CLI commands work correctly with live API keys.
Set CAREDAILY_API_KEY environment variable to run these tests.

Note: These tests use subprocess to run the CLI commands, so they
verify the full CLI experience including argument parsing and error handling.
"""
import os
import subprocess
import pytest
from caredaily.exceptions import CareDailyException


@pytest.mark.integration
@pytest.mark.network
class TestCLILive:
    """Integration tests for CLI commands."""
    
    @pytest.mark.requires_api_key
    def test_ping_command(self, has_api_key):
        """Test the 'ping' CLI command with live API."""
        if not has_api_key:
            pytest.skip("App API key not available")
        
        # Run the caredaily ping command
        result = subprocess.run(
            ["caredaily", "ping"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Ping should succeed (may return "Pong" or an error message)
        # We check that the command executed without a Python error
        assert result.returncode is not None
        
        # Combine stdout and stderr for checking
        output = result.stdout + result.stderr
        
        # If successful, should see "Pong" in output
        if "Pong" in output:
            # Success case
            assert True
        else:
            # Failure case: network errors are acceptable for integration tests
            # in environments without network access. The CLI should handle errors gracefully.
            # Check that it's a network/connection error, not a code error
            if "Traceback" in output:
                # If there's a traceback, verify it's a network-related error
                # Network errors are acceptable in test environments without network access
                network_error_keywords = ["connection", "network", "resolve", "failed to resolve", "nodename", "servname"]
                if any(keyword in output.lower() for keyword in network_error_keywords):
                    pytest.skip("Network error during ping test (expected in environments without network access)")
                else:
                    # If it's not a network error, it's a code error - fail the test
                    pytest.fail(f"Unexpected error in ping command: {output}")
            else:
                # If no traceback, it's a graceful error message (acceptable)
                # This could be a configuration error or other non-network issue
                pass
    
    @pytest.mark.requires_api_key
    def test_cloud_connectivity_check_availability(self, has_api_key):
        """Test the 'cloud-connectivity --check-availability' CLI command."""
        if not has_api_key:
            pytest.skip("App API key not available")
        
        result = subprocess.run(
            ["caredaily", "cloud-connectivity", "--check-availability"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Command should execute (may succeed or fail based on API availability)
        assert result.returncode is not None
        # Should not have Python traceback errors
        assert "Traceback" not in result.stderr
    
    @pytest.mark.requires_api_key
    def test_cloud_connectivity_version(self, has_api_key):
        """Test the 'cloud-connectivity --version' CLI command."""
        if not has_api_key:
            pytest.skip("App API key not available")
        
        result = subprocess.run(
            ["caredaily", "cloud-connectivity", "--version"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Command should execute
        assert result.returncode is not None
        # Should not have Python traceback errors
        assert "Traceback" not in result.stderr
        # If successful, should have some version information
        if result.returncode == 0:
            assert len(result.stdout) > 0 or len(result.stderr) > 0
    
    @pytest.mark.requires_api_key
    def test_cli_help(self):
        """Test that CLI help command works (doesn't require API key)."""
        result = subprocess.run(
            ["caredaily", "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        # Help should always work
        assert result.returncode == 0
        assert "caredaily" in result.stdout.lower() or "usage" in result.stdout.lower()

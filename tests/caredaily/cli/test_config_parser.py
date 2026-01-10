import os
import pytest
from configparser import ConfigParser

from caredaily import CareDaily, CareDailyException


class TestConfigParser:
    """Functional tests for the CareDaily configuration parser."""

    def test_config_parser_reads_default_profile(self, tmp_path):
        """Test that config parser correctly reads default profile from config and credentials files."""
        # Create .caredaily directory structure
        caredaily_dir = tmp_path / ".caredaily"
        caredaily_dir.mkdir()

        config_path = caredaily_dir / "config"
        credentials_path = caredaily_dir / "credentials"

        # Write config file with default profile
        config = ConfigParser()
        config["default"] = {
            "hostname": "test.example.com",
            "ssl_verify": "true",
            "proxies": "",
        }
        with open(config_path, "w") as f:
            config.write(f)

        # Write credentials file with default profile
        credentials = ConfigParser()
        credentials["default"] = {
            "key": "default_api_key_12345",
            "key_type": "0",
            "key_expire_ms": "1234567890",
        }
        with open(credentials_path, "w") as f:
            credentials.write(f)

        # Mock CAREDAILY_INTEGRATION_PATH environment variable
        with pytest.MonkeyPatch.context() as m:
            m.setenv("CAREDAILY_INTEGRATION_PATH", str(tmp_path))

            # Initialize CareDaily
            caredaily = CareDaily(raise_errors=False)

            # Verify config was parsed correctly
            assert caredaily._config.get("hostname") == "test.example.com"
            assert caredaily._config.get("api_key") == "default_api_key_12345"
            assert caredaily._config.get("key_type") == "0"
            assert caredaily._config.get("ssl_verify") is True

    def test_config_parser_reads_named_profile(self, tmp_path):
        """Test that config parser correctly reads a named profile."""
        # Create .caredaily directory structure
        caredaily_dir = tmp_path / ".caredaily"
        caredaily_dir.mkdir()

        config_path = caredaily_dir / "config"
        credentials_path = caredaily_dir / "credentials"

        # Write config file with default and production profile
        config = ConfigParser()
        config["default"] = {
            "hostname": "default.example.com",
            "ssl_verify": "true",
        }
        config["profile production"] = {
            "hostname": "prod.example.com",
            "ssl_verify": "false",
            "proxies": '{"http": "http://proxy.example.com:8080"}',
        }
        with open(config_path, "w") as f:
            config.write(f)

        # Write credentials file with default and production profile
        credentials = ConfigParser()
        credentials["default"] = {
            "key": "default_key",
            "key_type": "0",
        }
        credentials["production"] = {
            "key": "production_key_98765",
            "key_type": "11",
            "key_expire_ms": "9876543210",
        }
        with open(credentials_path, "w") as f:
            credentials.write(f)

        # Mock CAREDAILY_INTEGRATION_PATH environment variable
        with pytest.MonkeyPatch.context() as m:
            m.setenv("CAREDAILY_INTEGRATION_PATH", str(tmp_path))

            # Initialize CareDaily with production profile
            caredaily = CareDaily(profile="production", raise_errors=False)

            # Verify production profile was parsed correctly
            assert caredaily._config.get("hostname") == "prod.example.com"
            assert caredaily._config.get("api_key") == "production_key_98765"
            assert caredaily._config.get("key_type") == "11"
            assert caredaily._config.get("ssl_verify") is False

    def test_config_parser_profile_from_environment(self, tmp_path):
        """Test that config parser reads profile from CAREDAILY_PROFILE environment variable."""
        # Create .caredaily directory structure
        caredaily_dir = tmp_path / ".caredaily"
        caredaily_dir.mkdir()

        config_path = caredaily_dir / "config"
        credentials_path = caredaily_dir / "credentials"

        # Write config file
        config = ConfigParser()
        config["default"] = {
            "hostname": "default.example.com",
            "ssl_verify": "true",
        }
        config["profile dev"] = {
            "hostname": "dev.example.com",
        }
        with open(config_path, "w") as f:
            config.write(f)

        # Write credentials file
        credentials = ConfigParser()
        credentials["default"] = {
            "key": "default_key",
            "key_type": "0",
        }
        credentials["dev"] = {
            "key": "dev_key_555",
            "key_type": "0",
        }
        with open(credentials_path, "w") as f:
            credentials.write(f)

        # Mock environment variables
        with pytest.MonkeyPatch.context() as m:
            m.setenv("CAREDAILY_INTEGRATION_PATH", str(tmp_path))
            m.setenv("CAREDAILY_PROFILE", "dev")

            # Initialize CareDaily without explicit profile
            caredaily = CareDaily(raise_errors=False)

            # Verify dev profile was used
            assert caredaily._config.get("hostname") == "dev.example.com"
            assert caredaily._config.get("api_key") == "dev_key_555"

    def test_config_parser_profile_fallback_to_default(self, tmp_path):
        """Test that config parser falls back to default values when profile values are missing."""
        # Create .caredaily directory structure
        caredaily_dir = tmp_path / ".caredaily"
        caredaily_dir.mkdir()

        config_path = caredaily_dir / "config"
        credentials_path = caredaily_dir / "credentials"

        # Write config file with partial profile
        config = ConfigParser()
        config["default"] = {
            "hostname": "default.example.com",
            "ssl_verify": "true",
            "proxies": "",
        }
        config["profile staging"] = {
            "hostname": "staging.example.com",
            # ssl_verify and proxies not specified
        }
        with open(config_path, "w") as f:
            config.write(f)

        # Write credentials file with partial profile
        credentials = ConfigParser()
        credentials["default"] = {
            "key": "default_key",
            "key_type": "0",
        }
        credentials["staging"] = {
            "key": "staging_key",
            # key_type not specified
        }
        with open(credentials_path, "w") as f:
            credentials.write(f)

        # Mock CAREDAILY_INTEGRATION_PATH environment variable
        with pytest.MonkeyPatch.context() as m:
            m.setenv("CAREDAILY_INTEGRATION_PATH", str(tmp_path))

            # Initialize CareDaily with staging profile
            caredaily = CareDaily(profile="staging", raise_errors=False)

            # Verify staging profile values are used
            assert caredaily._config.get("hostname") == "staging.example.com"
            assert caredaily._config.get("api_key") == "staging_key"

            # Verify default values are used for missing profile settings
            assert caredaily._config.get("ssl_verify") is True

    def test_config_parser_ssl_verify_parsing(self, tmp_path):
        """Test that config parser correctly parses various ssl_verify values."""
        # Create .caredaily directory structure
        caredaily_dir = tmp_path / ".caredaily"
        caredaily_dir.mkdir()

        config_path = caredaily_dir / "config"
        credentials_path = caredaily_dir / "credentials"

        # Write credentials file
        credentials = ConfigParser()
        credentials["default"] = {
            "key": "test_key",
            "key_type": "0",
        }
        with open(credentials_path, "w") as f:
            credentials.write(f)

        # Test various ssl_verify values
        test_cases = [
            ("true", True),
            ("True", True),
            ("TRUE", True),
            ("false", False),
            ("False", False),
            ("FALSE", False),
        ]

        for ssl_value, expected in test_cases:
            # Write config file with test ssl_verify value
            config = ConfigParser()
            config["default"] = {
                "hostname": "test.example.com",
                "ssl_verify": ssl_value,
            }
            with open(config_path, "w") as f:
                config.write(f)

            # Mock CAREDAILY_INTEGRATION_PATH environment variable
            with pytest.MonkeyPatch.context() as m:
                m.setenv("CAREDAILY_INTEGRATION_PATH", str(tmp_path))

                # Initialize CareDaily
                caredaily = CareDaily(raise_errors=False)

                # Verify ssl_verify was parsed correctly
                assert caredaily._config.get("ssl_verify") == expected, \
                    f"ssl_verify='{ssl_value}' should parse to {expected}"

    def test_config_parser_missing_default_section_raises_error(self, tmp_path):
        """Test that config parser raises error when default section is missing."""
        # Create .caredaily directory structure
        caredaily_dir = tmp_path / ".caredaily"
        caredaily_dir.mkdir()

        config_path = caredaily_dir / "config"
        credentials_path = caredaily_dir / "credentials"

        # Write config file without default section
        config = ConfigParser()
        config["profile test"] = {
            "hostname": "test.example.com",
        }
        with open(config_path, "w") as f:
            config.write(f)

        # Write credentials file
        credentials = ConfigParser()
        credentials["default"] = {
            "key": "test_key",
            "key_type": "0",
        }
        with open(credentials_path, "w") as f:
            credentials.write(f)

        # Mock CAREDAILY_INTEGRATION_PATH environment variable
        with pytest.MonkeyPatch.context() as m:
            m.setenv("CAREDAILY_INTEGRATION_PATH", str(tmp_path))

            # Should raise error when raise_errors=True
            with pytest.raises(CareDailyException) as exc_info:
                CareDaily(raise_errors=True)

            assert "missing 'default' section" in str(exc_info.value)

    def test_config_parser_missing_profile_raises_error(self, tmp_path):
        """Test that config parser raises error when specified profile is missing."""
        # Create .caredaily directory structure
        caredaily_dir = tmp_path / ".caredaily"
        caredaily_dir.mkdir()

        config_path = caredaily_dir / "config"
        credentials_path = caredaily_dir / "credentials"

        # Write config file with default section only
        config = ConfigParser()
        config["default"] = {
            "hostname": "default.example.com",
            "ssl_verify": "true",
        }
        with open(config_path, "w") as f:
            config.write(f)

        # Write credentials file
        credentials = ConfigParser()
        credentials["default"] = {
            "key": "default_key",
            "key_type": "0",
        }
        with open(credentials_path, "w") as f:
            credentials.write(f)

        # Mock CAREDAILY_INTEGRATION_PATH environment variable
        with pytest.MonkeyPatch.context() as m:
            m.setenv("CAREDAILY_INTEGRATION_PATH", str(tmp_path))

            # Should raise error when profile doesn't exist
            with pytest.raises(CareDailyException) as exc_info:
                CareDaily(profile="nonexistent", raise_errors=True)

            assert "missing 'profile nonexistent' section" in str(exc_info.value)

    def test_config_parser_empty_credentials_profile(self, tmp_path):
        """Test that config parser handles empty credentials profile sections."""
        # Create .caredaily directory structure
        caredaily_dir = tmp_path / ".caredaily"
        caredaily_dir.mkdir()

        config_path = caredaily_dir / "config"
        credentials_path = caredaily_dir / "credentials"

        # Write config file
        config = ConfigParser()
        config["default"] = {
            "hostname": "default.example.com",
            "ssl_verify": "true",
        }
        config["profile test"] = {
            "hostname": "test.example.com",
        }
        with open(config_path, "w") as f:
            config.write(f)

        # Write credentials file with empty profile section
        credentials = ConfigParser()
        credentials["default"] = {
            "key": "default_key",
            "key_type": "0",
        }
        credentials["test"] = {}  # Empty section
        with open(credentials_path, "w") as f:
            credentials.write(f)

        # Mock CAREDAILY_INTEGRATION_PATH environment variable
        with pytest.MonkeyPatch.context() as m:
            m.setenv("CAREDAILY_INTEGRATION_PATH", str(tmp_path))

            # Initialize CareDaily with test profile
            caredaily = CareDaily(profile="test", raise_errors=False)

            # Should fall back to default credentials
            assert caredaily._config.get("api_key") == "default_key"
            # But use profile hostname
            assert caredaily._config.get("hostname") == "test.example.com"

    def test_config_parser_proxies_json_format(self, tmp_path):
        """Test that config parser correctly handles proxies in JSON format."""
        # Create .caredaily directory structure
        caredaily_dir = tmp_path / ".caredaily"
        caredaily_dir.mkdir()

        config_path = caredaily_dir / "config"
        credentials_path = caredaily_dir / "credentials"

        # Write config file with JSON proxies
        config = ConfigParser()
        config["default"] = {
            "hostname": "test.example.com",
            "ssl_verify": "true",
            "proxies": '{"http": "http://proxy.example.com:8080", "https": "https://proxy.example.com:8443"}',
        }
        with open(config_path, "w") as f:
            config.write(f)

        # Write credentials file
        credentials = ConfigParser()
        credentials["default"] = {
            "key": "test_key",
            "key_type": "0",
        }
        with open(credentials_path, "w") as f:
            credentials.write(f)

        # Mock CAREDAILY_INTEGRATION_PATH environment variable
        with pytest.MonkeyPatch.context() as m:
            m.setenv("CAREDAILY_INTEGRATION_PATH", str(tmp_path))

            # Initialize CareDaily
            caredaily = CareDaily(raise_errors=False)

            # Verify proxies config exists
            assert caredaily._config.get("proxies") is not None

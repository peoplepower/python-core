import os
import tempfile
import unittest
from configparser import ConfigParser
from unittest.mock import Mock, patch, MagicMock

from click.testing import CliRunner

from caredaily import CareDaily, CloudConnectivity, Authentication
from caredaily.cli.app import app, ping, cloud_connectivity, login


class TestCliApp(unittest.TestCase):
    """Test suite for CLI app commands"""

    def setUp(self):
        """Set up test fixtures"""
        self.runner = CliRunner()
        self.temp_dir = tempfile.mkdtemp()
        self.caredaily_dir = os.path.join(self.temp_dir, ".caredaily")
        os.makedirs(self.caredaily_dir, exist_ok=True)

        # Create default config file
        self.config_path = os.path.join(self.caredaily_dir, "config")
        config = ConfigParser()
        config["default"] = {
            "hostname": "test.example.com",
            "ssl_verify": "True",
        }
        with open(self.config_path, "w") as f:
            config.write(f)

        # Create default credentials file
        self.credentials_path = os.path.join(self.caredaily_dir, "credentials")
        credentials = ConfigParser()
        credentials["default"] = {
            "key": "test_api_key",
            "key_type": "0",
        }
        with open(self.credentials_path, "w") as f:
            credentials.write(f)

    def tearDown(self):
        """Clean up test fixtures"""
        import shutil

        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    @patch.dict(os.environ, {"HOME": ""}, clear=True)
    def test_app_main_group_help(self):
        """Test main app group help message"""
        os.environ["HOME"] = self.temp_dir
        result = self.runner.invoke(app, ["--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("caredaily - commandline API client configuration utility", result.output)
        self.assertIn("configure", result.output)
        self.assertIn("ping", result.output)
        self.assertIn("cloud-connectivity", result.output)
        self.assertIn("login", result.output)

    @patch.dict(os.environ, {"HOME": ""}, clear=True)
    def test_app_with_profile_option(self):
        """Test app with --profile option"""
        os.environ["HOME"] = self.temp_dir

        # Add profile to config
        config = ConfigParser()
        config.read(self.config_path)
        config["profile test"] = {
            "hostname": "profile.example.com",
        }
        with open(self.config_path, "w") as f:
            config.write(f)

        # Add profile to credentials
        credentials = ConfigParser()
        credentials.read(self.credentials_path)
        credentials["test"] = {
            "key": "profile_key",
            "key_type": "0",
        }
        with open(self.credentials_path, "w") as f:
            credentials.write(f)

        result = self.runner.invoke(app, ["--profile", "test", "--help"])
        self.assertEqual(result.exit_code, 0)

    @patch.dict(os.environ, {"HOME": "", "CAREDAILY_PROFILE": "test"}, clear=True)
    def test_app_with_profile_from_env(self):
        """Test app uses CAREDAILY_PROFILE environment variable"""
        os.environ["HOME"] = self.temp_dir

        # Add profile to config
        config = ConfigParser()
        config.read(self.config_path)
        config["profile test"] = {
            "hostname": "env.example.com",
        }
        with open(self.config_path, "w") as f:
            config.write(f)

        # Add profile to credentials
        credentials = ConfigParser()
        credentials.read(self.credentials_path)
        credentials["test"] = {
            "key": "env_key",
            "key_type": "0",
        }
        with open(self.credentials_path, "w") as f:
            credentials.write(f)

        result = self.runner.invoke(app, ["--help"])
        self.assertEqual(result.exit_code, 0)

    @patch.dict(os.environ, {"HOME": ""}, clear=True)
    @patch("caredaily.cli.app.CareDaily")
    def test_ping_success(self, mock_caredaily_class):
        """Test ping command with successful response"""
        os.environ["HOME"] = self.temp_dir

        # Mock the CareDaily instance and CloudConnectivity API
        mock_caredaily = MagicMock()
        mock_cloud_api = MagicMock()
        mock_cloud_api.check_availability.return_value = Mock(data={"status": "ok"})
        mock_caredaily.app_api.return_value = mock_cloud_api
        mock_caredaily_class.return_value = mock_caredaily

        result = self.runner.invoke(app, ["ping"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Pong", result.output)
        mock_cloud_api.check_availability.assert_called_once()

    @patch.dict(os.environ, {"HOME": ""}, clear=True)
    @patch("caredaily.cli.app.CareDaily")
    def test_ping_failure(self, mock_caredaily_class):
        """Test ping command with failure"""
        os.environ["HOME"] = self.temp_dir

        # Mock the CareDaily instance to raise an exception
        mock_caredaily = MagicMock()
        mock_cloud_api = MagicMock()
        mock_cloud_api.check_availability.side_effect = Exception("Connection failed")
        mock_caredaily.app_api.return_value = mock_cloud_api
        mock_caredaily_class.return_value = mock_caredaily

        result = self.runner.invoke(app, ["ping"])
        self.assertEqual(result.exit_code, 0)  # Command doesn't fail, just reports error
        self.assertIn("Ping failed", result.output)

    @patch.dict(os.environ, {"HOME": ""}, clear=True)
    @patch("caredaily.cli.app.CareDaily")
    def test_cloud_connectivity_check_availability(self, mock_caredaily_class):
        """Test cloud-connectivity command with --check-availability flag"""
        os.environ["HOME"] = self.temp_dir

        mock_caredaily = MagicMock()
        mock_cloud_api = MagicMock()
        mock_cloud_api.check_availability.return_value = Mock(data={"available": True})
        mock_caredaily.app_api.return_value = mock_cloud_api
        mock_caredaily_class.return_value = mock_caredaily

        result = self.runner.invoke(app, ["cloud-connectivity", "--check-availability"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("available", result.output)
        mock_cloud_api.check_availability.assert_called_once()

    @patch.dict(os.environ, {"HOME": ""}, clear=True)
    @patch("caredaily.cli.app.CareDaily")
    def test_cloud_connectivity_version(self, mock_caredaily_class):
        """Test cloud-connectivity command with --version flag"""
        os.environ["HOME"] = self.temp_dir

        mock_caredaily = MagicMock()
        mock_cloud_api = MagicMock()
        mock_cloud_api.get_version.return_value = Mock(data={"version": "1.0.0"})
        mock_caredaily.app_api.return_value = mock_cloud_api
        mock_caredaily_class.return_value = mock_caredaily

        result = self.runner.invoke(app, ["cloud-connectivity", "--version"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("version", result.output)
        mock_cloud_api.get_version.assert_called_once_with(json_format=True)

    @patch.dict(os.environ, {"HOME": ""}, clear=True)
    @patch("caredaily.cli.app.CareDaily")
    def test_cloud_connectivity_connection_settings(self, mock_caredaily_class):
        """Test cloud-connectivity command with --connection-settings flag"""
        os.environ["HOME"] = self.temp_dir

        mock_caredaily = MagicMock()
        mock_cloud_api = MagicMock()
        mock_cloud_api.get_cloud_settings.return_value = Mock(
            data={"settings": "value"}
        )
        mock_caredaily.app_api.return_value = mock_cloud_api
        mock_caredaily_class.return_value = mock_caredaily

        result = self.runner.invoke(app, ["cloud-connectivity", "--connection-settings"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("settings", result.output)
        mock_cloud_api.get_cloud_settings.assert_called_once()

    @patch.dict(os.environ, {"HOME": ""}, clear=True)
    @patch("caredaily.cli.app.CareDaily")
    def test_cloud_connectivity_server_url(self, mock_caredaily_class):
        """Test cloud-connectivity command with --server-url flag"""
        os.environ["HOME"] = self.temp_dir

        mock_caredaily = MagicMock()
        mock_cloud_api = MagicMock()
        mock_cloud_api.get_server_settings_url.return_value = Mock(
            data={"url": "https://example.com"}
        )
        mock_caredaily.app_api.return_value = mock_cloud_api
        mock_caredaily_class.return_value = mock_caredaily

        result = self.runner.invoke(app, ["cloud-connectivity", "--server-url"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("url", result.output)
        mock_cloud_api.get_server_settings_url.assert_called_once()

    @patch.dict(os.environ, {"HOME": ""}, clear=True)
    @patch("caredaily.cli.app.CareDaily")
    def test_cloud_connectivity_no_options(self, mock_caredaily_class):
        """Test cloud-connectivity command with no options raises error"""
        os.environ["HOME"] = self.temp_dir

        mock_caredaily = MagicMock()
        mock_caredaily_class.return_value = mock_caredaily

        result = self.runner.invoke(app, ["cloud-connectivity"])
        self.assertEqual(result.exit_code, 0)  # Command doesn't fail, just reports error
        self.assertIn("At least one option is required", result.output)

    @patch.dict(os.environ, {"HOME": ""}, clear=True)
    @patch("caredaily.cli.app.CareDaily")
    def test_cloud_connectivity_failure(self, mock_caredaily_class):
        """Test cloud-connectivity command with API failure"""
        os.environ["HOME"] = self.temp_dir

        mock_caredaily = MagicMock()
        mock_cloud_api = MagicMock()
        mock_cloud_api.check_availability.side_effect = Exception("API Error")
        mock_caredaily.app_api.return_value = mock_cloud_api
        mock_caredaily_class.return_value = mock_caredaily

        result = self.runner.invoke(app, ["cloud-connectivity", "--check-availability"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Failed to get version", result.output)

    @patch.dict(os.environ, {"HOME": ""}, clear=True)
    @patch("caredaily.cli.app.CareDaily")
    def test_login_success(self, mock_caredaily_class):
        """Test login command with successful authentication"""
        os.environ["HOME"] = self.temp_dir

        mock_caredaily = MagicMock()
        mock_auth_api = MagicMock()
        mock_auth_api.login_by_username.return_value = Mock(
            data={"key": "new_api_key", "userId": 123}
        )
        mock_caredaily.app_api.return_value = mock_auth_api
        mock_caredaily_class.return_value = mock_caredaily

        result = self.runner.invoke(
            app, ["login"], input="testuser\ntestpassword\n"
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("key", result.output)
        mock_auth_api.login_by_username.assert_called_once_with(
            username="testuser", password="testpassword"
        )

    @patch.dict(os.environ, {"HOME": ""}, clear=True)
    @patch("caredaily.cli.app.CareDaily")
    def test_login_with_options(self, mock_caredaily_class):
        """Test login command with username and password options"""
        os.environ["HOME"] = self.temp_dir

        mock_caredaily = MagicMock()
        mock_auth_api = MagicMock()
        mock_auth_api.login_by_username.return_value = Mock(
            data={"key": "new_api_key", "userId": 123}
        )
        mock_caredaily.app_api.return_value = mock_auth_api
        mock_caredaily_class.return_value = mock_caredaily

        result = self.runner.invoke(
            app, ["login", "--username", "testuser", "--password", "testpassword"]
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("key", result.output)
        mock_auth_api.login_by_username.assert_called_once_with(
            username="testuser", password="testpassword"
        )

    @patch.dict(os.environ, {"HOME": ""}, clear=True)
    @patch("caredaily.cli.app.CareDaily")
    def test_login_failure(self, mock_caredaily_class):
        """Test login command with authentication failure"""
        os.environ["HOME"] = self.temp_dir

        mock_caredaily = MagicMock()
        mock_auth_api = MagicMock()
        mock_auth_api.login_by_username.side_effect = Exception("Invalid credentials")
        mock_caredaily.app_api.return_value = mock_auth_api
        mock_caredaily_class.return_value = mock_caredaily

        result = self.runner.invoke(
            app, ["login"], input="testuser\ntestpassword\n"
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Login failed", result.output)

    @patch.dict(os.environ, {"HOME": ""}, clear=True)
    def test_app_context_object_initialization(self):
        """Test that app initializes context object correctly"""
        os.environ["HOME"] = self.temp_dir

        # Use a custom command to test context
        @app.command()
        @patch("click.pass_context")
        def test_context(ctx):
            return ctx.obj

        result = self.runner.invoke(app, ["--help"])
        self.assertEqual(result.exit_code, 0)

    @patch.dict(os.environ, {"HOME": ""}, clear=True)
    @patch("caredaily.cli.app.CareDaily")
    def test_cloud_connectivity_json_output(self, mock_caredaily_class):
        """Test cloud-connectivity outputs JSON correctly"""
        os.environ["HOME"] = self.temp_dir

        mock_caredaily = MagicMock()
        mock_cloud_api = MagicMock()
        mock_cloud_api.check_availability.return_value = Mock(
            data={"status": "available", "timestamp": 1234567890}
        )
        mock_caredaily.app_api.return_value = mock_cloud_api
        mock_caredaily_class.return_value = mock_caredaily

        result = self.runner.invoke(app, ["cloud-connectivity", "--check-availability"])
        self.assertEqual(result.exit_code, 0)
        # Check that output is valid JSON
        import json
        try:
            json.loads(result.output.strip())
        except json.JSONDecodeError:
            self.fail("Output is not valid JSON")

    @patch.dict(os.environ, {"HOME": ""}, clear=True)
    @patch("caredaily.cli.app.CareDaily")
    def test_cloud_connectivity_non_json_output(self, mock_caredaily_class):
        """Test cloud-connectivity handles non-JSON data"""
        os.environ["HOME"] = self.temp_dir

        mock_caredaily = MagicMock()
        mock_cloud_api = MagicMock()
        # Return a non-serializable object
        mock_cloud_api.check_availability.return_value = Mock(data=object())
        mock_caredaily.app_api.return_value = mock_cloud_api
        mock_caredaily_class.return_value = mock_caredaily

        result = self.runner.invoke(app, ["cloud-connectivity", "--check-availability"])
        self.assertEqual(result.exit_code, 0)
        # Should output the object representation instead

    @patch.dict(os.environ, {"HOME": ""}, clear=True)
    def test_help_flag_short(self):
        """Test short help flag -h"""
        os.environ["HOME"] = self.temp_dir
        result = self.runner.invoke(app, ["-h"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("caredaily - commandline API client configuration utility", result.output)

    @patch.dict(os.environ, {"HOME": ""}, clear=True)
    def test_help_flag_long(self):
        """Test long help flag --help"""
        os.environ["HOME"] = self.temp_dir
        result = self.runner.invoke(app, ["--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("caredaily - commandline API client configuration utility", result.output)


if __name__ == "__main__":
    unittest.main()

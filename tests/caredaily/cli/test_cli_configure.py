import os
import tempfile
import unittest
from configparser import ConfigParser
from unittest.mock import Mock, patch, MagicMock

from click.testing import CliRunner

from caredaily import CareDaily, CloudConnectivity, Authentication, APIKeyType, CareDailyException
from caredaily.cli.app import app
from caredaily.cli.configure import configure, init, interactive, list, list_profiles


class TestCliConfigure(unittest.TestCase):
    """Test suite for CLI configure commands"""

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
    def test_configure_help(self):
        """Test configure command help"""
        os.environ["HOME"] = self.temp_dir
        result = self.runner.invoke(app, ["configure", "--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("interactive", result.output)
        self.assertIn("list", result.output)
        self.assertIn("list-profiles", result.output)
        self.assertIn("init", result.output)

    @patch.dict(os.environ, {"HOME": ""}, clear=True)
    @patch("caredaily.cli.configure.CareDaily")
    def test_init_new_config_without_signin(self, mock_caredaily_class):
        """Test init command creating new configuration without sign in"""
        os.environ["HOME"] = self.temp_dir

        # Remove existing config
        if os.path.exists(self.caredaily_dir):
            import shutil
            shutil.rmtree(self.caredaily_dir)

        mock_caredaily = MagicMock()
        mock_cloud_api = MagicMock()
        mock_cloud_api.check_availability.return_value = Mock(data={"status": "ok"})
        mock_caredaily.app_api.return_value = mock_cloud_api
        mock_caredaily_class.return_value = mock_caredaily

        result = self.runner.invoke(
            app,
            ["configure", "init"],
            input="app.peoplepowerco.com\n/tmp/core\n/tmp/private\nn\ny\n",
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Initialization completed successfully", result.output)
        self.assertTrue(os.path.exists(self.config_path))
        self.assertTrue(os.path.exists(self.credentials_path))

    @patch.dict(os.environ, {"HOME": ""}, clear=True)
    @patch("caredaily.cli.configure.CareDaily")
    def test_init_existing_config(self, mock_caredaily_class):
        """Test init command with existing configuration"""
        os.environ["HOME"] = self.temp_dir

        mock_caredaily = MagicMock()
        mock_caredaily_class.return_value = mock_caredaily

        result = self.runner.invoke(app, ["configure", "init"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Configuration already exists", result.output)

    @patch.dict(os.environ, {"HOME": ""}, clear=True)
    @patch("caredaily.cli.app.CareDaily")
    def test_init_with_signin(self, mock_caredaily_class):
        """Test init command with sign in"""
        os.environ["HOME"] = self.temp_dir

        # Remove existing config
        if os.path.exists(self.caredaily_dir):
            import shutil
            shutil.rmtree(self.caredaily_dir)

        mock_caredaily = MagicMock()
        mock_cloud_api = MagicMock()
        mock_cloud_api.check_availability.return_value = Mock(data={"status": "ok"})
        mock_auth_api = MagicMock()
        mock_auth_api.login_by_username.return_value = Mock(
            data={"key": "new_key", "keyExpireMs": 3600000, "keyType": 0}
        )
        mock_caredaily.app_api.side_effect = lambda x: (
            mock_cloud_api if x == CloudConnectivity else mock_auth_api
        )
        mock_caredaily.update_config = MagicMock()
        mock_caredaily_class.return_value = mock_caredaily

        result = self.runner.invoke(
            app,
            ["configure", "init"],
            input="app.peoplepowerco.com\n/tmp/core\n/tmp/private\ny\ntestuser\ntestpass\ny\n",
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Initialization completed successfully", result.output)

        # Verify credentials were saved
        credentials = ConfigParser()
        credentials.read(self.credentials_path)
        self.assertEqual(credentials["default"]["key"], "new_key")

    @patch.dict(os.environ, {"HOME": ""}, clear=True)
    @patch("caredaily.CareDaily")
    def test_init_cancel(self, mock_caredaily_class):
        """Test init command cancellation"""
        os.environ["HOME"] = self.temp_dir

        # Remove existing config
        if os.path.exists(self.caredaily_dir):
            import shutil
            shutil.rmtree(self.caredaily_dir)

        mock_caredaily = MagicMock()
        mock_cloud_api = MagicMock()
        mock_cloud_api.check_availability.return_value = Mock(data={"status": "ok"})
        mock_caredaily.app_api.return_value = mock_cloud_api
        mock_caredaily_class.return_value = mock_caredaily

        result = self.runner.invoke(
            app,
            ["configure", "init"],
            input="app.peoplepowerco.com\n/tmp/core\n/tmp/private\nn\nn\n",
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Initialization canceled", result.output)

    @patch.dict(os.environ, {"HOME": ""}, clear=True)
    @patch("caredaily.CareDaily")
    def test_init_with_profile_from_env(self, mock_caredaily_class):
        """Test init command with CAREDAILY_PROFILE set"""
        os.environ["HOME"] = self.temp_dir
        os.environ["CAREDAILY_PROFILE"] = "testprofile"

        # Remove existing config
        if os.path.exists(self.caredaily_dir):
            import shutil
            shutil.rmtree(self.caredaily_dir)

        mock_caredaily = MagicMock()
        mock_cloud_api = MagicMock()
        mock_cloud_api.check_availability.return_value = Mock(data={"status": "ok"})
        mock_caredaily.app_api.return_value = mock_cloud_api
        mock_caredaily_class.return_value = mock_caredaily

        result = self.runner.invoke(
            app,
            ["configure", "init"],
            input="app.peoplepowerco.com\n/tmp/core\n/tmp/private\nn\ny\n",
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("testprofile", result.output)

    @patch.dict(os.environ, {"HOME": ""}, clear=True)
    @patch("caredaily.cli.configure.CareDaily")
    def test_init_availability_check_failure(self, mock_caredaily_class):
        """Test init command when availability check fails"""
        os.environ["HOME"] = self.temp_dir

        # Remove existing config
        if os.path.exists(self.caredaily_dir):
            import shutil
            shutil.rmtree(self.caredaily_dir)

        mock_caredaily = MagicMock()
        mock_cloud_api = MagicMock()
        mock_cloud_api.check_availability.side_effect = Exception("Connection error")
        mock_caredaily.app_api.return_value = mock_cloud_api
        mock_caredaily_class.return_value = mock_caredaily

        result = self.runner.invoke(
            app, ["configure", "init"], input="invalid.hostname.com\n"
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Error checking availability", result.output)

    @patch.dict(os.environ, {"HOME": ""}, clear=True)
    @patch("caredaily.cli.configure.CareDaily")
    def test_list_default_profile(self, mock_caredaily_class):
        """Test list command with default profile"""
        os.environ["HOME"] = self.temp_dir

        mock_caredaily = MagicMock()
        mock_caredaily_class.return_value = mock_caredaily

        result = self.runner.invoke(app, ["configure", "list"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("hostname", result.output)
        self.assertIn("test.example.com", result.output)
        self.assertIn("ssl_verify", result.output)
        self.assertIn("key", result.output)

    @patch.dict(os.environ, {"HOME": ""}, clear=True)
    @patch("caredaily.cli.configure.CareDaily")
    def test_list_specific_profile(self, mock_caredaily_class):
        """Test list command with specific profile"""
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
            "key_type": "11",
        }
        with open(self.credentials_path, "w") as f:
            credentials.write(f)

        mock_caredaily = MagicMock()
        mock_caredaily_class.return_value = mock_caredaily

        result = self.runner.invoke(app, ["configure", "list", "--profile", "test"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("profile.example.com", result.output)

    @patch.dict(os.environ, {"HOME": ""}, clear=True)
    @patch("caredaily.cli.configure.CareDaily")
    def test_list_nonexistent_profile(self, mock_caredaily_class):
        """Test list command with non-existent profile"""
        os.environ["HOME"] = self.temp_dir

        mock_caredaily = MagicMock()
        mock_caredaily_class.return_value = mock_caredaily

        result = self.runner.invoke(app, ["configure", "list", "--profile", "nonexistent"])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("not found", result.output)

    @patch.dict(os.environ, {"HOME": ""}, clear=True)
    @patch("caredaily.cli.configure.CareDaily")
    def test_list_obfuscates_api_key(self, mock_caredaily_class):
        """Test list command obfuscates API key"""
        os.environ["HOME"] = self.temp_dir

        mock_caredaily = MagicMock()
        mock_caredaily_class.return_value = mock_caredaily

        result = self.runner.invoke(app, ["configure", "list"])
        self.assertEqual(result.exit_code, 0)
        # API key should be obfuscated (starts with ***)
        self.assertIn("*****", result.output)
        # Full API key should not be visible
        self.assertNotIn("test_api_key", result.output)

    @patch.dict(os.environ, {"HOME": ""}, clear=True)
    @patch("caredaily.cli.configure.CareDaily")
    def test_list_profiles(self, mock_caredaily_class):
        """Test list-profiles command"""
        os.environ["HOME"] = self.temp_dir

        # Add multiple profiles
        credentials = ConfigParser()
        credentials.read(self.credentials_path)
        credentials["profile1"] = {"key": "key1", "key_type": "0"}
        credentials["profile2"] = {"key": "key2", "key_type": "11"}
        with open(self.credentials_path, "w") as f:
            credentials.write(f)

        mock_caredaily = MagicMock()
        mock_caredaily_class.return_value = mock_caredaily

        result = self.runner.invoke(app, ["configure", "list-profiles"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("default", result.output)
        self.assertIn("profile1", result.output)
        self.assertIn("profile2", result.output)

    @patch.dict(os.environ, {"HOME": ""}, clear=True)
    @patch("caredaily.cli.configure.CareDaily")
    def test_interactive_without_profile(self, mock_caredaily_class):
        """Test interactive command without profile specified"""
        os.environ["HOME"] = self.temp_dir

        mock_caredaily = MagicMock()
        mock_caredaily_class.return_value = mock_caredaily

        result = self.runner.invoke(app, ["configure", "interactive"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Profile not specified", result.output)

    @patch.dict(os.environ, {"HOME": ""}, clear=True)
    @patch("caredaily.cli.app.CareDaily")
    def test_interactive_with_profile(self, mock_caredaily_class):
        """Test interactive command with profile"""
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

        mock_caredaily = MagicMock()
        mock_cloud_api = MagicMock()
        mock_cloud_api.check_availability.return_value = Mock(data={"status": "ok"})
        mock_caredaily.app_api.return_value = mock_cloud_api
        mock_caredaily.update_config = MagicMock()
        mock_caredaily_class.return_value = mock_caredaily

        result = self.runner.invoke(
            app,
            ["configure", "interactive", "--profile", "test"],
            input="profile.example.com\ny\n\nn\nnew_key\n0\n",
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Configured 'test' successfully", result.output)

    @patch.dict(os.environ, {"HOME": ""}, clear=True)
    @patch("caredaily.cli.app.CareDaily")
    def test_interactive_with_signin(self, mock_caredaily_class):
        """Test interactive command with sign in"""
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

        mock_caredaily = MagicMock()
        mock_cloud_api = MagicMock()
        mock_cloud_api.check_availability.return_value = Mock(data={"status": "ok"})
        mock_auth_api = MagicMock()
        mock_auth_api.login_by_username.return_value = Mock(
            data={"key": "new_key", "keyExpireMs": 3600000, "keyType": 0}
        )
        mock_caredaily.app_api.side_effect = lambda x: (
            mock_cloud_api if x == CloudConnectivity else mock_auth_api
        )
        mock_caredaily.update_config = MagicMock()
        mock_caredaily_class.return_value = mock_caredaily

        result = self.runner.invoke(
            app,
            ["configure", "interactive", "--profile", "test"],
            input="profile.example.com\ny\n\ny\ntestuser\ntestpass\nUser\n",
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Configured 'test' successfully", result.output)

        # Verify credentials were updated
        credentials = ConfigParser()
        credentials.read(self.credentials_path)
        self.assertEqual(credentials["test"]["key"], "new_key")

    @patch.dict(os.environ, {"HOME": ""}, clear=True)
    @patch("caredaily.cli.app.CareDaily")
    def test_interactive_with_username_password_options(self, mock_caredaily_class):
        """Test interactive command with username and password options"""
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

        mock_caredaily = MagicMock()
        mock_cloud_api = MagicMock()
        mock_cloud_api.check_availability.return_value = Mock(data={"status": "ok"})
        mock_auth_api = MagicMock()
        mock_auth_api.login_by_username.return_value = Mock(
            data={"key": "new_key", "keyExpireMs": 3600000, "keyType": 0}
        )
        mock_caredaily.app_api.side_effect = lambda x: (
            mock_cloud_api if x == CloudConnectivity else mock_auth_api
        )
        mock_caredaily.update_config = MagicMock()
        mock_caredaily_class.return_value = mock_caredaily

        result = self.runner.invoke(
            app,
            [
                "configure",
                "interactive",
                "--profile",
                "test",
                "--username",
                "testuser",
                "--password",
                "testpass",
            ],
            input="profile.example.com\ny\n\nUser\n",
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Configured 'test' successfully", result.output)

    @patch.dict(os.environ, {"HOME": ""}, clear=True)
    @patch("caredaily.cli.app.CareDaily")
    def test_interactive_with_passcode(self, mock_caredaily_class):
        """Test interactive command with passcode requirement"""
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

        mock_caredaily = MagicMock()
        mock_cloud_api = MagicMock()
        mock_cloud_api.check_availability.return_value = Mock(data={"status": "ok"})
        mock_auth_api = MagicMock()

        # First call raises exception requiring passcode
        passcode_exception = CareDailyException("Passcode required", context={"resultCode": 17})
        mock_auth_api.login_by_username.side_effect = [
            passcode_exception,
            Mock(data={"key": "new_key", "keyExpireMs": 3600000, "keyType": 0}),
        ]

        mock_caredaily.app_api.side_effect = lambda x: (
            mock_cloud_api if x == CloudConnectivity else mock_auth_api
        )
        mock_caredaily.update_config = MagicMock()
        mock_caredaily_class.return_value = mock_caredaily

        result = self.runner.invoke(
            app,
            ["configure", "interactive", "--profile", "test"],
            input="profile.example.com\ny\n\ny\ntestuser\ntestpass\nUser\n123456\n",
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Configured 'test' successfully", result.output)

    @patch.dict(os.environ, {"HOME": ""}, clear=True)
    @patch("caredaily.cli.configure.CareDaily")
    def test_interactive_not_initialized(self, mock_caredaily_class):
        """Test interactive command when config is not initialized"""
        os.environ["HOME"] = self.temp_dir

        # Remove default section from config
        config = ConfigParser()
        with open(self.config_path, "w") as f:
            config.write(f)

        mock_caredaily = MagicMock()
        mock_caredaily_class.return_value = mock_caredaily

        result = self.runner.invoke(
            app, ["configure", "interactive", "--profile", "test"]
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Configuration not initialized", result.output)

    @patch.dict(os.environ, {"HOME": ""}, clear=True)
    @patch("caredaily.cli.configure.CareDaily")
    def test_interactive_availability_check_failure(self, mock_caredaily_class):
        """Test interactive command when availability check fails"""
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

        mock_caredaily = MagicMock()
        mock_cloud_api = MagicMock()
        mock_cloud_api.check_availability.side_effect = Exception("Connection error")
        mock_caredaily.app_api.return_value = mock_cloud_api
        mock_caredaily.update_config = MagicMock()
        mock_caredaily_class.return_value = mock_caredaily

        result = self.runner.invoke(
            app,
            ["configure", "interactive", "--profile", "test"],
            input="invalid.hostname.com\ny\n\n",
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Error checking availability", result.output)

    @patch.dict(os.environ, {"HOME": ""}, clear=True)
    @patch("caredaily.cli.app.CareDaily")
    def test_interactive_creates_new_profile_section(self, mock_caredaily_class):
        """Test interactive command creates new profile section if not exists"""
        os.environ["HOME"] = self.temp_dir

        mock_caredaily = MagicMock()
        mock_cloud_api = MagicMock()
        mock_cloud_api.check_availability.return_value = Mock(data={"status": "ok"})
        mock_caredaily.app_api.return_value = mock_cloud_api
        mock_caredaily.update_config = MagicMock()
        mock_caredaily_class.return_value = mock_caredaily

        result = self.runner.invoke(
            app,
            ["configure", "interactive", "--profile", "newprofile"],
            input="new.example.com\ny\n\nn\nnew_key\n0\n",
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Configured 'newprofile' successfully", result.output)

        # Verify new profile was created
        config = ConfigParser()
        config.read(self.config_path)
        self.assertTrue(config.has_section("profile newprofile"))

        credentials = ConfigParser()
        credentials.read(self.credentials_path)
        self.assertTrue(credentials.has_section("newprofile"))

    @patch.dict(os.environ, {"HOME": "", "CAREDAILY_PROFILE": "envprofile"}, clear=True)
    @patch("caredaily.cli.app.CareDaily")
    def test_interactive_uses_env_profile(self, mock_caredaily_class):
        """Test interactive command uses CAREDAILY_PROFILE from environment"""
        os.environ["HOME"] = self.temp_dir

        # Add profile to config
        config = ConfigParser()
        config.read(self.config_path)
        config["profile envprofile"] = {
            "hostname": "env.example.com",
        }
        with open(self.config_path, "w") as f:
            config.write(f)

        # Add profile to credentials
        credentials = ConfigParser()
        credentials.read(self.credentials_path)
        credentials["envprofile"] = {
            "key": "env_key",
            "key_type": "0",
        }
        with open(self.credentials_path, "w") as f:
            credentials.write(f)

        mock_caredaily = MagicMock()
        mock_cloud_api = MagicMock()
        mock_cloud_api.check_availability.return_value = Mock(data={"status": "ok"})
        mock_caredaily.app_api.return_value = mock_cloud_api
        mock_caredaily.update_config = MagicMock()
        mock_caredaily_class.return_value = mock_caredaily

        result = self.runner.invoke(
            app,
            ["configure", "interactive"],
            input="env.example.com\ny\n\nn\nenv_key\n0\n",
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Configured 'envprofile' successfully", result.output)


if __name__ == "__main__":
    unittest.main()

import logging
import os
import tempfile
import unittest
from configparser import ConfigParser
from unittest.mock import Mock, patch

from caredaily.apis import (
    AdminDevices,
    AdminLocations,
    AdminTags,
    Analytic,
    AppFiles,
    Authentication,
    Billing,
    BotDeveloper,
    BotStore,
    Challenges,
    CloudConnectivity,
    CloudsIntegration,
    DeveloperTeams,
    DeviceFiles,
    DeviceMeasurements,
    Devices,
    DeviceTypesAndParameters,
    EnergyManagement,
    Execution,
    Firmware,
    Groups,
    Locations,
    Narratives,
    Organizations,
    PaidServices,
    ProfessionalMonitoring,
    RAG,
    Reports,
    Rules,
    System,
    SystemAndUserProperties,
    UserAccounts,
    UserCommunication,
    UserGroups,
    Users,
    Weather,
    Websocket,
)
from caredaily.caredaily import CareDaily
from caredaily.exceptions import CareDailyException


class TestCareDaily(unittest.TestCase):
    def setUp(self):
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
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    @patch.dict(os.environ, {"CAREDAILY_INTEGRATION_PATH": ""})
    def test_init_with_default_config(self, mock_home=None):
        os.environ["CAREDAILY_INTEGRATION_PATH"] = self.temp_dir
        caredaily = CareDaily(raise_errors=False)

        self.assertIsInstance(caredaily._config, dict)
        self.assertEqual(caredaily._config.get("hostname"), "test.example.com")
        self.assertEqual(caredaily._config.get("api_key"), "test_api_key")
        self.assertEqual(caredaily._config.get("key_type"), "0")
        self.assertTrue(caredaily._config.get("ssl_verify"))

    @patch.dict(os.environ, {"CAREDAILY_INTEGRATION_PATH": ""})
    def test_init_with_profile(self, mock_home=None):
        os.environ["CAREDAILY_INTEGRATION_PATH"] = self.temp_dir

        # Add profile to config
        config = ConfigParser()
        config.read(self.config_path)
        config["profile test"] = {
            "hostname": "profile.example.com",
            "ssl_verify": "False",
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

        caredaily = CareDaily(profile="test", raise_errors=False)

        self.assertEqual(caredaily._config.get("hostname"), "profile.example.com")
        self.assertEqual(caredaily._config.get("api_key"), "profile_key")
        self.assertEqual(caredaily._config.get("key_type"), "11")
        self.assertFalse(caredaily._config.get("ssl_verify"))

    @patch.dict(os.environ, {"CAREDAILY_INTEGRATION_PATH": "", "CAREDAILY_PROFILE": "test"})
    def test_init_with_profile_from_env(self, mock_home=None):
        os.environ["CAREDAILY_INTEGRATION_PATH"] = self.temp_dir

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

        caredaily = CareDaily(raise_errors=False)

        self.assertEqual(caredaily._config.get("hostname"), "env.example.com")
        self.assertEqual(caredaily._config.get("api_key"), "env_key")

    @patch.dict(os.environ, {"CAREDAILY_INTEGRATION_PATH": ""})
    def test_init_missing_default_section_with_raise_errors(self, mock_home=None):
        os.environ["CAREDAILY_INTEGRATION_PATH"] = self.temp_dir

        # Create config without default section
        config = ConfigParser()
        with open(self.config_path, "w") as f:
            config.write(f)

        with self.assertRaises(CareDailyException) as context:
            CareDaily(raise_errors=True)

        self.assertIn("missing 'default' section", str(context.exception))

    @patch.dict(os.environ, {"CAREDAILY_INTEGRATION_PATH": ""})
    def test_init_missing_default_section_without_raise_errors(self, mock_home=None):
        os.environ["CAREDAILY_INTEGRATION_PATH"] = self.temp_dir

        # Create config without default section
        config = ConfigParser()
        with open(self.config_path, "w") as f:
            config.write(f)

        # Should not raise when raise_errors=False
        caredaily = CareDaily(raise_errors=False)
        self.assertIsInstance(caredaily._config, dict)

    @patch.dict(os.environ, {"CAREDAILY_INTEGRATION_PATH": ""})
    def test_init_missing_profile_section_with_raise_errors(self, mock_home=None):
        os.environ["CAREDAILY_INTEGRATION_PATH"] = self.temp_dir

        with self.assertRaises(CareDailyException) as context:
            CareDaily(profile="nonexistent", raise_errors=True)

        self.assertIn("missing 'profile nonexistent' section", str(context.exception))

    @patch.dict(os.environ, {"CAREDAILY_INTEGRATION_PATH": "", "CAREDAILY_PROFILE": ""}, clear=False)
    def test_init_missing_credentials_default_with_raise_errors(self, mock_home=None):
        os.environ["CAREDAILY_INTEGRATION_PATH"] = self.temp_dir
        os.environ["CAREDAILY_PROFILE"] = ""

        # Create credentials without default section
        credentials = ConfigParser()
        with open(self.credentials_path, "w") as f:
            credentials.write(f)

        with self.assertRaises(CareDailyException) as context:
            CareDaily(raise_errors=True)

        self.assertIn("Credentials file is missing 'default' section", str(context.exception))

    @patch.dict(os.environ, {"CAREDAILY_INTEGRATION_PATH": ""})
    def test_init_missing_credentials_profile_with_raise_errors(self, mock_home=None):
        os.environ["CAREDAILY_INTEGRATION_PATH"] = self.temp_dir

        # Add profile to config
        config = ConfigParser()
        config.read(self.config_path)
        config["profile test"] = {
            "hostname": "test.example.com",
        }
        with open(self.config_path, "w") as f:
            config.write(f)

        with self.assertRaises(CareDailyException) as context:
            CareDaily(profile="test", raise_errors=True)

        self.assertIn("Credentials file is missing 'test' section", str(context.exception))

    @patch.dict(os.environ, {"CAREDAILY_INTEGRATION_PATH": ""})
    def test_init_ssl_verify_parsing(self, mock_home=None):
        os.environ["CAREDAILY_INTEGRATION_PATH"] = self.temp_dir

        test_cases = [
            ("true", True),
            ("True", True),
            ("false", False),
            ("False", False),
        ]

        for ssl_value, expected in test_cases:
            config = ConfigParser()
            config["default"] = {
                "hostname": "test.example.com",
                "ssl_verify": ssl_value,
            }
            with open(self.config_path, "w") as f:
                config.write(f)

            caredaily = CareDaily(raise_errors=False)
            self.assertEqual(caredaily._config.get("ssl_verify"), expected)

    @patch.dict(os.environ, {"CAREDAILY_INTEGRATION_PATH": ""})
    def test_init_ssl_verify_invalid_value(self, mock_home=None):
        os.environ["CAREDAILY_INTEGRATION_PATH"] = self.temp_dir

        config = ConfigParser()
        config["default"] = {
            "hostname": "test.example.com",
            "ssl_verify": "invalid",
        }
        with open(self.config_path, "w") as f:
            config.write(f)

        caredaily = CareDaily(raise_errors=False)
        # Should default to True on error
        self.assertTrue(caredaily._config.get("ssl_verify"))

    @patch.dict(os.environ, {"CAREDAILY_INTEGRATION_PATH": ""})
    def test_init_proxies_config(self, mock_home=None):
        os.environ["CAREDAILY_INTEGRATION_PATH"] = self.temp_dir

        config = ConfigParser()
        config["default"] = {
            "hostname": "test.example.com",
            "proxies": '{"http": "http://proxy.example.com:8080"}',
        }
        with open(self.config_path, "w") as f:
            config.write(f)

        caredaily = CareDaily(raise_errors=False)
        self.assertIsNotNone(caredaily._config.get("proxies"))

    @patch.dict(os.environ, {"CAREDAILY_INTEGRATION_PATH": ""})
    def test_update_config_valid_keys(self, mock_home=None):
        os.environ["CAREDAILY_INTEGRATION_PATH"] = self.temp_dir
        caredaily = CareDaily(raise_errors=False)

        valid_keys = [
            ("hostname", "new.example.com"),
            ("api_key", "new_key"),
            ("key_type", "11"),
            ("proxies", {"http": "http://proxy.com"}),
        ]

        for key, value in valid_keys:
            caredaily.update_config(key, value)
            self.assertEqual(caredaily._config.get(key), value)

    @patch.dict(os.environ, {"CAREDAILY_INTEGRATION_PATH": ""})
    def test_update_config_with_falsy_value(self, mock_home=None):
        os.environ["CAREDAILY_INTEGRATION_PATH"] = self.temp_dir
        caredaily = CareDaily(raise_errors=False)

        # Set a value first
        caredaily._config["ssl_verify"] = True
        # Update with False (falsy value but not None) should set it to False
        caredaily.update_config("ssl_verify", False)
        # False is a valid value (implementation checks 'value is not None')
        self.assertIn("ssl_verify", caredaily._config)
        self.assertEqual(caredaily._config["ssl_verify"], False)

    @patch.dict(os.environ, {"CAREDAILY_INTEGRATION_PATH": ""})
    def test_update_config_invalid_key(self, mock_home=None):
        os.environ["CAREDAILY_INTEGRATION_PATH"] = self.temp_dir
        caredaily = CareDaily(raise_errors=False)

        initial_config = caredaily._config.copy()
        caredaily.update_config("invalid_key", "value")

        # Config should remain unchanged
        self.assertEqual(caredaily._config, initial_config)

    @patch.dict(os.environ, {"CAREDAILY_INTEGRATION_PATH": ""})
    def test_update_config_logger(self, mock_home=None):
        os.environ["CAREDAILY_INTEGRATION_PATH"] = self.temp_dir
        caredaily = CareDaily(raise_errors=False)

        custom_logger = logging.getLogger("custom")
        caredaily.update_config("logger", custom_logger)

        self.assertEqual(caredaily.logger, custom_logger)

    @patch.dict(os.environ, {"CAREDAILY_INTEGRATION_PATH": ""})
    def test_update_config_delete_key(self, mock_home=None):
        os.environ["CAREDAILY_INTEGRATION_PATH"] = self.temp_dir
        caredaily = CareDaily(raise_errors=False)

        caredaily._config["hostname"] = "test.com"
        caredaily.update_config("hostname", None)

        self.assertNotIn("hostname", caredaily._config)

    @patch.dict(os.environ, {"CAREDAILY_INTEGRATION_PATH": ""})
    def test_get_config(self, mock_home=None):
        os.environ["CAREDAILY_INTEGRATION_PATH"] = self.temp_dir
        caredaily = CareDaily(raise_errors=False)

        config = caredaily.get_config()

        self.assertIsInstance(config, dict)
        self.assertIn("hostname", config)
        self.assertIn("ssl_verify", config)
        self.assertIn("proxies", config)

    @patch.dict(os.environ, {"CAREDAILY_INTEGRATION_PATH": ""})
    def test_app_api_cloud_connectivity(self, mock_home=None):
        os.environ["CAREDAILY_INTEGRATION_PATH"] = self.temp_dir
        caredaily = CareDaily(raise_errors=False)

        api = caredaily.app_api(CloudConnectivity)
        self.assertIsInstance(api, CloudConnectivity)

    @patch.dict(os.environ, {"CAREDAILY_INTEGRATION_PATH": ""})
    def test_app_api_all_types(self, mock_home=None):
        os.environ["CAREDAILY_INTEGRATION_PATH"] = self.temp_dir
        caredaily = CareDaily(raise_errors=False)

        app_api_types = [
            (CloudConnectivity, CloudConnectivity),
            (Authentication, Authentication),
            (UserAccounts, UserAccounts),
            (Locations, Locations),
            (Devices, Devices),
            (DeviceMeasurements, DeviceMeasurements),
            (UserCommunication, UserCommunication),
            (SystemAndUserProperties, SystemAndUserProperties),
            (DeviceFiles, DeviceFiles),
            (AppFiles, AppFiles),
            (Rules, Rules),
            (PaidServices, PaidServices),
            (ProfessionalMonitoring, ProfessionalMonitoring),
            (EnergyManagement, EnergyManagement),
            (Weather, Weather),
            (DeviceTypesAndParameters, DeviceTypesAndParameters),
            (CloudsIntegration, CloudsIntegration),
            (RAG, RAG),
            (Websocket, Websocket),
        ]

        for api_type, expected_class in app_api_types:
            api = caredaily.app_api(api_type)
            self.assertIsInstance(api, expected_class)

    @patch.dict(os.environ, {"CAREDAILY_INTEGRATION_PATH": ""})
    def test_app_api_unknown_type(self, mock_home=None):
        os.environ["CAREDAILY_INTEGRATION_PATH"] = self.temp_dir
        caredaily = CareDaily(raise_errors=False)

        class UnknownType:
            pass

        api = caredaily.app_api(UnknownType)
        self.assertIsNone(api)

    @patch.dict(os.environ, {"CAREDAILY_INTEGRATION_PATH": ""})
    def test_admin_api_all_types(self, mock_home=None):
        os.environ["CAREDAILY_INTEGRATION_PATH"] = self.temp_dir
        caredaily = CareDaily(raise_errors=False)

        admin_api_types = [
            (System, System),
            (Organizations, Organizations),
            (Groups, Groups),
            (Users, Users),
            (UserGroups, UserGroups),
            (AdminDevices, AdminDevices),
            (AdminLocations, AdminLocations),
            (Challenges, Challenges),
            (AdminTags, AdminTags),
            (Narratives, Narratives),
            (Billing, Billing),
            (Firmware, Firmware),
            (Reports, Reports),
        ]

        for api_type, expected_class in admin_api_types:
            api = caredaily.admin_api(api_type)
            self.assertIsInstance(api, expected_class)

    @patch.dict(os.environ, {"CAREDAILY_INTEGRATION_PATH": ""})
    def test_admin_api_unknown_type(self, mock_home=None):
        os.environ["CAREDAILY_INTEGRATION_PATH"] = self.temp_dir
        caredaily = CareDaily(raise_errors=False)

        class UnknownType:
            pass

        api = caredaily.admin_api(UnknownType)
        self.assertIsNone(api)

    @patch.dict(os.environ, {"CAREDAILY_INTEGRATION_PATH": ""})
    def test_bot_api_all_types(self, mock_home=None):
        os.environ["CAREDAILY_INTEGRATION_PATH"] = self.temp_dir
        caredaily = CareDaily(raise_errors=False)

        bot_api_types = [
            (Analytic, Analytic),
            (BotDeveloper, BotDeveloper),
            (BotStore, BotStore),
            (DeveloperTeams, DeveloperTeams),
            (Execution, Execution),
        ]

        for api_type, expected_class in bot_api_types:
            api = caredaily.bot_api(api_type)
            self.assertIsInstance(api, expected_class)

    @patch.dict(os.environ, {"CAREDAILY_INTEGRATION_PATH": ""})
    def test_bot_api_unknown_type(self, mock_home=None):
        os.environ["CAREDAILY_INTEGRATION_PATH"] = self.temp_dir
        caredaily = CareDaily(raise_errors=False)

        class UnknownType:
            pass

        api = caredaily.bot_api(UnknownType)
        self.assertIsNone(api)


    @patch.dict(os.environ, {"CAREDAILY_INTEGRATION_PATH": ""}, clear=True)
    @patch("os.name", "nt")
    def test_init_windows_path(self, mock_os_name=None):
        os.environ["CAREDAILY_INTEGRATION_PATH"] = self.temp_dir

        caredaily = CareDaily(raise_errors=False)
        self.assertIsInstance(caredaily._config, dict)

    @patch.dict(os.environ, {"CAREDAILY_INTEGRATION_PATH": ""})
    def test_init_profile_fallback_to_default(self, mock_home=None):
        os.environ["CAREDAILY_INTEGRATION_PATH"] = self.temp_dir

        # Add profile config but not credentials
        config = ConfigParser()
        config.read(self.config_path)
        config["profile test"] = {
            "hostname": "profile.example.com",
        }
        with open(self.config_path, "w") as f:
            config.write(f)

        # Add profile credentials
        credentials = ConfigParser()
        credentials.read(self.credentials_path)
        credentials["test"] = {}  # Empty profile section
        with open(self.credentials_path, "w") as f:
            credentials.write(f)

        caredaily = CareDaily(profile="test", raise_errors=False)

        # Should fall back to default credentials
        self.assertEqual(caredaily._config.get("api_key"), "test_api_key")
        # But use profile hostname
        self.assertEqual(caredaily._config.get("hostname"), "profile.example.com")

    @patch.dict(os.environ, {"CAREDAILY_INTEGRATION_PATH": ""})
    def test_logger_initialization(self, mock_home=None):
        os.environ["CAREDAILY_INTEGRATION_PATH"] = self.temp_dir

        caredaily = CareDaily(raise_errors=False)
        self.assertIsInstance(caredaily.logger, logging.Logger)

    @patch.dict(os.environ, {"CAREDAILY_INTEGRATION_PATH": ""})
    def test_config_exception_context(self, mock_home=None):
        os.environ["CAREDAILY_INTEGRATION_PATH"] = self.temp_dir

        # Create config without default section
        config = ConfigParser()
        with open(self.config_path, "w") as f:
            config.write(f)

        try:
            CareDaily(raise_errors=True)
        except CareDailyException as e:
            self.assertIsNotNone(e.context)
            self.assertIn("code", e.context)
            self.assertIn("config_path", e.context)

    @patch.dict(os.environ, {"CAREDAILY_INTEGRATION_PATH": ""})
    @patch("caredaily.caredaily.ConfigParser")
    def test_init_with_general_exception(self, mock_config_parser, mock_home=None):
        os.environ["CAREDAILY_INTEGRATION_PATH"] = self.temp_dir

        # Mock ConfigParser to raise a general exception (not CareDailyException)
        mock_config_instance = Mock()
        mock_config_instance.read.side_effect = RuntimeError("Unexpected error")
        mock_config_parser.return_value = mock_config_instance

        # This should not raise, but log the error instead
        caredaily = CareDaily(raise_errors=False)

        # Config should still be initialized (empty dict)
        self.assertIsInstance(caredaily._config, dict)


if __name__ == "__main__":
    unittest.main()

# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "python-dotenv",
#   "tabulate",
#   "click",
#   "requests",
#   "pydantic",
# ]
# ///

import os
from configparser import ConfigParser
from logging import Logger

from .apis import (
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
    Community,
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
from .exceptions import CareDailyException

from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file (looks for .env in current or parent directories by default)
env_filepath = find_dotenv()
load_dotenv()

class CareDaily:
    def __init__(self, profile: str = None, raise_errors: bool = True):
        self.logger = Logger(__name__)
        self._config = {}

        __config = {}
        # Load config from configuration file
        try:
            config_object = ConfigParser()
            credentials_object = ConfigParser()

            integration_path = os.environ.get("CAREDAILY_INTEGRATION_PATH")
            if not integration_path:
                if os.name == "nt":  # Windows
                    integration_path = os.environ["UserProfile"]
                else:  # Unix-based systems
                    integration_path = os.environ["HOME"]

            profile = profile or os.environ.get("CAREDAILY_PROFILE")
            config_path = os.path.join(integration_path, ".caredaily", "config")
            credentials_path = os.path.join(integration_path, ".caredaily", "credentials")

            config_object.read(config_path)
            default_config = {}
            if "default" not in config_object.sections():
                if raise_errors:
                    raise CareDailyException("Configuration file is missing 'default' section.", {"code": -1, "config_path": config_path, "profile": profile})
            else:
                default_config = config_object["default"]
            profile_config = {}
            if profile:
                if f"profile {profile}" not in config_object.sections():
                    if raise_errors:
                        raise CareDailyException(f"Configuration file is missing 'profile {profile}' section.", {"code": -2, "config_path": config_path, "profile": profile})
                else:
                    profile_config = config_object[f"profile {profile}"]
            __config["hostname"] = profile_config.get("hostname") or default_config.get(
                "hostname"
            )
            try:
                ssl_verify_value = profile_config.get("ssl_verify") or default_config.get("ssl_verify") or "True"
                __config["ssl_verify"] = eval(ssl_verify_value.capitalize())
            except Exception as e:
                self.logger.warning(f"Error while reading ssl_verify: {e}")
                __config["ssl_verify"] = True
            __config["proxies"] = profile_config.get("proxies") or default_config.get(
                "proxies"
            )

            credentials_object.read(credentials_path)
            default_credentials = {}
            if "default" not in credentials_object.sections():
                if raise_errors:
                    raise CareDailyException("Credentials file is missing 'default' section.", {"code": -1, "credentials_path": credentials_path, "profile": profile})
            else:
                default_credentials = credentials_object["default"]
            profile_credentials = {}
            if profile:
                if f"{profile}" not in credentials_object.sections():
                    if raise_errors:
                        raise CareDailyException(f"Credentials file is missing '{profile}' section.", {"code": -2, "credentials_path": credentials_path, "profile": profile})
                else:
                    profile_credentials = credentials_object[f"{profile}"]
            __config["api_key"] = profile_credentials.get(
                "key"
            ) or default_credentials.get("key")
            __config["key_type"] = profile_credentials.get(
                "key_type"
            ) or default_credentials.get("key_type")
        except CareDailyException as e:
            raise e
        except Exception as e:
            import traceback
            self.logger.error(traceback.format_exc())
            self.logger.error(f"Error while reading configuration file: {e}")

        self._config = __config
        self.logger.debug(f"__config: {__config}")

    def update_config(self, key: str, value):
        if key not in [
            "hostname",
            "api_key",
            "key_type",
            "ssl_verify",
            "proxies",
            "logger",
        ]:
            return
        if key == "logger":
            self.logger = value or Logger(__name__)
        if value is not None:
            self._config[key] = value
        elif key in self._config:
            del self._config[key]

    def get_config(self):
        adapter = self.app_api(CloudConnectivity).adapter
        return {
            "hostname": adapter.url.split("://")[1],
            "api_key": adapter._headers.get("API_KEY"),
            "admin_key": adapter._headers.get("ADMIN_KEY"),
            "analytic_key": adapter._headers.get("ANALYTIC_KEY"),
            "ssl_verify": adapter._ssl_verify,
            "proxies": adapter._proxies,
        }

    # App APIs
    def app_api(self, type: type):
        if type == CloudConnectivity:
            return CloudConnectivity(self._config)
        if type == Authentication:
            return Authentication(self._config)
        if type == UserAccounts:
            return UserAccounts(self._config)
        if type == Locations:
            return Locations(self._config)
        if type == Devices:
            return Devices(self._config)
        if type == DeviceMeasurements:
            return DeviceMeasurements(self._config)
        if type == UserCommunication:
            return UserCommunication(self._config)
        if type == SystemAndUserProperties:
            return SystemAndUserProperties(self._config)
        if type == DeviceFiles:
            return DeviceFiles(self._config)
        if type == AppFiles:
            return AppFiles(self._config)
        if type == Rules:
            return Rules(self._config)
        if type == PaidServices:
            return PaidServices(self._config)
        if type == ProfessionalMonitoring:
            return ProfessionalMonitoring(self._config)
        if type == EnergyManagement:
            return EnergyManagement(self._config)
        if type == Weather:
            return Weather(self._config)
        if type == DeviceTypesAndParameters:
            return DeviceTypesAndParameters(self._config)
        if type == CloudsIntegration:
            return CloudsIntegration(self._config)
        if type == RAG:
            return RAG(self._config)
        if type == Community:
            return Community(self._config)
        if type == Websocket:
            return Websocket(self._config)
        return None

    # Admin APIs
    def admin_api(self, type: type):
        if type == System:
            return System(self._config)
        if type == Organizations:
            return Organizations(self._config)
        if type == Groups:
            return Groups(self._config)
        if type == Users:
            return Users(self._config)
        if type == UserGroups:
            return UserGroups(self._config)
        if type == AdminDevices:
            return AdminDevices(self._config)
        if type == AdminLocations:
            return AdminLocations(self._config)
        if type == Challenges:
            return Challenges(self._config)
        if type == AdminTags:
            return AdminTags(self._config)
        if type == Narratives:
            return Narratives(self._config)
        if type == Billing:
            return Billing(self._config)
        if type == Firmware:
            return Firmware(self._config)
        if type == Reports:
            return Reports(self._config)
        return None

    # Bot APIs
    def bot_api(self, type: type):
        if type == Analytic:
            return Analytic(self._config)
        if type == BotDeveloper:
            return BotDeveloper(self._config)
        if type == DeveloperTeams:
            return DeveloperTeams(self._config)
        if type == BotStore:
            return BotStore(self._config)
        if type == Execution:
            self.logger.debug(f"Execution: config={self._config}")
            return Execution(self._config)
        return None

# /// script
# requires-python = ">=3.8"
# ///
"""
CareDaily Python SDK

Provides APIs, models, and utilities for interacting with the CareDaily platform.
"""

__version__ = "1.0.1"

from .apis import (
    AdminDevices,
    AdminLocations,
    AdminTags,
    Analytic,
    API,
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
from .caredaily import CareDaily
from .exceptions import CareDailyException
from .models import (
    APIKeyType,
    SignatureAlgorithm,
    Cloud,
    MQTT,
    PythonRuntime,
    Result,
    ResultCode,
    Server,
    ServerType,
    TimeZone,
)

__all__ = [
    "APIKeyType",
    "SignatureAlgorithm",
    "CareDaily",
    "CareDailyException",
    "Cloud",
    "MQTT",
    "PythonRuntime",
    "Result",
    "ResultCode",
    "Server",
    "ServerType",
    "TimeZone",
    # APIs
    "API",
    # App APIs
    "AppFiles",
    "Authentication",
    "CloudConnectivity",
    "CloudsIntegration",
    "Community",
    "DeviceFiles",
    "DeviceMeasurements",
    "Devices",
    "DeviceTypesAndParameters",
    "EnergyManagement",
    "Locations",
    "PaidServices",
    "ProfessionalMonitoring",
    "RAG",
    "Rules",
    "SystemAndUserProperties",
    "UserAccounts",
    "UserCommunication",
    "Weather",
    "Websocket",
    # Admin APIs
    "AdminDevices",
    "AdminLocations",
    "AdminTags",
    "Billing",
    "Challenges",
    "Firmware",
    "Groups",
    "Narratives",
    "Organizations",
    "Reports",
    "System",
    "UserGroups",
    "Users",
    # Bot APIs
    "Analytic",
    "BotDeveloper",
    "BotStore",
    "DeveloperTeams",
    "Execution",
]

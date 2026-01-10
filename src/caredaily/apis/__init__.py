# /// script
# requires-python = ">=3.8"
# ///

from .admin import (
    Billing,
    Challenges,
    Devices as AdminDevices,
    Groups,
    Locations as AdminLocations,
    Narratives,
    Organizations,
    System,
    Tags as AdminTags,
    UserGroups,
    Users,
)
from .api import API
from .app import (
    AppFiles,
    Authentication,
    CloudConnectivity,
    CloudsIntegration,
    Community,
    DeviceFiles,
    DeviceMeasurements,
    Devices,
    DeviceTypesAndParameters,
    EnergyManagement,
    Locations,
    PaidServices,
    ProfessionalMonitoring,
    RAG,
    Rules,
    SystemAndUserProperties,
    UserAccounts,
    UserCommunication,
    Weather,
    Websocket,
)
from .bot import (
    BotDeveloper,
    BotStore,
    DeveloperTeams,
)
from .device import (
    Execution,
)
from .service import (
    AI,
    Questions,
    Services,
    Tags,
    Variables,
    VoiceCalls,
)

__all__ = [
    "API",
    # App APIs
    "CloudConnectivity",
    "Authentication",
    "UserAccounts",
    "Locations",
    "Devices",
    "DeviceMeasurements",
    "UserCommunication",
    "SystemAndUserProperties",
    "DeviceFiles",
    "AppFiles",
    "Rules",
    "PaidServices",
    "ProfessionalMonitoring",
    "EnergyManagement",
    "Weather",
    "DeviceTypesAndParameters",
    "CloudsIntegration",
    "RAG",
    "Community",
    "Websocket",
    # Admin APIs
    "System",
    "Organizations",
    "Groups",
    "Users",
    "UserGroups",
    "AdminDevices",
    "AdminLocations",
    "Challenges",
    "AdminTags",
    "Narratives",
    "Billing",
    # Bot APIs
    "BotDeveloper",
    "DeveloperTeams",
    "BotStore",
    # Service APIs
    "Services",
    "Questions",
    "Tags",
    "Variables",
    "VoiceCalls",
    "AI",
    # Device APIs
    "Execution",
]

# Endpoint Implementation Report

Generated: 2026-03-27 18:27:52.555119

**Total Endpoints:** 229
**Total Operations:** 364
**Source Files:** admin.yaml, bots.yaml, cloud.yaml
**Implemented:** 364 (100.0%)
**Missing:** 0 (0.0%)
**Duplicate Endpoints:** 2

## Duplicate Endpoints

⚠️  The following endpoints are defined in multiple source YAML files. Consider consolidating these definitions to a single source file to avoid confusion and potential conflicts.

- ⚠️  **POST** `/cloud/appstore/stream`
  - Defined in: cloud.yaml, bots.yaml
- ⚠️  **GET** `/cloud/appstore/summary`
  - Defined in: cloud.yaml, bots.yaml

## Missing Endpoints

✅ All endpoints are implemented!

## Implementation Details by Source File

### admin.yaml

#### /admin/json/billingItems

- ✅ **GET**: Implemented in:
  - `admin/billing.py`

#### /admin/json/billingPlans

- ✅ **GET**: Implemented in:
  - `admin/billing.py`
- ✅ **POST**: Implemented in:
  - `admin/billing.py`

#### /admin/json/billingPlans/{planId}/versions

- ✅ **GET**: Implemented in:
  - `admin/billing.py`
- ✅ **POST**: Implemented in:
  - `admin/billing.py`

#### /admin/json/brands

- ✅ **GET**: Implemented in:
  - `admin/organizations.py`

#### /admin/json/devices

- ✅ **GET**: Implemented in:
  - `admin/devices.py`

#### /admin/json/fwgroup

- ✅ **GET**: Implemented in:
  - `admin/firmware.py`
- ✅ **PUT**: Implemented in:
  - `admin/firmware.py`

#### /admin/json/fwjobs

- ✅ **DELETE**: Implemented in:
  - `admin/firmware.py`
- ✅ **GET**: Implemented in:
  - `admin/firmware.py`
- ✅ **POST**: Implemented in:
  - `admin/firmware.py`

#### /admin/json/fwversion

- ✅ **DELETE**: Implemented in:
  - `admin/firmware.py`
- ✅ **GET**: Implemented in:
  - `admin/firmware.py`
- ✅ **POST**: Implemented in:
  - `admin/firmware.py`

#### /admin/json/locations

- ✅ **GET**: Implemented in:
  - `admin/locations.py`

#### /admin/json/organizations

- ✅ **DELETE**: Implemented in:
  - `admin/organizations.py`
- ✅ **GET**: Implemented in:
  - `admin/organizations.py`
- ✅ **POST**: Implemented in:
  - `admin/organizations.py`
- ✅ **PUT**: Implemented in:
  - `admin/organizations.py`

#### /admin/json/organizations/{organizationId}/admins

- ✅ **GET**: Implemented in:
  - `admin/users.py`

#### /admin/json/organizations/{organizationId}/admins/{userId}

- ✅ **DELETE**: Implemented in:
  - `admin/users.py`
- ✅ **PUT**: Implemented in:
  - `admin/users.py`

#### /admin/json/organizations/{organizationId}/billingPlans

- ✅ **DELETE**: Implemented in:
  - `admin/billing.py`
- ✅ **GET**: Implemented in:
  - `admin/billing.py`
- ✅ **POST**: Implemented in:
  - `admin/billing.py`

#### /admin/json/organizations/{organizationId}/bills

- ✅ **GET**: Implemented in:
  - `admin/billing.py`
- ✅ **PUT**: Implemented in:
  - `admin/billing.py`

#### /admin/json/organizations/{organizationId}/bills/{billId}

- ✅ **GET**: Implemented in:
  - `admin/billing.py`

#### /admin/json/organizations/{organizationId}/challenges

- ✅ **GET**: Implemented in:
  - `admin/challenges.py`
- ✅ **POST**: Implemented in:
  - `admin/challenges.py`

#### /admin/json/organizations/{organizationId}/challenges/{challengeId}

- ✅ **DELETE**: Implemented in:
  - `admin/challenges.py`
- ✅ **PUT**: Implemented in:
  - `admin/challenges.py`

#### /admin/json/organizations/{organizationId}/challenges/{challengeId}/participants

- ✅ **GET**: Implemented in:
  - `admin/challenges.py`
- ✅ **PUT**: Implemented in:
  - `admin/challenges.py`

#### /admin/json/organizations/{organizationId}/challenges/{challengeId}/status/{status}

- ✅ **PUT**: Implemented in:
  - `admin/challenges.py`

#### /admin/json/organizations/{organizationId}/ehrFacilities

- ✅ **DELETE**: Implemented in:
  - `admin/organizations.py`
- ✅ **GET**: Implemented in:
  - `admin/organizations.py`
- ✅ **PUT**: Implemented in:
  - `admin/organizations.py`

#### /admin/json/organizations/{organizationId}/locationStatus

- ✅ **PUT**: Implemented in:
  - `admin/locations.py`

#### /admin/json/organizations/{organizationId}/locations

- ✅ **DELETE**: Implemented in:
  - `admin/locations.py`
- ✅ **POST**: Implemented in:
  - `admin/locations.py`
- ✅ **PUT**: Implemented in:
  - `admin/locations.py`

#### /admin/json/organizations/{organizationId}/narratives

- ✅ **GET**: Implemented in:
  - `admin/narratives.py`

#### /admin/json/organizations/{organizationId}/notificationUsers

- ✅ **GET**: Implemented in:
  - `admin/users.py`
- ✅ **PUT**: Implemented in:
  - `admin/users.py`

#### /admin/json/organizations/{organizationId}/notifications

- ✅ **POST**: Implemented in:
  - `admin/organizations.py`

#### /admin/json/organizations/{organizationId}/objects

- ✅ **GET**: Implemented in:
  - `admin/organizations.py`
- ✅ **POST**: Implemented in:
  - `admin/organizations.py`

#### /admin/json/organizations/{organizationId}/objects/{objectName}

- ✅ **DELETE**: Implemented in:
  - `admin/organizations.py`
- ✅ **GET**: Implemented in:
  - `admin/organizations.py`
- ✅ **PUT**: Implemented in:
  - `admin/organizations.py`

#### /admin/json/organizations/{organizationId}/surveys

- ✅ **GET**: Implemented in:
  - `admin/organizations.py`
- ✅ **POST**: Implemented in:
  - `admin/organizations.py`

#### /admin/json/organizations/{organizationId}/surveys/{surveyKey}

- ✅ **DELETE**: Implemented in:
  - `admin/organizations.py`
- ✅ **GET**: Implemented in:
  - `admin/organizations.py`
- ✅ **PUT**: Implemented in:
  - `admin/organizations.py`

#### /admin/json/organizations/{organizationId}/tags

- ✅ **DELETE**: Implemented in:
  - `admin/tags.py`
- ✅ **GET**: Implemented in:
  - `admin/tags.py`
- ✅ **PUT**: Implemented in:
  - `admin/tags.py`

#### /admin/json/roles

- ✅ **GET**: Implemented in:
  - `admin/users.py`

#### /admin/json/status

- ✅ **GET**: Implemented in:
  - `admin/system.py`

#### /admin/json/timeStates

- ✅ **GET**: Implemented in:
  - `admin/system.py`

#### /admin/json/users

- ✅ **GET**: Implemented in:
  - `admin/users.py`

#### /admin/json/users/{userId}/roles

- ✅ **DELETE**: Implemented in:
  - `admin/users.py`

#### /admin/json/users/{userId}/roles/{roleId}

- ✅ **PUT**: Implemented in:
  - `admin/users.py`

#### /reports/data

- ✅ **GET**: Implemented in:
  - `admin/reports.py`

#### /reports/data/{token}

- ✅ **GET**: Implemented in:
  - `admin/reports.py`

#### /reports/generate

- ✅ **GET**: Implemented in:
  - `admin/reports.py`

#### /reports/groups/{organizationId}

- ✅ **DELETE**: Implemented in:
  - `admin/reports.py`
- ✅ **GET**: Implemented in:
  - `admin/reports.py`
- ✅ **PUT**: Implemented in:
  - `admin/reports.py`

#### /reports/reports

- ✅ **GET**: Implemented in:
  - `admin/reports.py`

#### /reports/{organizationId}/collections

- ✅ **GET**: Implemented in:
  - `admin/reports.py`
- ✅ **POST**: Implemented in:
  - `admin/reports.py`

#### /reports/{organizationId}/collections/{collectionId}

- ✅ **DELETE**: Implemented in:
  - `admin/reports.py`
- ✅ **PUT**: Implemented in:
  - `admin/reports.py`

### bots.yaml

#### /analytic/admin/challenges/{challengeId}/participants

- ✅ **GET**: Implemented in:
  - `bot/analytic.py`

#### /analytic/ai

- ✅ **POST**: Implemented in:
  - `bot/analytic.py`

#### /analytic/appkey

- ✅ **GET**: Implemented in:
  - `bot/analytic.py`

#### /analytic/callCenter

- ✅ **GET**: Implemented in:
  - `bot/analytic.py`
- ✅ **PUT**: Implemented in:
  - `bot/analytic.py`

#### /analytic/callCenterAlerts

- ✅ **GET**: Implemented in:
  - `bot/analytic.py`

#### /analytic/dataRequests

- ✅ **POST**: Implemented in:
  - `bot/analytic.py`

#### /analytic/devices/{deviceId}/parameters

- ✅ **GET**: Implemented in:
  - `bot/analytic.py`
- ✅ **POST**: Implemented in:
  - `bot/analytic.py`

#### /analytic/execute

- ✅ **DELETE**: Implemented in:
  - `bot/analytic.py`
- ✅ **PUT**: Implemented in:
  - `bot/analytic.py`

#### /analytic/fallFeedback

- ✅ **POST**: Implemented in:
  - `bot/analytic.py`

#### /analytic/location/{locationId}

- ✅ **PUT**: Implemented in:
  - `bot/analytic.py`

#### /analytic/location/{locationId}/events

- ✅ **GET**: Implemented in:
  - `bot/analytic.py`

#### /analytic/location/{locationId}/notifications

- ✅ **POST**: Implemented in:
  - `bot/analytic.py`

#### /analytic/mms

- ✅ **POST**: Implemented in:
  - `bot/analytic.py`

#### /analytic/notifications

- ✅ **POST**: Implemented in:
  - `bot/analytic.py`

#### /analytic/openai

- ✅ **POST**: Implemented in:
  - `bot/analytic.py`

#### /analytic/parameters

- ✅ **PUT**: Implemented in:
  - `bot/analytic.py`

#### /analytic/questions

- ✅ **DELETE**: Implemented in:
  - `bot/analytic.py`
- ✅ **GET**: Implemented in:
  - `bot/analytic.py`
- ✅ **POST**: Implemented in:
  - `bot/analytic.py`
- ✅ **PUT**: Implemented in:
  - `bot/analytic.py`

#### /analytic/questions/collections

- ✅ **DELETE**: Implemented in:
  - `bot/analytic.py`
- ✅ **GET**: Implemented in:
  - `bot/analytic.py`
- ✅ **PUT**: Implemented in:
  - `bot/analytic.py`

#### /analytic/secrets

- ✅ **GET**: Implemented in:
  - `bot/analytic.py`

#### /analytic/start

- ✅ **POST**: Implemented in:
  - `bot/analytic.py`

#### /analytic/stream

- ✅ **POST**: Implemented in:
  - `bot/analytic.py`

#### /analytic/tags

- ✅ **DELETE**: Implemented in:
  - `bot/analytic.py`
- ✅ **GET**: Implemented in:
  - `bot/analytic.py`
- ✅ **PUT**: Implemented in:
  - `bot/analytic.py`

#### /analytic/ticket

- ✅ **POST**: Implemented in:
  - `bot/analytic.py`

#### /analytic/variables

- ✅ **POST**: Implemented in:
  - `bot/analytic.py`

#### /analytic/variables/{name}

- ✅ **DELETE**: Implemented in:
  - `bot/analytic.py`
- ✅ **GET**: Implemented in:
  - `bot/analytic.py`
- ✅ **POST**: Implemented in:
  - `bot/analytic.py`

#### /analytic/voiceCall

- ✅ **POST**: Implemented in:
  - `bot/analytic.py`

#### /analytic/voiceCallAnswer

- ✅ **DELETE**: Implemented in:
  - `bot/analytic.py`
- ✅ **POST**: Implemented in:
  - `bot/analytic.py`

#### /cloud/appstore/appInfo

- ✅ **GET**: Implemented in:
  - `bot/bot_store.py`

#### /cloud/appstore/appInstance

- ✅ **DELETE**: Implemented in:
  - `bot/bot_store.py`
- ✅ **GET**: Implemented in:
  - `bot/bot_store.py`
- ✅ **POST**: Implemented in:
  - `bot/bot_store.py`
- ✅ **PUT**: Implemented in:
  - `bot/bot_store.py`

#### /cloud/appstore/objects/{name}

- ✅ **GET**: Implemented in:
  - `bot/bot_store.py`

#### /cloud/appstore/organizations

- ✅ **GET**: Implemented in:
  - `bot/bot_store.py`

#### /cloud/appstore/organizations/{organizationId}

- ✅ **DELETE**: Implemented in:
  - `bot/bot_store.py`
- ✅ **POST**: Implemented in:
  - `bot/bot_store.py`
- ✅ **PUT**: Implemented in:
  - `bot/bot_store.py`

#### /cloud/appstore/search

- ✅ **GET**: Implemented in:
  - `bot/bot_store.py`

#### /cloud/developer/apps

- ✅ **GET**: Implemented in:
  - `bot/bot_developer.py`
- ✅ **PUT**: Implemented in:
  - `bot/bot_developer.py`

#### /cloud/developer/cloudwatchlog

- ✅ **GET**: Implemented in:
  - `bot/bot_developer.py`
- ✅ **PUT**: Implemented in:
  - `bot/bot_developer.py`

#### /cloud/developer/cloudwatchlog/export

- ✅ **GET**: Implemented in:
  - `bot/bot_developer.py`
- ✅ **POST**: Implemented in:
  - `bot/bot_developer.py`

#### /cloud/developer/executionHistory

- ✅ **GET**: Implemented in:
  - `bot/bot_developer.py`

#### /cloud/developer/messageTopics

- ✅ **PUT**: Implemented in:
  - `bot/bot_developer.py`

#### /cloud/developer/objects/{name}

- ✅ **PUT**: Implemented in:
  - `bot/bot_developer.py`

#### /cloud/developer/stats

- ✅ **GET**: Implemented in:
  - `bot/bot_developer.py`

#### /cloud/developer/teams

- ✅ **GET**: Implemented in:
  - `bot/developer_teams.py`
- ✅ **POST**: Implemented in:
  - `bot/developer_teams.py`

#### /cloud/developer/teams/{teamName}

- ✅ **DELETE**: Implemented in:
  - `bot/developer_teams.py`
- ✅ **POST**: Implemented in:
  - `bot/developer_teams.py`

#### /cloud/developer/teams/{teamName}/secrets

- ✅ **DELETE**: Implemented in:
  - `bot/developer_teams.py`
- ✅ **GET**: Implemented in:
  - `bot/developer_teams.py`
- ✅ **PUT**: Implemented in:
  - `bot/developer_teams.py`

#### /cloud/developer/upload

- ✅ **POST**: Implemented in:
  - `bot/bot_developer.py`

#### /cloud/developer/upload/{requestId}

- ✅ **GET**: Implemented in:
  - `bot/bot_developer.py`

#### /cloud/developer/versionStatus

- ✅ **PUT**: Implemented in:
  - `bot/bot_developer.py`

#### /cloud/developer/versions

- ✅ **DELETE**: Implemented in:
  - `bot/bot_developer.py`
- ✅ **GET**: Implemented in:
  - `bot/bot_developer.py`
- ✅ **PUT**: Implemented in:
  - `bot/bot_developer.py`

#### /deviceio/analytic

- ✅ **GET**: Implemented in:
  - `bot/execution.py`

### cloud.yaml

#### /auth/authorize/{appId}

- ✅ **GET**: Implemented in:
  - `app/clouds_integration.py`

#### /cloud/appstore/stream

- ✅ **POST**: Implemented in:
  - `app/locations.py`
  - `bot/bot_store.py`

#### /cloud/appstore/summary

- ✅ **GET**: Implemented in:
  - `app/locations.py`
  - `bot/bot_store.py`

#### /cloud/json/alerts

- ✅ **GET**: Implemented in:
  - `app/device_measurements.py`

#### /cloud/json/appfiles

- ✅ **GET**: Implemented in:
  - `app/app_files.py`
- ✅ **POST**: Implemented in:
  - `app/app_files.py`

#### /cloud/json/appfiles/{fileId}

- ✅ **DELETE**: Implemented in:
  - `app/app_files.py`
- ✅ **GET**: Implemented in:
  - `app/app_files.py`

#### /cloud/json/appfiles/{fileId}/url

- ✅ **GET**: Implemented in:
  - `app/app_files.py`

#### /cloud/json/authClient

- ✅ **DELETE**: Implemented in:
  - `app/clouds_integration.py`
- ✅ **POST**: Implemented in:
  - `app/clouds_integration.py`

#### /cloud/json/authToken

- ✅ **GET**: Implemented in:
  - `app/authentication.py`

#### /cloud/json/authorizations/{authId}

- ✅ **DELETE**: Implemented in:
  - `app/clouds_integration.py`

#### /cloud/json/authorize

- ✅ **GET**: Implemented in:
  - `app/clouds_integration.py`

#### /cloud/json/badges

- ✅ **PUT**: Implemented in:
  - `app/user_accounts.py`

#### /cloud/json/callCenter

- ✅ **DELETE**: Implemented in:
  - `app/professional_monitoring.py`
- ✅ **GET**: Implemented in:
  - `app/professional_monitoring.py`
- ✅ **PUT**: Implemented in:
  - `app/professional_monitoring.py`

#### /cloud/json/callCenterAlerts

- ✅ **GET**: Implemented in:
  - `app/professional_monitoring.py`

#### /cloud/json/callCenterTest

- ✅ **DELETE**: Implemented in:
  - `app/professional_monitoring.py`
- ✅ **POST**: Implemented in:
  - `app/professional_monitoring.py`

#### /cloud/json/communityPostComments

- ✅ **DELETE**: Implemented in:
  - `app/community.py`
- ✅ **POST**: Implemented in:
  - `app/community.py`

#### /cloud/json/communityPostReaction

- ✅ **PUT**: Implemented in:
  - `app/community.py`

#### /cloud/json/communityPosts

- ✅ **DELETE**: Implemented in:
  - `app/community.py`
- ✅ **GET**: Implemented in:
  - `app/community.py`
- ✅ **POST**: Implemented in:
  - `app/community.py`
- ✅ **PUT**: Implemented in:
  - `app/community.py`

#### /cloud/json/communityPosts/{postId}/files

- ✅ **DELETE**: Implemented in:
  - `app/community.py`
- ✅ **GET**: Implemented in:
  - `app/community.py`
- ✅ **POST**: Implemented in:
  - `app/community.py`
- ✅ **PUT**: Implemented in:
  - `app/community.py`

#### /cloud/json/countries

- ✅ **GET**: Implemented in:
  - `app/locations.py`

#### /cloud/json/dataRequests

- ✅ **GET**: Implemented in:
  - `app/device_measurements.py`
- ✅ **POST**: Implemented in:
  - `app/device_measurements.py`

#### /cloud/json/deviceLogContent

- ✅ **GET**: Implemented in:
  - `app/devices.py`

#### /cloud/json/deviceLogs

- ✅ **GET**: Implemented in:
  - `app/devices.py`

#### /cloud/json/deviceParameters

- ✅ **GET**: Implemented in:
  - `app/device_types_and_parameters.py`
- ✅ **POST**: Implemented in:
  - `app/device_types_and_parameters.py`

#### /cloud/json/deviceParameters/{parameterName}

- ✅ **DELETE**: Implemented in:
  - `app/device_types_and_parameters.py`

#### /cloud/json/deviceType

- ✅ **POST**: Implemented in:
  - `app/device_types_and_parameters.py`

#### /cloud/json/deviceType/{deviceTypeId}

- ✅ **PUT**: Implemented in:
  - `app/device_types_and_parameters.py`

#### /cloud/json/deviceType/{deviceTypeId}/goals

- ✅ **GET**: Implemented in:
  - `app/device_types_and_parameters.py`

#### /cloud/json/deviceType/{deviceTypeId}/rules

- ✅ **GET**: Implemented in:
  - `app/device_types_and_parameters.py`

#### /cloud/json/deviceType/{deviceTypeId}/rules/{ruleId}

- ✅ **DELETE**: Implemented in:
  - `app/device_types_and_parameters.py`
- ✅ **POST**: Implemented in:
  - `app/device_types_and_parameters.py`

#### /cloud/json/deviceTypeAttrs

- ✅ **GET**: Implemented in:
  - `app/device_types_and_parameters.py`

#### /cloud/json/deviceTypes

- ✅ **GET**: Implemented in:
  - `app/device_types_and_parameters.py`

#### /cloud/json/devicemodels

- ✅ **DELETE**: Implemented in:
  - `app/device_types_and_parameters.py`
- ✅ **GET**: Implemented in:
  - `app/device_types_and_parameters.py`
- ✅ **PUT**: Implemented in:
  - `app/device_types_and_parameters.py`

#### /cloud/json/devices

- ✅ **DELETE**: Implemented in:
  - `app/devices.py`
- ✅ **GET**: Implemented in:
  - `app/devices.py`
- ✅ **POST**: Implemented in:
  - `app/devices.py`

#### /cloud/json/devices/{deviceId}

- ✅ **GET**: Implemented in:
  - `app/devices.py`

#### /cloud/json/devices/{deviceId}/currentEnergyUsage

- ✅ **GET**: Implemented in:
  - `app/energy_management.py`

#### /cloud/json/devices/{deviceId}/energyUsage/{aggregation}/{startDate}

- ✅ **GET**: Implemented in:
  - `app/energy_management.py`

#### /cloud/json/devices/{deviceId}/parameters

- ✅ **GET**: Implemented in:
  - `app/device_measurements.py`
- ✅ **PUT**: Implemented in:
  - `app/device_measurements.py`

#### /cloud/json/devices/{deviceId}/parametersByCount/{rowCount}

- ✅ **GET**: Implemented in:
  - `app/device_measurements.py`

#### /cloud/json/devices/{deviceId}/parametersByDate/{startDate}

- ✅ **GET**: Implemented in:
  - `app/device_measurements.py`

#### /cloud/json/devices/{deviceId}/properties

- ✅ **DELETE**: Implemented in:
  - `app/devices.py`
- ✅ **GET**: Implemented in:
  - `app/devices.py`
- ✅ **POST**: Implemented in:
  - `app/devices.py`

#### /cloud/json/devices/{deviceId}/sensitivityMap

- ✅ **DELETE**: Implemented in:
  - `app/devices.py`
- ✅ **POST**: Implemented in:
  - `app/devices.py`

#### /cloud/json/devices/{deviceId}/services

- ✅ **GET**: Implemented in:
  - `app/devices.py`

#### /cloud/json/devices/{deviceId}/voip

- ✅ **DELETE**: Implemented in:
  - `app/devices.py`
- ✅ **POST**: Implemented in:
  - `app/devices.py`

#### /cloud/json/devices/{deviceId}/voipCall

- ✅ **DELETE**: Implemented in:
  - `app/devices.py`
- ✅ **PUT**: Implemented in:
  - `app/devices.py`

#### /cloud/json/emailVerificationMessage

- ✅ **GET**: Implemented in:
  - `app/user_accounts.py`
- ✅ **PUT**: Implemented in:
  - `app/user_accounts.py`

#### /cloud/json/feedback

- ✅ **POST**: Implemented in:
  - `app/user_communication.py`

#### /cloud/json/feedback/{appName}/{type}

- ✅ **GET**: Implemented in:
  - `app/user_communication.py`

#### /cloud/json/feedback/{feedbackId}

- ✅ **GET**: Implemented in:
  - `app/user_communication.py`

#### /cloud/json/feedback/{feedbackId}/{rank}

- ✅ **PUT**: Implemented in:
  - `app/user_communication.py`

#### /cloud/json/fileDevices

- ✅ **GET**: Implemented in:
  - `app/device_files.py`

#### /cloud/json/files

- ✅ **DELETE**: Implemented in:
  - `app/device_files.py`
- ✅ **GET**: Implemented in:
  - `app/device_files.py`
- ✅ **POST**: Implemented in:
  - `app/device_files.py`

#### /cloud/json/files/{fileId}

- ✅ **DELETE**: Implemented in:
  - `app/device_files.py`
- ✅ **GET**: Implemented in:
  - `app/device_files.py`
- ✅ **POST**: Implemented in:
  - `app/device_files.py`
- ✅ **PUT**: Implemented in:
  - `app/device_files.py`

#### /cloud/json/files/{fileId}/report/{reportType}

- ✅ **PUT**: Implemented in:
  - `app/device_files.py`

#### /cloud/json/files/{fileId}/url

- ✅ **GET**: Implemented in:
  - `app/device_files.py`

#### /cloud/json/filesByCount/{count}

- ✅ **GET**: Implemented in:
  - `app/device_files.py`

#### /cloud/json/filesInfo/{fileId}

- ✅ **GET**: Implemented in:
  - `app/device_files.py`

#### /cloud/json/filesSummary/{aggregation}

- ✅ **GET**: Implemented in:
  - `app/device_files.py`

#### /cloud/json/fwupdate

- ✅ **GET**: Implemented in:
  - `app/devices.py`
- ✅ **PUT**: Implemented in:
  - `app/devices.py`

#### /cloud/json/goals/{goalId}/installation

- ✅ **GET**: Implemented in:
  - `app/device_types_and_parameters.py`

#### /cloud/json/location

- ✅ **POST**: Implemented in:
  - `app/locations.py`

#### /cloud/json/location/{locationId}

- ✅ **DELETE**: Implemented in:
  - `app/locations.py`
- ✅ **PUT**: Implemented in:
  - `app/locations.py`

#### /cloud/json/location/{locationId}/event/{eventName}

- ✅ **POST**: Implemented in:
  - `app/locations.py`

#### /cloud/json/location/{locationId}/events

- ✅ **GET**: Implemented in:
  - `app/locations.py`

#### /cloud/json/location/{locationId}/organization/{domainName}

- ✅ **PUT**: Implemented in:
  - `app/locations.py`

#### /cloud/json/location/{locationId}/priorities

- ✅ **GET**: Implemented in:
  - `app/locations.py`

#### /cloud/json/location/{locationId}/spaces

- ✅ **DELETE**: Implemented in:
  - `app/locations.py`
- ✅ **GET**: Implemented in:
  - `app/locations.py`
- ✅ **POST**: Implemented in:
  - `app/locations.py`

#### /cloud/json/location/{locationId}/subs

- ✅ **DELETE**: Implemented in:
  - `app/locations.py`
- ✅ **PUT**: Implemented in:
  - `app/locations.py`

#### /cloud/json/location/{locationId}/users

- ✅ **DELETE**: Implemented in:
  - `app/locations.py`
- ✅ **GET**: Implemented in:
  - `app/locations.py`
- ✅ **POST**: Implemented in:
  - `app/locations.py`
- ✅ **PUT**: Implemented in:
  - `app/locations.py`

#### /cloud/json/locationTotals

- ✅ **GET**: Implemented in:
  - `app/locations.py`

#### /cloud/json/locations/{locationId}/deviceActivation/{deviceType}

- ✅ **GET**: Implemented in:
  - `app/devices.py`

#### /cloud/json/locations/{locationId}/devices/{deviceId}

- ✅ **DELETE**: Implemented in:
  - `app/devices.py`
- ✅ **PUT**: Implemented in:
  - `app/devices.py`

#### /cloud/json/locations/{locationId}/devices/{deviceId}/copySimulator

- ✅ **POST**: Implemented in:
  - `app/devices.py`

#### /cloud/json/locations/{locationId}/devices/{deviceId}/simCard

- ✅ **PUT**: Implemented in:
  - `app/devices.py`

#### /cloud/json/locations/{locationId}/devices/{deviceId}/spaces/{spaceId}

- ✅ **DELETE**: Implemented in:
  - `app/devices.py`
- ✅ **PUT**: Implemented in:
  - `app/devices.py`

#### /cloud/json/locations/{locationId}/energyUsage/{aggregation}/{startDate}

- ✅ **GET**: Implemented in:
  - `app/energy_management.py`

#### /cloud/json/locations/{locationId}/narratives

- ✅ **DELETE**: Implemented in:
  - `app/locations.py`
- ✅ **GET**: Implemented in:
  - `app/locations.py`
- ✅ **PUT**: Implemented in:
  - `app/locations.py`

#### /cloud/json/locations/{locationId}/state

- ✅ **DELETE**: Implemented in:
  - `app/locations.py`
- ✅ **GET**: Implemented in:
  - `app/locations.py`
- ✅ **PUT**: Implemented in:
  - `app/locations.py`

#### /cloud/json/locations/{locationId}/timeStates

- ✅ **GET**: Implemented in:
  - `app/locations.py`
- ✅ **PUT**: Implemented in:
  - `app/locations.py`

#### /cloud/json/login

- ✅ **GET**: Implemented in:
  - `app/authentication.py`

#### /cloud/json/loginByKey

- ✅ **GET**: Implemented in:
  - `app/authentication.py`

#### /cloud/json/logout

- ✅ **GET**: Implemented in:
  - `app/authentication.py`

#### /cloud/json/media

- ✅ **DELETE**: Implemented in:
  - `app/device_types_and_parameters.py`
- ✅ **GET**: Implemented in:
  - `app/device_types_and_parameters.py`
- ✅ **PUT**: Implemented in:
  - `app/device_types_and_parameters.py`

#### /cloud/json/messageRead

- ✅ **PUT**: Implemented in:
  - `app/user_communication.py`

#### /cloud/json/messageTopics

- ✅ **GET**: Implemented in:
  - `app/user_communication.py`

#### /cloud/json/messages

- ✅ **GET**: Implemented in:
  - `app/user_communication.py`
- ✅ **POST**: Implemented in:
  - `app/user_communication.py`
- ✅ **PUT**: Implemented in:
  - `app/user_communication.py`

#### /cloud/json/newPassword

- ✅ **GET**: Implemented in:
  - `app/user_accounts.py`
- ✅ **PUT**: Implemented in:
  - `app/user_accounts.py`

#### /cloud/json/notificationSubscriptions

- ✅ **GET**: Implemented in:
  - `app/user_communication.py`

#### /cloud/json/notificationSubscriptions/{type}

- ✅ **PUT**: Implemented in:
  - `app/user_communication.py`

#### /cloud/json/notificationToken/{appName}/{token}

- ✅ **PUT**: Implemented in:
  - `app/user_communication.py`

#### /cloud/json/notificationToken/{token}

- ✅ **DELETE**: Implemented in:
  - `app/user_communication.py`

#### /cloud/json/notifications

- ✅ **GET**: Implemented in:
  - `app/user_communication.py`
- ✅ **POST**: Implemented in:
  - `app/user_communication.py`

#### /cloud/json/parameters

- ✅ **GET**: Implemented in:
  - `app/device_measurements.py`
- ✅ **PUT**: Implemented in:
  - `app/device_measurements.py`

#### /cloud/json/passcode

- ✅ **GET**: Implemented in:
  - `app/authentication.py`

#### /cloud/json/preregistered/{deviceId}

- ✅ **GET**: Implemented in:
  - `app/devices.py`

#### /cloud/json/pronouns

- ✅ **GET**: Implemented in:
  - `app/user_accounts.py`

#### /cloud/json/questions

- ✅ **GET**: Implemented in:
  - `app/user_communication.py`
- ✅ **PUT**: Implemented in:
  - `app/user_communication.py`

#### /cloud/json/receipt/apple

- ✅ **POST**: Implemented in:
  - `app/paid_services.py`

#### /cloud/json/ruleConditions

- ✅ **GET**: Implemented in:
  - `app/rules.py`

#### /cloud/json/rules

- ✅ **DELETE**: Implemented in:
  - `app/rules.py`
- ✅ **GET**: Implemented in:
  - `app/rules.py`
- ✅ **POST**: Implemented in:
  - `app/rules.py`

#### /cloud/json/rules/{ruleId}

- ✅ **DELETE**: Implemented in:
  - `app/rules.py`
- ✅ **PUT**: Implemented in:
  - `app/rules.py`

#### /cloud/json/rules/{ruleId}/attrs

- ✅ **PUT**: Implemented in:
  - `app/rules.py`

#### /cloud/json/rulesStatus/{status}

- ✅ **PUT**: Implemented in:
  - `app/rules.py`

#### /cloud/json/servicePlans

- ✅ **GET**: Implemented in:
  - `app/paid_services.py`

#### /cloud/json/settings

- ✅ **GET**: Implemented in:
  - `app/cloud_connectivity.py`

#### /cloud/json/settingsCloud

- ✅ **GET**: Implemented in:
  - `app/cloud_connectivity.py`

#### /cloud/json/settingsServer

- ✅ **GET**: Implemented in:
  - `app/cloud_connectivity.py`

#### /cloud/json/settingsServer/{type}

- ✅ **GET**: Implemented in:
  - `app/cloud_connectivity.py`

#### /cloud/json/signatureKey

- ✅ **GET**: Implemented in:
  - `app/authentication.py`
- ✅ **PUT**: Implemented in:
  - `app/authentication.py`

#### /cloud/json/stories

- ✅ **DELETE**: Implemented in:
  - `app/device_types_and_parameters.py`
- ✅ **GET**: Implemented in:
  - `app/device_types_and_parameters.py`
- ✅ **PUT**: Implemented in:
  - `app/device_types_and_parameters.py`

#### /cloud/json/support

- ✅ **POST**: Implemented in:
  - `app/user_communication.py`

#### /cloud/json/surveyAnswers

- ✅ **GET**: Implemented in:
  - `app/user_communication.py`
- ✅ **POST**: Implemented in:
  - `app/user_communication.py`

#### /cloud/json/surveyQuestions

- ✅ **GET**: Implemented in:
  - `app/user_communication.py`
- ✅ **PUT**: Implemented in:
  - `app/user_communication.py`

#### /cloud/json/systemProperty/{propertyName}

- ✅ **GET**: Implemented in:
  - `app/system_and_user_properties.py`

#### /cloud/json/termsOfServices

- ✅ **GET**: Implemented in:
  - `app/user_accounts.py`

#### /cloud/json/termsOfServices/{signatureId}

- ✅ **PUT**: Implemented in:
  - `app/user_accounts.py`

#### /cloud/json/ticket

- ✅ **POST**: Implemented in:
  - `app/user_communication.py`

#### /cloud/json/token

- ✅ **GET**: Implemented in:
  - `app/authentication.py`

#### /cloud/json/totp

- ✅ **DELETE**: Implemented in:
  - `app/authentication.py`
- ✅ **GET**: Implemented in:
  - `app/authentication.py`
- ✅ **POST**: Implemented in:
  - `app/authentication.py`
- ✅ **PUT**: Implemented in:
  - `app/authentication.py`

#### /cloud/json/units

- ✅ **GET**: Implemented in:
  - `app/device_measurements.py`

#### /cloud/json/user

- ✅ **DELETE**: Implemented in:
  - `app/user_accounts.py`
- ✅ **GET**: Implemented in:
  - `app/user_accounts.py`
- ✅ **POST**: Implemented in:
  - `app/user_accounts.py`
- ✅ **PUT**: Implemented in:
  - `app/user_accounts.py`

#### /cloud/json/userCodes

- ✅ **DELETE**: Implemented in:
  - `app/user_accounts.py`
- ✅ **GET**: Implemented in:
  - `app/user_accounts.py`
- ✅ **PUT**: Implemented in:
  - `app/user_accounts.py`

#### /cloud/json/userProperties

- ✅ **GET**: Implemented in:
  - `app/system_and_user_properties.py`
- ✅ **POST**: Implemented in:
  - `app/system_and_user_properties.py`

#### /cloud/json/userProperty/{name}

- ✅ **GET**: Implemented in:
  - `app/system_and_user_properties.py`
- ✅ **PUT**: Implemented in:
  - `app/system_and_user_properties.py`

#### /cloud/json/userServicePlanTransactions/{userServicePlanId}

- ✅ **GET**: Implemented in:
  - `app/paid_services.py`

#### /cloud/json/userServicePlans

- ✅ **GET**: Implemented in:
  - `app/paid_services.py`

#### /cloud/json/userServicePlans/{servicePlanId}

- ✅ **DELETE**: Implemented in:
  - `app/paid_services.py`
- ✅ **POST**: Implemented in:
  - `app/paid_services.py`

#### /cloud/json/usertags/{tag}

- ✅ **DELETE**: Implemented in:
  - `app/user_accounts.py`
- ✅ **PUT**: Implemented in:
  - `app/user_accounts.py`

#### /cloud/json/weather/current/geocode/{latitude}/{longitude}

- ✅ **GET**: Implemented in:
  - `app/weather.py`

#### /cloud/json/weather/current/location/{locationId}

- ✅ **GET**: Implemented in:
  - `app/weather.py`

#### /cloud/json/weather/forecast/geocode/{latitude}/{longitude}

- ✅ **GET**: Implemented in:
  - `app/weather.py`

#### /cloud/json/weather/forecast/location/{locationId}

- ✅ **GET**: Implemented in:
  - `app/weather.py`

#### /espapi/oauth/approve/{approved}

- ✅ **GET**: Implemented in:
  - `app/clouds_integration.py`

#### /espapi/oauth/authorize/{brand}

- ✅ **GET**: Implemented in:
  - `app/clouds_integration.py`

#### /espapi/oauth/token

- ✅ **POST**: Implemented in:
  - `app/clouds_integration.py`

#### /espapi/version

- ✅ **GET**: Implemented in:
  - `app/cloud_connectivity.py`

#### /espapi/watch

- ✅ **GET**: Implemented in:
  - `app/cloud_connectivity.py`


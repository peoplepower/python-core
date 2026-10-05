All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.3] - 2026-10-05

### Added
- Locations: `get_escalations`, `create_escalation`, and `update_escalation`
  for the new `/cloud/json/escalations` endpoints
- Locations: `escalation_id` filter on `get_narratives`; narratives can carry an
  `escalationId` in `put_narrative`

### Changed
- API specs (cloud, admin, bots) updated to server API v65
- DeviceTypesAndParameters: `add_default_rule` now requires `location_id`
  (breaking)

### Removed
- Weather API class (all `/cloud/json/weather/...` endpoints removed from the spec)
- Admin Challenges API class (`/admin/json/organizations/{organizationId}/challenges...`)
- Bot Analytic: `get_challenge_participants` (`/analytic/admin/challenges/{challengeId}/participants`)
- UserAccounts: `put_user_code`, `get_user_codes`, `delete_user_code` (`/cloud/json/userCodes`)
- DeviceTypesAndParameters: `simple` and `organization_id` on `get_device_types`
- PaidServices: `get_card` on `get_location_service_plans`

## [1.0.2] - 2026-09-11

### Added
- Admin Users: `get_notification_assignments` and `update_notification_assignments`
  for the new `/admin/json/organizations/{organizationId}/notificationAssignments`
  endpoints (replace the removed bot store botNotifications endpoints)
- Locations: `store` parameter on `put_narrative` (publish-only narratives)
- Admin Reports: `sub_orgs` and `demand_user_id` filters on `get_report_executions`

### Changed
- API specs (cloud, admin, bots) updated to server API v63
- Bot Analytic: `send_ai_request` rewritten for the new AI agents contract —
  takes `message`, `conversation_id`, `request_id`, `location_id`, `timeout_ms`
  instead of `model_name`/`ai_data`/`key` (breaking)

### Removed
- Bot BotStore: `get_bot_notifications` and `update_bot_notifications`
  (`/cloud/appstore/botNotifications/{organizationId}` removed from the v63 spec;
  use the admin notificationAssignments APIs instead)

## [1.0.0] - 2026-01-11

### Added
- Initial release of CareDaily Python SDK
- Comprehensive API client for CareDaily cloud platform
- CLI tool (`caredaily`) for device and account management
- Support for App APIs: Authentication, UserAccounts, Locations, Devices, DeviceMeasurements, and more
- Support for Admin APIs: System, Organizations, Users, Groups, Billing, and more
- Support for Bot APIs: BotDeveloper, DeveloperTeams, BotStore
- Support for Service APIs: AI, Questions, Tags, Variables, VoiceCalls
- Support for Device APIs: Execution
- Profile-based configuration system with `~/.caredaily/config` and `~/.caredaily/credentials`
- RestAdapter HTTP client with standardized error handling
- Pydantic models for type-safe API responses
- Full test suite with 86 tests and pytest-cov integration
- Comprehensive README with installation and usage examples
- CLI commands: `configure`, `ping`, `login`, `cloud-connectivity`
- Support for multiple API key types (User, Admin, Analytic)
- SSL verification and proxy support
- Modern src-layout package structure
- Apache 2.0 license

### Documentation
- Complete API reference documentation links
- Detailed CLAUDE.md for development guidance
- Contributing guidelines (CONTRIBUTING.md)
- Code of Conduct (CODE_OF_CONDUCT.md)
- Installation and quick start guide
- SDK and CLI usage examples

[Unreleased]: https://github.com/peoplepower/python-core/compare/v1.0.2...HEAD
[1.0.2]: https://github.com/peoplepower/python-core/compare/v1.0.0...v1.0.2
[1.0.0]: https://github.com/peoplepower/python-core/releases/tag/v1.0.0
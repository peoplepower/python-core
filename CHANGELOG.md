All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/peoplepower/python-core/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/peoplepower/python-core/releases/tag/v1.0.0
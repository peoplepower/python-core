# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is `caredaily`, a Python SDK and CLI tool for interacting with the CareDaily API (powered by People Power Company). It provides both programmatic access via Python classes and a command-line interface for managing CareDaily cloud services.

The project consists of:
- **SDK**: Python classes for making API calls to CareDaily services
- **CLI**: Command-line tool (`caredaily`) for configuration and API interaction
- **Models**: Pydantic models for type-safe API responses

## Development Commands

### Virtual Environment

Before working on the project, create and activate a Python virtual environment:

```bash
# Create a virtual environment if it doesn't exist
python -m venv venv

# Activate the virtual environment (on Unix or macOS)
source venv/bin/activate

# On Windows, use:
venv\Scripts\activate
```



### Setup
```bash
# Install package in development mode with dev dependencies
pip install -e ".[dev]"
```

### Testing
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=caredaily --cov-report=html

# Run specific test file
pytest tests/caredaily/apis/app/test_authentication.py

# Run specific test class or method
pytest tests/caredaily/apis/app/test_authentication.py::TestAuthentication::test_login_by_username
```

### Code Quality
```bash
# Run ruff linter
ruff check src/

# Auto-fix linting issues
ruff check --fix src/

# Format code with ruff
ruff format src/

# Check formatting without changes
ruff format --check src/
```

### Building
```bash
# Build distribution packages
python -m build

# Install built package locally
pip install dist/caredaily-*.whl
```

### CLI Usage
```bash
# Initialize configuration
caredaily configure init

# Interactive profile configuration
caredaily configure interactive --profile myprofile

# Check API connectivity
caredaily ping

# Login with credentials
caredaily login --username user --password pass

# Check cloud connectivity
caredaily cloud-connectivity --check-availability
```

## Architecture

### Configuration System

The SDK uses a profile-based configuration system stored in `~/.caredaily/`:
- **config**: Contains hostname, SSL verification, and proxy settings
- **credentials**: Contains API keys and key types (separate from config for security)

Profiles are loaded via:
1. `--profile` CLI flag
2. `CAREDAILY_PROFILE` environment variable
3. Falls back to `default` profile

### Core Components

**CareDaily** (`caredaily.py`): Main entry point class that:
- Loads configuration from `~/.caredaily/config` and `~/.caredaily/credentials`
- Provides factory methods for API instances: `app_api()`, `admin_api()`, `bot_api()`
- Manages authentication and connection configuration

**RestAdapter** (`http.py`): HTTP client wrapper that:
- Handles all HTTP methods (GET, POST, PUT, DELETE)
- Manages API key authentication via headers (API_KEY, ADMIN_KEY, ANALYTIC_API_KEY)
- Provides consistent error handling and result parsing
- All API responses are wrapped in `Result` objects with standardized error codes

**API Classes** (`apis/`): Organized by API type:
- **app/**: User-facing app APIs (Authentication, Locations, Devices, DeviceMeasurements, UserCommunication, Rules, Weather, RAG, etc.)
- **admin/**: Administrative APIs (System, Organizations, Users, AdminDevices, AdminLocations, Billing, Firmware, Reports, etc.)
- **bot/**: Bot developer APIs (BotDeveloper, BotStore, DeveloperTeams, Analytic, Execution)

All API classes inherit from `API` base class which initializes the `RestAdapter`.

**Models** (`models.py`): Pydantic models for:
- `Result`: Standard API response wrapper with result_code, result_code_message, and data
- `ResultCode`: Enum of all possible API error codes (0=SUCCESS, 2=WRONG_API_KEY, etc.)
- `APIKeyType`: Enum for key types (USER=1, ADMIN=2, ANALYTIC=3)
- Domain models like `Cloud`, `Server`, `MQTT`, etc.

### API Pattern

Every API endpoint follows this pattern:
1. API class method accepts typed parameters
2. Constructs endpoint URL and parameters
3. Calls `self.adapter.get/post/put/delete()`
4. RestAdapter handles HTTP request and response parsing
5. Returns `Result` object with parsed data or raises `CareDailyException`

Example:
```python
def get_cloud_settings(self, device_id: str = None, connected: bool = None):
    params = {k: v for k, v in {"device_id": device_id, "connected": connected}.items() if v is not None}
    result: Result = self.adapter.get("/espapi/cloud/json/settings", ep_params=params)
    return result
```

### Testing Pattern

Tests use `unittest` with mocked `RestAdapter`:
- Mock the `adapter` attribute on API instances
- Configure mock return values for HTTP methods
- Assert correct endpoint/params were called
- Verify return value matches expected result

### CLI Architecture

Built with Click framework:
- Main group command: `app()` initializes CareDaily instance and stores in context
- Subcommands access `ctx.obj["caredaily"]` for API calls
- `configure` subgroup handles profile management
- Each command corresponds to one or more API calls

## Important Patterns

### Error Handling
- API errors raise `CareDailyException` with message and optional context dict
- RestAdapter automatically raises exception for non-SUCCESS result codes
- CLI commands should catch exceptions and display user-friendly messages

### API Key Types
Three authentication types based on use case:
- **USER (1)**: Regular user API key (header: API_KEY)
- **ADMIN (2)**: Administrative access (header: ADMIN_KEY)
- **ANALYTIC (3)**: Analytics/reporting access (header: ANALYTIC_API_KEY)

### Profile Management
- Use `raise_errors=False` when instantiating CareDaily in CLI to allow graceful handling of missing config
- Use `raise_errors=True` (default) when using as SDK to fail fast on misconfiguration

### Parameter Filtering
Remove None values from parameters before passing to RestAdapter:
```python
params = {k: v for k, v in params.items() if v is not None}
```

## Code Style

- Line length: 88 characters (Black-compatible)
- Python version: 3.10+ required, 3.14 supported
- Use double quotes for strings
- Use trailing commas in multi-line structures
- Ruff handles both linting and formatting
- PEP 585 style type hints preferred (e.g., `list[str]` over `List[str]`)

## Project Structure

```
├── CHANGELOG.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE.txt
├── README.md
├── docs
│   ├── ACCEPTANCE_CRITERIA.md
│   ├── CARE_DAILY_APIS.md
│   ├── CLAUDE.md
│   ├── COVERAGE_REPORT_MAINTENANCE.md
│   ├── Doxyfile
│   ├── acceptance
│   │   └── apis
│   └── api
│       ├── admin.yaml
│       ├── bots.yaml
│       └── cloud.yaml
├── img
│   ├── caredaily-logo-horiz-dark.svg
│   └── caredaily-logo-horiz.svg
├── pyproject.toml
├── src
│   └── caredaily
│       ├── __init__.py
│       ├── __main__.py
│       ├── apis
│       ├── caredaily.py
│       ├── cli
│       ├── exceptions.py
│       ├── http.py
│       └── models.py
└── tests
    ├── API_TEST_COVERAGE_REPORT.md
    ├── ENDPOINT_IMPLEMENTATION_REPORT.md
    ├── __init__.py
    ├── caredaily
    │   ├── __init__.py
    │   ├── apis
    │   ├── cli
    │   ├── test_caredaily.py
    │   └── test_http.py
    ├── check_endpoint_implementation.py
    └── generate_coverage_report.py
```

## Available Claude Agents

This project includes specialized Claude agents in `.claude/agents/`:

- **developer-agent**: Use this agent when you need to implement features, review code, design architecture, write tests, debug issues, refactor code, or create technical documentation. This agent should be launched proactively during development workflows. Examples: code reviews after feature implementation, architectural design for new features, debugging production issues, refactoring technical debt.

- **qa-specialist**: Use this agent when you need comprehensive quality assurance expertise for testing strategies, test case development, bug analysis, or coverage assessment. Examples: creating test cases for new features, reviewing user stories for testability, documenting and analyzing bugs, identifying test scenarios for high-risk features, performing coverage analysis before releases.

These agents can be invoked using the Task tool when you need specialized expertise in development or quality assurance workflows. Each agent has deep domain knowledge and follows project-specific patterns and standards.

## API Documentation

Official API documentation: https://app.peoplepowerco.com/cloud/apidocs/cloud.html

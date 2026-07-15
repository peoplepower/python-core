# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`caredaily` is a Python SDK and CLI for the CareDaily API (powered by People Power Company). It has three parts:

- **SDK**: `CareDaily` entry-point class plus per-domain API classes under `src/caredaily/apis/`
- **CLI**: `caredaily` command built with Click (`src/caredaily/cli/`)
- **Models**: Pydantic models and enums in `src/caredaily/models.py`

Official API documentation: https://app.peoplepowerco.com/cloud/apidocs/cloud.html

## Development Commands

Use a virtual environment (`python -m venv venv && source venv/bin/activate`), then:

```bash
# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Optional extras: websockets, rsa (cryptography for RSA key auth)
pip install -e ".[dev,websockets,rsa]"

# Run all tests
pytest

# Run a single file / class / method
pytest tests/caredaily/apis/app/test_authentication.py
pytest tests/caredaily/apis/app/test_authentication.py::TestAuthentication::test_login_by_username

# Coverage
pytest --cov=caredaily --cov-report=html

# Lint / format (ruff handles both)
ruff check src/
ruff check --fix src/
ruff format src/

# Build distribution packages
python -m build
```

## Architecture

### Request flow

Every API call follows the same path:

1. An API class method (e.g. `Authentication.login_by_username`) accepts typed parameters, filters out `None` values, and builds the endpoint path (typically `/cloud/json/...` for app APIs, `/admin/json/...` for admin, `/botengine/json/...` for bots).
2. It calls `self.adapter.get/post/put/delete()` on the `RestAdapter` (`src/caredaily/http.py`).
3. `RestAdapter` attaches the auth header based on `APIKeyType` — `API_KEY` (USER=1), `ADMIN_KEY` (ADMIN=2), or `ANALYTIC_API_KEY` (ANALYTIC=3) — sends the request, and parses the response into a `Result` (Pydantic model with `result_code`, `result_code_message`, and data).
4. Non-SUCCESS result codes raise `CareDailyException` (message + optional context dict). `ResultCode` in `models.py` enumerates all API error codes.

All API classes inherit from `API` (`src/caredaily/apis/api.py`), which constructs the `RestAdapter` from the config dict.

### CareDaily entry point and factory methods

`CareDaily` (`src/caredaily/caredaily.py`) loads configuration and hands out API instances. The factory methods take the API **class** and return a configured instance:

```python
from caredaily import CareDaily
from caredaily.apis.app import Authentication

cd = CareDaily(profile="myprofile")
auth = cd.app_api(Authentication)   # also: cd.admin_api(...), cd.bot_api(...)
```

Each factory (`app_api`, `admin_api`, `bot_api`) is an explicit if-chain over known classes and returns `None` for unknown types. **When adding a new API class**, you must (1) create it under the right `apis/` subpackage, (2) export it from `apis/__init__.py`, and (3) add it to the matching factory chain in `caredaily.py`.

API subpackages:
- `apis/app/` — user-facing APIs (Authentication, Locations, Devices, DeviceMeasurements, Rules, Weather, RAG, Websocket, ...)
- `apis/admin/` — administrative APIs (System, Organizations, Users, Billing, Firmware, Reports, ...)
- `apis/bot/` — bot developer APIs (BotDeveloper, BotStore, DeveloperTeams, Analytic, Execution)

### Configuration system

Profile-based INI files under `~/.caredaily/` (directory overridable via `CAREDAILY_INTEGRATION_PATH`):
- **config**: hostname, `ssl_verify`, proxies
- **credentials**: API keys and key types (kept separate from config for security)

Both files have a `[default]` section plus optional `[profile <name>]` sections; profile values fall back to defaults. Profile selection order: constructor/`--profile` flag → `CAREDAILY_PROFILE` env var → `default`. A `.env` file is auto-loaded via python-dotenv.

`raise_errors` on `CareDaily(...)`:
- `True` (default, SDK use): fail fast on missing/invalid config
- `False` (CLI use): tolerate missing config so `caredaily configure` can run

### CLI

`src/caredaily/cli/app.py` defines the main Click group: it instantiates `CareDaily(profile, raise_errors=False)` and stores it in `ctx.obj["caredaily"]`; subcommands pull it from context and call factory methods. `configure.py` holds the `configure` subgroup (init, interactive profile setup). Commands catch `CareDailyException` and print user-friendly messages.

```bash
caredaily configure init
caredaily configure interactive --profile myprofile
caredaily ping
caredaily login --username user --password pass
caredaily cloud-connectivity --check-availability
```

### Testing pattern

Tests use `unittest` with a mocked adapter — no HTTP is exercised. The tests mirror the `src/` layout under `tests/caredaily/`:

```python
self.auth = Authentication()
self.auth.adapter = MagicMock()
self.auth.adapter.get.return_value = "login-result"
result = self.auth.login_by_username("user", password="pw")
args, kwargs = self.auth.adapter.get.call_args
self.assertEqual(args[0], "/cloud/json/login")
```

Assert the endpoint path, `ep_params`, and `ep_headers` passed to the adapter, and that the adapter's return value is passed through.

## Important Patterns

- **Parameter filtering**: strip `None` values before calling the adapter:
  `params = {k: v for k, v in params.items() if v is not None}`
- **Result wrapper**: every adapter call returns a `Result`; the adapter raises `CareDailyException` on non-SUCCESS codes, so callers usually don't need to check `result_code` themselves.

## Code Style

- Line length 88, double quotes, trailing commas in multi-line structures (ruff format, Black-compatible)
- Python 3.10+ required (3.14 supported); prefer PEP 585 type hints (`list[str]` over `List[str]`)
- Import sorting via ruff's isort rules (`extend-select = ["I"]`)

## Available Claude Agents

Specialized agents in `.claude/agents/`, invocable via the Task tool:

- **developer-agent**: feature implementation, code review, architecture design, debugging, refactoring, technical documentation
- **qa-specialist**: testing strategies, test case development, bug analysis, coverage assessment

## Knowledge base

This repo is documented in the OKF knowledge bundle at
<https://github.com/peoplepower/knowledge> (clone it locally if you
don't have a checkout). If your change alters behavior
documented there — device types, endpoints, webhooks, device
parameters, auth, architecture — update the matching concept(s):

1. Find them: `grep -rl 'python-core' <knowledge checkout> --include='*.md'`
2. Edit the concept, bump its `timestamp`, and adjust its `sources`
   frontmatter if code paths moved.
3. Add a dated entry to the bundle's `log.md`.
4. Run `python3 tools/okf.py index && python3 tools/okf.py validate`
   from the bundle root.

See `playbooks/keeping-knowledge-fresh.md` in the bundle for the full
freshness process.

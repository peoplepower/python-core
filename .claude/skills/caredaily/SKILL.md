---
name: caredaily
description: Use the caredaily Python SDK and CLI to call the CareDaily (People Power) API — authentication (username/passcode/RSA signature), profiles/config under ~/.caredaily/, the CareDaily factory pattern, and CLI commands. Use when asked to call CareDaily/People Power cloud APIs, log in, manage profiles, or script against devices/locations/users via this SDK.
---

# Using the caredaily SDK and CLI

This skill covers *using* the SDK/CLI to talk to the CareDaily cloud. For
developing the SDK itself (adding API classes, tests, style), see `CLAUDE.md`.

## Quick start (SDK)

```python
from caredaily import CareDaily
from caredaily.apis.app import Authentication, Locations

cd = CareDaily(profile="myprofile")   # profile optional; falls back to [default]
locs = cd.app_api(Locations)          # pass the CLASS, not an instance or string
result = locs.get_locations()         # returns Result; payload dict in result.data
```

- Factories: `cd.app_api(...)`, `cd.admin_api(...)`, `cd.bot_api(...)` — each is
  an if-chain over known classes in `src/caredaily/caredaily.py`. A class from
  the wrong subpackage returns `None` **silently**; a later `AttributeError:
  'NoneType' object has no attribute ...` means you used the wrong factory.
- Use `CareDaily(raise_errors=False)` when config may not exist yet (this is
  what the CLI does so `caredaily configure init` can run).
- Pass `None` for optional parameters to omit them — every API method filters
  `None` values before sending the request.

## Configuration and profiles

INI files under `~/.caredaily/` (base dir overridable via
`CAREDAILY_INTEGRATION_PATH`; profile selectable via constructor arg, `--profile`
flag, or `CAREDAILY_PROFILE` env var; a `.env` file is auto-loaded):

| File | Sections | Keys |
|------|----------|------|
| `config` | `[default]`, `[profile <name>]` | `hostname`, `ssl_verify`, `proxies` |
| `credentials` | `[default]`, `[<name>]` | `key`, `key_expire_ms`, `key_type` |
| `keys/` | — | RSA private keys from signature login (`<profile>_<app>_private_key.pem`) |

**Gotcha:** the section naming is asymmetric — `config` uses `[profile myname]`
but `credentials` uses plain `[myname]`. Easy to get wrong when editing by hand;
prefer `caredaily configure interactive --profile myname`.

`ssl_verify` must be the literal string `true` or `false` (it is parsed with
`eval(value.capitalize())`; anything else falls back to `True` with a warning).

## Authentication

All flows live in `Authentication` (`src/caredaily/apis/app/authentication.py`).

**Username/password:**

```python
auth = cd.app_api(Authentication)
result = auth.login_by_username("user@example.com", password="...")
api_key = result.data["key"]
```

**Passcode / TOTP:** if the account requires a second factor, the login raises
`CareDailyException` (import from `caredaily`) with
`context["resultCode"] == 17` (PASSCODE_REQUIRED). Obtain the code —
`auth.send_passcode(username, pref_delivery_type=None, brand=None, prefix=None,
app_hash=None)` triggers an SMS/email code, or use the user's TOTP app — then
retry `login_by_username(username, passcode=...)` with `passcode=` instead of
`password=`. The retry returns the same `Result` shape (key at
`result.data["key"]`).

**RSA signature login (2-step):** `caredaily configure signature --profile p
--app-name myapp` handles the whole recipe — login with `sign=True`, sign the
temporary key with SHA512withRSA (PKCS1v15), resend the signature as the
passcode. Requires the optional extra: `pip install caredaily[rsa]`. Keys are
stored under `~/.caredaily/keys/` (chmod 600). Details:
`okf/apis/authentication-and-signature-login.md`.

**Existing key:** `auth.login_by_key(key, key_type=...)`.

Key types are `APIKeyType` in `src/caredaily/models.py` and are **not
sequential**: `USER = 0`, `ADMIN = 11`, `ACCESS_TOKEN = 13`, `REFRESH_TOKEN =
14`, `SERVICE = 15`, `ANALYTIC = 16`.

## Results and errors

- Every call returns a `Result` (Pydantic model): `result.data` is the payload
  dict, plus `result_code` / `result_code_message`.
- Non-SUCCESS codes raise `CareDailyException` — `.message` (str) and
  `.context` (dict). Server errors carry `context["resultCode"]`; SDK config
  errors carry a negative `context["code"]`. You normally don't need to check
  `result_code` yourself.
- Common `ResultCode` values (`src/caredaily/models.py`): 0 SUCCESS,
  2 WRONG_API_KEY, 7 ACCESS_DENIED, 12 INVALID_CREDENTIALS,
  17 PASSCODE_REQUIRED, 24 STEP_REQUIRED.

## CLI

Global option `--profile <name>` on the root group.

```bash
caredaily configure init                      # first-time setup (refuses if config exists)
caredaily configure interactive --profile p   # create/edit a profile, optional sign-in
caredaily configure list [--profile p]        # show effective config (key obfuscated)
caredaily configure list-profiles             # sections in the credentials file
caredaily configure signature --profile p --app-name myapp   # RSA signature login
caredaily ping                                # connectivity check ("Pong")
caredaily login --username u --password pw    # username login, prints result
caredaily cloud-connectivity --check-availability   # or --version /
                                              # --connection-settings / --server-url
```

## API classes by factory

Import from `caredaily.apis` (or the subpackage):

- **`app_api`** (`caredaily.apis.app`): AI, AppFiles, Authentication,
  CloudConnectivity, CloudsIntegration, DeviceFiles, DeviceMeasurements,
  Devices, DeviceTypesAndParameters, EnergyManagement, Locations, PaidServices,
  ProfessionalMonitoring, RAG, Rules, SystemAndUserProperties, UserAccounts,
  UserCommunication, Weather, Websocket
- **`admin_api`** (`caredaily.apis.admin`): Billing, Challenges, AdminDevices,
  Firmware, Groups, AdminLocations, Narratives, Organizations, Reports, System,
  AdminTags, UserGroups, Users
- **`bot_api`** (`caredaily.apis.bot`): Analytic, BotDeveloper, BotStore,
  DeveloperTeams, Execution

## Deeper references (don't duplicate — read these)

- `okf/architecture/` — repo layout, request flow, factories, configuration
- `okf/apis/api-surface.md`, `okf/apis/authentication-and-signature-login.md`
- `okf/cli/caredaily-cli.md`
- `docs/api/{cloud,admin,bots}.yaml` — OpenAPI specs;
  `docs/acceptance/apis/*.md` — endpoint acceptance notes
- `tests/caredaily/apis/**` and `tests/integration/` — working usage examples
- Official docs: https://app.peoplepowerco.com/cloud/apidocs/cloud.html

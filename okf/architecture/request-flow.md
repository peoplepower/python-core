---
type: Architecture
title: Request Flow and RestAdapter
description: The single path every SDK call takes through the API base class and RestAdapter, auth headers by key type, Result parsing, and error handling.
resource: peoplepower/python-core:src/caredaily/http.py
tags: [python-core, architecture, http, auth]
status: draft
generated: { by: claude_code/claude-fable-5, at: 2026-09-11T00:00:00Z }
stale_after: 2027-09-11T00:00:00Z
sources:
  - id: http
    resource: peoplepower/python-core:src/caredaily/http.py
    title: RestAdapter implementation
    last_modified: 2026-01-18T10:27:48-08:00
  - id: api-base
    resource: peoplepower/python-core:src/caredaily/apis/api.py
    title: API base class
    last_modified: 2026-01-18T10:27:48-08:00
  - id: models
    resource: peoplepower/python-core:src/caredaily/models.py
    title: Result / ResultCode / APIKeyType models
    last_modified: 2026-07-06T21:27:48-07:00
---

Every API call follows one path[^http][^api-base]:

1. An API class method (e.g. `Authentication.login_by_username`) accepts typed
   parameters, strips `None` values
   (`params = {k: v for k, v in params.items() if v is not None}`), and builds
   the endpoint path.
2. It calls `self.adapter.get/post/put/delete(endpoint, ep_headers=, ep_params=, ep_json=, ep_data=)`.
3. `RestAdapter._do()` merges `ep_headers` over the base headers, sends via
   `requests.request`, and parses the response into a `Result`.
4. Non-SUCCESS result codes raise `CareDailyException` — callers normally never
   check `result_code` themselves.

All API classes inherit from `API` (`apis/api.py`), whose constructor builds the
adapter from a config dict (`hostname`, `api_key`, `key_type`, `ssl_verify`,
`proxies`, `logger`), dropping `None` values so `RestAdapter` defaults apply
(default hostname `app.peoplepowerco.com`)[^api-base].

# Auth headers by key type

`RestAdapter` picks the auth header from `APIKeyType` (coerced from int/str;
invalid values silently fall back to no auth header)[^http][^models]:

| APIKeyType | Enum value | Header sent |
| --- | --- | --- |
| `USER` | 0 | `API_KEY` |
| `ADMIN` | 11 | `ADMIN_KEY` |
| `ANALYTIC` | 16 | `ANALYTIC_API_KEY` |
| `ACCESS_TOKEN` / `REFRESH_TOKEN` / `SERVICE` | 13 / 14 / 15 | none (no adapter mapping) |

`Content-Type: application/json` is always set. Per-call `ep_headers` override
base headers; a header explicitly set to `None` makes `requests` drop it —
[Authentication uses this](/apis/authentication-and-signature-login.md) to remap
`ADMIN_KEY` → `API_KEY` on app endpoints.

# Response handling

For a 2xx `application/json` response, the body is validated into `Result`
(aliased Pydantic model: `result_code`, `result_code_message`, `key_expire`,
`collection_total_size`, ...) and the raw dict is stored on `result.data`[^http].

| Condition | Outcome |
| --- | --- |
| `result_code` present and ≠ `ResultCode.SUCCESS` (0) | `CareDailyException("[<code>] <message>", context=raw dict)` |
| JSON parse or model validation fails | `CareDailyException` (`Bad JSON response` / `Invalid JSON`) |
| 2xx `text/*` or `application/xml` | `Result(resultCode=0, data={"text": response.text})` |
| non-2xx JSON | bare `Exception(data_out["message"])` — NOT a `CareDailyException` |
| transport error (`requests.exceptions.RequestException`) | `CareDailyException("Request failed")` |
| unrecognized content type | `CareDailyException("Bad response")` |

`ResultCode` in `models.py` enumerates all API error codes (0–47); codes 15 and
36 were removed from the API spec in v61 but remain in the enum[^models].
`ssl_verify=False` also disables urllib3 warnings.

[^http]: RestAdapter implementation
[^api-base]: API base class
[^models]: Result / ResultCode / APIKeyType models

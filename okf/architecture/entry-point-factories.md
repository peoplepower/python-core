---
type: Architecture
title: CareDaily Entry Point and Factories
description: How the CareDaily class hands out configured API instances via explicit if-chain factories, and the checklist for adding a new API class.
resource: peoplepower/python-core:src/caredaily/caredaily.py
tags: [python-core, architecture, factory]
status: draft
generated: { by: claude_code/claude-fable-5, at: 2026-09-11T00:00:00Z }
stale_after: 2027-09-11T00:00:00Z
sources:
  - id: caredaily
    resource: peoplepower/python-core:src/caredaily/caredaily.py
    title: CareDaily entry point
    last_modified: 2026-07-10T23:03:51-07:00
---

`CareDaily` (`src/caredaily/caredaily.py`) loads
[profile configuration](/architecture/configuration.md) at construction and
hands out API instances. The factories take the API **class** and return a
configured instance built from the internal config dict[^caredaily]:

```python
from caredaily import CareDaily
from caredaily.apis.app import Authentication

cd = CareDaily(profile="myprofile")
auth = cd.app_api(Authentication)   # also: cd.admin_api(...), cd.bot_api(...)
```

Each factory (`app_api`, `admin_api`, `bot_api`) is an explicit if-chain over
known classes and returns `None` for unknown types — there is no registry or
reflection. A new API class that isn't added to its chain silently yields
`None` at the call site.

# Adding a new API class — checklist

1. Create the class under the right subpackage (`apis/app/`, `apis/admin/`,
   `apis/bot/`), inheriting from `API`.
2. Export it from `apis/__init__.py` (and re-export via the package root if it
   should be importable as `from caredaily import X`).
3. Add it to the matching factory if-chain in `caredaily.py`.
4. Add a mirrored test module under `tests/caredaily/apis/` using the
   [mocked-adapter pattern](/testing/mocked-adapter-pattern.md).

# Other entry-point behavior

* `raise_errors=True` (default, SDK use) fails fast on missing/invalid config;
  `raise_errors=False` (CLI use) tolerates it so `caredaily configure` can run.
* `update_config(key, value)` mutates only the allowed keys `hostname`,
  `api_key`, `key_type`, `ssl_verify`, `proxies`, `logger`; `value=None`
  deletes the key. New instances from the factories pick up the change;
  already-created API instances keep their old adapter.
* `get_config()` reports the *effective* adapter settings by instantiating a
  throwaway `CloudConnectivity` and reading its adapter's URL and headers.

[^caredaily]: CareDaily entry point

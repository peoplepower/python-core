---
type: Architecture
title: Configuration System
description: Profile-based INI files under ~/.caredaily/, the env vars that override them, and the config vs credentials section-naming asymmetry.
resource: peoplepower/python-core:src/caredaily/caredaily.py
tags: [python-core, configuration, profiles]
status: draft
generated: { by: claude_code/claude-fable-5, at: 2026-09-11T00:00:00Z }
stale_after: 2027-09-11T00:00:00Z
sources:
  - id: caredaily
    resource: peoplepower/python-core:src/caredaily/caredaily.py
    title: Config loading in CareDaily.__init__
    last_modified: 2026-07-10T23:03:51-07:00
  - id: configure-cli
    resource: peoplepower/python-core:src/caredaily/cli/configure.py
    title: configure CLI subgroup
    last_modified: 2026-07-07T13:13:04-07:00
---

Configuration lives in two INI files under `~/.caredaily/` (base directory
overridable via `CAREDAILY_INTEGRATION_PATH`; on Windows the default base is
`%UserProfile%`)[^caredaily]:

| File | Keys | Purpose |
| --- | --- | --- |
| `config` | `hostname`, `ssl_verify`, `proxies` | Connection settings |
| `credentials` | `key`, `key_type` | API keys — kept separate from config for security |

Profile values fall back to the `[default]` section per key. Profile selection
order: constructor / `--profile` flag → `CAREDAILY_PROFILE` env var → `default`.
A `.env` file is auto-loaded via python-dotenv at module import.

# Section-naming asymmetry (gotcha)

The two files name profile sections differently[^caredaily]:

* `config` uses `[profile <name>]` (e.g. `[profile sbox]`)
* `credentials` uses bare `[<name>]` (e.g. `[sbox]`)

Using the wrong form makes the profile invisible — with `raise_errors=True`
that raises `CareDailyException` (code -2, "missing 'profile <name>' /
'<name>' section"); with `raise_errors=False` it silently falls back to
defaults.

# Parsing quirks

* `ssl_verify` is parsed with `eval(value.capitalize())` — only `true`/`false`
  spellings work; anything else logs a warning and defaults to `True`.
* `key_type` is stored as a string and coerced to
  [`APIKeyType`](/architecture/request-flow.md) by the adapter; invalid values
  silently drop the auth header.
* Missing `[default]` sections raise (code -1) only when `raise_errors=True`.

# Managing profiles

`caredaily configure init` scaffolds the files;
`caredaily configure interactive --profile <name>` walks through profile
setup[^configure-cli]. See [caredaily CLI](/cli/caredaily-cli.md).

[^caredaily]: Config loading in CareDaily.__init__
[^configure-cli]: configure CLI subgroup

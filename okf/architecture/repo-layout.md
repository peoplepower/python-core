---
type: Architecture
title: Repo Layout
description: The three parts of the caredaily package (SDK, CLI, Pydantic models) and the map of the source tree.
resource: peoplepower/python-core:src/caredaily
tags: [python-core, architecture, layout]
status: draft
generated: { by: claude_code/claude-fable-5, at: 2026-09-11T00:00:00Z }
stale_after: 2027-09-11T00:00:00Z
sources:
  - id: src-tree
    resource: peoplepower/python-core:src/caredaily
    title: caredaily package source
    last_modified: 2026-07-10T23:03:51-07:00
  - id: pyproject
    resource: peoplepower/python-core:pyproject.toml
    title: Package metadata and extras
    last_modified: 2026-03-27T21:39:02-07:00
  - id: gitignore
    resource: peoplepower/python-core:.gitignore
    title: Ignore rules (.claude/* with !.claude/skills/ carve-out)
    last_modified: 2026-09-11T00:00:00Z
---

`python-core` ships one installable package, `caredaily`, with three parts[^src-tree]:

| Part | Location | Role |
| --- | --- | --- |
| SDK | `src/caredaily/caredaily.py` + `src/caredaily/apis/` | `CareDaily` entry point handing out per-domain API classes |
| CLI | `src/caredaily/cli/` | `caredaily` command built with Click |
| Models | `src/caredaily/models.py` | Pydantic models (`Result`, `Cloud`, `Server`, ...) and enums (`ResultCode`, `APIKeyType`, ...) |

# Source tree

| Path | Contents |
| --- | --- |
| `src/caredaily/caredaily.py` | [`CareDaily` entry point and factories](/architecture/entry-point-factories.md) |
| `src/caredaily/http.py` | `RestAdapter` — the only HTTP layer ([request flow](/architecture/request-flow.md)) |
| `src/caredaily/models.py` | `Result`, `ResultCode`, `APIKeyType`, `ServerType`, `SignatureAlgorithm`, ... |
| `src/caredaily/exceptions.py` | `CareDailyException` (message + optional context dict) |
| `src/caredaily/apis/api.py` | `API` base class — builds the adapter from a config dict |
| `src/caredaily/apis/app/` | User-facing APIs (`/cloud/json/...`) — see [API surface](/apis/api-surface.md) |
| `src/caredaily/apis/admin/` | Administrative APIs (`/admin/json/...`, some legacy `/espapi/admin/json/...`) |
| `src/caredaily/apis/bot/` | Bot developer APIs (`/botengine/json/...`) |
| `src/caredaily/cli/app.py` | Click group + `ping`, `login`, `cloud-connectivity` commands |
| `src/caredaily/cli/configure.py` | `configure` subgroup (init, interactive profile setup) |
| `tests/caredaily/` | Mirrors `src/` layout; [mocked-adapter pattern](/testing/mocked-adapter-pattern.md) |
| `.claude/skills/caredaily/SKILL.md` | Claude Code project skill teaching SDK/CLI *usage* (factories, auth flows, gotchas); the only tracked part of `.claude/` — `.gitignore` uses `.claude/*` + `!.claude/skills/` so local settings/agents/worktrees stay ignored[^gitignore] |

# Packaging

* Python 3.10+ required, 3.14 supported; PEP 585 hints preferred[^pyproject].
* Extras: `[dev]` (pytest, ruff, build), `[websockets]`, `[rsa]` (cryptography for RSA key auth)[^pyproject].
* Lint/format is ruff only (Black-compatible, line length 88, isort via `extend-select = ["I"]`).
* Source modules carry PEP 723 inline-script headers (`# /// script`) so they can also run standalone.

[^src-tree]: caredaily package source
[^pyproject]: Package metadata and extras
[^gitignore]: Ignore rules (.claude/* with !.claude/skills/ carve-out)

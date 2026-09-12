---
type: CLI
title: caredaily CLI
description: The Click command group, how it wires CareDaily into context, and the available commands.
resource: peoplepower/python-core:src/caredaily/cli/app.py
tags: [python-core, cli, click]
status: draft
generated: { by: claude_code/claude-fable-5, at: 2026-09-11T00:00:00Z }
stale_after: 2027-09-11T00:00:00Z
sources:
  - id: cli-app
    resource: peoplepower/python-core:src/caredaily/cli/app.py
    title: Main Click group and commands
    last_modified: 2026-01-18T10:27:48-08:00
  - id: configure-cli
    resource: peoplepower/python-core:src/caredaily/cli/configure.py
    title: configure subgroup
    last_modified: 2026-07-07T13:13:04-07:00
---

`src/caredaily/cli/app.py` defines the main Click group[^cli-app]. It
instantiates `CareDaily(profile, raise_errors=False)` (tolerating missing
config so `configure` can run) and stores it in `ctx.obj["caredaily"]`;
subcommands pull it from context and call the
[factory methods](/architecture/entry-point-factories.md). Commands catch
exceptions and print user-friendly messages rather than raising.

`--profile` defaults from the `CAREDAILY_PROFILE` env var; `-h/--help` both
work.

# Commands

| Command | Does |
| --- | --- |
| `caredaily configure init` | Scaffold `~/.caredaily/` config + credentials files[^configure-cli] |
| `caredaily configure interactive --profile <name>` | Interactive profile setup[^configure-cli] |
| `caredaily ping` | `CloudConnectivity.check_availability()` → "Pong" |
| `caredaily cloud-connectivity --check-availability/--version/--connection-settings/--server-url` | Cloud info queries (one flag required) |
| `caredaily login --username <u> --password <p>` | `Authentication.login_by_username` (prompts when flags omitted; password hidden) |

[^cli-app]: Main Click group and commands
[^configure-cli]: configure subgroup

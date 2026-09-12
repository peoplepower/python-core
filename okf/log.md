# Log

## 2026-09-11

* **Update**: Recorded the new Claude Code project skill `.claude/skills/caredaily/SKILL.md` (SDK/CLI usage guide: factories, auth flows including TOTP/RSA signature, gotchas) in the repo-layout concept, along with the `.gitignore` change (`.claude/*` + `!.claude/skills/`) that makes skills the only tracked part of `.claude/`. Merged to main in peoplepower/python-core (commit 558a508).
* **Creation**: Scaffolded the python-core bundle from the OKF v0.2 boilerplate. Authored initial concepts: repo layout, request flow / RestAdapter, CareDaily entry-point factories, configuration system, API surface, authentication and signature login, caredaily CLI, and the mocked-adapter test pattern. Registered the bundle as `python-core` in the machine registry.
* **Finding**: The `APIKeyType` enum values in `src/caredaily/models.py` (USER=0, ADMIN=11, ACCESS_TOKEN=13, REFRESH_TOKEN=14, SERVICE=15, ANALYTIC=16) do not match the USER=1/ADMIN=2/ANALYTIC=3 summary in CLAUDE.md; concepts here record the code's actual values.

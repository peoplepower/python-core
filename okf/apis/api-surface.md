---
type: Reference
title: API Surface
description: Every API class by subpackage (app / admin / bot), the factory that serves it, and its endpoint prefix.
resource: peoplepower/python-core:src/caredaily/apis
tags: [python-core, apis, reference]
status: draft
generated: { by: claude_code/claude-fable-5, at: 2026-09-11T00:00:00Z }
stale_after: 2027-03-11T00:00:00Z
sources:
  - id: apis-init
    resource: peoplepower/python-core:src/caredaily/apis/__init__.py
    title: apis package exports
    last_modified: 2026-07-10T23:03:51-07:00
  - id: caredaily
    resource: peoplepower/python-core:src/caredaily/caredaily.py
    title: Factory if-chains
    last_modified: 2026-07-10T23:03:51-07:00
---

All classes inherit from `API` and are served by the matching
[factory](/architecture/entry-point-factories.md) on `CareDaily`. Official
endpoint docs: <https://app.peoplepowerco.com/cloud/apidocs/cloud.html>.

# App APIs — `cd.app_api(...)`, `/cloud/json/...`

`apis/app/`[^apis-init][^caredaily]: `Authentication`, `UserAccounts`,
`Locations`, `Devices`, `DeviceMeasurements`, `DeviceTypesAndParameters`,
`DeviceFiles`, `AppFiles`, `UserCommunication`, `SystemAndUserProperties`,
`Rules`, `PaidServices`, `ProfessionalMonitoring`, `EnergyManagement`,
`Weather`, `CloudConnectivity`, `CloudsIntegration`, `RAG`, `AI`, `Websocket`.

App APIs migrated from legacy `/espapi/cloud/json/` to `/cloud/json/` on
2026-07-07 — the espapi route cannot validate EdDSA JWT API keys
("[2] JWK not found"). See
[authentication](/apis/authentication-and-signature-login.md).

`Websocket` (extra: `[websockets]`) is the one class that goes beyond the
adapter: it fetches the websocket URL via REST, then provides an async client
(`connect`, `authenticate`, async context manager).

# Admin APIs — `cd.admin_api(...)`, `/admin/json/...`

`apis/admin/`: `System`, `Organizations`, `Groups`, `Users`, `UserGroups`,
`AdminDevices`, `AdminLocations`, `AdminTags`, `Challenges`, `Narratives`,
`Billing`, `Firmware`, `Reports`.

A few admin APIs (narratives, tags, groups) still use legacy
`/espapi/admin/json/...` paths — the same JWK failure class may surface there
with JWT keys.

# Bot APIs — `cd.bot_api(...)`, `/botengine/json/...`

`apis/bot/`: `Analytic`, `BotDeveloper`, `BotStore`, `DeveloperTeams`,
`Execution`.

[^apis-init]: apis package exports
[^caredaily]: Factory if-chains

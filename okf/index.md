---
okf_version: "0.2"
type: Bundle Index
title: python-core Knowledge Bundle
description: Repo-local knowledge for the caredaily Python SDK and CLI — the CareDaily entry point, RestAdapter request flow, profile configuration, API surface, authentication flows, and the mocked-adapter testing pattern.
tags: [okf, python-core, caredaily, sdk, api]
generated: { by: claude_code/claude-fable-5, at: 2026-09-11T00:00:00Z }
status: draft
---

# Start here

* [README](/README.md) - How this bundle is organized and how to use the tooling.
* [Repo layout](/architecture/repo-layout.md) - The three parts of the package (SDK, CLI, models) and the source tree map.
* [Request flow and RestAdapter](/architecture/request-flow.md) - The single path every API call takes, auth headers by key type, and error handling.
* [CareDaily entry point and factories](/architecture/entry-point-factories.md) - The factory if-chains and the checklist for adding a new API class.
* [Configuration system](/architecture/configuration.md) - Profile INI files under ~/.caredaily/, env vars, and the config/credentials section-naming asymmetry.

# APIs

* [API surface](/apis/api-surface.md) - Every API class by subpackage (app / admin / bot) and its endpoint prefix.
* [Authentication and signature login](/apis/authentication-and-signature-login.md) - Login endpoints, TOTP, and the two-step RSA signature login recipe with its gotchas.

# CLI

* [caredaily CLI](/cli/caredaily-cli.md) - The Click command group, context wiring, and available commands.

# Testing

* [Mocked-adapter test pattern](/testing/mocked-adapter-pattern.md) - The unittest + MagicMock convention every SDK test follows.

# Related bundles

* [developer-knowledge](bundle://developer-knowledge/index.md) - Platform-wide Care Daily API knowledge; this bundle covers only the Python SDK internals.

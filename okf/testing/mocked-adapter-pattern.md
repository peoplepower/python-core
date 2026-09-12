---
type: Testing Pattern
title: Mocked-Adapter Test Pattern
description: The unittest + MagicMock convention every SDK test follows — no HTTP, assert the endpoint, params, and headers passed to the adapter.
resource: peoplepower/python-core:tests/caredaily
tags: [python-core, testing, unittest]
status: draft
generated: { by: claude_code/claude-fable-5, at: 2026-09-11T00:00:00Z }
stale_after: 2027-09-11T00:00:00Z
sources:
  - id: tests
    resource: peoplepower/python-core:tests/caredaily
    title: SDK test suite
    last_modified: 2026-07-10T23:03:51-07:00
---

Tests use `unittest` with the adapter replaced by a `MagicMock` — no HTTP is
ever exercised. The tests mirror the `src/` layout under `tests/caredaily/`
(one test module per API module)[^tests].

```python
self.auth = Authentication()
self.auth.adapter = MagicMock()
self.auth.adapter.get.return_value = "login-result"

result = self.auth.login_by_username("user", password="pw")

args, kwargs = self.auth.adapter.get.call_args
self.assertEqual(args[0], "/cloud/json/login")
```

Assert three things per method:

1. the endpoint path (first positional arg to the adapter),
2. the `ep_params` / `ep_headers` / `ep_json` kwargs — including that `None`
   parameters were stripped (see [request flow](/architecture/request-flow.md)),
3. that the adapter's return value is passed through unchanged.

Run with `pytest` from the repo root; single tests via
`pytest tests/caredaily/apis/app/test_authentication.py::TestAuthentication::test_login_by_username`.
Coverage: `pytest --cov=caredaily --cov-report=html`.

When [adding a new API class](/architecture/entry-point-factories.md), add the
mirrored test module in the same change.

[^tests]: SDK test suite

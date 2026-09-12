# python-core knowledge bundle

An [OKF v0.2](/SPEC.md) bundle documenting the internals of `python-core` —
the `caredaily` Python SDK and CLI for the CareDaily API (People Power
Company). It lives inside the repo it documents, so bundle-relative source
references point at the checkout one directory up.

Platform-wide API knowledge (endpoints, device types, webhooks) belongs in
the `developer-knowledge` bundle; this bundle covers only how *this SDK*
is built: the entry point, adapter, configuration, CLI, and test patterns.

## Layout

| Directory | Contents |
| --- | --- |
| `architecture/` | Repo layout, request flow, entry-point factories, configuration |
| `apis/` | API surface map and authentication flows |
| `cli/` | The `caredaily` Click CLI |
| `testing/` | The mocked-adapter unittest pattern |
| `playbooks/` | How to add knowledge and keep it fresh |
| `tools/` | `okf.py` (index / validate / freshness / viz) |

## Working on the bundle

From this directory:

```sh
python3 tools/okf.py index      # regenerate subdirectory index.md files
python3 tools/okf.py validate   # must exit 0 before committing
python3 tools/okf.py freshness  # list concepts due for review
```

Every change: update the concept, bump `generated.at`, append a dated entry
to [log.md](/log.md), then run `index` and `validate`.

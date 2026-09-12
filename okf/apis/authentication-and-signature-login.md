---
type: API Recipe
title: Authentication and Signature Login
description: The Authentication API's endpoints, TOTP factors, and the working two-step RSA signature login flow with its header gotchas.
resource: peoplepower/python-core:src/caredaily/apis/app/authentication.py
tags: [python-core, auth, rsa, login]
status: draft
generated: { by: claude_code/claude-fable-5, at: 2026-09-11T00:00:00Z }
stale_after: 2027-03-11T00:00:00Z
sources:
  - id: auth
    resource: peoplepower/python-core:src/caredaily/apis/app/authentication.py
    title: Authentication API class
    last_modified: 2026-07-07T13:13:04-07:00
  - id: webcore
    resource: peoplepower/webcore:src/data/services/authService.ts
    title: webcore reference implementation (loginBySignature, sign)
    last_modified: 2026-07-07T00:00:00Z
---

# Endpoints

All on `/cloud/json/` (GET unless noted)[^auth]:

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `login_by_username` | `/login` | Username/password (or signature) login |
| `send_passcode` | `/passcode` | Send an SMS/email passcode |
| `login_by_key` | `/loginByKey` | Exchange an existing key for a new one |
| `logout` | `/logout` | Invalidate the current key |
| `create/confirm/get/delete_totp_factor` | `/totp` (POST/PUT/GET/DELETE) | TOTP second factor management |
| `get_private_key` / `put_public_key` | `/signatureKey` (GET/PUT) | RSA key material for signature login |
| `get_operation_token` | `/token` | Operation tokens |
| `get_auth_token` | `/authToken` | Auth tokens |

Requires the `[rsa]` extra (cryptography) for signature flows.

# RSA signature login (two-step)

Working recipe as of 2026-07-07, both user and admin flows[^auth][^webcore]:

1. `GET /cloud/json/signatureKey` returns a base64 DER (PKCS#8) private key;
   the server keeps the public half. Pass `endUser=true` for the regular-user
   flow (enables passwordless step 1); omit it for admin.
2. First `/login` call with `sign=true` (+password for admin, no password for
   the endUser flow) returns a temporary key.
3. Sign the temp key's UTF-8 bytes with PKCS#1 v1.5 + SHA-512
   (`SignatureAlgorithm.SHA512withRSA`).
4. Second `/login` call sends the base64 signature as the **`passcode`
   header** (never as password), with `sign=true&signAlgorithm=SHA512withRSA`.

Reference implementations when this SDK disagrees with the server: webcore's
`authService.ts` (`loginBySignature`, `sign`)[^webcore]; iOS uses
`SecKeyCreateSignature` with `RSASignatureMessagePKCS1v15SHA512` and must
unwrap PKCS#8 → PKCS#1 (Security.framework quirk; Python `cryptography` loads
PKCS#8 directly).

# Gotchas

* App endpoints need the `API_KEY` header even when holding an admin key —
  `Authentication._user_key_headers()` remaps `ADMIN_KEY` → `API_KEY` and sets
  the base `ADMIN_KEY` header to `None` so `requests` drops it (see
  [request flow](/architecture/request-flow.md)).
* "[2] JWK not found" can also mean a profile hostname/key mismatch: a
  `"iss":"PPCProd"` JWT sent to `sbox.peoplepowerco.com` fails because sbox
  lacks prod's JWK.
* Legacy `/espapi/cloud/json/` cannot validate EdDSA JWT keys at all — app
  APIs migrated to `/cloud/json/` on 2026-07-07 (see
  [API surface](/apis/api-surface.md)).

[^auth]: Authentication API class
[^webcore]: webcore reference implementation (loginBySignature, sign)

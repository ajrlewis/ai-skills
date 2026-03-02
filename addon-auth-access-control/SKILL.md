---
name: addon-auth-access-control
description: Use when a project needs authentication, authorization, and session or token policy across web and API surfaces; pair with architect-stack-selector and addon-human-pr-review-gate.
---

# Add-on: Auth Access Control

Use this skill when a project needs a reusable identity boundary, route protection, and explicit access policy instead of ad hoc auth checks.

## Compatibility

- Works with `architect-python-uv-fastapi-sqlalchemy`, `architect-nextjs-bun-app`, and `architect-next-prisma-bun-vector`.
- Can be combined with `architect-nostr-intent-router` when Nostr identity or signer-based access is part of the product.
- Usually not needed for offline-only `architect-python-uv-batch` jobs unless they expose operator APIs.

## Inputs

Collect:
- `AUTH_MODE`: `session-cookie` | `jwt-bearer` | `api-key` | `mixed`.
- `IDENTITY_SOURCE`: `first-party` | `oauth` | `nostr-signer`.
- `ACCESS_MODEL`: `rbac` | `roles+scopes`.
- `REQUIRE_MFA_FOR_ADMIN`: `yes` | `no` (default `yes`).
- `SESSION_TTL_MINUTES`: default `60`.

## Integration Workflow

1. Add auth policy artifacts:
```text
docs/AUTH_MODEL.md
src/{{MODULE_NAME}}/auth/config.*
src/{{MODULE_NAME}}/auth/guards.*
src/{{MODULE_NAME}}/auth/session_store.*
src/{{MODULE_NAME}}/api/routes/auth.*
tests/auth/
```

2. Define identity and trust boundaries:
- document who issues identities
- define token/session format and expiry
- separate authentication from authorization
- default protected routes to deny unless explicitly allowed

3. Enforce access policy:
- add route-level guards for protected endpoints and pages
- centralize role and scope checks
- return stable unauthorized and forbidden responses

4. Add operational safety:
- rotation and revocation path for sessions or API keys
- explicit admin-path hardening
- audit notes for privileged actions

## Required Template

### `docs/AUTH_MODEL.md`
```markdown
# Auth Model

## Identity Source
- first-party

## Auth Mode
- session-cookie

## Access Rules
| Surface | Auth Required | Role/Scope |
|---|---|---|
| /api/auth/me | yes | authenticated |
| /api/admin/* | yes | admin |

## Session Rules
- TTL: 60 minutes
- Admin routes require MFA: yes
```

## Guardrails

- Documentation contract for generated code:
  - Python: write module docstrings and docstrings for public classes, methods, and functions.
  - Next.js/TypeScript: write JSDoc for exported components, hooks, utilities, and route handlers.
  - Add concise rationale comments only for non-obvious logic, invariants, or safety constraints.
  - Apply this contract even when using template snippets below; expand templates as needed.


- Default deny for protected surfaces.
- Keep secrets, signing keys, and refresh tokens server-only.
- Verify role and scope claims on the server; never trust client-mutated claims.
- Hash stored API keys and session secrets where persistence is required.
- Treat missing access rules as a blocker, not a warning.

## Validation Checklist

- Confirm generated code includes required docstrings/JSDoc and rationale comments for non-obvious logic.


```bash
test -f docs/AUTH_MODEL.md
rg -n "auth|guard|session|forbidden|unauthorized" src || true
test -d tests/auth || true
```

Manual checks:
- Anonymous access to protected routes fails with controlled `401` or `403`.
- Privileged routes enforce role or scope checks consistently.

## Decision Justification Rule

- Every non-trivial decision must include a concrete justification.
- Capture the alternatives considered and why they were rejected.
- State tradeoffs and residual risks for the chosen option.
- If justification is missing, treat the task as incomplete and surface it as a blocker.

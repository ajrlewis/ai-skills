---
name: addon-observability-nextjs-pino
description: Use when a Next.js or TypeScript server runtime needs production-grade structured logging via pino with redaction, correlation IDs, and telemetry-friendly output.
---

# Add-on: Next.js Observability with pino

Use this skill when a Next.js or TypeScript server runtime needs package-backed structured logging.
This is the default implementation add-on for Next.js when `addon-observability-telemetry` is in scope.

## Compatibility

- Best fit for `architect-nextjs-bun-app`.
- Also valid for server-side TypeScript apps and API route handlers.
- Pairs cleanly with `addon-observability-telemetry`, which defines the higher-level telemetry contract.

## Inputs

Collect:
- `TELEMETRY_MODE`: `logs-only` | `logs+metrics` | `logs+metrics+traces`.
- `LOG_FORMAT`: default `json`; use `logfmt` only when the user explicitly requests it.
- `PII_REDACTION`: `strict` | `standard`.
- `LOG_BACKEND`: default `pino`; only use an explicit equivalent when the user requests it and the tradeoff is documented.

## Integration Workflow

1. Add package-backed logging dependencies:
```bash
bun add pino
```
- If the user explicitly wants a framework helper, add the narrowest compatible package instead of building custom request log plumbing.
- If `TELEMETRY_MODE` includes metrics or traces, add the relevant OpenTelemetry packages instead of inventing custom instrumentation helpers.

2. Add Next.js observability artifacts:
```text
src/lib/observability/logging.ts
src/lib/observability/context.ts
```
- `logging.ts` should configure `pino`, serializers, redaction, and child logger helpers.
- `context.ts` should handle correlation ID creation or propagation; do not create a custom logger implementation.

3. Bind runtime context:
- In route handlers and server actions, create or propagate a correlation ID before emitting logs.
- Use child loggers to attach route, request, or job metadata instead of interpolating free-form strings.

4. Standardize event shape:
- emit stable event names
- include `correlation_id`
- classify levels consistently
- keep errors structured and redacted

## Guardrails

- Prefer `pino` as the default production logger for Next.js and server-side TypeScript.
- Do not use raw `console.log` in production request paths except in tests or local-only scripts.
- Do not build a custom `logger.ts` that wraps `console.log` and calls that observability.
- Keep the local module limited to `pino` configuration, redaction, serializers, and child logger helpers.
- Do not leak secrets, auth headers, cookies, or full request bodies.

## Validation Checklist

```bash
rg -n "from \"pino\"|from 'pino'|require\\(\"pino\"\\)" src
rg -n "correlation_id" src
rg -n "console\\.log" src || true
```

Manual checks:
- server logs include a correlation identifier
- log output is structured and machine-parseable
- the code configures `pino` instead of implementing logging from scratch

## Decision Justification Rule

- Every non-trivial decision must include a concrete justification.
- Capture the alternatives considered and why they were rejected.
- State tradeoffs and residual risks for the chosen option.
- If justification is missing, treat the task as incomplete and surface it as a blocker.

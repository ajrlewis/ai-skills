---
name: addon-observability-python-structlog
description: Use when a Python API or worker needs production-grade structured logging via structlog with correlation IDs, redaction, and telemetry-friendly output.
---

# Add-on: Python Observability with structlog

Use this skill when a Python runtime needs package-backed structured logging.
This is the default implementation add-on for Python when `addon-observability-telemetry` is in scope.

## Compatibility

- Best fit for `architect-python-uv-fastapi-sqlalchemy`.
- Also valid for `architect-python-uv-batch` and Python worker-style projects.
- Pairs cleanly with `addon-observability-telemetry`, which defines the higher-level telemetry contract.

## Inputs

Collect:
- `TELEMETRY_MODE`: `logs-only` | `logs+metrics` | `logs+metrics+traces`.
- `LOG_FORMAT`: `json` | `logfmt`.
- `PII_REDACTION`: `strict` | `standard`.
- `PYTHON_OBSERVABILITY_PROFILE`: `api` | `worker`.
- `LOG_BACKEND`: default `structlog`; only use `loguru` when the user explicitly requests it and the tradeoff is documented.

## Integration Workflow

1. Add package-backed logging dependencies:
```bash
uv add structlog
```
- If `TELEMETRY_MODE` includes metrics or traces, add the relevant OpenTelemetry packages instead of inventing custom counters or span helpers.

2. Add Python observability artifacts:
```text
src/{{MODULE_NAME}}/observability/logging.py
src/{{MODULE_NAME}}/observability/context.py
```
- `logging.py` should configure `structlog` processors, output rendering, and redaction hooks.
- `context.py` should bind correlation IDs or run IDs using context-local state; do not create a custom logger implementation.

3. Bind runtime context:
- For FastAPI, add request middleware that creates or propagates a correlation ID and binds it before request handling.
- For workers, bind a run ID or job ID at the command entrypoint before pipeline execution starts.

4. Standardize event shape:
- emit stable event names
- include `correlation_id`
- include explicit error codes for expected failures
- keep exception details structured and redacted

## Guardrails

- Prefer `structlog` as the default production path for Python services.
- Do not build a custom logger around `print()` or bare stdlib logging as the primary implementation.
- Do not emit raw secrets, auth headers, or full unredacted payloads.
- Keep the local module limited to `structlog` configuration, processors, and context binding.
- If the user explicitly chooses `loguru`, document why it was chosen over `structlog` and keep the same redaction and correlation requirements.

## Validation Checklist

```bash
rg -n "import structlog|from structlog" src
rg -n "correlation_id|run_id" src
rg -n "print\\(" src || true
```

Manual checks:
- request or run logs include a correlation identifier
- log output is structured and machine-parseable
- the code configures `structlog` instead of implementing logging from scratch

## Decision Justification Rule

- Every non-trivial decision must include a concrete justification.
- Capture the alternatives considered and why they were rejected.
- State tradeoffs and residual risks for the chosen option.
- If justification is missing, treat the task as incomplete and surface it as a blocker.

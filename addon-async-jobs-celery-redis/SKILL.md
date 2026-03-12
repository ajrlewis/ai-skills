---
name: addon-async-jobs-celery-redis
description: Use when adding durable background jobs for CPU/IO-heavy document processing using Celery + Redis (or RQ if explicitly requested), with job state transitions stored in Postgres.
---

# Add-on: Async Jobs (Celery + Redis)

Use this skill when the API must enqueue long-running document tasks and return immediately (202 + job_id).

FastAPI request handlers must only:
- accept uploads
- create DB rows
- enqueue the worker task
- return status identifiers

## Inputs

Collect:
- `REDIS_URL`: default `redis://redis:6379/0` (compose internal).
- `JOB_TIMEOUT_SECONDS`: default `900`.
- `JOB_MAX_RETRIES`: default `3`.

## Celery Integration Workflow (Preferred)

1. Add dependencies:
```bash
uv add celery redis
```

2. Add modules:
```text
src/{{PY_MODULE}}/jobs/
  celery_app.py
  tasks.py
  service.py
```

3. Worker task requirements:
- task accepts stable identifiers (`document_id`, `job_id`) rather than raw bytes
- task is idempotent (safe to retry)
- task updates job status in Postgres:
  - `queued` -> `running` -> `succeeded` | `failed`
  - persist `started_at`, `finished_at`, and error details

4. Task routing:
- `preprocess_document(job_id, document_id)`
- later stages can be separate tasks or a single orchestrated task, but keep stage boundaries explicit in DB for auditability.

5. Configure Celery defaults:
- `task_acks_late=True` (so crashes requeue)
- per-task `autoretry_for` with bounded backoff
- explicit soft+hard time limits if supported

## Redis Service (Local Dev)

Add a `redis` service in compose and wire:
- API env: `REDIS_URL`
- worker env: `REDIS_URL`

## RQ Alternative

Out of scope for this add-on. If the user explicitly requests RQ, create a separate `addon-async-jobs-rq-redis` skill rather than mixing implementations.

## Guardrails

- Never run preprocessing synchronously in `POST /documents/upload`.
- Always store job state in Postgres; do not treat Redis as the source of truth.
- Ensure worker uses the same codebase/image as API but with a separate command.
- If you add a task stage, add a corresponding deterministic eval fixture for it (`addon-deterministic-eval-suite`).

## Decision Justification Rule

- Every non-trivial decision must include a concrete justification.
- Capture the alternatives considered and why they were rejected.
- State tradeoffs and residual risks for the chosen option.
- If justification is missing, treat the task as incomplete and surface it as a blocker.

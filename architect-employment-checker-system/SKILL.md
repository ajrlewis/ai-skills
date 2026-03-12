---
name: architect-employment-checker-system
description: Use when scaffolding an employment-document checker (Next.js + FastAPI) with Redis queue workers, Postgres system-of-record, MinIO/S3 artifact storage, and auditable page/span citations (non-RAG by default).
---

# Architect: Employment Checker System (Structured Document Analysis)

Use this skill to scaffold the full multi-service system described in the Employment Checker System Summary:
- deterministic, page-aware PDF preprocessing
- structured clause extraction + Range/rule validation
- auditable outputs with exact page/chunk/span citations
- Postgres as system-of-record; object storage for artifacts
- background workers for all heavy document processing

This is **not** a semantic-search-first RAG architecture. Vector search is optional and should be excluded unless explicitly requested.

## Compatibility

- Pair with `architect-python-uv-fastapi-sqlalchemy` for the Python API base.
- Pair with `architect-nextjs-bun-app` or `architect-nextjs-vercel-app` for the Next.js UI base.
- Strongly recommended add-ons:
  - `addon-decision-justification-ledger`
  - `addon-deterministic-eval-suite`
  - `addon-human-pr-review-gate`
  - `addon-observability-python-structlog`
  - `addon-observability-nextjs-pino`

## Inputs

Collect:
- `PROJECT_NAME`: repo/folder name (kebab-case).
- `PY_MODULE`: Python import module for the API (snake_case).
- `WEB_APP`: Next.js app folder name (default `web`).
- `API_SERVICE`: API folder name (default `api`).
- `PYTHON_VERSION`: default `3.12`.
- `QUEUE_IMPL`: `celery` (required for this architecture).
- `S3_BUCKET`: default `documents`.

Default local dev secrets (override if user provides):
- `MINIO_ROOT_USER=minio`
- `MINIO_ROOT_PASSWORD=minio123`

## Target Repo Layout (Monorepo)

Prefer a monorepo to keep compose wiring, API contracts, and review UI aligned:
```text
apps/{{WEB_APP}}/             # Next.js
services/{{API_SERVICE}}/     # FastAPI + shared worker code
docker-compose.yml
```

If the user explicitly wants separate repos, keep the same service boundaries and contracts.

## Service Contract (Non-Negotiables)

- `POST /documents/upload`:
  - accepts a PDF upload
  - stores the original PDF in S3/MinIO
  - creates `documents` and `jobs` rows
  - enqueues preprocess/extract/validate via the queue
  - returns `202 Accepted` with `job_id` (+ `document_id` if available)
- No heavy PDF work inside request handlers.
- Every derived artifact must be traceable back to the original PDF via:
  - `document_id`
  - `page_number`
  - `chunk_id` and `chunk_index`
  - span markers (`char_start`/`char_end`) or equivalent

## Compose Baseline (Local Dev)

Include these services:
- `postgres`
- `redis`
- `minio`
- `api` (FastAPI)
- `worker` (Celery/RQ)
- `frontend` (Next.js)

Also include a **bucket init** step (one-shot container or API startup hook) to ensure `S3_BUCKET` exists.

## Orchestration Workflow (High Level)

1. Scaffold base API (`architect-python-uv-fastapi-sqlalchemy`).
2. Add object storage integration (`addon-object-storage-minio-s3`).
3. Add async jobs + worker (`addon-async-jobs-celery-redis`).
4. Add Postgres schema for the pipeline (`addon-postgres-document-pipeline-schema`).
5. Add preprocessing + page artifacts (`addon-pdf-preprocess-page-artifacts`).
6. Add header/footer cleanup (`addon-header-footer-cleanup`).
7. Add JSONL chunk artifacts (`addon-jsonl-chunking-citations`).
8. Add clause extraction (`addon-clause-extraction-citations`).
9. Add Range/rule validation (`addon-range-rules-validation`).
10. Add report synthesis (`addon-report-synthesis-audit`).
11. Scaffold UI surfaces (`ui-employment-checker-console`).

## Guardrails

- Store both `raw` and `clean` page content. Never destructively overwrite the raw artifact.
- Store canonical artifacts (PDF, markdown, JSONL, reports) in S3/MinIO; store queryable rows in Postgres.
- Make all worker stages idempotent by `document_id` + `stage` (safe re-runs).
- Persist job state transitions and error payloads for auditability.
- Prefer deterministic parsing and explicit page boundaries; avoid regex-only page splitting when possible.

## Decision Justification Rule

- Every non-trivial decision must include a concrete justification.
- Capture the alternatives considered and why they were rejected.
- State tradeoffs and residual risks for the chosen option.
- If justification is missing, treat the task as incomplete and surface it as a blocker.

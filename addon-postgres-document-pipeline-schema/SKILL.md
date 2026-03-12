---
name: addon-postgres-document-pipeline-schema
description: Use when adding the Postgres schema for structured employment-document analysis (documents/pages/chunks/clauses/validations/jobs/reports) with JSONB metadata and audit-friendly indices.
---

# Add-on: Postgres Schema (Document Pipeline)

Use this skill to add relational tables that make the pipeline queryable, auditable, and reprocessable.

## Inputs

Collect:
- `USE_ALEMBIC`: `yes` (default when paired with `architect-python-uv-fastapi-sqlalchemy`).
- `DOC_ID_KIND`: `uuid` (default) or `ulid` (only if user requests).

## Required Tables (Core)

Create tables aligned with the system summary:
- `documents`
- `jobs`
- `document_pages`
- `document_chunks`
- `extracted_clauses`
- `validations`
- `reports`

Optional but recommended:
- `range_rules` (versioned rule/policy set; “Range”)
- `agent_runs` (record extraction/validation model version + prompts)
- `review_items` / `review_decisions` (human review workflow)

## Column Conventions

Prefer:
- stable ids (`uuid` recommended)
- `created_at`, `updated_at` timestamps
- `status` enums or constrained strings
- `metadata_jsonb` for parser/cleanup provenance

### `documents` (minimum)
- `id`
- `filename`
- `mime_type`
- `checksum`
- `storage_key` (raw PDF key)
- `status`
- `page_count`
- `created_at`

### `document_pages` (minimum)
- `id`
- `document_id`
- `page_number` (1-based)
- `raw_markdown`
- `clean_markdown`
- `metadata_jsonb` (e.g., header/footer removal decisions)

### `document_chunks` (minimum)
- `id`
- `document_id`
- `page_number`
- `chunk_index` (0-based within page)
- `heading` (nullable)
- `text`
- `char_start`, `char_end` (spans within the chosen page artifact)
- `metadata_jsonb` (parser, cleaned flag, section path)

### `jobs` (minimum)
- `id`
- `document_id`
- `job_type` (e.g., `preprocess`)
- `status` (`queued|running|succeeded|failed`)
- `error` (nullable)
- `started_at`, `finished_at`

## Indices / Constraints (Audit-Friendly)

- Unique: `(document_id, page_number)` on `document_pages`
- Index: `(document_id, page_number, chunk_index)` on `document_chunks`
- Index: `(document_id, status)` on `jobs`
- Foreign keys everywhere; decide cascade behavior explicitly and justify it

## Migration Workflow (Alembic)

When paired with `architect-python-uv-fastapi-sqlalchemy`:
- add SQLAlchemy models
- generate an Alembic migration
- ensure local compose startup can run migrations automatically (or via a documented command)

## Guardrails

- Never store only a single giant JSON blob; store artifacts in S3/MinIO and ingest rows for querying.
- Preserve raw vs clean text for each page.
- Schema must support reprocessing and deterministic reproducibility (store parser versions + cleanup params in JSONB).

## Decision Justification Rule

- Every non-trivial decision must include a concrete justification.
- Capture the alternatives considered and why they were rejected.
- State tradeoffs and residual risks for the chosen option.
- If justification is missing, treat the task as incomplete and surface it as a blocker.


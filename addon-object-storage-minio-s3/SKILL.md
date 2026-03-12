---
name: addon-object-storage-minio-s3
description: Use when adding S3-compatible object storage for raw PDFs and derived artifacts (MinIO locally; S3 in prod), including bucket init, key conventions, and upload/download helpers.
---

# Add-on: Object Storage (MinIO/S3)

Use this skill when the project needs durable storage for:
- original uploaded PDFs
- derived markdown/page artifacts
- JSONL artifacts
- report exports

Local dev uses MinIO; production can switch to AWS S3 (or any S3-compatible store) without changing calling code.

## Inputs

Collect:
- `S3_BUCKET`: default `documents`.
- `S3_REGION`: default `us-east-1` (ignored by MinIO but kept for portability).
- `S3_ENDPOINT_URL`: for MinIO, typically `http://minio:9000` inside compose.

## Key Layout (Deterministic)

Use stable keys:
- `documents/raw/{document_id}.pdf`
- `documents/markdown/{document_id}.md`
- `documents/pages/{document_id}/page-{page_number}.md`
- `documents/jsonl/{document_id}.jsonl`
- `documents/reports/{document_id}.json`
- `documents/reports/{document_id}.md` (optional)

## Integration Workflow (Python)

1. Add dependencies:
```bash
uv add boto3
```

2. Add a small storage module:
```text
src/{{PY_MODULE}}/storage/
  s3.py
```

`s3.py` should expose:
- `put_object_bytes(bucket, key, data, content_type) -> None`
- `get_object_bytes(bucket, key) -> bytes`
- `presign_get_url(bucket, key, expires_seconds) -> str` (optional)
- `ensure_bucket(bucket) -> None` (used by bootstrap/init)

3. Configure via env vars (API + worker share this):
- `S3_ENDPOINT_URL` (set for MinIO)
- `S3_BUCKET`
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION` (optional)

## docker-compose MinIO (Local Dev)

Add a `minio` service with:
- ports `9000` (S3 API) and `9001` (console)
- root creds from env
- a persistent volume

Add a one-shot bucket init step (preferred):
- container runs MinIO client (`mc`) to create `S3_BUCKET` if missing
- treat this as idempotent

## Guardrails

- Never store PDFs or artifacts solely on local disk in prod paths; always go through object storage abstraction.
- Always persist the `storage_key`/object key in Postgres rows so any artifact is reproducible.
- Use content-type metadata consistently (`application/pdf`, `text/markdown`, `application/json`).
- Avoid embedding secrets in code or docker-compose; use env vars.

## Decision Justification Rule

- Every non-trivial decision must include a concrete justification.
- Capture the alternatives considered and why they were rejected.
- State tradeoffs and residual risks for the chosen option.
- If justification is missing, treat the task as incomplete and surface it as a blocker.


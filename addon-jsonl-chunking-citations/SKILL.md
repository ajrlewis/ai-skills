---
name: addon-jsonl-chunking-citations
description: Use when generating structured JSONL chunks with page-aware citation metadata, storing the JSONL as an artifact, and ingesting records into Postgres rows for querying.
---

# Add-on: JSONL Chunking + Citation Metadata

Use this skill to create the canonical intermediate representation:
- JSONL records (archival artifact in object storage)
- `document_chunks` rows (queryable in Postgres)

This is the foundation for extraction, validation, and audit-ready citations.

## Inputs

Collect:
- `CHUNK_TARGET_CHARS`: default `1200`.
- `CHUNK_MIN_CHARS`: default `400`.
- `CHUNK_OVERLAP_CHARS`: default `120` (only if using sliding windows).
- `CHUNK_STRATEGY`: `paragraph` (default) or `window`.

## JSONL Record Shape (Required)

Each JSONL line must include:
- `document_id`
- `page` (1-based)
- `chunk_id` (stable within document; e.g., `p{page}_c{chunk_index}`)
- `chunk_index` (0-based within page)
- `text`
- `char_start`, `char_end` (span markers relative to the chosen page artifact)
- `heading` (nullable)
- `metadata` (parser name/version, cleaned flag, strategy params)

## Generation Workflow

1. Input: `document_pages.clean_markdown` (preferred) or `raw_markdown` (only if cleanup not run yet).
2. Chunk per page:
   - `paragraph` strategy: split on blank lines; merge/split to hit `CHUNK_TARGET_CHARS`
   - `window` strategy: sliding window over the page string
3. For each chunk, compute deterministic span markers:
   - `char_start`/`char_end` in the page string used for chunking
4. Emit JSONL line and insert/update a `document_chunks` row.
5. Store the JSONL file in object storage at `documents/jsonl/{document_id}.jsonl`.

## Guardrails

- Use **cleaned** text for chunking whenever available; keep provenance in `metadata.cleaned=true`.
- Ensure chunk ids are stable across reruns given the same page text + parameters.
- Do not store only the JSONL blob in Postgres; ingest rows for query use.

## Decision Justification Rule

- Every non-trivial decision must include a concrete justification.
- Capture the alternatives considered and why they were rejected.
- State tradeoffs and residual risks for the chosen option.
- If justification is missing, treat the task as incomplete and surface it as a blocker.


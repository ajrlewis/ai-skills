---
name: addon-pdf-preprocess-page-artifacts
description: Use when adding deterministic PDF preprocessing that produces page-level artifacts with explicit page boundaries and provenance metadata (raw + cleaned stored separately).
---

# Add-on: PDF Preprocessing (Page Artifacts)

Use this skill to implement the preprocessing stage that turns an uploaded PDF into:
- page-level text/markdown artifacts (raw)
- page-level cleaned artifacts (after header/footer cleanup; separate stage)
- stable provenance metadata for audit + reprocessing

## Inputs

Collect:
- `PDF_PARSER`: `docling` (if available) or `pypdf`/`pdfplumber` fallback.
- `PAGE_MARKER_STYLE`: `structured-pages` (preferred) or `markdown-markers`.

## Output Contracts

For each page (1-based), persist:
- `raw_page_markdown` (or raw extracted text)
- `metadata_jsonb` including parser name/version and extraction params

Also persist canonical whole-document artifacts to object storage:
- raw PDF (already stored on upload)
- optional markdown export (include page markers if used)

## Implementation Notes

### Preferred: Structured Pages

If the parser yields pages directly:
- iterate page objects
- insert one `document_pages` row per page
- avoid regex page splitting

### Fallback: Markdown Markers

If the parser only yields markdown:
- emit deterministic markers:
  - `<!-- PAGE:1 -->`
  - `<!-- PAGE:2 -->`
- split on markers; never infer pages by heuristics alone

## Worker Responsibilities

The preprocess worker should:
1. Download raw PDF from object storage
2. Extract per-page raw content deterministically
3. Insert/update `document_pages.raw_markdown`
4. Update `documents.page_count` and `documents.status`
5. Enqueue the next stage (cleanup / chunking / extraction) or mark stage completion

## Guardrails

- Do not run cleanup in the raw extraction step; raw must remain raw.
- Ensure preprocessing is idempotent (safe retries) for the same `document_id`.
- Store extraction parameters and parser version so results are reproducible.

## Decision Justification Rule

- Every non-trivial decision must include a concrete justification.
- Capture the alternatives considered and why they were rejected.
- State tradeoffs and residual risks for the chosen option.
- If justification is missing, treat the task as incomplete and surface it as a blocker.


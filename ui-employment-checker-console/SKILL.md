---
name: ui-employment-checker-console
description: Use when adding a Next.js UI for PDF upload, job status polling, page/clauses/validations browsing, and human review of low-confidence extractions/validations.
---

# UI: Employment Checker Console (Next.js)

Use this skill to add the UI surfaces needed for the system:
- upload PDFs
- show processing progress
- browse extracted pages/chunks
- review extracted clauses + validations
- resolve review-needed items (human-in-the-loop)

## Inputs

Collect:
- `API_BASE_URL`: local default `http://localhost:8000`.
- `POLL_INTERVAL_MS`: default `1500` while running; back off when complete.

## Required Screens

Implement minimal screens/routes:
- Upload:
  - file picker/dropzone
  - submit -> show `job_id` + `document_id`
- Job status:
  - poll `GET /jobs/{job_id}`
  - show stage/progress + errors
- Document overview:
  - `GET /documents/{document_id}`
  - links to pages/clauses/results
- Pages viewer:
  - list pages, show `raw` vs `clean` toggle
- Clauses + validations:
  - table with clause type, confidence, review-needed, linked citations
- Results/report:
  - render `GET /documents/{document_id}/results`
  - download report artifact (presigned URL or API proxy)
- Review queue (optional but recommended):
  - show items where `review_needed=true`
  - capture human decision and persist via API

## UX Guardrails

- Display citations prominently (page + snippet + link to page view).
- Treat jobs as asynchronous; never block UI waiting for upload processing.
- On failures, show error payload and a “reprocess” action if supported.

## Decision Justification Rule

- Every non-trivial decision must include a concrete justification.
- Capture the alternatives considered and why they were rejected.
- State tradeoffs and residual risks for the chosen option.
- If justification is missing, treat the task as incomplete and surface it as a blocker.


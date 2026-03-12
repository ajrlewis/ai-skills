---
name: addon-report-synthesis-audit
description: Use when aggregating extraction + validation outputs into an audit-ready report artifact (JSON/Markdown) stored in S3/MinIO and summarized in Postgres for UI consumption.
---

# Add-on: Report Synthesis (Audit-Ready)

Use this skill to implement the postprocess stage that produces:
- a UI-ready summary object
- exportable report artifacts (JSON, optional Markdown/PDF later)
- stable linkage to citations for every finding

## Inputs

Collect:
- `REPORT_FORMATS`: default `json,markdown`.
- `SORT_ORDER`: default `severity desc, confidence asc`.

## Output Contracts

1. Postgres:
- `reports.summary_jsonb` contains a compact summary for UI:
  - top findings by severity
  - counts by result/severity
  - review-needed items
  - report generation provenance

2. Object storage:
- `documents/reports/{document_id}.json`
- optionally `documents/reports/{document_id}.md`

## Synthesis Workflow

1. Load:
   - `documents`
   - `extracted_clauses`
   - `validations`
2. Group findings by:
   - severity
   - clause type
   - rule
3. For each finding, include:
   - result, severity, confidence
   - explanation
   - citation block: page/chunk/span + short source quote
4. Persist report artifact(s) and a `reports` row.

## Guardrails

- Never output a finding without a source anchor (page/chunk/span + quote).
- Keep report generation deterministic given the same inputs (stable sorting + stable IDs).
- If a finding is `review_needed`, highlight it prominently in the report summary.

## Decision Justification Rule

- Every non-trivial decision must include a concrete justification.
- Capture the alternatives considered and why they were rejected.
- State tradeoffs and residual risks for the chosen option.
- If justification is missing, treat the task as incomplete and surface it as a blocker.


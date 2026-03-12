---
name: addon-header-footer-cleanup
description: Use when removing noisy repeated headers/footers from page artifacts while preserving raw text and recording cleanup decisions for auditability.
---

# Add-on: Header/Footer Cleanup (Repeated Lines)

Use this skill to implement the cleanup stage that removes repeated header/footer noise from LLM-facing text while preserving raw page content for traceability.

## Inputs

Collect:
- `REPEAT_THRESHOLD_RATIO`: default `0.6` (line must appear on >= 60% of pages to be a removal candidate).
- `TOP_BAND_LINES`: default `3` (lines considered “header band”).
- `BOTTOM_BAND_LINES`: default `3` (lines considered “footer band”).
- `MIN_LINE_LEN`: default `6` (ignore tiny lines for repetition counting).

## Algorithm (Deterministic)

1. For each page, split into lines.
2. Normalize each line for comparison:
   - NFKC normalize
   - lowercase
   - collapse whitespace
   - strip common page-number patterns (`page 3 of 12`, `3/12`, etc.) for comparison only
3. Count how often each normalized line appears across pages.
4. Mark a line as a removal candidate if:
   - it appears on >= `REPEAT_THRESHOLD_RATIO` of pages, and
   - it appears mostly within the top/bottom bands
5. Remove candidates from the cleaned page text.
6. Persist:
   - `document_pages.clean_markdown`
   - `document_pages.metadata_jsonb.cleanup` with:
     - removed normalized lines
     - per-page removals (original text)
     - thresholds used

## Storage Contract

Never overwrite `raw_markdown`. Always store:
- `raw_markdown`
- `clean_markdown`

## Guardrails

- Avoid deleting content that looks like a section heading or clause text; if uncertain, keep it.
- Record exactly what was removed and why in metadata for auditing.
- Keep cleanup deterministic given the same inputs and parameters.

## Decision Justification Rule

- Every non-trivial decision must include a concrete justification.
- Capture the alternatives considered and why they were rejected.
- State tradeoffs and residual risks for the chosen option.
- If justification is missing, treat the task as incomplete and surface it as a blocker.


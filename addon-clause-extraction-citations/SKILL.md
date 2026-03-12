---
name: addon-clause-extraction-citations
description: Use when extracting employment-related clauses from cleaned chunks into structured records with exact page/chunk/span citations, confidence, and a review-needed signal (LLM-assisted but audit-first).
---

# Add-on: Clause Extraction (Citations + Confidence)

Use this skill after chunking to extract structured clause records suitable for validation.

The extraction stage operates on **cleaned** chunks, but must remain auditable back to the original document via page/chunk/span citations.

## Compatibility

- Works best when paired with `addon-direct-llm-sdk` (preferred) or `addon-langchain-llm`.
- Requires `addon-jsonl-chunking-citations` (or an equivalent chunk table with spans).

## Inputs

Collect:
- `CLAUSE_TYPES`: default set:
  - `compensation`, `bonus`, `commission`, `benefits`, `termination`, `notice`, `severance`,
    `non_compete`, `non_solicit`, `confidentiality`, `ip_assignment`, `governing_law`,
    `dispute_resolution`, `work_location`, `remote_work`, `hours`, `pto`
- `CONFIDENCE_REVIEW_THRESHOLD`: default `0.7`.
- `LLM_MODEL`: user-provided; otherwise choose a stable, cost-appropriate model and justify.

## Output Contract (`extracted_clauses`)

Each extracted clause must include:
- `document_id`
- `chunk_id` (FK to `document_chunks`)
- `clause_type`
- `normalized_text` (agent-produced normalization)
- `source_quote` (verbatim quote from the chunk whenever possible)
- `citation_jsonb`:
  - `page_number`
  - `chunk_id`
  - `char_start`, `char_end`
  - optional `raw_storage_key` for PDF
- `confidence` (0..1)
- `review_needed` boolean (set when confidence < threshold or ambiguities detected)
- `agent_run_id` / provenance fields (model, prompt version)

## Extraction Workflow

1. Iterate `document_chunks` for a document in deterministic order (page asc, chunk_index asc).
2. For each chunk:
   - run clause extraction (LLM-assisted allowed)
   - enforce a strict JSON schema output (reject + retry or mark review-needed if schema fails)
3. Deduplicate clauses:
   - exact same `source_quote` + `clause_type` within a document should not create duplicates
4. Store results in `extracted_clauses` with citations pointing to chunk spans.

## Guardrails

- Never “invent” clauses: every clause must be anchored to a `source_quote` from a specific chunk.
- If the agent cannot quote the source confidently, mark as `review_needed` rather than guessing.
- Persist prompts/model versions for auditability.

## Decision Justification Rule

- Every non-trivial decision must include a concrete justification.
- Capture the alternatives considered and why they were rejected.
- State tradeoffs and residual risks for the chosen option.
- If justification is missing, treat the task as incomplete and surface it as a blocker.


---
name: addon-range-rules-validation
description: Use when validating extracted clauses against a known rule/policy set (“Range”) to produce compliant/non-compliant/uncertain results with severity, confidence, and auditable citations (no retrieval-first RAG).
---

# Add-on: Range Rules Validation (Policy Engine)

Use this skill to implement the validation stage:
- consumes `extracted_clauses`
- compares against known rules/policies (“Range”)
- emits structured validation results with explanations, severity, confidence, and review flags

This stage should not depend on top-k retrieval over the document as the main method.

## Inputs

Collect:
- `RANGE_RULE_SOURCE`: `db` (recommended) or `repo-file` (YAML/JSON checked into repo).
- `VALIDATION_RESULT_SET`: `compliant|non_compliant|uncertain`.
- `SEVERITY_LEVELS`: default `info|low|medium|high|critical`.
- `UNCERTAINTY_REVIEW_THRESHOLD`: default `0.6`.

## Data Contracts

### Rules

Model rules as versioned objects with:
- `rule_id` (stable)
- `name`
- `description`
- `applies_to_clause_types`
- `logic` (deterministic checks) and/or `guidance` (LLM-assisted rubric)
- `version`, `effective_at`

### Validations (`validations` table)

Each validation record must include:
- `clause_id`
- `rule_id` / `rule_name`
- `result` (from `VALIDATION_RESULT_SET`)
- `explanation` (human-readable)
- `severity`
- `confidence` (0..1)
- `review_needed` (true when uncertain or confidence low)
- citations: reuse clause citation linkage; do not lose source anchoring

## Validation Workflow

1. Load active ruleset (latest version or effective-at timestamp).
2. For each `extracted_clause`:
   - select applicable rules by `clause_type`
   - evaluate deterministically when possible
   - if LLM-assisted evaluation is used, enforce strict schema output and store model+prompt provenance
3. Persist one validation row per (clause, rule) evaluation.
4. Mark `review_needed` when:
   - result is `uncertain`, or
   - confidence < threshold, or
   - clause is missing a required field for the rule

## Guardrails

- Do not fetch extra context via semantic retrieval unless explicitly requested; validate on clause + rule.
- If a rule cannot be applied due to missing evidence, output `uncertain` and set `review_needed=true`.
- Store rule versions used in every validation for reproducibility.

## Decision Justification Rule

- Every non-trivial decision must include a concrete justification.
- Capture the alternatives considered and why they were rejected.
- State tradeoffs and residual risks for the chosen option.
- If justification is missing, treat the task as incomplete and surface it as a blocker.


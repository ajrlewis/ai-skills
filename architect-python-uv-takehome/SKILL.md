---
name: architect-python-uv-takehome
description: Use when scaffolding a lightweight Python uv take-home, prototype, or interview assignment where speed and clarity matter more than production defaults, especially for fixed-layout deliverables such as document extraction pipelines, validation agents, and golden-file comparisons.
---

# Architect: Python + uv Take-Home

Use this skill for short, time-boxed Python projects such as take-home assignments, experiments, and proof-of-concepts.
This skill is intentionally lighter than the production architect skills:
- no Docker unless the user explicitly asks for it
- no CI scaffolding unless the user explicitly asks for it
- no review gate, observability, or deployment requirements by default
- prefer direct CLI workflows and simple local validation

Use this when the prompt already defines the expected output shape, for example a `solution/` directory with specific subfolders and artifacts.

This skill is optimized for reviewer speed:
- make the project easy to run in one pass
- keep dependencies low and familiar
- show correctness with deterministic checks
- use LLMs only where they add clear value

This skill is scaffolding, not the core solution.
Use it to reduce setup time and standardize the workflow, but keep the assignment-specific reasoning, parsing rules, and validation logic clearly visible in the project itself.

## Inputs

Collect these values:
- `PROJECT_ROOT`: default `solution`
- `PROJECT_NAME`: human-readable project name
- `MODULE_NAME`: snake_case Python package name
- `CLI_NAME`: command name for `uv run ...`
- `PYTHON_VERSION`: default `3.12`
- `USE_LLM`: `yes` or `no`
- `LLM_STYLE`: `direct-sdk` | `langchain` (default `direct-sdk`)
- `HAS_FIXED_OUTPUT_SHAPE`: `yes` or `no`
- `OUTPUT_ARTIFACTS`: required files the prompt expects

## Selection Rules

- If the user needs a quick CLI or offline data-processing submission, use this skill instead of `architect-python-uv-batch`.
- If the prompt defines a specific deliverable layout, preserve that layout exactly.
- If the task is evaluation-heavy, keep checks local and deterministic before adding any LLM-based review.
- If the assignment includes both "generate output" and "explain differences," split those into deterministic generation plus a separate reporting layer.
- If the user needs a web API, database, Docker-first runtime, or CI pipeline, use a heavier architect skill instead.

## Scaffold Workflow

1. Create a lightweight Python project with `uv`.
2. Match the prompt's required directory layout exactly.
3. Add only the dependencies needed to complete the assignment.
4. Build direct CLI entrypoints for the required tasks.
5. Produce output artifacts in the expected paths.
6. Add a minimal smoke test and deterministic validation path.
7. Make the happy path runnable in two commands or fewer.
8. Keep the generated scaffolding subordinate to the assignment-specific logic.

## Default Project Shape

When the prompt specifies a `solution/` directory, use:

```text
solution/
  README.md
  pyproject.toml
  requirements.txt
  src/
    {{MODULE_NAME}}/
      extractor/
      agent/
      models/
      utils/
      cli.py
  tests/
  output/
```

If the prompt explicitly requires a different structure such as `solution/src/extractor`, follow the prompt instead of this default package layout.

For assignment prompts with fixed paths, a direct layout is also valid:

```text
solution/
  README.md
  pyproject.toml
  requirements.txt
  src/
    extractor/
    agent/
    common/
    cli.py
  tests/
  output/
```

## Dependency Defaults

Start with the smallest useful set:

```bash
uv init
uv add pydantic orjson jsonschema typer rich
uv add -d pytest
```

Add only as needed:
- markdown parsing: `markdown-it-py`
- tabular parsing: `pandas`
- LLM direct SDK: provider package such as `openai`
- diff/report helpers: stdlib first, add packages only if they remove meaningful complexity

If the prompt explicitly asks for `requirements.txt` or the reviewer is likely to expect it, export one after dependency setup:

```bash
uv export --format requirements-txt -o requirements.txt
```

## CLI Pattern

Prefer a small CLI with explicit commands:

```text
extract
validate
run-all
```

Expected behavior:
- `extract`: read source inputs and write normalized output JSON
- `validate`: compare extracted output to schema and any provided reference files
- `run-all`: run extraction, then validation, then write final artifacts

Prefer exposing these through a script entrypoint so the reviewer can run:

```bash
uv run {{CLI_NAME}} run-all
```

## Best-Fit Assignment Profile

This skill is a strong fit when the assignment looks like:
- parse a messy input document into a normalized JSON schema
- compare the generated JSON to a provided reference file
- produce a human-readable validation report
- optionally use an LLM to explain discrepancies, confidence, or edge cases

For these tasks, the strongest default architecture is:
- deterministic extractor first
- deterministic schema and reference comparison second
- optional LLM narrative layer last

Do not start with a fully agentic design when a simple pipeline is clearer and easier to verify.

## Positioning Rule

When using this skill in a real submission:
- treat the skill as a setup accelerator, not the main artifact
- keep the submitted repository focused on the assignment, not on the skill system
- make sure the core extraction and validation logic is plainly readable without any knowledge of the skill

The reviewer should conclude:
- the skill saved setup time
- the implementation decisions are still yours
- the correctness claims come from deterministic checks, not from trust in scaffolding

The reviewer should not conclude:
- the solution is mostly generated boilerplate
- the workflow is more interesting than the result
- the candidate is hiding weak reasoning behind tool usage

## Extraction Pattern

For document extraction tasks:
- identify the 2-6 sections that actually contain authoritative data
- parse those sections first instead of reading the entire corpus linearly
- normalize values into a stable schema
- record uncertainty when text is ambiguous or spread across multiple sections
- prefer deterministic parsing of known headings, tables, and labels before calling an LLM
- if an LLM is needed, send only the narrowest relevant excerpt rather than the whole document

For legal or contract-like markdown:
- prefer heading and article boundaries
- preserve source citations when practical (`section`, `heading`, `line snippet`)
- treat summary schedules and tables as corroborating evidence, not always the sole source of truth
- when multiple sections repeat the same term, prefer the most authoritative contractual definition and note conflicts explicitly

## Extraction + Validation Layout

For fixed-layout assignments that ask for an extractor and a validator, prefer:

```text
solution/
  src/
    extractor/
      load_inputs.py
      parse_document.py
      normalize_terms.py
      write_output.py
    agent/
      compare_terms.py
      score_confidence.py
      write_report.py
    common/
      schema_tools.py
      types.py
    cli.py
  output/
    extracted_terms.json
    validation_report.md
```

This keeps the responsibilities obvious to a reviewer:
- `extractor/` generates normalized data
- `agent/` evaluates and explains
- `common/` holds shared schema and utility code

Keep the extractor and validator code concrete and assignment-specific.
Do not bury domain parsing behind generic framework layers if that makes the logic harder to inspect.

## Validation Pattern

Start with deterministic checks:

1. Validate output JSON against the provided schema.
2. Compare extracted output to the provided reference output.
3. Produce a field-by-field discrepancy summary.
4. Fail only on real structural or content mismatches, not formatting differences.
5. Separate objective mismatches from subjective interpretation notes.

If an LLM is used, keep it advisory:
- use it to explain discrepancies
- use it to draft a narrative validation report
- do not let it replace the deterministic diff
- do not let it silently "fix" extracted values without showing the original mismatch

For reviewer-facing scoring, prefer:
- exact pass/fail for schema compliance
- explicit discrepancy counts for content mismatches
- optional confidence scores per field with brief reasoning

## Minimal Eval Guidance

Prefer simple, assignment-aligned evals over production gating.

Required checks:
- schema compliance
- golden-file comparison against provided expected output
- required artifact existence
- at least one end-to-end smoke test

For extraction tasks, the most useful deterministic eval is a semantic diff:
- compare keys recursively
- report missing fields, unexpected fields, and changed values
- treat ordering as insignificant unless the schema makes order meaningful
- normalize trivial formatting differences before diffing (whitespace, case where appropriate, numeric string formatting)
- use `scripts/semantic_diff.py expected.json actual.json` for a fast machine-readable baseline diff

For fixed test input plus fixed expected output, the default grading path should be:
1. Run the extractor on the provided input.
2. Validate the resulting JSON against the schema.
3. Compare it to the provided expected JSON.
4. Emit a concise diff summary and an expanded markdown report.

This is usually enough to demonstrate real correctness in a take-home without adding heavy eval infrastructure.

If the prompt includes a provided reference output, that reference comparison should be the centerpiece of the validation story.
Do not substitute a vague "AI evaluation" for an explicit diff against the expected output.

## README Contract

Keep setup instructions short and local-first:
- install dependencies
- run the extractor
- run the validator
- run the all-in-one command
- explain where outputs are written
- document any environment variables for LLM usage
- include one copy-paste command block a reviewer can run without reading the code first

Do not add deployment, infrastructure, or CI instructions unless the user asked for them.

## Walkthrough Guidance

If you explain your process in a walkthrough, demo, or follow-up interview, frame the skill usage like this:

1. Use `npx skills add ...` to install a lightweight scaffold so setup and project shape are handled quickly.
2. Adapt the scaffold to the assignment's required directory layout and deliverables.
3. Implement the assignment-specific extraction logic directly in the repo.
4. Run deterministic validation against the provided schema and expected output.
5. Use any LLM-powered reporting only as a final explanatory layer.

In walkthroughs, emphasize:
- why the chosen structure fits the prompt
- what parts are deterministic
- what parts required interpretation
- how you verified correctness

In walkthroughs, do not emphasize:
- the skill mechanism itself as the clever part
- generic scaffolding over domain-specific logic
- "agent" behavior that is not backed by clear validation

## Guardrails

- Match the prompt's required output paths exactly.
- Prefer readable code over abstractions that save little time.
- Keep modules small and easy to review during a time-boxed assessment.
- Use deterministic logic for core correctness checks.
- Surface ambiguous extraction decisions explicitly instead of hiding them.
- Keep LLM calls optional and bounded behind a small interface.
- Optimize for "easy to grade" over "architecturally impressive."
- Prefer transparent diffs and traceable reasoning over clever but opaque agent loops.
- Avoid making the final repository feel like a generic generated starter.
- Keep the submission credible even if the reviewer ignores the skill entirely.

## Validation Checklist

Run the smallest useful verification set:

```bash
uv run pytest -q
uv run {{CLI_NAME}} extract
uv run {{CLI_NAME}} validate
uv run {{CLI_NAME}} run-all
```

Manual checks:
- expected output files exist
- extracted JSON validates against the target schema
- discrepancy report is readable and references concrete differences
- the README's quickstart works exactly as written

## Decision Justification Rule

- Every non-trivial decision must include a concrete justification.
- Capture the alternatives considered and why they were rejected.
- State tradeoffs and residual risks for the chosen option.
- If justification is missing, treat the task as incomplete and surface it as a blocker.

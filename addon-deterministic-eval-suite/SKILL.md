---
name: addon-deterministic-eval-suite
description: Use when you need hard pass fail eval gates for generated projects and skills; pair with addon-decision-justification-ledger and addon-human-pr-review-gate.
---

# Add-on: Deterministic Eval Suite

Use this skill when a project needs reproducible, merge-blocking evaluation checks.

## Compatibility

- Works with all `architect-*` scaffolds.
- Recommended default for `production-default` mode.

## Inputs

Collect:
- `EVAL_SCOPE`: `skill-only` | `project-only` | `both` (default `both`).
- `BLOCK_ON_FAIL`: `yes` | `no` (default `yes`).
- `RUN_DOCKER_CHECKS`: `yes` | `no` (default `yes` for production-default).

## Integration Workflow

1. Add deterministic eval artifacts:
```text
evals/deterministic/manifest.yaml
evals/deterministic/run.sh
evals/deterministic/checks/
.github/workflows/evals-deterministic.yml
```

2. Baseline checks (always include):
- file/contract existence checks
- lint/type/test/build command checks
- docker artifact checks (`Dockerfile`, `docker-compose.yml`, image build)
- decision trace checks (`docs/DECISION_LOG.md`, `REVIEW_BUNDLE/DECISION_TRACE.md`)
- non-zero exit on failure
- for skills repositories: frontmatter naming check (`scripts/validation/check_skill_frontmatter.sh`)
- for skills repositories: decision-policy check (`scripts/validation/check_skill_decision_policy.sh`)

3. Skill-specific checks:
- one check file per selected skill
- examples:
- `check_nostr_profile.sh`
- `check_rag_ingest_query.sh`
- `check_review_bundle.sh`
- `check_decision_trace.sh`

4. Output summary:
- write deterministic run summary to `REVIEW_BUNDLE/TEST_EVIDENCE.md`.

## Required Template

### `evals/deterministic/manifest.yaml`
```yaml
version: 1
checks:
  - id: contracts
    command: "bash evals/deterministic/checks/check_contracts.sh"
  - id: tests
    command: "bash evals/deterministic/checks/check_tests.sh"
  - id: build
    command: "bash evals/deterministic/checks/check_build.sh"
  - id: decision_trace
    command: "bash evals/deterministic/checks/check_decision_trace.sh"
```

## Guardrails

- Deterministic evals are source-of-truth merge gates.
- Avoid network-dependent assertions unless explicitly required.
- Keep commands idempotent and non-destructive.
- Fail closed: missing required checks must fail the run.
- Treat missing decision rationale artifacts as deterministic failure.

## Validation Checklist

```bash
test -f evals/deterministic/manifest.yaml
test -f evals/deterministic/run.sh
test -f .github/workflows/evals-deterministic.yml
bash evals/deterministic/run.sh
```

## Decision Justification Rule

- Every non-trivial decision must include a concrete justification.
- Capture the alternatives considered and why they were rejected.
- State tradeoffs and residual risks for the chosen option.
- If justification is missing, treat the task as incomplete and surface it as a blocker.

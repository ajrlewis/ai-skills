---
name: addon-llm-judge-evals
description: Use when you want rubric based LLM quality scoring on generated outputs; pair with addon-deterministic-eval-suite.
---

# Add-on: LLM Judge Evals

Use this skill when you need qualitative evaluation (clarity, domain fit, UX coherence, docs quality) in addition to deterministic checks.

## Compatibility

- Works with all stacks.
- Best paired with `addon-deterministic-eval-suite`.

## Inputs

Collect:
- `JUDGE_MODEL`: model id to run scoring.
- `JUDGE_RUBRIC_MODE`: `product` | `security` | `developer-experience` | `custom`.
- `PASS_THRESHOLD`: default `0.75`.
- `BLOCK_ON_JUDGE_FAIL`: `yes` | `no` (default `no`).

## Integration Workflow

1. Add judge artifacts:
```text
evals/judge/rubric.md
evals/judge/cases/
scripts/evals/run_llm_judge.py
.github/workflows/evals-judge.yml
REVIEW_BUNDLE/JUDGE_REPORT.md
```

2. Define rubric:
- scoring categories and weights
- failure reasons template
- required evidence links (files/lines/commands)

3. Execute judge run:
- evaluate generated files against rubric per scenario
- store structured JSON + markdown summary

4. Merge policy:
- default advisory (`BLOCK_ON_JUDGE_FAIL=no`)
- blocking only when explicitly configured

## Required Template

### `evals/judge/rubric.md`
```markdown
# Judge Rubric

- Technical coherence (0-1)
- Requirement coverage (0-1)
- Domain language alignment (0-1)
- UX quality and states (0-1)
- Documentation clarity (0-1)

Pass threshold: 0.75
```

## Guardrails

- Never replace deterministic gates with judge scores.
- Keep prompts/rubrics versioned in repo for auditability.
- Record model/version and timestamp for each run.
- Surface uncertainty as explicit notes, not silent pass.

## Validation Checklist

```bash
test -f evals/judge/rubric.md
test -f scripts/evals/run_llm_judge.py
test -f .github/workflows/evals-judge.yml
test -f REVIEW_BUNDLE/JUDGE_REPORT.md || true
```

## Decision Justification Rule

- Every non-trivial decision must include a concrete justification.
- Capture the alternatives considered and why they were rejected.
- State tradeoffs and residual risks for the chosen option.
- If justification is missing, treat the task as incomplete and surface it as a blocker.

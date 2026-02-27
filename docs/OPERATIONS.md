# Operations

## Operating Modes

Default mode is `production-default`:
- Base architect skills must emit Docker artifacts (`Dockerfile`, `.dockerignore`, `docker-compose.yml` where relevant).
- CI must include image build checks.
- Validation must include containerized checks.
- Non-trivial decisions must be recorded with explicit rationale.

Alternative modes:
- `local-no-docker`: only when user explicitly requests `NO_DOCKER=yes`.
- `offline-smoke`: constrained environment fallback; still create required files and record limitations in `TEST_NOTES.md`.

## Standard Workflow

1. Use `architect-stack-selector` first.
2. Apply exactly one base architect skill.
3. Apply needed add-ons and UI skills.
4. Apply `addon-human-pr-review-gate` for production-default (unless explicitly opted out).
5. Apply `addon-decision-justification-ledger` for production-default (required, no opt-out).
6. Apply `addon-domain-semantic-adaptation` for production-default (unless explicitly opted out).
7. Apply `addon-deterministic-eval-suite` for production-default (unless explicitly opted out).
8. Run validation checklists from all selected skills.
9. If constrained, document what could not be fully verified.

Prompt template:

```text
Use architect-stack-selector.
Goal: <describe app>.
Constraints: <runtime, db, deployment, timeline>.
Domain language: <preferred terms, forbidden terms, tone>.
Mode: production-default (or NO_DOCKER=yes only if explicitly requested).
Decision visibility: required (no non-trivial decision without rationale).
Pick the minimal skill set, scaffold now, and run validations.
```

## Agent Usage

Codex / Claude Code:
- Open target repo.
- Paste router prompt.
- Then run base + add-on/UI prompt.

Cursor / Windsurf:
- Open target repo.
- Use the same prompts in chat.
- Ensure file edit permissions are enabled.

## Testing Playbook

### 1) Python Batch + RAG

Path:
- `test-output/simple-python-batch`

Run:

```bash
cd test-output/simple-python-batch
docker run --rm -v "$PWD":/app -w /app ghcr.io/astral-sh/uv:python3.12-bookworm-slim uv lock
docker compose build
docker compose run --rm app
ls -1 data/processed
```

### 2) Next.js Nostr Client (base + protocol)

Path:
- `test-output/simple-nextjs-nostr-client`

Run:

```bash
cd test-output/simple-nextjs-nostr-client
docker run --rm -v "$PWD":/app -w /app oven/bun:1.1.38 sh -lc "bun install"
docker compose up --build
```

Open:
- `http://localhost:3000/feed`

### 3) UI Layer Test (`ui-social-feed-shell`)

Path:
- `test-output/ui-social-feed-shell`

Run:

```bash
cd test-output/ui-social-feed-shell
docker compose up --build
```

Open:
- `http://localhost:3000/feed`

Expected checks:
- Desktop 3-column feed shell is visible.
- Composer is login-gated.
- Timeline has loading/empty/error states.
- Internal links use `next/link` (no raw internal anchors).

### 4) Meditations Journal Stack (NIP-23 + Greek Translation)

Path:
- `test-output/meditations-journal-nostr`

Run:

```bash
cd test-output/meditations-journal-nostr
docker compose up --build
```

Open:
- `http://localhost:3000/journal`

Expected checks:
- Signer status gates publish controls.
- Translation pane supports `koine` and `attic`.
- Publish flow emits NIP-23 long-form events (`kind: 30023`).

### 5) Python Multi-Format RAG Worker (Generic)

Path:
- `test-output/simple-python-rag-worker`

Run:

```bash
cd test-output/simple-python-rag-worker
PYTHONPATH=src python3 -m simple_rag_worker.cli rag-ingest --source data/inbox --formats markdown,txt,csv
PYTHONPATH=src python3 -m simple_rag_worker.cli rag-query --q "discipline reason justice" --top-k 3
python3 -m unittest discover -s tests -v
docker compose config
```

Expected checks:
- Ingest writes processed text files to `data/processed`.
- Query returns ranked results from `data/index/index.json`.
- Unit tests pass without additional runtime setup.

## Human Review Gate

Use this by default in production flows:
- `addon-human-pr-review-gate`

Expected artifacts in target project:
- `REVIEW_BUNDLE/SUMMARY.md`
- `REVIEW_BUNDLE/FILE_MANIFEST.txt`
- `REVIEW_BUNDLE/RISK_REPORT.md`
- `REVIEW_BUNDLE/DEPENDENCY_DIFF.md`
- `REVIEW_BUNDLE/DOCKER_REPORT.md`
- `REVIEW_BUNDLE/TEST_EVIDENCE.md`
- `REVIEW_BUNDLE/POLICY_CHECKLIST.md`
- `scripts/review/generate_review_bundle.sh`
- `.github/workflows/review-gate.yml`
- `CODEOWNERS`

## Decision Justification Ledger

Use this by default in production flows:
- `addon-decision-justification-ledger`

Expected artifacts in target project:
- `docs/DECISION_LOG.md`
- `REVIEW_BUNDLE/DECISION_TRACE.md`

Expected checks:
- Every non-trivial architecture or implementation choice has options, chosen path, and rationale.
- Decision IDs map directly to changed files in review bundle.
- Missing rationale is treated as incomplete and blocks merge.

## Domain Semantic Adaptation

Use this by default in production flows:
- `addon-domain-semantic-adaptation`

Expected artifacts in target project:
- `docs/DOMAIN_LANGUAGE.md`
- `docs/DOMAIN_DECISIONS.md`

Expected checks:
- Domain terms from user prompt are reflected in UI/docs.
- Forbidden terms are not used in user-facing copy.
- Technical/security identifiers remain stable where required.

## Eval Pair

Default required:
- `addon-deterministic-eval-suite`

Optional quality layer:
- `addon-llm-judge-evals`

Expected deterministic artifacts:
- `evals/deterministic/manifest.yaml`
- `evals/deterministic/run.sh`
- `.github/workflows/evals-deterministic.yml`

Expected judge artifacts:
- `evals/judge/rubric.md`
- `scripts/evals/run_llm_judge.py`
- `.github/workflows/evals-judge.yml`
- `REVIEW_BUNDLE/JUDGE_REPORT.md`

Policy:
- Deterministic evals are merge-blocking by default.
- LLM judge scores are advisory by default unless explicitly configured as blocking.
- Decision-log and decision-trace checks are merge-blocking in production-default mode.

## NIP Governance (Nostr Projects)

Recommended skills:
- `architect-nostr-intent-router`
- `addon-nostr-nip-profile-selector`
- `addon-nostr-nip-sync-lock`

Expected artifacts:
- `docs/nostr/NIP_REQUIREMENTS.md`
- `docs/nostr/NIP_DECISIONS.md`
- `src/lib/nostr/nip-profile.ts`
- `docs/nostr/NIP_PROFILE.md`
- `scripts/nostr/sync_nips_lock.py`
- `docs/nostr/nips.lock.json`

Refresh lockfile:

```bash
python3 scripts/nostr/sync_nips_lock.py --nips 1,7,19,21,23,65 --out docs/nostr/nips.lock.json --ref master
```

## Skill Naming Enforcement

For this skills repo, enforce frontmatter + folder naming:

```bash
scripts/validation/check_skill_frontmatter.sh .
```

Policy:
- Skill folders must be prefixed with `architect-`, `addon-`, or `ui-`.
- `SKILL.md` frontmatter `name` must exactly match folder name.

## Skill Decision Policy Enforcement

For this skills repo, enforce mandatory decision-justification language in each skill:

```bash
scripts/validation/check_skill_decision_policy.sh .
```

Policy:
- Every skill must include `## Decision Justification Rule`.
- Every skill must state that missing justification is a blocker.

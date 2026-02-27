# ⚡ AI Architect Skills

Composable skills for scaffolding production-ready projects with AI coding agents.

This repo uses a layered model:
- `architect-*`: base infrastructure and project scaffold
- `addon-*`: domain/integration capabilities
- `ui-*`: presentation and UX layers
- `architect-stack-selector`: router that chooses the minimal valid combination

Production default:
- include `addon-human-pr-review-gate` for human-in-the-loop merge safety.
- include `addon-decision-justification-ledger` so each non-trivial decision is traceable.
- include `addon-domain-semantic-adaptation` so output language matches user intent.
- include `addon-deterministic-eval-suite` for hard pass/fail validation.
- use `architect-stack-selector` as control plane (select + scaffold + validate).

## Skill Catalog

Base architect skills:
- `architect-stack-selector`
- `architect-nostr-intent-router`
- `architect-python-uv-batch`
- `architect-python-uv-fastapi-sqlalchemy`
- `architect-nextjs-bun-app`
- `architect-next-prisma-bun-vector`

Add-on skills:
- `addon-decision-justification-ledger`
- `addon-human-pr-review-gate`
- `addon-domain-semantic-adaptation`
- `addon-deterministic-eval-suite`
- `addon-llm-judge-evals`
- `addon-rag-ingestion-pipeline`
- `addon-docling-legal-chunk-embed`
- `addon-nostr-client-nextjs`
- `addon-nostr-nip-profile-selector`
- `addon-nostr-nip-sync-lock`
- `addon-nostr-key-custody`
- `addon-nostr-nip23-longform`
- `addon-llm-ancient-greek-translation`
- `addon-llm-translation`
- `addon-langchain-llm`
- `addon-langgraph-agent`
- `addon-google-agent-dev-kit`
- `addon-vercel-ai-labs`

Legacy (not selected by router by default):
- `addon-rag-pdf-pipeline`

UI skills:
- `ui-social-feed-shell`
- `ui-editorial-writing-surface`
- `ui-document-intake-dropzone`

## Install

If you rename this repo (for example to `ai-architect-skills`), replace `ajrlewis/ai-skills` in commands below with your new `<owner>/<repo>`.

Install all:

```bash
npx skills add ajrlewis/ai-skills --all
```

Install selected:

```bash
npx skills add ajrlewis/ai-skills --skill architect-stack-selector
npx skills add ajrlewis/ai-skills --skill architect-nostr-intent-router
npx skills add ajrlewis/ai-skills --skill architect-nextjs-bun-app
npx skills add ajrlewis/ai-skills --skill addon-nostr-client-nextjs
npx skills add ajrlewis/ai-skills --skill addon-nostr-nip-profile-selector
npx skills add ajrlewis/ai-skills --skill ui-social-feed-shell
npx skills add ajrlewis/ai-skills --skill ui-document-intake-dropzone
npx skills add ajrlewis/ai-skills --skill addon-decision-justification-ledger
npx skills add ajrlewis/ai-skills --skill addon-domain-semantic-adaptation
npx skills add ajrlewis/ai-skills --skill addon-deterministic-eval-suite
npx skills add ajrlewis/ai-skills --skill addon-human-pr-review-gate
npx skills add ajrlewis/ai-skills --skill addon-llm-translation
npx skills add ajrlewis/ai-skills --skill addon-langchain-llm
npx skills add ajrlewis/ai-skills --skill addon-langgraph-agent
npx skills add ajrlewis/ai-skills --skill addon-google-agent-dev-kit
npx skills add ajrlewis/ai-skills --skill addon-vercel-ai-labs
```

Eval pair (deterministic + LLM judge):

```bash
npx skills add ajrlewis/ai-skills --skill addon-deterministic-eval-suite --skill addon-llm-judge-evals
```

Decision visibility default:

```bash
npx skills add ajrlewis/ai-skills --skill addon-decision-justification-ledger
```

Nostr profile + lock workflow:

```bash
npx skills add ajrlewis/ai-skills --skill architect-nostr-intent-router --skill addon-nostr-nip-profile-selector --skill addon-nostr-nip-sync-lock
```

Nostr-aware app routing (detect intents -> choose NIPs -> scaffold):

```bash
npx skills add ajrlewis/ai-skills --skill architect-nextjs-bun-app --skill architect-nostr-intent-router --skill addon-nostr-client-nextjs --skill addon-nostr-nip-profile-selector
```

Typography-first journal stack (Next.js + NIP-23 + Greek translation):

```bash
npx skills add ajrlewis/ai-skills --skill architect-nextjs-bun-app --skill architect-nostr-intent-router --skill addon-nostr-client-nextjs --skill addon-nostr-nip-profile-selector --skill addon-nostr-key-custody --skill addon-nostr-nip23-longform --skill addon-llm-ancient-greek-translation --skill ui-editorial-writing-surface --skill addon-domain-semantic-adaptation --skill addon-human-pr-review-gate
```

Legal PDF clause RAG stack (Docling + embeddings):

```bash
npx skills add ajrlewis/ai-skills --skill architect-python-uv-batch --skill addon-rag-ingestion-pipeline --skill addon-docling-legal-chunk-embed --skill addon-domain-semantic-adaptation --skill addon-human-pr-review-gate
```

## Docs

- Operator workflow and testing: [docs/OPERATIONS.md](docs/OPERATIONS.md)
- Scenario recipes and prompts: [docs/SCENARIOS.md](docs/SCENARIOS.md)

## Naming Check

Enforce skill folder/frontmatter naming policy:

```bash
scripts/validation/check_skill_frontmatter.sh .
```

Enforce decision-justification policy across all skills:

```bash
scripts/validation/check_skill_decision_policy.sh .
```

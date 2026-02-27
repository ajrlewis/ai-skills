# Scenarios

## Quick Compositions

Production note:
- For production-default flows, append `addon-human-pr-review-gate` unless explicitly opting out.
- For production-default flows, append `addon-decision-justification-ledger` (required).
- For production-default flows, append `addon-domain-semantic-adaptation` unless explicitly opting out.
- For production-default flows, append `addon-deterministic-eval-suite` unless explicitly opting out.

- Python data/PDF/Markdown RAG worker:
`architect-python-uv-batch` + `addon-rag-ingestion-pipeline`
- Python legal PDF clause RAG worker:
`architect-python-uv-batch` + `addon-rag-ingestion-pipeline` + `addon-docling-legal-chunk-embed`
- Python API + LangChain LLM routes:
`architect-python-uv-fastapi-sqlalchemy` + `addon-langchain-llm`
- Python API + LangGraph agent workflow:
`architect-python-uv-fastapi-sqlalchemy` + `addon-langgraph-agent`
- Cross-architecture LLM translation:
`architect-nextjs-bun-app` or `architect-python-uv-fastapi-sqlalchemy` + `addon-llm-translation`
- Cross-architecture LangChain LLM routes:
`architect-nextjs-bun-app` or `architect-python-uv-fastapi-sqlalchemy` + `addon-langchain-llm`
- Cross-architecture LangGraph agent workflow:
`architect-nextjs-bun-app` or `architect-python-uv-fastapi-sqlalchemy` + `addon-langgraph-agent`
- Cross-architecture Google ADK agent workflow:
`architect-nextjs-bun-app` or `architect-python-uv-fastapi-sqlalchemy` + `addon-google-agent-dev-kit`
- Next.js Vercel AI Labs workflow:
`architect-nextjs-bun-app` + `addon-vercel-ai-labs`
- Next.js Nostr client:
`architect-nextjs-bun-app` + `architect-nostr-intent-router` + `addon-nostr-client-nextjs` + `addon-nostr-nip-profile-selector`
- Next.js Nostr social feed client:
`architect-nextjs-bun-app` + `architect-nostr-intent-router` + `addon-nostr-client-nextjs` + `addon-nostr-nip-profile-selector` + `ui-social-feed-shell`
- Next.js typography-first Nostr long-form journal:
`architect-nextjs-bun-app` + `architect-nostr-intent-router` + `addon-nostr-client-nextjs` + `addon-nostr-nip-profile-selector` + `addon-nostr-key-custody` + `addon-nostr-nip23-longform` + `addon-llm-ancient-greek-translation` + `ui-editorial-writing-surface`
- Next.js document intake UI for RAG:
`architect-nextjs-bun-app` + `addon-rag-ingestion-pipeline` + `ui-document-intake-dropzone`
- Next.js + Prisma + pgvector:
`architect-next-prisma-bun-vector` (+ `addon-rag-ingestion-pipeline` when ingestion is needed)

## One Command + Prompt

### Python batch RAG (PDF + Markdown)

```bash
npx skills add ajrlewis/ai-skills --skill architect-python-uv-batch --skill addon-rag-ingestion-pipeline
```

```text
Use architect-python-uv-batch and addon-rag-ingestion-pipeline.
Scaffold a Python uv batch project that ingests PDF and Markdown, chunks content, creates embeddings, and supports rag-query with citations.
Mode: production-default with Docker artifacts and CI image build checks.
Run validation and report outcomes.
```

### Python legal clause RAG (Docling)

```bash
npx skills add ajrlewis/ai-skills --skill architect-python-uv-batch --skill addon-rag-ingestion-pipeline --skill addon-docling-legal-chunk-embed
```

```text
Use architect-python-uv-batch, addon-rag-ingestion-pipeline, and addon-docling-legal-chunk-embed.
Scaffold a Python worker that converts legal PDFs to markdown with Docling, chunks by clause/section, and writes embedding-ready index records with citations.
Mode: production-default with Docker artifacts.
Run validation and report outcomes.
```

### FastAPI + LangChain LLM

```bash
npx skills add ajrlewis/ai-skills --skill architect-python-uv-fastapi-sqlalchemy --skill addon-langchain-llm
```

```text
Use architect-python-uv-fastapi-sqlalchemy and addon-langchain-llm.
Add `/v1/llm/chat` with typed request/response, provider/model configuration, and timeout boundaries.
Mode: production-default with containerized validation.
```

### FastAPI + LangGraph agent

```bash
npx skills add ajrlewis/ai-skills --skill architect-python-uv-fastapi-sqlalchemy --skill addon-langgraph-agent
```

```text
Use architect-python-uv-fastapi-sqlalchemy and addon-langgraph-agent.
Add stateful agent run endpoints with checkpointing, step limits, and run telemetry.
Mode: production-default with containerized validation.
```

### Cross-architecture LLM translation

```bash
npx skills add ajrlewis/ai-skills --skill architect-nextjs-bun-app --skill addon-llm-translation
```

```text
Use architect-nextjs-bun-app and addon-llm-translation.
Add a server-side translation route with typed source/target language contract, provider fallback behavior, and explicit review state before publish.
Mode: production-default with containerized validation.
```

### Cross-architecture LangChain LLM

```bash
npx skills add ajrlewis/ai-skills --skill architect-python-uv-fastapi-sqlalchemy --skill addon-langchain-llm
```

```text
Use architect-python-uv-fastapi-sqlalchemy and addon-langchain-llm.
Add provider-agnostic LangChain chat route(s) with typed request/response, allow-listed provider/model selection, and timeout boundaries.
Mode: production-default with containerized validation.
```

### Cross-architecture LangGraph agent

```bash
npx skills add ajrlewis/ai-skills --skill architect-python-uv-fastapi-sqlalchemy --skill addon-langgraph-agent
```

```text
Use architect-python-uv-fastapi-sqlalchemy and addon-langgraph-agent.
Add agent run endpoints with bounded steps, tool allow-list enforcement, and run telemetry for post-run inspection.
Mode: production-default with containerized validation.
```

### Cross-architecture Google ADK agent

```bash
npx skills add ajrlewis/ai-skills --skill architect-python-uv-fastapi-sqlalchemy --skill addon-google-agent-dev-kit
```

```text
Use architect-python-uv-fastapi-sqlalchemy and addon-google-agent-dev-kit.
Implement ADK-backed agent runs with explicit policy boundaries, bounded execution, and degraded fallback when runtime/provider is unavailable.
Mode: production-default with containerized validation.
```

### Next.js Vercel AI Labs

```bash
npx skills add ajrlewis/ai-skills --skill architect-nextjs-bun-app --skill addon-vercel-ai-labs
```

```text
Use architect-nextjs-bun-app and addon-vercel-ai-labs.
Add an AI SDK-based chat route and UI panel with streaming support, typed request/response schemas, provider/model allow-lists, and bounded timeout behavior.
Mode: production-default with Docker artifacts.
```

### Next.js Nostr client

```bash
npx skills add ajrlewis/ai-skills --skill architect-nextjs-bun-app --skill architect-nostr-intent-router --skill addon-nostr-client-nextjs --skill addon-nostr-nip-profile-selector
```

```text
Use architect-nextjs-bun-app, architect-nostr-intent-router, addon-nostr-client-nextjs, and addon-nostr-nip-profile-selector.
Detect Nostr intent, choose a justified NIP profile, then scaffold relay subscription, NIP-07 login, and publish flow with explicit NIP contract docs.
Mode: production-default with Docker artifacts.
```

### Next.js Nostr social feed client

```bash
npx skills add ajrlewis/ai-skills --skill architect-nextjs-bun-app --skill architect-nostr-intent-router --skill addon-nostr-client-nextjs --skill addon-nostr-nip-profile-selector --skill ui-social-feed-shell
```

```text
Use architect-nextjs-bun-app, architect-nostr-intent-router, addon-nostr-client-nextjs, addon-nostr-nip-profile-selector, and ui-social-feed-shell.
Build a login-gated Nostr feed with composer, timeline, side rails, and responsive social layout.
Mode: production-default with Docker artifacts.
Run lint/build and summarize generated UI layers.
```

### Next.js typography-first journal (NIP-23 + Ancient Greek)

```bash
npx skills add ajrlewis/ai-skills --skill architect-nextjs-bun-app --skill architect-nostr-intent-router --skill addon-nostr-client-nextjs --skill addon-nostr-nip-profile-selector --skill addon-nostr-key-custody --skill addon-nostr-nip23-longform --skill addon-llm-ancient-greek-translation --skill ui-editorial-writing-surface
```

```text
Use architect-nextjs-bun-app, architect-nostr-intent-router, addon-nostr-client-nextjs, addon-nostr-nip-profile-selector, addon-nostr-key-custody, addon-nostr-nip23-longform, addon-llm-ancient-greek-translation, and ui-editorial-writing-surface.
Build a minimalist Next.js journal inspired by Marcus Aurelius's Meditations with typography-first writing flow, private key management, Koine/Attic translation preview, and NIP-23 long-form publish (kind 30023).
Mode: production-default with Docker artifacts.
Run lint/build and summarize signer, translation, and publish flows.
```

### Next.js PDF/Markdown intake UI

```bash
npx skills add ajrlewis/ai-skills --skill architect-nextjs-bun-app --skill addon-rag-ingestion-pipeline --skill ui-document-intake-dropzone
```

```text
Use architect-nextjs-bun-app, addon-rag-ingestion-pipeline, and ui-document-intake-dropzone.
Build a responsive document intake route where users can add PDF/Markdown files, view queue states, and trigger ingestion actions.
Mode: production-default with Docker artifacts.
Run lint/build and summarize intake state handling.
```

### Nostr NIP profile + lock sync

```bash
npx skills add ajrlewis/ai-skills --skill architect-nostr-intent-router --skill addon-nostr-nip-profile-selector --skill addon-nostr-nip-sync-lock
```

```text
Use architect-nostr-intent-router, addon-nostr-nip-profile-selector, and addon-nostr-nip-sync-lock.
Detect product-level Nostr requirements, select a justified NIP profile, generate docs/nostr/NIP_REQUIREMENTS.md plus docs/nostr/NIP_PROFILE.md, and add scripts/nostr/sync_nips_lock.py with docs/nostr/nips.lock.json.
```

### Next.js + Prisma + pgvector

```bash
npx skills add ajrlewis/ai-skills --skill architect-next-prisma-bun-vector
```

```text
Use architect-next-prisma-bun-vector.
Scaffold a production-ready Next.js + Prisma + PostgreSQL/pgvector stack with Docker, CI, and sample vector search service.
Mode: production-default.
Run validation and report outcomes.
```

### Router-first

```bash
npx skills add ajrlewis/ai-skills --skill architect-stack-selector
```

```text
Use architect-stack-selector.
Goal: <describe app in one sentence>.
Constraints: <runtime preferences, data formats, db, deployment target>.
Mode: production-default (unless explicitly NO_DOCKER=yes).
Decision visibility: required with explicit rationale per non-trivial choice.
Select the minimal skill set, scaffold it, and run each selected skill's validation checklist.
```

### Human PR review gate only

```bash
npx skills add ajrlewis/ai-skills --skill addon-human-pr-review-gate
```

```text
Use addon-human-pr-review-gate.
Add a REVIEW_BUNDLE, trusted PR review workflow, and CODEOWNERS protections so human reviewers can safely approve agent-generated code.
```

### Decision justification ledger only

```bash
npx skills add ajrlewis/ai-skills --skill addon-decision-justification-ledger
```

```text
Use addon-decision-justification-ledger.
Add docs/DECISION_LOG.md and REVIEW_BUNDLE/DECISION_TRACE.md, and require explicit rationale for every non-trivial decision.
```

### Domain semantic adaptation only

```bash
npx skills add ajrlewis/ai-skills --skill addon-domain-semantic-adaptation
```

```text
Use addon-domain-semantic-adaptation.
Adapt generated UI/docs/aliases to domain-specific terminology from the user prompt and emit docs/DOMAIN_LANGUAGE.md plus docs/DOMAIN_DECISIONS.md.
```

### Eval pair (deterministic + LLM judge)

```bash
npx skills add ajrlewis/ai-skills --skill addon-deterministic-eval-suite --skill addon-llm-judge-evals
```

```text
Use addon-deterministic-eval-suite and addon-llm-judge-evals.
Add hard pass fail eval checks plus rubric-based LLM quality scoring. Keep deterministic checks merge-blocking and LLM judge advisory unless explicitly configured as blocking.
```

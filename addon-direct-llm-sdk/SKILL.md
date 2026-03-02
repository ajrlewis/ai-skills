---
name: addon-direct-llm-sdk
description: Use when a project needs direct provider SDK based LLM calls without LangChain, Google ADK, or Vercel AI abstractions; pair with architect-stack-selector.
---

# Add-on: Direct LLM SDK

Use this skill when a project needs explicit provider SDK control for chat, completions, embeddings, or tool calls without an additional orchestration framework.

## Compatibility

- Works with `architect-python-uv-fastapi-sqlalchemy`, `architect-python-uv-batch`, `architect-nextjs-bun-app`, and `architect-next-prisma-bun-vector`.
- Use this instead of `addon-langchain-llm` when abstraction overhead is not wanted.
- If paired with `addon-llm-judge-evals`, do not assume auto backend resolution; the current judge contract must be extended before direct SDK becomes a supported judge backend.

## Inputs

Collect:
- `SDK_PROVIDER`: `openai` | `anthropic` | `google` | `openrouter`.
- `DEFAULT_MODEL`: provider model id.
- `ENABLE_STREAMING`: `yes` | `no` (default `yes`).
- `REQUEST_TIMEOUT_SECONDS`: default `60`.
- `MAX_RETRIES`: default `2`.

## Integration Workflow

1. Add provider client artifacts:
```text
src/{{MODULE_NAME}}/llm/client.*
src/{{MODULE_NAME}}/llm/types.*
src/{{MODULE_NAME}}/llm/provider_config.*
src/{{MODULE_NAME}}/api/routes/llm.*
docs/LLM_PROVIDER_POLICY.md
```

2. Bound provider usage:
- centralize SDK initialization
- enforce provider and model allow-lists
- add timeout, retry, and cancellation controls

3. Normalize app contract:
- return stable typed responses independent of provider
- translate provider-specific errors into controlled app errors
- keep streaming and non-streaming shapes consistent

4. Protect operational safety:
- keep API credentials server-only
- log provider metadata, not raw prompts or secrets, unless explicitly required
- define fallback behavior for provider outages

## Required Template

### Chat response shape
```json
{
  "outputText": "string",
  "model": "string",
  "provider": "string"
}
```

## Guardrails

- Documentation contract for generated code:
  - Python: write module docstrings and docstrings for public classes, methods, and functions.
  - Next.js/TypeScript: write JSDoc for exported components, hooks, utilities, and route handlers.
  - Add concise rationale comments only for non-obvious logic, invariants, or safety constraints.
  - Apply this contract even when using template snippets below; expand templates as needed.


- Do not expose provider SDK clients directly to untrusted client code.
- Do not let callers pass arbitrary provider or model values without validation.
- Normalize provider-specific exceptions before they cross route boundaries.
- Prefer one internal adapter per provider so future migrations stay contained.
- If `addon-llm-judge-evals` is present, either use a separately supported judge backend or extend the judge contract explicitly before advertising direct-SDK judge support.

## Validation Checklist

- Confirm generated code includes required docstrings/JSDoc and rationale comments for non-obvious logic.


```bash
test -f docs/LLM_PROVIDER_POLICY.md || true
rg -n "DEFAULT_MODEL|provider|stream|timeout|retry" src || true
```

Manual checks:
- Invalid provider or model requests fail with controlled validation errors.
- Streaming disconnects stop upstream provider generation promptly.

## Decision Justification Rule

- Every non-trivial decision must include a concrete justification.
- Capture the alternatives considered and why they were rejected.
- State tradeoffs and residual risks for the chosen option.
- If justification is missing, treat the task as incomplete and surface it as a blocker.

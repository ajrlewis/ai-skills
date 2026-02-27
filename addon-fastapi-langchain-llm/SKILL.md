---
name: addon-fastapi-langchain-llm
description: Use when adding LangChain LLM chat or retrieval routes to FastAPI; pair with architect-python-uv-fastapi-sqlalchemy.
---

# Add-on: FastAPI + LangChain LLM

Use this skill when an existing FastAPI service needs LLM-powered endpoints (chat, retrieval, summarization) using LangChain primitives.

## Compatibility

- Best with `architect-python-uv-fastapi-sqlalchemy`.
- Can be layered onto any Python FastAPI project with async request handlers.

## Inputs

Collect:
- `LLM_PROVIDER`: `openai` | `anthropic` | `ollama` (default `openai`).
- `DEFAULT_MODEL`: provider model id.
- `ENABLE_STREAMING`: `yes`/`no` (default `yes`).
- `USE_RAG`: `yes`/`no`.
- `MAX_INPUT_TOKENS`: default `8000`.

## Integration Workflow

1. Add dependencies:
```bash
uv add langchain langchain-core langchain-community pydantic-settings tiktoken
```
- Provider packages:
```bash
uv add langchain-openai
uv add langchain-anthropic
```
- Optional local provider:
```bash
uv add langchain-ollama
```

2. Add files:
```text
src/{{MODULE_NAME}}/llm/provider.py
src/{{MODULE_NAME}}/llm/prompts.py
src/{{MODULE_NAME}}/llm/chains.py
src/{{MODULE_NAME}}/api/routes/llm.py
src/{{MODULE_NAME}}/schemas/llm.py
```

3. Register the new router in app bootstrap:
- `app.include_router(llm_router, prefix="/v1/llm")`

4. Add env variables:
- `LLM_PROVIDER`
- `LLM_MODEL`
- `OPENAI_API_KEY` or provider-specific equivalent

5. If `USE_RAG=yes`, integrate retriever interface from your RAG add-on and compose retrieval chain.

## Required Templates

### `src/{{MODULE_NAME}}/schemas/llm.py`
```python
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=8000)
    stream: bool = True


class ChatResponse(BaseModel):
    output_text: str
    model: str
```

### `src/{{MODULE_NAME}}/llm/provider.py`
```python
from langchain_openai import ChatOpenAI


def build_chat_model(model: str, temperature: float = 0.2):
    return ChatOpenAI(model=model, temperature=temperature)
```

### `src/{{MODULE_NAME}}/api/routes/llm.py`
```python
from fastapi import APIRouter

from {{MODULE_NAME}}.schemas.llm import ChatRequest, ChatResponse

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest) -> ChatResponse:
    # Replace with LangChain chain invocation in implementation phase.
    return ChatResponse(output_text=f"echo: {payload.message}", model="placeholder")
```

## Guardrails

- Validate request size/tokens before model invocation.
- Never log secrets or raw auth headers.
- Enforce model/provider selection from allow-list.
- Add timeout and retry boundaries around upstream LLM calls.
- For streaming, gracefully terminate on client disconnect.

## Validation Checklist

```bash
uv run ruff check .
uv run mypy src
uv run pytest -q
uv run python -m compileall src
```
- Manual checks:
- `POST /v1/llm/chat` returns typed response.
- Invalid payload returns `422`.
- Timeout path returns controlled 5xx/4xx response contract.

## Decision Justification Rule

- Every non-trivial decision must include a concrete justification.
- Capture the alternatives considered and why they were rejected.
- State tradeoffs and residual risks for the chosen option.
- If justification is missing, treat the task as incomplete and surface it as a blocker.

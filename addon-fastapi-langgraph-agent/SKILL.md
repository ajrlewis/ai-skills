---
name: addon-fastapi-langgraph-agent
description: Use when adding LangGraph stateful agent workflows to FastAPI; pair with architect-python-uv-fastapi-sqlalchemy.
---

# Add-on: FastAPI + LangGraph Agent

Use this skill when a FastAPI project needs multi-step agent workflows (tool use, planning, stateful execution) via LangGraph.

## Compatibility

- Best with `architect-python-uv-fastapi-sqlalchemy`.
- Can be combined with `addon-fastapi-langchain-llm`.

## Inputs

Collect:
- `AGENT_SCOPE`: primary tasks the agent is allowed to perform.
- `CHECKPOINT_BACKEND`: `memory` | `postgres` | `redis`.
- `ALLOW_TOOLS`: list of tool names.
- `MAX_STEPS`: default `10`.
- `TIMEOUT_SECONDS`: default `45`.

## Integration Workflow

1. Add dependencies:
```bash
uv add langgraph langchain-core pydantic-settings
```
- Optional persistence:
```bash
uv add psycopg[binary] redis
```

2. Add files:
```text
src/{{MODULE_NAME}}/agent/state.py
src/{{MODULE_NAME}}/agent/graph.py
src/{{MODULE_NAME}}/agent/tools.py
src/{{MODULE_NAME}}/agent/checkpoint.py
src/{{MODULE_NAME}}/api/routes/agent.py
src/{{MODULE_NAME}}/schemas/agent.py
```

3. Expose execution endpoints:
- `POST /v1/agent/runs`
- `GET /v1/agent/runs/{run_id}`

4. Add run telemetry:
- `run_id`, `steps`, `status`, `started_at`, `finished_at`, `error`

## Required Templates

### `src/{{MODULE_NAME}}/schemas/agent.py`
```python
from pydantic import BaseModel, Field


class AgentRunRequest(BaseModel):
    input_text: str = Field(min_length=1, max_length=12000)
    thread_id: str


class AgentRunResponse(BaseModel):
    run_id: str
    status: str
```

### `src/{{MODULE_NAME}}/agent/state.py`
```python
from typing import TypedDict


class AgentState(TypedDict, total=False):
    thread_id: str
    input_text: str
    output_text: str
    step_count: int
```

### `src/{{MODULE_NAME}}/api/routes/agent.py`
```python
import uuid
from fastapi import APIRouter

from {{MODULE_NAME}}.schemas.agent import AgentRunRequest, AgentRunResponse

router = APIRouter()


@router.post("/runs", response_model=AgentRunResponse)
async def create_run(payload: AgentRunRequest) -> AgentRunResponse:
    run_id = str(uuid.uuid4())
    return AgentRunResponse(run_id=run_id, status="queued")
```

## Guardrails

- Documentation contract for generated code:
  - Python: write module docstrings and docstrings for public classes, methods, and functions.
  - Next.js/TypeScript: write JSDoc for exported components, hooks, utilities, and route handlers.
  - Add concise rationale comments only for non-obvious logic, invariants, or safety constraints.
  - Apply this contract even when using template snippets below; expand templates as needed.


- Restrict agent tools to explicit allow-list.
- Enforce max step count and execution timeout.
- Do not allow arbitrary shell/network tools unless explicitly approved.
- Persist run status and failures for inspection.
- Keep deterministic fallbacks for provider/tool failures.

## Validation Checklist

- Confirm generated code includes required docstrings/JSDoc and rationale comments for non-obvious logic.


```bash
uv run ruff check .
uv run mypy src
uv run pytest -q
```
- Manual checks:
- Run creation returns `run_id`.
- Invalid input rejected with `422`.
- Agent aborts after `MAX_STEPS` and returns bounded error.

## Decision Justification Rule

- Every non-trivial decision must include a concrete justification.
- Capture the alternatives considered and why they were rejected.
- State tradeoffs and residual risks for the chosen option.
- If justification is missing, treat the task as incomplete and surface it as a blocker.

---
name: architect-nextjs-bun-app
description: Use when scaffolding a production-ready Next.js Bun Docker base for web apps.
---

# Architect: Next.js + Bun App

Use this skill to scaffold a production-minded Next.js app baseline before layering domain-specific add-ons.

## Inputs

Collect:
- `PROJECT_NAME`: kebab-case folder/package name.
- `USE_TAILWIND`: `yes`/`no` (default `yes`).
- `APP_PORT`: default `3000`.
- `NO_DOCKER`: default `no`. Set `yes` only when user explicitly opts out.

Version defaults:
- `create-next-app@15`
- `oven/bun` image `1.1.38-alpine`

## Preflight Checks

Run before scaffolding:
```bash
command -v bun >/dev/null && bun --version || echo "bun-missing"
command -v docker >/dev/null && docker --version || echo "docker-missing"
```

Execution modes:
- `production-default`: containerized scaffold and validation (`NO_DOCKER=no`).
- `local-no-docker`: skip container files only when user explicitly sets `NO_DOCKER=yes`.
- `offline-smoke`: tool/network constrained; scaffold and run limited checks.

Production-default contract:
- Must create `Dockerfile`, `.dockerignore`, and `docker-compose.yml`.
- Must include CI image build check.
- Must include at least one containerized validation command.

## Scaffold Workflow

1. Initialize app:
```bash
bunx --bun create-next-app@15 {{PROJECT_NAME}} --typescript --eslint --src-dir --app --use-bun --import-alias "@/*"
cd {{PROJECT_NAME}}
```
- If `USE_TAILWIND=yes`, include `--tailwind`.
- If `offline-smoke` blocks `create-next-app`, manually scaffold minimal Next structure:
```text
package.json
bun.lockb (or note pending generation when network is available)
tsconfig.json
next-env.d.ts
next.config.ts
public/
src/app/layout.tsx
src/app/page.tsx
src/app/globals.css
```
- In `offline-smoke`, include `TEST_NOTES.md` with constraints and unverified checks.

2. Add test stack:
```bash
bun add -d vitest @vitest/coverage-v8 jsdom @types/node
```

3. Add project files:
- `vitest.config.ts`
- `Dockerfile`
- `.dockerignore`
- `docker-compose.yml`
- `.github/workflows/ci.yml`
- `src/lib/env.ts`
If `NO_DOCKER=yes`, explicitly document the exception and skip container artifacts/checks.

## Required Templates

### `src/lib/env.ts`
```typescript
import { z } from "zod";

const EnvSchema = z.object({
  NODE_ENV: z.enum(["development", "test", "production"]).default("development"),
});

export const env = EnvSchema.parse(process.env);
```

### `vitest.config.ts`
```typescript
import path from "node:path";
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    environment: "jsdom",
    coverage: {
      provider: "v8",
      reporter: ["text", "lcov", "html"],
    },
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
});
```

### `Dockerfile`
```dockerfile
FROM oven/bun:1.1.38-alpine AS deps
WORKDIR /app
COPY package.json bun.lockb* ./
RUN bun install --frozen-lockfile

FROM deps AS build
WORKDIR /app
COPY . .
RUN bun run build

FROM oven/bun:1.1.38-alpine AS run
WORKDIR /app
ENV NODE_ENV=production
ENV PORT={{APP_PORT}}
COPY --from=build /app/package.json /app/bun.lockb* ./
COPY --from=build /app/node_modules ./node_modules
COPY --from=build /app/.next ./.next
COPY --from=build /app/public ./public
USER bun
EXPOSE {{APP_PORT}}
CMD ["bun", "run", "start"]
```

### `.dockerignore`
```gitignore
.git
node_modules
.next
coverage
.turbo
*.log
```

### `docker-compose.yml` (`NO_DOCKER=no`)
```yaml
services:
  web:
    build: .
    environment:
      PORT: "{{APP_PORT}}"
      NODE_ENV: production
    ports:
      - "{{APP_PORT}}:{{APP_PORT}}"
```

### `.github/workflows/ci.yml`
```yaml
name: ci
on:
  push:
  pull_request:

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v2
        with:
          bun-version: "1.1.38"
      - run: bun install --frozen-lockfile
      - run: bun run lint
      - run: bunx vitest run --coverage
      - run: bun run build
      - uses: docker/setup-buildx-action@v3
      - uses: docker/build-push-action@v6
        with:
          context: .
          push: false
          tags: {{PROJECT_NAME}}:ci
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

## Guardrails

- Avoid `@latest` for runtime-critical scaffold dependencies.
- Keep browser-only APIs out of server components.
- Validate environment variables at startup.
- Run the container as non-root (`USER bun`).
- Treat `NO_DOCKER=yes` as explicit exception behavior.
- Ensure `bun.lockb` exists before Docker build when using `--frozen-lockfile`.

## Validation Checklist

```bash
bun run lint
bunx vitest run --coverage
bun run build
test -f bun.lockb
docker build -t {{PROJECT_NAME}}:local .
docker compose up -d --build
```
`local-no-docker` (`NO_DOCKER=yes`):
```bash
bun run lint
bunx vitest run --coverage
bun run build
```
Fallback (`offline-smoke`):
```bash
test -f package.json
test -d public
test -f src/app/page.tsx
test -f src/app/layout.tsx
test -f Dockerfile || echo "docker-artifacts-missing-in-offline-smoke"
```

## Decision Justification Rule

- Every non-trivial decision must include a concrete justification.
- Capture the alternatives considered and why they were rejected.
- State tradeoffs and residual risks for the chosen option.
- If justification is missing, treat the task as incomplete and surface it as a blocker.

---
name: architect-nextjs-vercel-app
description: Use when scaffolding a production-ready Next.js (Node + pnpm) app intended for deployment on Vercel; includes Vercel-friendly defaults, CI, Vitest, env validation, and optional Docker parity for local/CI reproducibility.
---

# Architect: Next.js + Vercel App

Use this skill to scaffold a production-minded Next.js baseline optimized for Vercel deployment.
By default, include Docker artifacts for local/CI parity and deterministic builds. Only allow `NO_DOCKER=yes` when the user explicitly opts out.

## Inputs

Collect:
- `PROJECT_NAME`: kebab-case folder/package name.
- `USE_TAILWIND`: `yes`/`no` (default `yes`).
- `APP_PORT`: default `3000`.
- `PKG_MANAGER`: default `pnpm`.
- `NO_DOCKER`: default `no`. Set `yes` only when user explicitly opts out.

Version defaults:
- `create-next-app@15`
- Node base image: `node:20-alpine` (update to active LTS only when requested)

## Preflight Checks

Run before scaffolding:
```bash
command -v node >/dev/null && node --version || echo "node-missing"
command -v corepack >/dev/null && corepack --version || echo "corepack-missing"
command -v docker >/dev/null && docker --version || echo "docker-missing"
```

## Scaffold Workflow

1. Initialize app:
```bash
corepack enable
npx create-next-app@15 {{PROJECT_NAME}} --typescript --eslint --src-dir --app --import-alias "@/*" --use-pnpm
cd {{PROJECT_NAME}}
```
- If `USE_TAILWIND=yes`, include `--tailwind`.
- If `offline-smoke` constraints block `create-next-app`, manually scaffold a minimal Next structure and add `TEST_NOTES.md` describing what could not be verified yet.

2. Add baseline packages:
```bash
pnpm add zod
pnpm add -D vitest @vitest/coverage-v8 jsdom @types/node eslint-plugin-jsdoc
```

3. Add project files:
- `src/lib/env.ts`
- `vitest.config.ts`
- `eslint.config.mjs` (extend generated Next config with JSDoc rules for exported symbols)
- `.github/workflows/ci.yml`
- `vercel.json`
- If `NO_DOCKER=no`: `Dockerfile`, `.dockerignore`, and `docker-compose.yml`

4. Add scripts (if missing):
- `test`: `vitest`
- `test:ci`: `vitest run --coverage`

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

### `eslint.config.mjs` (extend generated config)
```javascript
import { dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { FlatCompat } from "@eslint/eslintrc";
import jsdoc from "eslint-plugin-jsdoc";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const compat = new FlatCompat({
  baseDirectory: __dirname,
});

const eslintConfig = [
  ...compat.extends("next/core-web-vitals", "next/typescript"),
  {
    files: ["src/**/*.{ts,tsx}"],
    plugins: { jsdoc },
    rules: {
      "jsdoc/require-jsdoc": [
        "error",
        {
          contexts: [
            "ExportNamedDeclaration > FunctionDeclaration",
            "ExportDefaultDeclaration > FunctionDeclaration",
            "ExportNamedDeclaration > ClassDeclaration",
            "ExportNamedDeclaration > VariableDeclaration > VariableDeclarator[init.type='ArrowFunctionExpression']",
          ],
        },
      ],
      "jsdoc/require-description": "error",
      "jsdoc/require-param": "off",
      "jsdoc/require-returns": "off",
    },
  },
];

export default eslintConfig;
```

### `vercel.json`
```json
{
  "framework": "nextjs",
  "installCommand": "pnpm install --frozen-lockfile",
  "buildCommand": "pnpm build"
}
```

### `Dockerfile` (`NO_DOCKER=no`)
```dockerfile
FROM node:20-alpine AS deps
WORKDIR /app
RUN corepack enable
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

FROM node:20-alpine AS build
WORKDIR /app
RUN corepack enable
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN pnpm run build

FROM node:20-alpine AS prod-deps
WORKDIR /app
RUN corepack enable
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile --prod

FROM node:20-alpine AS run
WORKDIR /app
ENV NODE_ENV=production
ENV PORT={{APP_PORT}}
RUN corepack enable
COPY --from=build /app/package.json ./package.json
COPY --from=build /app/public ./public
COPY --from=build /app/.next ./.next
COPY --from=prod-deps /app/node_modules ./node_modules
EXPOSE {{APP_PORT}}
CMD ["pnpm", "run", "start"]
```

### `.dockerignore`
```gitignore
.git
node_modules
.next
coverage
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
      - uses: actions/setup-node@v4
        with:
          node-version: "lts/*"
      - uses: pnpm/action-setup@v4
        with:
          version: "9"
      - run: pnpm install --frozen-lockfile
      - run: pnpm run lint
      - run: pnpm run test:ci
      - run: pnpm run build
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

- Documentation contract for generated code:
  - Python: write module docstrings and docstrings for public classes, methods, and functions.
  - Next.js/TypeScript: write JSDoc for exported components, hooks, utilities, and route handlers.
  - Add concise rationale comments only for non-obvious logic, invariants, or safety constraints.
  - Apply this contract even when using template snippets below; expand templates as needed.


- Avoid `@latest` for runtime-critical scaffold dependencies.
- Keep browser-only APIs out of server components.
- Validate environment variables at startup.
- Treat `NO_DOCKER=yes` as explicit exception behavior and document it.
- Ensure `pnpm-lock.yaml` is committed before Docker build; the Dockerfile copies it explicitly for deterministic `--frozen-lockfile` installs.

## Validation Checklist

- Confirm generated code includes required docstrings/JSDoc and rationale comments for non-obvious logic.

`NO_DOCKER=no`:
```bash
pnpm run lint
pnpm run test:ci
pnpm run build
test -f pnpm-lock.yaml
docker build -t {{PROJECT_NAME}}:local .
docker run --rm -d -p {{APP_PORT}}:{{APP_PORT}} --name {{PROJECT_NAME}}-smoke {{PROJECT_NAME}}:local
curl http://localhost:{{APP_PORT}}/
docker stop {{PROJECT_NAME}}-smoke
docker compose up -d --build
```
`local-no-docker` (`NO_DOCKER=yes`):
```bash
pnpm run lint
pnpm run test:ci
pnpm run build
```
Fallback (`offline-smoke`):
```bash
test -f package.json
test -d public
test -f src/app/page.tsx
test -f src/app/layout.tsx
test -f vercel.json
test -f Dockerfile || echo "docker-artifacts-missing-in-offline-smoke"
```

## Decision Justification Rule

- Every non-trivial decision must include a concrete justification.
- Capture the alternatives considered and why they were rejected.
- State tradeoffs and residual risks for the chosen option.
- If justification is missing, treat the task as incomplete and surface it as a blocker.

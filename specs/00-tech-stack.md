# 00 — Tech Stack

Status: accepted
Date: 2026-09-06

## Scope of this document

Technology decisions only. Functional requirements live in `01.index-information.md` onward.

## Backend

| Concern | Choice | Why |
|---|---|---|
| Language | Python 3.12+ | Modern typing and generics, stable perf |
| Framework | FastAPI | Async, Pydantic-native, auto OpenAPI |
| ASGI server | Uvicorn | Standard for FastAPI |
| Validation / DTOs | Pydantic v2 | Request/response schemas, settings |
| ORM | SQLAlchemy 2.0 (async) | Mature, explicit, good with complex tournament queries |
| Migrations | Alembic | Schema versioning from day one |
| Database | PostgreSQL 16 | Relational data (teams, matches, standings), CTEs/window functions for rankings |
| Auth | JWT (access + refresh), `bcrypt`/`argon2` hashing | Stateless, works well with SPA |
| Testing | pytest + pytest-asyncio + httpx.AsyncClient | Fast, async-native |
| Test data | factory-boy / Faker | Seed tournaments, brackets |
| Lint / format | Ruff (lint + format) + mypy | One tool, fast |
| Package manager | uv | Fast, lockfile, replaces pip/poetry |

## Frontend

| Concern | Choice | Why |
|---|---|---|
| Language | TypeScript | Type parity with backend schemas |
| Framework | React 19 + Vite | SPA, fast dev server, no SSR complexity needed |
| Routing | React Router v7 | Standard for SPA |
| Server state | TanStack Query | Cache, refetch, optimistic updates for live scores |
| Forms | React Hook Form + Zod | Validation mirrored from backend rules |
| Styling | Tailwind CSS + shadcn/ui | Fast, consistent, accessible primitives |
| API client | openapi-typescript (types generated from FastAPI's OpenAPI) | Backend contract is the source of truth |
| Testing | Vitest + React Testing Library + MSW | Unit/integration without a real backend |
| E2E | Playwright | Bracket flows are worth testing end to end |
| Animation | Motion (ex-Framer Motion) | Hero animation + UI transitions; single library (`01.index-information.md` §3) |
| i18n | react-i18next | EN/ES; frontend owns all translation (`01.index-information.md` §6) |
| Fonts | Fontsource (Inter + Barlow Condensed) | Self-hosted, no third-party request (`01.index-information.md` §1) |
| Package manager | pnpm | Fast, strict node_modules |

## Toolchain versions (verified 2026-09-06)

Pinned identically in `frontend/Dockerfile`, `.github/workflows/ci.yml`, and `package.json`.

| Tool | Version | Note |
|---|---|---|
| Python | 3.12 | via uv |
| Node | 24 LTS | not 26 — CI should not run a non-LTS runtime |
| pnpm | 11 | `packageManager` field pins it |
| Vite | 8 | `@vitejs/plugin-react@6` requires it |
| Vitest | 5 | supports Vite 6-8; Vitest 2 bundles Vite 5 and conflicts |

Vite, Vitest and `@vitejs/plugin-react` must move together — their peer ranges are coupled.

## Architecture

- **Layout**: monorepo — `backend/` + `frontend/` + `specs/`.
- **Backend layering**: `api/` (routers) → `services/` (domain logic: bracket generation, standings, scheduling) → `repositories/` (persistence) → `models/`.
  Rationale: tournament rules (round-robin points, tiebreakers, elimination progression) are real domain logic and must be testable without HTTP or DB.
- **Contract**: FastAPI generates OpenAPI → frontend types generated from it. No hand-written API types.
- **Local dev**: Docker Compose (floci + postgres + backend + frontend).
- **AWS**: all AWS interaction goes through Floci locally (`http://localhost:4566`) — see `02-floci-local-aws.md`. AWS endpoint is a setting, unset in real AWS.
- **CI**: GitHub Actions — ruff, mypy, pytest, vitest, build.

## Execution status (audited 2026-09-06)

The stack is **chosen and scaffolded**, not fully exercised. Recorded honestly so nobody reads
a row above as "this works today".

| State | Rows |
|---|---|
| **Proven end to end** | FastAPI, Uvicorn, Pydantic, Ruff, mypy, pytest, uv, TypeScript, React, Vite, TanStack Query, Tailwind, Vitest, RTL, MSW, pnpm |
| **Installed, not yet wired** | React Router, React Hook Form + Zod, openapi-typescript, factory-boy/Faker, SQLAlchemy + Alembic (0 models, 0 migrations), PyJWT + argon2 |
| **Declared, not installed** | shadcn/ui (`components.json` present, no components); Motion, react-i18next, Fontsource (committed by spec 01) |
| **Never exercised** | Docker Compose, Floci, PostgreSQL — Docker daemon has not been running |

Deferring the "not yet wired" rows is deliberate: wiring a router before a second route, or
generating API types before a real endpoint, would be speculative. This is not debt.

## Deliberately left out (for now)

- Redis / Celery — ruled out for background jobs by ADR 001 (SQS + Lambda instead).
- WebSockets — **confirmed unnecessary.** `01.index-information.md` rev 3 defines a match as
  team vs team with a manually entered score; there is no live timing or play-by-play, so
  TanStack Query refetching suffices. Revisit only if live scoring is ever introduced.
- Next.js — no SEO/SSR requirement stated; Vite is simpler.

## Impact of Floci

Practicing AWS is an explicit project goal, so some decisions above become genuinely open:

- **Auth — deferred by the CEO (2026-09-06).** Hand-rolled JWT vs. **Cognito** (Floci emulates
  it; LocalStack community did not). `01.index-information.md` treats Login as a route with no
  flow behind it, so the index page does not need this. To be decided when authentication is
  actually implemented.
- **Database** — plain Postgres container vs. **RDS via Floci** (real `postgres:16-alpine` behind the RDS API).
- **File storage** — local disk vs. **S3** for logos/exports. S3 is the obvious pick.
- ~~Background work~~ — **decided: SQS + container-image Lambda**, see `05-adr/001-background-work.md`.

These get decided per requirement, not upfront.

## Assumptions

1. Single deployment, not multi-tenant SaaS. **Still holds** after `01.index-information.md`
   rev 2: the free-tier tournament quota attaches to a *user*, not an organisation, so no
   tenant scoping is introduced. Billing itself is now a committed direction, not hypothetical.
2. Web only, it's necessary have responsive design.
3. Tournament data is relational and moderate in volume (thousands of matches, not millions).

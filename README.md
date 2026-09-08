# Sports Tournament

Tournament management app — FastAPI backend, React frontend, local AWS via
[Floci](https://github.com/floci-io/floci).

Design decisions live in [`specs/`](specs/). Start with
[`specs/00-tech-stack.md`](specs/00-tech-stack.md).

## Layout

```
backend/    FastAPI service (api -> services -> repositories -> models)
frontend/   React 19 + Vite SPA
specs/      Living design docs and ADRs
compose.yaml  floci + postgres + backend + frontend
```

## Prerequisites

| Tool | Purpose |
|---|---|
| Docker | Compose stack; Floci needs the Docker socket for Lambda/RDS/ECS |
| [uv](https://docs.astral.sh/uv/) | Backend dependencies |
| Node 22 + pnpm | Frontend dependencies |

## Quick start

```bash
# Everything, in containers
make up                 # http://localhost:5173 (web), :8000 (api), :4566 (aws)

# Or run pieces locally
make backend-install && make backend-test
make frontend-install && make frontend-test
```

`make help` lists every target.

## The one rule to remember

`AWS_ENDPOINT_URL` is **set** locally (pointing at Floci) and **unset** in real AWS, so the
same code runs against both. All AWS clients are built in
[`backend/src/tournament/aws/clients.py`](backend/src/tournament/aws/clients.py) — nowhere else.

## Architecture guardrail

`backend/src/tournament/services/` must not import FastAPI, boto3, or SQLAlchemy. That is what
lets one domain module serve both an HTTP route and a Lambda handler
([ADR 001](specs/05-adr/001-background-work.md)). The rule is enforced by
`backend/tests/test_architecture.py`, not by convention.

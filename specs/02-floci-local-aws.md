# 02 — Floci: local AWS

Status: proposed
Date: 2026-09-06
Source: https://github.com/floci-io/floci · docs https://floci.io/floci/

## Why it's here

Practicing AWS (deploys, service wiring, IaC) is an explicit goal of this project, not a side
effect. Floci is a free MIT-licensed local AWS emulator — the LocalStack community replacement
after that edition sunset in March 2026. No AWS account, no auth token, no feature gates.

## The one thing to understand

Every AWS service Floci emulates answers on **one endpoint**: `http://localhost:4566`.
Region can be anything. Credentials can be any non-empty value (`test` / `test`).
The AWS SDK, CLI, Terraform, and CDK all keep working — you only redirect the endpoint.

```bash
export AWS_ENDPOINT_URL=http://localhost:4566
export AWS_DEFAULT_REGION=us-east-1
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
```

## Prerequisites

| Requirement | Notes |
|---|---|
| Docker Engine / Docker Desktop | Mandatory. Floci itself is a container |
| Docker socket mounted | `-v /var/run/docker.sock:/var/run/docker.sock` — required for Lambda, RDS, ECS, EC2, EKS, ElastiCache (they spawn real containers) |
| `floci` CLI (optional) | `floci start` + `eval $(floci env)`; Compose works without it |
| AWS CLI v2 | To drive services from the terminal |
| `boto3` | Backend integration |
| `testcontainers-floci` (PyPI) | Isolated Floci instance per test run |

## Two modes of use

**1. Long-running dev instance (Docker Compose)** — shared, state persists across restarts.
**2. Ephemeral per-test instance (Testcontainers)** — isolated, no shared state, no port conflicts.

Both will be used: Compose for local development, Testcontainers for the integration test suite.

## Compose sketch

```yaml
services:
  floci:
    image: floci/floci:latest
    ports:
      - "4566:4566"
    environment:
      - FLOCI_HOSTNAME=floci        # so returned URLs resolve from other containers
      - FLOCI_STORAGE_MODE=hybrid   # in-memory speed, flushed every 5s
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    user: root

  backend:
    environment:
      - AWS_ENDPOINT_URL=http://floci:4566
    depends_on:
      - floci
```

> `FLOCI_HOSTNAME` matters: without it Floci hands back `localhost` URLs (e.g. SQS `QueueUrl`),
> which point at the wrong container when the backend runs in Compose.

## Storage modes

| Mode | Behavior | Use for |
|---|---|---|
| `memory` (default) | RAM only, lost on stop | CI / tests |
| `hybrid` | RAM + async flush every 5s | **local development** |
| `persistent` | Flushed on every write | State preservation |
| `wal` | Write-ahead log | Maximum durability |

## Candidate services for this app

Not committed to — these are the ones that plausibly fit a tournament app. Each gets justified
against a real requirement before adoption.

| Service | Plausible use here | Floci fidelity |
|---|---|---|
| S3 | Team logos, player photos, bracket exports | In-process, incl. pre-signed URLs |
| RDS PostgreSQL | The main database, AWS-shaped | **Real Docker** (`postgres:16-alpine`) |
| Cognito | Auth instead of hand-rolled JWT | In-process |
| SQS | Match-result processing queue | In-process, FIFO + DLQ |
| SNS / SES | Notify teams of fixtures | In-process |
| EventBridge Scheduler | Trigger match start / auto-forfeit | In-process |
| Lambda | Standings recalculation, thumbnails | **Real Docker** |
| API Gateway | Front the backend, practice the real topology | REST + HTTP API |
| DynamoDB | Live scoreboard / write-heavy events | In-process, incl. Streams |
| CloudFormation / Terraform | Practice IaC against the emulator | Standard AWS provider |
| ECS / ECR | Practice containerized deploy | **Real Docker** |

## Python integration

```python
import boto3

s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:4566",
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test",
)
```

In application code the endpoint must come from settings (Pydantic `BaseSettings`), unset in
real AWS so boto3 falls back to the genuine endpoints. Same code, both targets.

## Multi-account isolation

If `AWS_ACCESS_KEY_ID` is exactly 12 digits, Floci treats it as the account ID and isolates
resources per account. Anything else falls back to `000000000000`. Useful for practicing
cross-account assume-role patterns.

## Open questions

1. RDS-via-Floci for the main DB, or plain Postgres in Compose? (fidelity vs. speed)
2. Cognito, or the JWT auth from `00-tech-stack.md`?
3. Is IaC (Terraform / CDK) part of the practice goal, or just the SDK?

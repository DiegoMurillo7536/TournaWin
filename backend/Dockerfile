# Multi-stage build. One image, two entrypoints (API and Lambda) per ADR 001.
FROM python:3.12-slim AS base
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1
WORKDIR /app

# Dependencies first: this layer is cached until the lockfile changes.
FROM base AS deps
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

FROM base AS api
COPY --from=deps /app/.venv /app/.venv
# The project is a src-layout package that dependency installation skips
# (--no-install-project), so src/ has to be on the import path explicitly.
# Mirrors `pythonpath = ["src"]` in pyproject.toml, which is how pytest resolves it.
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app/src"
COPY src/ src/
COPY alembic/ alembic/
COPY alembic.ini pyproject.toml ./
EXPOSE 8000
CMD ["uvicorn", "tournament.main:app", "--host", "0.0.0.0", "--port", "8000"]

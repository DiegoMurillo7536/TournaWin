.PHONY: help up down logs backend-install backend-test backend-lint backend-typecheck \
        frontend-install frontend-test gen-api migrate check

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

up:  ## Start floci + postgres + backend + frontend
	docker compose up -d --build

down:  ## Stop everything
	docker compose down

logs:  ## Tail all service logs
	docker compose logs -f

backend-install:  ## Install backend dependencies
	cd backend && uv sync

backend-test:  ## Run backend unit tests
	cd backend && uv run pytest

backend-lint:  ## Lint and format-check the backend
	cd backend && uv run ruff format --check . && uv run ruff check .

backend-typecheck:  ## Type-check the backend
	cd backend && uv run mypy src tests

frontend-install:  ## Install frontend dependencies
	cd frontend && pnpm install

frontend-test:  ## Run frontend unit tests
	cd frontend && pnpm test

gen-api:  ## Regenerate TS types from the backend OpenAPI schema
	cd frontend && pnpm gen:api

migrate:  ## Apply database migrations
	cd backend && uv run alembic upgrade head

check: backend-lint backend-typecheck backend-test  ## Run every backend gate

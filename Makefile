.PHONY: help up down logs build test-api test-web lint format migrate seed clean

# Default target
help:
	@echo "Project K - AI Gamification Platform"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Docker:"
	@echo "  up          Start all services"
	@echo "  up-build    Start all services with rebuild"
	@echo "  down        Stop all services"
	@echo "  logs        View logs (all services)"
	@echo "  logs-api    View API logs"
	@echo "  logs-web    View Web logs"
	@echo "  logs-db     View Database logs"
	@echo "  build       Build all images"
	@echo "  clean       Remove all containers, volumes, and images"
	@echo ""
	@echo "Development:"
	@echo "  shell-api   Open shell in API container"
	@echo "  shell-db    Open psql in database container"
	@echo ""
	@echo "Database:"
	@echo "  migrate     Run database migrations"
	@echo "  migrate-new Create new migration (usage: make migrate-new MSG='migration name')"
	@echo "  seed        Seed database with sample data"
	@echo ""
	@echo "Testing:"
	@echo "  test-api    Run API tests"
	@echo "  test-web    Run Web tests"
	@echo "  test        Run all tests"
	@echo ""
	@echo "Code Quality:"
	@echo "  lint        Run linters"
	@echo "  lint-api    Run API linter (ruff)"
	@echo "  lint-web    Run Web linter (eslint)"
	@echo "  format      Format code"
	@echo "  format-api  Format API code"
	@echo "  format-web  Format Web code"

# =============================================================================
# Docker
# =============================================================================

up:
	docker compose up -d

up-build:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f

logs-api:
	docker compose logs -f api

logs-web:
	docker compose logs -f web

logs-db:
	docker compose logs -f db

build:
	docker compose build

clean:
	docker compose down -v --rmi all --remove-orphans

# =============================================================================
# Development Shells
# =============================================================================

shell-api:
	docker compose exec api bash

shell-db:
	docker compose exec db psql -U postgres -d project_k

# =============================================================================
# Database
# =============================================================================

migrate:
	docker compose exec api alembic upgrade head

migrate-new:
	docker compose exec api alembic revision --autogenerate -m "$(MSG)"

seed:
	docker compose exec api python -m scripts.seed

# =============================================================================
# Testing
# =============================================================================

test-api:
	docker compose exec api pytest -v

test-web:
	docker compose exec web npm test

test: test-api test-web

# =============================================================================
# Code Quality
# =============================================================================

lint-api:
	docker compose exec api ruff check .

lint-web:
	docker compose exec web npm run lint

lint: lint-api lint-web

format-api:
	docker compose exec api ruff format .

format-web:
	docker compose exec web npm run format

format: format-api format-web

# =============================================================================
# Local Development (without Docker)
# =============================================================================

.PHONY: dev-api dev-web install-api install-web

install-api:
	cd apps/api && pip install -r requirements.txt -r requirements-dev.txt

install-web:
	cd apps/web && npm install

dev-api:
	cd apps/api && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-web:
	cd apps/web && npm run dev

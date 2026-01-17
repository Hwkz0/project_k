# Project K - PowerShell Helper Scripts for Windows
# Usage: .\scripts.ps1 <command>

param(
    [Parameter(Position=0)]
    [string]$Command
)

function Show-Help {
    Write-Host "Project K - PowerShell Helper Scripts" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage: .\scripts.ps1 <command>" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Commands:"
    Write-Host "  up          Start all services"
    Write-Host "  up-build    Start all services with rebuild"
    Write-Host "  down        Stop all services"
    Write-Host "  logs        View all logs"
    Write-Host "  logs-api    View API logs"
    Write-Host "  logs-web    View Web logs"
    Write-Host "  seed        Seed database with demo data"
    Write-Host "  migrate     Run database migrations"
    Write-Host "  test-api    Run API tests"
    Write-Host "  lint-api    Run API linter"
    Write-Host "  shell-api   Open shell in API container"
    Write-Host "  shell-db    Open psql in database container"
    Write-Host ""
}

switch ($Command) {
    "up" {
        docker compose up -d
    }
    "up-build" {
        docker compose up -d --build
    }
    "down" {
        docker compose down
    }
    "logs" {
        docker compose logs -f
    }
    "logs-api" {
        docker compose logs -f api
    }
    "logs-web" {
        docker compose logs -f web
    }
    "seed" {
        docker compose exec api python -m scripts.seed
    }
    "migrate" {
        docker compose exec api alembic upgrade head
    }
    "test-api" {
        docker compose exec api pytest -v
    }
    "lint-api" {
        docker compose exec api ruff check .
    }
    "shell-api" {
        docker compose exec api bash
    }
    "shell-db" {
        docker compose exec db psql -U postgres -d project_k
    }
    default {
        Show-Help
    }
}

# 🎮 Project K - AI App Gamification Platform

A production-ready monorepo for gamifying the building of AI-powered applications. 

## 🚀 Local Dev in 3 Commands

```bash
# 1. Clone and setup
cp .env.example .env

# 2. Start everything
docker compose up --build

# 3. Seed demo data (in another terminal)
make seed
```

**That's it!** 
- 🌐 Frontend: http://localhost:5173
- 🔧 API: http://localhost:8000
- 📚 API Docs: http://localhost:8000/docs

## 📁 Project Structure

```
project_k/
├── apps/
│   ├── api/                 # FastAPI backend
│   │   ├── app/
│   │   │   ├── api/v1/      # Versioned API routes
│   │   │   ├── core/        # Config, security, deps
│   │   │   ├── models/      # SQLAlchemy models
│   │   │   ├── schemas/     # Pydantic schemas
│   │   │   ├── services/    # Business logic
│   │   │   ├── jobs/        # Background tasks
│   │   │   └── integrations/# AI provider integrations
│   │   ├── migrations/      # Alembic migrations
│   │   └── tests/
│   └── web/                 # React + Vite frontend
│       └── src/
│           ├── components/
│           ├── pages/
│           ├── api/
│           ├── hooks/
│           └── store/
├── packages/
│   └── shared/              # Shared TypeScript types
├── docker-compose.yml
├── Makefile
└── .github/workflows/
```

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | FastAPI, SQLAlchemy, Alembic, PostgreSQL |
| Frontend | React 18, TypeScript, Vite, Tailwind CSS |
| Auth | JWT (email/password) + OAuth placeholder |
| State | React Query + Zustand |
| Queue | FastAPI BackgroundTasks (Celery-ready) |
| DevOps | Docker, docker-compose, GitHub Actions |

## 📋 Core Features

- **Users & Teams** - User management with team/organization support
- **Projects** - Track AI applications being built
- **Quests & Challenges** - Tasks that award XP upon completion
- **Gamification** - XP, levels, badges, achievements system
- **Leaderboards** - Global, team, and project rankings
- **Activity Feed** - Real-time events and notifications
- **AI Integrations** - Pluggable AI provider interface

## 🔧 Development

### Prerequisites
- Docker & Docker Compose
- Node.js 20+ (for local frontend dev)
- Python 3.11+ (for local backend dev)

### Common Commands

```bash
# Start all services
make up

# Stop all services
make down

# View logs
make logs

# Run backend tests
make test-api

# Run linting
make lint

# Create new migration
make migration name="add_new_table"

# Apply migrations
make migrate

# Seed database
make seed

# Format code
make format
```

### Local Development (without Docker)

```bash
# Backend
cd apps/api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd apps/web
npm install
npm run dev
```

## 🚢 Deployment

### Render / Railway / Fly.io

1. Connect your repository
2. Set environment variables from `.env.example`
3. Deploy `apps/api` with Dockerfile
4. Deploy `apps/web` with Dockerfile
5. Add PostgreSQL addon

### Docker Registry Deploy

```bash
# Build and push images
docker build -t your-registry/project-k-api:latest ./apps/api
docker build -t your-registry/project-k-web:latest ./apps/web
docker push your-registry/project-k-api:latest
docker push your-registry/project-k-web:latest
```

### Environment Variables

See `.env.example` for all required variables.

## 📚 API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🧪 Testing

```bash
# Run all backend tests
make test-api

# Run with coverage
cd apps/api && pytest --cov=app tests/

# Run frontend tests
cd apps/web && npm test
```

## 📄 License

MIT License - see LICENSE file for details.
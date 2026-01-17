"""API v1 router combining all endpoint routers."""

from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    users,
    teams,
    projects,
    quests,
    leaderboards,
    activity,
    badges,
    achievements,
    integrations,
)

api_router = APIRouter()

# Authentication
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# Users
api_router.include_router(users.router, prefix="/users", tags=["users"])

# Teams
api_router.include_router(teams.router, prefix="/teams", tags=["teams"])

# Projects
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])

# Quests
api_router.include_router(quests.router, prefix="/quests", tags=["quests"])

# Leaderboards
api_router.include_router(leaderboards.router, prefix="/leaderboards", tags=["leaderboards"])

# Activity Feed
api_router.include_router(activity.router, prefix="/activity", tags=["activity"])

# Badges
api_router.include_router(badges.router, prefix="/badges", tags=["badges"])

# Achievements
api_router.include_router(achievements.router, prefix="/achievements", tags=["achievements"])

# AI Integrations
api_router.include_router(integrations.router, prefix="/integrations", tags=["integrations"])

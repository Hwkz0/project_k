"""Leaderboard endpoints."""

from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.leaderboard import LeaderboardType
from app.schemas.leaderboard import LeaderboardResponse, LeaderboardEntryRead
from app.services.leaderboard_service import LeaderboardService

router = APIRouter()


@router.get("/global", response_model=LeaderboardResponse)
def get_global_leaderboard(
    limit: int = Query(default=10, le=100),
    db: Session = Depends(get_db),
):
    """Get global leaderboard."""
    leaderboard_service = LeaderboardService(db)
    entries = leaderboard_service.get_global_leaderboard(limit=limit)
    
    return LeaderboardResponse(
        leaderboard_type=LeaderboardType.GLOBAL,
        entries=entries,
        total_count=len(entries),
    )


@router.get("/weekly", response_model=LeaderboardResponse)
def get_weekly_leaderboard(
    limit: int = Query(default=10, le=100),
    db: Session = Depends(get_db),
):
    """Get weekly leaderboard."""
    leaderboard_service = LeaderboardService(db)
    entries, period_key = leaderboard_service.get_weekly_leaderboard(limit=limit)
    
    return LeaderboardResponse(
        leaderboard_type=LeaderboardType.WEEKLY,
        period_key=period_key,
        entries=entries,
        total_count=len(entries),
    )


@router.get("/monthly", response_model=LeaderboardResponse)
def get_monthly_leaderboard(
    limit: int = Query(default=10, le=100),
    db: Session = Depends(get_db),
):
    """Get monthly leaderboard."""
    leaderboard_service = LeaderboardService(db)
    entries, period_key = leaderboard_service.get_monthly_leaderboard(limit=limit)
    
    return LeaderboardResponse(
        leaderboard_type=LeaderboardType.MONTHLY,
        period_key=period_key,
        entries=entries,
        total_count=len(entries),
    )


@router.get("/team/{team_id}", response_model=LeaderboardResponse)
def get_team_leaderboard(
    team_id: int,
    limit: int = Query(default=10, le=100),
    db: Session = Depends(get_db),
):
    """Get leaderboard for a specific team."""
    leaderboard_service = LeaderboardService(db)
    entries = leaderboard_service.get_team_leaderboard(team_id=team_id, limit=limit)
    
    return LeaderboardResponse(
        leaderboard_type=LeaderboardType.TEAM,
        scope_id=team_id,
        entries=entries,
        total_count=len(entries),
    )


@router.get("/project/{project_id}", response_model=LeaderboardResponse)
def get_project_leaderboard(
    project_id: int,
    limit: int = Query(default=10, le=100),
    db: Session = Depends(get_db),
):
    """Get leaderboard for a specific project (based on quest completions)."""
    leaderboard_service = LeaderboardService(db)
    entries = leaderboard_service.get_project_leaderboard(project_id=project_id, limit=limit)
    
    return LeaderboardResponse(
        leaderboard_type=LeaderboardType.PROJECT,
        scope_id=project_id,
        entries=entries,
        total_count=len(entries),
    )

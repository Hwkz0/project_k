"""Achievement endpoints."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.gamification import AchievementRead
from app.services.gamification_service import GamificationService

router = APIRouter()


@router.get("/", response_model=List[AchievementRead])
def list_achievements(
    include_secret: bool = False,
    db: Session = Depends(get_db),
):
    """List all achievements (optionally include secret ones)."""
    gamification_service = GamificationService(db)
    achievements = gamification_service.get_all_achievements()
    
    if not include_secret:
        achievements = [a for a in achievements if not a.is_secret]
    
    return achievements


@router.get("/{achievement_id}", response_model=AchievementRead)
def get_achievement(
    achievement_id: int,
    db: Session = Depends(get_db),
):
    """Get an achievement by ID."""
    gamification_service = GamificationService(db)
    achievement = gamification_service.get_achievement_by_id(achievement_id)
    
    if not achievement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Achievement not found",
        )
    
    return achievement

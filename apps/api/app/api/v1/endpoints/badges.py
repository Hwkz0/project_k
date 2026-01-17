"""Badge endpoints."""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.gamification import BadgeRead
from app.services.gamification_service import GamificationService

router = APIRouter()


@router.get("/", response_model=List[BadgeRead])
def list_badges(
    db: Session = Depends(get_db),
):
    """List all available badges."""
    gamification_service = GamificationService(db)
    return gamification_service.get_all_badges()


@router.get("/{badge_id}", response_model=BadgeRead)
def get_badge(
    badge_id: int,
    db: Session = Depends(get_db),
):
    """Get a badge by ID."""
    from fastapi import HTTPException, status
    
    gamification_service = GamificationService(db)
    badge = gamification_service.get_badge_by_id(badge_id)
    
    if not badge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Badge not found",
        )
    
    return badge

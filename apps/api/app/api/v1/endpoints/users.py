"""User endpoints."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.models.user import User
from app.schemas.user import UserRead, UserUpdate, UserPublic
from app.schemas.gamification import UserBadgeRead, UserAchievementRead
from app.services.user_service import UserService
from app.services.gamification_service import GamificationService

router = APIRouter()


@router.get("/me", response_model=UserRead)
def get_current_user_info(
    current_user: User = Depends(get_current_active_user),
):
    """Get current user profile."""
    return current_user


@router.put("/me", response_model=UserRead)
def update_current_user(
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Update current user profile."""
    user_service = UserService(db)
    return user_service.update(current_user, user_in)


@router.get("/me/badges", response_model=List[UserBadgeRead])
def get_current_user_badges(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get current user's badges."""
    gamification_service = GamificationService(db)
    return gamification_service.get_user_badges(current_user.id)


@router.get("/me/achievements", response_model=List[UserAchievementRead])
def get_current_user_achievements(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get current user's achievements."""
    gamification_service = GamificationService(db)
    return gamification_service.get_user_achievements(current_user.id)


@router.get("/{user_id}", response_model=UserPublic)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    """Get a user's public profile."""
    user_service = UserService(db)
    user = user_service.get_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    return user


@router.get("/{user_id}/badges", response_model=List[UserBadgeRead])
def get_user_badges(
    user_id: int,
    db: Session = Depends(get_db),
):
    """Get a user's badges."""
    user_service = UserService(db)
    user = user_service.get_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    gamification_service = GamificationService(db)
    return gamification_service.get_user_badges(user_id)


@router.get("/{user_id}/achievements", response_model=List[UserAchievementRead])
def get_user_achievements(
    user_id: int,
    db: Session = Depends(get_db),
):
    """Get a user's achievements."""
    user_service = UserService(db)
    user = user_service.get_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    gamification_service = GamificationService(db)
    return gamification_service.get_user_achievements(user_id)

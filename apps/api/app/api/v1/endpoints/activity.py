"""Activity feed endpoints."""

from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_active_user, get_optional_user
from app.models.user import User
from app.schemas.activity import ActivityFeedResponse
from app.services.activity_service import ActivityService

router = APIRouter()


@router.get("/", response_model=ActivityFeedResponse)
def get_activity_feed(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, le=100),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user),
):
    """Get public activity feed."""
    activity_service = ActivityService(db)
    items, total = activity_service.get_feed(
        page=page,
        per_page=per_page,
        public_only=current_user is None,
    )
    
    return ActivityFeedResponse(
        items=items,
        total=total,
        page=page,
        per_page=per_page,
        has_more=(page * per_page) < total,
    )


@router.get("/my-activity", response_model=ActivityFeedResponse)
def get_my_activity(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get current user's activity."""
    activity_service = ActivityService(db)
    items, total = activity_service.get_user_activity(
        user_id=current_user.id,
        page=page,
        per_page=per_page,
    )
    
    return ActivityFeedResponse(
        items=items,
        total=total,
        page=page,
        per_page=per_page,
        has_more=(page * per_page) < total,
    )


@router.get("/user/{user_id}", response_model=ActivityFeedResponse)
def get_user_activity(
    user_id: int,
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, le=100),
    db: Session = Depends(get_db),
):
    """Get a user's public activity."""
    activity_service = ActivityService(db)
    items, total = activity_service.get_user_activity(
        user_id=user_id,
        page=page,
        per_page=per_page,
        public_only=True,
    )
    
    return ActivityFeedResponse(
        items=items,
        total=total,
        page=page,
        per_page=per_page,
        has_more=(page * per_page) < total,
    )


@router.get("/team/{team_id}", response_model=ActivityFeedResponse)
def get_team_activity(
    team_id: int,
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, le=100),
    db: Session = Depends(get_db),
):
    """Get activity for a team."""
    activity_service = ActivityService(db)
    items, total = activity_service.get_team_activity(
        team_id=team_id,
        page=page,
        per_page=per_page,
    )
    
    return ActivityFeedResponse(
        items=items,
        total=total,
        page=page,
        per_page=per_page,
        has_more=(page * per_page) < total,
    )


@router.get("/project/{project_id}", response_model=ActivityFeedResponse)
def get_project_activity(
    project_id: int,
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, le=100),
    db: Session = Depends(get_db),
):
    """Get activity for a project."""
    activity_service = ActivityService(db)
    items, total = activity_service.get_project_activity(
        project_id=project_id,
        page=page,
        per_page=per_page,
    )
    
    return ActivityFeedResponse(
        items=items,
        total=total,
        page=page,
        per_page=per_page,
        has_more=(page * per_page) < total,
    )

"""Activity feed schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.activity import ActivityType


class ActivityEventBase(BaseModel):
    """Base activity event schema."""

    event_type: ActivityType
    title: str
    description: Optional[str] = None


class ActivityEventCreate(ActivityEventBase):
    """Schema for creating an activity event."""

    user_id: int
    project_id: Optional[int] = None
    team_id: Optional[int] = None
    quest_id: Optional[int] = None
    badge_id: Optional[int] = None
    achievement_id: Optional[int] = None
    metadata: Optional[str] = None
    xp_amount: int = 0
    is_public: bool = True


class ActivityEventRead(ActivityEventBase):
    """Schema for reading an activity event."""

    id: int
    user_id: int
    username: str
    user_avatar_url: Optional[str] = None
    project_id: Optional[int] = None
    team_id: Optional[int] = None
    quest_id: Optional[int] = None
    badge_id: Optional[int] = None
    achievement_id: Optional[int] = None
    xp_amount: int
    is_public: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ActivityFeedResponse(BaseModel):
    """Activity feed response with pagination."""

    items: list[ActivityEventRead]
    total: int
    page: int
    per_page: int
    has_more: bool

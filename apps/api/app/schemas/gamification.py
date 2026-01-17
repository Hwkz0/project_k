"""Gamification schemas for badges and achievements."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.gamification import BadgeCategory, AchievementCategory


class BadgeBase(BaseModel):
    """Base badge schema."""

    name: str
    description: str
    icon: str
    category: BadgeCategory


class BadgeCreate(BadgeBase):
    """Schema for creating a badge."""

    requirement_type: str
    requirement_value: int
    xp_bonus: int = 0


class BadgeRead(BadgeBase):
    """Schema for reading a badge."""

    id: int
    requirement_type: str
    requirement_value: int
    xp_bonus: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserBadgeRead(BaseModel):
    """Schema for reading a user's badge."""

    id: int
    badge: BadgeRead
    earned_at: datetime

    class Config:
        from_attributes = True


class AchievementBase(BaseModel):
    """Base achievement schema."""

    name: str
    description: str
    icon: str
    category: AchievementCategory


class AchievementCreate(AchievementBase):
    """Schema for creating an achievement."""

    points: int = 10
    xp_reward: int = 50
    rarity_score: int = 100
    is_secret: bool = False


class AchievementRead(AchievementBase):
    """Schema for reading an achievement."""

    id: int
    points: int
    xp_reward: int
    rarity_score: int
    is_secret: bool
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserAchievementRead(BaseModel):
    """Schema for reading a user's achievement."""

    id: int
    achievement: AchievementRead
    progress: int
    target: int
    is_completed: bool
    completed_at: Optional[datetime] = None
    started_at: datetime

    class Config:
        from_attributes = True

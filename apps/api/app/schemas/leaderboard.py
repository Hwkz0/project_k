from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.leaderboard import LeaderboardType


class LeaderboardEntryRead(BaseModel):
    """Schema for reading a leaderboard entry."""

    rank: int
    user_id: int
    username: str
    avatar_url: Optional[str] = None
    xp: int
    level: int
    computed_at: datetime

    class Config:
        from_attributes = True


class LeaderboardResponse(BaseModel):
    """Schema for leaderboard response."""

    leaderboard_type: LeaderboardType
    scope_id: Optional[int] = None
    period_key: Optional[str] = None
    entries: list[LeaderboardEntryRead]
    total_count: int
from datetime import datetime
from enum import Enum

from sqlalchemy import Column, DateTime, Enum as SQLEnum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class LeaderboardType(str, Enum):
    GLOBAL = "global"
    TEAM = "team"
    PROJECT = "project"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class LeaderboardEntry(Base):
    """Leaderboard entry (cached/computed)."""

    __tablename__ = "leaderboard_entries"

    id = Column(Integer, primary_key=True, index=True)
    leaderboard_type = Column(SQLEnum(LeaderboardType), nullable=False)

    # Scope (for team/project leaderboards)
    scope_id = Column(Integer, nullable=True)  # team_id or project_id

    # User ranking
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rank = Column(Integer, nullable=False)
    xp = Column(Integer, nullable=False)
    level = Column(Integer, nullable=False)

    # Period (for time-based leaderboards)
    period_key = Column(String(20), nullable=True)  # e.g., "2024-W01", "2024-01"

    # Timestamps
    computed_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User")
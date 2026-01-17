"""Activity feed models."""

from datetime import datetime
from enum import Enum

from sqlalchemy import Column, DateTime, Enum as SQLEnum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class ActivityType(str, Enum):
    """Activity event types."""
    # User events
    USER_REGISTERED = "user_registered"
    USER_LEVEL_UP = "user_level_up"
    
    # Quest events
    QUEST_COMPLETED = "quest_completed"
    QUEST_CREATED = "quest_created"
    
    # Project events
    PROJECT_CREATED = "project_created"
    PROJECT_PUBLISHED = "project_published"
    PROJECT_UPDATED = "project_updated"
    
    # Team events
    TEAM_CREATED = "team_created"
    TEAM_JOINED = "team_joined"
    
    # Gamification events
    BADGE_EARNED = "badge_earned"
    ACHIEVEMENT_UNLOCKED = "achievement_unlocked"
    XP_GAINED = "xp_gained"
    
    # Leaderboard events
    LEADERBOARD_RANK_UP = "leaderboard_rank_up"


class ActivityEvent(Base):
    """Activity event model for the activity feed."""

    __tablename__ = "activity_events"

    id = Column(Integer, primary_key=True, index=True)
    
    # Event type
    event_type = Column(SQLEnum(ActivityType), nullable=False, index=True)
    
    # Actor (user who performed the action)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Related entities (optional, depending on event type)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)
    quest_id = Column(Integer, ForeignKey("quests.id"), nullable=True)
    badge_id = Column(Integer, ForeignKey("badges.id"), nullable=True)
    achievement_id = Column(Integer, ForeignKey("achievements.id"), nullable=True)
    
    # Event data (JSON-like string for additional context)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    extra_data = Column(Text, nullable=True)  # JSON string for extra data
    
    # XP associated with this event (if any)
    xp_amount = Column(Integer, default=0, nullable=False)
    
    # Visibility
    is_public = Column(Integer, default=True, nullable=False)  # Visible to all users
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Relationships
    user = relationship("User", back_populates="activities")

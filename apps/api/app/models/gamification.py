"""Gamification models: Badges and Achievements."""

from datetime import datetime
from enum import Enum

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class BadgeCategory(str, Enum):
    """Badge category types."""
    ACHIEVEMENT = "achievement"
    MILESTONE = "milestone"
    SKILL = "skill"
    SPECIAL = "special"


class Badge(Base):
    """Badge model - visual rewards for accomplishments."""

    __tablename__ = "badges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    icon = Column(String(100), nullable=False)  # Icon identifier or URL
    category = Column(SQLEnum(BadgeCategory), default=BadgeCategory.ACHIEVEMENT, nullable=False)
    
    # Requirements (stored as JSON-like string, or could use JSONB for Postgres)
    requirement_type = Column(String(50), nullable=False)  # e.g., "quest_count", "xp_total", "level"
    requirement_value = Column(Integer, nullable=False)  # e.g., 10, 1000, 5
    
    # XP bonus for earning this badge
    xp_bonus = Column(Integer, default=0, nullable=False)
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user_badges = relationship("UserBadge", back_populates="badge")


class UserBadge(Base):
    """User badge association - badges earned by users."""

    __tablename__ = "user_badges"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    badge_id = Column(Integer, ForeignKey("badges.id"), nullable=False)
    
    # When the badge was earned
    earned_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="badges")
    badge = relationship("Badge", back_populates="user_badges")


class AchievementCategory(str, Enum):
    """Achievement category types."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"
    LEGENDARY = "legendary"


class Achievement(Base):
    """Achievement model - major milestones and accomplishments."""

    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    icon = Column(String(100), nullable=False)
    category = Column(SQLEnum(AchievementCategory), default=AchievementCategory.BEGINNER, nullable=False)
    
    # Point value for this achievement
    points = Column(Integer, default=10, nullable=False)
    
    # XP reward for unlocking
    xp_reward = Column(Integer, default=50, nullable=False)
    
    # Rarity (percentage of users who have this)
    rarity_score = Column(Integer, default=100, nullable=False)  # 100 = common, 1 = very rare
    
    # Secret achievement (hidden until unlocked)
    is_secret = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user_achievements = relationship("UserAchievement", back_populates="achievement")


class UserAchievement(Base):
    """User achievement association - achievements unlocked by users."""

    __tablename__ = "user_achievements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    achievement_id = Column(Integer, ForeignKey("achievements.id"), nullable=False)
    
    # Progress tracking (for achievements that require multiple steps)
    progress = Column(Integer, default=0, nullable=False)
    target = Column(Integer, default=1, nullable=False)
    
    # Completion
    is_completed = Column(Boolean, default=False, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    
    # Timestamps
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="achievements")
    achievement = relationship("Achievement", back_populates="user_achievements")

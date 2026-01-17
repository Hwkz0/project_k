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


class QuestDifficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"


class QuestCategory(str, Enum):
    SETUP = "setup"
    DEVELOPMENT = "development"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    DOCUMENTATION = "documentation"
    COMMUNITY = "community"


class Quest(Base):
    """Quest/Challenge model."""

    __tablename__ = "quests"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    difficulty = Column(SQLEnum(QuestDifficulty), default=QuestDifficulty.EASY, nullable=False)
    category = Column(SQLEnum(QuestCategory), default=QuestCategory. DEVELOPMENT, nullable=False)

    # Rewards
    xp_reward = Column(Integer, default=10, nullable=False)

    # Project association (optional - can be global quests)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)

    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    is_repeatable = Column(Boolean, default=False, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime. utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    project = relationship("Project", back_populates="quests")
    completions = relationship("QuestCompletion", back_populates="quest")


class QuestCompletion(Base):
    """Quest completion tracking."""

    __tablename__ = "quest_completions"

    id = Column(Integer, primary_key=True, index=True)
    quest_id = Column(Integer, ForeignKey("quests.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Completion details
    completed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    xp_earned = Column(Integer, nullable=False)

    # Relationships
    quest = relationship("Quest", back_populates="completions")
    user = relationship("User", back_populates="quest_completions")
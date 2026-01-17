from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    """User model."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=True)
    avatar_url = Column(Text, nullable=True)
    bio = Column(Text, nullable=True)

    # Gamification
    xp = Column(Integer, default=0, nullable=False)
    level = Column(Integer, default=1, nullable=False)

    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime. utcnow, nullable=False)

    # Relationships
    team_memberships = relationship("TeamMember", back_populates="user")
    projects = relationship("Project", back_populates="owner")
    quest_completions = relationship("QuestCompletion", back_populates="user")
    badges = relationship("UserBadge", back_populates="user")
    achievements = relationship("UserAchievement", back_populates="user")
    activities = relationship("ActivityEvent", back_populates="user")
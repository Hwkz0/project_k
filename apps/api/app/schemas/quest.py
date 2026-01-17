from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models. quest import QuestDifficulty, QuestCategory


class QuestBase(BaseModel):
    """Base quest schema."""

    title: str
    description: str
    difficulty: QuestDifficulty = QuestDifficulty. EASY
    category: QuestCategory = QuestCategory.DEVELOPMENT


class QuestCreate(QuestBase):
    """Schema for creating a quest."""

    xp_reward: int = 10
    project_id:  Optional[int] = None
    is_repeatable: bool = False


class QuestUpdate(BaseModel):
    """Schema for updating a quest."""

    title: Optional[str] = None
    description:  Optional[str] = None
    difficulty: Optional[QuestDifficulty] = None
    category: Optional[QuestCategory] = None
    xp_reward:  Optional[int] = None
    is_active: Optional[bool] = None


class QuestRead(QuestBase):
    """Schema for reading a quest."""

    id: int
    xp_reward: int
    project_id: Optional[int] = None
    is_active: bool
    is_repeatable: bool
    created_at: datetime

    class Config:
        from_attributes = True


class QuestCompletionRead(BaseModel):
    """Schema for reading a quest completion."""

    id: int
    quest_id:  int
    user_id: int
    completed_at: datetime
    xp_earned: int

    class Config:
        from_attributes = True
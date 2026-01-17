from typing import List, Optional

from sqlalchemy.orm import Session

from app.models. quest import Quest, QuestCompletion
from app.models.user import User
from app.schemas.quest import QuestCreate, QuestUpdate


class QuestService:
    """Service for quest operations."""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, quest_id: int) -> Optional[Quest]:
        """Get quest by ID."""
        return self.db.query(Quest).filter(Quest.id == quest_id).first()

    def get_all(self, skip: int = 0, limit: int = 20, active_only: bool = True) -> List[Quest]:
        """Get all quests with pagination."""
        query = self.db.query(Quest)
        if active_only:
            query = query.filter(Quest.is_active == True)
        return query.offset(skip).limit(limit).all()

    def get_by_project(self, project_id: int) -> List[Quest]:
        """Get quests for a project."""
        return self.db.query(Quest).filter(Quest.project_id == project_id).all()

    def get_global_quests(self) -> List[Quest]:
        """Get global quests (not tied to a project)."""
        return (
            self.db.query(Quest)
            .filter(Quest.project_id == None, Quest.is_active == True)
            .all()
        )

    def create(self, quest_in: QuestCreate) -> Quest:
        """Create a new quest."""
        quest = Quest(**quest_in.model_dump())
        self.db.add(quest)
        self.db.commit()
        self.db.refresh(quest)
        return quest

    def update(self, quest: Quest, quest_in: QuestUpdate) -> Quest:
        """Update a quest."""
        update_data = quest_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(quest, field, value)
        self.db.commit()
        self.db.refresh(quest)
        return quest

    def complete_quest(self, quest: Quest, user: User) -> QuestCompletion:
        """Complete a quest for a user."""
        # Check if already completed (if not repeatable)
        if not quest. is_repeatable:
            existing = (
                self.db.query(QuestCompletion)
                .filter(
                    QuestCompletion. quest_id == quest.id,
                    QuestCompletion. user_id == user.id,
                )
                .first()
            )
            if existing: 
                raise ValueError("Quest already completed")

        completion = QuestCompletion(
            quest_id=quest.id,
            user_id=user.id,
            xp_earned=quest.xp_reward,
        )
        self.db.add(completion)
        self.db.commit()
        self.db.refresh(completion)
        return completion

    def get_user_completions(self, user_id:  int) -> List[QuestCompletion]:
        """Get quest completions for a user."""
        return (
            self.db. query(QuestCompletion)
            .filter(QuestCompletion.user_id == user_id)
            .all()
        )

    def is_completed_by_user(self, quest_id: int, user_id:  int) -> bool:
        """Check if quest is completed by user."""
        return (
            self.db.query(QuestCompletion)
            .filter(
                QuestCompletion. quest_id == quest_id,
                QuestCompletion. user_id == user_id,
            )
            .first()
            is not None
        )
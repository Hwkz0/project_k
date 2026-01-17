"""Service for gamification operations."""

from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.gamification import Badge, UserBadge, Achievement, UserAchievement
from app.models.user import User
from app.models.quest import QuestCompletion


class GamificationService:
    """Service for gamification operations."""

    def __init__(self, db: Session):
        self.db = db

    # Badges
    def get_all_badges(self) -> List[Badge]:
        """Get all active badges."""
        return self.db.query(Badge).filter(Badge.is_active == True).all()

    def get_badge_by_id(self, badge_id: int) -> Optional[Badge]:
        """Get a badge by ID."""
        return self.db.query(Badge).filter(Badge.id == badge_id).first()

    def get_user_badges(self, user_id: int) -> List[UserBadge]:
        """Get badges for a user."""
        return self.db.query(UserBadge).filter(UserBadge.user_id == user_id).all()

    def award_badge(self, user: User, badge: Badge) -> Optional[UserBadge]:
        """Award a badge to a user."""
        # Check if already has badge
        existing = (
            self.db.query(UserBadge)
            .filter(UserBadge.user_id == user.id, UserBadge.badge_id == badge.id)
            .first()
        )
        if existing:
            return None

        user_badge = UserBadge(user_id=user.id, badge_id=badge.id)
        self.db.add(user_badge)
        self.db.commit()
        self.db.refresh(user_badge)
        return user_badge

    def check_and_award_badges(self, user: User) -> List[UserBadge]:
        """Check and award all eligible badges for a user."""
        awarded = []
        badges = self.get_all_badges()
        
        for badge in badges:
            if self._check_badge_requirement(user, badge):
                user_badge = self.award_badge(user, badge)
                if user_badge:
                    awarded.append(user_badge)
        
        return awarded

    def _check_badge_requirement(self, user: User, badge: Badge) -> bool:
        """Check if user meets badge requirements."""
        if badge.requirement_type == "quest_count":
            count = self.db.query(QuestCompletion).filter(
                QuestCompletion.user_id == user.id
            ).count()
            return count >= badge.requirement_value
        
        elif badge.requirement_type == "xp_total":
            return user.xp >= badge.requirement_value
        
        elif badge.requirement_type == "level":
            return user.level >= badge.requirement_value
        
        return False

    # Achievements
    def get_all_achievements(self) -> List[Achievement]:
        """Get all active achievements."""
        return self.db.query(Achievement).filter(Achievement.is_active == True).all()

    def get_achievement_by_id(self, achievement_id: int) -> Optional[Achievement]:
        """Get an achievement by ID."""
        return self.db.query(Achievement).filter(Achievement.id == achievement_id).first()

    def get_user_achievements(self, user_id: int) -> List[UserAchievement]:
        """Get achievements for a user."""
        return (
            self.db.query(UserAchievement)
            .filter(UserAchievement.user_id == user_id)
            .all()
        )

    def award_achievement(self, user: User, achievement: Achievement) -> Optional[UserAchievement]:
        """Award an achievement to a user."""
        existing = (
            self.db.query(UserAchievement)
            .filter(
                UserAchievement.user_id == user.id,
                UserAchievement.achievement_id == achievement.id,
            )
            .first()
        )
        
        if existing and existing.is_completed:
            return None

        if existing:
            # Update progress
            existing.progress = existing.target
            existing.is_completed = True
            existing.completed_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(existing)
            return existing
        
        user_achievement = UserAchievement(
            user_id=user.id,
            achievement_id=achievement.id,
            progress=1,
            target=1,
            is_completed=True,
            completed_at=datetime.utcnow(),
        )
        self.db.add(user_achievement)
        self.db.commit()
        self.db.refresh(user_achievement)
        return user_achievement

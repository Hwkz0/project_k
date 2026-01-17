"""Leaderboard service for ranking calculations."""

from datetime import datetime
from typing import List, Optional, Tuple

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.leaderboard import LeaderboardEntry, LeaderboardType
from app.models.user import User
from app.models.team import TeamMember
from app.models.quest import QuestCompletion
from app.schemas.leaderboard import LeaderboardEntryRead


class LeaderboardService:
    """Service for leaderboard operations."""

    def __init__(self, db: Session):
        self.db = db

    def get_global_leaderboard(self, limit: int = 10) -> List[LeaderboardEntryRead]:
        """Get global leaderboard by XP."""
        users = (
            self.db.query(User)
            .filter(User.is_active == True)
            .order_by(User.xp.desc())
            .limit(limit)
            .all()
        )
        
        return [
            LeaderboardEntryRead(
                rank=idx + 1,
                user_id=user.id,
                username=user.username,
                avatar_url=user.avatar_url,
                xp=user.xp,
                level=user.level,
                computed_at=datetime.utcnow(),
            )
            for idx, user in enumerate(users)
        ]

    def get_weekly_leaderboard(self, limit: int = 10) -> Tuple[List[LeaderboardEntryRead], str]:
        """Get weekly leaderboard by XP earned this week."""
        now = datetime.utcnow()
        week_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        # Go back to Monday
        week_start = week_start.replace(day=week_start.day - week_start.weekday())
        
        period_key = now.strftime("%Y-W%W")
        
        # Sum XP from quest completions this week
        weekly_xp = (
            self.db.query(
                QuestCompletion.user_id,
                func.sum(QuestCompletion.xp_earned).label("weekly_xp"),
            )
            .filter(QuestCompletion.completed_at >= week_start)
            .group_by(QuestCompletion.user_id)
            .order_by(func.sum(QuestCompletion.xp_earned).desc())
            .limit(limit)
            .all()
        )
        
        result = []
        for idx, (user_id, xp) in enumerate(weekly_xp):
            user = self.db.query(User).filter(User.id == user_id).first()
            if user:
                result.append(LeaderboardEntryRead(
                    rank=idx + 1,
                    user_id=user.id,
                    username=user.username,
                    avatar_url=user.avatar_url,
                    xp=int(xp),
                    level=user.level,
                    computed_at=datetime.utcnow(),
                ))
        
        return result, period_key

    def get_monthly_leaderboard(self, limit: int = 10) -> Tuple[List[LeaderboardEntryRead], str]:
        """Get monthly leaderboard by XP earned this month."""
        now = datetime.utcnow()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        period_key = now.strftime("%Y-%m")
        
        # Sum XP from quest completions this month
        monthly_xp = (
            self.db.query(
                QuestCompletion.user_id,
                func.sum(QuestCompletion.xp_earned).label("monthly_xp"),
            )
            .filter(QuestCompletion.completed_at >= month_start)
            .group_by(QuestCompletion.user_id)
            .order_by(func.sum(QuestCompletion.xp_earned).desc())
            .limit(limit)
            .all()
        )
        
        result = []
        for idx, (user_id, xp) in enumerate(monthly_xp):
            user = self.db.query(User).filter(User.id == user_id).first()
            if user:
                result.append(LeaderboardEntryRead(
                    rank=idx + 1,
                    user_id=user.id,
                    username=user.username,
                    avatar_url=user.avatar_url,
                    xp=int(xp),
                    level=user.level,
                    computed_at=datetime.utcnow(),
                ))
        
        return result, period_key

    def get_team_leaderboard(self, team_id: int, limit: int = 10) -> List[LeaderboardEntryRead]:
        """Get leaderboard for a specific team."""
        # Get team member user IDs
        member_ids = [
            m.user_id for m in
            self.db.query(TeamMember).filter(TeamMember.team_id == team_id).all()
        ]
        
        if not member_ids:
            return []
        
        users = (
            self.db.query(User)
            .filter(User.id.in_(member_ids), User.is_active == True)
            .order_by(User.xp.desc())
            .limit(limit)
            .all()
        )
        
        return [
            LeaderboardEntryRead(
                rank=idx + 1,
                user_id=user.id,
                username=user.username,
                avatar_url=user.avatar_url,
                xp=user.xp,
                level=user.level,
                computed_at=datetime.utcnow(),
            )
            for idx, user in enumerate(users)
        ]

    def get_project_leaderboard(self, project_id: int, limit: int = 10) -> List[LeaderboardEntryRead]:
        """Get leaderboard for a specific project based on quest completions."""
        from app.models.quest import Quest
        
        # Get quest IDs for this project
        quest_ids = [
            q.id for q in
            self.db.query(Quest).filter(Quest.project_id == project_id).all()
        ]
        
        if not quest_ids:
            return []
        
        # Sum XP from completions of project quests
        project_xp = (
            self.db.query(
                QuestCompletion.user_id,
                func.sum(QuestCompletion.xp_earned).label("project_xp"),
            )
            .filter(QuestCompletion.quest_id.in_(quest_ids))
            .group_by(QuestCompletion.user_id)
            .order_by(func.sum(QuestCompletion.xp_earned).desc())
            .limit(limit)
            .all()
        )
        
        result = []
        for idx, (user_id, xp) in enumerate(project_xp):
            user = self.db.query(User).filter(User.id == user_id).first()
            if user:
                result.append(LeaderboardEntryRead(
                    rank=idx + 1,
                    user_id=user.id,
                    username=user.username,
                    avatar_url=user.avatar_url,
                    xp=int(xp),
                    level=user.level,
                    computed_at=datetime.utcnow(),
                ))
        
        return result

    def cache_leaderboard(
        self,
        leaderboard_type: LeaderboardType,
        entries: List[LeaderboardEntryRead],
        scope_id: Optional[int] = None,
        period_key: Optional[str] = None,
    ):
        """Cache leaderboard entries in database."""
        # Clear existing entries for this leaderboard
        query = self.db.query(LeaderboardEntry).filter(
            LeaderboardEntry.leaderboard_type == leaderboard_type
        )
        if scope_id:
            query = query.filter(LeaderboardEntry.scope_id == scope_id)
        if period_key:
            query = query.filter(LeaderboardEntry.period_key == period_key)
        
        query.delete()
        
        # Insert new entries
        for entry in entries:
            db_entry = LeaderboardEntry(
                leaderboard_type=leaderboard_type,
                scope_id=scope_id,
                user_id=entry.user_id,
                rank=entry.rank,
                xp=entry.xp,
                level=entry.level,
                period_key=period_key,
            )
            self.db.add(db_entry)
        
        self.db.commit()

"""Activity service for managing activity events."""

from typing import List, Optional, Tuple

from sqlalchemy.orm import Session

from app.models.activity import ActivityEvent, ActivityType
from app.models.user import User
from app.schemas.activity import ActivityEventCreate, ActivityEventRead


class ActivityService:
    """Service for activity feed operations."""

    def __init__(self, db: Session):
        self.db = db

    def create_event(
        self,
        user_id: int,
        event_type: ActivityType,
        title: str,
        description: Optional[str] = None,
        project_id: Optional[int] = None,
        team_id: Optional[int] = None,
        quest_id: Optional[int] = None,
        badge_id: Optional[int] = None,
        achievement_id: Optional[int] = None,
        metadata: Optional[str] = None,
        xp_amount: int = 0,
        is_public: bool = True,
    ) -> ActivityEvent:
        """Create a new activity event."""
        event = ActivityEvent(
            user_id=user_id,
            event_type=event_type,
            title=title,
            description=description,
            project_id=project_id,
            team_id=team_id,
            quest_id=quest_id,
            badge_id=badge_id,
            achievement_id=achievement_id,
            metadata=metadata,
            xp_amount=xp_amount,
            is_public=is_public,
        )
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event

    def get_feed(
        self,
        page: int = 1,
        per_page: int = 20,
        public_only: bool = True,
    ) -> Tuple[List[ActivityEventRead], int]:
        """Get activity feed with pagination."""
        query = self.db.query(ActivityEvent)
        
        if public_only:
            query = query.filter(ActivityEvent.is_public == True)
        
        total = query.count()
        
        events = (
            query
            .order_by(ActivityEvent.created_at.desc())
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )
        
        return self._format_events(events), total

    def get_user_activity(
        self,
        user_id: int,
        page: int = 1,
        per_page: int = 20,
        public_only: bool = False,
    ) -> Tuple[List[ActivityEventRead], int]:
        """Get activity for a specific user."""
        query = self.db.query(ActivityEvent).filter(ActivityEvent.user_id == user_id)
        
        if public_only:
            query = query.filter(ActivityEvent.is_public == True)
        
        total = query.count()
        
        events = (
            query
            .order_by(ActivityEvent.created_at.desc())
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )
        
        return self._format_events(events), total

    def get_team_activity(
        self,
        team_id: int,
        page: int = 1,
        per_page: int = 20,
    ) -> Tuple[List[ActivityEventRead], int]:
        """Get activity for a specific team."""
        query = self.db.query(ActivityEvent).filter(
            ActivityEvent.team_id == team_id,
            ActivityEvent.is_public == True,
        )
        
        total = query.count()
        
        events = (
            query
            .order_by(ActivityEvent.created_at.desc())
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )
        
        return self._format_events(events), total

    def get_project_activity(
        self,
        project_id: int,
        page: int = 1,
        per_page: int = 20,
    ) -> Tuple[List[ActivityEventRead], int]:
        """Get activity for a specific project."""
        query = self.db.query(ActivityEvent).filter(
            ActivityEvent.project_id == project_id,
            ActivityEvent.is_public == True,
        )
        
        total = query.count()
        
        events = (
            query
            .order_by(ActivityEvent.created_at.desc())
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )
        
        return self._format_events(events), total

    def _format_events(self, events: List[ActivityEvent]) -> List[ActivityEventRead]:
        """Format activity events with user info."""
        result = []
        for event in events:
            user = self.db.query(User).filter(User.id == event.user_id).first()
            result.append(ActivityEventRead(
                id=event.id,
                event_type=event.event_type,
                title=event.title,
                description=event.description,
                user_id=event.user_id,
                username=user.username if user else "Unknown",
                user_avatar_url=user.avatar_url if user else None,
                project_id=event.project_id,
                team_id=event.team_id,
                quest_id=event.quest_id,
                badge_id=event.badge_id,
                achievement_id=event.achievement_id,
                xp_amount=event.xp_amount,
                is_public=bool(event.is_public),
                created_at=event.created_at,
            ))
        return result

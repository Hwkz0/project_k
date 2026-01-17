from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.team import Team, TeamMember, TeamRole
from app.models.user import User
from app. schemas.team import TeamCreate, TeamUpdate


class TeamService:
    """Service for team operations."""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, team_id: int) -> Optional[Team]:
        """Get team by ID."""
        return self.db.query(Team).filter(Team.id == team_id).first()

    def get_by_slug(self, slug: str) -> Optional[Team]:
        """Get team by slug."""
        return self.db.query(Team).filter(Team.slug == slug).first()

    def get_user_teams(self, user_id: int) -> List[Team]:
        """Get teams for a user."""
        return (
            self.db.query(Team)
            .join(TeamMember)
            .filter(TeamMember.user_id == user_id)
            .all()
        )

    def create(self, team_in:  TeamCreate, owner:  User) -> Team:
        """Create a new team."""
        team = Team(
            name=team_in.name,
            slug=team_in.slug,
            description=team_in.description,
        )
        self.db.add(team)
        self.db.flush()

        # Add owner as team member
        membership = TeamMember(
            team_id=team.id,
            user_id=owner.id,
            role=TeamRole. OWNER,
        )
        self.db.add(membership)
        self.db.commit()
        self.db.refresh(team)
        return team

    def update(self, team: Team, team_in: TeamUpdate) -> Team:
        """Update a team."""
        update_data = team_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(team, field, value)
        self.db.commit()
        self.db.refresh(team)
        return team

    def add_member(self, team: Team, user: User, role: TeamRole = TeamRole.MEMBER) -> TeamMember:
        """Add a member to a team."""
        membership = TeamMember(team_id=team.id, user_id=user.id, role=role)
        self.db.add(membership)
        self.db.commit()
        self.db.refresh(membership)
        return membership

    def get_members(self, team_id: int) -> List[TeamMember]:
        """Get team members."""
        return self.db.query(TeamMember).filter(TeamMember.team_id == team_id).all()
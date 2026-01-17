"""Team endpoints."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.models.user import User
from app.models.team import TeamRole
from app.schemas.team import TeamCreate, TeamUpdate, TeamRead, TeamMemberRead, TeamMemberAdd
from app.services.team_service import TeamService
from app.services.user_service import UserService
from app.services.activity_service import ActivityService
from app.models.activity import ActivityType

router = APIRouter()


@router.get("/", response_model=List[TeamRead])
def list_teams(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    """List all teams."""
    teams = db.query(TeamService.__class__).offset(skip).limit(limit).all()
    # TODO: Implement proper listing
    team_service = TeamService(db)
    return []


@router.post("/", response_model=TeamRead, status_code=status.HTTP_201_CREATED)
def create_team(
    team_in: TeamCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Create a new team."""
    team_service = TeamService(db)
    
    # Check if slug exists
    if team_service.get_by_slug(team_in.slug):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Team slug already taken",
        )
    
    team = team_service.create(team_in, current_user)
    
    # Create activity
    activity_service = ActivityService(db)
    activity_service.create_event(
        user_id=current_user.id,
        event_type=ActivityType.TEAM_CREATED,
        title=f"{current_user.username} created team {team.name}",
        team_id=team.id,
    )
    
    return team


@router.get("/my-teams", response_model=List[TeamRead])
def get_my_teams(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get teams the current user belongs to."""
    team_service = TeamService(db)
    return team_service.get_user_teams(current_user.id)


@router.get("/{team_id}", response_model=TeamRead)
def get_team(
    team_id: int,
    db: Session = Depends(get_db),
):
    """Get a team by ID."""
    team_service = TeamService(db)
    team = team_service.get_by_id(team_id)
    
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found",
        )
    
    return team


@router.put("/{team_id}", response_model=TeamRead)
def update_team(
    team_id: int,
    team_in: TeamUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Update a team (admin/owner only)."""
    team_service = TeamService(db)
    team = team_service.get_by_id(team_id)
    
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found",
        )
    
    # Check if user is admin/owner
    members = team_service.get_members(team_id)
    user_member = next((m for m in members if m.user_id == current_user.id), None)
    
    if not user_member or user_member.role not in [TeamRole.OWNER, TeamRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this team",
        )
    
    return team_service.update(team, team_in)


@router.get("/{team_id}/members", response_model=List[TeamMemberRead])
def get_team_members(
    team_id: int,
    db: Session = Depends(get_db),
):
    """Get team members."""
    team_service = TeamService(db)
    team = team_service.get_by_id(team_id)
    
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found",
        )
    
    members = team_service.get_members(team_id)
    result = []
    user_service = UserService(db)
    
    for member in members:
        user = user_service.get_by_id(member.user_id)
        result.append(TeamMemberRead(
            id=member.id,
            user_id=member.user_id,
            username=user.username,
            full_name=user.full_name,
            avatar_url=user.avatar_url,
            role=member.role,
            joined_at=member.joined_at,
        ))
    
    return result


@router.post("/{team_id}/members", response_model=TeamMemberRead, status_code=status.HTTP_201_CREATED)
def add_team_member(
    team_id: int,
    member_in: TeamMemberAdd,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Add a member to a team (admin/owner only)."""
    team_service = TeamService(db)
    team = team_service.get_by_id(team_id)
    
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found",
        )
    
    # Check if current user is admin/owner
    members = team_service.get_members(team_id)
    user_member = next((m for m in members if m.user_id == current_user.id), None)
    
    if not user_member or user_member.role not in [TeamRole.OWNER, TeamRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to add members to this team",
        )
    
    # Check if user to add exists
    user_service = UserService(db)
    user_to_add = user_service.get_by_id(member_in.user_id)
    
    if not user_to_add:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    # Check if already a member
    if any(m.user_id == member_in.user_id for m in members):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already a team member",
        )
    
    membership = team_service.add_member(team, user_to_add, member_in.role)
    
    # Create activity
    activity_service = ActivityService(db)
    activity_service.create_event(
        user_id=user_to_add.id,
        event_type=ActivityType.TEAM_JOINED,
        title=f"{user_to_add.username} joined team {team.name}",
        team_id=team.id,
    )
    
    return TeamMemberRead(
        id=membership.id,
        user_id=membership.user_id,
        username=user_to_add.username,
        full_name=user_to_add.full_name,
        avatar_url=user_to_add.avatar_url,
        role=membership.role,
        joined_at=membership.joined_at,
    )

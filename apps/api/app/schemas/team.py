"""Team schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models.team import TeamRole


class TeamBase(BaseModel):
    """Base team schema."""

    name: str = Field(..., min_length=1, max_length=100)
    slug: str = Field(..., min_length=1, max_length=100, pattern=r"^[a-z0-9-]+$")
    description: Optional[str] = None


class TeamCreate(TeamBase):
    """Schema for creating a team."""

    pass


class TeamUpdate(BaseModel):
    """Schema for updating a team."""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    avatar_url: Optional[str] = None


class TeamRead(TeamBase):
    """Schema for reading a team."""

    id: int
    avatar_url: Optional[str] = None
    created_at: datetime
    member_count: int = 0

    class Config:
        from_attributes = True


class TeamMemberRead(BaseModel):
    """Schema for reading a team member."""

    id: int
    user_id: int
    username: str
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    role: TeamRole
    joined_at: datetime

    class Config:
        from_attributes = True


class TeamMemberAdd(BaseModel):
    """Schema for adding a team member."""

    user_id: int
    role: TeamRole = TeamRole.MEMBER

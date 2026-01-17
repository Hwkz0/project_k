"""Project schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models.project import ProjectStatus


class ProjectBase(BaseModel):
    """Base project schema."""

    name: str = Field(..., min_length=1, max_length=100)
    slug: str = Field(..., min_length=1, max_length=100, pattern=r"^[a-z0-9-]+$")
    description: Optional[str] = None


class ProjectCreate(ProjectBase):
    """Schema for creating a project."""

    team_id: Optional[int] = None
    ai_provider: Optional[str] = None
    ai_model: Optional[str] = None


class ProjectUpdate(BaseModel):
    """Schema for updating a project."""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None
    ai_provider: Optional[str] = None
    ai_model: Optional[str] = None


class ProjectRead(ProjectBase):
    """Schema for reading a project."""

    id: int
    status: ProjectStatus
    owner_id: int
    team_id: Optional[int] = None
    ai_provider: Optional[str] = None
    ai_model: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ProjectWithOwner(ProjectRead):
    """Project schema with owner info."""

    owner_username: str
    owner_avatar_url: Optional[str] = None

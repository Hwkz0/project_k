from typing import List, Optional

from sqlalchemy.orm import Session

from app.models. project import Project, ProjectStatus
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectUpdate


class ProjectService:
    """Service for project operations."""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, project_id: int) -> Optional[Project]:
        """Get project by ID."""
        return self.db.query(Project).filter(Project.id == project_id).first()

    def get_by_slug(self, owner_id: int, slug: str) -> Optional[Project]:
        """Get project by owner and slug."""
        return (
            self.db.query(Project)
            .filter(Project.owner_id == owner_id, Project.slug == slug)
            .first()
        )

    def get_user_projects(self, user_id: int) -> List[Project]:
        """Get projects for a user."""
        return self.db.query(Project).filter(Project.owner_id == user_id).all()

    def get_team_projects(self, team_id: int) -> List[Project]:
        """Get projects for a team."""
        return self.db. query(Project).filter(Project.team_id == team_id).all()

    def get_all(self, skip: int = 0, limit:  int = 20) -> List[Project]:
        """Get all projects with pagination."""
        return self.db.query(Project).offset(skip).limit(limit).all()

    def create(self, project_in: ProjectCreate, owner: User) -> Project:
        """Create a new project."""
        project = Project(
            name=project_in.name,
            slug=project_in.slug,
            description=project_in.description,
            owner_id=owner.id,
            team_id=project_in.team_id,
            ai_provider=project_in.ai_provider,
            ai_model=project_in.ai_model,
        )
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def update(self, project:  Project, project_in: ProjectUpdate) -> Project:
        """Update a project."""
        update_data = project_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(project, field, value)
        self.db.commit()
        self.db.refresh(project)
        return project

    def publish(self, project: Project) -> Project:
        """Publish a project."""
        from datetime import datetime

        project.status = ProjectStatus. PUBLISHED
        project.published_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(project)
        return project
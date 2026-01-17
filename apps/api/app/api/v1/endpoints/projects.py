"""Project endpoints."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_active_user, get_optional_user
from app.models.user import User
from app.models.project import ProjectStatus
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectRead
from app.services.project_service import ProjectService
from app.services.activity_service import ActivityService
from app.jobs.gamification_jobs import check_achievements_for_user
from app.models.activity import ActivityType

router = APIRouter()


@router.get("/", response_model=List[ProjectRead])
def list_projects(
    skip: int = 0,
    limit: int = 20,
    status: ProjectStatus = None,
    db: Session = Depends(get_db),
):
    """List all projects (optionally filtered by status)."""
    project_service = ProjectService(db)
    projects = project_service.get_all(skip=skip, limit=limit)
    
    if status:
        projects = [p for p in projects if p.status == status]
    
    return projects


@router.post("/", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(
    project_in: ProjectCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Create a new project."""
    project_service = ProjectService(db)
    
    # Check if slug exists for this user
    if project_service.get_by_slug(current_user.id, project_in.slug):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project slug already exists for this user",
        )
    
    project = project_service.create(project_in, current_user)
    
    # Create activity
    activity_service = ActivityService(db)
    activity_service.create_event(
        user_id=current_user.id,
        event_type=ActivityType.PROJECT_CREATED,
        title=f"{current_user.username} created project {project.name}",
        project_id=project.id,
    )
    
    # Check for achievements in background
    background_tasks.add_task(check_achievements_for_user, db, current_user.id)
    
    return project


@router.get("/my-projects", response_model=List[ProjectRead])
def get_my_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get current user's projects."""
    project_service = ProjectService(db)
    return project_service.get_user_projects(current_user.id)


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
):
    """Get a project by ID."""
    project_service = ProjectService(db)
    project = project_service.get_by_id(project_id)
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    
    return project


@router.put("/{project_id}", response_model=ProjectRead)
def update_project(
    project_id: int,
    project_in: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Update a project."""
    project_service = ProjectService(db)
    project = project_service.get_by_id(project_id)
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    
    if project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this project",
        )
    
    updated = project_service.update(project, project_in)
    
    # Create activity
    activity_service = ActivityService(db)
    activity_service.create_event(
        user_id=current_user.id,
        event_type=ActivityType.PROJECT_UPDATED,
        title=f"{current_user.username} updated project {project.name}",
        project_id=project.id,
    )
    
    return updated


@router.post("/{project_id}/publish", response_model=ProjectRead)
def publish_project(
    project_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Publish a project."""
    project_service = ProjectService(db)
    project = project_service.get_by_id(project_id)
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    
    if project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to publish this project",
        )
    
    if project.status == ProjectStatus.PUBLISHED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project is already published",
        )
    
    published = project_service.publish(project)
    
    # Create activity
    activity_service = ActivityService(db)
    activity_service.create_event(
        user_id=current_user.id,
        event_type=ActivityType.PROJECT_PUBLISHED,
        title=f"{current_user.username} published project {project.name}",
        description=f"🚀 {project.name} is now live!",
        project_id=project.id,
        xp_amount=50,  # Bonus XP for publishing
    )
    
    # Award XP and check achievements
    from app.services.user_service import UserService
    user_service = UserService(db)
    user_service.add_xp(current_user, 50)
    
    background_tasks.add_task(check_achievements_for_user, db, current_user.id)
    
    return published


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Delete a project (soft delete - archive)."""
    project_service = ProjectService(db)
    project = project_service.get_by_id(project_id)
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    
    if project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this project",
        )
    
    # Soft delete - archive
    from app.schemas.project import ProjectUpdate
    project_service.update(project, ProjectUpdate(status=ProjectStatus.ARCHIVED))

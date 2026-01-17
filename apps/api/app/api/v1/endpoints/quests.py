"""Quest endpoints."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.models.user import User
from app.schemas.quest import QuestCreate, QuestUpdate, QuestRead, QuestCompletionRead
from app.services.quest_service import QuestService
from app.services.user_service import UserService
from app.services.activity_service import ActivityService
from app.jobs.gamification_jobs import check_achievements_for_user, recalculate_leaderboards
from app.models.activity import ActivityType

router = APIRouter()


@router.get("/", response_model=List[QuestRead])
def list_quests(
    skip: int = 0,
    limit: int = 20,
    active_only: bool = True,
    db: Session = Depends(get_db),
):
    """List all quests."""
    quest_service = QuestService(db)
    return quest_service.get_all(skip=skip, limit=limit, active_only=active_only)


@router.post("/", response_model=QuestRead, status_code=status.HTTP_201_CREATED)
def create_quest(
    quest_in: QuestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Create a new quest (admin only in production)."""
    # TODO: Add admin check
    quest_service = QuestService(db)
    quest = quest_service.create(quest_in)
    
    # Create activity
    activity_service = ActivityService(db)
    activity_service.create_event(
        user_id=current_user.id,
        event_type=ActivityType.QUEST_CREATED,
        title=f"New quest available: {quest.title}",
        quest_id=quest.id,
    )
    
    return quest


@router.get("/global", response_model=List[QuestRead])
def list_global_quests(
    db: Session = Depends(get_db),
):
    """List global quests (not tied to a project)."""
    quest_service = QuestService(db)
    return quest_service.get_global_quests()


@router.get("/my-completions", response_model=List[QuestCompletionRead])
def get_my_completions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get current user's quest completions."""
    quest_service = QuestService(db)
    return quest_service.get_user_completions(current_user.id)


@router.get("/{quest_id}", response_model=QuestRead)
def get_quest(
    quest_id: int,
    db: Session = Depends(get_db),
):
    """Get a quest by ID."""
    quest_service = QuestService(db)
    quest = quest_service.get_by_id(quest_id)
    
    if not quest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quest not found",
        )
    
    return quest


@router.put("/{quest_id}", response_model=QuestRead)
def update_quest(
    quest_id: int,
    quest_in: QuestUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Update a quest (admin only in production)."""
    # TODO: Add admin check
    quest_service = QuestService(db)
    quest = quest_service.get_by_id(quest_id)
    
    if not quest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quest not found",
        )
    
    return quest_service.update(quest, quest_in)


@router.post("/{quest_id}/complete", response_model=QuestCompletionRead)
def complete_quest(
    quest_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Complete a quest."""
    quest_service = QuestService(db)
    quest = quest_service.get_by_id(quest_id)
    
    if not quest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quest not found",
        )
    
    if not quest.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quest is not active",
        )
    
    # Check if already completed (non-repeatable)
    if not quest.is_repeatable and quest_service.is_completed_by_user(quest_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quest already completed",
        )
    
    try:
        completion = quest_service.complete_quest(quest, current_user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    
    # Award XP
    user_service = UserService(db)
    user, leveled_up = user_service.add_xp(current_user, quest.xp_reward)
    
    # Create activity
    activity_service = ActivityService(db)
    activity_service.create_event(
        user_id=current_user.id,
        event_type=ActivityType.QUEST_COMPLETED,
        title=f"{current_user.username} completed quest: {quest.title}",
        description=f"Earned {quest.xp_reward} XP!",
        quest_id=quest.id,
        xp_amount=quest.xp_reward,
    )
    
    # If leveled up, create another activity
    if leveled_up:
        activity_service.create_event(
            user_id=current_user.id,
            event_type=ActivityType.USER_LEVEL_UP,
            title=f"{current_user.username} reached level {user.level}!",
            description=f"🎉 Congratulations on reaching level {user.level}!",
            xp_amount=0,
        )
    
    # Check achievements and recalculate leaderboards in background
    background_tasks.add_task(check_achievements_for_user, db, current_user.id)
    background_tasks.add_task(recalculate_leaderboards, db)
    
    return completion


@router.get("/{quest_id}/status")
def get_quest_status(
    quest_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get quest completion status for current user."""
    quest_service = QuestService(db)
    quest = quest_service.get_by_id(quest_id)
    
    if not quest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quest not found",
        )
    
    is_completed = quest_service.is_completed_by_user(quest_id, current_user.id)
    
    return {
        "quest_id": quest_id,
        "is_completed": is_completed,
        "is_repeatable": quest.is_repeatable,
        "can_complete": quest.is_active and (quest.is_repeatable or not is_completed),
    }

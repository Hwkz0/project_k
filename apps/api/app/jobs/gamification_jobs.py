"""Background jobs for gamification and leaderboards."""

from sqlalchemy.orm import Session

from app.models.user import User
from app.models.activity import ActivityType
from app.services.gamification_service import GamificationService
from app.services.activity_service import ActivityService
from app.services.leaderboard_service import LeaderboardService
from app.models.leaderboard import LeaderboardType


def check_achievements_for_user(db: Session, user_id: int):
    """
    Background job to check and award badges/achievements for a user.
    
    This is called after quest completions, project publications, etc.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return
    
    gamification_service = GamificationService(db)
    activity_service = ActivityService(db)
    
    # Check and award badges
    awarded_badges = gamification_service.check_and_award_badges(user)
    
    for user_badge in awarded_badges:
        badge = user_badge.badge
        
        # Award bonus XP
        if badge.xp_bonus > 0:
            user.xp += badge.xp_bonus
            db.commit()
        
        # Create activity event
        activity_service.create_event(
            user_id=user.id,
            event_type=ActivityType.BADGE_EARNED,
            title=f"{user.username} earned the '{badge.name}' badge!",
            description=badge.description,
            badge_id=badge.id,
            xp_amount=badge.xp_bonus,
        )


def recalculate_leaderboards(db: Session):
    """
    Background job to recalculate and cache leaderboards.
    
    This can be called periodically or after significant XP changes.
    """
    leaderboard_service = LeaderboardService(db)
    
    # Recalculate global leaderboard
    global_entries = leaderboard_service.get_global_leaderboard(limit=100)
    leaderboard_service.cache_leaderboard(
        leaderboard_type=LeaderboardType.GLOBAL,
        entries=global_entries,
    )
    
    # Recalculate weekly leaderboard
    weekly_entries, weekly_key = leaderboard_service.get_weekly_leaderboard(limit=100)
    leaderboard_service.cache_leaderboard(
        leaderboard_type=LeaderboardType.WEEKLY,
        entries=weekly_entries,
        period_key=weekly_key,
    )
    
    # Recalculate monthly leaderboard
    monthly_entries, monthly_key = leaderboard_service.get_monthly_leaderboard(limit=100)
    leaderboard_service.cache_leaderboard(
        leaderboard_type=LeaderboardType.MONTHLY,
        entries=monthly_entries,
        period_key=monthly_key,
    )


def award_daily_bonus(db: Session, user_id: int):
    """
    Background job to award daily login bonus.
    
    This is a placeholder for future implementation.
    """
    # TODO: Implement daily login bonus
    pass


def process_achievement_progress(db: Session, user_id: int, achievement_type: str, progress: int):
    """
    Background job to update achievement progress.
    
    This is a placeholder for more complex achievement tracking.
    """
    # TODO: Implement achievement progress tracking
    pass

"""Seed script to create demo data."""

import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta
import random

from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.models.user import User
from app.models.team import Team, TeamMember, TeamRole
from app.models.project import Project, ProjectStatus
from app.models.quest import Quest, QuestCompletion, QuestDifficulty, QuestCategory
from app.models.gamification import Badge, Achievement, BadgeCategory, AchievementCategory
from app.models.activity import ActivityEvent, ActivityType


def seed_database():
    """Seed the database with demo data."""
    db = SessionLocal()
    
    try:
        print("🌱 Starting database seeding...")
        
        # Clear existing data (optional, comment out for append mode)
        print("  Clearing existing data...")
        db.query(ActivityEvent).delete()
        db.query(QuestCompletion).delete()
        db.query(Quest).delete()
        db.query(Project).delete()
        db.query(TeamMember).delete()
        db.query(Team).delete()
        db.query(Achievement).delete()
        db.query(Badge).delete()
        db.query(User).delete()
        db.commit()
        
        # Create users
        print("  Creating users...")
        users = []
        user_data = [
            ("alice", "alice@example.com", "Alice Johnson", 1250, 4),
            ("bob", "bob@example.com", "Bob Smith", 890, 3),
            ("charlie", "charlie@example.com", "Charlie Brown", 2100, 5),
            ("diana", "diana@example.com", "Diana Prince", 450, 2),
            ("eve", "eve@example.com", "Eve Wilson", 3500, 6),
            ("frank", "frank@example.com", "Frank Castle", 180, 1),
            ("grace", "grace@example.com", "Grace Hopper", 5200, 8),
            ("henry", "henry@example.com", "Henry Ford", 720, 3),
        ]
        
        for username, email, full_name, xp, level in user_data:
            user = User(
                username=username,
                email=email,
                full_name=full_name,
                hashed_password=get_password_hash("demo123"),
                xp=xp,
                level=level,
                is_active=True,
                created_at=datetime.utcnow() - timedelta(days=random.randint(30, 180)),
            )
            db.add(user)
            users.append(user)
        
        db.commit()
        for user in users:
            db.refresh(user)
        
        # Create teams
        print("  Creating teams...")
        teams = []
        team_data = [
            ("AI Innovators", "ai-innovators", "Building the future of AI applications"),
            ("Code Warriors", "code-warriors", "Elite developers pushing boundaries"),
            ("Data Wizards", "data-wizards", "Making sense of complex data"),
        ]
        
        for name, slug, description in team_data:
            team = Team(
                name=name,
                slug=slug,
                description=description,
                created_at=datetime.utcnow() - timedelta(days=random.randint(60, 120)),
            )
            db.add(team)
            teams.append(team)
        
        db.commit()
        for team in teams:
            db.refresh(team)
        
        # Add team members
        print("  Adding team members...")
        # Team 1: Alice (owner), Bob, Charlie
        db.add(TeamMember(team_id=teams[0].id, user_id=users[0].id, role=TeamRole.OWNER))
        db.add(TeamMember(team_id=teams[0].id, user_id=users[1].id, role=TeamRole.MEMBER))
        db.add(TeamMember(team_id=teams[0].id, user_id=users[2].id, role=TeamRole.ADMIN))
        
        # Team 2: Diana (owner), Eve, Frank
        db.add(TeamMember(team_id=teams[1].id, user_id=users[3].id, role=TeamRole.OWNER))
        db.add(TeamMember(team_id=teams[1].id, user_id=users[4].id, role=TeamRole.MEMBER))
        db.add(TeamMember(team_id=teams[1].id, user_id=users[5].id, role=TeamRole.MEMBER))
        
        # Team 3: Grace (owner), Henry
        db.add(TeamMember(team_id=teams[2].id, user_id=users[6].id, role=TeamRole.OWNER))
        db.add(TeamMember(team_id=teams[2].id, user_id=users[7].id, role=TeamRole.MEMBER))
        
        db.commit()
        
        # Create projects
        print("  Creating projects...")
        projects = []
        project_data = [
            ("ChatBot Pro", "chatbot-pro", "AI-powered customer service chatbot", users[0], teams[0], ProjectStatus.PUBLISHED),
            ("Image Generator", "image-gen", "Text-to-image generation using diffusion models", users[2], teams[0], ProjectStatus.IN_PROGRESS),
            ("Code Assistant", "code-assistant", "AI pair programming tool", users[4], teams[1], ProjectStatus.PUBLISHED),
            ("Data Analyzer", "data-analyzer", "Automated data analysis and visualization", users[6], teams[2], ProjectStatus.DRAFT),
            ("Voice Transcriber", "voice-transcribe", "Real-time speech-to-text transcription", users[1], None, ProjectStatus.IN_PROGRESS),
            ("Document Summarizer", "doc-summarizer", "Intelligent document summarization", users[3], None, ProjectStatus.PUBLISHED),
        ]
        
        for name, slug, description, owner, team, status in project_data:
            project = Project(
                name=name,
                slug=slug,
                description=description,
                owner_id=owner.id,
                team_id=team.id if team else None,
                status=status,
                ai_provider="mock" if status == ProjectStatus.PUBLISHED else None,
                created_at=datetime.utcnow() - timedelta(days=random.randint(10, 60)),
                published_at=datetime.utcnow() - timedelta(days=random.randint(1, 10)) if status == ProjectStatus.PUBLISHED else None,
            )
            db.add(project)
            projects.append(project)
        
        db.commit()
        for project in projects:
            db.refresh(project)
        
        # Create quests
        print("  Creating quests...")
        quests = []
        quest_data = [
            # Global quests
            ("First Steps", "Complete your profile setup", QuestDifficulty.EASY, QuestCategory.SETUP, 10, None),
            ("Hello AI World", "Create your first AI-powered project", QuestDifficulty.EASY, QuestCategory.DEVELOPMENT, 25, None),
            ("Documentation Hero", "Write documentation for your project", QuestDifficulty.MEDIUM, QuestCategory.DOCUMENTATION, 30, None),
            ("Test Master", "Achieve 80% test coverage", QuestDifficulty.HARD, QuestCategory.TESTING, 50, None),
            ("Deploy to Production", "Deploy your app to a cloud provider", QuestDifficulty.HARD, QuestCategory.DEPLOYMENT, 75, None),
            ("Community Star", "Help 5 other developers", QuestDifficulty.MEDIUM, QuestCategory.COMMUNITY, 40, None),
            ("AI Expert", "Integrate 3 different AI providers", QuestDifficulty.EXPERT, QuestCategory.DEVELOPMENT, 100, None),
            
            # Project-specific quests
            ("ChatBot Training", "Train your chatbot with custom data", QuestDifficulty.MEDIUM, QuestCategory.DEVELOPMENT, 35, projects[0]),
            ("Image Quality", "Achieve high-quality image generation", QuestDifficulty.HARD, QuestCategory.TESTING, 60, projects[1]),
            ("Code Review", "Complete a code review session", QuestDifficulty.EASY, QuestCategory.COMMUNITY, 20, projects[2]),
        ]
        
        for title, description, difficulty, category, xp_reward, project in quest_data:
            quest = Quest(
                title=title,
                description=description,
                difficulty=difficulty,
                category=category,
                xp_reward=xp_reward,
                project_id=project.id if project else None,
                is_active=True,
                is_repeatable=category == QuestCategory.COMMUNITY,
                created_at=datetime.utcnow() - timedelta(days=random.randint(30, 90)),
            )
            db.add(quest)
            quests.append(quest)
        
        db.commit()
        for quest in quests:
            db.refresh(quest)
        
        # Create badges
        print("  Creating badges...")
        badge_data = [
            ("Newcomer", "Welcome to the platform!", "🌟", BadgeCategory.MILESTONE, "xp_total", 0, 0),
            ("Rising Star", "Earned 100 XP", "⭐", BadgeCategory.MILESTONE, "xp_total", 100, 10),
            ("Bright Spark", "Earned 500 XP", "✨", BadgeCategory.MILESTONE, "xp_total", 500, 25),
            ("Power User", "Earned 1000 XP", "💫", BadgeCategory.MILESTONE, "xp_total", 1000, 50),
            ("Legend", "Earned 5000 XP", "🏆", BadgeCategory.MILESTONE, "xp_total", 5000, 100),
            
            ("Quest Novice", "Completed 1 quest", "🎯", BadgeCategory.ACHIEVEMENT, "quest_count", 1, 5),
            ("Quest Hunter", "Completed 5 quests", "🎯", BadgeCategory.ACHIEVEMENT, "quest_count", 5, 15),
            ("Quest Master", "Completed 20 quests", "🎯", BadgeCategory.ACHIEVEMENT, "quest_count", 20, 50),
            
            ("Level 5", "Reached level 5", "📈", BadgeCategory.SKILL, "level", 5, 25),
            ("Level 10", "Reached level 10", "📈", BadgeCategory.SKILL, "level", 10, 75),
        ]
        
        for name, description, icon, category, req_type, req_value, xp_bonus in badge_data:
            badge = Badge(
                name=name,
                description=description,
                icon=icon,
                category=category,
                requirement_type=req_type,
                requirement_value=req_value,
                xp_bonus=xp_bonus,
                is_active=True,
                created_at=datetime.utcnow() - timedelta(days=90),
            )
            db.add(badge)
        
        db.commit()
        
        # Create achievements
        print("  Creating achievements...")
        achievement_data = [
            ("First Blood", "Complete your very first quest", "🩸", AchievementCategory.BEGINNER, 10, 25, 100, False),
            ("Quick Learner", "Complete 3 quests in one day", "📚", AchievementCategory.BEGINNER, 20, 50, 80, False),
            ("Project Pioneer", "Create your first project", "🚀", AchievementCategory.BEGINNER, 15, 30, 90, False),
            ("Team Player", "Join a team", "🤝", AchievementCategory.BEGINNER, 10, 20, 85, False),
            ("Publisher", "Publish your first project", "📢", AchievementCategory.INTERMEDIATE, 30, 75, 60, False),
            ("Expert Coder", "Complete 10 development quests", "💻", AchievementCategory.ADVANCED, 50, 100, 40, False),
            ("AI Whisperer", "Use all AI providers", "🤖", AchievementCategory.EXPERT, 100, 250, 10, False),
            ("Completionist", "Earn all badges", "🏅", AchievementCategory.LEGENDARY, 500, 1000, 1, True),
        ]
        
        for name, description, icon, category, points, xp_reward, rarity, is_secret in achievement_data:
            achievement = Achievement(
                name=name,
                description=description,
                icon=icon,
                category=category,
                points=points,
                xp_reward=xp_reward,
                rarity_score=rarity,
                is_secret=is_secret,
                is_active=True,
                created_at=datetime.utcnow() - timedelta(days=90),
            )
            db.add(achievement)
        
        db.commit()
        
        # Create some quest completions
        print("  Creating quest completions...")
        completions = [
            (users[0], quests[0], 30),
            (users[0], quests[1], 25),
            (users[0], quests[2], 20),
            (users[2], quests[0], 28),
            (users[2], quests[1], 22),
            (users[2], quests[3], 15),
            (users[2], quests[4], 10),
            (users[4], quests[0], 35),
            (users[4], quests[1], 30),
            (users[4], quests[2], 25),
            (users[4], quests[3], 20),
            (users[4], quests[4], 15),
            (users[4], quests[5], 10),
            (users[6], quests[0], 40),
            (users[6], quests[1], 35),
            (users[6], quests[2], 30),
            (users[6], quests[3], 25),
            (users[6], quests[4], 20),
            (users[6], quests[5], 15),
            (users[6], quests[6], 5),
        ]
        
        for user, quest, days_ago in completions:
            completion = QuestCompletion(
                user_id=user.id,
                quest_id=quest.id,
                xp_earned=quest.xp_reward,
                completed_at=datetime.utcnow() - timedelta(days=days_ago),
            )
            db.add(completion)
        
        db.commit()
        
        # Create activity events
        print("  Creating activity events...")
        activities = [
            (users[6], ActivityType.USER_LEVEL_UP, "grace reached level 8!", None, None, 7),
            (users[4], ActivityType.PROJECT_PUBLISHED, "eve published Code Assistant", projects[2].id, None, 5),
            (users[0], ActivityType.QUEST_COMPLETED, "alice completed Documentation Hero", None, quests[2].id, 4),
            (users[2], ActivityType.BADGE_EARNED, "charlie earned Power User badge", None, None, 3),
            (users[6], ActivityType.QUEST_COMPLETED, "grace completed AI Expert quest", None, quests[6].id, 2),
            (users[3], ActivityType.PROJECT_PUBLISHED, "diana published Document Summarizer", projects[5].id, None, 1),
        ]
        
        for user, event_type, title, project_id, quest_id, days_ago in activities:
            event = ActivityEvent(
                user_id=user.id,
                event_type=event_type,
                title=title,
                project_id=project_id,
                quest_id=quest_id,
                is_public=True,
                created_at=datetime.utcnow() - timedelta(days=days_ago),
            )
            db.add(event)
        
        db.commit()
        
        print("\n✅ Database seeding completed!")
        print(f"   Created {len(users)} users")
        print(f"   Created {len(teams)} teams")
        print(f"   Created {len(projects)} projects")
        print(f"   Created {len(quests)} quests")
        print("\n🔑 Demo login credentials:")
        print("   Email: alice@example.com")
        print("   Password: demo123")
        print("\n   (All demo users use password: demo123)")
        
    except Exception as e:
        print(f"\n❌ Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()

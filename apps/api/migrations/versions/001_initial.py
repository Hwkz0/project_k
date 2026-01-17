"""Initial migration - create all tables

Revision ID: 001_initial
Revises: 
Create Date: 2026-01-17

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('username', sa.String(50), nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('full_name', sa.String(100), nullable=True),
        sa.Column('avatar_url', sa.Text(), nullable=True),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('xp', sa.Integer(), nullable=False, default=0),
        sa.Column('level', sa.Integer(), nullable=False, default=1),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('is_superuser', sa.Boolean(), nullable=False, default=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    op.create_index('ix_users_username', 'users', ['username'], unique=True)
    op.create_index('ix_users_id', 'users', ['id'], unique=False)

    # Teams table
    op.create_table(
        'teams',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('slug', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('avatar_url', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_teams_slug', 'teams', ['slug'], unique=True)
    op.create_index('ix_teams_id', 'teams', ['id'], unique=False)

    # Team members table
    op.create_table(
        'team_members',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('team_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('role', sa.Enum('owner', 'admin', 'member', name='teamrole'), nullable=False),
        sa.Column('joined_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['team_id'], ['teams.id']),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_team_members_id', 'team_members', ['id'], unique=False)

    # Projects table
    op.create_table(
        'projects',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('slug', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.Enum('draft', 'in_progress', 'published', 'archived', name='projectstatus'), nullable=False),
        sa.Column('owner_id', sa.Integer(), nullable=False),
        sa.Column('team_id', sa.Integer(), nullable=True),
        sa.Column('ai_provider', sa.String(50), nullable=True),
        sa.Column('ai_model', sa.String(100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('published_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id']),
        sa.ForeignKeyConstraint(['team_id'], ['teams.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_projects_slug', 'projects', ['slug'], unique=False)
    op.create_index('ix_projects_id', 'projects', ['id'], unique=False)

    # Quests table
    op.create_table(
        'quests',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('difficulty', sa.Enum('easy', 'medium', 'hard', 'expert', name='questdifficulty'), nullable=False),
        sa.Column('category', sa.Enum('setup', 'development', 'testing', 'deployment', 'documentation', 'community', name='questcategory'), nullable=False),
        sa.Column('xp_reward', sa.Integer(), nullable=False, default=10),
        sa.Column('project_id', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('is_repeatable', sa.Boolean(), nullable=False, default=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_quests_id', 'quests', ['id'], unique=False)

    # Quest completions table
    op.create_table(
        'quest_completions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('quest_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('completed_at', sa.DateTime(), nullable=False),
        sa.Column('xp_earned', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['quest_id'], ['quests.id']),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_quest_completions_id', 'quest_completions', ['id'], unique=False)

    # Badges table
    op.create_table(
        'badges',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('icon', sa.String(100), nullable=False),
        sa.Column('category', sa.Enum('achievement', 'milestone', 'skill', 'special', name='badgecategory'), nullable=False),
        sa.Column('requirement_type', sa.String(50), nullable=False),
        sa.Column('requirement_value', sa.Integer(), nullable=False),
        sa.Column('xp_bonus', sa.Integer(), nullable=False, default=0),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
    )
    op.create_index('ix_badges_id', 'badges', ['id'], unique=False)

    # User badges table
    op.create_table(
        'user_badges',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('badge_id', sa.Integer(), nullable=False),
        sa.Column('earned_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['badge_id'], ['badges.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_user_badges_id', 'user_badges', ['id'], unique=False)

    # Achievements table
    op.create_table(
        'achievements',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('icon', sa.String(100), nullable=False),
        sa.Column('category', sa.Enum('beginner', 'intermediate', 'advanced', 'expert', 'legendary', name='achievementcategory'), nullable=False),
        sa.Column('points', sa.Integer(), nullable=False, default=10),
        sa.Column('xp_reward', sa.Integer(), nullable=False, default=50),
        sa.Column('rarity_score', sa.Integer(), nullable=False, default=100),
        sa.Column('is_secret', sa.Boolean(), nullable=False, default=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
    )
    op.create_index('ix_achievements_id', 'achievements', ['id'], unique=False)

    # User achievements table
    op.create_table(
        'user_achievements',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('achievement_id', sa.Integer(), nullable=False),
        sa.Column('progress', sa.Integer(), nullable=False, default=0),
        sa.Column('target', sa.Integer(), nullable=False, default=1),
        sa.Column('is_completed', sa.Boolean(), nullable=False, default=False),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['achievement_id'], ['achievements.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_user_achievements_id', 'user_achievements', ['id'], unique=False)

    # Activity events table
    op.create_table(
        'activity_events',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('event_type', sa.Enum(
            'user_registered', 'user_level_up',
            'quest_completed', 'quest_created',
            'project_created', 'project_published', 'project_updated',
            'team_created', 'team_joined',
            'badge_earned', 'achievement_unlocked', 'xp_gained',
            'leaderboard_rank_up',
            name='activitytype'
        ), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=True),
        sa.Column('team_id', sa.Integer(), nullable=True),
        sa.Column('quest_id', sa.Integer(), nullable=True),
        sa.Column('badge_id', sa.Integer(), nullable=True),
        sa.Column('achievement_id', sa.Integer(), nullable=True),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('extra_data', sa.Text(), nullable=True),
        sa.Column('xp_amount', sa.Integer(), nullable=False, default=0),
        sa.Column('is_public', sa.Integer(), nullable=False, default=1),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id']),
        sa.ForeignKeyConstraint(['team_id'], ['teams.id']),
        sa.ForeignKeyConstraint(['quest_id'], ['quests.id']),
        sa.ForeignKeyConstraint(['badge_id'], ['badges.id']),
        sa.ForeignKeyConstraint(['achievement_id'], ['achievements.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_activity_events_id', 'activity_events', ['id'], unique=False)
    op.create_index('ix_activity_events_event_type', 'activity_events', ['event_type'], unique=False)
    op.create_index('ix_activity_events_created_at', 'activity_events', ['created_at'], unique=False)

    # Leaderboard entries table
    op.create_table(
        'leaderboard_entries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('leaderboard_type', sa.Enum('global', 'team', 'project', 'weekly', 'monthly', name='leaderboardtype'), nullable=False),
        sa.Column('scope_id', sa.Integer(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('rank', sa.Integer(), nullable=False),
        sa.Column('xp', sa.Integer(), nullable=False),
        sa.Column('level', sa.Integer(), nullable=False),
        sa.Column('period_key', sa.String(20), nullable=True),
        sa.Column('computed_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_leaderboard_entries_id', 'leaderboard_entries', ['id'], unique=False)


def downgrade() -> None:
    op.drop_table('leaderboard_entries')
    op.drop_table('activity_events')
    op.drop_table('user_achievements')
    op.drop_table('achievements')
    op.drop_table('user_badges')
    op.drop_table('badges')
    op.drop_table('quest_completions')
    op.drop_table('quests')
    op.drop_table('projects')
    op.drop_table('team_members')
    op.drop_table('teams')
    op.drop_table('users')
    
    # Drop enums
    op.execute('DROP TYPE IF EXISTS leaderboardtype')
    op.execute('DROP TYPE IF EXISTS activitytype')
    op.execute('DROP TYPE IF EXISTS achievementcategory')
    op.execute('DROP TYPE IF EXISTS badgecategory')
    op.execute('DROP TYPE IF EXISTS questcategory')
    op.execute('DROP TYPE IF EXISTS questdifficulty')
    op.execute('DROP TYPE IF EXISTS projectstatus')
    op.execute('DROP TYPE IF EXISTS teamrole')

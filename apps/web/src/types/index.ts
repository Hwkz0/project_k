// User types
export interface User {
  id: number;
  email: string;
  username: string;
  full_name: string | null;
  avatar_url: string | null;
  bio: string | null;
  xp: number;
  level: number;
  is_active: boolean;
  created_at: string;
}

export interface UserPublic {
  id: number;
  username: string;
  full_name: string | null;
  avatar_url: string | null;
  xp: number;
  level: number;
}

// Auth types
export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  username: string;
  password: string;
  full_name?: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

// Team types
export interface Team {
  id: number;
  name: string;
  slug: string;
  description: string | null;
  avatar_url: string | null;
  created_at: string;
  member_count: number;
}

export interface TeamMember {
  id: number;
  user_id: number;
  username: string;
  full_name: string | null;
  avatar_url: string | null;
  role: 'owner' | 'admin' | 'member';
  joined_at: string;
}

// Project types
export type ProjectStatus = 'draft' | 'in_progress' | 'published' | 'archived';

export interface Project {
  id: number;
  name: string;
  slug: string;
  description: string | null;
  status: ProjectStatus;
  owner_id: number;
  team_id: number | null;
  ai_provider: string | null;
  ai_model: string | null;
  created_at: string;
  updated_at: string;
  published_at: string | null;
}

// Quest types
export type QuestDifficulty = 'easy' | 'medium' | 'hard' | 'expert';
export type QuestCategory = 'setup' | 'development' | 'testing' | 'deployment' | 'documentation' | 'community';

export interface Quest {
  id: number;
  title: string;
  description: string;
  difficulty: QuestDifficulty;
  category: QuestCategory;
  xp_reward: number;
  project_id: number | null;
  is_active: boolean;
  is_repeatable: boolean;
  created_at: string;
}

export interface QuestCompletion {
  id: number;
  quest_id: number;
  user_id: number;
  completed_at: string;
  xp_earned: number;
}

export interface QuestStatus {
  quest_id: number;
  is_completed: boolean;
  is_repeatable: boolean;
  can_complete: boolean;
}

// Gamification types
export interface Badge {
  id: number;
  name: string;
  description: string;
  icon: string;
  category: string;
  requirement_type: string;
  requirement_value: number;
  xp_bonus: number;
  is_active: boolean;
  created_at: string;
}

export interface UserBadge {
  id: number;
  badge: Badge;
  earned_at: string;
}

export interface Achievement {
  id: number;
  name: string;
  description: string;
  icon: string;
  category: string;
  points: number;
  xp_reward: number;
  rarity_score: number;
  is_secret: boolean;
  is_active: boolean;
  created_at: string;
}

export interface UserAchievement {
  id: number;
  achievement: Achievement;
  progress: number;
  target: number;
  is_completed: boolean;
  completed_at: string | null;
  started_at: string;
}

// Leaderboard types
export type LeaderboardType = 'global' | 'team' | 'project' | 'weekly' | 'monthly';

export interface LeaderboardEntry {
  rank: number;
  user_id: number;
  username: string;
  avatar_url: string | null;
  xp: number;
  level: number;
  computed_at: string;
}

export interface LeaderboardResponse {
  leaderboard_type: LeaderboardType;
  scope_id: number | null;
  period_key: string | null;
  entries: LeaderboardEntry[];
  total_count: number;
}

// Activity types
export type ActivityType =
  | 'user_registered'
  | 'user_level_up'
  | 'quest_completed'
  | 'quest_created'
  | 'project_created'
  | 'project_published'
  | 'project_updated'
  | 'team_created'
  | 'team_joined'
  | 'badge_earned'
  | 'achievement_unlocked'
  | 'xp_gained'
  | 'leaderboard_rank_up';

export interface ActivityEvent {
  id: number;
  event_type: ActivityType;
  title: string;
  description: string | null;
  user_id: number;
  username: string;
  user_avatar_url: string | null;
  project_id: number | null;
  team_id: number | null;
  quest_id: number | null;
  badge_id: number | null;
  achievement_id: number | null;
  xp_amount: number;
  is_public: boolean;
  created_at: string;
}

export interface ActivityFeedResponse {
  items: ActivityEvent[];
  total: number;
  page: number;
  per_page: number;
  has_more: boolean;
}

// API Error type
export interface ApiError {
  detail: string;
}

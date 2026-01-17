import api from './client';
import type {
  User,
  LoginCredentials,
  RegisterData,
  AuthTokens,
  Project,
  Quest,
  QuestCompletion,
  QuestStatus,
  LeaderboardResponse,
  ActivityFeedResponse,
  Badge,
  Achievement,
  UserBadge,
  UserAchievement,
  Team,
} from '../types';

// Auth API
export const authApi = {
  login: async (credentials: LoginCredentials): Promise<AuthTokens> => {
    const response = await api.post<AuthTokens>('/auth/login', credentials);
    return response.data;
  },

  register: async (data: RegisterData): Promise<User> => {
    const response = await api.post<User>('/auth/register', data);
    return response.data;
  },

  refresh: async (refreshToken: string): Promise<AuthTokens> => {
    const response = await api.post<AuthTokens>('/auth/refresh', {
      refresh_token: refreshToken,
    });
    return response.data;
  },
};

// Users API
export const usersApi = {
  getCurrentUser: async (): Promise<User> => {
    const response = await api.get<User>('/users/me');
    return response.data;
  },

  updateCurrentUser: async (data: Partial<User>): Promise<User> => {
    const response = await api.put<User>('/users/me', data);
    return response.data;
  },

  getUserBadges: async (): Promise<UserBadge[]> => {
    const response = await api.get<UserBadge[]>('/users/me/badges');
    return response.data;
  },

  getUserAchievements: async (): Promise<UserAchievement[]> => {
    const response = await api.get<UserAchievement[]>('/users/me/achievements');
    return response.data;
  },
};

// Projects API
export const projectsApi = {
  getAll: async (skip = 0, limit = 20): Promise<Project[]> => {
    const response = await api.get<Project[]>('/projects/', {
      params: { skip, limit },
    });
    return response.data;
  },

  getMyProjects: async (): Promise<Project[]> => {
    const response = await api.get<Project[]>('/projects/my-projects');
    return response.data;
  },

  getById: async (id: number): Promise<Project> => {
    const response = await api.get<Project>(`/projects/${id}`);
    return response.data;
  },

  create: async (data: Partial<Project>): Promise<Project> => {
    const response = await api.post<Project>('/projects/', data);
    return response.data;
  },

  update: async (id: number, data: Partial<Project>): Promise<Project> => {
    const response = await api.put<Project>(`/projects/${id}`, data);
    return response.data;
  },

  publish: async (id: number): Promise<Project> => {
    const response = await api.post<Project>(`/projects/${id}/publish`);
    return response.data;
  },
};

// Quests API
export const questsApi = {
  getAll: async (skip = 0, limit = 20): Promise<Quest[]> => {
    const response = await api.get<Quest[]>('/quests/', {
      params: { skip, limit },
    });
    return response.data;
  },

  getGlobal: async (): Promise<Quest[]> => {
    const response = await api.get<Quest[]>('/quests/global');
    return response.data;
  },

  getById: async (id: number): Promise<Quest> => {
    const response = await api.get<Quest>(`/quests/${id}`);
    return response.data;
  },

  complete: async (id: number): Promise<QuestCompletion> => {
    const response = await api.post<QuestCompletion>(`/quests/${id}/complete`);
    return response.data;
  },

  getStatus: async (id: number): Promise<QuestStatus> => {
    const response = await api.get<QuestStatus>(`/quests/${id}/status`);
    return response.data;
  },

  getMyCompletions: async (): Promise<QuestCompletion[]> => {
    const response = await api.get<QuestCompletion[]>('/quests/my-completions');
    return response.data;
  },
};

// Leaderboards API
export const leaderboardsApi = {
  getGlobal: async (limit = 10): Promise<LeaderboardResponse> => {
    const response = await api.get<LeaderboardResponse>('/leaderboards/global', {
      params: { limit },
    });
    return response.data;
  },

  getWeekly: async (limit = 10): Promise<LeaderboardResponse> => {
    const response = await api.get<LeaderboardResponse>('/leaderboards/weekly', {
      params: { limit },
    });
    return response.data;
  },

  getMonthly: async (limit = 10): Promise<LeaderboardResponse> => {
    const response = await api.get<LeaderboardResponse>('/leaderboards/monthly', {
      params: { limit },
    });
    return response.data;
  },

  getTeam: async (teamId: number, limit = 10): Promise<LeaderboardResponse> => {
    const response = await api.get<LeaderboardResponse>(`/leaderboards/team/${teamId}`, {
      params: { limit },
    });
    return response.data;
  },
};

// Activity API
export const activityApi = {
  getFeed: async (page = 1, perPage = 20): Promise<ActivityFeedResponse> => {
    const response = await api.get<ActivityFeedResponse>('/activity/', {
      params: { page, per_page: perPage },
    });
    return response.data;
  },

  getMyActivity: async (page = 1, perPage = 20): Promise<ActivityFeedResponse> => {
    const response = await api.get<ActivityFeedResponse>('/activity/my-activity', {
      params: { page, per_page: perPage },
    });
    return response.data;
  },
};

// Badges API
export const badgesApi = {
  getAll: async (): Promise<Badge[]> => {
    const response = await api.get<Badge[]>('/badges/');
    return response.data;
  },
};

// Achievements API
export const achievementsApi = {
  getAll: async (): Promise<Achievement[]> => {
    const response = await api.get<Achievement[]>('/achievements/');
    return response.data;
  },
};

// Teams API
export const teamsApi = {
  getMyTeams: async (): Promise<Team[]> => {
    const response = await api.get<Team[]>('/teams/my-teams');
    return response.data;
  },

  create: async (data: Partial<Team>): Promise<Team> => {
    const response = await api.post<Team>('/teams/', data);
    return response.data;
  },
};

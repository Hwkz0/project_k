import { useQuery } from '@tanstack/react-query';
import { useAuthStore } from '../store/authStore';
import { usersApi, badgesApi, achievementsApi } from '../api';
import { Card, StatCard } from '../components/Card';
import { Badge } from '../components/Badge';
import { User, Zap, Star, Award, Trophy, Target } from 'lucide-react';

export default function ProfilePage() {
  const { user } = useAuthStore();

  // Fetch user badges
  const { data: userBadges } = useQuery({
    queryKey: ['userBadges'],
    queryFn: usersApi.getUserBadges,
  });

  // Fetch user achievements
  const { data: userAchievements } = useQuery({
    queryKey: ['userAchievements'],
    queryFn: usersApi.getUserAchievements,
  });

  // Fetch all badges
  const { data: allBadges } = useQuery({
    queryKey: ['badges'],
    queryFn: badgesApi.getAll,
  });

  // Fetch all achievements
  const { data: allAchievements } = useQuery({
    queryKey: ['achievements'],
    queryFn: achievementsApi.getAll,
  });

  const earnedBadgeIds = new Set(userBadges?.map((b) => b.badge.id) || []);
  const completedAchievementIds = new Set(
    userAchievements?.filter((a) => a.is_completed).map((a) => a.achievement.id) || []
  );

  // Calculate XP progress
  const xpForCurrentLevel = (user?.level || 1) * (user?.level || 1) * 100;
  const xpForNextLevel = ((user?.level || 1) + 1) * ((user?.level || 1) + 1) * 100;
  const xpProgress = Math.min(
    ((user?.xp || 0) - xpForCurrentLevel) / (xpForNextLevel - xpForCurrentLevel) * 100,
    100
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Profile</h1>
        <p className="text-gray-500 mt-1">View your stats and achievements</p>
      </div>

      {/* User Info Card */}
      <Card>
        <div className="flex items-start gap-6">
          {/* Avatar */}
          <div className="w-24 h-24 rounded-full bg-gradient-to-br from-primary-400 to-accent-400 flex items-center justify-center text-white text-4xl font-bold">
            {user?.username?.[0]?.toUpperCase() || 'U'}
          </div>

          {/* User Details */}
          <div className="flex-1">
            <h2 className="text-2xl font-bold text-gray-900">{user?.username}</h2>
            <p className="text-gray-500">{user?.email}</p>
            {user?.full_name && (
              <p className="text-gray-600 mt-1">{user.full_name}</p>
            )}
            {user?.bio && (
              <p className="text-gray-500 mt-2">{user.bio}</p>
            )}
            <p className="text-sm text-gray-400 mt-2">
              Member since {new Date(user?.created_at || '').toLocaleDateString()}
            </p>
          </div>
        </div>

        {/* Level Progress */}
        <div className="mt-6 pt-6 border-t border-gray-200">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-700">
              Level {user?.level || 1}
            </span>
            <span className="text-sm text-gray-500">
              {user?.xp || 0} / {xpForNextLevel} XP
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-4">
            <div
              className="bg-gradient-to-r from-primary-500 to-accent-500 h-4 rounded-full transition-all duration-500"
              style={{ width: `${xpProgress}%` }}
            />
          </div>
        </div>
      </Card>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatCard
          label="Total XP"
          value={user?.xp?.toLocaleString() || '0'}
          icon={<Zap className="w-6 h-6" />}
        />
        <StatCard
          label="Level"
          value={user?.level || 1}
          icon={<Star className="w-6 h-6" />}
        />
        <StatCard
          label="Badges"
          value={`${userBadges?.length || 0} / ${allBadges?.length || 0}`}
          icon={<Award className="w-6 h-6" />}
        />
        <StatCard
          label="Achievements"
          value={`${completedAchievementIds.size} / ${allAchievements?.length || 0}`}
          icon={<Trophy className="w-6 h-6" />}
        />
      </div>

      {/* Badges */}
      <Card title="Badges" subtitle="Earn badges by reaching milestones">
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
          {allBadges?.map((badge) => {
            const earned = earnedBadgeIds.has(badge.id);
            return (
              <div
                key={badge.id}
                className={`p-4 rounded-lg border text-center transition-colors ${
                  earned
                    ? 'bg-accent-50 border-accent-200'
                    : 'bg-gray-50 border-gray-200 opacity-50'
                }`}
              >
                <div className="text-3xl mb-2">{badge.icon}</div>
                <p className={`text-sm font-medium ${earned ? 'text-accent-800' : 'text-gray-500'}`}>
                  {badge.name}
                </p>
                {earned && (
                  <Badge variant="accent" size="sm">
                    Earned
                  </Badge>
                )}
              </div>
            );
          })}
          {!allBadges?.length && (
            <p className="col-span-full text-center text-gray-500 py-4">
              No badges available
            </p>
          )}
        </div>
      </Card>

      {/* Achievements */}
      <Card title="Achievements" subtitle="Unlock achievements by completing challenges">
        <div className="space-y-3">
          {allAchievements?.map((achievement) => {
            const completed = completedAchievementIds.has(achievement.id);
            return (
              <div
                key={achievement.id}
                className={`flex items-center gap-4 p-4 rounded-lg border ${
                  completed
                    ? 'bg-green-50 border-green-200'
                    : 'bg-gray-50 border-gray-200 opacity-60'
                }`}
              >
                <div className="text-2xl">{achievement.icon}</div>
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <p className={`font-medium ${completed ? 'text-green-800' : 'text-gray-700'}`}>
                      {achievement.name}
                    </p>
                    {achievement.is_secret && !completed && (
                      <Badge variant="gray">Secret</Badge>
                    )}
                  </div>
                  <p className={`text-sm ${completed ? 'text-green-600' : 'text-gray-500'}`}>
                    {achievement.description}
                  </p>
                </div>
                <div className="text-right">
                  {completed ? (
                    <Badge variant="success">Completed</Badge>
                  ) : (
                    <Badge variant="accent">+{achievement.xp_reward} XP</Badge>
                  )}
                </div>
              </div>
            );
          })}
          {!allAchievements?.length && (
            <p className="text-center text-gray-500 py-4">
              No achievements available
            </p>
          )}
        </div>
      </Card>
    </div>
  );
}

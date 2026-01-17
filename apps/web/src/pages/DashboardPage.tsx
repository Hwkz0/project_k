import { useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useAuthStore } from '../store/authStore';
import { usersApi, projectsApi, questsApi, leaderboardsApi } from '../api';
import { Card, StatCard } from '../components/Card';
import { Badge, DifficultyBadge } from '../components/Badge';
import { 
  Zap, 
  Target, 
  FolderKanban, 
  Trophy,
  ArrowRight,
  Star,
} from 'lucide-react';
import { Link } from 'react-router-dom';

export default function DashboardPage() {
  const { user, setUser } = useAuthStore();

  // Fetch user data
  const { data: currentUser } = useQuery({
    queryKey: ['currentUser'],
    queryFn: usersApi.getCurrentUser,
  });

  // Fetch projects
  const { data: projects } = useQuery({
    queryKey: ['myProjects'],
    queryFn: projectsApi.getMyProjects,
  });

  // Fetch quests
  const { data: quests } = useQuery({
    queryKey: ['quests'],
    queryFn: () => questsApi.getAll(0, 5),
  });

  // Fetch leaderboard
  const { data: leaderboard } = useQuery({
    queryKey: ['leaderboard', 'global'],
    queryFn: () => leaderboardsApi.getGlobal(5),
  });

  // Update user in store when fetched
  useEffect(() => {
    if (currentUser) {
      setUser(currentUser);
    }
  }, [currentUser, setUser]);

  // Calculate XP progress to next level
  const xpForCurrentLevel = (user?.level || 1) * (user?.level || 1) * 100;
  const xpForNextLevel = ((user?.level || 1) + 1) * ((user?.level || 1) + 1) * 100;
  const xpProgress = Math.min(
    ((user?.xp || 0) - xpForCurrentLevel) / (xpForNextLevel - xpForCurrentLevel) * 100,
    100
  );

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">
          Welcome back, {user?.username || 'Developer'}! 👋
        </h1>
        <p className="text-gray-500 mt-1">
          Here's what's happening with your AI projects
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          label="Total XP"
          value={user?.xp?.toLocaleString() || '0'}
          icon={<Zap className="w-6 h-6" />}
        />
        <StatCard
          label="Current Level"
          value={user?.level || 1}
          icon={<Star className="w-6 h-6" />}
        />
        <StatCard
          label="Projects"
          value={projects?.length || 0}
          icon={<FolderKanban className="w-6 h-6" />}
        />
        <StatCard
          label="Quests Completed"
          value="0"
          icon={<Target className="w-6 h-6" />}
        />
      </div>

      {/* Level Progress */}
      <Card>
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-medium text-gray-700">
            Level {user?.level || 1} Progress
          </span>
          <span className="text-sm text-gray-500">
            {user?.xp || 0} / {xpForNextLevel} XP
          </span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-3">
          <div
            className="bg-gradient-to-r from-primary-500 to-accent-500 h-3 rounded-full transition-all duration-500"
            style={{ width: `${xpProgress}%` }}
          />
        </div>
        <p className="text-xs text-gray-500 mt-2">
          {xpForNextLevel - (user?.xp || 0)} XP until level {(user?.level || 1) + 1}
        </p>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Available Quests */}
        <Card
          title="Available Quests"
          subtitle="Complete quests to earn XP"
          action={
            <Link to="/quests" className="text-sm text-primary-600 hover:text-primary-700 flex items-center gap-1">
              View all <ArrowRight className="w-4 h-4" />
            </Link>
          }
        >
          <div className="space-y-3">
            {quests?.slice(0, 4).map((quest) => (
              <div
                key={quest.id}
                className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
              >
                <div className="flex-1 min-w-0">
                  <p className="font-medium text-gray-900 truncate">{quest.title}</p>
                  <div className="flex items-center gap-2 mt-1">
                    <DifficultyBadge difficulty={quest.difficulty} />
                    <span className="text-xs text-gray-500">{quest.category}</span>
                  </div>
                </div>
                <div className="text-right ml-4">
                  <Badge variant="accent">+{quest.xp_reward} XP</Badge>
                </div>
              </div>
            ))}
            {!quests?.length && (
              <p className="text-gray-500 text-center py-4">No quests available</p>
            )}
          </div>
        </Card>

        {/* Leaderboard Preview */}
        <Card
          title="Top Players"
          subtitle="Global leaderboard"
          action={
            <Link to="/leaderboards" className="text-sm text-primary-600 hover:text-primary-700 flex items-center gap-1">
              View all <ArrowRight className="w-4 h-4" />
            </Link>
          }
        >
          <div className="space-y-3">
            {leaderboard?.entries.map((entry, index) => (
              <div
                key={entry.user_id}
                className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg"
              >
                <div className={`
                  w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm
                  ${index === 0 ? 'bg-yellow-100 text-yellow-700' : ''}
                  ${index === 1 ? 'bg-gray-100 text-gray-700' : ''}
                  ${index === 2 ? 'bg-orange-100 text-orange-700' : ''}
                  ${index > 2 ? 'bg-gray-100 text-gray-600' : ''}
                `}>
                  {entry.rank}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="font-medium text-gray-900 truncate">
                    {entry.username}
                    {entry.user_id === user?.id && (
                      <span className="text-primary-600 ml-1">(you)</span>
                    )}
                  </p>
                  <p className="text-xs text-gray-500">Level {entry.level}</p>
                </div>
                <div className="text-right">
                  <p className="font-semibold text-gray-900">{entry.xp.toLocaleString()}</p>
                  <p className="text-xs text-gray-500">XP</p>
                </div>
              </div>
            ))}
            {!leaderboard?.entries.length && (
              <p className="text-gray-500 text-center py-4">No leaderboard data</p>
            )}
          </div>
        </Card>
      </div>
    </div>
  );
}

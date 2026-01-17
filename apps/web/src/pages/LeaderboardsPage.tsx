import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { leaderboardsApi } from '../api';
import { Card } from '../components/Card';
import { useAuthStore } from '../store/authStore';
import { Trophy, Medal, Award, Crown } from 'lucide-react';

type LeaderboardTab = 'global' | 'weekly' | 'monthly';

export default function LeaderboardsPage() {
  const [activeTab, setActiveTab] = useState<LeaderboardTab>('global');
  const { user } = useAuthStore();

  // Fetch leaderboards
  const { data: globalLeaderboard, isLoading: loadingGlobal } = useQuery({
    queryKey: ['leaderboard', 'global'],
    queryFn: () => leaderboardsApi.getGlobal(20),
  });

  const { data: weeklyLeaderboard, isLoading: loadingWeekly } = useQuery({
    queryKey: ['leaderboard', 'weekly'],
    queryFn: () => leaderboardsApi.getWeekly(20),
  });

  const { data: monthlyLeaderboard, isLoading: loadingMonthly } = useQuery({
    queryKey: ['leaderboard', 'monthly'],
    queryFn: () => leaderboardsApi.getMonthly(20),
  });

  const leaderboards = {
    global: globalLeaderboard,
    weekly: weeklyLeaderboard,
    monthly: monthlyLeaderboard,
  };

  const loading = {
    global: loadingGlobal,
    weekly: loadingWeekly,
    monthly: loadingMonthly,
  };

  const activeLeaderboard = leaderboards[activeTab];
  const isLoading = loading[activeTab];

  const getRankIcon = (rank: number) => {
    switch (rank) {
      case 1:
        return <Crown className="w-5 h-5 text-yellow-500" />;
      case 2:
        return <Medal className="w-5 h-5 text-gray-400" />;
      case 3:
        return <Award className="w-5 h-5 text-orange-500" />;
      default:
        return null;
    }
  };

  const getRankStyle = (rank: number) => {
    switch (rank) {
      case 1:
        return 'bg-gradient-to-r from-yellow-50 to-yellow-100 border-yellow-200';
      case 2:
        return 'bg-gradient-to-r from-gray-50 to-gray-100 border-gray-200';
      case 3:
        return 'bg-gradient-to-r from-orange-50 to-orange-100 border-orange-200';
      default:
        return 'bg-white border-gray-200';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Leaderboards</h1>
        <p className="text-gray-500 mt-1">See how you rank against other developers</p>
      </div>

      {/* Tabs */}
      <div className="flex gap-2">
        {(['global', 'weekly', 'monthly'] as const).map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              activeTab === tab
                ? 'bg-primary-600 text-white'
                : 'bg-white text-gray-600 hover:bg-gray-50 border border-gray-200'
            }`}
          >
            {tab.charAt(0).toUpperCase() + tab.slice(1)}
          </button>
        ))}
      </div>

      {/* Leaderboard */}
      <Card>
        <div className="flex items-center gap-2 mb-6">
          <Trophy className="w-6 h-6 text-primary-600" />
          <h2 className="text-xl font-bold text-gray-900">
            {activeTab.charAt(0).toUpperCase() + activeTab.slice(1)} Rankings
          </h2>
          {activeLeaderboard?.period_key && (
            <span className="text-sm text-gray-500 ml-2">
              ({activeLeaderboard.period_key})
            </span>
          )}
        </div>

        {isLoading ? (
          <div className="space-y-3">
            {[1, 2, 3, 4, 5].map((i) => (
              <div key={i} className="h-16 bg-gray-100 rounded-lg animate-pulse" />
            ))}
          </div>
        ) : activeLeaderboard?.entries.length ? (
          <div className="space-y-3">
            {activeLeaderboard.entries.map((entry) => {
              const isCurrentUser = entry.user_id === user?.id;
              return (
                <div
                  key={entry.user_id}
                  className={`flex items-center gap-4 p-4 rounded-lg border transition-colors ${
                    isCurrentUser
                      ? 'bg-primary-50 border-primary-200 ring-2 ring-primary-500'
                      : getRankStyle(entry.rank)
                  }`}
                >
                  {/* Rank */}
                  <div className="w-12 flex items-center justify-center">
                    {getRankIcon(entry.rank) || (
                      <span className="text-lg font-bold text-gray-400">
                        #{entry.rank}
                      </span>
                    )}
                  </div>

                  {/* Avatar */}
                  <div className="w-12 h-12 rounded-full bg-gradient-to-br from-primary-400 to-accent-400 flex items-center justify-center text-white font-bold text-lg">
                    {entry.username[0].toUpperCase()}
                  </div>

                  {/* User info */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <p className="font-semibold text-gray-900 truncate">
                        {entry.username}
                      </p>
                      {isCurrentUser && (
                        <span className="px-2 py-0.5 bg-primary-100 text-primary-700 text-xs font-medium rounded-full">
                          You
                        </span>
                      )}
                    </div>
                    <p className="text-sm text-gray-500">Level {entry.level}</p>
                  </div>

                  {/* XP */}
                  <div className="text-right">
                    <p className="text-xl font-bold text-gray-900">
                      {entry.xp.toLocaleString()}
                    </p>
                    <p className="text-sm text-gray-500">XP</p>
                  </div>
                </div>
              );
            })}
          </div>
        ) : (
          <div className="text-center py-12 text-gray-500">
            <Trophy className="w-12 h-12 mx-auto mb-4 text-gray-300" />
            <p>No leaderboard data available</p>
            <p className="text-sm mt-1">Complete quests to appear on the leaderboard!</p>
          </div>
        )}
      </Card>
    </div>
  );
}

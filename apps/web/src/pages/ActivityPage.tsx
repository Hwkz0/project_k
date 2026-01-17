import { useQuery } from '@tanstack/react-query';
import { activityApi } from '../api';
import { Card, EmptyState } from '../components/Card';
import { Badge } from '../components/Badge';
import { 
  Activity as ActivityIcon,
  Trophy,
  Swords,
  FolderKanban,
  Users,
  Star,
  Zap,
  Award,
} from 'lucide-react';
import type { ActivityEvent, ActivityType } from '../types';

const activityIcons: Record<ActivityType, React.ReactNode> = {
  user_registered: <Star className="w-4 h-4" />,
  user_level_up: <Zap className="w-4 h-4" />,
  quest_completed: <Swords className="w-4 h-4" />,
  quest_created: <Swords className="w-4 h-4" />,
  project_created: <FolderKanban className="w-4 h-4" />,
  project_published: <FolderKanban className="w-4 h-4" />,
  project_updated: <FolderKanban className="w-4 h-4" />,
  team_created: <Users className="w-4 h-4" />,
  team_joined: <Users className="w-4 h-4" />,
  badge_earned: <Award className="w-4 h-4" />,
  achievement_unlocked: <Trophy className="w-4 h-4" />,
  xp_gained: <Zap className="w-4 h-4" />,
  leaderboard_rank_up: <Trophy className="w-4 h-4" />,
};

const activityColors: Record<ActivityType, string> = {
  user_registered: 'bg-blue-100 text-blue-600',
  user_level_up: 'bg-yellow-100 text-yellow-600',
  quest_completed: 'bg-green-100 text-green-600',
  quest_created: 'bg-purple-100 text-purple-600',
  project_created: 'bg-indigo-100 text-indigo-600',
  project_published: 'bg-green-100 text-green-600',
  project_updated: 'bg-gray-100 text-gray-600',
  team_created: 'bg-orange-100 text-orange-600',
  team_joined: 'bg-orange-100 text-orange-600',
  badge_earned: 'bg-pink-100 text-pink-600',
  achievement_unlocked: 'bg-yellow-100 text-yellow-600',
  xp_gained: 'bg-accent-100 text-accent-600',
  leaderboard_rank_up: 'bg-primary-100 text-primary-600',
};

function formatTimeAgo(date: string) {
  const seconds = Math.floor((Date.now() - new Date(date).getTime()) / 1000);
  
  if (seconds < 60) return 'just now';
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
  if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
  if (seconds < 604800) return `${Math.floor(seconds / 86400)}d ago`;
  return new Date(date).toLocaleDateString();
}

function ActivityItem({ activity }: { activity: ActivityEvent }) {
  return (
    <div className="flex gap-4 p-4 hover:bg-gray-50 rounded-lg transition-colors">
      {/* Icon */}
      <div className={`p-2 rounded-lg ${activityColors[activity.event_type]}`}>
        {activityIcons[activity.event_type]}
      </div>

      {/* Content */}
      <div className="flex-1 min-w-0">
        <p className="text-gray-900">
          <span className="font-medium">{activity.username}</span>{' '}
          {activity.title.replace(activity.username, '').trim()}
        </p>
        {activity.description && (
          <p className="text-sm text-gray-500 mt-0.5">{activity.description}</p>
        )}
        <div className="flex items-center gap-2 mt-1">
          <span className="text-xs text-gray-400">
            {formatTimeAgo(activity.created_at)}
          </span>
          {activity.xp_amount > 0 && (
            <Badge variant="accent" size="sm">
              +{activity.xp_amount} XP
            </Badge>
          )}
        </div>
      </div>
    </div>
  );
}

export default function ActivityPage() {
  // Fetch activity feed
  const { data: activityFeed, isLoading } = useQuery({
    queryKey: ['activity'],
    queryFn: () => activityApi.getFeed(1, 50),
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Activity Feed</h1>
        <p className="text-gray-500 mt-1">See what's happening in the community</p>
      </div>

      {/* Activity List */}
      <Card>
        {isLoading ? (
          <div className="space-y-4">
            {[1, 2, 3, 4, 5].map((i) => (
              <div key={i} className="flex gap-4 animate-pulse">
                <div className="w-10 h-10 bg-gray-200 rounded-lg" />
                <div className="flex-1">
                  <div className="h-4 bg-gray-200 rounded w-3/4 mb-2" />
                  <div className="h-3 bg-gray-200 rounded w-1/4" />
                </div>
              </div>
            ))}
          </div>
        ) : activityFeed?.items.length ? (
          <div className="divide-y divide-gray-100">
            {activityFeed.items.map((activity) => (
              <ActivityItem key={activity.id} activity={activity} />
            ))}
          </div>
        ) : (
          <EmptyState
            icon={<ActivityIcon className="w-12 h-12" />}
            title="No activity yet"
            description="Activity will appear here as you and others complete quests, earn badges, and publish projects"
          />
        )}
      </Card>
    </div>
  );
}

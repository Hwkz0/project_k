import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { questsApi } from '../api';
import { Card, EmptyState } from '../components/Card';
import { Button } from '../components/Button';
import { Badge, DifficultyBadge } from '../components/Badge';
import { Swords, CheckCircle, Clock, Zap } from 'lucide-react';
import type { Quest } from '../types';

export default function QuestsPage() {
  const queryClient = useQueryClient();

  // Fetch quests
  const { data: quests, isLoading } = useQuery({
    queryKey: ['quests'],
    queryFn: () => questsApi.getAll(0, 50),
  });

  // Fetch completions
  const { data: completions } = useQuery({
    queryKey: ['myCompletions'],
    queryFn: questsApi.getMyCompletions,
  });

  // Complete quest mutation
  const completeMutation = useMutation({
    mutationFn: questsApi.complete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['quests'] });
      queryClient.invalidateQueries({ queryKey: ['myCompletions'] });
      queryClient.invalidateQueries({ queryKey: ['currentUser'] });
    },
  });

  const completedQuestIds = new Set(completions?.map((c) => c.quest_id) || []);

  const isCompleted = (questId: number) => completedQuestIds.has(questId);

  // Group quests by category
  const questsByCategory = quests?.reduce((acc, quest) => {
    if (!acc[quest.category]) {
      acc[quest.category] = [];
    }
    acc[quest.category].push(quest);
    return acc;
  }, {} as Record<string, Quest[]>);

  const categoryLabels: Record<string, string> = {
    setup: '🔧 Setup',
    development: '💻 Development',
    testing: '🧪 Testing',
    deployment: '🚀 Deployment',
    documentation: '📝 Documentation',
    community: '👥 Community',
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Quests</h1>
        <p className="text-gray-500 mt-1">
          Complete quests to earn XP and level up your skills
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card className="flex items-center gap-4">
          <div className="p-3 bg-primary-50 rounded-lg">
            <Swords className="w-6 h-6 text-primary-600" />
          </div>
          <div>
            <p className="text-2xl font-bold text-gray-900">{quests?.length || 0}</p>
            <p className="text-sm text-gray-500">Total Quests</p>
          </div>
        </Card>
        <Card className="flex items-center gap-4">
          <div className="p-3 bg-green-50 rounded-lg">
            <CheckCircle className="w-6 h-6 text-green-600" />
          </div>
          <div>
            <p className="text-2xl font-bold text-gray-900">{completions?.length || 0}</p>
            <p className="text-sm text-gray-500">Completed</p>
          </div>
        </Card>
        <Card className="flex items-center gap-4">
          <div className="p-3 bg-accent-50 rounded-lg">
            <Zap className="w-6 h-6 text-accent-600" />
          </div>
          <div>
            <p className="text-2xl font-bold text-gray-900">
              {completions?.reduce((sum, c) => sum + c.xp_earned, 0) || 0}
            </p>
            <p className="text-sm text-gray-500">XP Earned</p>
          </div>
        </Card>
      </div>

      {/* Quests by Category */}
      {isLoading ? (
        <div className="space-y-6">
          {[1, 2, 3].map((i) => (
            <div key={i} className="card animate-pulse">
              <div className="h-6 bg-gray-200 rounded w-1/4 mb-4" />
              <div className="space-y-3">
                <div className="h-16 bg-gray-100 rounded" />
                <div className="h-16 bg-gray-100 rounded" />
              </div>
            </div>
          ))}
        </div>
      ) : questsByCategory && Object.keys(questsByCategory).length > 0 ? (
        <div className="space-y-6">
          {Object.entries(questsByCategory).map(([category, categoryQuests]) => (
            <Card key={category} title={categoryLabels[category] || category}>
              <div className="space-y-3">
                {categoryQuests.map((quest) => {
                  const completed = isCompleted(quest.id);
                  return (
                    <div
                      key={quest.id}
                      className={`flex items-center gap-4 p-4 rounded-lg border transition-colors ${
                        completed
                          ? 'bg-green-50 border-green-200'
                          : 'bg-gray-50 border-gray-200 hover:border-primary-300'
                      }`}
                    >
                      <div className={`flex-shrink-0 ${completed ? 'text-green-500' : 'text-gray-400'}`}>
                        {completed ? (
                          <CheckCircle className="w-6 h-6" />
                        ) : (
                          <Clock className="w-6 h-6" />
                        )}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-1">
                          <h3 className={`font-medium ${completed ? 'text-green-800' : 'text-gray-900'}`}>
                            {quest.title}
                          </h3>
                          <DifficultyBadge difficulty={quest.difficulty} />
                          {quest.is_repeatable && (
                            <Badge variant="gray">Repeatable</Badge>
                          )}
                        </div>
                        <p className={`text-sm ${completed ? 'text-green-600' : 'text-gray-500'}`}>
                          {quest.description}
                        </p>
                      </div>
                      <div className="flex items-center gap-3">
                        <Badge variant="accent" size="md">
                          +{quest.xp_reward} XP
                        </Badge>
                        {!completed || quest.is_repeatable ? (
                          <Button
                            size="sm"
                            onClick={() => completeMutation.mutate(quest.id)}
                            isLoading={completeMutation.isPending}
                          >
                            Complete
                          </Button>
                        ) : (
                          <span className="text-sm text-green-600 font-medium">
                            ✓ Done
                          </span>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            </Card>
          ))}
        </div>
      ) : (
        <Card>
          <EmptyState
            icon={<Swords className="w-12 h-12" />}
            title="No quests available"
            description="Check back later for new quests to complete"
          />
        </Card>
      )}
    </div>
  );
}

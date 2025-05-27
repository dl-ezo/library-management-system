import { useState, useEffect } from 'react';
import { fetchFeedbacks } from '../lib/api';
import { Feedback } from '../types/feedback';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { ExternalLink } from 'lucide-react';
import { format } from 'date-fns';

interface FeedbackListProps {
  refreshTrigger?: number;
}

export function FeedbackList({ refreshTrigger }: FeedbackListProps) {
  const [feedbacks, setFeedbacks] = useState<Feedback[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadFeedbacks();
  }, [refreshTrigger]);

  const loadFeedbacks = async () => {
    setLoading(true);
    try {
      const data = await fetchFeedbacks();
      setFeedbacks(data);
    } catch (error) {
      console.error('Failed to fetch feedbacks:', error);
    } finally {
      setLoading(false);
    }
  };

  const getCategoryBadgeColor = (category: string) => {
    switch (category) {
      case 'bug':
        return 'bg-red-100 text-red-800';
      case 'feature':
        return 'bg-blue-100 text-blue-800';
      case 'improvement':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getCategoryLabel = (category: string) => {
    switch (category) {
      case 'bug':
        return 'バグ報告';
      case 'feature':
        return '機能要望';
      case 'improvement':
        return '改善提案';
      default:
        return category;
    }
  };

  if (loading) {
    return (
      <Card>
        <CardContent className="p-6">
          <div className="text-center">読み込み中...</div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>フィードバック一覧</CardTitle>
      </CardHeader>
      <CardContent>
        {feedbacks.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            まだフィードバックがありません
          </div>
        ) : (
          <div className="space-y-4">
            {feedbacks.map((feedback) => (
              <div key={feedback.id} className="border rounded-lg p-4 hover:bg-gray-50">
                <div className="flex items-start justify-between mb-2">
                  <h3 className="font-semibold text-lg">{feedback.title}</h3>
                  <Badge className={getCategoryBadgeColor(feedback.category)}>
                    {getCategoryLabel(feedback.category)}
                  </Badge>
                </div>
                
                <p className="text-gray-700 mb-3 whitespace-pre-wrap">
                  {feedback.description}
                </p>
                
                <div className="flex items-center justify-between text-sm text-gray-500">
                  <div>
                    <span>投稿者: {feedback.author_name}</span>
                    <span className="mx-2">•</span>
                    <span>作成日: {format(new Date(feedback.created_at), 'yyyy/MM/dd HH:mm')}</span>
                  </div>
                  
                  {feedback.github_issue_url && (
                    <a
                      href={feedback.github_issue_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1 text-blue-600 hover:text-blue-800 underline"
                    >
                      GitHub Issue <ExternalLink className="h-3 w-3" />
                    </a>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
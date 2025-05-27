import { useState, useEffect } from 'react';
import { createFeedback, fetchFeedbackCategories } from '../lib/api';
import { FeedbackCreate, FeedbackCategory } from '../types/feedback';
import { Input } from './ui/input';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Textarea } from './ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Alert, AlertDescription } from './ui/alert';
import { ExternalLink } from 'lucide-react';

interface FeedbackFormProps {
  onSuccess?: () => void;
}

export function FeedbackForm({ onSuccess }: FeedbackFormProps) {
  const [formData, setFormData] = useState<FeedbackCreate>({
    title: '',
    description: '',
    category: 'improvement',
    author_name: ''
  });
  const [categories, setCategories] = useState<FeedbackCategory[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<{ message: string; issueUrl?: string } | null>(null);

  useEffect(() => {
    loadCategories();
  }, []);

  const loadCategories = async () => {
    try {
      const data = await fetchFeedbackCategories();
      setCategories(data);
    } catch (error) {
      console.error('Failed to load categories:', error);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(null);

    try {
      const result = await createFeedback(formData);
      
      const successMessage = result.github_issue_url 
        ? 'フィードバックを送信し、GitHub Issueを作成しました！'
        : 'フィードバックを送信しました！';
      
      setSuccess({
        message: successMessage,
        issueUrl: result.github_issue_url || undefined
      });
      
      // フォームをリセット
      setFormData({
        title: '',
        description: '',
        category: 'improvement',
        author_name: ''
      });
      
      onSuccess?.();
    } catch (error) {
      setError(error instanceof Error ? error.message : 'フィードバックの送信に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (field: keyof FeedbackCreate, value: string) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  return (
    <Card className="w-full max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle>フィードバックを送信</CardTitle>
      </CardHeader>
      <CardContent>
        {error && (
          <Alert className="mb-4 border-red-200 text-red-800">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}
        
        {success && (
          <Alert className="mb-4 border-green-200 text-green-800">
            <AlertDescription>
              {success.message}
              {success.issueUrl && (
                <div className="mt-2">
                  <a 
                    href={success.issueUrl} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-1 text-blue-600 hover:text-blue-800 underline"
                  >
                    GitHub Issueを確認 <ExternalLink className="h-3 w-3" />
                  </a>
                </div>
              )}
            </AlertDescription>
          </Alert>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="author_name" className="block text-sm font-medium mb-2">
              お名前 *
            </label>
            <Input
              id="author_name"
              value={formData.author_name}
              onChange={(e) => handleChange('author_name', e.target.value)}
              placeholder="お名前を入力してください"
              required
            />
          </div>

          <div>
            <label htmlFor="title" className="block text-sm font-medium mb-2">
              タイトル *
            </label>
            <Input
              id="title"
              value={formData.title}
              onChange={(e) => handleChange('title', e.target.value)}
              placeholder="フィードバックのタイトルを入力してください"
              required
            />
          </div>

          <div>
            <label htmlFor="category" className="block text-sm font-medium mb-2">
              カテゴリ *
            </label>
            <Select value={formData.category} onValueChange={(value) => handleChange('category', value)}>
              <SelectTrigger>
                <SelectValue placeholder="カテゴリを選択してください" />
              </SelectTrigger>
              <SelectContent>
                {categories.map((category) => (
                  <SelectItem key={category.value} value={category.value}>
                    {category.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div>
            <label htmlFor="description" className="block text-sm font-medium mb-2">
              詳細 *
            </label>
            <Textarea
              id="description"
              value={formData.description}
              onChange={(e) => handleChange('description', e.target.value)}
              placeholder="詳細な説明を入力してください"
              rows={6}
              required
            />
          </div>

          <Button type="submit" disabled={loading} className="w-full">
            {loading ? '送信中...' : 'フィードバックを送信'}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
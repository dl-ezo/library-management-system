import { useState } from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Textarea } from './ui/textarea';
import { Loader2, ExternalLink, Sparkles } from 'lucide-react';
import { getBookRecommendations } from '../lib/api';
import { BookRecommendation } from '../types/recommendation';
import { Alert, AlertDescription } from './ui/alert';

export const BookRecommendations = () => {
  const [query, setQuery] = useState('');
  const [recommendations, setRecommendations] = useState<BookRecommendation[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setIsLoading(true);
    setError(null);
    setRecommendations([]);

    try {
      const response = await getBookRecommendations(query.trim());
      setRecommendations(response.recommendations);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'おすすめ書籍の取得に失敗しました');
    } finally {
      setIsLoading(false);
    }
  };

  const exampleQueries = [
    'プログラミング初心者向けの本が欲しい',
    '機械学習について学びたい',
    '自己啓発やビジネススキルに関する本',
    'ミステリー小説でおすすめはありますか',
    '歴史に関する面白い本を探している'
  ];

  const handleExampleClick = (example: string) => {
    setQuery(example);
  };

  return (
    <div className="space-y-6">
      <div className="text-center">
        <div className="flex items-center justify-center gap-2 mb-2">
          <Sparkles className="h-6 w-6 text-blue-500" />
          <h2 className="text-2xl font-bold">AI書籍おすすめ</h2>
        </div>
        <p className="text-muted-foreground">
          どんな本をお探しですか？自然言語で入力してください。AIがあなたにぴったりの書籍を推薦します。
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <Textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="例：プログラミングを学びたい初心者向けの本が欲しい、ビジネススキルを向上させる本を探している..."
            className="min-h-[100px]"
            disabled={isLoading}
          />
        </div>
        
        <div className="flex flex-wrap gap-2">
          <span className="text-sm text-muted-foreground">例：</span>
          {exampleQueries.map((example, index) => (
            <Button
              key={index}
              type="button"
              variant="outline"
              size="sm"
              onClick={() => handleExampleClick(example)}
              disabled={isLoading}
              className="text-xs"
            >
              {example}
            </Button>
          ))}
        </div>

        <Button type="submit" disabled={isLoading || !query.trim()} className="w-full">
          {isLoading ? (
            <>
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              AIが書籍を検索中...
            </>
          ) : (
            <>
              <Sparkles className="mr-2 h-4 w-4" />
              おすすめ書籍を取得
            </>
          )}
        </Button>
      </form>

      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {recommendations.length > 0 && (
        <div className="space-y-4">
          <h3 className="text-lg font-semibold">おすすめ書籍</h3>
          <div className="grid gap-4">
            {recommendations.map((book, index) => (
              <Card key={index} className="hover:shadow-md transition-shadow">
                <CardHeader>
                  <div className="flex justify-between items-start gap-4">
                    <div className="flex-1">
                      <CardTitle className="text-lg">{book.title}</CardTitle>
                      <CardDescription className="text-base mt-1">
                        著者: {book.author}
                      </CardDescription>
                    </div>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => window.open(book.amazon_url, '_blank')}
                      className="shrink-0"
                    >
                      <ExternalLink className="mr-2 h-4 w-4" />
                      Amazon
                    </Button>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="bg-muted p-3 rounded-md">
                    <p className="text-sm font-medium mb-1">おすすめポイント:</p>
                    <p className="text-sm text-muted-foreground">
                      {book.recommendation_reason}
                    </p>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
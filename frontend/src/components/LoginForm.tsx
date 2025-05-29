import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Alert, AlertDescription } from './ui/alert';

interface LoginFormProps {
  onSwitchToRegister?: () => void;
}

export function LoginForm({ onSwitchToRegister }: LoginFormProps) {
  const { login } = useAuth();
  const [username, setUsername] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!username.trim()) return;

    setLoading(true);
    setError(null);

    try {
      await login({ username: username.trim() });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'ログインに失敗しました');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader>
        <CardTitle>ログイン</CardTitle>
      </CardHeader>
      <CardContent>
        {error && (
          <Alert className="mb-4 border-red-200 text-red-800">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="username" className="block text-sm font-medium mb-2">
              ユーザー名
            </label>
            <Input
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="ユーザー名を入力してください"
              required
            />
          </div>

          <Button type="submit" disabled={loading} className="w-full">
            {loading ? 'ログイン中...' : 'ログイン'}
          </Button>
        </form>

        {onSwitchToRegister && (
          <div className="mt-4 text-center">
            <p className="text-sm text-gray-600">
              アカウントをお持ちでない方は{' '}
              <button
                type="button"
                onClick={onSwitchToRegister}
                className="text-blue-600 hover:text-blue-800 underline"
              >
                新規登録
              </button>
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
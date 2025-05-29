import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Alert, AlertDescription } from './ui/alert';

interface RegisterFormProps {
  onSwitchToLogin?: () => void;
}

export function RegisterForm({ onSwitchToLogin }: RegisterFormProps) {
  const { register } = useAuth();
  const [formData, setFormData] = useState({
    username: '',
    display_name: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.username.trim() || !formData.display_name.trim()) return;

    setLoading(true);
    setError(null);

    try {
      await register({
        username: formData.username.trim(),
        display_name: formData.display_name.trim()
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'ユーザー登録に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (field: string, value: string) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader>
        <CardTitle>新規登録</CardTitle>
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
              ユーザー名 *
            </label>
            <Input
              id="username"
              value={formData.username}
              onChange={(e) => handleChange('username', e.target.value)}
              placeholder="ユーザー名を入力してください"
              required
            />
          </div>

          <div>
            <label htmlFor="display_name" className="block text-sm font-medium mb-2">
              表示名 *
            </label>
            <Input
              id="display_name"
              value={formData.display_name}
              onChange={(e) => handleChange('display_name', e.target.value)}
              placeholder="表示名を入力してください"
              required
            />
          </div>

          <Button type="submit" disabled={loading} className="w-full">
            {loading ? '登録中...' : 'アカウント作成'}
          </Button>
        </form>

        {onSwitchToLogin && (
          <div className="mt-4 text-center">
            <p className="text-sm text-gray-600">
              すでにアカウントをお持ちの方は{' '}
              <button
                type="button"
                onClick={onSwitchToLogin}
                className="text-blue-600 hover:text-blue-800 underline"
              >
                ログイン
              </button>
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
import React from 'react';
import { useState } from 'react';
import { createBook } from '../lib/api';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';

interface AddBookFormProps {
  onBookAdded: () => void;
}

export function AddBookForm({ onBookAdded }: AddBookFormProps) {
  const [title, setTitle] = useState('');
  const [author, setAuthor] = useState(''); // Added author state
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;

    setLoading(true);
    try {
      // Updated createBook call to include author
      await createBook({ title: title.trim(), author: author.trim() ? author.trim() : undefined });
      setTitle('');
      setAuthor(''); // Reset author state
      onBookAdded();
    } catch (error) {
      console.error('Failed to add book:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>新しい本を登録</CardTitle>
      </CardHeader>
      <CardContent>
        {/* Changed to flex-col for main form elements */}
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          {/* Wrapper for inputs */}
          <div className="flex flex-col gap-2">
            <Input
              placeholder="タイトル"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
            />
            <Input
              placeholder="著者 (任意)"
              value={author}
              onChange={(e) => setAuthor(e.target.value)}
            />
          </div>
          <Button type="submit" disabled={loading}>
            {loading ? '登録中...' : '登録'}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}

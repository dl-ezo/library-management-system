import React from 'react';
import { useState } from 'react';
import { borrowBook } from '../lib/api';
import { useAuth } from '../contexts/AuthContext';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';

interface BorrowBookFormProps {
  bookId: number;
  onBookBorrowed: () => void;
}

export function BorrowBookForm({ bookId, onBookBorrowed }: BorrowBookFormProps) {
  const { user } = useAuth();
  const [returnDate, setReturnDate] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!returnDate || !user) return;

    setLoading(true);
    try {
      await borrowBook(bookId, user.display_name, returnDate);
      setReturnDate('');
      onBookBorrowed();
    } catch (error) {
      console.error('Failed to borrow book:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>本を借りる</CardTitle>
      </CardHeader>
      <CardContent>
        {user && (
          <div className="mb-4 p-3 bg-blue-50 rounded-lg">
            <p className="text-sm text-blue-700">
              借りる人: <span className="font-semibold">{user.display_name}</span>
            </p>
          </div>
        )}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="returnDate" className="block text-sm font-medium mb-2">
              返却予定日
            </label>
            <Input
              id="returnDate"
              type="date"
              value={returnDate}
              onChange={(e) => setReturnDate(e.target.value)}
              required
            />
          </div>
          <Button type="submit" disabled={loading}>
            {loading ? '処理中...' : '借りる'}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}

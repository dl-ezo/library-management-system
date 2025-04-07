import React from 'react';
import { useState } from 'react';
import { borrowBook } from '../lib/api';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';

interface BorrowBookFormProps {
  bookId: number;
  onBookBorrowed: () => void;
}

export function BorrowBookForm({ bookId, onBookBorrowed }: BorrowBookFormProps) {
  const [borrowerName, setBorrowerName] = useState('');
  const [returnDate, setReturnDate] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!borrowerName.trim() || !returnDate) return;

    setLoading(true);
    try {
      await borrowBook(bookId, borrowerName, returnDate);
      setBorrowerName('');
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
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <Input
              placeholder="お名前"
              value={borrowerName}
              onChange={(e) => setBorrowerName(e.target.value)}
              required
            />
          </div>
          <div>
            <Input
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

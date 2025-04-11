import React, { useState, useEffect } from 'react';
import { fetchBooks } from '../lib/api';
import { Book } from '../types/book';
import { Input } from './ui/input';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from './ui/table';
import { format } from 'date-fns';

interface BookListProps {
  refreshTrigger: number;
  onBorrowClick: (bookId: number) => void;
  onReturnClick: (bookId: number) => Promise<void>;
  onDeleteClick?: (bookId: number) => Promise<void>;
  showDeleteButton?: boolean;
  showBorrowReturnButtons?: boolean;
}

export function BookList({ 
  refreshTrigger, 
  onBorrowClick, 
  onReturnClick, 
  onDeleteClick,
  showDeleteButton = true,
  showBorrowReturnButtons = true 
}: BookListProps) {
  const [books, setBooks] = useState<Book[]>([]);
  const [titleSearch, setTitleSearch] = useState('');
  const [borrowerSearch, setBorrowerSearch] = useState('');
  const [sortByTitle, setSortByTitle] = useState(false);
  const [loading, setLoading] = useState(false);

  const loadBooks = async () => {
    setLoading(true);
    try {
      const data = await fetchBooks(titleSearch || undefined, borrowerSearch || undefined, sortByTitle);
      setBooks(data);
    } catch (error) {
      console.error('Failed to fetch books:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadBooks();
  }, [refreshTrigger, sortByTitle]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    loadBooks();
  };
  
  const handleToggleSort = () => {
    const newSortState = !sortByTitle;
    setSortByTitle(newSortState);
    loadBooks();
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>図書一覧</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSearch} className="flex flex-col md:flex-row gap-4 mb-6">
          <div className="flex-1">
            <Input
              placeholder="タイトルで検索"
              value={titleSearch}
              onChange={(e) => setTitleSearch(e.target.value)}
            />
          </div>
          <div className="flex-1">
            <Input
              placeholder="借りている人で検索"
              value={borrowerSearch}
              onChange={(e) => setBorrowerSearch(e.target.value)}
            />
          </div>
          <Button type="submit">検索</Button>
          <Button 
            type="button" 
            variant={sortByTitle ? "default" : "outline"} 
            onClick={handleToggleSort}
          >
            {sortByTitle ? "タイトルソート ↓" : "タイトルソート"}
          </Button>
        </form>

        {loading ? (
          <div className="text-center py-4">読み込み中...</div>
        ) : (
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>ID</TableHead>
                <TableHead>タイトル</TableHead>
                <TableHead>借りている人</TableHead>
                <TableHead>返却予定日</TableHead>
                <TableHead>アクション</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {books.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={5} className="text-center">
                    図書が見つかりません
                  </TableCell>
                </TableRow>
              ) : (
                books.map((book) => (
                  <TableRow key={book.id}>
                    <TableCell>{book.id}</TableCell>
                    <TableCell>{book.title}</TableCell>
                    <TableCell>{book.borrower_name || '-'}</TableCell>
                    <TableCell>
                      {book.return_date ? format(new Date(book.return_date), 'yyyy/MM/dd') : '-'}
                    </TableCell>
                    <TableCell>
                      <div className="flex flex-row gap-2">
                        {showBorrowReturnButtons && (
                          book.borrower_name ? (
                            <Button 
                              variant="outline" 
                              size="sm" 
                              onClick={() => onReturnClick(book.id)}
                            >
                              返却
                            </Button>
                          ) : (
                            <Button 
                              variant="outline" 
                              size="sm" 
                              onClick={() => onBorrowClick(book.id)}
                            >
                              借りる
                            </Button>
                          )
                        )}
                        {showDeleteButton && onDeleteClick && (
                          <Button 
                            variant="destructive"
                            size="sm" 
                            onClick={() => onDeleteClick(book.id)}
                          >
                            削除
                          </Button>
                        )}
                      </div>
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        )}
      </CardContent>
    </Card>
  );
}

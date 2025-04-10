import { useState } from 'react';
import './App.css';
import { BookList } from './components/BookList';
import { AddBookForm } from './components/AddBookForm';
import { BorrowBookForm } from './components/BorrowBookForm';
import { returnBook, deleteBook } from './lib/api';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from './components/ui/dialog';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './components/ui/tabs';

function App() {
  const [selectedBookId, setSelectedBookId] = useState<number | null>(null);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const refreshBooks = () => {
    setRefreshTrigger(prev => prev + 1);
  };

  const handleBookReturn = async (bookId: number) => {
    try {
      await returnBook(bookId);
      refreshBooks();
    } catch (error) {
      console.error('Failed to return book:', error);
    }
  };

  const handleBorrowClick = (bookId: number) => {
    setSelectedBookId(bookId);
    setIsDialogOpen(true);
  };

  const handleDialogClose = () => {
    setIsDialogOpen(false);
    setSelectedBookId(null);
  };

  const handleBookBorrowed = () => {
    handleDialogClose();
    refreshBooks();
  };

  const handleDeleteBook = async (bookId: number) => {
    if (!window.confirm('本を削除してもよろしいですか？')) {
      return;
    }
    
    try {
      await deleteBook(bookId);
      refreshBooks();
    } catch (error) {
      console.error('Failed to delete book:', error);
    }
  };

  return (
    <div className="container mx-auto py-8 px-4">
      <h1 className="text-3xl font-bold mb-8 text-center">社内図書管理システム</h1>
      
      <Tabs defaultValue="management" className="mb-8">
        <TabsList className="grid grid-cols-2 mb-4">
          <TabsTrigger value="management">本のマスター管理</TabsTrigger>
          <TabsTrigger value="borrow">貸出・返却管理</TabsTrigger>
        </TabsList>
        
        <TabsContent value="management">
          <div className="space-y-8">
            <AddBookForm onBookAdded={refreshBooks} />
            
            <BookList 
              refreshTrigger={refreshTrigger}
              onBorrowClick={handleBorrowClick}
              onReturnClick={handleBookReturn}
              onDeleteClick={handleDeleteBook}
              showDeleteButton={true}
              showBorrowReturnButtons={false}
            />
          </div>
        </TabsContent>
        
        <TabsContent value="borrow">
          <BookList 
            refreshTrigger={refreshTrigger}
            onBorrowClick={handleBorrowClick}
            onReturnClick={handleBookReturn}
            showDeleteButton={false}
            showBorrowReturnButtons={true}
          />
        </TabsContent>
      </Tabs>

      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>本を借りる</DialogTitle>
          </DialogHeader>
          {selectedBookId && (
            <BorrowBookForm 
              bookId={selectedBookId} 
              onBookBorrowed={handleBookBorrowed} 
            />
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
}

export default App;

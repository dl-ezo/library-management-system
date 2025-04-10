import { useState } from 'react';
import './App.css';
import { BookList } from './components/BookList';
import { AddBookForm } from './components/AddBookForm';
import { BorrowBookForm } from './components/BorrowBookForm';
import { returnBook, deleteBook } from './lib/api';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from './components/ui/dialog';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './components/ui/tabs';
import { Settings } from 'lucide-react';
import { Button } from './components/ui/button';

function App() {
  const [selectedBookId, setSelectedBookId] = useState<number | null>(null);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [showMasterManagement, setShowMasterManagement] = useState(false);

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
      <div className="flex items-center mb-8">
        <h1 className="text-3xl font-bold text-center flex-grow">社内図書管理システム</h1>
        <Button 
          variant="ghost" 
          size="icon" 
          className="ml-2"
          onClick={() => setShowMasterManagement(true)}
        >
          <Settings className="h-5 w-5" />
        </Button>
      </div>
      
      {showMasterManagement ? (
        <div className="space-y-8">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">本のマスター管理</h2>
            <Button variant="outline" onClick={() => setShowMasterManagement(false)}>
              閉じる
            </Button>
          </div>
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
      ) : (
        <Tabs defaultValue="borrow" className="mb-8">
          <TabsList className="grid w-full grid-cols-1 mb-4">
            <TabsTrigger value="borrow">貸出・返却管理</TabsTrigger>
          </TabsList>
          
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
      )}

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

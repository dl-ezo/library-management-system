import { useState } from 'react';
import './App.css';
import { BookList } from './components/BookList';
import { AddBookForm } from './components/AddBookForm';
import { BorrowBookForm } from './components/BorrowBookForm';
import { FeedbackForm } from './components/FeedbackForm';
import { FeedbackList } from './components/FeedbackList';
import { AuthPage } from './components/AuthPage';
import { UserHeader } from './components/UserHeader';
import { returnBook, deleteBook } from './lib/api';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from './components/ui/dialog';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './components/ui/tabs';
import { Settings } from 'lucide-react';
import { Button } from './components/ui/button';
import { ThemeToggle } from './components/theme/ThemeToggle';
import { AuthProvider, useAuth } from './contexts/AuthContext';

function LibraryApp() {
  const { isAuthenticated, isLoading } = useAuth();
  const [selectedBookId, setSelectedBookId] = useState<number | null>(null);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [feedbackRefreshTrigger, setFeedbackRefreshTrigger] = useState(0);
  const [showMasterManagement, setShowMasterManagement] = useState(false);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="text-lg">読み込み中...</div>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <AuthPage />;
  }

  const refreshBooks = () => {
    setRefreshTrigger(prev => prev + 1);
  };

  const refreshFeedbacks = () => {
    setFeedbackRefreshTrigger(prev => prev + 1);
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
        <div className="flex items-center gap-2">
          <ThemeToggle />
          <Button 
            variant="ghost" 
            size="icon" 
            className="ml-2"
            onClick={() => setShowMasterManagement(true)}
          >
            <Settings className="h-5 w-5" />
          </Button>
        </div>
      </div>
      
      <UserHeader />
      
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
          <TabsList className="grid w-full grid-cols-2 mb-4">
            <TabsTrigger value="borrow">貸出・返却管理</TabsTrigger>
            <TabsTrigger value="feedback">フィードバック</TabsTrigger>
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
          
          <TabsContent value="feedback">
            <div className="space-y-8">
              <FeedbackForm onSuccess={refreshFeedbacks} />
              <FeedbackList refreshTrigger={feedbackRefreshTrigger} />
            </div>
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

function App() {
  return (
    <AuthProvider>
      <LibraryApp />
    </AuthProvider>
  );
}

export default App;

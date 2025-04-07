import { useState } from 'react'
import './App.css'
import { BookList } from './components/BookList'
import { AddBookForm } from './components/AddBookForm'
import { BorrowBookForm } from './components/BorrowBookForm'
import { returnBook } from './lib/api'
import { Dialog, DialogContent, DialogHeader, DialogTitle } from './components/ui/dialog'

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

  return (
    <div className="container mx-auto py-8 px-4">
      <h1 className="text-3xl font-bold mb-8 text-center">社内図書管理システム</h1>
      
      <div className="space-y-8">
        <AddBookForm onBookAdded={refreshBooks} />
        
        <BookList 
          refreshTrigger={refreshTrigger}
          onBorrowClick={handleBorrowClick}
          onReturnClick={handleBookReturn}
        />
      </div>

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
  )
}

export default App

from typing import List, Optional, Dict
from datetime import date
from app.domain.models import Book
from app.domain.repositories import BookRepository

class InMemoryBookRepository(BookRepository):
    """インメモリの本リポジトリ実装"""
    
    def __init__(self):
        self.books: Dict[int, Book] = {}
        self.next_id = 1
    
    def add(self, book: Book) -> Book:
        book.id = self.next_id
        self.books[book.id] = book
        self.next_id += 1
        return book
    
    def get_by_id(self, book_id: int) -> Optional[Book]:
        return self.books.get(book_id)
    
    def get_all(self) -> List[Book]:
        return list(self.books.values())
    
    def search(self, title: Optional[str] = None, borrower_name: Optional[str] = None, sort_by_title: bool = False) -> List[Book]:
        result = self.get_all()
        
        if title:
            result = [book for book in result if title.lower() in book.title.lower()]
        
        if borrower_name:
            result = [book for book in result if book.borrower_name and borrower_name.lower() in book.borrower_name.lower()]
        
        if sort_by_title:
            result = sorted(result, key=lambda book: book.title.lower())
        
        return result
    
    def update(self, book: Book) -> Book:
        if book.id in self.books:
            self.books[book.id] = book
        return book
    
    def delete(self, book_id: int) -> bool:
        if book_id in self.books:
            del self.books[book_id]
            return True
        return False

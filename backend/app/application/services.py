from typing import List, Optional
from datetime import date
from app.domain.models import Book
from app.domain.repositories import BookRepository

class BookService:
    """本のアプリケーションサービス"""
    
    def __init__(self, repository: BookRepository):
        self.repository = repository
    
    def create_book(self, title: str) -> Book:
        """新しい本を作成する"""
        book = Book(id=0, title=title)
        return self.repository.add(book)
    
    def get_books(self, title: Optional[str] = None, borrower_name: Optional[str] = None) -> List[Book]:
        """本を検索する"""
        return self.repository.search(title, borrower_name)
    
    def get_book(self, book_id: int) -> Optional[Book]:
        """IDで本を取得する"""
        return self.repository.get_by_id(book_id)
    
    def borrow_book(self, book_id: int, borrower_name: str, return_date: date) -> Optional[Book]:
        """本を借りる"""
        book = self.repository.get_by_id(book_id)
        if not book:
            return None
        
        book.borrow(borrower_name, return_date)
        return self.repository.update(book)
    
    def return_book(self, book_id: int) -> Optional[Book]:
        """本を返却する"""
        book = self.repository.get_by_id(book_id)
        if not book:
            return None
        
        book.return_book()
        return self.repository.update(book)

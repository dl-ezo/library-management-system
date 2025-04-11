from typing import List, Optional, Any
from .models import Book
from abc import ABC, abstractmethod

class BookRepository(ABC):
    """本のリポジトリインターフェース"""
    
    @abstractmethod
    def add(self, book: Book) -> Book:
        """本を追加する"""
        pass
    
    @abstractmethod
    def get_by_id(self, book_id: int) -> Optional[Book]:
        """IDで本を取得する"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[Book]:
        """全ての本を取得する"""
        pass
    
    @abstractmethod
    def search(self, title: Optional[str] = None, borrower_name: Optional[str] = None) -> List[Book]:
        """本を検索する"""
        pass
    
    @abstractmethod
    def update(self, book: Book) -> Book:
        """本を更新する"""
        pass
    
    @abstractmethod
    def delete(self, book_id: int) -> bool:
        """本を削除する"""
        pass

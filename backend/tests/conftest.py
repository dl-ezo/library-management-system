import pytest
import os
from datetime import date
from typing import Dict, List, Optional
import sys

# テスト時にモジュールを正しく読み込むために、テスト用の環境変数を設定
os.environ["DATABASE_URL"] = "postgresql://postgres:postgres@localhost:5432/library_test"
os.environ["TEST_MODE"] = "1"

# app.domain以下をインポート
from app.domain.models import Book
from app.domain.repositories import BookRepository
from app.application.services import BookService

class TestInMemoryBookRepository(BookRepository):
    """テスト用インメモリリポジトリ"""
    
    def __init__(self):
        self.books: Dict[int, Book] = {}
        self.next_id = 1
    
    def add(self, book: Book) -> Book:
        book_id = self.next_id
        self.next_id += 1
        book = Book(
            id=book_id,
            title=book.title,
            borrower_name=book.borrower_name,
            return_date=book.return_date
        )
        self.books[book_id] = book
        return book
    
    def get_by_id(self, book_id: int) -> Optional[Book]:
        return self.books.get(book_id)
    
    def update(self, book: Book) -> Book:
        if book.id in self.books:
            self.books[book.id] = book
        return book
    
    def get_all(self) -> List[Book]:
        return list(self.books.values())
    
    def search(self, title: Optional[str] = None, borrower_name: Optional[str] = None) -> List[Book]:
        result = list(self.books.values())
        
        if title:
            result = [book for book in result if title.lower() in book.title.lower()]
        
        if borrower_name:
            result = [book for book in result if book.borrower_name and borrower_name == book.borrower_name]
        
        return result

@pytest.fixture(scope="function", autouse=True)
def setup_test_service():
    """テスト用サービスのセットアップ"""
    # app.dependenciesをモンキーパッチしてテスト用リポジトリを使用
    from app import dependencies
    
    # オリジナルのget_book_service関数を保存
    original_get_book_service = dependencies.get_book_service
    
    # テスト用のget_book_service関数を作成
    def mock_get_book_service():
        return BookService(repository=TestInMemoryBookRepository())
    
    # モンキーパッチ適用
    dependencies.get_book_service = mock_get_book_service
    
    # アプリケーションをインポート（APIクライアントを使うため）
    from app.main import app
    
    # テスト実行
    yield
    
    # 元の関数に戻す
    dependencies.get_book_service = original_get_book_service
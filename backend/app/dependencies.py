from app.application.services import BookService
from app.infrastructure.repositories import InMemoryBookRepository
from app.infrastructure.postgres_repository import PostgresBookRepository
from app.infrastructure.database import get_connection, init_db, is_test_mode
import os

# データベースの初期化
init_db()

# シングルトンのリポジトリインスタンス
_repository_instance = None
_service_instance = None

def get_book_service():
    """BookServiceのインスタンスを取得する"""
    global _repository_instance, _service_instance
    
    if _service_instance is None:
        if is_test_mode:
            _repository_instance = InMemoryBookRepository()
        else:
            # 通常モード：PostgreSQLを使用
            conn = get_connection()
            if conn:
                conn.close()
                _repository_instance = PostgresBookRepository()
            else:
                _repository_instance = InMemoryBookRepository()
        
        _service_instance = BookService(repository=_repository_instance)
    
    return _service_instance

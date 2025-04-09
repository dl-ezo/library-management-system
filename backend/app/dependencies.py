from app.application.services import BookService
from app.infrastructure.repositories import InMemoryBookRepository
from app.infrastructure.postgres_repository import PostgresBookRepository
from app.infrastructure.database import get_connection, init_db, is_test_mode
import os
import sqlite3

# データベースの初期化
init_db()

# テストモードかどうかを確認
def get_book_service():
    """BookServiceのインスタンスを取得する"""
    if is_test_mode:
        # テストモード：SQLiteを使用
        from tests.sqlite_repository import SQLiteBookRepository
        conn = get_connection()
        repository = SQLiteBookRepository(conn)
        return BookService(repository=repository)
    else:
        # 通常モード：PostgreSQLを使用
        conn = get_connection()
        if conn:
            conn.close()
            repository = PostgresBookRepository()
        else:
            repository = InMemoryBookRepository()
        return BookService(repository=repository)

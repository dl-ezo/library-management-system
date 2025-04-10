from typing import List, Optional, Dict, Any
import sqlite3
from datetime import date, datetime

from app.domain.models import Book
from app.domain.repositories import BookRepository

class SQLiteBookRepository(BookRepository):
    """SQLiteを使用した本のリポジトリ実装"""
    
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
    
    def get_all(self) -> List[Book]:
        """すべての本を取得する"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, title, borrower_name, return_date FROM books")
        rows = cursor.fetchall()
        return [self._row_to_book(row) for row in rows]
        
    def add(self, book: Book) -> Book:
        """新しい本を追加する"""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO books (title, borrower_name, return_date) VALUES (?, ?, ?)",
            (book.title, book.borrower_name, book.return_date.isoformat() if book.return_date else None)
        )
        self.conn.commit()
        book_id = cursor.lastrowid
        return Book(id=book_id, title=book.title, borrower_name=book.borrower_name, return_date=book.return_date)
    
    def get_by_id(self, book_id: int) -> Optional[Book]:
        """IDで本を取得する"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, title, borrower_name, return_date FROM books WHERE id = ?", (book_id,))
        row = cursor.fetchone()
        if not row:
            return None
        
        return self._row_to_book(row)
    
    def update(self, book: Book) -> Book:
        """本を更新する"""
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE books SET title = ?, borrower_name = ?, return_date = ? WHERE id = ?",
            (
                book.title,
                book.borrower_name,
                book.return_date.isoformat() if book.return_date else None,
                book.id
            )
        )
        self.conn.commit()
        return book
    
    def search(self, title: Optional[str] = None, borrower_name: Optional[str] = None) -> List[Book]:
        """本を検索する"""
        query = "SELECT id, title, borrower_name, return_date FROM books"
        params = []
        
        # 検索条件を追加
        conditions = []
        if title:
            conditions.append("title LIKE ?")
            params.append(f"%{title}%")
        if borrower_name:
            conditions.append("borrower_name = ?")
            params.append(borrower_name)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        return [self._row_to_book(row) for row in rows]
    
    def delete(self, book_id: int) -> bool:
        """本を削除する"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
        deleted = cursor.rowcount > 0
        self.conn.commit()
        return deleted
        
    def _row_to_book(self, row: tuple) -> Book:
        """SQLiteの行をBookオブジェクトに変換する"""
        book_id, title, borrower_name, return_date = row
        
        # 文字列から日付オブジェクトに変換
        parsed_date = None
        if return_date:
            try:
                parsed_date = date.fromisoformat(return_date)
            except ValueError:
                # エラーが発生した場合はNoneを使用
                pass
        
        return Book(
            id=book_id,
            title=title,
            borrower_name=borrower_name,
            return_date=parsed_date
        )

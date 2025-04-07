from typing import List, Optional
from datetime import date
import psycopg
from app.domain.models import Book
from app.domain.repositories import BookRepository
from app.infrastructure.database import get_connection

class PostgresBookRepository(BookRepository):
    """PostgreSQLの本リポジトリ実装"""

    def add(self, book: Book) -> Book:
        conn = get_connection()
        if not conn:
            from app.infrastructure.repositories import InMemoryBookRepository
            return InMemoryBookRepository().add(book)

        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO books (title, borrower_name, return_date) VALUES (%s, %s, %s) RETURNING id",
                (book.title, book.borrower_name, book.return_date)
            )
            book.id = cur.fetchone()[0]
        conn.commit()
        conn.close()
        return book

    def get_by_id(self, book_id: int) -> Optional[Book]:
        conn = get_connection()
        if not conn:
            from app.infrastructure.repositories import InMemoryBookRepository
            return InMemoryBookRepository().get_by_id(book_id)

        with conn.cursor() as cur:
            cur.execute("SELECT id, title, borrower_name, return_date FROM books WHERE id = %s", (book_id,))
            result = cur.fetchone()
            if not result:
                return None
            id, title, borrower_name, return_date = result
            book = Book(id=id, title=title, borrower_name=borrower_name, return_date=return_date)
        conn.close()
        return book

    def get_all(self) -> List[Book]:
        conn = get_connection()
        if not conn:
            from app.infrastructure.repositories import InMemoryBookRepository
            return InMemoryBookRepository().get_all()

        books = []
        with conn.cursor() as cur:
            cur.execute("SELECT id, title, borrower_name, return_date FROM books")
            for row in cur.fetchall():
                id, title, borrower_name, return_date = row
                books.append(Book(id=id, title=title, borrower_name=borrower_name, return_date=return_date))
        conn.close()
        return books

    def search(self, title: Optional[str] = None, borrower_name: Optional[str] = None) -> List[Book]:
        conn = get_connection()
        if not conn:
            from app.infrastructure.repositories import InMemoryBookRepository
            return InMemoryBookRepository().search(title, borrower_name)

        books = []
        query = "SELECT id, title, borrower_name, return_date FROM books WHERE 1=1"
        params = []

        if title:
            query += " AND title ILIKE %s"
            params.append(f"%{title}%")

        if borrower_name:
            query += " AND borrower_name ILIKE %s"
            params.append(f"%{borrower_name}%")

        with conn.cursor() as cur:
            cur.execute(query, params)
            for row in cur.fetchall():
                id, title, borrower_name, return_date = row
                books.append(Book(id=id, title=title, borrower_name=borrower_name, return_date=return_date))
        conn.close()
        return books

    def update(self, book: Book) -> Book:
        conn = get_connection()
        if not conn:
            from app.infrastructure.repositories import InMemoryBookRepository
            return InMemoryBookRepository().update(book)

        with conn.cursor() as cur:
            cur.execute(
                "UPDATE books SET title = %s, borrower_name = %s, return_date = %s WHERE id = %s",
                (book.title, book.borrower_name, book.return_date, book.id)
            )
        conn.commit()
        conn.close()
        return book

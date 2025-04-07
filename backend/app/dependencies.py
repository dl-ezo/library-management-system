from app.application.services import BookService
from app.infrastructure.repositories import InMemoryBookRepository
from app.infrastructure.postgres_repository import PostgresBookRepository
from app.infrastructure.database import get_connection, init_db

init_db()

conn = get_connection()
if conn:
    conn.close()
    book_repository = PostgresBookRepository()
else:
    book_repository = InMemoryBookRepository()

book_service = BookService(repository=book_repository)

def get_book_service():
    return book_service

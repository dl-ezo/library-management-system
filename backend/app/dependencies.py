from app.application.services import BookService
from app.infrastructure.repositories import InMemoryBookRepository

book_repository = InMemoryBookRepository()
book_service = BookService(repository=book_repository)

def get_book_service():
    return book_service

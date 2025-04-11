from app.domain.models import Book
from app.infrastructure.repositories import InMemoryBookRepository

repo = InMemoryBookRepository()
repo.add(Book(id=0, title='Python入門'))
repo.add(Book(id=0, title='Javaプログラミング'))
repo.add(Book(id=0, title='アルゴリズムとデータ構造'))
repo.add(Book(id=0, title='機械学習の基礎'))

books = repo.get_all()
for book in books:
    print(f'ID: {book.id}, Title: {book.title}')

from app.domain.models import Book
from app.infrastructure.repositories import InMemoryBookRepository

def initialize_repository(repo: InMemoryBookRepository) -> None:
    """テスト用のデータを初期化する"""
    repo.add(Book(id=0, title='Python入門'))
    repo.add(Book(id=0, title='Javaプログラミング'))
    repo.add(Book(id=0, title='アルゴリズムとデータ構造'))
    repo.add(Book(id=0, title='機械学習の基礎'))

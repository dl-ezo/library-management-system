import pytest
from fastapi.testclient import TestClient
from datetime import date, timedelta

# テスト時にapp.mainをインポートするためのインポート
from app.main import app

# テストクライアントを作成
from app.main import app
from fastapi.testclient import TestClient
from app.infrastructure.repositories import InMemoryBookRepository
from app.application.services import BookService
from app.dependencies import get_book_service

_test_repository = InMemoryBookRepository()

def get_test_book_service():
    return BookService(repository=_test_repository)

@pytest.fixture(scope="module")
def client():
    app.dependency_overrides[get_book_service] = get_test_book_service
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides = {}

def test_create_book(client):
    response = client.post(
        "/api/books/",
        json={"title": "テスト本", "author": "Test Author"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "テスト本"
    assert data["author"] == "Test Author"
    assert data["id"] is not None
    assert data["borrower_name"] is None
    assert data["return_date"] is None

def test_create_book_without_author(client):
    response = client.post(
        "/api/books/",
        json={"title": "Book Without Author"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Book Without Author"
    assert data["author"] is None
    assert data["id"] is not None
    assert data["borrower_name"] is None
    assert data["return_date"] is None

def test_read_books(client):
    # Create a book with an author
    response = client.post("/api/books/", json={"title": "検索テスト本", "author": "Search Test Author"})
    assert response.status_code == 200
    book_data = response.json()
    book_id = book_data["id"]
    assert book_data["author"] == "Search Test Author"

    # Test fetching all books (no specific author check here, just that it runs)
    client.get("/api/books/")
    
    # Test fetching the specific book by ID
    response = client.get(f"/api/books/{book_id}")
    assert response.status_code == 200
    fetched_book_data = response.json()
    assert fetched_book_data["title"] == "検索テスト本"
    assert fetched_book_data["author"] == "Search Test Author"
    
    # Test searching for the book by title
    response = client.get("/api/books/?title=検索テスト")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["title"] == "検索テスト本" # Assuming it's the first one or only one
    assert data[0]["author"] == "Search Test Author"

def test_borrow_book(client):
    response = client.post("/api/books/", json={"title": "貸出テスト本", "author": "Borrow Test Author"})
    assert response.status_code == 200
    book_data = response.json()
    book_id = book_data["id"]
    assert book_data["author"] == "Borrow Test Author"
    
    # Fetch the book to ensure it's there before borrowing
    response = client.get(f"/api/books/{book_id}")
    assert response.status_code == 200
    assert response.json()["author"] == "Borrow Test Author"
    
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    response = client.put(
        f"/api/books/{book_id}/borrow",
        json={"borrower_name": "テストユーザー", "return_date": tomorrow}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "貸出テスト本"
    assert data["author"] == "Borrow Test Author"
    assert data["borrower_name"] == "テストユーザー"
    assert data["return_date"] == tomorrow
    
    # Search for the borrowed book
    response = client.get("/api/books/?borrower_name=テストユーザー")
    assert response.status_code == 200
    data = response.json()
    # This assumes this is the only book borrowed by "テストユーザー" or the first one.
    # A more robust test might need to iterate or ensure a clean state.
    assert len(data) > 0
    assert data[0]["title"] == "貸出テスト本"
    assert data[0]["author"] == "Borrow Test Author"
    assert data[0]["borrower_name"] == "テストユーザー"

def test_return_book(client):
    response = client.post("/api/books/", json={"title": "返却テスト本", "author": "Return Test Author"})
    assert response.status_code == 200
    book_data = response.json()
    book_id = book_data["id"]
    assert book_data["author"] == "Return Test Author"
    
    # Fetch the book to ensure it's there
    response = client.get(f"/api/books/{book_id}")
    assert response.status_code == 200
    assert response.json()["author"] == "Return Test Author"
    
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    # Borrow the book first
    response = client.put(
        f"/api/books/{book_id}/borrow",
        json={"borrower_name": "テストユーザー", "return_date": tomorrow}
    )
    assert response.status_code == 200
    assert response.json()["author"] == "Return Test Author" # Ensure author persists
    
    # Return the book
    response = client.put(f"/api/books/{book_id}/return")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "返却テスト本"
    assert data["author"] == "Return Test Author"
    assert data["borrower_name"] is None
    assert data["return_date"] is None

def test_delete_book(client):
    response = client.post("/api/books/", json={"title": "削除テスト本"})
    assert response.status_code == 200
    book_id = response.json()["id"]
    
    response = client.get(f"/api/books/{book_id}")
    assert response.status_code == 200
    
    response = client.delete(f"/api/books/{book_id}")
    assert response.status_code == 200
    
    response = client.get(f"/api/books/{book_id}")
    assert response.status_code == 404

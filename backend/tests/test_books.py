import pytest
from fastapi.testclient import TestClient
from datetime import date, timedelta

from app.main import app
from app.infrastructure.repositories import InMemoryBookRepository
from app.application.services import BookService
from app.dependencies import get_book_service

@pytest.fixture(scope="module")
def test_book_repository():
    """テスト用のBookリポジトリを作成"""
    return InMemoryBookRepository()

@pytest.fixture(scope="module")
def client(test_book_repository):
    """テスト用クライアントを作成"""
    def get_test_book_service():
        return BookService(repository=test_book_repository)
    
    app.dependency_overrides[get_book_service] = get_test_book_service
    
    with TestClient(app) as test_client:
        yield test_client
    
    # クリーンアップ
    app.dependency_overrides = {}

def test_create_book(client):
    response = client.post(
        "/api/books/",
        json={"title": "テスト本"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "テスト本"
    assert data["id"] is not None
    assert data["borrower_name"] is None
    assert data["return_date"] is None

def test_read_books(client):
    response = client.post("/api/books/", json={"title": "検索テスト本"})
    assert response.status_code == 200
    book_id = response.json()["id"]
    print(f"Created book with ID: {book_id}")
    
    all_books = client.get("/api/books/")
    print(f"All books: {all_books.json()}")
    
    response = client.get(f"/api/books/{book_id}")
    print(f"Get book response: {response.status_code}")
    assert response.status_code == 200
    
    response = client.get("/api/books/?title=検索テスト")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "検索テスト" in data[0]["title"]

def test_borrow_book(client):
    response = client.post("/api/books/", json={"title": "貸出テスト本"})
    assert response.status_code == 200
    book_id = response.json()["id"]
    
    response = client.get(f"/api/books/{book_id}")
    assert response.status_code == 200
    
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    response = client.put(
        f"/api/books/{book_id}/borrow",
        json={"borrower_name": "テストユーザー", "return_date": tomorrow}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["borrower_name"] == "テストユーザー"
    assert data["return_date"] == tomorrow
    
    response = client.get("/api/books/?borrower_name=テストユーザー")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["borrower_name"] == "テストユーザー"

def test_return_book(client):
    response = client.post("/api/books/", json={"title": "返却テスト本"})
    assert response.status_code == 200
    book_id = response.json()["id"]
    
    response = client.get(f"/api/books/{book_id}")
    assert response.status_code == 200
    
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    response = client.put(
        f"/api/books/{book_id}/borrow",
        json={"borrower_name": "テストユーザー", "return_date": tomorrow}
    )
    assert response.status_code == 200
    
    response = client.put(f"/api/books/{book_id}/return")
    assert response.status_code == 200
    data = response.json()
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

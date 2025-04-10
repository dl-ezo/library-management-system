import pytest
from fastapi.testclient import TestClient
from datetime import date, timedelta

# テスト時にapp.mainをインポートするためのインポート
from app.main import app

# テストクライアントを作成
client = TestClient(app)

def test_create_book():
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

def test_read_books():
    client.post("/api/books/", json={"title": "検索テスト本"})
    
    response = client.get("/api/books/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    
    response = client.get("/api/books/?title=検索テスト")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "検索テスト" in data[0]["title"]

def test_borrow_book():
    response = client.post("/api/books/", json={"title": "貸出テスト本"})
    book_id = response.json()["id"]
    
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

def test_return_book():
    response = client.post("/api/books/", json={"title": "返却テスト本"})
    book_id = response.json()["id"]
    
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    client.put(
        f"/api/books/{book_id}/borrow",
        json={"borrower_name": "テストユーザー", "return_date": tomorrow}
    )
    
    response = client.put(f"/api/books/{book_id}/return")
    assert response.status_code == 200
    data = response.json()
    assert data["borrower_name"] is None
    assert data["return_date"] is None

def test_delete_book():
    response = client.post("/api/books/", json={"title": "削除テスト本"})
    book_id = response.json()["id"]
    
    response = client.get(f"/api/books/{book_id}")
    assert response.status_code == 200
    
    response = client.delete(f"/api/books/{book_id}")
    assert response.status_code == 200
    
    response = client.get(f"/api/books/{book_id}")
    assert response.status_code == 404

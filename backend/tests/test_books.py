import pytest
from fastapi.testclient import TestClient
from datetime import date, timedelta

from app.main import app

client = TestClient(app)

def test_create_book():
    response = client.post(
        "/books/",
        json={"title": "テスト本"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "テスト本"
    assert data["id"] is not None
    assert data["borrower_name"] is None
    assert data["return_date"] is None

def test_read_books():
    client.post("/books/", json={"title": "検索テスト本"})
    
    response = client.get("/books/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    
    response = client.get("/books/?title=検索テスト")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "検索テスト" in data[0]["title"]

def test_borrow_book():
    response = client.post("/books/", json={"title": "貸出テスト本"})
    book_id = response.json()["id"]
    
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    response = client.put(
        f"/books/{book_id}/borrow",
        json={"borrower_name": "テストユーザー", "return_date": tomorrow}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["borrower_name"] == "テストユーザー"
    assert data["return_date"] == tomorrow
    
    response = client.get("/books/?borrower_name=テストユーザー")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["borrower_name"] == "テストユーザー"

def test_return_book():
    response = client.post("/books/", json={"title": "返却テスト本"})
    book_id = response.json()["id"]
    
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    client.put(
        f"/books/{book_id}/borrow",
        json={"borrower_name": "テストユーザー", "return_date": tomorrow}
    )
    
    response = client.put(f"/books/{book_id}/return")
    assert response.status_code == 200
    data = response.json()
    assert data["borrower_name"] is None
    assert data["return_date"] is None

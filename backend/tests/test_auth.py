import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.infrastructure.user_repositories import InMemoryUserRepository
from app.application.user_services import UserService
from app.dependencies import get_user_service

# テスト用のユーザーリポジトリ
_test_user_repository = InMemoryUserRepository()

def get_test_user_service():
    return UserService(repository=_test_user_repository)

@pytest.fixture(scope="module")
def client():
    app.dependency_overrides[get_user_service] = get_test_user_service
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides = {}

def test_register_user(client):
    """ユーザー登録のテスト"""
    response = client.post(
        "/api/auth/register",
        json={"username": "testuser", "display_name": "テストユーザー"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["username"] == "testuser"
    assert data["user"]["display_name"] == "テストユーザー"
    assert data["access_token"] is not None
    assert data["token_type"] == "bearer"

def test_login_user(client):
    """ユーザーログインのテスト"""
    # まずユーザーを登録
    client.post(
        "/api/auth/register",
        json={"username": "logintest", "display_name": "ログインテスト"}
    )
    
    # ログインをテスト
    response = client.post(
        "/api/auth/login",
        json={"username": "logintest"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["username"] == "logintest"
    assert data["access_token"] is not None

def test_get_current_user(client):
    """現在のユーザー情報取得のテスト"""
    # ユーザー登録
    register_response = client.post(
        "/api/auth/register",
        json={"username": "currentuser", "display_name": "現在のユーザー"}
    )
    token = register_response.json()["access_token"]
    
    # 認証ヘッダーでユーザー情報を取得
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "currentuser"
    assert data["display_name"] == "現在のユーザー"

def test_duplicate_username_registration(client):
    """重複ユーザー名での登録エラーテスト"""
    # 最初のユーザー登録
    client.post(
        "/api/auth/register",
        json={"username": "duplicate", "display_name": "重複テスト1"}
    )
    
    # 同じユーザー名で再登録（エラーになるはず）
    response = client.post(
        "/api/auth/register",
        json={"username": "duplicate", "display_name": "重複テスト2"}
    )
    assert response.status_code == 400

def test_login_nonexistent_user(client):
    """存在しないユーザーでのログインエラーテスト"""
    response = client.post(
        "/api/auth/login",
        json={"username": "nonexistent"}
    )
    assert response.status_code == 401

def test_unauthorized_access(client):
    """認証なしでのアクセスエラーテスト"""
    response = client.get("/api/auth/me")
    assert response.status_code == 401
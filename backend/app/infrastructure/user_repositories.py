from typing import Optional, List, Dict
from datetime import datetime
from app.domain.user_models import User
from app.domain.user_repositories import UserRepository
from app.infrastructure.database import get_connection
import os

class InMemoryUserRepository(UserRepository):
    """インメモリユーザーリポジトリ実装（テスト用）"""
    
    def __init__(self):
        self._users: Dict[int, User] = {}
        self._next_id = 1
    
    def save(self, user: User) -> User:
        if user.id is None or user.id == 0:
            user.id = self._next_id
            self._next_id += 1
        self._users[user.id] = user
        return user
    
    def find_by_id(self, user_id: int) -> Optional[User]:
        return self._users.get(user_id)
    
    def find_by_username(self, username: str) -> Optional[User]:
        for user in self._users.values():
            if user.username == username:
                return user
        return None
    
    def find_all(self) -> List[User]:
        return list(self._users.values())
    
    def delete(self, user_id: int) -> bool:
        if user_id in self._users:
            del self._users[user_id]
            return True
        return False

class PostgresUserRepository(UserRepository):
    """PostgreSQLユーザーリポジトリ実装"""
    
    def save(self, user: User) -> User:
        conn = get_connection()
        if not conn:
            raise RuntimeError("Database connection not available")
        
        cursor = conn.cursor()
        try:
            if user.id is None or user.id == 0:
                cursor.execute(
                    "INSERT INTO users (username, display_name, created_at) VALUES (%s, %s, %s) RETURNING id",
                    (user.username, user.display_name, user.created_at)
                )
                user.id = cursor.fetchone()[0]
            else:
                cursor.execute(
                    "UPDATE users SET username = %s, display_name = %s WHERE id = %s",
                    (user.username, user.display_name, user.id)
                )
            conn.commit()
            return user
        finally:
            cursor.close()
            conn.close()
    
    def find_by_id(self, user_id: int) -> Optional[User]:
        conn = get_connection()
        if not conn:
            return None
        
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, username, display_name, created_at FROM users WHERE id = %s", (user_id,))
            row = cursor.fetchone()
            if row:
                return User(id=row[0], username=row[1], display_name=row[2], created_at=row[3])
            return None
        finally:
            cursor.close()
            conn.close()
    
    def find_by_username(self, username: str) -> Optional[User]:
        conn = get_connection()
        if not conn:
            return None
        
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, username, display_name, created_at FROM users WHERE username = %s", (username,))
            row = cursor.fetchone()
            if row:
                return User(id=row[0], username=row[1], display_name=row[2], created_at=row[3])
            return None
        finally:
            cursor.close()
            conn.close()
    
    def find_all(self) -> List[User]:
        conn = get_connection()
        if not conn:
            return []
        
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, username, display_name, created_at FROM users ORDER BY created_at DESC")
            rows = cursor.fetchall()
            return [User(id=row[0], username=row[1], display_name=row[2], created_at=row[3]) for row in rows]
        finally:
            cursor.close()
            conn.close()
    
    def delete(self, user_id: int) -> bool:
        conn = get_connection()
        if not conn:
            return False
        
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()
            conn.close()

def get_user_repository() -> UserRepository:
    """ユーザーリポジトリを取得する"""
    is_test_mode = os.environ.get("TEST_MODE", "0") == "1"
    if is_test_mode:
        return InMemoryUserRepository()
    else:
        return PostgresUserRepository()
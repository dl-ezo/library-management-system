from abc import ABC, abstractmethod
from typing import Optional, List
from .user_models import User

class UserRepository(ABC):
    """ユーザーリポジトリのインターフェース"""
    
    @abstractmethod
    def save(self, user: User) -> User:
        """ユーザーを保存する"""
        pass
    
    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[User]:
        """IDでユーザーを検索する"""
        pass
    
    @abstractmethod
    def find_by_username(self, username: str) -> Optional[User]:
        """ユーザー名でユーザーを検索する"""
        pass
    
    @abstractmethod
    def find_all(self) -> List[User]:
        """すべてのユーザーを取得する"""
        pass
    
    @abstractmethod
    def delete(self, user_id: int) -> bool:
        """ユーザーを削除する"""
        pass
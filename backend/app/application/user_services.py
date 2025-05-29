from typing import Optional, List, Tuple
from datetime import datetime, timedelta
from app.domain.user_models import User
from app.domain.user_repositories import UserRepository
from app.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

class UserService:
    """ユーザーアプリケーションサービス"""
    
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    def create_user(self, username: str, display_name: str) -> User:
        """新しいユーザーを作成する"""
        # ユーザー名の重複チェック
        existing_user = self.repository.find_by_username(username)
        if existing_user:
            raise ValueError("このユーザー名は既に使用されています")
        
        # ユーザー名の妥当性チェック
        if not username or len(username.strip()) == 0:
            raise ValueError("ユーザー名は必須です")
        
        if len(username) > 50:
            raise ValueError("ユーザー名は50文字以内で入力してください")
        
        if not display_name or len(display_name.strip()) == 0:
            raise ValueError("表示名は必須です")
        
        if len(display_name) > 100:
            raise ValueError("表示名は100文字以内で入力してください")
        
        user = User(id=0, username=username.strip(), display_name=display_name.strip())
        return self.repository.save(user)
    
    def login_user(self, username: str) -> Tuple[User, str]:
        """ユーザーログイン（ユーザー名のみ）"""
        user = self.repository.find_by_username(username)
        if not user:
            raise ValueError("ユーザーが見つかりません")
        
        # アクセストークンを生成
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        
        return user, access_token
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """ユーザー名でユーザーを取得する"""
        return self.repository.find_by_username(username)
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """IDでユーザーを取得する"""
        return self.repository.find_by_id(user_id)
    
    def get_all_users(self) -> List[User]:
        """すべてのユーザーを取得する"""
        return self.repository.find_all()
    
    def update_user(self, user_id: int, display_name: str) -> Optional[User]:
        """ユーザー情報を更新する"""
        user = self.repository.find_by_id(user_id)
        if not user:
            return None
        
        if not display_name or len(display_name.strip()) == 0:
            raise ValueError("表示名は必須です")
        
        if len(display_name) > 100:
            raise ValueError("表示名は100文字以内で入力してください")
        
        user.update_display_name(display_name.strip())
        return self.repository.save(user)
    
    def delete_user(self, user_id: int) -> bool:
        """ユーザーを削除する"""
        return self.repository.delete(user_id)
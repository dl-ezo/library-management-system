from datetime import datetime
from typing import Optional

class User:
    """ユーザーのドメインモデル"""
    
    def __init__(self, id: int, username: str, display_name: str, created_at: Optional[datetime] = None):
        self.id = id
        self.username = username
        self.display_name = display_name
        self.created_at = created_at or datetime.now()
    
    def update_display_name(self, new_display_name: str) -> None:
        """表示名を更新する"""
        self.display_name = new_display_name
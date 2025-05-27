from typing import List, Optional
from abc import ABC, abstractmethod
from .feedback_models import Feedback

class FeedbackRepository(ABC):
    """フィードバックのリポジトリインターフェース"""
    
    @abstractmethod
    def add(self, feedback: Feedback) -> Feedback:
        """フィードバックを追加する"""
        pass
    
    @abstractmethod
    def get_by_id(self, feedback_id: int) -> Optional[Feedback]:
        """IDでフィードバックを取得する"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[Feedback]:
        """全てのフィードバックを取得する"""
        pass
    
    @abstractmethod
    def update(self, feedback: Feedback) -> Feedback:
        """フィードバックを更新する"""
        pass
    
    @abstractmethod
    def delete(self, feedback_id: int) -> bool:
        """フィードバックを削除する"""
        pass
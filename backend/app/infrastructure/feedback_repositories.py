from typing import List, Optional, Dict
from datetime import datetime
from app.domain.feedback_models import Feedback
from app.domain.feedback_repositories import FeedbackRepository

class InMemoryFeedbackRepository(FeedbackRepository):
    """インメモリのフィードバックリポジトリ実装"""
    
    def __init__(self):
        self.feedbacks: Dict[int, Feedback] = {}
        self.next_id = 1
    
    def add(self, feedback: Feedback) -> Feedback:
        feedback.id = self.next_id
        self.feedbacks[feedback.id] = feedback
        self.next_id += 1
        return feedback
    
    def get_by_id(self, feedback_id: int) -> Optional[Feedback]:
        return self.feedbacks.get(feedback_id)
    
    def get_all(self) -> List[Feedback]:
        return list(self.feedbacks.values())
    
    def update(self, feedback: Feedback) -> Feedback:
        if feedback.id in self.feedbacks:
            self.feedbacks[feedback.id] = feedback
        return feedback
    
    def delete(self, feedback_id: int) -> bool:
        if feedback_id in self.feedbacks:
            del self.feedbacks[feedback_id]
            return True
        return False
from typing import List, Optional
import logging
from app.domain.feedback_models import Feedback
from app.domain.feedback_repositories import FeedbackRepository
from app.application.github_service import GitHubService

logger = logging.getLogger(__name__)

class FeedbackService:
    """フィードバックのアプリケーションサービス"""
    
    def __init__(self, repository: FeedbackRepository, github_service: GitHubService):
        self.repository = repository
        self.github_service = github_service
    
    def create_feedback(self, title: str, description: str, category: str) -> Feedback:
        """新しいフィードバックを作成する"""
        # フィードバックを作成
        feedback = Feedback.create(title, description, category)
        
        # バリデーション
        if not feedback.is_valid_category():
            raise ValueError(f"無効なカテゴリです: {category}")
        
        if not title.strip():
            raise ValueError("タイトルは必須です")
        
        if not description.strip():
            raise ValueError("詳細は必須です")
        
        # リポジトリに保存
        saved_feedback = self.repository.add(feedback)
        
        # GitHub Issue作成を試行
        if self.github_service.is_available():
            try:
                issue_url = self.github_service.create_issue_from_feedback(saved_feedback)
                if issue_url:
                    saved_feedback.set_github_issue_url(issue_url)
                    # GitHub Issue URLを保存
                    self.repository.update(saved_feedback)
                    logger.info(f"GitHub Issue作成成功: {issue_url}")
                else:
                    logger.warning("GitHub Issue作成に失敗しました")
            except Exception as e:
                logger.error(f"GitHub Issue作成中にエラー: {e}")
        else:
            logger.info("GitHub API が利用できないため、Issue作成をスキップします")
        
        return saved_feedback
    
    def get_feedbacks(self) -> List[Feedback]:
        """フィードバック一覧を取得する"""
        return self.repository.get_all()
    
    def get_feedback(self, feedback_id: int) -> Optional[Feedback]:
        """IDでフィードバックを取得する"""
        return self.repository.get_by_id(feedback_id)
    
    def delete_feedback(self, feedback_id: int) -> bool:
        """フィードバックを削除する"""
        return self.repository.delete(feedback_id)
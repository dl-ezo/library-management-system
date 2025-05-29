from app.application.services import BookService
from app.application.feedback_services import FeedbackService
from app.application.github_service import GitHubService
from app.application.user_services import UserService
from app.infrastructure.repositories import InMemoryBookRepository
from app.infrastructure.feedback_repositories import InMemoryFeedbackRepository
from app.infrastructure.postgres_repository import PostgresBookRepository
from app.infrastructure.user_repositories import get_user_repository
from app.infrastructure.database import get_connection, init_db, is_test_mode
import os

# データベースの初期化
init_db()

# シングルトンのリポジトリインスタンス
_repository_instance = None
_service_instance = None

# フィードバック用シングルトンインスタンス
_feedback_repository_instance = None
_feedback_service_instance = None
_github_service_instance = None

# ユーザー用シングルトンインスタンス
_user_service_instance = None

def get_book_service():
    """BookServiceのインスタンスを取得する"""
    global _repository_instance, _service_instance
    
    if _service_instance is None:
        if is_test_mode:
            _repository_instance = InMemoryBookRepository()
        else:
            # 通常モード：PostgreSQLを使用
            conn = get_connection()
            if conn:
                conn.close()
                _repository_instance = PostgresBookRepository()
            else:
                _repository_instance = InMemoryBookRepository()
        
        _service_instance = BookService(repository=_repository_instance)
    
    return _service_instance

def get_feedback_service():
    """FeedbackServiceのインスタンスを取得する"""
    global _feedback_repository_instance, _feedback_service_instance, _github_service_instance
    
    if _feedback_service_instance is None:
        # フィードバックリポジトリのインスタンス作成
        _feedback_repository_instance = InMemoryFeedbackRepository()
        
        # GitHubサービスのインスタンス作成
        _github_service_instance = GitHubService()
        
        # フィードバックサービスのインスタンス作成
        _feedback_service_instance = FeedbackService(
            repository=_feedback_repository_instance,
            github_service=_github_service_instance
        )
    
    return _feedback_service_instance

def get_user_service():
    """UserServiceのインスタンスを取得する"""
    global _user_service_instance
    
    if _user_service_instance is None:
        user_repository = get_user_repository()
        _user_service_instance = UserService(repository=user_repository)
    
    return _user_service_instance

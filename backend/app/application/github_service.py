import os
import logging
from typing import Optional
from github import Github, GithubException
from app.domain.feedback_models import Feedback

logger = logging.getLogger(__name__)

class GitHubService:
    """GitHub Issue作成サービス"""
    
    def __init__(self):
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.github_repo = os.getenv("GITHUB_REPO", "dl-ezo/library-management-system")
        self.github_client = None
        
        if self.github_token:
            try:
                self.github_client = Github(self.github_token)
                # 接続テスト
                self.github_client.get_user().login
                logger.info("GitHub API接続成功")
            except Exception as e:
                logger.error(f"GitHub API接続失敗: {e}")
                self.github_client = None
        else:
            logger.warning("GITHUB_TOKENが設定されていません")
    
    def create_issue_from_feedback(self, feedback: Feedback) -> Optional[str]:
        """フィードバックからGitHub Issueを作成する"""
        if not self.github_client:
            logger.warning("GitHub API が利用できません")
            return None
        
        try:
            repo = self.github_client.get_repo(self.github_repo)
            
            # カテゴリに応じたラベルを設定
            labels = ["feedback"]
            if feedback.category == "bug":
                labels.append("bug")
            elif feedback.category == "feature":
                labels.append("enhancement")
            elif feedback.category == "improvement":
                labels.append("enhancement")
            
            # Issue本文を作成
            body = f"""## フィードバック詳細

**カテゴリ**: {self._get_category_display_name(feedback.category)}

**詳細**:
{feedback.description}

---
*このIssueはユーザーフィードバック機能により自動作成されました*
*作成日時: {feedback.created_at.strftime('%Y-%m-%d %H:%M:%S')}*
"""
            
            # Issueを作成
            issue = repo.create_issue(
                title=f"[フィードバック] {feedback.title}",
                body=body,
                labels=labels
            )
            
            logger.info(f"GitHub Issue作成成功: {issue.html_url}")
            return issue.html_url
            
        except GithubException as e:
            logger.error(f"GitHub Issue作成失敗: {e}")
            return None
        except Exception as e:
            logger.error(f"予期しないエラー: {e}")
            return None
    
    def _get_category_display_name(self, category: str) -> str:
        """カテゴリの表示名を取得"""
        category_names = {
            "bug": "バグ報告",
            "feature": "機能要望",
            "improvement": "改善提案"
        }
        return category_names.get(category, category)
    
    def is_available(self) -> bool:
        """GitHub APIが利用可能かチェック"""
        return self.github_client is not None
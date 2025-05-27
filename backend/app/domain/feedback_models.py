from datetime import datetime
from typing import Optional
from dataclasses import dataclass

@dataclass
class Feedback:
    """フィードバックのドメインモデル"""
    id: int
    title: str
    description: str
    category: str  # "bug", "feature", "improvement"
    author_name: str
    created_at: datetime
    github_issue_url: Optional[str] = None
    
    @classmethod
    def create(cls, title: str, description: str, category: str, author_name: str) -> 'Feedback':
        """新しいフィードバックを作成する"""
        return cls(
            id=0,  # リポジトリで設定される
            title=title,
            description=description,
            category=category,
            author_name=author_name,
            created_at=datetime.now(),
            github_issue_url=None
        )
    
    def set_github_issue_url(self, url: str) -> None:
        """GitHub Issue URLを設定する"""
        self.github_issue_url = url
    
    def is_valid_category(self) -> bool:
        """カテゴリが有効かチェック"""
        valid_categories = ["bug", "feature", "improvement"]
        return self.category in valid_categories
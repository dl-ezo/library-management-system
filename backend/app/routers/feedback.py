from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from app.application.feedback_services import FeedbackService
from app.domain.feedback_models import Feedback as DomainFeedback
from app.dependencies import get_feedback_service

router = APIRouter(
    prefix="/feedback",
    tags=["feedback"],
)

class FeedbackBase(BaseModel):
    title: str
    description: str
    category: str  # "bug", "feature", "improvement"

class FeedbackCreate(FeedbackBase):
    pass

class Feedback(FeedbackBase):
    id: int
    created_at: datetime
    github_issue_url: Optional[str] = None

    class Config:
        from_attributes = True

def domain_to_dto(feedback: DomainFeedback) -> Feedback:
    return Feedback(
        id=feedback.id,
        title=feedback.title,
        description=feedback.description,
        category=feedback.category,
        created_at=feedback.created_at,
        github_issue_url=feedback.github_issue_url
    )

@router.post("/", response_model=Feedback)
async def create_feedback(feedback: FeedbackCreate, service: FeedbackService = Depends(get_feedback_service)):
    """フィードバックを作成する"""
    try:
        domain_feedback = service.create_feedback(
            title=feedback.title,
            description=feedback.description,
            category=feedback.category
        )
        return domain_to_dto(domain_feedback)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="フィードバックの作成に失敗しました")

@router.get("/", response_model=List[Feedback])
async def read_feedbacks(service: FeedbackService = Depends(get_feedback_service)):
    """フィードバック一覧を取得する"""
    domain_feedbacks = service.get_feedbacks()
    return [domain_to_dto(feedback) for feedback in domain_feedbacks]

@router.get("/{feedback_id}", response_model=Feedback)
async def read_feedback(feedback_id: int, service: FeedbackService = Depends(get_feedback_service)):
    """IDでフィードバックを取得する"""
    domain_feedback = service.get_feedback(feedback_id)
    if not domain_feedback:
        raise HTTPException(status_code=404, detail="フィードバックが見つかりません")
    return domain_to_dto(domain_feedback)

@router.delete("/{feedback_id}")
async def delete_feedback(feedback_id: int, service: FeedbackService = Depends(get_feedback_service)):
    """フィードバックを削除する"""
    success = service.delete_feedback(feedback_id)
    if not success:
        raise HTTPException(status_code=404, detail="フィードバックが見つかりません")
    return {"message": "フィードバックを削除しました"}

@router.get("/categories/", response_model=List[dict])
async def get_categories():
    """フィードバックカテゴリ一覧を取得する"""
    return [
        {"value": "bug", "label": "バグ報告"},
        {"value": "feature", "label": "機能要望"},
        {"value": "improvement", "label": "改善提案"}
    ]
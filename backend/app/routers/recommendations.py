from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import anthropic
import os
import json
import re

router = APIRouter(
    prefix="/books/recommendations",
    tags=["recommendations"],
)

class RecommendationRequest(BaseModel):
    query: str

class BookRecommendation(BaseModel):
    title: str
    author: str
    amazon_url: str
    recommendation_reason: str

class RecommendationResponse(BaseModel):
    recommendations: List[BookRecommendation]

def create_amazon_url(title: str, author: str) -> str:
    """書籍のタイトルと著者からAmazonの検索URLを生成"""
    search_query = f"{title} {author}".replace(" ", "+")
    return f"https://www.amazon.co.jp/s?k={search_query}&i=stripbooks"

def parse_ai_response(response_text: str) -> List[BookRecommendation]:
    """AIの応答を解析して書籍推薦リストに変換"""
    try:
        # JSONブロックを抽出
        json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            # JSONブロックがない場合、JSON形式の部分を探す
            json_start = response_text.find('[')
            json_end = response_text.rfind(']') + 1
            if json_start != -1 and json_end != 0:
                json_str = response_text[json_start:json_end]
            else:
                raise ValueError("JSON format not found in response")
        
        # JSONを解析
        recommendations_data = json.loads(json_str)
        recommendations = []
        
        for item in recommendations_data:
            title = item.get('title', '')
            author = item.get('author', '')
            amazon_url = create_amazon_url(title, author)
            recommendation_reason = item.get('reason', '')
            
            recommendations.append(BookRecommendation(
                title=title,
                author=author,
                amazon_url=amazon_url,
                recommendation_reason=recommendation_reason
            ))
        
        return recommendations
    except Exception as e:
        raise ValueError(f"Failed to parse AI response: {str(e)}")

@router.post("/", response_model=RecommendationResponse)
async def get_book_recommendations(request: RecommendationRequest):
    try:
        # Anthropic APIキーを環境変数から取得
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="Anthropic API key not configured")
        
        client = anthropic.Anthropic(api_key=api_key)
        
        # プロンプトを作成
        prompt = f"""
あなたは経験豊富な書籍推薦エキスパートです。以下のユーザーのリクエストに基づいて、5冊の書籍を推薦してください。

ユーザーのリクエスト: {request.query}

以下のJSON形式で回答してください：

```json
[
  {{
    "title": "書籍タイトル",
    "author": "著者名",
    "reason": "この書籍をおすすめする理由（100文字程度）"
  }}
]
```

- 実在する書籍のみを推薦してください
- 日本語で出版されている書籍を優先してください
- 各書籍について、なぜその本がユーザーのリクエストに適しているかを明確に説明してください
- 多様なジャンルや著者から選んでください
"""
        
        # Claude APIを呼び出し
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=2000,
            temperature=0.7,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        # レスポンスを解析
        ai_response = message.content[0].text
        recommendations = parse_ai_response(ai_response)
        
        return RecommendationResponse(recommendations=recommendations)
        
    except anthropic.APIError as e:
        raise HTTPException(status_code=500, detail=f"Anthropic API error: {str(e)}")
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"Response parsing error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
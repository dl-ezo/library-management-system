from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from pydantic import BaseModel
from datetime import datetime
from app.application.user_services import UserService
from app.domain.user_models import User as DomainUser
from app.auth import Token
from app.auth_dependencies import get_current_user
from app.dependencies import get_user_service

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
)

class UserBase(BaseModel):
    username: str
    display_name: str

class UserCreate(UserBase):
    pass

class UserLogin(BaseModel):
    username: str

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

def domain_to_dto(user: DomainUser) -> User:
    return User(
        id=user.id,
        username=user.username,
        display_name=user.display_name,
        created_at=user.created_at
    )

@router.post("/register", response_model=dict)
async def register(user: UserCreate, service: UserService = Depends(get_user_service)):
    """新規ユーザー登録"""
    try:
        domain_user = service.create_user(user.username, user.display_name)
        user_dto = domain_to_dto(domain_user)
        
        # 登録後、自動でログイン
        domain_user, access_token = service.login_user(domain_user.username)
        
        return {
            "user": user_dto,
            "access_token": access_token,
            "token_type": "bearer"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="ユーザー登録に失敗しました")

@router.post("/login", response_model=dict)
async def login(user_login: UserLogin, service: UserService = Depends(get_user_service)):
    """ユーザーログイン"""
    try:
        domain_user, access_token = service.login_user(user_login.username)
        user_dto = domain_to_dto(domain_user)
        
        return {
            "user": user_dto,
            "access_token": access_token,
            "token_type": "bearer"
        }
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="ログインに失敗しました")

@router.get("/me", response_model=User)
async def get_current_user_info(current_user: DomainUser = Depends(get_current_user)):
    """現在のユーザー情報を取得"""
    return domain_to_dto(current_user)

@router.get("/users", response_model=List[User])
async def get_all_users(
    current_user: DomainUser = Depends(get_current_user),
    service: UserService = Depends(get_user_service)
):
    """すべてのユーザーを取得（認証が必要）"""
    domain_users = service.get_all_users()
    return [domain_to_dto(user) for user in domain_users]

class UserUpdate(BaseModel):
    display_name: str

@router.put("/me", response_model=User)
async def update_current_user(
    user_update: UserUpdate,
    current_user: DomainUser = Depends(get_current_user),
    service: UserService = Depends(get_user_service)
):
    """現在のユーザー情報を更新"""
    try:
        updated_user = service.update_user(current_user.id, user_update.display_name)
        if not updated_user:
            raise HTTPException(status_code=404, detail="ユーザーが見つかりません")
        return domain_to_dto(updated_user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="ユーザー情報の更新に失敗しました")
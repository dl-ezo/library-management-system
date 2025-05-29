from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth import verify_token
from app.application.user_services import UserService
from app.dependencies import get_user_service
from app.domain.user_models import User

security = HTTPBearer()
security_optional = HTTPBearer(auto_error=False)

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user_service: UserService = Depends(get_user_service)
) -> User:
    """現在のユーザーを取得する"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="認証に失敗しました",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = verify_token(credentials.credentials, credentials_exception)
    user = user_service.get_user_by_username(token_data.username)
    if user is None:
        raise credentials_exception
    return user

def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_optional),
    user_service: UserService = Depends(get_user_service)
) -> Optional[User]:
    """現在のユーザーを取得する（認証は任意）"""
    if credentials is None:
        return None
    
    try:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="認証に失敗しました",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        token_data = verify_token(credentials.credentials, credentials_exception)
        user = user_service.get_user_by_username(token_data.username)
        return user
    except HTTPException:
        return None
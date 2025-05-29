import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """アプリケーション設定"""
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    GITHUB_REPO: str = os.getenv("GITHUB_REPO", "dl-ezo/library-management-system")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()

import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """アプリケーション設定"""
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    GITHUB_REPO: str = os.getenv("GITHUB_REPO", "dl-ezo/library-management-system")
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()

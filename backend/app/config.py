import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """アプリケーション設定"""
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    
    class Config:
        env_file = ".env"

settings = Settings()

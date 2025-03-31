from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Daily News Aggregator"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # 데이터베이스 설정
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./ai_news.db")
    
    # DeepSeek AI API 설정
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    
    # JWT 설정
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 뉴스 수집 설정
    NEWS_UPDATE_INTERVAL: int = 24  # 시간 단위
    MAX_NEWS_PER_CATEGORY: int = 10
    
    class Config:
        case_sensitive = True

settings = Settings() 
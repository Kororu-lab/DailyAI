from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import news, auth, subscribers
from src.core.config import settings
from src.core.database import engine, Base
from src.services.scheduler import NewsScheduler
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Daily News Aggregator",
    description="AI와 기술 관련 최신 소식을 수집하고 요약하는 서비스",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(news.router, prefix="/api/news", tags=["news"])
app.include_router(subscribers.router, prefix="/api/subscribers", tags=["subscribers"])

# 스케줄러 인스턴스
scheduler = NewsScheduler()

@app.on_event("startup")
async def startup_event():
    # 스케줄러 시작
    asyncio.create_task(scheduler.run_daily())
    logger.info("News scheduler started")

@app.on_event("shutdown")
async def shutdown_event():
    # 스케줄러 중지
    scheduler.stop()
    logger.info("News scheduler stopped")

@app.get("/")
async def root():
    return {"message": "AI Daily News Aggregator API에 오신 것을 환영합니다!"} 
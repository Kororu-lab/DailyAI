from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from src.core.database import get_db
from src.models.news import News
from src.services.news_collector import NewsCollector
from src.services.news_analyzer import NewsAnalyzer
import asyncio

router = APIRouter()

@router.get("/")
async def get_news(
    skip: int = 0,
    limit: int = 10,
    category: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(News)
    
    if category:
        query = query.filter(News.category == category)
    
    news = query.order_by(News.published_date.desc()).offset(skip).limit(limit).all()
    return news

@router.get("/clusters")
async def get_clusters(db: Session = Depends(get_db)):
    clusters = db.query(News.cluster_name).distinct().all()
    return [{"name": cluster[0]} for cluster in clusters]

@router.get("/cluster/{cluster_name}")
async def get_news_by_cluster(
    cluster_name: str,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    news = db.query(News).filter(
        News.cluster_name == cluster_name
    ).order_by(News.published_date.desc()).offset(skip).limit(limit).all()
    return news

@router.get("/today")
async def get_today_news(db: Session = Depends(get_db)):
    today = datetime.utcnow().date()
    news = db.query(News).filter(
        News.published_date >= today
    ).order_by(News.published_date.desc()).all()
    return news

@router.post("/collect")
async def collect_news():
    collector = NewsCollector()
    await collector.run()
    return {"message": "News collection completed"}

@router.post("/analyze")
async def analyze_news():
    analyzer = NewsAnalyzer()
    await analyzer.process_news()
    return {"message": "News analysis completed"}

@router.get("/summary")
async def get_daily_summary(db: Session = Depends(get_db)):
    today = datetime.utcnow().date()
    news = db.query(News).filter(
        News.published_date >= today
    ).all()
    
    if not news:
        raise HTTPException(status_code=404, detail="No news found for today")
    
    # 카테고리별 통계
    categories = {}
    for item in news:
        if item.category not in categories:
            categories[item.category] = 0
        categories[item.category] += 1
    
    # 감성 분석 통계
    sentiments = {}
    for item in news:
        if item.sentiment not in sentiments:
            sentiments[item.sentiment] = 0
        sentiments[item.sentiment] += 1
    
    return {
        "total_news": len(news),
        "categories": categories,
        "sentiments": sentiments,
        "top_keywords": [item.keywords for item in news[:5]]
    } 
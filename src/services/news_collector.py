import aiohttp
import asyncio
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict
from src.models.news import News
from src.core.database import SessionLocal
from src.core.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsCollector:
    def __init__(self):
        self.sources = [
            # AI 전문 뉴스
            {
                "name": "TechCrunch AI",
                "url": "https://techcrunch.com/tag/artificial-intelligence/",
                "selector": "article"
            },
            {
                "name": "MIT Technology Review AI",
                "url": "https://www.technologyreview.com/ai/",
                "selector": ".contentListItem"
            },
            {
                "name": "AI News",
                "url": "https://artificialintelligence-news.com/",
                "selector": "article"
            },
            {
                "name": "VentureBeat AI",
                "url": "https://venturebeat.com/category/ai/",
                "selector": "article"
            },
            {
                "name": "ZDNet AI",
                "url": "https://www.zdnet.com/topic/artificial-intelligence/",
                "selector": "article"
            },
            
            # 기술 뉴스
            {
                "name": "The Verge",
                "url": "https://www.theverge.com/tech",
                "selector": "article"
            },
            {
                "name": "Wired",
                "url": "https://www.wired.com/tag/technology/",
                "selector": "article"
            },
            {
                "name": "Ars Technica",
                "url": "https://arstechnica.com/tech/",
                "selector": "article"
            },
            {
                "name": "Engadget",
                "url": "https://www.engadget.com/",
                "selector": "article"
            },
            
            # AI 연구 및 학술
            {
                "name": "arXiv AI",
                "url": "https://arxiv.org/list/cs.AI/recent",
                "selector": "dt"
            },
            {
                "name": "Google AI Blog",
                "url": "https://ai.googleblog.com/",
                "selector": "article"
            },
            {
                "name": "OpenAI Blog",
                "url": "https://openai.com/blog",
                "selector": "article"
            },
            {
                "name": "DeepMind Blog",
                "url": "https://deepmind.com/blog",
                "selector": "article"
            },
            
            # AI 업계 뉴스
            {
                "name": "AI Business",
                "url": "https://aibusiness.com/",
                "selector": "article"
            },
            {
                "name": "Synced AI",
                "url": "https://syncedreview.com/",
                "selector": "article"
            },
            {
                "name": "KDnuggets",
                "url": "https://www.kdnuggets.com/",
                "selector": "article"
            },
            
            # 한국 AI 뉴스
            {
                "name": "AI Times",
                "url": "https://aitimes.com/",
                "selector": "article"
            },
            {
                "name": "테크M",
                "url": "https://www.techm.kr/ai/",
                "selector": "article"
            },
            {
                "name": "ZDNet Korea",
                "url": "https://www.zdnet.co.kr/ai/",
                "selector": "article"
            }
        ]
        
    async def fetch_page(self, session: aiohttp.ClientSession, url: str) -> str:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    logger.error(f"Error fetching {url}: Status {response.status}")
                    return ""
        except Exception as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            return ""

    async def parse_news(self, html: str, source: Dict) -> List[Dict]:
        news_items = []
        soup = BeautifulSoup(html, 'html.parser')
        
        for article in soup.select(source["selector"]):
            try:
                # 제목 추출 (다양한 HTML 구조 고려)
                title_elem = article.find(["h1", "h2", "h3", "h4", "a"])
                if not title_elem:
                    continue
                    
                title = title_elem.text.strip()
                
                # 링크 추출
                link = article.find("a")["href"]
                if not link.startswith("http"):
                    link = f"https://{source['url'].split('/')[2]}{link}"
                
                # 내용 추출 (가능한 경우)
                content_elem = article.find(["p", "div"], class_=["content", "description", "summary"])
                content = content_elem.text.strip() if content_elem else ""
                
                # 카테고리 결정
                category = "AI" if "ai" in source["name"].lower() else "Technology"
                
                news_items.append({
                    "title": title,
                    "content": content,
                    "url": link,
                    "source": source["name"],
                    "published_date": datetime.utcnow(),
                    "category": category
                })
            except Exception as e:
                logger.error(f"Error parsing article from {source['name']}: {str(e)}")
                continue
                
        return news_items

    async def collect_news(self):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for source in self.sources:
                html = await self.fetch_page(session, source["url"])
                if html:
                    news_items = await self.parse_news(html, source)
                    tasks.extend(news_items)
                    logger.info(f"Collected {len(news_items)} news items from {source['name']}")
            
            return tasks

    def save_news(self, news_items: List[Dict]):
        db = SessionLocal()
        try:
            for item in news_items:
                # 중복 체크
                existing = db.query(News).filter(News.url == item["url"]).first()
                if not existing:
                    news = News(**item)
                    db.add(news)
            db.commit()
            logger.info(f"Saved {len(news_items)} news items to database")
        except Exception as e:
            logger.error(f"Error saving news: {str(e)}")
            db.rollback()
        finally:
            db.close()

    async def run(self):
        news_items = await self.collect_news()
        self.save_news(news_items)
        logger.info(f"Total collected news items: {len(news_items)}") 
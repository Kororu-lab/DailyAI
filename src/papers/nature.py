from typing import List, Dict, Any
import feedparser
from datetime import datetime
import logging
from src.services.news_collectors import BaseNewsCollector
import aiohttp

logger = logging.getLogger(__name__)

class NatureAICollector(BaseNewsCollector):
    """Nature AI News 수집기"""
    
    def __init__(self, max_items: int = 10):
        super().__init__(max_items)
        self.url = "https://www.nature.com/nature.rss"
    
    async def collect(self) -> List[Dict[str, Any]]:
        """Nature의 AI 관련 기사를 수집합니다."""
        news_list = []
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                if response.status == 200:
                    feed = feedparser.parse(await response.text())
                    for entry in feed.entries:
                        # AI 관련 키워드가 포함된 기사만 필터링
                        if any(keyword in entry.title.lower() or keyword in entry.get('description', '').lower() 
                              for keyword in ['ai', 'artificial intelligence', 'machine learning', 'deep learning', 'neural network']):
                            # 날짜 필드가 없는 경우 현재 날짜 사용
                            try:
                                if hasattr(entry, 'published'):
                                    date = datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %z').strftime('%Y-%m-%d')
                                elif hasattr(entry, 'updated'):
                                    date = datetime.strptime(entry.updated, '%a, %d %b %Y %H:%M:%S %z').strftime('%Y-%m-%d')
                                else:
                                    date = datetime.now().strftime('%Y-%m-%d')
                            except (ValueError, AttributeError):
                                date = datetime.now().strftime('%Y-%m-%d')

                            news = {
                                'title': entry.title,
                                'url': entry.link,
                                'date': date,
                                'author': entry.get('author', 'Nature'),
                                'body': entry.get('description', ''),
                                'source': 'Nature AI'
                            }
                            news_list.append(news)
                            if len(news_list) >= self.max_items:
                                break
        return news_list 
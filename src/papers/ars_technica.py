from typing import List, Dict, Any
import feedparser
from datetime import datetime
import logging
from src.services.news_collectors import BaseNewsCollector

logger = logging.getLogger(__name__)

class ArsTechnicaAICollector(BaseNewsCollector):
    """Ars Technica AI 뉴스 수집기"""
    
    def __init__(self, max_items: int = 10):
        super().__init__(max_items)
        self.url = "https://arstechnica.com/tag/artificial-intelligence/feed/"
    
    async def collect(self) -> List[Dict[str, Any]]:
        try:
            feed = feedparser.parse(self.url)
            news_list = []
            
            for entry in feed.entries[:self.max_items]:
                try:
                    title = self._clean_text(entry.title)
                    url = entry.link
                    author = self._clean_text(entry.author) if hasattr(entry, 'author') else "Ars Technica Staff"
                    date = self._clean_text(entry.published) if hasattr(entry, 'published') else datetime.now().strftime("%Y-%m-%d")
                    body = self._clean_text(entry.summary) if hasattr(entry, 'summary') else ""
                    
                    news_list.append({
                        'title': title,
                        'url': url,
                        'author': author,
                        'date': date,
                        'body': body,
                        'source': 'Ars Technica AI'
                    })
                    
                except Exception as e:
                    logger.error(f"Ars Technica 기사 처리 중 오류 발생: {str(e)}")
                    continue
            
            return news_list
            
        except Exception as e:
            logger.error(f"Ars Technica 수집 중 오류 발생: {str(e)}")
            return [] 
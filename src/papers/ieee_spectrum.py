from typing import List, Dict, Any
import feedparser
from datetime import datetime
import logging
from src.services.news_collectors import BaseNewsCollector

logger = logging.getLogger(__name__)

class IEEESpectrumAICollector(BaseNewsCollector):
    """IEEE Spectrum AI 수집기"""
    
    def __init__(self, max_items: int = 10):
        super().__init__(max_items)
        self.url = "https://spectrum.ieee.org/feeds/topic/artificial-intelligence.rss"
    
    async def collect(self) -> List[Dict[str, Any]]:
        try:
            feed = feedparser.parse(self.url)
            news_list = []
            
            for entry in feed.entries[:self.max_items]:
                try:
                    title = self._clean_text(entry.title)
                    url = entry.link
                    author = self._clean_text(entry.author) if hasattr(entry, 'author') else "IEEE Spectrum Staff"
                    date = self._clean_text(entry.published) if hasattr(entry, 'published') else datetime.now().strftime("%Y-%m-%d")
                    body = self._clean_text(entry.summary) if hasattr(entry, 'summary') else ""
                    
                    news_list.append({
                        'title': title,
                        'url': url,
                        'author': author,
                        'date': date,
                        'body': body,
                        'source': 'IEEE Spectrum AI'
                    })
                    
                except Exception as e:
                    logger.error(f"IEEE Spectrum AI 기사 처리 중 오류 발생: {str(e)}")
                    continue
            
            return news_list
            
        except Exception as e:
            logger.error(f"IEEE Spectrum AI 수집 중 오류 발생: {str(e)}")
            return [] 
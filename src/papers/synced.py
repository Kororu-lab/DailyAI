from typing import List, Dict, Any
from datetime import datetime
import feedparser
from src.services.news_collectors import BaseNewsCollector

class SyncedAICollector(BaseNewsCollector):
    """Synced AI 수집기"""
    
    def __init__(self, max_items: int = 10):
        super().__init__(max_items)
        self.url = "https://syncedreview.com/feed/"
        
    async def collect(self) -> List[Dict[str, Any]]:
        """Synced의 AI 관련 뉴스를 수집합니다."""
        news_list = []
        feed = feedparser.parse(self.url)
        
        for entry in feed.entries[:self.max_items]:
            try:
                title = self._clean_text(entry.title)
                url = entry.link
                author = self._clean_text(entry.author) if hasattr(entry, 'author') else "Synced"
                date = self._clean_text(entry.published) if hasattr(entry, 'published') else datetime.now().strftime("%Y-%m-%d")
                body = self._clean_text(entry.summary) if hasattr(entry, 'summary') else ""
                
                news_list.append({
                    'title': title,
                    'url': url,
                    'author': author,
                    'date': date,
                    'body': body,
                    'source': 'Synced AI'
                })
                
            except Exception as e:
                continue
                
        return news_list 
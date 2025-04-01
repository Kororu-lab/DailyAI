from typing import List, Dict, Any
from datetime import datetime
import feedparser
from src.services.news_collectors import BaseNewsCollector

class VentureBeatAICollector(BaseNewsCollector):
    """VentureBeat AI 수집기"""
    
    def __init__(self, max_items: int = 10):
        super().__init__(max_items)
        self.url = "https://venturebeat.com/feed/"
        
    async def collect(self) -> List[Dict[str, Any]]:
        """VentureBeat의 AI 관련 뉴스를 수집합니다."""
        news_list = []
        feed = feedparser.parse(self.url)
        
        for entry in feed.entries[:self.max_items]:
            try:
                # AI 관련 기사만 필터링
                if not any(keyword in entry.title.lower() or 
                         (hasattr(entry, 'summary') and keyword in entry.summary.lower())
                         for keyword in ['ai', 'artificial intelligence', 'machine learning', 'deep learning']):
                    continue
                    
                title = self._clean_text(entry.title)
                url = entry.link
                author = self._clean_text(entry.author) if hasattr(entry, 'author') else "VentureBeat"
                date = self._clean_text(entry.published) if hasattr(entry, 'published') else datetime.now().strftime("%Y-%m-%d")
                body = self._clean_text(entry.summary) if hasattr(entry, 'summary') else ""
                
                news_list.append({
                    'title': title,
                    'url': url,
                    'author': author,
                    'date': date,
                    'body': body,
                    'source': 'VentureBeat AI'
                })
                
            except Exception as e:
                continue
                
        return news_list 
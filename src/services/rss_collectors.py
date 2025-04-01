from typing import List, Optional
import feedparser
from datetime import datetime
from src.models.news import News

class RSSBaseCollector:
    def __init__(self, url: str, source_name: str):
        self.url = url
        self.source_name = source_name

    def collect(self) -> List[News]:
        try:
            feed = feedparser.parse(self.url)
            news_items = []
            
            for entry in feed.entries:
                try:
                    # 날짜 파싱
                    published_date = datetime(*entry.published_parsed[:6]) if hasattr(entry, 'published_parsed') else datetime.now()
                    
                    # 제목과 URL 추출
                    title = entry.title
                    url = entry.link
                    
                    # 저자 추출 (있는 경우)
                    author = entry.author if hasattr(entry, 'author') else None
                    
                    # 초록 추출 (있는 경우)
                    abstract = entry.summary if hasattr(entry, 'summary') else None
                    
                    # HTML 태그 제거
                    if abstract:
                        from bs4 import BeautifulSoup
                        abstract = BeautifulSoup(abstract, 'html.parser').get_text()
                    
                    news_items.append(News(
                        title=title,
                        url=url,
                        author=author,
                        abstract=abstract,
                        created_at=published_date,
                        source=self.source_name
                    ))
                except Exception as e:
                    print(f"Error parsing entry: {e}")
                    continue
            
            return news_items
        except Exception as e:
            print(f"Error fetching RSS feed: {e}")
            return []

class TechCrunchAICollector(RSSBaseCollector):
    def __init__(self):
        super().__init__("https://techcrunch.com/tag/artificial-intelligence/feed/", "TechCrunch AI")

class MITTechnologyReviewAICollector(RSSBaseCollector):
    def __init__(self):
        super().__init__("https://www.technologyreview.com/topic/artificial-intelligence/feed/", "MIT Technology Review AI")

class ArsTechnicaAICollector(RSSBaseCollector):
    def __init__(self):
        super().__init__("https://arstechnica.com/tag/artificial-intelligence/feed/", "Ars Technica AI")

class SlashdotAICollector(RSSBaseCollector):
    def __init__(self):
        super().__init__("https://slashdot.org/tag/ai/rss/", "Slashdot AI") 
from typing import List, Dict, Any
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from datetime import datetime
from src.models.news import News
import logging
import re
from abc import ABC, abstractmethod
import requests
import feedparser

logger = logging.getLogger(__name__)

class BaseNewsCollector(ABC):
    """뉴스 수집을 위한 기본 클래스"""
    
    def __init__(self, max_items: int = 10):
        self.max_items = max_items
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    @abstractmethod
    async def collect(self) -> List[Dict[str, Any]]:
        """뉴스를 수집하는 추상 메서드"""
        pass
    
    def _clean_text(self, text: str) -> str:
        """텍스트 정제"""
        if not text:
            return ""
        # HTML 태그 제거
        text = re.sub(r'<[^>]+>', '', text)
        # 특수 문자 처리
        text = text.replace('&nbsp;', ' ').replace('&amp;', '&')
        # 연속된 공백 제거
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

class TechCrunchAICollector(BaseNewsCollector):
    """TechCrunch AI 뉴스 수집기"""
    
    def __init__(self, max_items: int = 10):
        super().__init__(max_items)
        self.url = "https://techcrunch.com/tag/artificial-intelligence/feed/"
    
    async def collect(self) -> List[Dict[str, Any]]:
        try:
            feed = feedparser.parse(self.url)
            news_list = []
            
            for entry in feed.entries[:self.max_items]:
                try:
                    title = self._clean_text(entry.title)
                    url = entry.link
                    author = self._clean_text(entry.author) if hasattr(entry, 'author') else "TechCrunch Staff"
                    date = self._clean_text(entry.published) if hasattr(entry, 'published') else datetime.now().strftime("%Y-%m-%d")
                    body = self._clean_text(entry.summary) if hasattr(entry, 'summary') else ""
                    
                    news_list.append({
                        'title': title,
                        'url': url,
                        'author': author,
                        'date': date,
                        'body': body,
                        'source': 'TechCrunch AI'
                    })
                    
                except Exception as e:
                    logger.error(f"TechCrunch 기사 처리 중 오류 발생: {str(e)}")
                    continue
            
            return news_list
            
        except Exception as e:
            logger.error(f"TechCrunch 수집 중 오류 발생: {str(e)}")
            return []

class MITTechnologyReviewAICollector(BaseNewsCollector):
    """MIT Technology Review AI 뉴스 수집기"""
    
    def __init__(self, max_items: int = 10):
        super().__init__(max_items)
        self.url = "https://www.technologyreview.com/feed/"
    
    async def collect(self) -> List[Dict[str, Any]]:
        try:
            feed = feedparser.parse(self.url)
            news_list = []
            
            for entry in feed.entries[:self.max_items]:
                try:
                    # AI 관련 기사만 필터링
                    if not any(tag.term.lower() in ['ai', 'artificial intelligence', 'machine learning'] 
                             for tag in entry.get('tags', [])):
                        continue
                        
                    title = self._clean_text(entry.title)
                    url = entry.link
                    author = self._clean_text(entry.author) if hasattr(entry, 'author') else "MIT Technology Review Staff"
                    date = self._clean_text(entry.published) if hasattr(entry, 'published') else datetime.now().strftime("%Y-%m-%d")
                    body = self._clean_text(entry.summary) if hasattr(entry, 'summary') else ""
                    
                    news_list.append({
                        'title': title,
                        'url': url,
                        'author': author,
                        'date': date,
                        'body': body,
                        'source': 'MIT Technology Review AI'
                    })
                    
                except Exception as e:
                    logger.error(f"MIT Technology Review 기사 처리 중 오류 발생: {str(e)}")
                    continue
            
            return news_list
            
        except Exception as e:
            logger.error(f"MIT Technology Review 수집 중 오류 발생: {str(e)}")
            return []

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
from typing import List, Optional
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging
from src.models.news import News

logger = logging.getLogger(__name__)

class BS4BaseCollector:
    def __init__(self, url: str):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def collect(self) -> List[News]:
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            return self.parse(soup)
        except Exception as e:
            print(f"Error fetching page: {e}")
            return []

    def parse(self, soup: BeautifulSoup) -> List[News]:
        raise NotImplementedError("Subclasses must implement parse()")

class SyncedAICollector(BS4BaseCollector):
    def __init__(self):
        super().__init__("https://syncedreview.com/tag/artificial-intelligence/")

    def parse(self, soup: BeautifulSoup) -> List[News]:
        news_items = []
        articles = soup.find_all('article', class_='post')
        
        for article in articles:
            try:
                title_elem = article.find('div', class_='entry-thumbnail').find('a')
                if not title_elem:
                    continue
                    
                title = title_elem.get('title', '').strip()
                url = title_elem['href']
                
                author_elem = article.find('span', class_='entry-author')
                author = author_elem.get_text(strip=True) if author_elem else None
                
                date_elem = article.find('span', class_='entry-date').find('a')
                date_str = date_elem.get_text(strip=True) if date_elem else None
                created_at = datetime.strptime(date_str, '%Y-%m-%d') if date_str else datetime.now()
                
                abstract_elem = article.find('div', class_='entry-content')
                abstract = abstract_elem.get_text(strip=True) if abstract_elem else None
                
                news_items.append(News(
                    title=title,
                    url=url,
                    author=author,
                    abstract=abstract,
                    created_at=created_at
                ))
            except Exception as e:
                print(f"Error parsing article: {e}")
                continue
                
        return news_items

class AITimesCollector(BS4BaseCollector):
    def __init__(self):
        super().__init__("https://www.aitimes.com/")

    def parse(self, soup: BeautifulSoup) -> List[News]:
        news_items = []
        articles = soup.find_all('article', class_='post')
        
        for article in articles:
            try:
                title_elem = article.find('h2', class_='entry-title')
                if not title_elem:
                    continue
                    
                title = title_elem.get_text(strip=True)
                url = title_elem.find('a')['href']
                
                author_elem = article.find('span', class_='author')
                author = author_elem.get_text(strip=True) if author_elem else None
                
                date_elem = article.find('time', class_='entry-date')
                date_str = date_elem['datetime'] if date_elem else None
                created_at = datetime.fromisoformat(date_str.replace('Z', '+00:00')) if date_str else datetime.now()
                
                abstract_elem = article.find('div', class_='entry-content')
                abstract = abstract_elem.get_text(strip=True) if abstract_elem else None
                
                news_items.append(News(
                    title=title,
                    url=url,
                    author=author,
                    abstract=abstract,
                    created_at=created_at
                ))
            except Exception as e:
                print(f"Error parsing article: {e}")
                continue
                
        return news_items

class WiredAICollector(BS4BaseCollector):
    def __init__(self):
        super().__init__("https://www.wired.com/tag/artificial-intelligence/")

    def parse(self, soup: BeautifulSoup) -> List[News]:
        news_items = []
        articles = soup.find_all('article', class_='article-component')
        
        for article in articles:
            try:
                title_elem = article.find('h2', class_='article-component__title')
                if not title_elem:
                    continue
                    
                title = title_elem.get_text(strip=True)
                url = title_elem.find('a')['href']
                
                author_elem = article.find('span', class_='article-component__author')
                author = author_elem.get_text(strip=True) if author_elem else None
                
                date_elem = article.find('time', class_='article-component__date')
                date_str = date_elem['datetime'] if date_elem else None
                created_at = datetime.fromisoformat(date_str.replace('Z', '+00:00')) if date_str else datetime.now()
                
                abstract_elem = article.find('div', class_='article-component__dek')
                abstract = abstract_elem.get_text(strip=True) if abstract_elem else None
                
                news_items.append(News(
                    title=title,
                    url=url,
                    author=author,
                    abstract=abstract,
                    created_at=created_at
                ))
            except Exception as e:
                print(f"Error parsing article: {e}")
                continue
                
        return news_items

class TheVergeAICollector(BS4BaseCollector):
    def __init__(self):
        super().__init__("https://www.theverge.com/ai-artificial-intelligence")

    def parse(self, soup: BeautifulSoup) -> List[News]:
        news_items = []
        articles = soup.find_all('article', class_='group')
        
        for article in articles:
            try:
                title_elem = article.find('h2', class_='group-hover:text-black-60')
                if not title_elem:
                    continue
                    
                title = title_elem.get_text(strip=True)
                url = title_elem.find('a')['href']
                
                author_elem = article.find('a', class_='text-gray-31 hover:text-black dark:text-gray-94')
                author = author_elem.get_text(strip=True) if author_elem else None
                
                date_elem = article.find('time')
                date_str = date_elem['datetime'] if date_elem else None
                created_at = datetime.fromisoformat(date_str.replace('Z', '+00:00')) if date_str else datetime.now()
                
                abstract_elem = article.find('p', class_='group-hover:text-black-60')
                abstract = abstract_elem.get_text(strip=True) if abstract_elem else None
                
                news_items.append(News(
                    title=title,
                    url=url,
                    author=author,
                    abstract=abstract,
                    created_at=created_at
                ))
            except Exception as e:
                print(f"Error parsing article: {e}")
                continue
                
        return news_items

class EngadgetAICollector(BS4BaseCollector):
    def __init__(self):
        super().__init__("https://www.engadget.com/ai-artificial-intelligence/")

    def parse(self, soup: BeautifulSoup) -> List[News]:
        news_items = []
        articles = soup.find_all('article', class_='article')
        
        for article in articles:
            try:
                title_elem = article.find('h2', class_='article-title')
                if not title_elem:
                    continue
                    
                title = title_elem.get_text(strip=True)
                url = title_elem.find('a')['href']
                
                author_elem = article.find('span', class_='article-author')
                author = author_elem.get_text(strip=True) if author_elem else None
                
                date_elem = article.find('time')
                date_str = date_elem['datetime'] if date_elem else None
                created_at = datetime.fromisoformat(date_str.replace('Z', '+00:00')) if date_str else datetime.now()
                
                abstract_elem = article.find('div', class_='article-excerpt')
                abstract = abstract_elem.get_text(strip=True) if abstract_elem else None
                
                news_items.append(News(
                    title=title,
                    url=url,
                    author=author,
                    abstract=abstract,
                    created_at=created_at
                ))
            except Exception as e:
                print(f"Error parsing article: {e}")
                continue
                
        return news_items

class GizmodoAICollector(BS4BaseCollector):
    def __init__(self):
        super().__init__("https://gizmodo.com/ai-artificial-intelligence")

    def parse(self, soup: BeautifulSoup) -> List[News]:
        news_items = []
        articles = soup.find_all('article', class_='article')
        
        for article in articles:
            try:
                title_elem = article.find('h2', class_='article-title')
                if not title_elem:
                    continue
                    
                title = title_elem.get_text(strip=True)
                url = title_elem.find('a')['href']
                
                author_elem = article.find('span', class_='article-author')
                author = author_elem.get_text(strip=True) if author_elem else None
                
                date_elem = article.find('time')
                date_str = date_elem['datetime'] if date_elem else None
                created_at = datetime.fromisoformat(date_str.replace('Z', '+00:00')) if date_str else datetime.now()
                
                abstract_elem = article.find('div', class_='article-excerpt')
                abstract = abstract_elem.get_text(strip=True) if abstract_elem else None
                
                news_items.append(News(
                    title=title,
                    url=url,
                    author=author,
                    abstract=abstract,
                    created_at=created_at
                ))
            except Exception as e:
                print(f"Error parsing article: {e}")
                continue
                
        return news_items

class ZDNetAICollector(BS4BaseCollector):
    def __init__(self):
        super().__init__("https://www.zdnet.com/topic/artificial-intelligence/")

    def parse(self, soup: BeautifulSoup) -> List[News]:
        news_items = []
        articles = soup.find_all('article', class_='article')
        
        for article in articles:
            try:
                title_elem = article.find('h3', class_='article-title')
                if not title_elem:
                    continue
                    
                title = title_elem.get_text(strip=True)
                url = title_elem.find('a')['href']
                
                author_elem = article.find('span', class_='article-author')
                author = author_elem.get_text(strip=True) if author_elem else None
                
                date_elem = article.find('time')
                date_str = date_elem['datetime'] if date_elem else None
                created_at = datetime.fromisoformat(date_str.replace('Z', '+00:00')) if date_str else datetime.now()
                
                abstract_elem = article.find('div', class_='article-excerpt')
                abstract = abstract_elem.get_text(strip=True) if abstract_elem else None
                
                news_items.append(News(
                    title=title,
                    url=url,
                    author=author,
                    abstract=abstract,
                    created_at=created_at
                ))
            except Exception as e:
                print(f"Error parsing article: {e}")
                continue
                
        return news_items

class CNETAICollector(BS4BaseCollector):
    def __init__(self):
        super().__init__("https://www.cnet.com/ai-artificial-intelligence/")

    def parse(self, soup: BeautifulSoup) -> List[News]:
        news_items = []
        articles = soup.find_all('article', class_='article')
        
        for article in articles:
            try:
                title_elem = article.find('h3', class_='article-title')
                if not title_elem:
                    continue
                    
                title = title_elem.get_text(strip=True)
                url = title_elem.find('a')['href']
                
                author_elem = article.find('span', class_='article-author')
                author = author_elem.get_text(strip=True) if author_elem else None
                
                date_elem = article.find('time')
                date_str = date_elem['datetime'] if date_elem else None
                created_at = datetime.fromisoformat(date_str.replace('Z', '+00:00')) if date_str else datetime.now()
                
                abstract_elem = article.find('div', class_='article-excerpt')
                abstract = abstract_elem.get_text(strip=True) if abstract_elem else None
                
                news_items.append(News(
                    title=title,
                    url=url,
                    author=author,
                    abstract=abstract,
                    created_at=created_at
                ))
            except Exception as e:
                print(f"Error parsing article: {e}")
                continue
                
        return news_items

class MashableAICollector(BS4BaseCollector):
    def __init__(self):
        super().__init__("https://mashable.com/ai-artificial-intelligence")

    def parse(self, soup: BeautifulSoup) -> List[News]:
        news_items = []
        articles = soup.find_all('article', class_='article')
        
        for article in articles:
            try:
                title_elem = article.find('h2', class_='article-title')
                if not title_elem:
                    continue
                    
                title = title_elem.get_text(strip=True)
                url = title_elem.find('a')['href']
                
                author_elem = article.find('span', class_='article-author')
                author = author_elem.get_text(strip=True) if author_elem else None
                
                date_elem = article.find('time')
                date_str = date_elem['datetime'] if date_elem else None
                created_at = datetime.fromisoformat(date_str.replace('Z', '+00:00')) if date_str else datetime.now()
                
                abstract_elem = article.find('div', class_='article-excerpt')
                abstract = abstract_elem.get_text(strip=True) if abstract_elem else None
                
                news_items.append(News(
                    title=title,
                    url=url,
                    author=author,
                    abstract=abstract,
                    created_at=created_at
                ))
            except Exception as e:
                print(f"Error parsing article: {e}")
                continue
                
        return news_items

class DigitalTrendsAICollector(BS4BaseCollector):
    def __init__(self):
        super().__init__("https://www.digitaltrends.com/ai-artificial-intelligence/")

    def parse(self, soup: BeautifulSoup) -> List[News]:
        news_items = []
        articles = soup.find_all('article', class_='article')
        
        for article in articles:
            try:
                title_elem = article.find('h2', class_='article-title')
                if not title_elem:
                    continue
                    
                title = title_elem.get_text(strip=True)
                url = title_elem.find('a')['href']
                
                author_elem = article.find('span', class_='article-author')
                author = author_elem.get_text(strip=True) if author_elem else None
                
                date_elem = article.find('time')
                date_str = date_elem['datetime'] if date_elem else None
                created_at = datetime.fromisoformat(date_str.replace('Z', '+00:00')) if date_str else datetime.now()
                
                abstract_elem = article.find('div', class_='article-excerpt')
                abstract = abstract_elem.get_text(strip=True) if abstract_elem else None
                
                news_items.append(News(
                    title=title,
                    url=url,
                    author=author,
                    abstract=abstract,
                    created_at=created_at
                ))
            except Exception as e:
                print(f"Error parsing article: {e}")
                continue
                
        return news_items

class TheNextWebAICollector(BS4BaseCollector):
    def __init__(self):
        super().__init__("https://thenextweb.com/artificial-intelligence")

    def parse(self, soup: BeautifulSoup) -> List[News]:
        news_items = []
        articles = soup.find_all('article', class_='article')
        
        for article in articles:
            try:
                title_elem = article.find('h2', class_='article-title')
                if not title_elem:
                    continue
                    
                title = title_elem.get_text(strip=True)
                url = title_elem.find('a')['href']
                
                author_elem = article.find('span', class_='article-author')
                author = author_elem.get_text(strip=True) if author_elem else None
                
                date_elem = article.find('time')
                date_str = date_elem['datetime'] if date_elem else None
                created_at = datetime.fromisoformat(date_str.replace('Z', '+00:00')) if date_str else datetime.now()
                
                abstract_elem = article.find('div', class_='article-excerpt')
                abstract = abstract_elem.get_text(strip=True) if abstract_elem else None
                
                news_items.append(News(
                    title=title,
                    url=url,
                    author=author,
                    abstract=abstract,
                    created_at=created_at
                ))
            except Exception as e:
                print(f"Error parsing article: {e}")
                continue
                
        return news_items 
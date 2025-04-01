from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
import time
import logging
from typing import List, Optional
from src.models.news import News

logger = logging.getLogger(__name__)

class SeleniumBaseCollector:
    """Selenium 기반 수집기의 기본 클래스"""
    
    def __init__(self, url: str, max_items: int = 10, wait_time: int = 10):
        self.url = url
        self.max_items = max_items
        self.wait_time = wait_time
        self.driver = None
    
    def setup_driver(self):
        """Chrome WebDriver 설정"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # 헤드리스 모드
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
    
    def wait_for_element(self, by: By, value: str, timeout: Optional[int] = None) -> Optional[object]:
        """요소가 나타날 때까지 대기"""
        if timeout is None:
            timeout = self.wait_time
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except Exception as e:
            logger.error(f"{self.__class__.__name__}: Element not found after {timeout} seconds")
            return None
    
    def collect(self) -> List[News]:
        """뉴스 수집 (하위 클래스에서 구현)"""
        raise NotImplementedError
    
    def __del__(self):
        """드라이버 정리"""
        if self.driver:
            self.driver.quit()

class ArxivAICollector(SeleniumBaseCollector):
    """arXiv AI 논문 수집기"""
    
    def __init__(self):
        super().__init__(
            url="https://arxiv.org/list/cs.AI/recent",
            max_items=10,
            wait_time=20
        )
    
    def collect(self) -> List[News]:
        try:
            if not self.driver:
                self.setup_driver()
            self.driver.get(self.url)
            
            # 페이지 로딩을 위한 대기 시간
            time.sleep(5)
            
            # 논문 목록 대기
            articles = self.wait_for_element(By.CSS_SELECTOR, "dl")
            if not articles:
                return []
            
            news_items = []
            articles = self.driver.find_elements(By.CSS_SELECTOR, "dt")
            
            for article in articles[:self.max_items]:
                try:
                    # 논문 ID와 제목 추출
                    title_elem = article.find_element(By.CSS_SELECTOR, "a[title='Abstract']")
                    title = title_elem.text.strip()
                    url = f"https://arxiv.org{title_elem.get_attribute('href')}"
                    
                    # 작성자 추출
                    try:
                        authors = article.find_element(By.CSS_SELECTOR, "dd").text.strip()
                    except:
                        authors = None
                    
                    # 날짜 추출
                    try:
                        date_str = article.find_element(By.CSS_SELECTOR, "dt").text.split("Submitted")[1].strip()
                        created_at = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                    except:
                        created_at = datetime.now()
                    
                    news_items.append(News(
                        title=title,
                        url=url,
                        author=authors,
                        abstract=None,
                        created_at=created_at,
                        source="arXiv AI"
                    ))
                except Exception as e:
                    logger.error(f"arXiv 논문 항목 추출 중 오류: {str(e)}")
                    continue
            
            return news_items
            
        except Exception as e:
            logger.error(f"arXiv 논문 수집 중 오류: {str(e)}")
            return [] 
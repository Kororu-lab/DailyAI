from typing import List, Dict
import asyncio
from datetime import datetime, timedelta
from src.models.news import News
from src.core.database import SessionLocal
from src.core.config import settings
import logging
from deepseek import DeepSeekAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsAnalyzer:
    def __init__(self):
        self.api = DeepSeekAPI(api_key=settings.DEEPSEEK_API_KEY)
        
    async def analyze_news(self, news: News) -> Dict:
        try:
            # 뉴스 내용 요약
            summary_prompt = f"다음 뉴스 기사를 3-4 문장으로 요약해주세요:\n\n{news.content}"
            summary = await self.api.generate_text(summary_prompt)
            
            # 감성 분석
            sentiment_prompt = f"다음 뉴스의 감성을 분석해주세요 (긍정/중립/부정):\n\n{news.content}"
            sentiment = await self.api.generate_text(sentiment_prompt)
            
            # 키워드 추출
            keywords_prompt = f"다음 뉴스에서 가장 중요한 키워드 5개를 추출해주세요:\n\n{news.content}"
            keywords = await self.api.generate_text(keywords_prompt)
            
            return {
                "summary": summary,
                "sentiment": sentiment,
                "keywords": keywords
            }
        except Exception as e:
            logger.error(f"Error analyzing news {news.id}: {str(e)}")
            return None

    async def cluster_news(self, news_list: List[News]) -> List[Dict]:
        try:
            # 뉴스 클러스터링을 위한 프롬프트 생성
            news_texts = [f"{news.title}\n{news.content}" for news in news_list]
            cluster_prompt = f"다음 뉴스들을 주제별로 그룹화해주세요:\n\n{'\n\n'.join(news_texts)}"
            
            # DeepSeek AI를 사용하여 클러스터링 수행
            clusters = await self.api.generate_text(cluster_prompt)
            
            # 클러스터 결과 파싱 및 반환
            return self._parse_clusters(clusters)
        except Exception as e:
            logger.error(f"Error clustering news: {str(e)}")
            return []

    def _parse_clusters(self, cluster_text: str) -> List[Dict]:
        # 클러스터 텍스트를 파싱하여 구조화된 데이터로 변환
        # 실제 구현에서는 더 복잡한 파싱 로직이 필요할 수 있습니다
        clusters = []
        current_cluster = {"name": "", "news_ids": []}
        
        for line in cluster_text.split("\n"):
            if line.startswith("Cluster"):
                if current_cluster["name"]:
                    clusters.append(current_cluster)
                current_cluster = {"name": line, "news_ids": []}
            elif line.strip():
                # 뉴스 ID 추출 로직 (실제 구현에서는 더 정교한 파싱이 필요)
                try:
                    news_id = int(line.split(":")[0].strip())
                    current_cluster["news_ids"].append(news_id)
                except:
                    continue
        
        if current_cluster["name"]:
            clusters.append(current_cluster)
            
        return clusters

    async def process_news(self):
        db = SessionLocal()
        try:
            # 최근 24시간 동안의 뉴스 가져오기
            recent_news = db.query(News).filter(
                News.created_at >= datetime.utcnow() - timedelta(hours=24)
            ).all()
            
            # 각 뉴스 분석
            for news in recent_news:
                analysis = await self.analyze_news(news)
                if analysis:
                    news.summary = analysis["summary"]
                    news.sentiment = analysis["sentiment"]
                    news.keywords = analysis["keywords"]
            
            # 뉴스 클러스터링
            if recent_news:
                clusters = await self.cluster_news(recent_news)
                for cluster in clusters:
                    for news_id in cluster["news_ids"]:
                        news = db.query(News).filter(News.id == news_id).first()
                        if news:
                            news.cluster_id = clusters.index(cluster)
                            news.cluster_name = cluster["name"]
            
            db.commit()
            logger.info(f"Processed {len(recent_news)} news items")
            
        except Exception as e:
            logger.error(f"Error processing news: {str(e)}")
            db.rollback()
        finally:
            db.close() 
import asyncio
from datetime import datetime, time
from src.services.news_collector import NewsCollector
from src.services.news_analyzer import NewsAnalyzer
from src.services.email_service import EmailService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsScheduler:
    def __init__(self):
        self.collector = NewsCollector()
        self.analyzer = NewsAnalyzer()
        self.email_service = EmailService()
        self.is_running = False

    async def collect_and_analyze_news(self):
        try:
            # 뉴스 수집
            await self.collector.run()
            logger.info("News collection completed")

            # 뉴스 분석
            await self.analyzer.process_news()
            logger.info("News analysis completed")

            # 이메일 발송
            await self.email_service.send_daily_newsletter()
            logger.info("Daily newsletter sent")

        except Exception as e:
            logger.error(f"Error in collect_and_analyze_news: {str(e)}")

    async def run_daily(self):
        self.is_running = True
        while self.is_running:
            try:
                now = datetime.now()
                # 매일 오전 8시에 실행
                target_time = time(8, 0)
                
                if now.time() >= target_time:
                    logger.info("Starting daily news collection and analysis")
                    await self.collect_and_analyze_news()
                    
                    # 다음 실행을 위해 24시간 대기
                    await asyncio.sleep(24 * 60 * 60)
                else:
                    # 다음 실행 시간까지 대기
                    next_run = datetime.combine(now.date(), target_time)
                    if now.time() > target_time:
                        next_run = datetime.combine(now.date().replace(day=now.day + 1), target_time)
                    
                    wait_seconds = (next_run - now).total_seconds()
                    logger.info(f"Waiting {wait_seconds/3600:.1f} hours until next run")
                    await asyncio.sleep(wait_seconds)

            except Exception as e:
                logger.error(f"Error in scheduler: {str(e)}")
                await asyncio.sleep(60)  # 에러 발생 시 1분 대기 후 재시도

    def stop(self):
        self.is_running = False
        logger.info("Scheduler stopped") 
import asyncio
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
import logging
from dotenv import load_dotenv

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/scheduler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# .env 파일 로드
load_dotenv()

# PYTHONPATH 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from collect_news import collect_news
from generate_report import generate_report
from send_report import send_report

async def run_daily_task():
    """매일 실행할 작업을 수행합니다."""
    try:
        # 어제 날짜의 뉴스 수집
        logger.info("뉴스 수집 시작")
        await collect_news()
        
        # 리포트 생성
        logger.info("리포트 생성 시작")
        await generate_report()
        
        # 리포트 이메일 전송
        logger.info("리포트 이메일 전송 시작")
        send_report()
        
        logger.info("일일 작업 완료")
        
    except Exception as e:
        logger.error(f"작업 실행 중 오류 발생: {str(e)}")

async def main():
    """메인 함수"""
    # 필요한 디렉토리 생성
    Path("logs").mkdir(exist_ok=True)
    Path("data").mkdir(exist_ok=True)
    Path("reports").mkdir(exist_ok=True)
    
    while True:
        now = datetime.now()
        # KST 02:00에 실행 (UTC 17:00)
        if now.hour == 2 and now.minute == 0:
            logger.info("KST 02:00 작업 시작")
            await run_daily_task()
        
        # 1분마다 체크
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main()) 
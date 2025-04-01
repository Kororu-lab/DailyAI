import asyncio
import json
from pathlib import Path
from datetime import datetime
from src.services.news_analyzer import NewsAnalyzer
from src.collect_news import collect_news
import os

async def generate_report():
    """뉴스를 수집하고 분석하여 HTML 리포트를 생성합니다."""
    # 환경 변수에서 API 키 가져오기
    api_key = os.getenv('DEEPSEEK_API_KEY')
    if not api_key:
        raise ValueError("DEEPSEEK_API_KEY 환경 변수가 설정되지 않았습니다.")
    
    # 뉴스 분석기 초기화
    analyzer = NewsAnalyzer(api_key)
    
    # 뉴스 데이터 로드
    news_file = Path("data/ai_news_20250401.json")
    if not news_file.exists():
        raise FileNotFoundError(f"뉴스 파일을 찾을 수 없습니다: {news_file}")
    
    with open(news_file, 'r', encoding='utf-8') as f:
        news_list = json.load(f)
    
    print(f"분석할 뉴스 파일: {news_file}")
    
    # 뉴스 분석
    analyzed_news = await analyzer.analyze_news(news_list)
    
    # HTML 생성
    html = analyzer.generate_html(analyzed_news)
    
    # 리포트 저장
    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)
    
    report_file = report_dir / f"ai_news_report_{datetime.now().strftime('%Y%m%d')}.html"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"리포트가 생성되었습니다: {report_file}")

if __name__ == "__main__":
    asyncio.run(generate_report()) 
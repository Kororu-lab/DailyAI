import asyncio
import json
from datetime import datetime, timedelta
from pathlib import Path
from src.papers.techcrunch import TechCrunchAICollector
from src.papers.mit_tech_review import MITTechnologyReviewAICollector
from src.papers.ars_technica import ArsTechnicaAICollector
from src.papers.nature import NatureAICollector
from src.papers.ieee_spectrum import IEEESpectrumAICollector
from src.papers.venturebeat import VentureBeatAICollector
from src.papers.arxiv import ArxivAICollector
from src.papers.synced import SyncedAICollector

async def collect_news():
    """모든 AI 뉴스 수집기에서 최근 7일간의 뉴스를 수집합니다."""
    collectors = [
        TechCrunchAICollector(),
        MITTechnologyReviewAICollector(),
        ArsTechnicaAICollector(),
        NatureAICollector(),
        IEEESpectrumAICollector(),
        VentureBeatAICollector(),
        ArxivAICollector(),
        SyncedAICollector()
    ]
    
    all_news = []
    cutoff_date = datetime.now() - timedelta(days=7)
    
    for collector in collectors:
        try:
            news_list = await collector.collect()
            for news in news_list:
                try:
                    news_date = datetime.strptime(news['date'], "%Y-%m-%d")
                    if news_date >= cutoff_date:
                        all_news.append(news)
                except ValueError:
                    # 날짜 형식이 다른 경우 현재 날짜로 설정
                    news['date'] = datetime.now().strftime("%Y-%m-%d")
                    all_news.append(news)
        except Exception as e:
            print(f"Error collecting news from {collector.__class__.__name__}: {str(e)}")
    
    # 날짜순으로 정렬
    all_news.sort(key=lambda x: x['date'], reverse=True)
    
    # 데이터 저장
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    output_file = data_dir / f"ai_news_{datetime.now().strftime('%Y%m%d')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_news, f, ensure_ascii=False, indent=2)
    
    print(f"총 {len(all_news)}개의 기사를 수집하여 {output_file}에 저장했습니다.")

if __name__ == "__main__":
    asyncio.run(collect_news()) 
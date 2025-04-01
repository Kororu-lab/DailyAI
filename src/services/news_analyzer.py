from typing import List, Dict, Any
import asyncio
from datetime import datetime
import logging
import aiohttp
import re
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsAnalyzer:
    """AI 뉴스 분석기"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def analyze_news(self, news_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """뉴스 목록을 분석하여 분류와 요약을 생성합니다."""
        logger.info(f"분석 시작: 총 {len(news_list)}개의 뉴스")
        
        # 1단계: 분야별 분류 및 필터링
        classified_news = await self._classify_news(news_list)
        logger.info(f"분류 완료: {len(classified_news)}개의 뉴스가 분류됨")
        
        # 2단계: 뉴스 메타데이터 정리
        processed_news = self._process_metadata(classified_news)
        logger.info(f"메타데이터 처리 완료: {len(processed_news)}개의 뉴스")
        
        # 3단계: 본문 요약
        summarized_news = await self._summarize_news(processed_news)
        logger.info(f"요약 완료: {len(summarized_news)}개의 뉴스")
        
        return summarized_news

    async def _classify_news(self, news_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """뉴스를 분야별로 분류하고 불필요한 뉴스를 필터링합니다."""
        logger.info("뉴스 분류 시작")
        
        # 전체 뉴스 정보를 한 번에 전송
        news_text = ""
        for i, news in enumerate(news_list):
            news_text += f"""
{i+1}. 제목: {news['title']}
본문: {news['body'][:500]}...
"""
        
        clustering_prompt = f"""다음 AI 관련 뉴스들을 분석하여 적절한 카테고리로 분류해주세요.
각 뉴스의 내용을 고려하여 가장 적합한 카테고리를 지정해주세요.

{news_text}

응답 형식:
[뉴스 번호]: [카테고리] - [분류 이유]
예시:
1: AI 모델 개발 - 새로운 언어 모델 개발 소식
2: AI 규제 정책 - 정부의 AI 규제 프레임워크 발표
...
"""
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_url,
                    headers=self.headers,
                    json={
                        "model": "deepseek-chat",
                        "messages": [{"role": "user", "content": clustering_prompt}],
                        "temperature": 0.3
                    }
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        clustering_text = result['choices'][0]['message']['content']
                        
                        # 분류 결과 파싱
                        classified_news = []
                        for line in clustering_text.split('\n'):
                            if ':' in line:
                                try:
                                    # 뉴스 번호와 카테고리 추출
                                    news_idx = int(line.split(':')[0].strip())
                                    category = line.split(':')[1].split('-')[0].strip()
                                    
                                    if 1 <= news_idx <= len(news_list):
                                        news = news_list[news_idx - 1]
                                        news['category'] = category
                                        classified_news.append(news)
                                        logger.info(f"분류 완료: {news['title']} -> {news['category']}")
                                except (ValueError, IndexError) as e:
                                    logger.warning(f"분류 결과 파싱 오류: {str(e)}")
                                    continue
                        
                        # 카테고리별 통계
                        category_stats = {}
                        for news in classified_news:
                            category = news['category']
                            if category not in category_stats:
                                category_stats[category] = 0
                            category_stats[category] += 1
                        
                        logger.info(f"분류 통계: {category_stats}")
                        return classified_news
                    else:
                        logger.error(f"API 호출 실패: {response.status}")
                        return []
        except Exception as e:
            logger.error(f"분류 중 오류 발생: {str(e)}")
            return []

    def _process_metadata(self, news_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """뉴스 메타데이터를 정리합니다."""
        logger.info("메타데이터 처리 시작")
        processed_news = []
        for news in news_list:
            processed_news.append({
                'title': news['title'],
                'url': news['url'],
                'date': news['date'],
                'author': news.get('author', '작성자 미상'),
                'source': news.get('source', '출처 미상'),
                'category': news['category'],
                'body': news['body'],
                'summary': news.get('body', '')[:200] + '...'  # 임시 요약
            })
        logger.info(f"메타데이터 처리 완료: {len(processed_news)}개의 뉴스")
        return processed_news

    async def _summarize_news(self, news_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """뉴스 본문을 요약합니다."""
        logger.info("뉴스 요약 시작")
        return news_list  # 임시로 요약 단계 스킵

    def format_analysis_item(self, item: Dict[str, Any]) -> str:
        """분석 항목을 HTML 형식으로 변환합니다."""
        # 제목 추출 (마크다운 형식 처리)
        title = item.get('title', '제목 없음')
        
        # URL 추출
        url = item.get('url', '#')
        
        # 요약 및 번역 생성
        summary_prompt = f"""다음 뉴스의 핵심 내용을 2-3문장으로 요약하고 한국어로 번역해주세요:

제목: {title}
본문: {item.get('body', '')[:500]}...

응답 형식:
[요약]
[한국어 번역]
"""
        
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json={
                    "model": "deepseek-chat",
                    "messages": [{"role": "user", "content": summary_prompt}],
                    "temperature": 0.3
                }
            )
            if response.status_code == 200:
                result = response.json()
                summary_text = result['choices'][0]['message']['content'].strip()
                
                # 요약과 번역 분리
                summary_parts = summary_text.split('\n\n')
                summary = summary_parts[0].replace('[요약]', '').strip() if len(summary_parts) > 0 else ''
                translation = summary_parts[1].replace('[한국어 번역]', '').strip() if len(summary_parts) > 1 else ''
            else:
                summary = item.get('body', '')[:200] + "..."
                translation = ""
        except Exception as e:
            logger.error(f"요약 생성 중 오류 발생: {str(e)}")
            summary = item.get('body', '')[:200] + "..."
            translation = ""
        
        # 카테고리 추출
        category = item.get('category', '미분류')
        
        # HTML 형식으로 변환
        html = f"""
        <div class="analysis-item">
            <div class="item-header">
                <div>
                    <h3>{title}</h3>
                    <p class="summary">{summary}</p>
                    <p class="translation">{translation}</p>
                </div>
                <a href="{url}" class="source-link" target="_blank" rel="noopener noreferrer">
                    <span class="source-icon">🔗</span> 원문 보기
                </a>
            </div>
            <div class="item-content">
                <div class="news-meta">
                    <span class="source">{item.get('source', '출처 미상')}</span>
                    <span class="author">{item.get('author', '작성자 미상')}</span>
                    <span class="date">{item.get('date', '')}</span>
                </div>
                <div class="category-tag">{category}</div>
            </div>
        </div>
        """
        return html

    def generate_html(self, analysis_results: List[Dict[str, Any]]) -> str:
        """분석 결과를 HTML 형식으로 변환합니다."""
        # AI 관련성이 낮은 뉴스 필터링
        filtered_results = [item for item in analysis_results if not item.get('category', '').startswith('(AI')]
        
        # 카테고리별로 뉴스 그룹화
        category_news = {}
        for item in filtered_results:
            category = item.get('category', '미분류')
            if category not in category_news:
                category_news[category] = []
            category_news[category].append(item)
        
        # 카테고리별 뉴스 수 계산
        category_counts = [(category, len(news)) for category, news in category_news.items()]
        logger.info(f"카테고리별 뉴스 수: {category_counts}")
        
        # HTML 생성
        html = f"""
        <!DOCTYPE html>
        <html lang="ko">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>AI 뉴스 분석 리포트</title>
            <style>
                :root {{
                    --primary-color: #2563eb;
                    --secondary-color: #1e40af;
                    --text-color: #1f2937;
                    --bg-color: #f3f4f6;
                    --card-bg: #ffffff;
                    --border-color: #e5e7eb;
                }}
                
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                    line-height: 1.6;
                    color: var(--text-color);
                    background-color: var(--bg-color);
                }}
                
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 2rem;
                }}
                
                .header {{
                    text-align: center;
                    margin-bottom: 3rem;
                    padding: 2rem;
                    background: var(--card-bg);
                    border-radius: 1rem;
                    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                }}
                
                .header h1 {{
                    color: var(--primary-color);
                    font-size: 2.5rem;
                    margin-bottom: 1rem;
                }}
                
                .date {{
                    color: #6b7280;
                    font-size: 1rem;
                }}
                
                .section {{
                    margin-bottom: 2rem;
                    padding: 2rem;
                    background: var(--card-bg);
                    border-radius: 1rem;
                    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                }}
                
                .section h2 {{
                    color: var(--primary-color);
                    font-size: 1.8rem;
                    margin-bottom: 1.5rem;
                    padding-bottom: 0.5rem;
                    border-bottom: 2px solid var(--border-color);
                }}
                
                .analysis-item {{
                    margin-bottom: 1.5rem;
                    padding: 1.5rem;
                    background: var(--bg-color);
                    border-radius: 0.75rem;
                    transition: transform 0.2s ease;
                }}
                
                .analysis-item:hover {{
                    transform: translateY(-2px);
                }}
                
                .item-header {{
                    display: flex;
                    justify-content: space-between;
                    align-items: flex-start;
                    margin-bottom: 1rem;
                }}
                
                .item-header h3 {{
                    color: var(--text-color);
                    font-size: 1.4rem;
                    font-weight: 600;
                    margin-bottom: 0.5rem;
                }}
                
                .item-header .summary {{
                    color: #4b5563;
                    font-size: 1rem;
                    margin-bottom: 0.5rem;
                }}
                
                .item-header .translation {{
                    color: #4b5563;
                    font-size: 1rem;
                    margin-bottom: 0.5rem;
                    font-style: italic;
                }}
                
                .source-link {{
                    display: inline-flex;
                    align-items: center;
                    padding: 0.5rem 1rem;
                    background: var(--primary-color);
                    color: white;
                    text-decoration: none;
                    border-radius: 0.5rem;
                    font-size: 0.9rem;
                    transition: background-color 0.2s ease;
                }}
                
                .source-link:hover {{
                    background: var(--secondary-color);
                }}
                
                .source-icon {{
                    margin-right: 0.5rem;
                }}
                
                .item-content {{
                    color: #4b5563;
                }}
                
                .news-meta {{
                    display: flex;
                    gap: 1rem;
                    font-size: 0.9rem;
                    color: #6b7280;
                    margin-top: 1rem;
                    padding-top: 1rem;
                    border-top: 1px solid var(--border-color);
                }}
                
                .source, .author {{
                    font-weight: 500;
                }}
                
                .category-tag {{
                    display: inline-block;
                    padding: 0.25rem 0.75rem;
                    background: var(--primary-color);
                    color: white;
                    border-radius: 9999px;
                    font-size: 0.875rem;
                    font-weight: 500;
                    margin-top: 0.5rem;
                }}
                
                @media (max-width: 768px) {{
                    .container {{
                        padding: 1rem;
                    }}
                    
                    .header h1 {{
                        font-size: 2rem;
                    }}
                    
                    .section {{
                        padding: 1.5rem;
                    }}
                    
                    .item-header {{
                        flex-direction: column;
                        align-items: flex-start;
                        gap: 1rem;
                    }}
                    
                    .source-link {{
                        width: 100%;
                        justify-content: center;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>AI 뉴스 분석 리포트</h1>
                    <div class="date">생성일: {datetime.now().strftime('%Y-%m-%d')}</div>
                </div>
        """
        
        # 카테고리별 섹션 생성
        for category, news in category_news.items():
            html += f"""
            <div class="section">
                <h2>{category}</h2>
            """
            
            for item in news:
                html += self.format_analysis_item(item)
            
            html += """
                </div>
            """
        
        html += """
            </div>
        </body>
        </html>
        """
        
        return html 
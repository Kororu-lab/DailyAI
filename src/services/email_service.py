import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from typing import List
import json
from src.core.config import settings
from src.models.news import News
from src.models.subscriber import Subscriber
from src.core.database import SessionLocal
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.smtp_username = settings.SMTP_USERNAME
        self.smtp_password = settings.SMTP_PASSWORD

    def create_email_content(self, news_items: List[News]) -> str:
        # 뉴스 카테고리별로 그룹화
        categories = {}
        for news in news_items:
            if news.category not in categories:
                categories[news.category] = []
            categories[news.category].append(news)

        # HTML 이메일 템플릿 생성
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                .category {{ margin-bottom: 20px; }}
                .category-title {{ 
                    color: #2c3e50; 
                    border-bottom: 2px solid #3498db; 
                    padding-bottom: 5px; 
                }}
                .news-item {{ 
                    margin: 10px 0; 
                    padding: 10px; 
                    background-color: #f8f9fa; 
                    border-radius: 5px; 
                }}
                .news-title {{ 
                    color: #2c3e50; 
                    font-weight: bold; 
                    margin-bottom: 5px; 
                }}
                .news-summary {{ color: #34495e; }}
                .news-meta {{ 
                    color: #7f8c8d; 
                    font-size: 0.9em; 
                    margin-top: 5px; 
                }}
            </style>
        </head>
        <body>
            <h1>AI & 기술 뉴스 요약 ({datetime.now().strftime('%Y-%m-%d')})</h1>
        """

        for category, items in categories.items():
            html_content += f"""
            <div class="category">
                <h2 class="category-title">{category}</h2>
            """
            
            for news in items:
                html_content += f"""
                <div class="news-item">
                    <div class="news-title">
                        <a href="{news.url}" style="color: #2c3e50; text-decoration: none;">
                            {news.title}
                        </a>
                    </div>
                    <div class="news-summary">{news.summary}</div>
                    <div class="news-meta">
                        출처: {news.source} | 
                        발행일: {news.published_date.strftime('%Y-%m-%d %H:%M')} | 
                        감성: {news.sentiment}
                    </div>
                </div>
                """

            html_content += "</div>"

        html_content += """
        <div style="margin-top: 20px; font-size: 0.9em; color: #7f8c8d;">
            <p>이 뉴스레터는 AI Daily News Aggregator에서 자동으로 발송됩니다.</p>
            <p>구독 해지를 원하시면 이메일로 회신해 주세요.</p>
        </div>
        </body>
        </html>
        """

        return html_content

    def send_email(self, to_email: str, subject: str, html_content: str):
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.smtp_username
            msg['To'] = to_email

            msg.attach(MIMEText(html_content, 'html'))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)

            logger.info(f"Email sent successfully to {to_email}")
            return True
        except Exception as e:
            logger.error(f"Error sending email to {to_email}: {str(e)}")
            return False

    async def send_daily_newsletter(self):
        db = SessionLocal()
        try:
            # 오늘의 뉴스 가져오기
            today = datetime.utcnow().date()
            news_items = db.query(News).filter(
                News.published_date >= today
            ).order_by(News.published_date.desc()).all()

            if not news_items:
                logger.info("No news items found for today")
                return

            # 활성 구독자 가져오기
            subscribers = db.query(Subscriber).filter(
                Subscriber.is_active == True
            ).all()

            # 이메일 내용 생성
            html_content = self.create_email_content(news_items)
            subject = f"AI & 기술 뉴스 요약 ({today.strftime('%Y-%m-%d')})"

            # 각 구독자에게 이메일 발송
            for subscriber in subscribers:
                if self.send_email(subscriber.email, subject, html_content):
                    subscriber.last_sent_at = datetime.utcnow()
                    db.add(subscriber)

            db.commit()
            logger.info(f"Daily newsletter sent to {len(subscribers)} subscribers")

        except Exception as e:
            logger.error(f"Error sending daily newsletter: {str(e)}")
            db.rollback()
        finally:
            db.close() 
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
import os
from datetime import datetime, timedelta
import logging
from dotenv import load_dotenv

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/email_sender.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# .env 파일 로드
load_dotenv()

def send_report():
    """생성된 HTML 리포트를 이메일로 전송합니다."""
    try:
        # 이메일 설정
        smtp_server = os.getenv('SMTP_SERVER')
        smtp_port = int(os.getenv('SMTP_PORT', '587'))
        smtp_username = os.getenv('SMTP_USERNAME')
        smtp_password = os.getenv('SMTP_PASSWORD')
        
        if not all([smtp_server, smtp_username, smtp_password]):
            raise ValueError("이메일 설정이 완료되지 않았습니다.")

        # 이메일 목록 읽기
        email_list_path = Path("config/email_list.txt")
        if not email_list_path.exists():
            raise FileNotFoundError("이메일 목록 파일을 찾을 수 없습니다.")
        
        with open(email_list_path, 'r') as f:
            recipients = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        if not recipients:
            raise ValueError("이메일 목록이 비어있습니다.")

        # 어제 날짜의 리포트 파일 찾기
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
        report_file = Path(f"reports/ai_news_report_{yesterday}.html")
        
        if not report_file.exists():
            raise FileNotFoundError(f"리포트 파일을 찾을 수 없습니다: {report_file}")

        # 이메일 메시지 생성
        msg = MIMEMultipart()
        msg['Subject'] = f'AI 뉴스 리포트 - {yesterday}'
        msg['From'] = smtp_username
        msg['To'] = ', '.join(recipients)

        # HTML 내용 추가
        with open(report_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        msg.attach(MIMEText(html_content, 'html'))

        # SMTP 서버 연결 및 이메일 전송
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)

        logger.info(f"리포트가 성공적으로 전송되었습니다: {', '.join(recipients)}")
        return True

    except Exception as e:
        logger.error(f"이메일 전송 중 오류 발생: {str(e)}")
        return False

if __name__ == "__main__":
    send_report() 
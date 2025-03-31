from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from src.core.database import Base

class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), index=True)
    content = Column(Text)
    url = Column(String(1000), unique=True)
    source = Column(String(200))
    published_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    category = Column(String(100))
    summary = Column(Text)
    sentiment = Column(String(50))
    
    # 뉴스 클러스터링을 위한 필드
    cluster_id = Column(Integer, nullable=True)
    cluster_name = Column(String(200), nullable=True)
    
    # 메타데이터
    keywords = Column(String(500))
    language = Column(String(50))
    read_time = Column(Integer)  # 예상 읽기 시간 (분)
    
    def __repr__(self):
        return f"<News {self.title}>" 
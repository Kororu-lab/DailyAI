# AI Daily News Aggregator

매일 아침 AI와 기술 관련 최신 소식들을 자동으로 수집하고 요약하여 제공하는 웹 애플리케이션입니다.

## 주요 기능

- 다양한 소스에서 AI 및 기술 관련 뉴스 자동 수집
- DeepSeek AI API를 활용한 뉴스 클러스터링 및 요약
- 매일 아침 새로운 뉴스 제공
- 웹 인터페이스를 통한 사용자 친화적인 뉴스 탐색

## 기술 스택

- Python 3.8+
- FastAPI (웹 프레임워크)
- DeepSeek AI API (뉴스 분석 및 요약)
- SQLAlchemy (데이터베이스 ORM)
- BeautifulSoup4 (웹 스크래핑)
- React (프론트엔드)

## 설치 방법

1. 저장소 클론
```bash
git clone https://github.com/yourusername/ai-daily-news.git
cd ai-daily-news
```

2. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는
.\venv\Scripts\activate  # Windows
```

3. 의존성 설치
```bash
pip install -r requirements.txt
```

4. 환경 변수 설정
```bash
cp .env.example .env
# .env 파일에 필요한 API 키와 설정값을 입력하세요
```

5. 데이터베이스 마이그레이션
```bash
alembic upgrade head
```

6. 애플리케이션 실행
```bash
uvicorn src.main:app --reload
```

## 프로젝트 구조

```
ai-daily-news/
├── src/                    # 소스 코드
│   ├── api/               # API 엔드포인트
│   ├── core/              # 핵심 기능
│   ├── models/            # 데이터 모델
│   ├── services/          # 비즈니스 로직
│   └── utils/             # 유틸리티 함수
├── tests/                 # 테스트 코드
├── docs/                  # 문서
├── data/                  # 데이터 파일
├── alembic/              # 데이터베이스 마이그레이션
├── requirements.txt      # Python 의존성
└── README.md            # 프로젝트 설명
```

## 라이선스

MIT License

## 기여 방법

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request 
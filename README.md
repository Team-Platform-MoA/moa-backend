# MoA Backend

치매 부양자를 위한 감정 분석 및 위로 메시지 제공 서비스

## 실행 방법

### 개발 서버 실행

```bash
# 간단한 실행 (권장)
uv run python main.py

# 또는 직접 uvicorn 사용
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 환경 설정

`.env` 파일에 다음 환경변수를 설정하세요:

```
GEMINI_API_KEY=your_gemini_api_key_here
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net
MONGODB_DATABASE=your_database
```

## API 엔드포인트

- `POST /api/analysis/` - 메시지 감정 분석
- `GET /api/users/{user_id}/history` - 사용자 분석 기록 조회
- `WS /ws` - WebSocket 연결

## 프로젝트 구조

```
app/
├── api/              # API 라우터
├── core/             # 핵심 설정 (config, database)
├── models/           # 데이터 모델
├── services/         # 비즈니스 로직
└── utils/            # 유틸리티 함수
```

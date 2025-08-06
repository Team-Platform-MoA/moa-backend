# MoA Backend

치매 부양자를 위한 감정 분석 및 위로 메시지 제공 서비스

## 실행 방법

### 1. 의존성 설치
```bash
uv sync
```

### 2. 환경 변수 설정
```bash
GEMINI_API_KEY=your_gemini_api_key_here
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net
MONGODB_DATABASE=your_database
```

### 3. 서버 실행
```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 데이터 모델

### User 모델
- `user_id`: 사용자 고유 ID (UUID)
- `name`: 사용자 이름
- `age`: 사용자 나이
- `dependent_type`: 부양자 유형 (Enum: 어머니, 아버지, 남편, 아내, 친척, 시부모님)
- `dependent_age`: 부양자 나이
- `is_onboarded`: 온보딩 완료 여부
- `created_at`: 생성 시간
- `last_active`: 마지막 활동 시간
- `total_conversations`: 총 대화 수

### Conversation 모델
- `user_id`: 사용자 ID
- `user_message`: 사용자 메시지
- `user_timestamp`: 사용자 메시지 시간
- `ai_sentiment`: AI 감정 분석 결과 (positive, neutral, negative)
- `ai_score`: AI 점수 (-1.0 ~ 1.0)
- `ai_comfort_message`: AI 위로 메시지
- `ai_timestamp`: AI 응답 시간
- `is_processed`: 처리 완료 여부

## API 리스트

### 사용자 관리
- `POST /api/users/onboarding` - 사용자 온보딩 정보 저장
- `GET /api/users/{user_id}/onboarding` - 사용자 온보딩 상태 조회
- `GET /api/users/{user_id}/history` - 사용자 대화 기록 조회

### 감정 분석
- `POST /api/analysis` - 메시지 감정 분석

### WebSocket
- `WS /ws` - WebSocket 연결

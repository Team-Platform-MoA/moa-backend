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
- `birth_year`: 사용자 출생년도
- `gender`: 사용자 성별 (Enum: 여성, 남성, 기타)
- `family_relationship`: 가족과의 관계 (Enum: 자녀, 배우자, 며느리/사위, 손주)
- `daily_care_hours`: 하루 돌봄 시간 (시간)
- `family_member_name`: 부양받는 가족 이름
- `family_member_birth_year`: 부양받는 가족 출생년도
- `family_member_gender`: 부양받는 가족 성별
- `family_member_dementia_stage`: 부양받는 가족 치매 정도
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
- `POST /api/users/onboarding` - 완전한 온보딩 정보 저장 (사용자 + 가족 정보)
- `GET /api/users/{user_id}/onboarding` - 사용자 온보딩 상태 조회
- `GET /api/users/{user_id}/history` - 사용자 대화 기록 조회

### 감정 분석
- `POST /api/analysis` - 메시지 감정 분석

### WebSocket
- `WS /ws` - WebSocket 연결

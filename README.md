# MoA Backend

치매 부양자를 위한 감정 분석 및 위로 메시지 제공 서비스  
**오디오 답변 처리, STT(Speech-to-Text), AI 감정 리포트 생성을 지원하는 FastAPI 기반 백엔드 서비스**

## 🚀 주요 기능

- **📱 오디오 답변 처리**: 3개 질문에 대한 오디오 답변 수집 및 배치 처리
- **🎤 음성 인식**: OpenAI Whisper API를 통한 고품질 STT 변환
- **🤖 AI 감정 분석**: 치매 부양자 전용 감정 리포트 생성
- **☁️ 클라우드 스토리지**: GCP Cloud Storage를 통한 오디오 파일 관리
- **📊 사용자 관리**: 온보딩, 히스토리 조회 등 종합 사용자 관리

## 🛠️ 기술 스택

- **Framework**: FastAPI
- **Database**: MongoDB + Beanie ODM
- **AI Services**: OpenAI Whisper (STT), Gemini/OpenAI (감정 분석)
- **Storage**: Google Cloud Storage
- **Language**: Python 3.11+
- **Package Manager**: uv

## 📁 프로젝트 구조

```
moa-backend/
├── app/
│   ├── api/                    # API 라우터
│   │   ├── answers.py         # 오디오 답변 관련 API
│   │   ├── users.py           # 사용자 관리 API
│   │   └── analysis.py        # 감정 분석 API
│   ├── core/                   # 핵심 설정
│   │   ├── config.py          # 환경 설정
│   │   ├── constants.py       # 상수 및 메시지 정의
│   │   ├── database.py        # 데이터베이스 연결
│   │   └── logger.py          # 로깅 설정
│   ├── external/               # 외부 서비스 연동
│   │   └── ai/                # AI 서비스 클라이언트
│   │       ├── base.py        # AI 서비스 기본 클래스
│   │       ├── client.py      # AI 클라이언트 팩토리
│   │       ├── openai.py      # OpenAI 구현체
│   │       └── gemini.py      # Gemini 구현체
│   ├── models/                 # 데이터 모델
│   │   └── models.py          # User, Conversation 모델
│   ├── prompts/                # AI 프롬프트 관리
│   │   ├── base.py            # 기본 프롬프트 클래스
│   │   └── report.py          # 감정 리포트 프롬프트
│   ├── schemas/                # API 스키마
│   │   ├── common.py          # 공통 Enum 정의
│   │   ├── reports.py         # 리포트 관련 스키마
│   │   ├── requests.py        # 요청 스키마
│   │   └── responses.py       # 응답 스키마
│   ├── services/               # 비즈니스 로직
│   │   ├── answer.py          # 오디오 답변 처리 서비스
│   │   ├── gcp_storage.py     # GCP 스토리지 서비스
│   │   ├── speech_to_text.py  # STT 서비스
│   │   ├── question.py        # 질문 관리 서비스
│   │   ├── report.py          # 감정 리포트 생성 서비스
│   │   └── user.py            # 사용자 관리 서비스
│   ├── utils/                  # 공통 유틸리티
│   │   └── common.py          # 공통 함수들
│   └── main.py                # FastAPI 앱 엔트리포인트
├── pyproject.toml             # 프로젝트 의존성
├── uv.lock                    # 의존성 락 파일
└── README.md                  # 프로젝트 문서
```

## ⚙️ 실행 방법

### 1. 의존성 설치

```bash
uv sync
```

### 2. 환경 변수 설정

```bash
# OpenAI API 키 (STT용)
OPENAI_API_KEY=your_openai_api_key_here

# AI 서비스 선택 (openai 또는 gemini)
AI_SERVICE=openai
GEMINI_API_KEY=your_gemini_api_key_here  # Gemini 사용시

# MongoDB 설정
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net
MONGODB_DATABASE=your_database

# GCP 설정 (오디오 파일 저장용)
GCP_PROJECT_ID=your_gcp_project_id
GCP_BUCKET_NAME=your_bucket_name
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/service-account.json
```

### 3. 서버 실행

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📊 데이터 모델

### User 모델

```python
class User(Document):
    # 기본 사용자 정보
    user_id: str                              # 사용자 고유 ID
    name: str                                 # 사용자 이름
    birth_year: int                           # 출생년도
    gender: Gender                            # 성별 (여성, 남성, 기타)

    # 부양 관련 정보
    family_relationship: FamilyRelationship   # 가족과의 관계
    daily_care_hours: int                     # 하루 돌봄 시간

    # 부양받는 가족 정보
    family_member_nickname: str               # 가족 애칭
    family_member_birth_year: int             # 가족 출생년도
    family_member_gender: Gender              # 가족 성별
    family_member_dementia_stage: DementiaStage  # 치매 정도

    # 활동 정보
    created_at: datetime                      # 생성 시간
    last_active: datetime                     # 마지막 활동 시간
    total_conversations: int                  # 총 대화 수
    is_onboarded: bool                        # 온보딩 완료 여부
```

### Conversation 모델

```python
class Conversation(Document):
    # 기본 정보
    user_id: str                              # 사용자 ID
    conversation_date: str                    # 대화 날짜
    is_processed: bool                        # 처리 완료 여부

    # 사용자 데이터
    user_message: str                         # 통합 Q&A 메시지
    user_timestamp: datetime                  # 사용자 메시지 시간
    audio_uri_1: Optional[str]               # 질문1 오디오 URI
    audio_uri_2: Optional[str]               # 질문2 오디오 URI
    audio_uri_3: Optional[str]               # 질문3 오디오 URI

    # AI 응답 데이터
    ai_sentiment: str                         # 감정 분석 결과
    ai_score: float                          # 감정 점수
    ai_comfort_message: str                  # 위로 메시지
    ai_timestamp: datetime                   # AI 응답 시간

    # 감정 리포트
    report: Optional[ConversationReport]     # AI 생성 감정 리포트
```

### ConversationReport 모델

```python
class ConversationReport(BaseModel):
    emotion_score: int                       # 종합 감정 점수 (1-100)
    daily_summary: str
    emotion_analysis: ConversationReportEmotion  # 세부 감정 분석
    letter: str                              # 개인화된 위로 편지

class ConversationReportEmotion(BaseModel):
    stress: int                              # 스트레스 수준 (0-100)
    resilience: int                          # 회복 탄력성 (0-100)
    stability: int                           # 정서 안정성 (0-100)
```

## 🔗 API 엔드포인트

### 🎯 답변 관리 (`/api/answers`)

- `GET /questions` - 전체 질문 목록 조회
- `GET /questions/{question_number}` - 특정 질문 조회
- `POST /audio` - 오디오 답변 업로드 및 처리

### 👤 사용자 관리 (`/api/users`)

- `POST /onboarding` - 완전한 온보딩 정보 저장
- `GET /{user_id}/onboarding` - 사용자 온보딩 상태 조회
- `GET /{user_id}/history` - 사용자 대화 기록 조회

## 🎵 오디오 처리 워크플로우

1. **개별 업로드**: 사용자가 3개 질문에 대해 오디오 답변 업로드
2. **배치 처리**: 3번째 질문 완료 시 전체 오디오 STT 일괄 처리
3. **AI 분석**: 텍스트 변환 완료 후 감정 리포트 생성
4. **응답 반환**: 처리 결과와 감정 리포트를 클라이언트에 반환

## 🧪 개발 정보

### 지원 오디오 형식

- WAV, MP3, MP4, M4A, WebM, OGG, AAC, FLAC, 3GPP
- 최대 파일 크기: 10MB

### 질문 내용

1. "{가족관계}의 상태 중에서 오늘 가장 신경 쓰인 부분이 있으셨나요?"
2. "오늘 돌봄 과정에서 '아, 이건 정말 나 혼자서는 안 되겠다'라고 느낀 순간이 있으셨나요?"
3. "오늘 본인을 위해 챙긴 것이 있다면 어떤 것이었나요? 혹시 챙기지 못했다면 그 이유는 뭐였을까요?"

### 개발 원칙

- **의존성 주입**: 모든 서비스는 팩토리 함수를 통한 주입
- **상수 관리**: 모든 메시지와 설정값은 중앙 집중화
- **에러 처리**: Graceful degradation과 상세한 로깅
- **타입 안전성**: 엄격한 타입 힌트와 Pydantic 검증

## 🔧 환경 설정

### 개발 환경

```bash
# 개발 서버 실행 (Hot reload)
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 테스트 실행
uv run pytest

# 코드 포맷팅
uv run black app/
uv run isort app/
```

### 프로덕션 환경

```bash
# 프로덕션 서버 실행
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📝 라이센스

이 프로젝트는 MIT 라이센스 하에 배포됩니다.

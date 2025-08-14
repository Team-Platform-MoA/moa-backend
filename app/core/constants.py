"""애플리케이션 상수 정의"""

# 질문 관련 상수
MAX_QUESTION_NUMBER = 3
MIN_QUESTION_NUMBER = 1
FINAL_QUESTION_NUMBER = 3

# 질문 내용
QUESTIONS = {
    1: "오늘 부양하면서 어떤 순간이 가장 기억에 남나요?",
    2: "지금 이 순간 마음속에서 가장 큰 감정은 무엇인가요?",
    3: "오늘 나 자신에게 해주고 싶은 말이 있다면?"
}

# 오디오 파일 관련 상수
MAX_AUDIO_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_AUDIO_TYPES = [
    "audio/wav",
    "audio/mpeg",
    "audio/mp4",
    "audio/m4a",
    "audio/webm",
    "audio/ogg",
    "audio/x-wav",
    "audio/x-m4a",
    "audio/aac",
    "audio/flac",
    "audio/3gpp",
]

# AI 관련 상수
DEFAULT_AI_SENTIMENT = "neutral"
DEFAULT_AI_SCORE = 0.0
STT_MODEL = "whisper-1"
STT_LANGUAGE = "ko"
STT_TEMPERATURE = 0

# 메시지 상수
class Messages:
    AUDIO_UPLOAD_SUCCESS = "질문 {question_number} 오디오가 저장되었습니다."
    ALL_ANSWERS_COMPLETE = "모든 답변 처리가 완료되었습니다."
    ONBOARDING_SUCCESS = "온보딩이 성공적으로 완료되었습니다."
    ONBOARDING_COMPLETE = "온보딩 완료"
    ONBOARDING_INCOMPLETE = "온보딩 미완료"
    DEFAULT_COMFORT_MESSAGE = "답변들이 저장되고 있습니다."
    
    STT_START = "🎤 전체 오디오 STT 처리 시작..."
    STT_COMPLETE = "✅ 전체 오디오 STT 처리 완료"
    STT_NO_FILES = "⚠️ 처리할 오디오 파일이 없습니다."
    STT_PROCESSING = "📝 {count}개의 오디오 파일 처리 중..."
    STT_QUESTION_SUCCESS = "✅ 질문 {question_num} STT 완료: {text}..."
    STT_QUESTION_FAILED = "❌ 질문 {question_num} STT 실패: {error}"
    STT_FAILED = "❌ 전체 오디오 STT 처리 실패: {error}"
    
    AUDIO_URI_SAVE_SUCCESS = "✅ 질문 {question_number} 오디오 URI 저장 완료: {audio_uri}"
    AUDIO_URI_SAVE_FAILED = "❌ 오디오 URI 저장 실패: {error}"
    
    USER_CREATED = "새 사용자 생성: {user_id}"
    CONVERSATION_CREATED = "새 Conversation 생성: {user_id} - {date} (한국 시간)"
    
    AUDIO_PROCESSING_FAILED = "❌ 오디오 답변 처리 실패: {error}"
    
    # 리포트 관련 성공 메시지
    REPORT_GENERATION_SUCCESS = "리포트 생성 및 저장 완료: user_id={user_id}"
    REPORT_SAVE_SUCCESS = "리포트 저장 완료 user_id={user_id} ts={timestamp}"
    
    # 사용자 관련 메시지
    USER_LAST_ACTIVE_DEBUG = "사용자 활동 시간 업데이트: user_id={user_id}"

# 에러 메시지 상수
class ErrorMessages:
    INVALID_QUESTION_NUMBER = "유효하지 않은 질문 번호입니다. (1-{max_questions})"
    QUESTION_NOT_FOUND = "질문 번호 {question_number}를 찾을 수 없습니다."
    UNSUPPORTED_AUDIO_FORMAT = "지원하지 않는 오디오 형식입니다. 지원 형식: {formats}"
    FILE_SIZE_EXCEEDED = "파일 크기가 {max_size}MB를 초과합니다."
    USER_NOT_FOUND = "사용자를 찾을 수 없습니다."
    AUDIO_FILE_NOT_FOUND = "오디오 파일을 찾을 수 없습니다."
    STT_TIMEOUT = "음성 변환 시간이 초과되었습니다."
    INVALID_API_KEY = "OpenAI API 키가 유효하지 않습니다."
    INVALID_GCS_URI = "잘못된 GCS URI 형식: {uri}"
    STT_CONVERSION_FAILED = "음성 변환 실패: {error}"
    ONBOARDING_PROCESSING_ERROR = "온보딩 처리 중 오류가 발생했습니다: {error}"
    ONBOARDING_STATUS_ERROR = "온보딩 상태 조회 중 오류가 발생했습니다: {error}"
    HISTORY_QUERY_ERROR = "기록 조회 중 오류가 발생했습니다: {error}"
    AUDIO_ANSWER_PROCESSING_ERROR = "오디오 답변 처리 중 오류가 발생했습니다: {error}"
    ENUM_VALIDATION_MISSING = "데이터 검증 실패: {field_name}이(가) 설정되지 않았습니다."
    ENUM_VALIDATION_INVALID = "데이터 검증 실패: {field_name}이(가) 올바른 Enum 타입이 아닙니다."
    
    # 리포트 관련 에러 메시지
    REPORT_EMPTY_RESPONSE = "리포트 응답이 비어있음"
    REPORT_SAVE_FAILED = "리포트 저장 실패: {error}"
    REPORT_GENERATION_FAILED = "리포트 생성 실패 (전체 프로세스는 계속): {error}"
    REPORT_GENERATION_EXCEPTION = "리포트 생성 예외 상세:"
    REPORT_SAVE_EXCEPTION = "리포트 저장 예외 상세:"
    
    # 사용자 관련 에러 메시지
    USER_LAST_ACTIVE_UPDATE_FAILED = "사용자 활동 시간 업데이트 실패: {error}"
    
    # 오디오 처리 관련 에러 메시지
    AUDIO_PROCESSING_EXCEPTION = "오디오 답변 처리 중 예외 발생:"

# 디폴트 값 상수
class Defaults:
    USER_CONVERSATIONS_COUNT = 0
    USER_ONBOARDED_STATUS = False
    CONVERSATION_PROCESSED_STATUS = True
    USER_MESSAGE_EMPTY = ""
    HISTORY_LIMIT = 10
    TEXT_PREVIEW_LENGTH = 50

# 파일 형식 상수
class FileFormats:
    DATE_FORMAT = "%Y-%m-%d"
    TEMP_FILE_PREFIX = "audio_"
    
# 타임존 상수
KOREA_TIMEZONE = "Asia/Seoul"

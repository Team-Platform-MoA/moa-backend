from typing import Dict, Optional
from app.core.constants import QUESTIONS

class QuestionService:
    """질문 관리 서비스"""
    
    @classmethod
    def get_question_text(cls, question_number: int) -> Optional[str]:
        """질문 번호로 질문 내용 조회"""
        return QUESTIONS.get(question_number)
    
    @classmethod
    def get_all_questions(cls) -> Dict[int, str]:
        """모든 질문 목록 반환"""
        return QUESTIONS.copy()
    
    @classmethod
    def is_valid_question_number(cls, question_number: int) -> bool:
        """유효한 질문 번호인지 확인"""
        return question_number in QUESTIONS
    
    @classmethod
    def get_total_questions(cls) -> int:
        """전체 질문 개수 반환"""
        return len(QUESTIONS)


question_service = QuestionService()

def get_question_service() -> QuestionService:
    """Question 서비스 인스턴스 반환"""
    return question_service

from typing import Dict, Optional
from app.core.constants import QUESTIONS, FAMILY_MEMBER_TITLES, DEFAULT_FAMILY_TITLE
from app.schemas.common import FamilyRelationship, Gender
from app.models.models import User

class QuestionService:
    """질문 관리 서비스"""
    
    @classmethod
    def get_question_text(cls, question_number: int, user: Optional[User] = None) -> Optional[str]:
        """질문 번호로 질문 내용 조회 (사용자 정보에 따라 동적 생성)"""
        question_template = QUESTIONS.get(question_number)
        if not question_template:
            return None

        if question_number == 1 and user:
            family_member = cls._get_family_member_title(user.family_relationship, user.family_member_gender)
            return question_template.format(family_member=family_member)
        
        return question_template
    
    @classmethod
    def _get_family_member_title(cls, relationship: FamilyRelationship, gender: Gender) -> str:
        """가족 관계와 성별에 따른 호칭 반환"""
        key = (relationship.value, gender.value)
        return FAMILY_MEMBER_TITLES.get(key, DEFAULT_FAMILY_TITLE)
    
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

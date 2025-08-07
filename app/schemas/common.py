from enum import Enum

class Gender(str, Enum):
    """성별 Enum"""
    FEMALE = "여성"
    MALE = "남성"
    OTHER = "기타"

class DementiaStage(str, Enum):
    """치매 정도 Enum"""
    EARLY = "초기"
    MIDDLE = "중기"
    LATE = "말기"

class FamilyRelationship(str, Enum):
    """가족 관계 Enum"""
    CHILD = "자녀"
    SPOUSE = "배우자"
    IN_LAW = "며느리/사위"
    GRANDCHILD = "손주"
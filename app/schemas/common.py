from enum import Enum

class DependentType(str, Enum):
    """사용자가 부양해야 할 가족의 유형 Enum"""
    MOTHER = "어머니"
    FATHER = "아버지"
    HUSBAND = "남편"
    WIFE = "아내"
    RELATIVE = "친척"
    IN_LAWS = "시부모님" 
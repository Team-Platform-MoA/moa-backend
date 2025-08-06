from enum import Enum

class CaregiverType(str, Enum):
    """부양자 유형 Enum"""
    MOTHER = "어머니"
    FATHER = "아버지"
    HUSBAND = "남편"
    WIFE = "아내"
    RELATIVE = "친척"
    IN_LAWS = "시부모님" 
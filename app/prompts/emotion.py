"""
감정 분석 프롬프트
"""
from app.prompts.base import BasePrompt


class EmotionAnalysisPrompt(BasePrompt):
    """감정 분석 프롬프트"""
    
    def generate(self, **kwargs) -> str:
        """
        감정 분석 프롬프트를 생성합니다.
        
        Args:
            text (str): 분석할 사용자의 발화 내용
            
        Returns:
            str: 완성된 프롬프트
        """
        text = kwargs.get("text", "")
        
        prompt = f"""
당신은 치매 환자를 돌보는 가족(부양자)의 감정을 이해하고 위로하는 심리상담가입니다.
아래 입력된 발화 내용은 치매 부양자가 일상에서 겪은 일이나 감정을 말한 것입니다.

1. 발화 내용을 분석하여 감정을 판별하세요.
2. 그 감정에 맞추어 깊이 공감하고, 부양자의 노고를 인정하며, 혼자가 아니라는 안도감을 줄 수 있는 위로 문구를 작성하세요.
3. 위로 문구는 진심이 느껴지고, 지나친 희망 고문이 되지 않도록 현실적인 언어를 사용하세요.
4. 치매 부양자의 정서적 소진을 완화하는 방향으로 작성하세요.

사용자의 발화: "{text}"

반드시 아래 JSON 형식으로만 응답하세요. 다른 텍스트는 포함하지 마세요:

{{
  "sentiment": "positive | neutral | negative",
  "score": -1.0 ~ 1.0,
  "comfort_message": "치매 부양자에게 보내는 맞춤형 위로 문구 (한글, 2~3문장)"
}}

예시:
{{
  "sentiment": "negative",
  "score": -0.8,
  "comfort_message": "하루하루가 지치고 무겁게 느껴질 수 있어요. 하지만 당신이 보여주는 사랑과 헌신은 분명 큰 의미가 있고, 혼자가 아니라는 것을 기억해 주세요."
}}

JSON 응답:"""
        
        return prompt
    
    def get_expected_format(self) -> str:
        """기대하는 응답 형식을 반환합니다."""
        return "json" 
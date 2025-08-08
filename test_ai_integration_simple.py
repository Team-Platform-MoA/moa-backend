#!/usr/bin/env python3
"""
AI 통합 테스트 스크립트 (간단 버전 - MongoDB 연결 없음)
"""
import asyncio
import json
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# MongoDB 관련 import 제거
import sys
sys.path.append('.')

from app.external.ai.client import get_ai_client
from app.prompts.emotion import EmotionAnalysisPrompt
from app.prompts.report import EmotionReportPrompt


async def test_report_generation():
    """리포트 생성 테스트"""
    print("\n🧪 리포트 생성 테스트 시작...")
    
    try:
        # AI 클라이언트 초기화
        ai_client = get_ai_client()
        
        # 테스트 데이터
        user_answers = {
            "memorable_moment": "어머니가 제 이름을 잠깐 기억하신 순간",
            "current_emotion": "희망과 절망 사이에서 갈등하는 마음",
            "message_to_self": "오늘도 잘 해냈어, 내일도 힘내자"
        }
        
        # 프롬프트 생성
        report_prompt = EmotionReportPrompt()
        prompt = report_prompt.generate(user_answers=user_answers)
        
        print(f"📝 생성된 프롬프트 길이: {len(prompt)} 문자")
        print("📝 프롬프트 미리보기:")
        print(prompt[:500] + "..." if len(prompt) > 500 else prompt)
        
        # AI 응답 생성
        result = await ai_client.generate_structured_content(prompt)
        
        print("✅ 리포트 생성 결과:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(f"❌ 리포트 생성 테스트 실패: {e}")
        import traceback
        traceback.print_exc()


async def test_ai_client_availability():
    """AI 클라이언트 사용 가능성 테스트"""
    print("🔍 AI 클라이언트 사용 가능성 테스트...")
    
    try:
        ai_client = get_ai_client()
        is_available = ai_client.is_available()
        
        print(f"✅ AI 클라이언트 사용 가능: {is_available}")
        
        if not is_available:
            print("⚠️  GEMINI_API_KEY가 설정되지 않았거나 클라이언트 초기화에 실패했습니다.")
            print("   .env 파일에 GEMINI_API_KEY를 설정해주세요.")
        
        return is_available
        
    except Exception as e:
        print(f"❌ AI 클라이언트 테스트 실패: {e}")
        return False


async def main():
    """메인 테스트 함수"""
    print("🚀 AI 통합 테스트 시작\n")
    
    # AI 클라이언트 사용 가능성 확인
    is_available = await test_ai_client_availability()
    
    if not is_available:
        print("\n❌ AI 클라이언트를 사용할 수 없습니다. 환경 변수를 확인해주세요.")
        return
    
    # 감정 분석 테스트
    await test_emotion_analysis()
    
    # 리포트 생성 테스트
    await test_report_generation()
    
    print("\n🎉 모든 테스트 완료!")


if __name__ == "__main__":
    asyncio.run(main()) 
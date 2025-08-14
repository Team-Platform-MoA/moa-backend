#!/usr/bin/env python3
"""
GPT AI 통합 테스트 스크립트
"""
import asyncio
import json
import traceback
from dotenv import load_dotenv

load_dotenv()

import sys
sys.path.append('.')

from app.external.ai.client import get_ai_client
from app.prompts.report import EmotionReportPrompt


async def test_gpt_client_availability():
    """GPT 클라이언트 사용 가능성 테스트"""
    print("🔍 GPT 클라이언트 사용 가능성 테스트...")

    try:
        ai_client = get_ai_client("openai")
        is_available = ai_client.is_available()
        print(f"✅ GPT 클라이언트 사용 가능: {is_available}")

        if not is_available:
            print("⚠️  OPENAI_API_KEY가 설정되지 않았거나 클라이언트 초기화에 실패했습니다.")
            print("    .env 파일에 OPENAI_API_KEY를 설정해주세요.")

        return is_available

    except Exception as e:
        print(f"❌ GPT 클라이언트 테스트 실패: {type(e).__name__} - {e}")
        traceback.print_exc()
        return False


async def test_gpt_report_generation():
    """GPT 리포트 생성 테스트"""
    print("\n🧪 GPT 리포트 생성 테스트 시작...")

    try:
        print("📡 GPT 클라이언트 초기화 중...")
        ai_client = get_ai_client("openai")
        print("✅ GPT 클라이언트 초기화 완료")

        user_answers = """Q1: 오늘 부양하면서 어떤 순간이 가장 기억에 남나요?
            A1: 어머니가 제 이름을 잠깐 기억하신 순간이었어요. 오랜만에 들어서 눈물이 났습니다.
            Q2: 지금 이 순간 마음속에서 가장 큰 감정은 무엇인가요?
            A2: 희망과 절망 사이에서 갈등하는 마음이에요. 감사함과 동시에 지친 마음도 있어요.
            Q3: 오늘 나 자신에게 해주고 싶은 말이 있다면?
            A3: 오늘도 잘 해냈어, 내일도 힘내자. 완벽하지 않아도 괜찮아."""

        print("🛠️ 프롬프트 생성 중...")
        report_prompt = EmotionReportPrompt()
        prompt = report_prompt.generate(user_answers=user_answers)

        print(f"📝 생성된 프롬프트 길이: {len(prompt)} 문자")
        print("📝 프롬프트 미리보기:")
        print(prompt[:300] + "..." if len(prompt) > 300 else prompt)

        print("\n🚀 GPT 응답 요청 중... (최대 30초 대기)")
        result = await asyncio.wait_for(
            ai_client.generate_structured_content(prompt),
            timeout=30
        )

        print("\n✅ GPT 리포트 생성 결과 수신 완료:")
        print(json.dumps(result, ensure_ascii=False, indent=2))

    except asyncio.TimeoutError:
        print("❌ [TimeoutError] 30초 안에 GPT 응답을 받지 못했습니다.")
        print("   프롬프트가 너무 복잡하거나 네트워크 상태를 확인해주세요.")
        print("   프롬프트 길이:", len(prompt), "문자")
        traceback.print_exc()

    except Exception as e:
        print(f"❌ [Exception] 알 수 없는 예외 발생: {type(e).__name__} - {e}")
        traceback.print_exc()

    except BaseException as be:
        print(f"❌ [BaseException] 치명적인 예외 발생: {type(be).__name__} - {be}")
        traceback.print_exc()

    finally:
        print("\n🔚 GPT 리포트 생성 테스트 종료")


async def test_gpt_simple_prompt():
    """GPT 간단한 프롬프트 테스트"""
    print("\n🧪 GPT 간단한 프롬프트 테스트...")

    try:
        print("📡 GPT 클라이언트 초기화 중...")
        ai_client = get_ai_client("openai")
        print("✅ GPT 클라이언트 초기화 완료")

        simple_prompt = """
"안녕하세요"라고 한국어로 인사해주세요.

JSON 형식으로 응답하세요:
{
  "greeting": "안녕하세요"
}
"""

        print(f"📝 프롬프트 길이: {len(simple_prompt)} 문자")
        print("📝 프롬프트 내용:")
        print(simple_prompt)

        print("\n🚀 GPT 응답 요청 중... (최대 15초 대기)")
        result = await asyncio.wait_for(
            ai_client.generate_structured_content(simple_prompt),
            timeout=15
        )

        print("\n✅ GPT 간단한 테스트 결과:")
        print(json.dumps(result, ensure_ascii=False, indent=2))

    except asyncio.TimeoutError:
        print("❌ [TimeoutError] 15초 안에 GPT 응답을 받지 못했습니다.")
        traceback.print_exc()

    except Exception as e:
        print(f"❌ [Exception] 예외 발생: {type(e).__name__} - {e}")
        traceback.print_exc()

    finally:
        print("\n🔚 GPT 간단한 테스트 종료")


async def main():
    print("🚀 GPT AI 통합 테스트 시작\n")

    try:
        is_available = await test_gpt_client_availability()

        if not is_available:
            print("\n⛔️ 테스트 중단: GPT 클라이언트를 사용할 수 없습니다.")
            return

        # 간단한 테스트 먼저
        await test_gpt_simple_prompt()
        
        # 리포트 생성 테스트
        await test_gpt_report_generation()

    except Exception as e:
        print(f"❌ [Main] 예기치 못한 에러 발생: {type(e).__name__} - {e}")
        traceback.print_exc()

    finally:
        print("\n🎉 모든 GPT 테스트 종료")


if __name__ == "__main__":
    asyncio.run(main()) 
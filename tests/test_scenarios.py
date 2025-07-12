"""
시나리오 테스트
- 다양한 채팅 시나리오 테스트
- 에러 처리 시나리오 테스트
- API Key 시나리오 테스트
"""

import unittest
from src.services.chat_service import ChatService
from src.dto.request_dto import ChatRequest
from src.exceptions.chat_exceptions import ValidationException, OpenAIClientException
from tests.test_input import get_test_max_tokens


class TestScenarios(unittest.TestCase):
    """시나리오 테스트 클래스"""
    
    def setUp(self):
        """테스트 설정"""
        self.chat_service = ChatService()
    
    def test_basic_conversation_scenario(self):
        """기본 대화 시나리오 테스트"""
        print("\n1. 기본 대화 시나리오 테스트")
        print("-" * 40)
        
        request = ChatRequest(
            user_message="안녕하세요",
            max_tokens=get_test_max_tokens(),
        )
        
        print(f"사용자: {request.user_message}")
        
        response = self.chat_service.process_chat_request(request)
        
        print(f"AI: {response.response_text}")
        print(f"응답 시간: {response.response_time:.2f}초")
        
        self.assertTrue(response.success)
        self.assertIsNotNone(response.response_text)
        
        print("[SUCCESS] 기본 대화 시나리오 성공")
    
    def test_role_based_conversation_scenario(self):
        """역할 기반 대화 시나리오 테스트"""
        print("\n2. 역할 기반 대화 시나리오 테스트")
        print("-" * 40)
        
        request = ChatRequest(
            user_message="파이썬을 가르쳐주세요",
            role="당신은 친근하고 이해하기 쉬운 프로그래밍 선생님입니다.",
            max_tokens=get_test_max_tokens(),
        )
        
        print(f"역할: {request.role}")
        print(f"사용자: {request.user_message}")
        
        response = self.chat_service.process_chat_request(request)
        
        print(f"AI: {response.response_text}")
        print(f"응답 시간: {response.response_time:.2f}초")
        
        self.assertTrue(response.success)
        self.assertIsNotNone(response.response_text)
        
        print("[SUCCESS] 역할 기반 대화 시나리오 성공")
    
    def test_memory_context_scenario(self):
        """메모리 컨텍스트 시나리오 테스트"""
        print("\n3. 메모리 컨텍스트 시나리오 테스트")
        print("-" * 40)
        
        request = ChatRequest(
            user_message="내가 좋아하는 색깔이 뭐였지?",
            memory_context=["사용자가 파란색을 좋아한다고 언급함"],
            max_tokens=get_test_max_tokens(),
        )
        
        print(f"메모리: {request.memory_context}")
        print(f"사용자: {request.user_message}")
        
        response = self.chat_service.process_chat_request(request)
        
        print(f"AI: {response.response_text}")
        print(f"응답 시간: {response.response_time:.2f}초")
        
        self.assertTrue(response.success)
        self.assertIsNotNone(response.response_text)
        
        print("[SUCCESS] 메모리 컨텍스트 시나리오 성공")
    
    def test_instruction_based_scenario(self):
        """지시사항 기반 시나리오 테스트"""
        print("\n4. 지시사항 기반 시나리오 테스트")
        print("-" * 40)
        
        request = ChatRequest(
            user_message="파이썬의 장점을 설명해주세요",
            instructions="간단하고 명확하게 3가지 장점만 설명해주세요.",
            max_tokens=get_test_max_tokens(),
        )
        
        print(f"지시사항: {request.instructions}")
        print(f"사용자: {request.user_message}")
        
        response = self.chat_service.process_chat_request(request)
        
        print(f"AI: {response.response_text}")
        print(f"응답 시간: {response.response_time:.2f}초")
        
        self.assertTrue(response.success)
        self.assertIsNotNone(response.response_text)
        
        print("[SUCCESS] 지시사항 기반 시나리오 성공")
    
    def test_conversation_history_scenario(self):
        """대화 히스토리 시나리오 테스트"""
        print("\n5. 대화 히스토리 시나리오 테스트")
        print("-" * 40)
        
        request = ChatRequest(
            user_message="그럼 자바는 어떤가요?",
            conversation_history=[
                "user: 파이썬에 대해 설명해주세요",
                "assistant: 파이썬은 간단하고 읽기 쉬운 프로그래밍 언어입니다."
            ],
            max_tokens=get_test_max_tokens(),
        )
        
        print(f"대화 히스토리: {request.conversation_history}")
        print(f"사용자: {request.user_message}")
        
        response = self.chat_service.process_chat_request(request)
        
        print(f"AI: {response.response_text}")
        print(f"응답 시간: {response.response_time:.2f}초")
        
        self.assertTrue(response.success)
        self.assertIsNotNone(response.response_text)
        
        print("[SUCCESS] 대화 히스토리 시나리오 성공")
    
    def test_complex_scenario(self):
        """복합 시나리오 테스트"""
        print("\n6. 복합 시나리오 테스트")
        print("-" * 40)
        
        request = ChatRequest(
            user_message="프로그래밍을 배우고 싶어요",
            role="당신은 경험이 풍부한 프로그래밍 멘토입니다.",
            instructions="초보자에게 친근하고 격려하는 톤으로 답해주세요.",
            memory_context=["사용자가 프로그래밍에 관심을 보임"],
            conversation_history=[
                "user: 안녕하세요",
                "assistant: 안녕하세요! 무엇을 도와드릴까요?"
            ],
            max_tokens=get_test_max_tokens(),
            use_user_api_key=False
        )
        
        print(f"역할: {request.role}")
        print(f"지시사항: {request.instructions}")
        print(f"메모리: {request.memory_context}")
        print(f"대화 히스토리: {request.conversation_history}")
        print(f"사용자: {request.user_message}")
        
        response = self.chat_service.process_chat_request(request)
        
        print(f"AI: {response.response_text}")
        print(f"응답 시간: {response.response_time:.2f}초")
        
        self.assertTrue(response.success)
        self.assertIsNotNone(response.response_text)
        
        print("[SUCCESS] 복합 시나리오 성공")
    
    def test_error_handling_scenario(self):
        """에러 처리 시나리오 테스트"""
        print("\n7. 에러 처리 시나리오 테스트")
        print("-" * 40)
        
        # 빈 메시지 테스트
        request = ChatRequest(
            user_message="",
            max_tokens=get_test_max_tokens(),
        )
        
        print("빈 메시지 테스트:")
        try:
            response = self.chat_service.process_chat_request(request)
            self.fail("빈 메시지에 대해 예외가 발생해야 합니다.")
        except ValidationException as e:
            print(f"예상된 예외 발생: {e.message}")
            self.assertEqual(e.field, "user_message")
        
        # 잘못된 max_tokens 테스트
        request = ChatRequest(
            user_message="테스트",
            max_tokens=-1,
        )
        
        print("잘못된 max_tokens 테스트:")
        try:
            response = self.chat_service.process_chat_request(request)
            self.fail("잘못된 max_tokens에 대해 예외가 발생해야 합니다.")
        except ValidationException as e:
            print(f"예상된 예외 발생: {e.message}")
            self.assertEqual(e.field, "max_tokens")
        
        print("[SUCCESS] 에러 처리 시나리오 성공")
    
    def test_api_key_and_use_user_api_key_scenarios(self):
        """API Key 및 사용자 API Key 시나리오 테스트"""
        print("\n8. API Key 및 사용자 API Key 시나리오 테스트")
        print("-" * 40)
        
        # 기본 API Key 사용 테스트
        request = ChatRequest(
            user_message="안녕하세요",
            max_tokens=get_test_max_tokens(),
        )
        
        print("기본 API Key 사용 테스트:")
        response = self.chat_service.process_chat_request(request)
        print(f"API Key 소스: {response.api_key_source}")
        self.assertTrue(response.success)
        
        # 사용자 API Key 사용 테스트 (유효하지 않은 키)
        request = ChatRequest(
            user_message="안녕하세요",
            openai_api_key="invalid-key",
            use_user_api_key=True,
            max_tokens=get_test_max_tokens()
        )
        
        print("사용자 API Key 사용 테스트 (유효하지 않은 키):")
        response = self.chat_service.process_chat_request(request)
        print(f"API Key 소스: {response.api_key_source}")
        self.assertTrue(response.success)
        
        # 일반 모드에서 유효하지 않은 키 사용 테스트
        request = ChatRequest(
            user_message="안녕하세요",
            openai_api_key="invalid-key",
            max_tokens=get_test_max_tokens()
        )
        
        print("일반 모드에서 유효하지 않은 키 사용 테스트:")
        try:
            response = self.chat_service.process_chat_request(request)
            self.fail("유효하지 않은 키에 대해 예외가 발생해야 합니다.")
        except OpenAIClientException as e:
            print(f"예상된 예외 발생: {e.message}")
        
        print("[SUCCESS] API Key 시나리오 테스트 성공")


def run_scenario_tests():
    """시나리오 테스트 실행"""
    print("🎭 시나리오 테스트 시작")
    print("=" * 50)
    
    # 테스트 스위트 생성
    test_suite = unittest.TestSuite()
    
    # 테스트 케이스들 추가
    test_suite.addTest(TestScenarios("test_basic_conversation_scenario"))
    test_suite.addTest(TestScenarios("test_role_based_conversation_scenario"))
    test_suite.addTest(TestScenarios("test_memory_context_scenario"))
    test_suite.addTest(TestScenarios("test_instruction_based_scenario"))
    test_suite.addTest(TestScenarios("test_conversation_history_scenario"))
    test_suite.addTest(TestScenarios("test_complex_scenario"))
    test_suite.addTest(TestScenarios("test_error_handling_scenario"))
    test_suite.addTest(TestScenarios("test_api_key_and_use_user_api_key_scenarios"))
    
    # 테스트 실행
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("✅ 모든 시나리오 테스트 통과!")
    else:
        print("❌ 일부 시나리오 테스트 실패")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    run_scenario_tests() 
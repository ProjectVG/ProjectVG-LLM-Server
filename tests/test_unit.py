"""
단위 테스트
- OpenAI 클라이언트 초기화 테스트
- 단순 채팅 요청 테스트
- 응답 시간 테스트
- 메모리 매개변수 테스트
- 지시사항 매개변수 테스트
- MAX_TOKEN 제한 테스트
- API Key 기능 테스트
- 사용자 API Key 기능 테스트
"""

import unittest
from src.services.chat_service import ChatService
from src.config import config
from tests.test_input import get_test_max_tokens


class TestUnit(unittest.TestCase):
    """단위 테스트 클래스"""
    
    def setUp(self):
        """테스트 설정"""
        self.chat_service = ChatService()
    
    def test_chat_service_initialization(self):
        """채팅 서비스 초기화 테스트"""
        print("\n1. 채팅 서비스 초기화 테스트")
        print("-" * 40)
        
        self.assertIsNotNone(self.chat_service)
        self.assertIsNotNone(self.chat_service.openai_client)
        
        print("[SUCCESS] 채팅 서비스 초기화 성공")
    
    def test_simple_chat_request(self):
        """단순 채팅 요청 테스트"""
        print("\n2. 단순 채팅 요청 테스트")
        print("-" * 40)
        
        from src.dto.request_dto import ChatRequest
        
        request = ChatRequest(
            user_prompt="안녕하세요",
            max_tokens=get_test_max_tokens(),
        )
        
        print(f"프롬프트: {request.user_prompt}")
        
        response = self.chat_service.process_chat_request(request)
        
        print(f"응답: {response.response_text}")
        print(f"응답 시간: {response.response_time:.2f}초")
        print(f"API Key 소스: {response.api_key_source}")
        
        self.assertIsNotNone(response)
        self.assertIsNotNone(response.response_text)
        self.assertGreater(len(response.response_text), 0)
        self.assertIsNotNone(response.api_key_source)
        
        print("[SUCCESS] 단순 채팅 요청 성공")
    
    def test_response_time(self):
        """응답 시간 테스트"""
        print("\n3. 응답 시간 테스트")
        print("-" * 40)
        
        from src.dto.request_dto import ChatRequest
        
        request = ChatRequest(
            user_prompt="안녕하세요",
            max_tokens=get_test_max_tokens(),
        )
        
        print(f"프롬프트: {request.user_prompt}")
        
        response = self.chat_service.process_chat_request(request)
        
        print(f"응답 시간: {response.response_time:.2f}초")
        
        self.assertIsNotNone(response.response_time)
        self.assertGreater(response.response_time, 0)
        self.assertLess(response.response_time, 30)
        
        print("[SUCCESS] 응답 시간 테스트 성공")
    
    def test_memory_parameter(self):
        """메모리 매개변수 테스트"""
        print("\n4. 메모리 매개변수 테스트")
        print("-" * 40)
        
        from src.dto.request_dto import ChatRoleRequest
        
        request = ChatRoleRequest(
            user_prompt="메모리에 뭐가 있어?",
            memory_context=["테스트 메모리"],
            max_tokens=get_test_max_tokens(),
        )
        
        print(f"메모리: {request.memory_context}")
        print(f"프롬프트: {request.user_prompt}")
        
        response = self.chat_service.process_chat_role_request(request)
        
        print(f"응답: {response.response_text}")
        print(f"응답 시간: {response.response_time:.2f}초")
        
        self.assertIsNotNone(response)
        self.assertIsNotNone(response.response_text)
        self.assertGreater(len(response.response_text), 0)
        
        print("[SUCCESS] 메모리 매개변수 테스트 성공")
    
    def test_instructions_parameter(self):
        """지시사항 매개변수 테스트"""
        print("\n5. 지시사항 매개변수 테스트")
        print("-" * 40)
        
        from src.dto.request_dto import ChatRequest
        
        request = ChatRequest(
            user_prompt="파이썬이 뭐야?",
            instructions="한 문장으로 답해주세요.",
            max_tokens=get_test_max_tokens(),
        )
        
        print(f"지시사항: {request.instructions}")
        print(f"프롬프트: {request.user_prompt}")
        
        response = self.chat_service.process_chat_request(request)
        
        print(f"응답: {response.response_text}")
        print(f"응답 시간: {response.response_time:.2f}초")
        
        self.assertIsNotNone(response)
        self.assertIsNotNone(response.response_text)
        self.assertGreater(len(response.response_text), 0)
        
        print("[SUCCESS] 지시사항 매개변수 테스트 성공")
    
    def test_max_token_limit(self):
        """MAX_TOKEN 제한 테스트"""
        print("\n6. MAX_TOKEN 제한 테스트")
        print("-" * 40)
        
        from src.dto.request_dto import ChatRequest
        
        request = ChatRequest(
            user_prompt="파이썬의 모든 특징과 장점을 자세히 설명해주세요. 가능한 한 길고 상세하게 설명해주세요.",
            max_tokens=16,  # OpenAI API 최소값
        )
        
        print(f"프롬프트: {request.user_prompt}")
        print(f"MAX_TOKEN 제한: {request.max_tokens}")
        
        response = self.chat_service.process_chat_request(request)
        
        response_length = len(response.response_text)
        
        print(f"응답: {response.response_text}")
        print(f"응답 길이: {response_length} 문자")
        print(f"응답 시간: {response.response_time:.2f}초")
        
        self.assertLessEqual(response_length, 50)
        
        print("[SUCCESS] MAX_TOKEN 제한 테스트 성공")
    
    def test_api_key_functionality(self):
        """API Key 기능 테스트"""
        print("\n7. API Key 기능 테스트")
        print("-" * 40)
        
        from src.dto.request_dto import ChatRequest
        
        # 테스트에서는 기본 API Key 사용
        request = ChatRequest(
            user_prompt="안녕하세요",
            max_tokens=get_test_max_tokens(),
        )
        
        response = self.chat_service.process_chat_request(request)
        
        print(f"기본 API Key 사용: {response.api_key_source}")
        self.assertIsNotNone(response.api_key_source)
        self.assertIn(response.api_key_source, ["default", "user_provided"])
        
        print("[SUCCESS] API Key 기능 테스트 성공")
    
    def test_use_user_api_key_functionality(self):
        """사용자 API Key 기능 테스트"""
        print("\n8. 사용자 API Key 기능 테스트")
        print("-" * 40)
        
        from src.dto.request_dto import ChatRequest
        
        request = ChatRequest(
            user_prompt="안녕하세요",
            max_tokens=get_test_max_tokens(),
        )
        
        response = self.chat_service.process_chat_request(request)
        
        print(f"API Key 소스: {response.api_key_source}")
        self.assertIsNotNone(response.api_key_source)
        self.assertTrue(response.success)
        
        print("[SUCCESS] 사용자 API Key 기능 테스트 성공")


def run_unit_tests():
    """단위 테스트 실행"""
    print("🧪 단위 테스트 시작")
    print("=" * 50)
    
    # 테스트 스위트 생성
    test_suite = unittest.TestSuite()
    
    # 테스트 케이스들 추가
    test_suite.addTest(TestUnit("test_chat_service_initialization"))
    test_suite.addTest(TestUnit("test_simple_chat_request"))
    test_suite.addTest(TestUnit("test_response_time"))
    test_suite.addTest(TestUnit("test_memory_parameter"))
    test_suite.addTest(TestUnit("test_instructions_parameter"))
    test_suite.addTest(TestUnit("test_max_token_limit"))
    test_suite.addTest(TestUnit("test_api_key_functionality"))
    test_suite.addTest(TestUnit("test_use_user_api_key_functionality"))
    
    # 테스트 실행
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("✅ 모든 단위 테스트 통과!")
    else:
        print("❌ 일부 단위 테스트 실패")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    run_unit_tests() 
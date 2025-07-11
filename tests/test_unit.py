"""
단위 테스트
- OpenAI 클라이언트 초기화 테스트
- 단순 채팅 요청 테스트
- 응답 시간 테스트
- 메모리 매개변수 테스트
- 지시사항 매개변수 테스트
- MAX_TOKEN 제한 테스트
"""

import unittest
from src.core.openai_client import OpenAIChatClient
from src.config import config
from tests.test_input import get_test_max_tokens


class TestUnit(unittest.TestCase):
    """단위 테스트 클래스"""
    
    def setUp(self):
        """테스트 설정"""
        api_key = config.get("OPENAI_API_KEY")
        if not api_key:
            self.skipTest("OPENAI_API_KEY가 설정되지 않았습니다.")
        
        self.client = OpenAIChatClient()
    
    def test_openai_client_initialization(self):
        """OpenAI 클라이언트 초기화 테스트"""
        print("\n1. OpenAI 클라이언트 초기화 테스트")
        print("-" * 40)
        
        self.assertIsNotNone(self.client.api_key)
        self.assertIsNotNone(self.client.client)
        
        print("[SUCCESS] OpenAI 클라이언트 초기화 성공")
    
    def test_simple_chat_request(self):
        """단순 채팅 요청 테스트"""
        print("\n2. 단순 채팅 요청 테스트")
        print("-" * 40)
        
        user_input = "안녕하세요"
        print(f"프롬프트: {user_input}")
        
        openai_response, response_time = self.client.chat(
            user_prompt=user_input, 
            memory=[],
            max_tokens=get_test_max_tokens()
        )
        
        response_text = openai_response.output_text
        print(f"응답: {response_text}")
        print(f"응답 시간: {response_time:.2f}초")
        
        self.assertIsNotNone(openai_response)
        self.assertIsNotNone(response_text)
        self.assertGreater(len(response_text), 0)
        
        print("[SUCCESS] 단순 채팅 요청 성공")
    
    def test_response_time(self):
        """응답 시간 테스트"""
        print("\n3. 응답 시간 테스트")
        print("-" * 40)
        
        user_input = "안녕하세요"
        print(f"프롬프트: {user_input}")
        
        openai_response, response_time = self.client.chat(
            user_prompt=user_input, 
            memory=[],
            max_tokens=get_test_max_tokens()
        )
        
        print(f"응답 시간: {response_time:.2f}초")
        
        self.assertIsNotNone(response_time)
        self.assertGreater(response_time, 0)
        self.assertLess(response_time, 30)
        
        print("[SUCCESS] 응답 시간 테스트 성공")
    
    def test_memory_parameter(self):
        """메모리 매개변수 테스트"""
        print("\n4. 메모리 매개변수 테스트")
        print("-" * 40)
        
        memory = ["테스트 메모리"]
        user_input = "메모리에 뭐가 있어?"
        
        print(f"메모리: {memory}")
        print(f"프롬프트: {user_input}")
        
        openai_response, response_time = self.client.chat(
            user_prompt=user_input, 
            memory=memory,
            max_tokens=get_test_max_tokens()
        )
        
        response_text = openai_response.output_text
        print(f"응답: {response_text}")
        print(f"응답 시간: {response_time:.2f}초")
        
        self.assertIsNotNone(openai_response)
        self.assertIsNotNone(response_text)
        self.assertGreater(len(response_text), 0)
        
        print("[SUCCESS] 메모리 매개변수 테스트 성공")
    
    def test_instructions_parameter(self):
        """지시사항 매개변수 테스트"""
        print("\n5. 지시사항 매개변수 테스트")
        print("-" * 40)
        
        instructions = "한 문장으로 답해주세요."
        user_input = "파이썬이 뭐야?"
        
        print(f"지시사항: {instructions}")
        print(f"프롬프트: {user_input}")
        
        openai_response, response_time = self.client.chat(
            user_prompt=user_input, 
            memory=[],
            instructions=instructions,
            max_tokens=get_test_max_tokens()
        )
        
        response_text = openai_response.output_text
        print(f"응답: {response_text}")
        print(f"응답 시간: {response_time:.2f}초")
        
        self.assertIsNotNone(openai_response)
        self.assertIsNotNone(response_text)
        self.assertGreater(len(response_text), 0)
        
        print("[SUCCESS] 지시사항 매개변수 테스트 성공")
    
    def test_max_token_limit(self):
        """MAX_TOKEN 제한 테스트"""
        print("\n6. MAX_TOKEN 제한 테스트")
        print("-" * 40)
        
        user_input = "파이썬의 모든 특징과 장점을 자세히 설명해주세요. 가능한 한 길고 상세하게 설명해주세요."
        max_tokens = 16  # OpenAI API 최소값
        
        print(f"프롬프트: {user_input}")
        print(f"MAX_TOKEN 제한: {max_tokens}")
        
        openai_response, response_time = self.client.chat(
            user_prompt=user_input, 
            memory=[],
            max_tokens=max_tokens
        )
        
        response_text = openai_response.output_text
        response_length = len(response_text)
        
        print(f"응답: {response_text}")
        print(f"응답 길이: {response_length} 문자")
        print(f"응답 시간: {response_time:.2f}초")
        
        self.assertLessEqual(response_length, 50)
        
        print("[SUCCESS] MAX_TOKEN 제한 테스트 성공")


def run_unit_tests():
    """단위 테스트 실행"""
    print("=" * 60)
    print("단위 테스트 시작")
    print("=" * 60)
    
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestUnit)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    print("=" * 60)
    print("단위 테스트 결과:")
    print(f"실행된 테스트: {result.testsRun}")
    print(f"성공: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"실패: {len(result.failures)}")
    print(f"오류: {len(result.errors)}")
    print("=" * 60)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    run_unit_tests() 
import unittest
from src.core.openai_client import OpenAIChatClient
from src.config import config
from input import get_test_memory, get_test_inputs, get_instructions


class TestSimpleRequest(unittest.TestCase):
    """단순 요청 테스트 클래스"""
    
    def setUp(self):
        """테스트 설정"""
        # 테스트용 메모리
        self.test_memory = get_test_memory()
    
    def test_openai_client_initialization(self):
        """OpenAI 클라이언트 초기화 테스트"""
        api_key = config.get("OPENAI_API_KEY")
        if not api_key:
            self.skipTest("OPENAI_API_KEY가 설정되지 않았습니다.")
        
        client = OpenAIChatClient()
        
        self.assertIsNotNone(client.api_key)
        self.assertIsNotNone(client.model)
        self.assertIsNotNone(client.client)
        
        print("OpenAI 클라이언트 초기화 성공")
    
    def test_simple_chat_request(self):
        """단순 채팅 요청 테스트"""
        api_key = config.get("OPENAI_API_KEY")
        if not api_key:
            self.skipTest("OPENAI_API_KEY가 설정되지 않았습니다.")
        
        client = OpenAIChatClient()
        
        user_input = "안녕하세요"
        reply, response = client.chat(user_input, memory=self.test_memory)
        
        self.assertIsNotNone(reply)
        self.assertIsInstance(reply, str)
        self.assertGreater(len(reply), 0)
        
        print(f"채팅 요청 성공: {reply[:50]}...")
    
    def test_multiple_chat_requests(self):
        """여러 채팅 요청 테스트"""
        api_key = config.get("OPENAI_API_KEY")
        if not api_key:
            self.skipTest("OPENAI_API_KEY가 설정되지 않았습니다.")
        
        client = OpenAIChatClient()
        
        test_inputs = get_test_inputs()
        
        for i, user_input in enumerate(test_inputs[:3]):  # 처음 3개만 테스트
            print(f"테스트 {i+1}: {user_input}")
            
            reply, response = client.chat(user_input, memory=self.test_memory)
            
            self.assertIsNotNone(reply)
            self.assertIsInstance(reply, str)
            self.assertGreater(len(reply), 0)
            
            print(f"응답: {reply[:50]}...")
    
    def test_chat_with_instructions(self):
        """지시사항이 포함된 채팅 테스트"""
        api_key = config.get("OPENAI_API_KEY")
        if not api_key:
            self.skipTest("OPENAI_API_KEY가 설정되지 않았습니다.")
        
        client = OpenAIChatClient()
        
        user_input = "파이썬에 대해 설명해줘"
        instructions = get_instructions()[0]
        
        reply, response = client.chat(
            user_input, 
            instructions=instructions,
            memory=self.test_memory
        )
        
        self.assertIsNotNone(reply)
        self.assertIsInstance(reply, str)
        self.assertGreater(len(reply), 0)
        
        print(f"지시사항 포함 채팅 성공: {reply[:50]}...")
    
    def test_response_time(self):
        """응답 시간 테스트"""
        api_key = config.get("OPENAI_API_KEY")
        if not api_key:
            self.skipTest("OPENAI_API_KEY가 설정되지 않았습니다.")
        
        client = OpenAIChatClient()
        
        user_input = "안녕하세요"
        reply, response = client.chat(user_input, memory=self.test_memory)
        
        self.assertIsNotNone(response.response_time)
        self.assertGreater(response.response_time, 0)
        self.assertLess(response.response_time, 30)
        
        print(f"응답 시간: {response.response_time:.2f}초")


def run_simple_request_tests():
    """단순 요청 테스트 실행"""
    print("단순 요청 테스트 시작")
    
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestSimpleRequest)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    print(f"\n테스트 결과:")
    print(f"실행된 테스트: {result.testsRun}")
    print(f"성공: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"실패: {len(result.failures)}")
    print(f"오류: {len(result.errors)}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    run_simple_request_tests() 
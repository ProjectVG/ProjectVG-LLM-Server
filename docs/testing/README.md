# LLM Server 테스트 및 품질 관리 가이드

이 문서는 LLM Server의 테스트 코드 작성, 실행, 그리고 품질 관리에 대한 상세한 가이드를 제공합니다.

## 🧪 테스트 개요

### 테스트 전략

1. **단위 테스트 (Unit Tests)** - 개별 함수/클래스 테스트
2. **시나리오 테스트 (Scenario Tests)** - 비즈니스 시나리오 테스트
3. **입력 검증 테스트 (Input Validation Tests)** - 입력 데이터 검증 테스트
4. **성능 테스트 (Performance Tests)** - 성능 및 부하 테스트

### 테스트 도구

- **unittest**: Python 기본 테스트 프레임워크
- **pytest**: Python 테스트 프레임워크 (선택사항)
- **httpx**: 비동기 HTTP 클라이언트 (API 테스트)
- **pytest-asyncio**: 비동기 테스트 지원

---

## 📁 테스트 구조

### 프로젝트 테스트 구조

```
tests/
├── __init__.py
├── test_unit.py          # 단위 테스트
├── test_scenarios.py     # 시나리오 테스트
├── test_input.py         # 입력 검증 테스트
└── run_tests.py          # 테스트 실행 스크립트
```

### 테스트 파일 명명 규칙

- `test_*.py`: 테스트 파일
- `test_*`: 테스트 함수
- `Test*`: 테스트 클래스

---

## 🔧 단위 테스트

### 1. 서비스 레이어 테스트

#### ChatService 테스트

```python
import unittest
from src.services.chat_service import ChatService
from src.dto.request_dto import ChatRequest
from src.dto.response_dto import ChatResponse

class TestUnit(unittest.TestCase):
    """단위 테스트 클래스"""
    
    def setUp(self):
        """테스트 설정"""
        self.chat_service = ChatService()
    
    def test_chat_service_initialization(self):
        """채팅 서비스 초기화 테스트"""
        self.assertIsNotNone(self.chat_service)
        self.assertIsNotNone(self.chat_service.openai_client)
    
    def test_simple_chat_request(self):
        """단순 채팅 요청 테스트"""
        request = ChatRequest(
            user_message="안녕하세요",
            max_tokens=100,
            free_mode=True
        )
        
        response = self.chat_service.process_chat_request(request)
        
        self.assertIsNotNone(response)
        self.assertIsNotNone(response.response_text)
        self.assertGreater(len(response.response_text), 0)
        self.assertIsNotNone(response.api_key_source)
    
    def test_response_time(self):
        """응답 시간 테스트"""
        request = ChatRequest(
            user_message="안녕하세요",
            max_tokens=100,
            free_mode=True
        )
        
        response = self.chat_service.process_chat_request(request)
        
        self.assertIsNotNone(response.response_time)
        self.assertGreater(response.response_time, 0)
        self.assertLess(response.response_time, 30)
    
    def test_memory_parameter(self):
        """메모리 매개변수 테스트"""
        request = ChatRequest(
            user_message="메모리에 뭐가 있어?",
            memory_context=["테스트 메모리"],
            max_tokens=100,
            free_mode=True
        )
        
        response = self.chat_service.process_chat_request(request)
        
        self.assertIsNotNone(response)
        self.assertIsNotNone(response.response_text)
        self.assertGreater(len(response.response_text), 0)
    
    def test_instructions_parameter(self):
        """지시사항 매개변수 테스트"""
        request = ChatRequest(
            user_message="파이썬이 뭐야?",
            instructions="한 문장으로 답해주세요.",
            max_tokens=100,
            free_mode=True
        )
        
        response = self.chat_service.process_chat_request(request)
        
        self.assertIsNotNone(response)
        self.assertIsNotNone(response.response_text)
        self.assertGreater(len(response.response_text), 0)
    
    def test_max_token_limit(self):
        """MAX_TOKEN 제한 테스트"""
        request = ChatRequest(
            user_message="파이썬의 모든 특징과 장점을 자세히 설명해주세요.",
            max_tokens=16,  # OpenAI API 최소값
            free_mode=True
        )
        
        response = self.chat_service.process_chat_request(request)
        response_length = len(response.response_text)
        
        self.assertLessEqual(response_length, 50)
    
    def test_api_key_functionality(self):
        """API Key 기능 테스트"""
        request = ChatRequest(
            user_message="안녕하세요",
            max_tokens=100,
            free_mode=True
        )
        
        response = self.chat_service.process_chat_request(request)
        
        self.assertIsNotNone(response.api_key_source)
        self.assertIn(response.api_key_source, ["default", "user_provided"])
    
    def test_free_mode_functionality(self):
        """Free 모드 기능 테스트"""
        request = ChatRequest(
            user_message="안녕하세요",
            max_tokens=100,
            free_mode=True
        )
        
        response = self.chat_service.process_chat_request(request)
        
        self.assertIsNotNone(response.api_key_source)
        self.assertTrue(response.success)
```

### 2. DTO 테스트

#### ChatRequest 검증 테스트

```python
import unittest
from src.dto.request_dto import ChatRequest

class TestChatRequest(unittest.TestCase):
    def test_valid_request(self):
        """유효한 요청 테스트"""
        request = ChatRequest(
            session_id="test_session",
            user_message="안녕하세요",
            max_tokens=1000,
            temperature=0.7
        )
        
        assert request.session_id == "test_session"
        assert request.user_message == "안녕하세요"
        assert request.max_tokens == 1000
        assert request.temperature == 0.7
    
    def test_conversation_history_format(self):
        """대화 히스토리 형식 테스트"""
        request = ChatRequest(
            user_message="테스트",
            conversation_history=["user:안녕하세요", "assistant:안녕하세요!"]
        )
        assert len(request.conversation_history) == 2
    
    def test_memory_context(self):
        """메모리 컨텍스트 테스트"""
        request = ChatRequest(
            user_message="테스트",
            memory_context=["사용자는 개발자입니다", "파이썬에 관심이 있습니다"]
        )
        assert len(request.memory_context) == 2
```

### 3. OpenAI 클라이언트 테스트

#### OpenAIClient 테스트

```python
import unittest
from unittest.mock import Mock, patch
from src.external.openai_client import OpenAIClient

class TestOpenAIClient(unittest.TestCase):
    def setUp(self):
        """테스트 설정"""
        self.client = OpenAIClient()
    
    def test_client_initialization(self):
        """클라이언트 초기화 테스트"""
        self.assertIsNotNone(self.client)
    
    @patch('openai.OpenAI')
    def test_generate_response_success(self, mock_openai):
        """성공적인 응답 생성 테스트"""
        # Mock 설정
        mock_response = Mock()
        mock_response.output_text = "테스트 응답"
        mock_response.model = "gpt-4o-mini"
        mock_response.usage.input_tokens = 10
        mock_response.usage.output_tokens = 5
        mock_response.usage.total_tokens = 15
        mock_response.text.format.type = "text"
        mock_response.created_at = 1234567890
        mock_response.temperature = 0.7
        
        mock_client = Mock()
        mock_client.responses.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        # 테스트 실행
        messages = [{"role": "user", "content": "테스트"}]
        response, response_time, api_key_source = self.client.generate_response(
            messages=messages,
            free_mode=True
        )
        
        # 검증
        self.assertEqual(response.output_text, "테스트 응답")
        self.assertIsNotNone(response_time)
        self.assertIsNotNone(api_key_source)
```

---

## 🎭 시나리오 테스트

### 1. 대화 지속성 테스트

```python
import unittest
from src.services.chat_service import ChatService
from src.dto.request_dto import ChatRequest

class TestScenarios(unittest.TestCase):
    """시나리오 테스트 클래스"""
    
    def setUp(self):
        """테스트 설정"""
        self.chat_service = ChatService()
        self.conversation_history = []
    
    def test_conversation_continuity(self):
        """대화 지속 테스트 - 첫 번째 대화에서 지시사항을 주고 두 번째 대화에서 확인"""
        history = []
        
        # 첫 번째 대화
        first_prompt = "다음 숫자를 기억하고 있어라. 68"
        request1 = ChatRequest(
            user_message=first_prompt,
            max_tokens=100,
            free_mode=True
        )
        
        response1 = self.chat_service.process_chat_request(request1)
        response_text = response1.response_text
        
        # history에 첫 번째 대화 추가
        history.append(f"user:{first_prompt}")
        history.append(f"assistant:{response_text}")
        
        # 두 번째 대화: 지시사항 확인
        second_prompt = "지금 방금 기억한 숫자는?"
        request2 = ChatRequest(
            user_message=second_prompt,
            conversation_history=history,
            max_tokens=100,
            free_mode=True
        )
        
        response2 = self.chat_service.process_chat_request(request2)
        response2_text = response2.response_text
        
        # 결과 검증
        self.assertIn("68", response2_text, "AI가 이전 지시사항을 기억하지 못함")
    
    def test_memory_functionality(self):
        """메모리 기능 테스트 - 메모리에 정보를 넣고 질문으로 확인"""
        # 메모리에 정보 추가
        memory = ["유저가 좋아하는 꽃은 백합이다."]
        prompt = "내가 좋아하는 꽃은?"
        
        request = ChatRequest(
            user_message=prompt,
            memory_context=memory,
            max_tokens=100,
            free_mode=True
        )
        
        response = self.chat_service.process_chat_request(request)
        
        # 결과 검증
        self.assertIn("백합", response.response_text, "AI가 메모리 정보를 활용하지 못함")
    
    def test_system_message(self):
        """시스템 메시지 테스트"""
        system_message = "말끝 뒤에 항상 냥을 붙여라"
        prompt = "안녕하세요"
        
        request = ChatRequest(
            user_message=prompt,
            system_message=system_message,
            max_tokens=100,
            free_mode=True
        )
        
        response = self.chat_service.process_chat_request(request)
        
        # 결과 검증
        self.assertIn("냥", response.response_text, "AI가 시스템 메시지를 따르지 않음")
    
    def test_instructions_format(self):
        """Instructions 테스트"""
        instructions = "응답 메시지는 항상 'assistance: (메시지)' 형태로 주어져야한다."
        prompt = "파이썬이 뭐야?"
        
        request = ChatRequest(
            user_message=prompt,
            instructions=instructions,
            max_tokens=100,
            free_mode=True
        )
        
        response = self.chat_service.process_chat_request(request)
        
        # 결과 검증
        self.assertTrue(
            response.response_text.strip().lower().startswith("assistance:"),
            "AI가 지정된 형식을 따르지 않음"
        )
```

### 2. 다중 대화 시나리오 테스트

```python
def test_multiple_conversation_scenario(self):
    """다중 대화 시나리오 테스트"""
    test_inputs = [
        "안녕하세요",
        "파이썬에 대해 알려주세요",
        "그럼 자바스크립트는?"
    ]
    memory = ["사용자는 프로그래밍에 관심이 있습니다"]
    
    for i, user_input in enumerate(test_inputs):
        request = ChatRequest(
            user_message=user_input,
            memory_context=memory,
            max_tokens=100,
            free_mode=True
        )
        
        response = self.chat_service.process_chat_request(request)
        
        # 기본 검증
        self.assertIsNotNone(response.response_text)
        self.assertGreater(len(response.response_text), 0)
        self.assertIsNotNone(response.api_key_source)
```

### 3. 성능 시나리오 테스트

```python
def test_performance_scenario(self):
    """성능 시나리오 테스트"""
    long_prompt = "파이썬의 모든 특징과 장점을 자세히 설명해주세요. " * 10
    
    request = ChatRequest(
        user_message=long_prompt,
        max_tokens=500,
        free_mode=True
    )
    
    response = self.chat_service.process_chat_request(request)
    
    # 성능 검증
    self.assertLess(response.response_time, 30)  # 30초 이내 응답
    self.assertGreater(len(response.response_text), 100)  # 충분한 응답 길이
```

---

## 🔍 입력 검증 테스트

### 1. 입력 데이터 검증

```python
import unittest
from src.dto.request_dto import ChatRequest
from src.exceptions.chat_exceptions import ValidationException

class TestInput(unittest.TestCase):
    def test_empty_user_message(self):
        """빈 사용자 메시지 검증"""
        request = ChatRequest(user_message="")
        
        # ChatService에서 검증
        from src.services.chat_service import ChatService
        service = ChatService()
        
        with self.assertRaises(ValidationException):
            service.process_chat_request(request)
    
    def test_invalid_max_tokens(self):
        """잘못된 max_tokens 검증"""
        request = ChatRequest(
            user_message="테스트",
            max_tokens=-1
        )
        
        service = ChatService()
        
        with self.assertRaises(ValidationException):
            service.process_chat_request(request)
    
    def test_invalid_temperature(self):
        """잘못된 temperature 검증"""
        request = ChatRequest(
            user_message="테스트",
            temperature=3.0
        )
        
        service = ChatService()
        
        with self.assertRaises(ValidationException):
            service.process_chat_request(request)
```

### 2. API Key 검증

```python
def test_api_key_validation(self):
    """API Key 검증 테스트"""
    # 유효하지 않은 API Key
    request = ChatRequest(
        user_message="테스트",
        openai_api_key="invalid-key",
        free_mode=False
    )
    
    service = ChatService()
    
    with self.assertRaises(Exception):  # ConfigurationException 또는 OpenAIClientException
        service.process_chat_request(request)
```

---

## 🚀 테스트 실행

### 1. 개별 테스트 실행

```bash
# 단위 테스트 실행
python -m unittest tests.test_unit

# 시나리오 테스트 실행
python -m unittest tests.test_scenarios

# 입력 검증 테스트 실행
python -m unittest tests.test_input
```

### 2. 전체 테스트 실행

```bash
# 모든 테스트 실행
python run_tests.py

# 또는
python -m unittest discover tests
```

### 3. 테스트 실행 스크립트

```python
# run_tests.py
import unittest
import sys
import os

# 테스트 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.test_unit import TestUnit
from tests.test_scenarios import TestScenarios
from tests.test_input import TestInput

def run_all_tests():
    """모든 테스트 실행"""
    # 테스트 스위트 생성
    test_suite = unittest.TestSuite()
    
    # 단위 테스트 추가
    test_suite.addTest(unittest.makeSuite(TestUnit))
    
    # 시나리오 테스트 추가
    test_suite.addTest(unittest.makeSuite(TestScenarios))
    
    # 입력 검증 테스트 추가
    test_suite.addTest(unittest.makeSuite(TestInput))
    
    # 테스트 실행
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
```

---

## 📊 테스트 결과 분석

### 1. 테스트 커버리지

```bash
# pytest-cov를 사용한 커버리지 측정
pip install pytest-cov

# 커버리지 측정
pytest --cov=src tests/
```

### 2. 성능 테스트

```python
import time
import statistics

def performance_test():
    """성능 테스트"""
    response_times = []
    
    for i in range(10):
        start_time = time.time()
        
        # 테스트 요청
        request = ChatRequest(
            user_message="안녕하세요",
            max_tokens=100,
            free_mode=True
        )
        
        response = chat_service.process_chat_request(request)
        
        end_time = time.time()
        response_times.append(end_time - start_time)
    
    # 통계 계산
    avg_time = statistics.mean(response_times)
    max_time = max(response_times)
    min_time = min(response_times)
    
    print(f"평균 응답 시간: {avg_time:.2f}초")
    print(f"최대 응답 시간: {max_time:.2f}초")
    print(f"최소 응답 시간: {min_time:.2f}초")
```

---

## 🔧 테스트 환경 설정

### 1. 테스트 환경 변수

```bash
# .env.test 파일
OPENAI_API_KEY=test-api-key
SERVER_HOST=0.0.0.0
SERVER_PORT=5601
LOG_LEVEL=DEBUG
LOG_FILE=logs/test.log
```

### 2. 테스트 데이터

```python
# tests/test_input.py
def get_test_max_tokens():
    """테스트용 최대 토큰 수 반환"""
    return 100

def get_performance_test_max_tokens():
    """성능 테스트용 최대 토큰 수 반환"""
    return 500

def get_test_inputs():
    """테스트용 입력 데이터 반환"""
    return [
        "안녕하세요",
        "파이썬에 대해 알려주세요",
        "그럼 자바스크립트는?",
        "프로그래밍 언어의 장점은?"
    ]

def get_test_memory():
    """테스트용 메모리 데이터 반환"""
    return [
        "사용자는 프로그래밍에 관심이 있습니다",
        "사용자는 학습에 열정적입니다"
    ]
```

---

## 🚨 문제 해결

### 1. 일반적인 테스트 문제

#### API Key 문제
```python
# Free 모드 사용으로 해결
request = ChatRequest(
    user_message="테스트",
    free_mode=True  # 기본 API Key 사용
)
```

#### 네트워크 연결 문제
```python
# Mock 사용으로 해결
@patch('openai.OpenAI')
def test_with_mock(self, mock_openai):
    # Mock 설정
    mock_response = Mock()
    mock_response.output_text = "테스트 응답"
    # ... 기타 Mock 설정
```

### 2. 테스트 디버깅

```python
def test_with_debugging(self):
    """디버깅이 포함된 테스트"""
    try:
        request = ChatRequest(
            user_message="테스트",
            free_mode=True
        )
        
        response = chat_service.process_chat_request(request)
        
        print(f"응답: {response.response_text}")
        print(f"응답 시간: {response.response_time}")
        print(f"API Key 소스: {response.api_key_source}")
        
        self.assertIsNotNone(response.response_text)
        
    except Exception as e:
        print(f"테스트 실패: {e}")
        raise
```

---

## 🔗 관련 문서

- **[개요 및 시작 가이드](./../overview/README.md)**: 프로젝트 소개 및 기본 사용법
- **[API 문서](./../api/README.md)**: API 명세 및 사용법
- **[아키텍처 가이드](./../architecture/README.md)**: 프로젝트 구조 및 개발 가이드
- **[배포 가이드](./../deployment/README.md)**: 배포 및 운영 가이드

---

**문서 버전**: 1.0  
**최종 업데이트**: 2024년 12월  
**작성자**: LLM Server 개발팀 
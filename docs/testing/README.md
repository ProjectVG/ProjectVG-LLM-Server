# LLM Server 테스트 및 품질 관리 가이드

이 문서는 LLM Server의 테스트 코드 작성, 실행, 그리고 품질 관리에 대한 상세한 가이드를 제공합니다.

## 🧪 테스트 개요

### 테스트 전략

1. **단위 테스트 (Unit Tests)** - 개별 함수/클래스 테스트
2. **통합 테스트 (Integration Tests)** - API 엔드포인트 테스트
3. **시나리오 테스트 (Scenario Tests)** - 비즈니스 시나리오 테스트
4. **성능 테스트 (Performance Tests)** - 성능 및 부하 테스트

### 테스트 도구

- **pytest**: Python 테스트 프레임워크
- **httpx**: 비동기 HTTP 클라이언트 (API 테스트)
- **pytest-asyncio**: 비동기 테스트 지원
- **pytest-mock**: Mock 객체 지원

---

## 📁 테스트 구조

### 프로젝트 테스트 구조

```
tests/
├── __init__.py
├── test_unit.py          # 단위 테스트
├── test_integration.py   # 통합 테스트
├── test_scenarios.py     # 시나리오 테스트
├── conftest.py          # pytest 설정
└── fixtures/            # 테스트 픽스처
    ├── __init__.py
    ├── mock_data.py     # Mock 데이터
    └── test_utils.py    # 테스트 유틸리티
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
import pytest
from unittest.mock import Mock, AsyncMock
from src.services.chat_service import ChatService
from src.dto.request_dto import ChatRequest
from src.dto.response_dto import ChatResponse

class TestChatService:
    @pytest.fixture
    def mock_openai_client(self):
        """OpenAI 클라이언트 Mock 객체"""
        mock_client = Mock()
        mock_client.chat_completion = AsyncMock()
        return mock_client
    
    @pytest.fixture
    def chat_service(self, mock_openai_client):
        """ChatService 인스턴스"""
        return ChatService(mock_openai_client)
    
    @pytest.fixture
    def sample_request(self):
        """샘플 채팅 요청"""
        return ChatRequest(
            session_id="test_session",
            user_message="안녕하세요",
            role="친근한 AI 어시스턴트",
            max_tokens=100,
            temperature=0.7
        )
    
    @pytest.mark.asyncio
    async def test_process_chat_success(self, chat_service, mock_openai_client, sample_request):
        """성공적인 채팅 처리 테스트"""
        # Given
        expected_response = Mock()
        expected_response.choices = [Mock()]
        expected_response.choices[0].message.content = "안녕하세요! 무엇을 도와드릴까요?"
        expected_response.usage.total_tokens = 50
        
        mock_openai_client.chat_completion.return_value = expected_response
        
        # When
        result = await chat_service.process_chat(sample_request)
        
        # Then
        assert result.success is True
        assert result.response_text == "안녕하세요! 무엇을 도와드릴까요?"
        assert result.total_tokens_used == 50
        assert result.session_id == "test_session"
        mock_openai_client.chat_completion.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_process_chat_openai_error(self, chat_service, mock_openai_client, sample_request):
        """OpenAI API 오류 처리 테스트"""
        # Given
        mock_openai_client.chat_completion.side_effect = Exception("API 오류")
        
        # When & Then
        with pytest.raises(Exception):
            await chat_service.process_chat(sample_request)
    
    def test_build_context_with_history(self, chat_service, sample_request):
        """대화 히스토리가 포함된 컨텍스트 구성 테스트"""
        # Given
        sample_request.conversation_history = [
            "user:안녕하세요",
            "assistant:안녕하세요! 무엇을 도와드릴까요?",
            "user:파이썬에 대해 알려주세요"
        ]
        
        # When
        context = chat_service._build_context(sample_request)
        
        # Then
        assert len(context.messages) == 5  # 시스템 + 히스토리 3개 + 현재 메시지
        assert context.messages[0]["role"] == "system"
        assert context.messages[1]["role"] == "user"
        assert context.messages[2]["role"] == "assistant"
        assert context.messages[3]["role"] == "user"
        assert context.messages[4]["role"] == "user"
    
    def test_build_context_with_memory(self, chat_service, sample_request):
        """메모리 컨텍스트가 포함된 컨텍스트 구성 테스트"""
        # Given
        sample_request.memory_context = [
            "사용자는 개발자입니다",
            "사용자는 파이썬에 관심이 있습니다"
        ]
        
        # When
        context = chat_service._build_context(sample_request)
        
        # Then
        assert len(context.messages) == 3  # 시스템(메모리) + 시스템(역할) + 사용자
        assert "기억: 사용자는 개발자입니다" in context.messages[0]["content"]
        assert "사용자는 파이썬에 관심이 있습니다" in context.messages[0]["content"]
```

### 2. DTO 테스트

#### ChatRequest 검증 테스트

```python
import pytest
from pydantic import ValidationError
from src.dto.request_dto import ChatRequest

class TestChatRequest:
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
    
    def test_empty_user_message_validation(self):
        """빈 사용자 메시지 검증 테스트"""
        with pytest.raises(ValidationError):
            ChatRequest(user_message="")
    
    def test_invalid_max_tokens_validation(self):
        """잘못된 max_tokens 검증 테스트"""
        with pytest.raises(ValidationError):
            ChatRequest(user_message="테스트", max_tokens=-1)
    
    def test_invalid_temperature_validation(self):
        """잘못된 temperature 검증 테스트"""
        with pytest.raises(ValidationError):
            ChatRequest(user_message="테스트", temperature=3.0)
    
    def test_conversation_history_validation(self):
        """대화 히스토리 형식 검증 테스트"""
        # 유효한 형식
        request = ChatRequest(
            user_message="테스트",
            conversation_history=["user:안녕하세요", "assistant:안녕하세요!"]
        )
        assert len(request.conversation_history) == 2
        
        # 잘못된 형식
        with pytest.raises(ValidationError):
            ChatRequest(
                user_message="테스트",
                conversation_history=["잘못된형식"]
            )
```

### 3. 설정 테스트

#### Config 클래스 테스트

```python
import pytest
import os
from src.config.config import Config
from src.exceptions.custom_exceptions import ConfigurationException

class TestConfig:
    def test_config_loading(self):
        """설정 로딩 테스트"""
        # Given
        os.environ["OPENAI_API_KEY"] = "test-key"
        os.environ["SERVER_PORT"] = "8080"
        
        # When
        config = Config()
        
        # Then
        assert config.openai_api_key == "test-key"
        assert config.server_port == 8080
    
    def test_config_defaults(self):
        """기본값 설정 테스트"""
        # Given
        if "OPENAI_API_KEY" in os.environ:
            del os.environ["OPENAI_API_KEY"]
        
        # When
        config = Config()
        
        # Then
        assert config.server_host == "0.0.0.0"
        assert config.server_port == 5601
    
    def test_config_validation_failure(self):
        """설정 검증 실패 테스트"""
        # Given
        if "OPENAI_API_KEY" in os.environ:
            del os.environ["OPENAI_API_KEY"]
        
        # When & Then
        with pytest.raises(ConfigurationException):
            config = Config()
            config.validate()
```

---

## 🌐 통합 테스트

### 1. API 엔드포인트 테스트

#### FastAPI 테스트 클라이언트 설정

```python
import pytest
from fastapi.testclient import TestClient
from app import app

@pytest.fixture
def client():
    """FastAPI 테스트 클라이언트"""
    return TestClient(app)

class TestChatAPI:
    def test_chat_endpoint_success(self, client):
        """채팅 엔드포인트 성공 테스트"""
        # Given
        payload = {
            "session_id": "test_session",
            "user_message": "안녕하세요",
            "max_tokens": 100,
            "temperature": 0.7
        }
        
        # When
        response = client.post("/api/v1/chat", json=payload)
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "response_text" in data
        assert data["session_id"] == "test_session"
    
    def test_chat_endpoint_validation_error(self, client):
        """채팅 엔드포인트 검증 오류 테스트"""
        # Given
        payload = {
            "user_message": "",  # 빈 메시지
            "max_tokens": -1     # 잘못된 토큰 수
        }
        
        # When
        response = client.post("/api/v1/chat", json=payload)
        
        # Then
        assert response.status_code == 422  # Validation Error
    
    def test_chat_endpoint_free_mode(self, client):
        """Free 모드 테스트"""
        # Given
        payload = {
            "session_id": "test_session",
            "user_message": "테스트 메시지",
            "openai_api_key": "sk-invalid-key",
            "free_mode": True
        }
        
        # When
        response = client.post("/api/v1/chat", json=payload)
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["api_key_source"] in ["user_provided", "default"]

class TestSystemAPI:
    def test_system_info_endpoint(self, client):
        """시스템 정보 엔드포인트 테스트"""
        # When
        response = client.get("/api/v1/system/info")
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert "system" in data
        assert "cpu" in data
        assert "memory" in data
        assert "disk" in data
    
    def test_system_status_endpoint(self, client):
        """시스템 상태 엔드포인트 테스트"""
        # When
        response = client.get("/api/v1/system/status")
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "cpu_usage" in data
        assert "memory_usage" in data
```

### 2. 비동기 API 테스트

```python
import pytest
import httpx
from httpx import AsyncClient

@pytest.mark.asyncio
class TestAsyncChatAPI:
    async def test_async_chat_endpoint(self):
        """비동기 채팅 엔드포인트 테스트"""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            # Given
            payload = {
                "session_id": "async_test",
                "user_message": "비동기 테스트",
                "max_tokens": 100
            }
            
            # When
            response = await ac.post("/api/v1/chat", json=payload)
            
            # Then
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
    
    async def test_concurrent_requests(self):
        """동시 요청 테스트"""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            # Given
            payloads = [
                {"user_message": f"테스트 {i}", "max_tokens": 50}
                for i in range(5)
            ]
            
            # When
            responses = await asyncio.gather(*[
                ac.post("/api/v1/chat", json=payload)
                for payload in payloads
            ])
            
            # Then
            for response in responses:
                assert response.status_code == 200
                data = response.json()
                assert data["success"] is True
```

---

## 📋 시나리오 테스트

### 1. 비즈니스 시나리오 테스트

```python
import pytest
from src.services.chat_service import ChatService
from src.dto.request_dto import ChatRequest

class TestChatScenarios:
    @pytest.fixture
    def chat_service(self, mock_openai_client):
        return ChatService(mock_openai_client)
    
    @pytest.mark.asyncio
    async def test_conversation_flow(self, chat_service, mock_openai_client):
        """대화 흐름 시나리오 테스트"""
        # Given - 첫 번째 메시지
        request1 = ChatRequest(
            session_id="conversation_test",
            user_message="안녕하세요",
            role="친근한 AI 어시스턴트"
        )
        
        # Mock 첫 번째 응답
        mock_response1 = Mock()
        mock_response1.choices = [Mock()]
        mock_response1.choices[0].message.content = "안녕하세요! 무엇을 도와드릴까요?"
        mock_response1.usage.total_tokens = 20
        
        mock_openai_client.chat_completion.return_value = mock_response1
        
        # When - 첫 번째 응답
        response1 = await chat_service.process_chat(request1)
        
        # Then
        assert response1.success is True
        assert "안녕하세요" in response1.response_text
        
        # Given - 두 번째 메시지 (대화 히스토리 포함)
        request2 = ChatRequest(
            session_id="conversation_test",
            user_message="파이썬에 대해 알려주세요",
            conversation_history=[
                "user:안녕하세요",
                "assistant:안녕하세요! 무엇을 도와드릴까요?"
            ]
        )
        
        # Mock 두 번째 응답
        mock_response2 = Mock()
        mock_response2.choices = [Mock()]
        mock_response2.choices[0].message.content = "파이썬은 프로그래밍 언어입니다..."
        mock_response2.usage.total_tokens = 50
        
        mock_openai_client.chat_completion.return_value = mock_response2
        
        # When - 두 번째 응답
        response2 = await chat_service.process_chat(request2)
        
        # Then
        assert response2.success is True
        assert "파이썬" in response2.response_text
        assert response2.total_tokens_used == 50
    
    @pytest.mark.asyncio
    async def test_api_key_fallback_scenario(self, chat_service, mock_openai_client):
        """API Key 폴백 시나리오 테스트"""
        # Given - 잘못된 API Key로 요청
        request = ChatRequest(
            session_id="fallback_test",
            user_message="테스트 메시지",
            openai_api_key="sk-invalid-key",
            free_mode=True
        )
        
        # Mock - 첫 번째 호출 실패, 두 번째 호출 성공
        mock_openai_client.chat_completion.side_effect = [
            Exception("Invalid API Key"),  # 첫 번째 호출 실패
            Mock(choices=[Mock()], usage=Mock(total_tokens=30))  # 두 번째 호출 성공
        ]
        
        # When
        response = await chat_service.process_chat(request)
        
        # Then
        assert response.success is True
        assert mock_openai_client.chat_completion.call_count == 2
    
    @pytest.mark.asyncio
    async def test_memory_context_scenario(self, chat_service, mock_openai_client):
        """메모리 컨텍스트 시나리오 테스트"""
        # Given
        request = ChatRequest(
            session_id="memory_test",
            user_message="내 관심사에 대해 말해봐",
            memory_context=[
                "사용자는 개발자입니다",
                "사용자는 AI에 관심이 있습니다",
                "사용자는 파이썬을 주로 사용합니다"
            ]
        )
        
        # Mock 응답
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "개발자이시군요! AI와 파이썬에 관심이 많으시네요."
        mock_response.usage.total_tokens = 40
        
        mock_openai_client.chat_completion.return_value = mock_response
        
        # When
        response = await chat_service.process_chat(request)
        
        # Then
        assert response.success is True
        assert "개발자" in response.response_text
```

### 2. 에러 시나리오 테스트

```python
class TestErrorScenarios:
    @pytest.mark.asyncio
    async def test_network_timeout_scenario(self, chat_service, mock_openai_client):
        """네트워크 타임아웃 시나리오 테스트"""
        # Given
        request = ChatRequest(user_message="테스트")
        mock_openai_client.chat_completion.side_effect = TimeoutError("Network timeout")
        
        # When & Then
        with pytest.raises(Exception):
            await chat_service.process_chat(request)
    
    @pytest.mark.asyncio
    async def test_rate_limit_scenario(self, chat_service, mock_openai_client):
        """Rate Limit 시나리오 테스트"""
        # Given
        request = ChatRequest(user_message="테스트")
        mock_openai_client.chat_completion.side_effect = Exception("Rate limit exceeded")
        
        # When & Then
        with pytest.raises(Exception):
            await chat_service.process_chat(request)
    
    @pytest.mark.asyncio
    async def test_invalid_response_scenario(self, chat_service, mock_openai_client):
        """잘못된 응답 시나리오 테스트"""
        # Given
        request = ChatRequest(user_message="테스트")
        mock_response = Mock()
        mock_response.choices = []  # 빈 응답
        mock_openai_client.chat_completion.return_value = mock_response
        
        # When & Then
        with pytest.raises(Exception):
            await chat_service.process_chat(request)
```

---

## ⚡ 성능 테스트

### 1. 부하 테스트

```python
import asyncio
import time
import pytest
from httpx import AsyncClient

class TestPerformance:
    @pytest.mark.asyncio
    async def test_concurrent_load(self):
        """동시 부하 테스트"""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            # Given
            num_requests = 10
            payload = {
                "user_message": "성능 테스트",
                "max_tokens": 50
            }
            
            # When
            start_time = time.time()
            responses = await asyncio.gather(*[
                ac.post("/api/v1/chat", json=payload)
                for _ in range(num_requests)
            ])
            end_time = time.time()
            
            # Then
            total_time = end_time - start_time
            avg_time = total_time / num_requests
            
            assert all(response.status_code == 200 for response in responses)
            assert avg_time < 5.0  # 평균 응답 시간 5초 이하
            print(f"평균 응답 시간: {avg_time:.2f}초")
    
    @pytest.mark.asyncio
    async def test_memory_usage(self, client):
        """메모리 사용량 테스트"""
        import psutil
        import os
        
        # Given
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # When
        for _ in range(100):
            response = client.post("/api/v1/chat", json={
                "user_message": "메모리 테스트",
                "max_tokens": 30
            })
            assert response.status_code == 200
        
        # Then
        final_memory = process.memory_info().rss
        memory_increase = (final_memory - initial_memory) / 1024 / 1024  # MB
        
        assert memory_increase < 100  # 메모리 증가량 100MB 이하
        print(f"메모리 증가량: {memory_increase:.2f}MB")
```

### 2. 응답 시간 테스트

```python
class TestResponseTime:
    def test_chat_response_time(self, client):
        """채팅 응답 시간 테스트"""
        import time
        
        # Given
        payload = {
            "user_message": "응답 시간 테스트",
            "max_tokens": 100
        }
        
        # When
        start_time = time.time()
        response = client.post("/api/v1/chat", json=payload)
        end_time = time.time()
        
        # Then
        response_time = end_time - start_time
        assert response.status_code == 200
        assert response_time < 10.0  # 응답 시간 10초 이하
        print(f"응답 시간: {response_time:.2f}초")
    
    def test_system_info_response_time(self, client):
        """시스템 정보 응답 시간 테스트"""
        import time
        
        # When
        start_time = time.time()
        response = client.get("/api/v1/system/info")
        end_time = time.time()
        
        # Then
        response_time = end_time - start_time
        assert response.status_code == 200
        assert response_time < 1.0  # 응답 시간 1초 이하
        print(f"시스템 정보 응답 시간: {response_time:.2f}초")
```

---

## 🛠️ 테스트 실행

### 1. 테스트 실행 명령어

```bash
# 모든 테스트 실행
pytest

# 특정 테스트 파일 실행
pytest tests/test_unit.py

# 특정 테스트 함수 실행
pytest tests/test_unit.py::TestChatService::test_process_chat_success

# 비동기 테스트만 실행
pytest -m asyncio

# 성능 테스트만 실행
pytest -m "performance"

# 커버리지와 함께 실행
pytest --cov=src --cov-report=html

# 상세 출력과 함께 실행
pytest -v

# 실패한 테스트만 재실행
pytest --lf
```

### 2. 테스트 설정

#### `pytest.ini` 설정
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --tb=short
    --strict-markers
    --disable-warnings
markers =
    unit: Unit tests
    integration: Integration tests
    scenario: Scenario tests
    performance: Performance tests
    asyncio: Async tests
```

#### `conftest.py` 설정
```python
import pytest
import asyncio
from unittest.mock import Mock
from src.services.chat_service import ChatService
from src.external.openai_client import OpenAIClient

@pytest.fixture(scope="session")
def event_loop():
    """비동기 테스트를 위한 이벤트 루프"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def mock_openai_client():
    """OpenAI 클라이언트 Mock"""
    mock_client = Mock(spec=OpenAIClient)
    mock_client.chat_completion = asyncio.coroutine(Mock())
    return mock_client

@pytest.fixture
def chat_service(mock_openai_client):
    """ChatService 인스턴스"""
    return ChatService(mock_openai_client)
```

### 3. 테스트 데이터 관리

#### `tests/fixtures/mock_data.py`
```python
"""테스트용 Mock 데이터"""

SAMPLE_CHAT_REQUEST = {
    "session_id": "test_session",
    "user_message": "안녕하세요",
    "role": "친근한 AI 어시스턴트",
    "max_tokens": 100,
    "temperature": 0.7
}

SAMPLE_CHAT_RESPONSE = {
    "session_id": "test_session",
    "response_text": "안녕하세요! 무엇을 도와드릴까요?",
    "model": "gpt-4o-mini",
    "input_tokens": 20,
    "output_tokens": 30,
    "total_tokens_used": 50,
    "response_time": 1.5,
    "success": True,
    "error_message": None,
    "api_key_source": "default"
}

SAMPLE_SYSTEM_INFO = {
    "timestamp": "2024-01-01T00:00:00",
    "system": {
        "platform": "Windows",
        "platform_version": "10.0.26100",
        "architecture": "AMD64",
        "hostname": "test-host",
        "python_version": "3.11.0"
    },
    "cpu": {
        "usage_percent": 15.2,
        "count": 8,
        "frequency_mhz": 2400.0
    },
    "memory": {
        "total_gb": 16.0,
        "available_gb": 8.0,
        "usage_percent": 50.0
    }
}
```

---

## 📊 품질 관리

### 1. 코드 커버리지

#### 커버리지 설정
```bash
# 커버리지 설치
pip install pytest-cov

# 커버리지 실행
pytest --cov=src --cov-report=html --cov-report=term-missing

# 커버리지 임계값 설정
pytest --cov=src --cov-fail-under=80
```

#### `.coveragerc` 설정
```ini
[run]
source = src
omit = 
    */tests/*
    */__pycache__/*
    */venv/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if 0:
    if __name__ == .__main__.:
    class .*\bProtocol\):
    @(abc\.)?abstractmethod
```

### 2. 코드 품질 검사

#### flake8 설정
```bash
# flake8 설치
pip install flake8

# 코드 검사
flake8 src/ tests/

# 설정 파일 (.flake8)
[flake8]
max-line-length = 100
exclude = .git,__pycache__,build,dist,*.egg-info
ignore = E203, W503
```

#### black 설정
```bash
# black 설치
pip install black

# 코드 포맷팅
black src/ tests/

# 설정 파일 (pyproject.toml)
[tool.black]
line-length = 100
target-version = ['py38']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | build
  | dist
)/
'''
```

### 3. 타입 검사

#### mypy 설정
```bash
# mypy 설치
pip install mypy

# 타입 검사
mypy src/

# 설정 파일 (mypy.ini)
[mypy]
python_version = 3.8
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
disallow_incomplete_defs = True
check_untyped_defs = True
disallow_untyped_decorators = True
no_implicit_optional = True
warn_redundant_casts = True
warn_unused_ignores = True
warn_no_return = True
warn_unreachable = True
strict_equality = True

[mypy-pydantic.*]
ignore_missing_imports = True
```

### 4. 보안 검사

#### bandit 설정
```bash
# bandit 설치
pip install bandit

# 보안 검사
bandit -r src/

# 설정 파일 (.bandit)
exclude_dirs = ['tests']
skips = ['B101']
```

---

## 🔄 CI/CD 통합

### 1. GitHub Actions 설정

#### `.github/workflows/test.yml`
```yaml
name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirement.txt
        pip install pytest pytest-cov flake8 black mypy bandit
    
    - name: Run tests
      run: |
        pytest --cov=src --cov-report=xml
    
    - name: Run linting
      run: |
        flake8 src/ tests/
        black --check src/ tests/
    
    - name: Run type checking
      run: |
        mypy src/
    
    - name: Run security checks
      run: |
        bandit -r src/
    
    - name: Upload coverage
      uses: codecov/codecov-action@v1
      with:
        file: ./coverage.xml
```

### 2. 테스트 자동화

#### `run_tests.py` 스크립트
```python
#!/usr/bin/env python3
"""테스트 실행 스크립트"""

import subprocess
import sys
import os

def run_command(command, description):
    """명령어 실행"""
    print(f"\n🔄 {description}...")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ {description} 완료")
        if result.stdout:
            print(result.stdout)
    else:
        print(f"❌ {description} 실패")
        print(result.stderr)
        return False
    
    return True

def main():
    """메인 테스트 실행"""
    print("🧪 LLM Server 테스트 실행")
    
    # 테스트 순서
    tests = [
        ("pytest --cov=src --cov-report=term-missing", "단위/통합 테스트"),
        ("flake8 src/ tests/", "코드 스타일 검사"),
        ("black --check src/ tests/", "코드 포맷팅 검사"),
        ("mypy src/", "타입 검사"),
        ("bandit -r src/", "보안 검사")
    ]
    
    all_passed = True
    
    for command, description in tests:
        if not run_command(command, description):
            all_passed = False
    
    if all_passed:
        print("\n🎉 모든 테스트 통과!")
        sys.exit(0)
    else:
        print("\n💥 일부 테스트 실패")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

---

## 📈 테스트 메트릭

### 1. 테스트 지표

- **커버리지**: 80% 이상 목표
- **응답 시간**: 평균 5초 이하
- **동시 요청**: 10개 이상 처리 가능
- **메모리 사용량**: 100MB 이하 증가

### 2. 테스트 리포트

```bash
# HTML 리포트 생성
pytest --cov=src --cov-report=html

# XML 리포트 생성 (CI/CD용)
pytest --cov=src --cov-report=xml

# 터미널 리포트
pytest --cov=src --cov-report=term-missing
```

---

## 🔗 관련 문서

- **[개요 및 시작 가이드](./../overview/README.md)**: 프로젝트 소개 및 기본 사용법
- **[API 문서](./../api/README.md)**: API 명세 및 사용법
- **[아키텍처 가이드](./../architecture/README.md)**: 프로젝트 구조 및 개발 가이드
- **[배포 가이드](./../deployment/README.md)**: 운영 환경 배포 방법

---

**문서 버전**: 1.0  
**최종 업데이트**: 2024년 12월  
**작성자**: LLM Server 개발팀 
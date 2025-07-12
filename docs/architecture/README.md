# LLM Server 아키텍처 및 개발 가이드

이 문서는 LLM Server의 아키텍처 설계, 개발 가이드라인, 그리고 핵심 컴포넌트에 대한 상세한 설명을 제공합니다.

## 🏗️ 아키텍처 개요

### 전체 구조

```
LLM Server
├── 🌐 API Layer (FastAPI)
│   ├── routes.py          # 채팅 API 라우터
│   ├── system_routes.py   # 시스템 모니터링 API
│   └── exception_handlers.py # 전역 예외 처리
├── 🏢 Service Layer
│   └── services/
│       └── chat_service.py # 채팅 비즈니스 로직
├── 🔗 External Layer
│   └── external/
│       └── openai_client.py # OpenAI API 연동
├── 📦 DTO Layer
│   └── dto/
│       ├── request_dto.py  # 요청 데이터 모델
│       └── response_dto.py # 응답 데이터 모델
├── ⚙️ Config Layer
│   └── config/
│       └── config.py       # 환경 설정 관리
├── 🛠️ Utils Layer
│   └── utils/
│       ├── logger.py       # 로깅 유틸리티
│       └── system_info.py  # 시스템 정보 수집
└── ⚠️ Exception Layer
    └── exceptions/
        └── custom_exceptions.py # 커스텀 예외 클래스
```

### 아키텍처 원칙

1. **계층 분리 (Layered Architecture)**
   - API Layer: HTTP 요청/응답 처리
   - Service Layer: 비즈니스 로직
   - External Layer: 외부 API 연동
   - DTO Layer: 데이터 전송 객체

2. **관심사 분리 (Separation of Concerns)**
   - 각 모듈은 단일 책임을 가짐
   - 의존성 최소화
   - 테스트 용이성 확보

3. **의존성 주입 (Dependency Injection)**
   - 느슨한 결합 (Loose Coupling)
   - 테스트 가능한 구조
   - 확장성 향상

---

## 📁 프로젝트 구조 상세

### 1. API Layer (`src/api/`)

#### `routes.py`
```python
# 채팅 API 엔드포인트 정의
@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # 요청 검증 및 서비스 호출
    return await chat_service.process_chat(request)
```

#### `system_routes.py`
```python
# 시스템 모니터링 API 엔드포인트
@router.get("/info")
async def get_system_info():
    # 시스템 정보 수집 및 반환
    return system_info_collector.get_full_info()
```

#### `exception_handlers.py`
```python
# 전역 예외 처리기
@app.exception_handler(ValidationException)
async def validation_exception_handler(request, exc):
    # 검증 오류 응답 생성
    return create_error_response(exc)
```

### 2. Service Layer (`src/services/`)

#### `chat_service.py`
```python
class ChatService:
    def __init__(self, openai_client: OpenAIClient):
        self.openai_client = openai_client
    
    async def process_chat(self, request: ChatRequest) -> ChatResponse:
        # 1. 요청 검증
        self._validate_request(request)
        
        # 2. 컨텍스트 구성
        context = self._build_context(request)
        
        # 3. OpenAI API 호출
        response = await self.openai_client.chat_completion(context)
        
        # 4. 응답 생성
        return self._create_response(response, request)
```

### 3. External Layer (`src/external/`)

#### `openai_client.py`
```python
class OpenAIClient:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
    
    async def chat_completion(self, context: ChatContext) -> OpenAIResponse:
        # OpenAI API 호출 로직
        response = await self.client.chat.completions.create(
            model=context.model,
            messages=context.messages,
            max_tokens=context.max_tokens,
            temperature=context.temperature
        )
        return response
```

### 4. DTO Layer (`src/dto/`)

#### `request_dto.py`
```python
class ChatRequest(BaseModel):
    session_id: str = ""
    user_message: str
    role: str = ""
    max_tokens: int = 1000
    temperature: float = 0.7
    # ... 기타 필드들
    
    @validator('user_message')
    def validate_user_message(cls, v):
        if not v.strip():
            raise ValueError("사용자 메시지는 비어있을 수 없습니다")
        return v
```

#### `response_dto.py`
```python
class ChatResponse(BaseModel):
    session_id: str
    response_text: str
    total_tokens_used: int
    response_time: float
    success: bool
    error_message: Optional[str] = None
    # ... 기타 필드들
```

### 5. Config Layer (`src/config/`)

#### `config.py`
```python
class Config:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.server_host = os.getenv("SERVER_HOST", "0.0.0.0")
        self.server_port = int(os.getenv("SERVER_PORT", "5601"))
        # ... 기타 설정들
    
    def validate(self):
        if not self.openai_api_key:
            raise ConfigurationException("OpenAI API Key가 설정되지 않았습니다")
```

---

## 🔧 핵심 컴포넌트 분석

### 1. 채팅 서비스 (ChatService)

#### 책임
- 채팅 요청 처리
- 컨텍스트 구성
- OpenAI API 호출
- 응답 생성

#### 주요 메서드
```python
class ChatService:
    async def process_chat(self, request: ChatRequest) -> ChatResponse:
        """채팅 요청을 처리하고 응답을 생성합니다."""
        
    def _build_context(self, request: ChatRequest) -> ChatContext:
        """요청을 기반으로 OpenAI API 호출 컨텍스트를 구성합니다."""
        
    def _create_response(self, openai_response: OpenAIResponse, 
                        request: ChatRequest) -> ChatResponse:
        """OpenAI 응답을 ChatResponse로 변환합니다."""
```

#### 컨텍스트 구성 로직
```python
def _build_context(self, request: ChatRequest) -> ChatContext:
    messages = []
    
    # 1. 시스템 메시지 추가
    if request.role:
        messages.append({"role": "system", "content": request.role})
    
    # 2. 메모리 컨텍스트 추가
    if request.memory_context:
        memory_text = "\n".join(request.memory_context)
        messages.append({"role": "system", "content": f"기억: {memory_text}"})
    
    # 3. 대화 히스토리 추가
    for history in request.conversation_history:
        role, content = history.split(":", 1)
        messages.append({"role": role, "content": content})
    
    # 4. 사용자 메시지 추가
    messages.append({"role": "user", "content": request.user_message})
    
    return ChatContext(
        messages=messages,
        model=request.model,
        max_tokens=request.max_tokens,
        temperature=request.temperature
    )
```

### 2. OpenAI 클라이언트 (OpenAIClient)

#### 책임
- OpenAI API 연동
- API Key 관리
- 응답 처리

#### 주요 메서드
```python
class OpenAIClient:
    async def chat_completion(self, context: ChatContext) -> OpenAIResponse:
        """OpenAI Chat Completion API를 호출합니다."""
        
    def _select_api_key(self, user_key: str = None, free_mode: bool = False) -> str:
        """사용할 API Key를 선택합니다."""
        
    def _validate_api_key(self, api_key: str) -> bool:
        """API Key의 유효성을 검증합니다."""
```

#### API Key 선택 로직
```python
def _select_api_key(self, user_key: str = None, free_mode: bool = False) -> str:
    # 1. 사용자 Key가 제공된 경우
    if user_key:
        if free_mode:
            # Free 모드: 유효성 검증 후 사용, 실패 시 기본 Key
            if self._validate_api_key(user_key):
                return user_key, "user_provided"
            else:
                return self.default_key, "default"
        else:
            # 일반 모드: 사용자 Key만 사용
            return user_key, "user_provided"
    
    # 2. 기본 Key 사용
    return self.default_key, "default"
```

### 3. 설정 관리 (Config)

#### 책임
- 환경 변수 관리
- 기본값 설정
- 설정 검증

#### 주요 기능
```python
class Config:
    def __init__(self):
        # 환경 변수에서 설정 로드
        self._load_from_env()
        
        # 기본값 설정
        self._set_defaults()
        
        # 설정 검증
        self.validate()
    
    def _load_from_env(self):
        """환경 변수에서 설정을 로드합니다."""
        
    def _set_defaults(self):
        """기본값을 설정합니다."""
        
    def validate(self):
        """설정의 유효성을 검증합니다."""
```

---

## 🛠️ 개발 가이드라인

### 1. 코드 스타일

#### Python 코딩 컨벤션
```python
# 파일명: snake_case
# 클래스명: PascalCase
# 함수/변수명: snake_case
# 상수: UPPER_SNAKE_CASE

class ChatService:
    def __init__(self, openai_client: OpenAIClient):
        self.openai_client = openai_client
        self.logger = logging.getLogger(__name__)
    
    async def process_chat(self, request: ChatRequest) -> ChatResponse:
        """채팅 요청을 처리합니다."""
        try:
            # 비즈니스 로직
            return await self._handle_chat_request(request)
        except Exception as e:
            self.logger.error(f"채팅 처리 중 오류 발생: {e}")
            raise
```

#### 주석 작성 가이드
```python
def _build_context(self, request: ChatRequest) -> ChatContext:
    """
    요청을 기반으로 OpenAI API 호출 컨텍스트를 구성합니다.
    
    Args:
        request (ChatRequest): 채팅 요청 객체
        
    Returns:
        ChatContext: OpenAI API 호출에 필요한 컨텍스트
        
    Raises:
        ValidationException: 요청 데이터가 유효하지 않은 경우
    """
```

### 2. 예외 처리

#### 커스텀 예외 정의
```python
class ValidationException(Exception):
    """요청 데이터 검증 실패 시 발생하는 예외"""
    pass

class ConfigurationException(Exception):
    """설정 오류 시 발생하는 예외"""
    pass

class ChatServiceException(Exception):
    """채팅 서비스 처리 중 오류 시 발생하는 예외"""
    pass

class OpenAIClientException(Exception):
    """OpenAI API 호출 중 오류 시 발생하는 예외"""
    pass
```

#### 예외 처리 패턴
```python
async def process_chat(self, request: ChatRequest) -> ChatResponse:
    try:
        # 1. 요청 검증
        self._validate_request(request)
        
        # 2. 비즈니스 로직 실행
        result = await self._execute_chat_logic(request)
        
        return result
        
    except ValidationException as e:
        # 검증 오류 처리
        self.logger.warning(f"요청 검증 실패: {e}")
        raise
        
    except OpenAIClientException as e:
        # OpenAI API 오류 처리
        self.logger.error(f"OpenAI API 오류: {e}")
        raise ChatServiceException(f"AI 서비스 연결 오류: {e}")
        
    except Exception as e:
        # 예상치 못한 오류 처리
        self.logger.error(f"예상치 못한 오류: {e}")
        raise ChatServiceException(f"서비스 처리 중 오류: {e}")
```

### 3. 로깅

#### 로깅 설정
```python
import logging

# 로거 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

#### 로깅 패턴
```python
class ChatService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    async def process_chat(self, request: ChatRequest) -> ChatResponse:
        self.logger.info(f"채팅 요청 시작: session_id={request.session_id}")
        
        try:
            result = await self._process_request(request)
            self.logger.info(f"채팅 요청 완료: session_id={request.session_id}, "
                           f"tokens={result.total_tokens_used}")
            return result
            
        except Exception as e:
            self.logger.error(f"채팅 요청 실패: session_id={request.session_id}, "
                            f"error={str(e)}")
            raise
```

### 4. 테스트 작성

#### 단위 테스트 패턴
```python
import pytest
from unittest.mock import Mock, AsyncMock

class TestChatService:
    @pytest.fixture
    def mock_openai_client(self):
        return Mock(spec=OpenAIClient)
    
    @pytest.fixture
    def chat_service(self, mock_openai_client):
        return ChatService(mock_openai_client)
    
    async def test_process_chat_success(self, chat_service, mock_openai_client):
        # Given
        request = ChatRequest(user_message="테스트 메시지")
        expected_response = ChatResponse(...)
        mock_openai_client.chat_completion.return_value = expected_response
        
        # When
        result = await chat_service.process_chat(request)
        
        # Then
        assert result.success is True
        assert result.response_text == expected_response.content
        mock_openai_client.chat_completion.assert_called_once()
```

#### 통합 테스트 패턴
```python
class TestChatAPI:
    async def test_chat_endpoint_success(self, client):
        # Given
        payload = {
            "user_message": "테스트 메시지",
            "session_id": "test_session"
        }
        
        # When
        response = await client.post("/api/v1/chat", json=payload)
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "response_text" in data
```

---

## 🔄 개발 워크플로우

### 1. 기능 개발 프로세스

1. **요구사항 분석**
   - 기능 명세 작성
   - API 설계
   - 데이터 모델 정의

2. **코드 구현**
   - DTO 클래스 작성
   - 서비스 로직 구현
   - API 엔드포인트 추가

3. **테스트 작성**
   - 단위 테스트
   - 통합 테스트
   - API 테스트

4. **문서 업데이트**
   - API 문서 업데이트
   - README 업데이트
   - 코드 주석 추가

### 2. 코드 리뷰 체크리스트

- [ ] 코드 스타일 준수
- [ ] 예외 처리 적절성
- [ ] 로깅 추가
- [ ] 테스트 코드 작성
- [ ] 문서 업데이트
- [ ] 보안 고려사항

### 3. 배포 프로세스

1. **개발 환경 테스트**
   ```bash
   python run_tests.py
   ```

2. **로컬 서버 테스트**
   ```bash
   python app.py
   ```

3. **Docker 빌드 테스트**
   ```bash
   docker-compose up --build
   ```

4. **프로덕션 배포**
   ```bash
   # 환경 변수 설정
   export OPENAI_API_KEY="your-api-key"
   
   # Docker 배포
   docker-compose -f docker-compose.prod.yml up -d
   ```

---

## 🔗 관련 문서

- **[개요 및 시작 가이드](./../overview/README.md)**: 프로젝트 소개 및 기본 사용법
- **[API 문서](./../api/README.md)**: API 명세 및 사용법
- **[배포 가이드](./../deployment/README.md)**: 운영 환경 배포 방법
- **[테스트 가이드](./../testing/README.md)**: 테스트 코드 작성 및 실행

---

**문서 버전**: 1.0  
**최종 업데이트**: 2024년 12월  
**작성자**: LLM Server 개발팀 
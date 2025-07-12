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
        └── chat_exceptions.py # 커스텀 예외 클래스
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
async def chat_with_ai(request: ChatRequest):
    # 요청 검증 및 서비스 호출
    return chat_service.process_chat_request(request)
```

#### `system_routes.py`
```python
# 시스템 모니터링 API 엔드포인트
@router.get("/info")
async def get_system_info():
    # 시스템 정보 수집 및 반환
    return SystemInfoCollector.get_system_info()
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
    def __init__(self):
        self.openai_client = OpenAIClient()
    
    def process_chat_request(self, request: ChatRequest) -> ChatResponse:
        # 1. 요청 검증
        self._validate_request(request)
        
        # 2. 메시지 구성
        system_message = self._create_system_message(request)
        conversation_history = self._format_conversation_history(request.conversation_history or [])
        user_message = self._create_user_message(request.user_message)
        
        # 3. OpenAI API 호출
        openai_response, response_time, api_key_source = self.openai_client.generate_response(
            messages=[system_message] + conversation_history + [user_message],
            api_key=request.openai_api_key,
            free_mode=request.free_mode,
            model=request.model,
            instructions=request.instructions,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        
        # 4. 응답 생성
        return ChatResponse.from_openai_response(
            openai_response=openai_response,
            session_id=request.session_id,
            response_time=response_time,
            api_key_source=api_key_source
        )
```

### 3. External Layer (`src/external/`)

#### `openai_client.py`
```python
class OpenAIClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or self._load_api_key()
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None
    
    def generate_response(
        self,
        messages: list[dict],
        api_key: str = None,
        free_mode: bool = False,
        model: str = DEFAULT_MODEL,
        instructions: str = "",
        max_tokens: int = DEFAULT_MAX_TOKENS,
        temperature: float = DEFAULT_TEMPERATURE
    ) -> tuple[Response, float, str]:
        # API Key 선택 및 검증
        selected_api_key, api_key_source = self._select_api_key(api_key, free_mode)
        
        # OpenAI API 호출
        client = OpenAI(api_key=selected_api_key)
        response = client.responses.create(
            model=model,
            input=messages,
            instructions=instructions,
            temperature=temperature,
            max_output_tokens=max_tokens
        )
        
        return response, response_time, api_key_source
```

### 4. DTO Layer (`src/dto/`)

#### `request_dto.py`
```python
class ChatRequest(BaseModel):
    session_id: Optional[str] = ""
    system_message: Optional[str] = ""
    user_message: Optional[str] = ""
    role: Optional[str] = ""
    instructions: Optional[str] = ""
    conversation_history: Optional[List[str]] = []
    memory_context: Optional[List[str]] = []
    max_tokens: Optional[int] = 1000
    temperature: Optional[float] = 0.7
    model: Optional[str] = "gpt-4o-mini"
    openai_api_key: Optional[str] = ""
    free_mode: Optional[bool] = False
    
    def get_system_message(self) -> str:
        """시스템 메시지를 조합하여 반환"""
        system_prompt = f"""
{self.system_message}

{self._format_role()}

{self._format_memory()}

{self._format_instructions()}
        """
        return system_prompt.strip()
```

#### `response_dto.py`
```python
@dataclass
class ChatResponse:
    session_id: str
    response_text: str
    model: str
    input_tokens: int
    output_tokens: int
    total_tokens_used: int
    output_format: str
    created_at: datetime
    temperature: Optional[float] = None
    instructions: Optional[str] = None
    response_time: Optional[float] = None
    success: bool = True
    error_message: Optional[str] = None
    api_key_source: Optional[str] = None
    
    @classmethod
    def from_openai_response(cls, openai_response, session_id: str = "", response_time: float = None, api_key_source: str = None):
        """OpenAI Response에서 ChatResponse 생성"""
        return cls(
            session_id=session_id,
            response_text=openai_response.output_text,
            model=openai_response.model,
            input_tokens=openai_response.usage.input_tokens,
            output_tokens=openai_response.usage.output_tokens,
            total_tokens_used=openai_response.usage.total_tokens,
            output_format=openai_response.text.format.type,
            created_at=datetime.fromtimestamp(openai_response.created_at),
            temperature=openai_response.temperature,
            response_time=response_time,
            success=True,
            api_key_source=api_key_source
        )
```

### 5. Config Layer (`src/config/`)

#### `config.py`
```python
class Config:
    """설정 관리 클래스"""
    
    SERVER_PORT = "5601"
    OPENAI_API_KEY = ""
    LOG_LEVEL = "INFO"
    LOG_FILE = "logs/app.log"
    DEFAULT_MODEL = "gpt-4o-mini"
    DEFAULT_TEMPERATURE = "0.7"
    DEFAULT_MAX_TOKENS = "1000"
    DEFAULT_SYSTEM_MESSAGE = "당신은 도움이 되는 AI 어시스턴트입니다."
    
    def __init__(self):
        self._load_env_file()
        self._load_from_env()
    
    def get(self, key: str, default: Optional[str] = None) -> str:
        """설정 값에서 값을 가져옴"""
        return getattr(self, key, default)
    
    def get_int(self, key: str, default: int = 0) -> int:
        """설정 값에서 정수 값을 가져옴"""
        value = self.get(key)
        try:
            return int(value) if value else default
        except (ValueError, TypeError):
            return default
```

---

## 🔧 핵심 컴포넌트 분석

### 1. 채팅 서비스 (ChatService)

#### 책임
- 채팅 요청 처리
- 메시지 구성
- OpenAI API 호출
- 응답 생성

#### 주요 메서드
```python
class ChatService:
    def process_chat_request(self, request: ChatRequest) -> ChatResponse:
        """채팅 요청을 처리하고 응답을 생성합니다."""
        
    def _validate_request(self, request: ChatRequest) -> None:
        """요청 데이터 검증"""
        
    def _create_system_message(self, request: ChatRequest) -> dict:
        """시스템 메시지 생성"""
        
    def _format_conversation_history(self, history: list[str]) -> list[dict]:
        """대화 히스토리 포맷팅"""
```

### 2. OpenAI 클라이언트 (OpenAIClient)

#### 책임
- OpenAI API 통신
- API Key 관리
- 응답 처리

#### 주요 메서드
```python
class OpenAIClient:
    def generate_response(
        self,
        messages: list[dict],
        api_key: str = None,
        free_mode: bool = False,
        model: str = DEFAULT_MODEL,
        instructions: str = "",
        max_tokens: int = DEFAULT_MAX_TOKENS,
        temperature: float = DEFAULT_TEMPERATURE
    ) -> tuple[Response, float, str]:
        """OpenAI API에 메시지 전송하여 응답 생성"""
        
    def _select_api_key(self, api_key: str = None, free_mode: bool = False) -> tuple[str, str]:
        """API Key 선택 및 검증"""
        
    def _validate_api_key(self, api_key: str) -> bool:
        """API Key 유효성 검증"""
```

### 3. 예외 처리 시스템

#### 커스텀 예외 클래스
```python
class ValidationException(Exception):
    """요청 데이터 검증 실패 시 발생하는 예외"""
    
class ConfigurationException(Exception):
    """설정 오류 시 발생하는 예외"""
    
class ChatServiceException(Exception):
    """채팅 서비스 처리 중 오류 시 발생하는 예외"""
    
class OpenAIClientException(Exception):
    """OpenAI API 호출 중 오류 시 발생하는 예외"""
```

#### 전역 예외 처리기
```python
@app.exception_handler(ValidationException)
async def validation_exception_handler(request, exc):
    """검증 예외 처리"""
    
@app.exception_handler(OpenAIClientException)
async def openai_client_exception_handler(request, exc):
    """OpenAI 클라이언트 예외 처리"""
    
@app.exception_handler(ChatServiceException)
async def chat_service_exception_handler(request, exc):
    """채팅 서비스 예외 처리"""
```

---

## 🔄 데이터 플로우

### 1. 채팅 요청 처리 플로우

```
1. HTTP 요청 수신 (POST /api/v1/chat)
   ↓
2. ChatRequest DTO 생성 및 검증
   ↓
3. ChatService.process_chat_request() 호출
   ↓
4. 요청 데이터 검증 (_validate_request)
   ↓
5. 메시지 구성 (_create_system_message, _format_conversation_history)
   ↓
6. OpenAI API 호출 (OpenAIClient.generate_response)
   ↓
7. 응답 생성 (ChatResponse.from_openai_response)
   ↓
8. HTTP 응답 반환
```

### 2. API Key 처리 플로우

```
1. 요청에서 API Key 확인
   ↓
2. Free 모드 여부 확인
   ↓
3. API Key 선택 (_select_api_key)
   ├─ Free 모드: 사용자 Key → 기본 Key
   └─ 일반 모드: 사용자 Key만 허용
   ↓
4. API Key 유효성 검증 (_validate_api_key)
   ↓
5. OpenAI API 호출
   ↓
6. API Key 소스 정보 응답에 포함
```

---

## 🛠️ 개발 가이드라인

### 1. 코드 스타일

#### Python 코딩 컨벤션
- **PEP 8** 준수
- **Type Hints** 사용
- **Docstring** 작성
- **명확한 변수명** 사용

#### 예시
```python
def process_chat_request(self, request: ChatRequest) -> ChatResponse:
    """
    채팅 요청을 처리하여 응답을 반환
    
    Args:
        request: 채팅 요청 데이터
        
    Returns:
        ChatResponse: 채팅 응답 데이터
        
    Raises:
        ChatServiceException: 채팅 서비스 처리 중 오류 발생 시
        ValidationException: 요청 데이터 검증 실패 시
    """
```

### 2. 에러 처리

#### 예외 처리 원칙
1. **구체적인 예외 사용**
2. **적절한 로깅**
3. **사용자 친화적 메시지**
4. **디버깅 정보 포함**

#### 예시
```python
try:
    response = await self.openai_client.generate_response(messages)
except OpenAIClientException as e:
    logger.error(f"OpenAI API 호출 실패: {e}")
    raise ChatServiceException(f"AI 서비스 연결 오류: {e.message}")
except Exception as e:
    logger.error(f"예상치 못한 오류: {e}")
    raise ChatServiceException(f"서비스 처리 중 오류: {str(e)}")
```

### 3. 로깅

#### 로깅 레벨
- **DEBUG**: 상세한 디버깅 정보
- **INFO**: 일반적인 정보
- **WARNING**: 경고 메시지
- **ERROR**: 오류 메시지
- **CRITICAL**: 심각한 오류

#### 예시
```python
logger.info(f"채팅 요청 처리 시작: {request.user_message[:50]}...")
logger.debug(f"OpenAI API 요청 시작 (model: {model}, temperature: {temperature})")
logger.error(f"OpenAI API 호출 중 오류 발생: {str(e)}")
```

### 4. 테스트

#### 테스트 구조
```
tests/
├── test_unit.py          # 단위 테스트
├── test_scenarios.py     # 시나리오 테스트
└── test_input.py         # 입력 검증 테스트
```

#### 테스트 예시
```python
def test_chat_service_process_chat_request():
    """채팅 서비스 요청 처리 테스트"""
    service = ChatService()
    request = ChatRequest(
        user_message="테스트 메시지",
        session_id="test_session"
    )
    
    response = service.process_chat_request(request)
    
    assert response.success is True
    assert response.response_text is not None
    assert response.session_id == "test_session"
```

---

## 📈 성능 최적화

### 1. 메모리 관리

#### 가비지 컬렉션
```python
import gc

# 주기적 가비지 컬렉션
gc.collect()

# 메모리 사용량 모니터링
import psutil
process = psutil.Process()
memory_usage = process.memory_info().rss / 1024 / 1024
logger.info(f"메모리 사용량: {memory_usage:.2f} MB")
```

### 2. 비동기 처리

#### 동시 요청 제한
```python
import asyncio

# 세마포어를 사용한 동시 요청 제한
semaphore = asyncio.Semaphore(10)

async def process_request(request):
    async with semaphore:
        return await chat_service.process_chat_request(request)
```

### 3. 캐싱

#### 응답 캐싱
```python
import functools
import time

@functools.lru_cache(maxsize=1000)
def cache_response(key: str, ttl: int = 300):
    """응답 캐싱"""
    # 캐시 로직 구현
    pass
```

---

## 🔗 관련 문서

- **[개요 및 시작 가이드](./../overview/README.md)**: 프로젝트 소개 및 기본 사용법
- **[API 문서](./../api/README.md)**: API 명세 및 사용법
- **[배포 가이드](./../deployment/README.md)**: 배포 및 운영 가이드
- **[테스트 가이드](./../testing/README.md)**: 테스트 및 품질 관리

---

**문서 버전**: 1.0  
**최종 업데이트**: 2024년 12월  
**작성자**: LLM Server 개발팀 
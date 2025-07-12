# 아키텍처 및 개발 가이드

## 개요

LLM Server는 FastAPI 기반의 모듈화된 아키텍처를 채택하여 확장성과 유지보수성을 고려한 설계를 제공합니다. 이 문서는 프로젝트의 구조, 컴포넌트 간의 관계, 그리고 개발 가이드라인을 설명합니다.

## 프로젝트 구조

```
LLM Server/
├── app.py                 # FastAPI 애플리케이션 진입점
├── docker-compose.yml     # Docker Compose 설정
├── Dockerfile            # Docker 이미지 빌드 설정
├── env.example           # 환경 변수 예시
├── requirement.txt       # Python 의존성
├── run_tests.py         # 테스트 실행 스크립트
├── src/                 # 소스 코드
│   ├── api/            # API 라우터
│   │   ├── routes.py   # 채팅 API 엔드포인트
│   │   └── system_routes.py # 시스템 모니터링 API
│   ├── config/         # 설정 관리
│   │   └── config.py   # 환경 변수 및 설정
│   ├── dto/            # 데이터 전송 객체
│   │   ├── request_dto.py  # 요청 DTO
│   │   └── response_dto.py # 응답 DTO
│   ├── external/       # 외부 서비스 연동
│   │   └── openai_client.py # OpenAI API 클라이언트
│   ├── services/       # 비즈니스 로직
│   │   └── chat_service.py  # 채팅 서비스
│   ├── utils/          # 유틸리티
│   │   ├── logger.py   # 로깅 설정
│   │   └── system_info.py # 시스템 정보 수집
│   └── exceptions/     # 커스텀 예외
│       └── chat_exceptions.py # 채팅 관련 예외
├── tests/              # 테스트 코드
│   ├── test_unit.py    # 단위 테스트
│   ├── test_scenarios.py # 시나리오 테스트
│   └── test_input.py   # 테스트 입력 데이터
└── docs/               # 문서
    ├── overview/       # 개요 및 시작 가이드
    ├── api/           # API 문서
    ├── architecture/  # 아키텍처 가이드
    ├── deployment/    # 배포 가이드
    └── testing/       # 테스트 가이드
```

## 핵심 컴포넌트

### 1. API Layer (`src/api/`)

FastAPI 라우터를 통해 HTTP 요청을 처리합니다.

#### 주요 파일:
- `routes.py`: 채팅 API 엔드포인트 (`/api/v1/chat`)
- `system_routes.py`: 시스템 모니터링 API

#### 특징:
- RESTful API 설계
- 자동 문서 생성 (Swagger/OpenAPI)
- 요청/응답 검증 (Pydantic)
- 글로벌 예외 처리

### 2. DTO Layer (`src/dto/`)

데이터 전송 객체를 정의하여 API 계층과 비즈니스 로직 계층 간의 데이터 교환을 담당합니다.

#### ChatRequest (요청 DTO)
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
    use_user_api_key: Optional[bool] = False
```

#### ChatResponse (응답 DTO)
```python
class ChatResponse(BaseModel):
    success: bool
    response_text: Optional[str] = None
    session_id: Optional[str] = None
    response_time: float = 0.0
    api_key_source: Optional[str] = None
    model_used: Optional[str] = None
    tokens_used: Optional[dict] = None
    error: Optional[dict] = None
```

### 3. Service Layer (`src/services/`)

비즈니스 로직을 처리하는 핵심 계층입니다.

#### ChatService
```python
class ChatService:
    def __init__(self):
        self.openai_client = OpenAIClient()
    
    def process_chat_request(self, request: ChatRequest) -> ChatResponse:
        # 1. 요청 데이터 검증
        # 2. 메시지 구성
        # 3. OpenAI API 호출
        # 4. 응답 생성 및 반환
```

#### 주요 기능:
- 요청 데이터 검증
- 시스템 메시지 생성
- 대화 히스토리 처리
- OpenAI API 호출
- 응답 데이터 변환

### 4. External Layer (`src/external/`)

외부 서비스와의 연동을 담당합니다.

#### OpenAIClient
```python
class OpenAIClient:
    def generate_response(
        self,
        messages: list[dict],
        api_key: str = None,
        use_user_api_key: bool = False,
        model: str = DEFAULT_MODEL,
        instructions: str = "",
        max_tokens: int = DEFAULT_MAX_TOKENS,
        temperature: float = DEFAULT_TEMPERATURE
    ) -> tuple[Response, float, str]:
```

#### API Key 관리:
- **기본 모드** (`use_user_api_key: false`): 서버 관리 API Key 사용
- **사용자 API Key 모드** (`use_user_api_key: true`): 사용자 제공 API Key 우선 사용

### 5. Configuration (`src/config/`)

환경 변수와 설정을 관리합니다.

#### Config 클래스
```python
class Config:
    OPENAI_API_KEY: str = ""
    LOG_LEVEL: str = "INFO"
    MAX_TOKENS: int = 1000
    DEFAULT_TEMPERATURE: float = 0.7
    DEFAULT_MODEL: str = "gpt-4o-mini"
```

### 6. Utilities (`src/utils/`)

공통 유틸리티 기능을 제공합니다.

#### Logger
- 구조화된 로깅
- 로그 레벨 설정
- 파일 및 콘솔 출력

#### SystemInfo
- CPU, 메모리, 디스크 정보 수집
- 시스템 모니터링 API 지원

### 7. Exceptions (`src/exceptions/`)

커스텀 예외 클래스를 정의하여 일관된 오류 처리를 제공합니다.

#### 주요 예외:
- `ValidationException`: 데이터 검증 오류
- `OpenAIClientException`: OpenAI API 오류
- `ChatServiceException`: 채팅 서비스 오류
- `ConfigurationException`: 설정 오류

## 데이터 흐름

### 1. 채팅 요청 처리 흐름

```
HTTP Request → API Router → DTO Validation → Service → OpenAI Client → Response
```

1. **HTTP 요청 수신**: FastAPI가 `/api/v1/chat` 엔드포인트로 요청 수신
2. **DTO 검증**: Pydantic이 요청 데이터 자동 검증
3. **서비스 호출**: ChatService가 비즈니스 로직 처리
4. **OpenAI API 호출**: OpenAIClient가 외부 API 호출
5. **응답 생성**: 결과를 ChatResponse DTO로 변환하여 반환

### 2. API Key 선택 로직

```
사용자 요청 → API Key 선택 → 검증 → 사용
```

1. **기본 모드** (`use_user_api_key: false`):
   - 서버 관리 API Key 사용
   - 사용자 API Key가 제공되어도 무시

2. **사용자 API Key 모드** (`use_user_api_key: true`):
   - 사용자 제공 API Key 우선 사용
   - 유효하지 않으면 서버 관리 API Key로 폴백

## 개발 가이드라인

### 1. 코드 구조

#### 모듈화 원칙
- 단일 책임 원칙 (SRP) 준수
- 의존성 주입 패턴 사용
- 인터페이스와 구현 분리

#### 네이밍 컨벤션
- 클래스: PascalCase (`ChatService`)
- 함수/변수: snake_case (`process_chat_request`)
- 상수: UPPER_SNAKE_CASE (`DEFAULT_MODEL`)

### 2. 에러 처리

#### 계층별 예외 처리
```python
# API Layer
@router.post("/chat")
async def chat_with_ai(request: ChatRequest):
    try:
        response = chat_service.process_chat_request(request)
        return response
    except ValidationException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except OpenAIClientException as e:
        raise HTTPException(status_code=503, detail=str(e))
```

#### 커스텀 예외 사용
```python
class ValidationException(Exception):
    def __init__(self, message: str, field: str = None, value: str = None):
        self.message = message
        self.field = field
        self.value = value
```

### 3. 로깅

#### 구조화된 로깅
```python
logger.info(f"채팅 요청 처리 시작: {request.user_message[:50]}...")
logger.error(f"OpenAI API 호출 중 오류: {str(e)}")
```

#### 로그 레벨 활용
- `DEBUG`: 상세한 디버깅 정보
- `INFO`: 일반적인 처리 정보
- `WARNING`: 경고 상황
- `ERROR`: 오류 상황

### 4. 테스트

#### 테스트 구조
- **단위 테스트**: 개별 컴포넌트 테스트
- **시나리오 테스트**: 전체 흐름 테스트
- **통합 테스트**: API 엔드포인트 테스트

#### 테스트 실행
```bash
python run_tests.py
```

## 확장성 고려사항

### 1. 모듈 확장
- 새로운 AI 모델 추가 시 `OpenAIClient` 확장
- 새로운 기능 추가 시 `ChatService` 확장
- 새로운 API 추가 시 라우터 추가

### 2. 설정 관리
- 환경별 설정 분리 (개발/테스트/운영)
- 동적 설정 변경 지원
- 설정 검증 강화

### 3. 성능 최적화
- 비동기 처리 활용
- 캐싱 전략 수립
- 데이터베이스 연동 고려

## 보안 고려사항

### 1. API Key 관리
- 환경 변수를 통한 안전한 저장
- API Key 검증 및 폴백 로직
- 사용량 모니터링

### 2. 입력 검증
- Pydantic을 통한 자동 검증
- SQL Injection 방지
- XSS 공격 방지

### 3. 로깅 보안
- 민감한 정보 로깅 제외
- 로그 레벨 적절한 설정
- 로그 파일 접근 권한 관리

## 모니터링 및 운영

### 1. 헬스체크
- `/api/v1/system/status` 엔드포인트
- 시스템 리소스 모니터링
- API 응답 시간 측정

### 2. 로깅
- 구조화된 로그 형식
- 로그 레벨별 관리
- 로그 파일 로테이션

### 3. 에러 추적
- 상세한 에러 메시지
- 스택 트레이스 기록
- 에러 통계 수집

---
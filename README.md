# LLM Server

**OpenAI API 통합 채팅 서버**

FastAPI 기반의 채팅 서버로, OpenAI API를 활용한 대화형 AI 서비스를 제공합니다. 한국어 최적화 및 비용 효율적인 API 키 관리가 특징입니다.

## 주요 특징

- **유연한 API 키 관리**: 사용자 제공 키와 서버 키 간 자동 전환
- **비용 추적**: 토큰 사용량 기반 실시간 비용 계산
- **대화 히스토리**: 컨텍스트 유지를 위한 대화 기록 관리
- **시스템 모니터링**: CPU, 메모리 등 시스템 리소스 모니터링
- **한국어 최적화**: 한국어 환경에 특화된 프롬프트 처리

## 빠른 시작

### 1. 환경 설정

```bash
# 의존성 설치
pip install -r requirement.txt

# 환경 변수 설정
cp env.example .env
```

### 2. 서버 실행

```bash
# 개발 환경
python app.py

# 프로덕션 환경 (Docker)
docker-compose up --build
```

### 3. API 테스트

```bash
# 서버 상태 확인
curl http://localhost:8080/api/v1/

# API 문서 확인
open http://localhost:8080/docs
```

## API 사용법

### 기본 채팅 요청

```python
import requests

response = requests.post("http://localhost:8080/api/v1/chat", json={
    "request_id": "unique_session_id",
    "user_prompt": "Python의 특징을 설명해주세요.",
    "system_prompt": "당신은 친절한 프로그래밍 튜터입니다.",
    "max_tokens": 1000,
    "temperature": 0.7,
    "model": "gpt-4o-mini"
})

result = response.json()
print(result['output_text'])
```

### 사용자 API 키 사용

```python
response = requests.post("http://localhost:8080/api/v1/chat", json={
    "user_prompt": "안녕하세요!",
    "openai_api_key": "sk-your-api-key",
    "use_user_api_key": True
})
```

## 프로젝트 구조

```
LLM Server/
├── app.py                   # FastAPI 애플리케이션 진입점
├── requirement.txt          # Python 의존성 패키지
├── env.example             # 환경 변수 설정 예시
├── docker-compose.yml      # Docker 컨테이너 설정
├── run_tests.py           # 테스트 실행 스크립트
├── sample.py              # API 사용 예시 코드
└── src/
    ├── api/               # API 레이어
    │   ├── routes.py      # 메인 채팅 API 엔드포인트
    │   ├── system_routes.py # 시스템 모니터링 API
    │   └── exception_handlers.py # 전역 예외 처리
    ├── services/          # 비즈니스 로직
    │   └── chat_service.py # 채팅 요청 처리 서비스
    ├── external/          # 외부 API 연동
    │   └── openai_client.py # OpenAI API 클라이언트
    ├── dto/              # 데이터 전송 객체
    │   ├── request_dto.py # 요청 데이터 모델
    │   └── response_dto.py # 응답 데이터 모델
    ├── config/           # 설정 관리
    │   └── config.py     # 환경 변수 및 설정
    ├── utils/            # 유틸리티
    │   ├── cost_calculator.py # 비용 계산
    │   └── error_handler.py # 오류 처리
    └── exceptions/       # 커스텀 예외
        └── chat_exceptions.py # 채팅 관련 예외
```

## 아키텍처 개요

### 요청 처리 흐름
1. **API 계층** (`routes.py`): HTTP 요청 수신 및 유효성 검사
2. **서비스 계층** (`chat_service.py`): 비즈니스 로직 처리
3. **외부 API** (`openai_client.py`): OpenAI API 호출
4. **응답 생성**: 비용 계산 및 성능 메트릭 포함

### 핵심 컴포넌트

**ChatService** (`src/services/chat_service.py:19`)
- 채팅 요청의 핵심 비즈니스 로직 처리
- API 키 선택 및 검증
- 비용 계산 및 토큰 사용량 추적

**OpenAIClient** (`src/external/openai_client.py:10`)
- OpenAI Responses API 활용
- 스트리밍, 백그라운드 처리 지원
- 웹 검색 통합 기능

**API 키 관리 로직** (`src/services/chat_service.py:36`)
- `use_user_api_key=True`: 사용자 제공 키 우선 사용
- `use_user_api_key=False`: 서버 관리 키 사용
- 비용 추적은 서버 키 사용 시에만 적용

## 테스트

```bash
# 전체 테스트 실행
python run_tests.py

# 단위 테스트만 실행
python -m unittest tests.test_unit

# 시나리오 테스트만 실행
python -m unittest tests.test_scenarios
```

## 배포

```bash
# Docker로 배포
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 상태 확인
curl http://localhost:8080/api/v1/system/status
```

## 환경 변수

```env
# 서버 설정
SERVER_PORT=8080

# OpenAI API
OPENAI_API_KEY=your_api_key_here

# 로깅
LOG_LEVEL=INFO
```

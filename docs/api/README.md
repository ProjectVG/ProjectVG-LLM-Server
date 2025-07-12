# LLM Server API 문서

이 문서는 LLM Server의 모든 API 엔드포인트에 대한 상세한 명세를 제공합니다.

## 📋 API 개요

- **Base URL**: `http://localhost:5601`
- **API Version**: v1
- **Content-Type**: `application/json`
- **문서**: http://localhost:5601/docs (FastAPI 자동 생성)

## 🔗 엔드포인트 목록

### 채팅 API
- **POST /api/v1/chat** - AI와의 채팅 기능

### 시스템 모니터링 API
- **GET /api/v1/system/info** - 전체 시스템 정보
- **GET /api/v1/system/status** - 헬스체크
- **GET /api/v1/system/cpu** - CPU 정보
- **GET /api/v1/system/memory** - 메모리 정보
- **GET /api/v1/system/disk** - 디스크 정보

### 기본 API
- **GET /api/v1/** - 서버 상태 확인

---

## 🤖 채팅 API

### POST /api/v1/chat

AI와의 채팅을 수행하는 메인 엔드포인트입니다.

#### Request Body

```json
{
  "session_id": "string",
  "system_message": "string",
  "user_message": "string",
  "role": "string",
  "instructions": "string",
  "conversation_history": ["string"],
  "memory_context": ["string"],
  "max_tokens": 1000,
  "temperature": 0.7,
  "model": "gpt-4o-mini",
  "openai_api_key": "string",
  "free_mode": false
}
```

#### 필드 상세 설명

| 필드 | 타입 | 필수 | 기본값 | 설명 |
|------|------|------|--------|------|
| `session_id` | string | ❌ | "" | 세션 ID (로깅 및 추적용) |
| `system_message` | string | ❌ | "" | 추가 시스템 프롬프트 메시지 |
| `user_message` | string | ❌ | "" | 사용자 입력 메시지 |
| `role` | string | ❌ | "" | AI 역할 설정 (시스템 프롬프트에 포함) |
| `instructions` | string | ❌ | "" | 추가 지시사항 |
| `conversation_history` | string[] | ❌ | [] | 최근 대화 내역 |
| `memory_context` | string[] | ❌ | [] | 장기 기억 Context |
| `max_tokens` | int | ❌ | 1000 | 최대 토큰 수 (0보다 커야 함) |
| `temperature` | float | ❌ | 0.7 | 생성 온도 (0-2 사이) |
| `model` | string | ❌ | "gpt-4o-mini" | 사용할 OpenAI 모델 |
| `openai_api_key` | string | ❌ | "" | 사용할 OpenAI API Key |
| `free_mode` | bool | ❌ | false | Free 모드 (API Key 실패 시 기본 Key 사용) |

#### conversation_history 필드 형식

conversation_history 배열의 각 항목은 `"role:content"` 형태의 문자열입니다.

- `role`: "user" 또는 "assistant"
- `content`: 실제 대화 내용

**예시:**
```json
[
  "user:안녕하세요",
  "assistant:안녕하세요! 무엇을 도와드릴까요?",
  "user:파이썬에 대해 알려주세요"
]
```

#### API Key 사용 방식

1. **일반 모드** (`free_mode: false`):
   - `openai_api_key`가 제공되어야 함
   - API Key가 유효하지 않으면 오류 발생

2. **Free 모드** (`free_mode: true`):
   - `openai_api_key`가 제공되면 우선 사용
   - API Key가 유효하지 않거나 제공되지 않으면 기본 Key 사용
   - 사용자 관리 및 사용량 추적 가능

#### Response

```json
{
  "session_id": "string",
  "response_text": "string",
  "model": "string",
  "input_tokens": 0,
  "output_tokens": 0,
  "total_tokens_used": 0,
  "output_format": "string",
  "created_at": "2024-01-01T00:00:00",
  "temperature": 0.0,
  "instructions": "string",
  "response_time": 0.0,
  "success": true,
  "error_message": null,
  "api_key_source": "user_provided"
}
```

#### Response 필드 설명

| 필드 | 타입 | 설명 |
|------|------|------|
| `session_id` | string | 세션 ID |
| `response_text` | string | AI 응답 텍스트 |
| `model` | string | 사용된 OpenAI 모델명 |
| `input_tokens` | int | 입력 토큰 수 |
| `output_tokens` | int | 출력 토큰 수 |
| `total_tokens_used` | int | 총 토큰 수 |
| `output_format` | string | 출력 형식 |
| `created_at` | string | 응답 생성 시간 (ISO 8601) |
| `temperature` | float | 사용된 temperature 값 |
| `instructions` | string | 전달된 지시사항 |
| `response_time` | float | 응답 처리 시간 (초) |
| `success` | bool | 성공 여부 |
| `error_message` | string | 오류 메시지 (실패 시) |
| `api_key_source` | string | 사용된 API Key 소스 ("user_provided" 또는 "default") |

#### HTTP 상태 코드

- `200 OK`: 성공적인 응답
- `400 Bad Request`: 요청 데이터 검증 오류
- `422 Unprocessable Entity`: 요청 데이터 형식 오류
- `500 Internal Server Error`: 서버 내부 오류
- `503 Service Unavailable`: AI 서비스 연결 오류

#### 사용 예시

**기본 사용:**
```python
import requests

response = requests.post("http://localhost:5601/api/v1/chat", json={
    "session_id": "session_123",
    "user_message": "파이썬에 대해 알려주세요",
    "role": "당신은 친근하고 유머러스한 AI 어시스턴트입니다.",
    "max_tokens": 1000,
    "temperature": 0.7
})

result = response.json()
print(result['response_text'])
```

**Free 모드 사용:**
```python
response = requests.post("http://localhost:5601/api/v1/chat", json={
    "session_id": "session_123",
    "user_message": "파이썬에 대해 알려주세요",
    "openai_api_key": "sk-your-api-key",
    "free_mode": True,
    "conversation_history": [
        "user:안녕하세요",
        "assistant:안녕하세요! 무엇을 도와드릴까요?"
    ]
})

result = response.json()
print(f"응답: {result['response_text']}")
print(f"API Key 소스: {result['api_key_source']}")
```

---

## 📊 시스템 모니터링 API

### GET /api/v1/system/info

전체 시스템 정보를 반환합니다.

#### Response

```json
{
  "timestamp": "2024-01-01T00:00:00",
  "system": {
    "platform": "Windows",
    "platform_version": "10.0.26100",
    "architecture": "AMD64",
    "processor": "Intel64 Family 6",
    "hostname": "DESKTOP-XXXXX",
    "python_version": "3.11.0"
  },
  "cpu": {
    "usage_percent": 25.5,
    "count": 8,
    "frequency": 2400.0
  },
  "memory": {
    "total": 8589934592,
    "available": 4294967296,
    "used": 4294967296,
    "usage_percent": 50.0
  },
  "disk": {
    "total": 107374182400,
    "used": 53687091200,
    "free": 53687091200,
    "usage_percent": 50.0
  }
}
```

### GET /api/v1/system/status

간단한 헬스체크를 위한 엔드포인트입니다.

#### Response

```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00",
  "uptime": 3600.5
}
```

### GET /api/v1/system/cpu

CPU 정보만 반환합니다.

#### Response

```json
{
  "timestamp": "2024-01-01T00:00:00",
  "cpu": {
    "usage_percent": 25.5,
    "count": 8,
    "frequency": 2400.0
  }
}
```

### GET /api/v1/system/memory

메모리 정보만 반환합니다.

#### Response

```json
{
  "timestamp": "2024-01-01T00:00:00",
  "memory": {
    "total": 8589934592,
    "available": 4294967296,
    "used": 4294967296,
    "usage_percent": 50.0
  }
}
```

### GET /api/v1/system/disk

디스크 정보만 반환합니다.

#### Response

```json
{
  "timestamp": "2024-01-01T00:00:00",
  "disk": {
    "total": 107374182400,
    "used": 53687091200,
    "free": 53687091200,
    "usage_percent": 50.0
  }
}
```

---

## 🔗 관련 문서

- **[개요 및 시작 가이드](./../overview/README.md)**: 프로젝트 소개 및 기본 사용법
- **[배포 가이드](./../deployment/README.md)**: 배포 및 운영 가이드
- **[아키텍처 가이드](./../architecture/README.md)**: 프로젝트 구조 및 개발 가이드
- **[테스트 가이드](./../testing/README.md)**: 테스트 및 품질 관리

---

**문서 버전**: 1.0  
**최종 업데이트**: 2024년 12월  
**작성자**: LLM Server 개발팀 
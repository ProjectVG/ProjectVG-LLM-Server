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
- **GET /** - 서버 상태 확인

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
| `user_message` | string | ✅ | - | 사용자 입력 메시지 |
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
    "usage_percent": 15.2,
    "count": 8,
    "frequency_mhz": 2400.0,
    "frequency_max_mhz": 3200.0,
    "load_average": [0.5, 0.3, 0.2]
  },
  "memory": {
    "total_gb": 16.0,
    "available_gb": 8.0,
    "used_gb": 8.0,
    "usage_percent": 50.0,
    "swap_total_gb": 2.0,
    "swap_used_gb": 0.1,
    "swap_usage_percent": 5.0
  },
  "disk": {
    "total_gb": 500.0,
    "used_gb": 200.0,
    "free_gb": 300.0,
    "usage_percent": 40.0,
    "read_bytes": 1024000,
    "write_bytes": 512000,
    "read_count": 100,
    "write_count": 50
  },
  "network": {
    "bytes_sent": 1000000,
    "bytes_recv": 2000000,
    "packets_sent": 1000,
    "packets_recv": 2000,
    "active_connections": 150
  },
  "process": {
    "pid": 1234,
    "name": "python.exe",
    "cpu_percent": 2.5,
    "memory_mb": 128.5,
    "memory_percent": 1.2,
    "num_threads": 8,
    "create_time": "2024-01-01T00:00:00"
  },
  "docker": {
    "is_docker": false,
    "container_id": null,
    "image": null
  }
}
```

### GET /api/v1/system/status

간단한 시스템 상태(헬스체크용)를 반환합니다.

#### Response

```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00",
  "cpu_usage": 15.2,
  "memory_usage": 35.0,
  "memory_available_gb": 5.2
}
```

### GET /api/v1/system/cpu

CPU 정보만 반환합니다.

#### Response

```json
{
  "timestamp": "2024-01-01T00:00:00",
  "cpu": {
    "usage_percent": 15.2,
    "count": 8,
    "frequency_mhz": 2400.0,
    "frequency_max_mhz": 3200.0,
    "load_average": [0.5, 0.3, 0.2]
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
    "total_gb": 16.0,
    "available_gb": 8.0,
    "used_gb": 8.0,
    "usage_percent": 50.0,
    "swap_total_gb": 2.0,
    "swap_used_gb": 0.1,
    "swap_usage_percent": 5.0
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
    "total_gb": 500.0,
    "used_gb": 200.0,
    "free_gb": 300.0,
    "usage_percent": 40.0,
    "read_bytes": 1024000,
    "write_bytes": 512000,
    "read_count": 100,
    "write_count": 50
  }
}
```

---

## ⚠️ 에러 처리

API는 체계적인 예외 처리 시스템을 사용하며, 다음과 같은 커스텀 예외들을 제공합니다:

### 예외 타입

1. **ValidationException** (400 Bad Request)
   - 요청 데이터 검증 실패
   - 필수 필드 누락, 잘못된 값 형식 등

2. **ConfigurationException** (500 Internal Server Error)
   - 시스템 설정 오류
   - API 키 누락, 환경 변수 오류 등

3. **ChatServiceException** (503 Service Unavailable)
   - 채팅 서비스 처리 중 오류
   - 비즈니스 로직 오류

4. **OpenAIClientException** (503 Service Unavailable)
   - OpenAI API 연결 오류
   - API 호출 실패, 네트워크 오류 등

### 에러 응답 형식

모든 에러는 일관된 형식으로 응답됩니다:

```json
{
  "session_id": "string",
  "response_text": "",
  "model": "",
  "input_tokens": 0,
  "output_tokens": 0,
  "total_tokens_used": 0,
  "output_format": "",
  "created_at": "2024-01-01T00:00:00",
  "temperature": null,
  "instructions": null,
  "response_time": 0.0,
  "success": false,
  "error_message": "오류 메시지",
  "api_key_source": null
}
```

### 검증 규칙

- `user_message`: 필수 필드, 빈 문자열 불가
- `max_tokens`: 0보다 커야 함
- `temperature`: 0과 2 사이의 값이어야 함
- `conversation_history`: 각 항목은 "role:content" 형식이어야 함
- `openai_api_key`: 일반 모드에서는 유효한 API Key 필요

---

## 📝 주의사항

1. **토큰 제한**: OpenAI API의 토큰 제한을 고려하여 conversation_history 길이를 적절히 관리하세요.
2. **메모리 관리**: memory_context 배열이 너무 길면 시스템 프롬프트가 복잡해질 수 있습니다.
3. **히스토리 형식**: conversation_history 배열의 각 항목은 반드시 "role:content" 형식을 지켜야 합니다.
4. **에러 처리**: 모든 API 호출은 적절한 에러 처리를 포함해야 합니다.
5. **API Key 보안**: API Key는 안전하게 관리하고, 응답에는 실제 키값이 포함되지 않습니다.

---

## 🔗 관련 문서

- **[API 테스트 예시](./test-examples.md)**: 다양한 언어별 API 사용 예시
- **[시스템 모니터링 상세](./system-monitoring.md)**: 시스템 모니터링 API 상세 가이드
- **[에러 처리 가이드](./error-handling.md)**: 에러 처리 및 디버깅 가이드

---

**문서 버전**: 1.0  
**최종 업데이트**: 2024년 12월  
**작성자**: LLM Server 개발팀 
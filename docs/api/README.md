# API 문서

## 개요

LLM Server는 OpenAI API를 활용한 채팅 서비스를 제공합니다. RESTful API를 통해 AI와의 대화를 지원하며, 다양한 매개변수를 통해 대화를 커스터마이징할 수 있습니다.

## 기본 정보

- **Base URL**: `http://localhost:8000`
- **API 버전**: v1
- **Content-Type**: `application/json`

## 엔드포인트

### POST /api/v1/chat

AI와 채팅하는 메인 엔드포인트입니다.

#### 요청 본문 (Request Body)

```json
{
  "session_id": "session-123",
  "system_message": "당신은 친근한 AI 어시스턴트입니다.",
  "user_message": "안녕하세요!",
  "role": "당신은 프로그래밍 전문가입니다.",
  "instructions": "간단하고 명확하게 답변해주세요.",
  "conversation_history": [
    "user: 이전 대화 내용",
    "assistant: AI 응답 내용"
  ],
  "memory_context": [
    "사용자가 파이썬을 좋아함",
    "사용자는 간단한 설명을 선호함"
  ],
  "max_tokens": 1000,
  "temperature": 0.7,
  "model": "gpt-4o-mini",
  "openai_api_key": "sk-...",
  "use_user_api_key": false
}
```

#### 필드 설명

| 필드 | 타입 | 필수 | 기본값 | 설명 |
|------|------|------|--------|------|
| `session_id` | string | ❌ | "" | 세션 식별자 |
| `system_message` | string | ❌ | "" | 시스템 메시지 |
| `user_message` | string | ✅ | "" | 사용자 메시지 |
| `role` | string | ❌ | "" | AI 역할 설정 |
| `instructions` | string | ❌ | "" | 추가 지시사항 |
| `conversation_history` | array | ❌ | [] | 대화 히스토리 |
| `memory_context` | array | ❌ | [] | 메모리 컨텍스트 |
| `max_tokens` | integer | ❌ | 1000 | 최대 토큰 수 |
| `temperature` | float | ❌ | 0.7 | 응답 창의성 (0-2) |
| `model` | string | ❌ | "gpt-4o-mini" | 사용할 모델 |
| `openai_api_key` | string | ❌ | "" | 사용자 OpenAI API Key |
| `use_user_api_key` | bool | ❌ | false | 사용자 API Key 사용 여부 |

#### API Key 관리

시스템은 두 가지 모드로 API Key를 관리합니다:

1. **기본 모드** (`use_user_api_key: false`):
   - 서버에서 관리하는 기본 API Key 사용
   - 사용자가 API Key를 제공하지 않아도 동작

2. **사용자 API Key 모드** (`use_user_api_key: true`):
   - 사용자가 제공한 API Key 우선 사용
   - 유효하지 않은 경우 기본 API Key로 폴백

#### 응답 본문 (Response Body)

```json
{
  "success": true,
  "response_text": "안녕하세요! 무엇을 도와드릴까요?",
  "session_id": "session-123",
  "response_time": 2.34,
  "api_key_source": "default",
  "model_used": "gpt-4o-mini",
  "tokens_used": {
    "prompt_tokens": 45,
    "completion_tokens": 23,
    "total_tokens": 68
  },
  "error": null
}
```

#### 응답 필드 설명

| 필드 | 타입 | 설명 |
|------|------|------|
| `success` | boolean | 요청 성공 여부 |
| `response_text` | string | AI 응답 텍스트 |
| `session_id` | string | 세션 식별자 |
| `response_time` | float | 응답 시간 (초) |
| `api_key_source` | string | 사용된 API Key 소스 ("default" 또는 "user_provided") |
| `model_used` | string | 사용된 모델명 |
| `tokens_used` | object | 토큰 사용량 정보 |
| `error` | object/null | 오류 정보 (성공 시 null) |

## 사용 예제

### 기본 채팅

```python
import requests

url = "http://localhost:8000/api/v1/chat"
data = {
    "user_message": "파이썬이 뭐야?",
    "max_tokens": 500,
    "use_user_api_key": False
}

response = requests.post(url, json=data)
result = response.json()
print(result["response_text"])
```

### 역할 기반 채팅

```python
data = {
    "user_message": "프로그래밍을 가르쳐주세요",
    "role": "당신은 친근하고 이해하기 쉬운 프로그래밍 선생님입니다.",
    "instructions": "초보자에게 적합한 설명을 해주세요.",
    "use_user_api_key": False
}
```

### 메모리 컨텍스트 활용

```python
data = {
    "user_message": "내가 좋아하는 색깔이 뭐였지?",
    "memory_context": ["사용자가 파란색을 좋아한다고 언급함"],
    "use_user_api_key": False
}
```

### 사용자 API Key 사용

```python
data = {
    "user_message": "안녕하세요",
    "openai_api_key": "sk-your-api-key-here",
    "use_user_api_key": True
}
```

## 오류 응답

```json
{
  "success": false,
  "response_text": null,
  "session_id": "session-123",
  "response_time": 0.0,
  "api_key_source": null,
  "model_used": null,
  "tokens_used": null,
  "error": {
    "message": "user_message는 필수 필드입니다.",
    "error_code": "VALIDATION_ERROR",
    "field": "user_message",
    "value": ""
  }
}
```

## 상태 코드

- `200`: 성공
- `400`: 잘못된 요청 (검증 오류)
- `422`: 요청 데이터 검증 실패
- `500`: 서버 내부 오류

## 제한사항

- `max_tokens`: 1-4000 (OpenAI API 제한)
- `temperature`: 0.0-2.0
- `conversation_history`: 최대 50개 메시지 권장
- `memory_context`: 최대 20개 항목 권장 
# LLM Server API

OpenAI API를 활용한 채팅 서버로, 시스템 프롬프트와 대화 히스토리를 관리하여 일관된 AI 응답을 제공합니다.

## 기본 정보

- **Base URL**: `http://localhost:5601`
- **API Version**: v1
- **Content-Type**: `application/json`

## 엔드포인트

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
  "model": "gpt-4o-mini"
}
```

#### 필드 설명

| 필드 | 타입 | 필수 | 기본값 | 설명 |
|------|------|------|--------|------|
| `session_id` | string | X | "" | 세션 ID |
| `system_message` | string | X | "" | 추가 시스템 프롬프트 메시지 |
| `user_message` | string | O | - | 사용자 입력 메시지 |
| `role` | string | X | "" | AI 역할 설정 (시스템 프롬프트에 포함) |
| `instructions` | string | X | "" | 추가 지시사항 |
| `conversation_history` | string[] | X | [] | 최근 대화 내역 |
| `memory_context` | string[] | X | [] | 장기 기억 Context |
| `max_tokens` | int | X | 1000 | 최대 토큰 수 (0보다 커야 함) |
| `temperature` | float | X | 0.7 | 생성 온도 (0-2 사이) |
| `model` | string | X | "gpt-4o-mini" | 사용할 모델 |

#### conversation_history 필드 형식

conversation_history 배열의 각 항목은 `"role:content"` 형태의 문자열입니다.

- `role`: "user" 또는 "assistant"
- `content`: 실제 대화 내용

예시:
```json
[
  "user:안녕하세요",
  "assistant:안녕하세요! 무엇을 도와드릴까요?",
  "user:파이썬에 대해 알려주세요"
]
```

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
  "error_message": null
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

#### HTTP 상태 코드

- `200 OK`: 성공적인 응답
- `400 Bad Request`: 요청 데이터 검증 오류
- `422 Unprocessable Entity`: 요청 데이터 형식 오류
- `500 Internal Server Error`: 서버 내부 오류
- `503 Service Unavailable`: AI 서비스 연결 오류

### GET /api/v1/

루트 엔드포인트로 API 기본 정보를 반환합니다.

#### Response

```json
{
  "message": "LLM Server API",
  "status": "running"
}
```



## 에러 처리

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
  "error_message": "오류 메시지"
}
```

### 검증 규칙

- `user_message`: 필수 필드, 빈 문자열 불가
- `max_tokens`: 0보다 커야 함
- `temperature`: 0과 2 사이의 값이어야 함
- `conversation_history`: 각 항목은 "role:content" 형식이어야 함

## 주의사항

1. **토큰 제한**: OpenAI API의 토큰 제한을 고려하여 conversation_history 길이를 적절히 관리하세요.
2. **메모리 관리**: memory_context 배열이 너무 길면 시스템 프롬프트가 복잡해질 수 있습니다.
3. **히스토리 형식**: conversation_history 배열의 각 항목은 반드시 "role:content" 형식을 지켜야 합니다.
4. **에러 처리**: 모든 API 호출은 적절한 에러 처리를 포함해야 합니다.

## 사용 예시

### JavaScript (Node.js)

```javascript
const axios = require('axios');

async function chatWithAI(sessionId, userMessage, history = [], memory = [], role = "") {
  try {
    const response = await axios.post('http://localhost:5601/api/v1/chat', {
      session_id: sessionId,
      system_message: '친근하게 대화해주세요',
      user_message: userMessage,
      role: role,
      instructions: '간결하고 명확하게 답변해주세요',
      conversation_history: history,
      memory_context: memory,
      max_tokens: 1000,
      temperature: 0.7,
      model: 'gpt-4o-mini'
    });
    
    return response.data;
  } catch (error) {
    if (error.response) {
      console.error('API Error:', error.response.data);
      return error.response.data;
    } else {
      console.error('Network Error:', error.message);
      throw error;
    }
  }
}

// 사용 예시
const sessionId = 'session_123';
const history = [
  'user:안녕하세요',
  'assistant:안녕하세요! 무엇을 도와드릴까요?'
];
const memory = ['사용자는 개발자입니다'];
const role = '당신은 친근하고 유머러스한 AI 어시스턴트입니다.';

chatWithAI(sessionId, '파이썬에 대해 알려주세요', history, memory, role)
  .then(response => {
    if (response.success) {
      console.log('AI Response:', response.response_text);
      console.log('Token Usage:', response.total_tokens_used);
    } else {
      console.log('Error:', response.error_message);
    }
  });
```

### Python

```python
import requests

def chat_with_ai(session_id, user_message, history=None, memory=None, role=""):
    if history is None:
        history = []
    if memory is None:
        memory = []
    
    payload = {
        'session_id': session_id,
        'system_message': '친근하게 대화해주세요',
        'user_message': user_message,
        'role': role,
        'instructions': '간결하고 명확하게 답변해주세요',
        'conversation_history': history,
        'memory_context': memory,
        'max_tokens': 1000,
        'temperature': 0.7,
        'model': 'gpt-4o-mini'
    }
    
    try:
        response = requests.post('http://localhost:5601/api/v1/chat', json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API 호출 오류: {e}")
        return None

# 사용 예시
session_id = 'session_123'
history = [
    'user:안녕하세요',
    'assistant:안녕하세요! 무엇을 도와드릴까요?'
]
memory = ['사용자는 개발자입니다']
role = '당신은 친근하고 유머러스한 AI 어시스턴트입니다.'

result = chat_with_ai(session_id, '파이썬에 대해 알려주세요', history, memory, role)
if result and result.get('success'):
    print('AI Response:', result['response_text'])
    print('Token Usage:', result['total_tokens_used'])
else:
    print('Error:', result.get('error_message', 'Unknown error'))
```

### cURL

```bash
curl -X POST "http://localhost:5601/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "session_123",
    "user_message": "파이썬에 대해 알려주세요",
    "role": "당신은 친근하고 유머러스한 AI 어시스턴트입니다.",
    "instructions": "간결하고 명확하게 답변해주세요",
    "conversation_history": [
      "user:안녕하세요",
      "assistant:안녕하세요! 무엇을 도와드릴까요?"
    ],
    "memory_context": ["사용자는 개발자입니다"],
    "max_tokens": 1000,
    "temperature": 0.7,
    "model": "gpt-4o-mini"
  }'
```

## 관련 문서

- **시스템 모니터링 API**: [SYSTEM_API_README.md](SYSTEM_API_README.md) - 시스템 정보 및 헬스체크 엔드포인트
- **프로젝트 README**: [../../README.md](../../README.md) - 전체 프로젝트 개요 및 설정 방법 
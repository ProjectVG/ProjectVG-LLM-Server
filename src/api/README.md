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
  "message": "string",
  "memory": ["string"],
  "instructions": "string",
  "history": ["string"]
}
```

#### 필드 설명

| 필드 | 타입 | 필수 | 기본값 | 설명 |
|------|------|------|--------|------|
| `message` | string | O | - | 사용자 입력 메시지 |
| `memory` | string[] | X | [] | AI가 기억할 정보 목록 |
| `instructions` | string | X | "" | 추가 지시사항 |
| `history` | string[] | X | [] | 대화 히스토리 (형식: "role:content") |

#### history 필드 형식

history 배열의 각 항목은 `"role:content"` 형태의 문자열입니다.

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
  "response_text": "string",
  "response_id": "string",
  "model": "string",
  "input_tokens": 0,
  "output_tokens": 0,
  "total_tokens": 0,
  "output_format": "string",
  "created_at": "2024-01-01T00:00:00",
  "temperature": 0.0,
  "instructions": "string",
  "response_time": 0.0
}
```

#### Response 필드 설명

| 필드 | 타입 | 설명 |
|------|------|------|
| `response_text` | string | AI 응답 텍스트 |
| `response_id` | string | OpenAI 응답 ID |
| `model` | string | 사용된 OpenAI 모델명 |
| `input_tokens` | int | 입력 토큰 수 |
| `output_tokens` | int | 출력 토큰 수 |
| `total_tokens` | int | 총 토큰 수 |
| `output_format` | string | 출력 형식 |
| `created_at` | string | 응답 생성 시간 (ISO 8601) |
| `temperature` | float | 사용된 temperature 값 |
| `instructions` | string | 전달된 지시사항 |
| `response_time` | float | 응답 처리 시간 (초) |

#### HTTP 상태 코드

- `200 OK`: 성공적인 응답
- `500 Internal Server Error`: 서버 내부 오류

#### 사용 예시

```bash
curl -X POST "http://localhost:5601/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "안녕하세요!",
    "memory": ["사용자는 프로그래밍을 좋아함"],
    "instructions": "친근하게 대화해주세요",
    "history": [
      "user:안녕하세요",
      "assistant:안녕하세요! 무엇을 도와드릴까요?"
    ]
  }'
```

### GET /api/v1/hello

서버 상태 확인용 엔드포인트입니다.

#### Response

```json
{
  "message": "Hello, World!",
  "status": "success"
}
```

### GET /

루트 엔드포인트로 API 기본 정보를 반환합니다.

#### Response

```json
{
  "message": "LLM Server API",
  "status": "running"
}
```

## 에러 처리

API는 표준 HTTP 상태 코드를 사용하며, 오류 발생 시 다음과 같은 형식으로 응답합니다:

```json
{
  "detail": "오류 메시지"
}
```

## 주의사항

1. **토큰 제한**: OpenAI API의 토큰 제한을 고려하여 history 길이를 적절히 관리하세요.
2. **메모리 관리**: memory 배열이 너무 길면 시스템 프롬프트가 복잡해질 수 있습니다.
3. **히스토리 형식**: history 배열의 각 항목은 반드시 "role:content" 형식을 지켜야 합니다.

## 구현 예시

### JavaScript (Node.js)

```javascript
const axios = require('axios');

async function chatWithAI(message, history = []) {
  try {
    const response = await axios.post('http://localhost:5601/api/v1/chat', {
      message: message,
      memory: ['사용자는 개발자입니다'],
      history: history
    });
    
    return response.data;
  } catch (error) {
    console.error('Chat error:', error.response.data);
    throw error;
  }
}

// 사용 예시
const history = [
  'user:안녕하세요',
  'assistant:안녕하세요! 무엇을 도와드릴까요?'
];

chatWithAI('파이썬에 대해 알려주세요', history)
  .then(response => {
    console.log('AI Response:', response.response_text);
  });
```

### Python

```python
import requests

def chat_with_ai(message, history=None):
    if history is None:
        history = []
    
    payload = {
        'message': message,
        'memory': ['사용자는 개발자입니다'],
        'history': history
    }
    
    response = requests.post('http://localhost:5601/api/v1/chat', json=payload)
    response.raise_for_status()
    
    return response.json()

# 사용 예시
history = [
    'user:안녕하세요',
    'assistant:안녕하세요! 무엇을 도와드릴까요?'
]

result = chat_with_ai('파이썬에 대해 알려주세요', history)
print('AI Response:', result['response_text'])
``` 
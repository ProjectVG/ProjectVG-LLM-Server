# OpenAI Responses API 완전 가이드

## 개요
OpenAI Responses API는 2025년 3월에 출시된 가장 진보된 API로, Chat Completions API와 Assistants API의 장점을 하나의 통합된 인터페이스로 결합했습니다. 상태 관리(stateful), 내장 도구, 웹 검색, 파일 검색 등 고급 기능을 자동으로 처리합니다.

## 기본 정보

**엔드포인트:** `POST https://api.openai.com/v1/responses`  
**인증:** Bearer Token 방식  
**특징:** Chat Completions의 모든 기능 + 추가 고급 기능

## 완전 파라미터 가이드

### 핵심 파라미터

| 파라미터 | 타입 | 필수 | 기본값 | 설명 |
|---------|------|------|-------|------|
| `model` | string | ✓ | - | 사용할 AI 모델 |
| `input` | string/array | ✓ | - | 텍스트, 이미지, 파일 입력 |
| `instructions` | string/null | | null | 시스템(개발자) 메시지 |
| `max_output_tokens` | integer/null | | null | 최대 출력 토큰 수 |
| `temperature` | number/null | | 1 | 샘플링 온도 (0-2) |
| `top_p` | number/null | | 1 | 핵심 샘플링 확률 |

### 고급 기능 파라미터

| 파라미터 | 타입 | 기본값 | 설명 |
|---------|------|-------|------|
| `background` | boolean/null | false | 백그라운드 처리 여부 |
| `conversation` | string/object/null | null | 대화 컨텍스트 관리 |
| `previous_response_id` | string/null | null | 이전 응답 ID (멀티턴 대화) |
| `store` | boolean/null | true | 응답 저장 여부 |
| `stream` | boolean/null | false | 스트리밍 응답 여부 |
| `parallel_tool_calls` | boolean/null | true | 병렬 도구 호출 허용 |
| `max_tool_calls` | integer/null | null | 최대 도구 호출 수 |

### 도구 및 출력 옵션

| 파라미터 | 타입 | 설명 |
|---------|------|------|
| `tools` | array | 사용 가능한 도구 배열 |
| `tool_choice` | string/object | 도구 선택 방식 |
| `include` | array/null | 추가 출력 데이터 포함 옵션 |
| `text` | object | 텍스트 응답 구성 옵션 |
| `reasoning` | object/null | 추론 모델 설정 (o-시리즈 전용) |

### 메타데이터 및 보안

| 파라미터 | 타입 | 설명 |
|---------|------|------|
| `metadata` | map | 키-값 쌍 메타데이터 (16개 제한) |
| `safety_identifier` | string | 사용자 식별자 (정책 위반 감지) |
| `prompt_cache_key` | string | 캐시 최적화 키 |
| `service_tier` | string/null | 처리 계층 ('auto', 'default', 'flex', 'priority') |
| `truncation` | string/null | 컨텍스트 창 초과 시 처리 방식 |

### include 옵션 상세

```json
{
  "include": [
    "web_search_call.action.sources",
    "code_interpreter_call.outputs", 
    "computer_call_output.output.image_url",
    "file_search_call.results",
    "message.input_image.image_url",
    "message.output_text.logprobs",
    "reasoning.encrypted_content"
  ]
}
```

## 입력 형식 상세

### 1. 텍스트 입력
```python
# 간단한 문자열
response = client.responses.create(
    model="gpt-4o-mini",
    input="tell me a joke"
)

# 메시지 배열 형식
response = client.responses.create(
    model="gpt-4o-mini",
    input=[
        {"role": "system", "content": "당신은 도움이 되는 AI 어시스턴트입니다."},
        {"role": "user", "content": "파이썬으로 Hello World를 출력하는 방법을 알려주세요."}
    ]
)
```

### 2. 이미지 입력
```python
response = client.responses.create(
    model="gpt-4o-mini",
    input=[
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": "이 이미지에 무엇이 있나요?"},
                {"type": "input_image", "image_url": "https://example.com/image.jpg"}
            ]
        }
    ]
)
```

### 3. 파일 입력
```python
response = client.responses.create(
    model="gpt-4o-mini",
    input=[
        {
            "role": "user", 
            "content": [
                {"type": "input_text", "text": "이 문서를 요약해주세요."},
                {"type": "input_file", "file_id": "file-abc123"}
            ]
        }
    ]
)
```

## 응답 형식

### 성공 응답
```json
{
  "id": "resp_abc123",
  "object": "response",
  "created_at": 1234567890,
  "model": "gpt-4o-mini",
  "output_text": "AI 응답 텍스트",
  "temperature": 0.7,
  "text": {
    "format": {
      "type": "text"
    }
  },
  "usage": {
    "input_tokens": 50,
    "output_tokens": 100,
    "total_tokens": 150
  },
  "status": "completed"
}
```

### 응답 필드 설명

| 필드 | 타입 | 설명 |
|------|------|------|
| `id` | string | 응답의 고유 식별자 |
| `object` | string | 객체 타입 ("response") |
| `created_at` | integer | Unix 타임스탬프 |
| `model` | string | 사용된 모델명 |
| `output_text` | string | AI가 생성한 응답 텍스트 |
| `temperature` | number | 사용된 temperature 값 |
| `text.format.type` | string | 텍스트 형식 타입 |
| `usage.input_tokens` | integer | 입력에 사용된 토큰 수 |
| `usage.output_tokens` | integer | 출력에 사용된 토큰 수 |
| `usage.total_tokens` | integer | 총 사용된 토큰 수 |
| `status` | string | 응답 상태 |

## 실제 사용 예시

### 1. 기본 텍스트 응답
```python
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 간단한 예시
response = client.responses.create(
    model="gpt-4o-mini",
    input="Write a one-sentence bedtime story about a unicorn."
)
print(response.output_text)

# 상세 설정 예시
response = client.responses.create(
    model="gpt-4o-mini",
    input=[
        {"role": "system", "content": "당신은 친근한 한국어 AI 어시스턴트입니다."},
        {"role": "user", "content": "안녕하세요! 오늘 날씨가 어떤가요?"}
    ],
    instructions="간단하고 친근하게 답변해주세요.",
    temperature=0.7,
    max_output_tokens=1000,
    metadata={"user_id": "user_123", "session": "session_456"}
)
print(response.output_text)
```

### 2. 스트리밍 응답
```python
stream = client.responses.create(
    model="gpt-4o",
    input="Say 'double bubble bath' ten times fast.",
    stream=True,
)

print("스트리밍 응답:")
for chunk in stream:
    if chunk.output:
        for output in chunk.output:
            if hasattr(output, 'content') and output.content:
                print(output.content, end='', flush=True)
print()
```

### 3. 대화 상태 관리
```python
# 수동 대화 관리
history = [{"role": "user", "content": "tell me a joke"}]

response = client.responses.create(
    model="gpt-4o-mini", 
    input=history,
    store=False
)

# 히스토리에 응답 추가
history.extend([
    {"role": "assistant", "content": response.output_text},
    {"role": "user", "content": "tell me another one"}
])

# 다음 응답
response2 = client.responses.create(
    model="gpt-4o-mini",
    input=history,
    store=False
)

# 자동 대화 관리 (conversation 사용)
response1 = client.responses.create(
    model="gpt-4o-mini",
    input="knock knock.",
    conversation="conv_123"
)

response2 = client.responses.create(
    model="gpt-4o-mini", 
    input="Orange.",
    conversation="conv_123"
)
```

### 4. 백그라운드 처리 예시
```python
import time

# 백그라운드 처리 시작
response = client.responses.create(
    model="o3",
    input="Write a comprehensive analysis of quantum computing",
    background=True,
    max_output_tokens=4000
)

response_id = response.id
print(f"백그라운드 작업 시작: {response_id}")

# 상태 확인 루프
while True:
    status = client.responses.retrieve(response_id)
    print(f"상태: {status.status}")
    
    if status.status in ["completed", "failed", "cancelled"]:
        break
    
    time.sleep(5)  # 5초마다 확인

if status.status == "completed":
    print("완료된 응답:")
    print(status.output_text)
else:
    print(f"작업 실패 또는 취소: {status.status}")
```

### 5. 웹 검색 활용
```python
response = client.responses.create(
    model="gpt-4o-mini",
    input="2025년 한국의 최신 AI 기술 동향을 알려주세요",
    tools=[{"type": "web_search"}],
    include=["web_search_call.action.sources"]
)

print("응답:", response.output_text)

# 웹 검색 소스 정보 확인
if hasattr(response, 'web_search_sources'):
    print("\n참고 소스:")
    for source in response.web_search_sources:
        print(f"- {source}")
```

### 6. 파일 검색 활용
```python
# 먼저 파일 업로드
file = client.files.create(
    file=open("document.pdf", "rb"),
    purpose="assistants"
)

# 파일 검색을 통한 응답
response = client.responses.create(
    model="gpt-4o-mini",
    input="이 문서의 핵심 내용을 요약해주세요",
    tools=[{"type": "file_search", "file_search": {"vector_store_ids": [file.id]}}],
    include=["file_search_call.results"]
)
```

### 7. Azure OpenAI 사용법
```python
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), 
    "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
    azure_endpoint="https://YOUR-RESOURCE-NAME.openai.azure.com/",
    azure_ad_token_provider=token_provider,
    api_version="2024-10-21"
)

response = client.responses.create(
    model="gpt-4o-mini",  # Azure deployment name
    input="Hello from Azure!"
)
```

## 백그라운드 처리

### 상태 조회
**엔드포인트:** `GET /v1/responses/{id}`

### 취소 요청  
**엔드포인트:** `POST /v1/responses/{id}/cancel`

### 상태 값
- `queued`: 대기 중
- `in_progress`: 처리 중  
- `completed`: 완료
- `failed`: 실패
- `cancelled`: 취소됨

## 오류 처리

### 일반적인 오류 코드
- `400`: 잘못된 요청
- `401`: 인증 실패
- `429`: 요청 제한 초과
- `500`: 서버 오류

### 오류 응답 예시
```json
{
  "error": {
    "message": "Invalid API key provided",
    "type": "invalid_request_error",
    "code": "invalid_api_key"
  }
}
```

## 주의사항

1. **토큰 제한**: 모델별로 최대 토큰 수가 다름
2. **요청 제한**: API 키별 분당 요청 수 제한 존재
3. **백그라운드 처리**: 긴 작업은 백그라운드 처리 권장
4. **비용**: 사용한 토큰 수에 따라 과금

## 지원 모델

- `gpt-4o-mini`: 빠르고 효율적인 모델
- `gpt-4o`: 고성능 범용 모델
- `o3`: 최신 고급 모델 (백그라운드 처리 지원)

## 내장 도구 (Built-in Tools)

### 웹 검색 (Web Search)
```python
response = client.responses.create(
    model="gpt-4o-mini",
    input="최신 AI 뉴스를 알려주세요",
    tools=[{"type": "web_search"}],
    include=["web_search_call.action.sources"]
)
```

### 파일 검색 (File Search) 
```python
response = client.responses.create(
    model="gpt-4o-mini",
    input="문서에서 핵심 포인트를 찾아주세요",
    tools=[{
        "type": "file_search",
        "file_search": {"vector_store_ids": ["vs_123"]}
    }],
    include=["file_search_call.results"]
)
```

### 코드 인터프리터 (Code Interpreter)
```python
response = client.responses.create(
    model="gpt-4o-mini",
    input="데이터를 분석하고 그래프를 그려주세요",
    tools=[{"type": "code_interpreter"}],
    include=["code_interpreter_call.outputs"]
)
```

### 컴퓨터 사용 (Computer Use - Preview)
```python
response = client.responses.create(
    model="computer-use-preview",
    input="웹 브라우저를 열고 특정 사이트를 방문해주세요",
    tools=[{"type": "computer"}],
    include=["computer_call_output.output.image_url"]
)
```

## 고급 기능

### 1. 추론 모델 설정 (o-시리즈)
```python
response = client.responses.create(
    model="o3-mini",
    input="복잡한 수학 문제를 단계별로 풀어주세요",
    reasoning={
        "effort": "high",  # low, medium, high
        "max_reasoning_tokens": 50000
    },
    include=["reasoning.encrypted_content"]
)
```

### 2. 구조화된 출력
```python
response = client.responses.create(
    model="gpt-4o-mini",
    input="사용자 정보를 JSON 형식으로 정리해주세요",
    text={
        "format": {
            "type": "json_schema",
            "json_schema": {
                "name": "user_info",
                "schema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "age": {"type": "integer"},
                        "email": {"type": "string"}
                    }
                }
            }
        }
    }
)
```

### 3. 프롬프트 템플릿
```python
response = client.responses.create(
    model="gpt-4o-mini",
    prompt={
        "template_id": "template_123",
        "variables": {
            "user_name": "홍길동",
            "topic": "AI 기술"
        }
    }
)
```

## 오류 처리 및 모범 사례

### 에러 핸들링
```python
from openai import OpenAI
import openai

client = OpenAI()

try:
    response = client.responses.create(
        model="gpt-4o-mini",
        input="Hello world",
        max_output_tokens=1000
    )
    print(response.output_text)
    
except openai.RateLimitError as e:
    print(f"Rate limit 초과: {e}")
    # 재시도 로직 구현
    
except openai.APIError as e:
    print(f"API 오류: {e}")
    
except Exception as e:
    print(f"예상치 못한 오류: {e}")
```

### 비용 최적화 팁
```python
# 1. 적절한 모델 선택
response = client.responses.create(
    model="gpt-4o-mini",  # 비용 효율적
    input="Simple question",
    max_output_tokens=100  # 토큰 제한
)

# 2. 캐시 활용
response = client.responses.create(
    model="gpt-4o-mini",
    input="Repeated question",
    prompt_cache_key="cache_key_123"  # 캐시 키 사용
)

# 3. 백그라운드 처리로 병렬 작업
tasks = [] 
for query in queries:
    task = client.responses.create(
        model="gpt-4o-mini",
        input=query,
        background=True
    )
    tasks.append(task.id)
```

## 성능 최적화

### 배치 처리
```python
import asyncio
from openai import AsyncOpenAI

async_client = AsyncOpenAI()

async def process_multiple_requests():
    tasks = []
    
    for i in range(10):
        task = async_client.responses.create(
            model="gpt-4o-mini",
            input=f"Query {i}",
        )
        tasks.append(task)
    
    responses = await asyncio.gather(*tasks)
    return responses

# 실행
responses = asyncio.run(process_multiple_requests())
```

## Responses API vs Chat Completions 비교

### Responses API의 장점

| 기능 | Chat Completions | Responses API |
|------|------------------|---------------|
| **상태 관리** | 수동 컨텍스트 관리 | 자동 상태 관리 (`previous_response_id`) |
| **내장 도구** | 수동 구현 필요 | 내장 웹검색, 파일검색, 코드실행 등 |
| **추론 성능** | 기본 성능 | 3% 향상 (SWE-benchmark) |
| **비용 효율성** | 기본 비용 | 40-80% 비용 절감 (캐시 최적화) |
| **암호화 추론** | 지원 안함 | ZDR 조직을 위한 암호화 추론 지원 |
| **이벤트 기반** | 토큰별 스트리밍 | 의미론적 이벤트 기반 |
| **입력 형식** | `messages` 배열만 | 문자열 또는 배열 (`input`) |

### 기능별 비교표

| 기능 | Chat Completions | Responses API |
|------|------------------|---------------|
| 텍스트 생성 | ✅ | ✅ |
| 오디오 | ✅ | 🚧 곧 출시 |
| 비전 | ✅ | ✅ |
| 구조화된 출력 | ✅ | ✅ |
| 함수 호출 | ✅ | ✅ |
| 웹 검색 | ❌ | ✅ |
| 파일 검색 | ❌ | ✅ |
| 컴퓨터 사용 | ❌ | ✅ |
| 코드 인터프리터 | ❌ | ✅ |
| MCP | ❌ | ✅ |
| 이미지 생성 | ❌ | ✅ |
| 추론 요약 | ❌ | ✅ |

## 단계별 마이그레이션 가이드

### 1단계: 기본 텍스트 생성 마이그레이션

**Chat Completions (이전)**
```python
from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-5",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]
)
print(completion.choices[0].message.content)
```

**Responses API (이후)**
```python
from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-5",
    instructions="You are a helpful assistant.",
    input="Hello!"
)
print(response.output_text)
```

**또는 메시지 배열 형식**
```python
response = client.responses.create(
    model="gpt-5",
    input=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]
)
print(response.output_text)
```

### 2단계: 멀티턴 대화 마이그레이션

**Chat Completions (수동 컨텍스트 관리)**
```python
# 컨텍스트를 직접 관리해야 함
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"}
]

res1 = client.chat.completions.create(model="gpt-5", messages=messages)

# 수동으로 메시지 히스토리에 추가
messages.append({"role": "assistant", "content": res1.choices[0].message.content})
messages.append({"role": "user", "content": "And its population?"})

res2 = client.chat.completions.create(model="gpt-5", messages=messages)
```

**Responses API (자동 상태 관리)**
```python
# 첫 번째 요청
res1 = client.responses.create(
    model="gpt-5",
    input="What is the capital of France?",
    store=True  # 상태 저장 활성화
)

# 두 번째 요청 - previous_response_id로 컨텍스트 자동 연결
res2 = client.responses.create(
    model="gpt-5",
    input="And its population?",
    previous_response_id=res1.id,  # 이전 응답 참조
    store=True
)
```

**ZDR(Zero Data Retention) 조직용 암호화 추론**
```python
# 데이터 보관 제한이 있는 조직용
res1 = client.responses.create(
    model="gpt-5",
    input="What is the capital of France?",
    store=False,  # 저장 비활성화
    include=["reasoning.encrypted_content"]  # 암호화된 추론 포함
)

res2 = client.responses.create(
    model="gpt-5",
    input="And its population?",
    store=False,
    include=["reasoning.encrypted_content"],
    # 암호화된 추론 컨텍스트 전달 (구체적 구현은 문서 참조)
)
```

### 3단계: 도구 사용 마이그레이션

**Chat Completions (수동 도구 구현)**
```python
import requests

def web_search(query):
    # 자체 웹 검색 API 구현 필요
    r = requests.get(f"https://api.example.com/search?q={query}")
    return r.json().get("results", [])

completion = client.chat.completions.create(
    model="gpt-5",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who is the current president of France?"}
    ],
    functions=[
        {
            "name": "web_search",
            "description": "Search the web for information",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"]
            }
        }
    ]
)
```

**Responses API (내장 도구 활용)**
```python
# 내장 웹 검색 도구 사용 - 구현 불필요!
answer = client.responses.create(
    model="gpt-5",
    input="Who is the current president of France?",
    tools=[{"type": "web_search_preview"}],
    include=["web_search_call.action.sources"]  # 검색 소스 포함
)
print(answer.output_text)
```

### 4단계: 구조화된 출력 마이그레이션

**Chat Completions**
```python
completion = client.chat.completions.create(
    model="gpt-5",
    messages=[{"role": "user", "content": "Extract user info as JSON"}],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "user_info",
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "integer"}
                }
            }
        }
    }
)
```

**Responses API**
```python
response = client.responses.create(
    model="gpt-5",
    input="Extract user info as JSON",
    text={
        "format": {
            "type": "json_schema",
            "json_schema": {
                "name": "user_info",
                "schema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "age": {"type": "integer"}
                    }
                }
            }
        }
    }
)
```

### 5단계: 스트리밍 마이그레이션

**Chat Completions (토큰별 스트리밍)**
```python
stream = client.chat.completions.create(
    model="gpt-5",
    messages=[{"role": "user", "content": "Tell me a story"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

**Responses API (의미론적 이벤트 기반)**
```python
stream = client.responses.create(
    model="gpt-5",
    input="Tell me a story",
    stream=True
)

for event in stream:
    if event.output:
        for output in event.output:
            if hasattr(output, 'content') and output.content:
                print(output.content, end="", flush=True)
```

## 응답 구조 비교

### Chat Completions 응답
```json
{
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "안녕하세요! 무엇을 도와드릴까요?",
        "refusal": null
      },
      "logprobs": null,
      "finish_reason": "stop"
    }
  ]
}
```

### Responses API 응답
```json
{
  "id": "msg_67b73f697ba4819183a15cc17d011509",
  "output": [
    {
      "id": "msg_67b73f697ba4819183a15cc17d011509",
      "type": "message",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "안녕하세요! 무엇을 도와드릴까요?",
          "annotations": []
        }
      ]
    }
  ],
  "output_text": "안녕하세요! 무엇을 도와드릴까요?"
}
```

## 마이그레이션 체크리스트

### ✅ 기본 마이그레이션
- [ ] `messages` → `input` 변경
- [ ] `max_tokens` → `max_output_tokens` 변경
- [ ] `response.choices[0].message.content` → `response.output_text` 변경
- [ ] 에러 핸들링 업데이트

### ✅ 고급 기능 활용
- [ ] `previous_response_id`를 사용한 멀티턴 대화 구현
- [ ] 내장 도구(`web_search_preview`, `file_search` 등) 도입
- [ ] `instructions` 필드로 시스템 메시지 분리
- [ ] `include` 필드로 추가 메타데이터 요청

### ✅ 성능 최적화
- [ ] `store: true`로 상태 관리 활성화 (비용 절감)
- [ ] `prompt_cache_key`로 캐시 최적화
- [ ] 백그라운드 처리 (`background: true`) 도입

### ✅ 보안 및 컴플라이언스
- [ ] ZDR 조직: `store: false` + `reasoning.encrypted_content` 설정
- [ ] `safety_identifier`로 사용자 추적 구현
- [ ] `metadata`로 요청 태깅

## 점진적 마이그레이션 전략

Responses API는 Chat Completions의 상위집합이므로 점진적 마이그레이션이 가능합니다:

1. **1단계**: 새 기능부터 Responses API 사용
2. **2단계**: 추론 모델이 필요한 워크플로우 마이그레이션
3. **3단계**: 비용 절감이 중요한 고빈도 API 호출 마이그레이션
4. **4단계**: 전체 시스템 마이그레이션

## Assistants API에서의 마이그레이션

2025년 8월 26일부터 Assistants API가 deprecate되며, 2026년 8월 26일에 완전 종료됩니다. Responses API가 Assistants API의 개선된 버전입니다.

**주요 개선사항:**
- 더 빠른 응답 속도
- 더 유연한 API 구조  
- 더 나은 타입 안전성
- 통합된 도구 생태계

## 지원 모델 및 가격

### 지원 모델
- **gpt-4o**: 고성능 범용 모델
- **gpt-4o-mini**: 빠르고 비용 효율적  
- **o3**, **o3-mini**: 최신 추론 모델
- **computer-use-preview**: 컴퓨터 제어 기능

### 특수 기능별 모델 지원
| 기능 | 지원 모델 |
|------|----------|
| 웹 검색 | gpt-4o, gpt-4o-mini |
| 파일 검색 | 모든 모델 |
| 코드 실행 | gpt-4o, gpt-4o-mini |
| 추론 기능 | o3, o3-mini |
| 컴퓨터 제어 | computer-use-preview |

---

**참고 문헌:**
- [OpenAI Platform API Reference](https://platform.openai.com/docs/api-reference/responses)
- [OpenAI Cookbook - Responses API Examples](https://cookbook.openai.com/examples/responses_api/responses_example)
- [Azure OpenAI Responses API](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/responses)
- [OpenAI Responses API Guide - DataCamp](https://www.datacamp.com/tutorial/openai-responses-api)
- [Official OpenAI Python Library](https://github.com/openai/openai-python)
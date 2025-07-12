# LLM Server

**LLM Server**는 FastAPI와 OpenAI API를 활용하여 대화형 AI 챗봇 기능을 제공하는 서버 프로젝트입니다.  
한국어 환경에 최적화되어 있으며, 시스템 프롬프트, 대화 히스토리, 메모리 컨텍스트 등 다양한 입력을 조합해 유연한 챗봇 응답을 생성할 수 있습니다.

---

## 주요 특징

- **FastAPI 기반** RESTful API 서버
- **OpenAI API 연동** (GPT-4.1, GPT-4o 등 지원)
- **시스템 프롬프트, 대화 히스토리, 메모리** 등 다양한 컨텍스트 관리
- **한글 주석 및 에러 메시지**로 한국어 사용자 친화적
- **모듈화된 구조**: API, Core, DTO, Config, Utils 등
- **시스템 모니터링 API** 내장
- **테스트 코드 및 샘플 코드 제공**

---

## 폴더 구조

```
LLM Server/
  ├── app.py                  # FastAPI 진입점
  ├── docker-compose.yml      # Docker Compose 설정
  ├── Dockerfile              # Docker 빌드 파일
  ├── requirement.txt         # Python 패키지 목록
  ├── src/
  │   ├── api/                # API 라우터 및 문서
  │   ├── config/             # 환경설정 관리
  │   ├── core/               # 시스템 프롬프트 등 핵심 로직
  │   ├── dto/                # 요청/응답 데이터 모델
  │   ├── external/           # 외부 API 연동 (OpenAI 등)
  │   ├── services/           # 비즈니스 로직 처리 서비스
  │   └── utils/              # 로깅, 시스템 정보 등 유틸리티
  └── tests/                  # 테스트 코드
```

---

## 빠른 시작

### 1. 환경 변수 설정

`.env` 파일 또는 환경 변수에 **OpenAI API Key** 등 필수 정보를 입력하세요.

예시:
```
OPENAI_API_KEY=sk-xxxxxxx
SERVER_PORT=5601
SERVER_HOST=0.0.0.0
```

### 2. 패키지 설치

```bash
pip install -r requirement.txt
```

### 3. 서버 실행

```bash
python app.py
```

### 4. Docker로 실행

```bash
docker-compose up --build
```

---

## 주요 API

### 1. 채팅 API

- **POST /api/v1/chat**  
  OpenAI LLM과 대화(챗봇) 기능 제공

#### 요청 예시

```json
{
  "session_id": "session_123",
  "system_message": "친근하게 대화해주세요",
  "user_message": "파이썬에 대해 알려줘",
  "role": "당신은 친근하고 유머러스한 AI 어시스턴트입니다. 항상 긍정적이고 도움이 되는 답변을 제공합니다.",
  "conversation_history": [
    "user:안녕하세요",
    "assistant:안녕하세요! 무엇을 도와드릴까요?"
  ],
  "memory_context": ["사용자는 개발자입니다"],
  "max_tokens": 1000,
  "temperature": 0.7,
  "model": "gpt-4o-mini"
}
```

#### 응답 예시

```json
{
  "session_id": "session_123",
  "response_text": "파이썬은 범용 프로그래밍 언어입니다...",
  "model": "gpt-4o-mini",
  "input_tokens": 20,
  "output_tokens": 50,
  "total_tokens_used": 70,
  "output_format": "text",
  "created_at": "2024-01-01T00:00:00",
  "temperature": 0.7,
  "instructions": "",
  "response_time": 1.23,
  "success": true,
  "error_message": null
}
```

- **GET /**  
  서버 상태 확인용 엔드포인트

---

### 2. 시스템 모니터링 API

- **GET /api/v1/system/info** : 전체 시스템 정보
- **GET /api/v1/system/status** : 간단한 헬스체크
- **GET /api/v1/system/cpu** : CPU 정보
- **GET /api/v1/system/memory** : 메모리 정보
- **GET /api/v1/system/disk** : 디스크 정보

자세한 예시는 `src/api/SYSTEM_API_README.md` 참고

---

## 개발/구현 참고사항

- **컨텍스트 관리**: 시스템 프롬프트, 대화 히스토리, 메모리 컨텍스트를 조합하여 LLM에 전달
- **서비스 레이어**: 비즈니스 로직을 서비스 클래스에서 처리하여 관심사 분리
- **에러 처리**: 체계적인 예외 처리와 에러 핸들러로 안정성 확보
- **로깅**: 모든 주요 이벤트 및 에러는 한글로 기록
- **환경설정**: `src/config/config.py`에서 환경 변수 관리
- **테스트**: `tests/` 폴더에 단위/시나리오 테스트 코드 포함
- **토큰 최적화**: 테스트 시 토큰 사용량을 제한하여 비용 효율성 확보

---

## 예제 코드

### Python

```python
import requests

payload = {
    "session_id": "session_123",
    "user_message": "파이썬에 대해 알려줘"
}
response = requests.post("http://localhost:5601/api/v1/chat", json=payload)
print(response.json())
```

### Node.js

```javascript
const axios = require('axios');
axios.post('http://localhost:5601/api/v1/chat', {
  session_id: 'session_123',
  user_message: '파이썬에 대해 알려줘'
}).then(res => {
  console.log(res.data);
});
```


더 자세한 API 명세 및 예시는 `src/api/README.md`와 `src/api/SYSTEM_API_README.md`를 참고하세요. 
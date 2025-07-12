# LLM Server - 개요 및 시작 가이드

## 프로젝트 소개

LLM Server는 OpenAI API를 활용한 채팅 서비스를 제공하는 FastAPI 기반의 웹 서버입니다. 사용자 친화적인 API를 통해 AI와의 대화를 지원하며, 다양한 매개변수를 통해 대화를 커스터마이징할 수 있습니다.

## 주요 기능

### 🤖 AI 채팅
- OpenAI GPT 모델을 활용한 자연어 대화
- 다양한 모델 지원 (gpt-4o-mini, gpt-4o 등)
- 실시간 응답 생성

### 🎭 역할 기반 대화
- AI의 역할을 설정하여 특정 컨텍스트에서 대화
- 예: 프로그래밍 선생님, 친근한 어시스턴트 등

### 💾 메모리 컨텍스트
- 대화 중 중요한 정보를 메모리에 저장
- 이전 대화 내용을 참조하여 연속성 있는 대화 지원

### 📝 지시사항 시스템
- AI에게 특정 형식이나 스타일로 응답하도록 지시
- 예: "간단하게 설명해주세요", "한 문장으로 답해주세요"

### 🔑 API Key 관리
- 서버 관리 API Key와 사용자 제공 API Key 지원
- 유연한 API Key 선택 및 폴백 시스템

### 📊 시스템 모니터링
- CPU, 메모리, 디스크 사용량 모니터링
- 실시간 시스템 상태 확인

## 빠른 시작

### 1. 환경 설정

#### 필수 요구사항
- Python 3.8 이상
- OpenAI API Key

#### 설치
```bash
# 저장소 클론
git clone <repository-url>
cd LLM-Server

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirement.txt
```

#### 환경 변수 설정
```bash
# .env 파일 생성
cp env.example .env

# .env 파일 편집
OPENAI_API_KEY=your-openai-api-key-here
LOG_LEVEL=INFO
```

### 2. 서버 실행

#### 개발 모드
```bash
# FastAPI 개발 서버 실행
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

#### Docker를 사용한 실행
```bash
# Docker Compose로 실행
docker-compose up -d

# 로그 확인
docker-compose logs -f
```

### 3. API 테스트

#### 기본 채팅 요청
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "user_message": "안녕하세요!",
    "max_tokens": 500,
    "use_user_api_key": false
  }'
```

#### Python 클라이언트 예제
```python
import requests

url = "http://localhost:8000/api/v1/chat"
data = {
    "user_message": "파이썬이 뭐야?",
    "role": "당신은 친근한 프로그래밍 선생님입니다.",
    "instructions": "초보자에게 이해하기 쉽게 설명해주세요.",
    "max_tokens": 500,
    "use_user_api_key": false
}

response = requests.post(url, json=data)
result = response.json()

print(f"AI 응답: {result['response_text']}")
print(f"응답 시간: {result['response_time']:.2f}초")
print(f"API Key 소스: {result['api_key_source']}")
```

## API 사용법

### 기본 채팅

가장 간단한 채팅 요청입니다.

```json
{
  "user_message": "안녕하세요!",
  "use_user_api_key": false
}
```

### 역할 기반 채팅

AI에게 특정 역할을 부여하여 대화합니다.

```json
{
  "user_message": "프로그래밍을 가르쳐주세요",
  "role": "당신은 경험이 풍부한 프로그래밍 멘토입니다.",
  "instructions": "초보자에게 친근하고 격려하는 톤으로 답해주세요.",
  "use_user_api_key": false
}
```

### 메모리 컨텍스트 활용

이전 대화 내용을 기억하여 연속성 있는 대화를 지원합니다.

```json
{
  "user_message": "내가 좋아하는 색깔이 뭐였지?",
  "memory_context": [
    "사용자가 파란색을 좋아한다고 언급함",
    "사용자는 간단한 설명을 선호함"
  ],
  "use_user_api_key": false
}
```

### 사용자 API Key 사용

자신의 OpenAI API Key를 사용하여 요청합니다.

```json
{
  "user_message": "안녕하세요",
  "openai_api_key": "sk-your-api-key-here",
  "use_user_api_key": true
}
```

## API Key 관리

### 기본 모드 (기본값)
- 서버에서 관리하는 API Key 사용
- `use_user_api_key: false` 또는 생략
- 사용자가 API Key를 제공하지 않아도 동작

### 사용자 API Key 모드
- 사용자가 제공한 API Key 우선 사용
- `use_user_api_key: true`로 설정
- 유효하지 않은 경우 서버 관리 API Key로 폴백

## 시스템 모니터링

### 헬스체크
```bash
curl http://localhost:8000/api/v1/system/status
```

### 시스템 정보
```bash
curl http://localhost:8000/api/v1/system/info
```

### CPU 정보
```bash
curl http://localhost:8000/api/v1/system/cpu
```

### 메모리 정보
```bash
curl http://localhost:8000/api/v1/system/memory
```

### 디스크 정보
```bash
curl http://localhost:8000/api/v1/system/disk
```

## 테스트

### 전체 테스트 실행
```bash
python run_tests.py
```

### 개별 테스트 실행
```bash
# 단위 테스트
python -m pytest tests/test_unit.py -v

# 시나리오 테스트
python -m pytest tests/test_scenarios.py -v
```

## 배포

### Docker를 사용한 배포
```bash
# 이미지 빌드
docker build -t llm-server .

# 컨테이너 실행
docker run -d -p 8000:8000 --env-file .env llm-server
```

### Docker Compose를 사용한 배포
```bash
# 서비스 시작
docker-compose up -d

# 서비스 중지
docker-compose down
```

## 문제 해결

### 일반적인 문제

#### 1. OpenAI API Key 오류
```
Error: 유효한 OpenAI API Key가 설정되지 않았습니다.
```
**해결방법:**
- `.env` 파일에 올바른 API Key 설정
- 환경 변수 `OPENAI_API_KEY` 확인

#### 2. 포트 충돌
```
Error: Address already in use
```
**해결방법:**
- 다른 포트 사용: `uvicorn app:app --port 8001`
- 기존 프로세스 종료

#### 3. 의존성 오류
```
Error: ModuleNotFoundError
```
**해결방법:**
- 가상환경 활성화 확인
- `pip install -r requirement.txt` 재실행

### 로그 확인

#### 개발 모드
```bash
# 콘솔에서 직접 확인
uvicorn app:app --reload
```

#### Docker 모드
```bash
# 컨테이너 로그 확인
docker-compose logs -f

# 특정 컨테이너 로그
docker logs <container-name>
```

## 문서

- **[API 문서](./../api/README.md)**: 상세한 API 명세
- **[아키텍처 가이드](./../architecture/README.md)**: 프로젝트 구조 및 개발 가이드
- **[배포 가이드](./../deployment/README.md)**: 배포 및 운영 가이드
- **[테스트 가이드](./../testing/README.md)**: 테스트 및 품질 관리

## 기여하기

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

---
# LLM Server 개요 및 시작 가이드

## 📋 프로젝트 소개

**LLM Server**는 FastAPI와 OpenAI API를 활용하여 대화형 AI 챗봇 기능을 제공하는 서버 프로젝트입니다. 한국어 환경에 최적화되어 있으며, 시스템 프롬프트, 대화 히스토리, 메모리 컨텍스트 등 다양한 입력을 조합해 유연한 챗봇 응답을 생성할 수 있습니다.

### 🎯 주요 목표

- **대화형 AI 서비스**: OpenAI GPT 모델을 활용한 자연스러운 대화 기능
- **컨텍스트 관리**: 시스템 프롬프트, 대화 히스토리, 메모리 컨텍스트 통합
- **API Key 관리**: 사용자 제공 API Key 지원 및 Free 모드 기능
- **시스템 모니터링**: 실시간 시스템 상태 및 성능 모니터링
- **확장 가능한 아키텍처**: 모듈화된 구조로 유지보수성 향상

## ✨ 주요 특징

### 🤖 AI 챗봇 기능
- **OpenAI API 연동**: GPT-4o-mini, GPT-4 등 다양한 모델 지원
- **컨텍스트 관리**: 시스템 프롬프트, 대화 히스토리, 메모리 컨텍스트 조합
- **역할 기반 응답**: AI의 역할을 설정하여 일관된 응답 생성
- **토큰 최적화**: 효율적인 토큰 사용으로 비용 절약

### 🔑 API Key 관리
- **사용자 제공 API Key**: 개별 사용자가 자신의 API Key 사용 가능
- **Free 모드**: API Key 실패 시 기본 Key로 폴백
- **Key 검증**: API Key 유효성 실시간 검증
- **보안**: 응답에 실제 API Key 노출하지 않음

### 📊 시스템 모니터링
- **실시간 모니터링**: CPU, 메모리, 디스크, 네트워크 사용량
- **헬스체크**: 시스템 상태 확인 엔드포인트
- **프로세스 정보**: 서버 프로세스 상세 정보
- **Docker 지원**: 컨테이너 환경 정보 제공

### 🏗️ 기술 스택
- **FastAPI**: 고성능 Python 웹 프레임워크
- **OpenAI API**: 최신 LLM 모델 활용
- **Pydantic**: 데이터 검증 및 직렬화
- **Docker**: 컨테이너화 지원
- **한국어 지원**: 한국어 주석 및 에러 메시지

## 🚀 빠른 시작

### 1. 환경 설정

#### 필수 요구사항
- Python 3.11 이상
- OpenAI API Key
- Docker (선택사항)

#### 환경 변수 설정

`.env` 파일을 생성하고 다음 내용을 입력하세요:

```env
# 서버 설정
SERVER_HOST=0.0.0.0
SERVER_PORT=5601

# OpenAI API 설정
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini

# 로깅 설정
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

### 2. 패키지 설치

```bash
# 가상환경 생성 (권장)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate     # Windows

# 패키지 설치
pip install -r requirement.txt
```

### 3. 서버 실행

#### 로컬 실행
```bash
python app.py
```

#### Docker 실행
```bash
# 이미지 빌드 및 실행
docker-compose up --build

# 백그라운드 실행
docker-compose up -d
```

### 4. 서버 확인

브라우저에서 다음 URL을 확인하세요:
- **서버 상태**: http://localhost:5601/api/v1/
- **API 문서**: http://localhost:5601/docs (FastAPI 자동 생성)

## 📝 기본 사용법

### 1. 간단한 채팅 요청

```python
import requests

# 기본 채팅 요청
response = requests.post("http://localhost:5601/api/v1/chat", json={
    "session_id": "test_session",
    "user_message": "안녕하세요! 파이썬에 대해 알려주세요.",
    "free_mode": True
})

print(response.json())
```

### 2. Free 모드 사용

```python
# Free 모드로 사용자 API Key 사용
response = requests.post("http://localhost:5601/api/v1/chat", json={
    "session_id": "test_session",
    "user_message": "파이썬에 대해 알려주세요",
    "openai_api_key": "sk-your-api-key",
    "free_mode": True
})

result = response.json()
print(f"응답: {result['response_text']}")
print(f"API Key 소스: {result['api_key_source']}")
```

### 3. 시스템 모니터링

```python
# 시스템 정보 확인
response = requests.get("http://localhost:5601/api/v1/system/info")
system_info = response.json()

print(f"CPU 사용률: {system_info['cpu']['usage_percent']}%")
print(f"메모리 사용률: {system_info['memory']['usage_percent']}%")

# 헬스체크
response = requests.get("http://localhost:5601/api/v1/system/status")
status = response.json()
print(f"시스템 상태: {status['status']}")
```

## 🔧 개발 환경 설정

### 1. 개발 도구 설치

```bash
# 개발용 패키지 설치
pip install -r requirement.txt

# 테스트 실행
python run_tests.py
```

### 2. 코드 포맷팅

```bash
# Black을 사용한 코드 포맷팅
black src/ tests/

# isort를 사용한 import 정렬
isort src/ tests/
```

### 3. 린팅

```bash
# flake8을 사용한 코드 검사
flake8 src/ tests/
```

## 📁 프로젝트 구조

```
LLM Server/
├── app.py                  # FastAPI 진입점
├── docker-compose.yml      # Docker Compose 설정
├── Dockerfile              # Docker 빌드 파일
├── requirement.txt         # Python 패키지 목록
├── env.example            # 환경 변수 예시 파일
├── docs/                   # 📚 개발자 문서
├── src/
│   ├── api/               # 🌐 API 라우터 및 문서
│   │   ├── routes.py      # 채팅 API 라우터
│   │   ├── system_routes.py # 시스템 모니터링 API
│   │   └── exception_handlers.py # 예외 처리
│   ├── config/            # ⚙️ 환경설정 관리
│   │   └── config.py      # 설정 관리 클래스
│   ├── dto/               # 📦 요청/응답 데이터 모델
│   │   ├── request_dto.py # 요청 데이터 모델
│   │   └── response_dto.py # 응답 데이터 모델
│   ├── external/          # 🔗 외부 API 연동 (OpenAI 등)
│   │   └── openai_client.py # OpenAI API 클라이언트
│   ├── services/          # 🏢 비즈니스 로직 처리 서비스
│   │   └── chat_service.py # 채팅 서비스
│   ├── utils/             # 🛠️ 로깅, 시스템 정보 등 유틸리티
│   │   ├── logger.py      # 로깅 유틸리티
│   │   └── system_info.py # 시스템 정보 수집
│   └── exceptions/        # ⚠️ 커스텀 예외 처리
│       └── chat_exceptions.py # 채팅 관련 예외
└── tests/                 # 🧪 테스트 코드
    ├── test_unit.py       # 단위 테스트
    ├── test_scenarios.py  # 시나리오 테스트
    └── test_input.py      # 입력 검증 테스트
```

## 🎯 다음 단계

- **[API 문서](./../api/README.md)**: 상세한 API 명세 및 사용법
- **[배포 가이드](./../deployment/README.md)**: 배포 및 운영 가이드
- **[아키텍처 가이드](./../architecture/README.md)**: 프로젝트 구조 및 개발 가이드
- **[테스트 가이드](./../testing/README.md)**: 테스트 및 품질 관리

---

**문서 버전**: 1.0  
**최종 업데이트**: 2024년 12월  
**작성자**: LLM Server 개발팀 
# LLM Server

**LLM Server**는 FastAPI와 OpenAI API를 활용하여 대화형 AI 챗봇 기능을 제공하는 서버 프로젝트입니다.  
한국어 환경에 최적화되어 있으며, 시스템 프롬프트, 대화 히스토리, 메모리 컨텍스트 등 다양한 입력을 조합해 유연한 챗봇 응답을 생성할 수 있습니다.

## 🚀 빠른 시작

### 1. 환경 설정

```bash
# 저장소 클론
git clone https://github.com/your-repo/llm-server.git
cd llm-server

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate     # Windows

# 패키지 설치
pip install -r requirement.txt
```

### 2. 환경 변수 설정

`.env` 파일을 생성하고 다음 내용을 입력하세요:

```env
OPENAI_API_KEY=sk-your-openai-api-key-here
SERVER_HOST=0.0.0.0
SERVER_PORT=5601
LOG_LEVEL=INFO
```

### 3. 서버 실행

```bash
# 로컬 실행
python app.py

# 또는 Docker 실행
docker-compose up --build
```

### 4. 서버 확인

- **서버 상태**: http://localhost:5601/
- **API 문서**: http://localhost:5601/docs
- **시스템 정보**: http://localhost:5601/api/v1/system/status

## 📋 주요 기능

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

## 🔗 API 사용 예시

### 기본 채팅 요청

```python
import requests

response = requests.post("http://localhost:5601/api/v1/chat", json={
    "session_id": "test_session",
    "user_message": "안녕하세요! 파이썬에 대해 알려주세요.",
    "role": "당신은 친근하고 유머러스한 AI 어시스턴트입니다.",
    "max_tokens": 1000,
    "temperature": 0.7
})

result = response.json()
print(result['response_text'])
```

### Free 모드 사용

```python
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

## 📁 프로젝트 구조

```
LLM Server/
├── app.py                  # FastAPI 진입점
├── docker-compose.yml      # Docker Compose 설정
├── Dockerfile              # Docker 빌드 파일
├── requirement.txt         # Python 패키지 목록
├── docs/                   # 📚 개발자 문서
│   ├── overview/          # 개요 및 시작 가이드
│   ├── api/              # API 문서
│   ├── architecture/     # 아키텍처 및 개발 가이드
│   ├── deployment/       # 배포 및 운영 가이드
│   ├── testing/          # 테스트 및 품질 관리
│   └── ...               # 기타 문서
├── src/
│   ├── api/              # 🌐 API 라우터 및 문서
│   ├── config/           # ⚙️ 환경설정 관리
│   ├── dto/              # 📦 요청/응답 데이터 모델
│   ├── external/         # 🔗 외부 API 연동 (OpenAI 등)
│   ├── services/         # 🏢 비즈니스 로직 처리 서비스
│   ├── utils/            # 🛠️ 로깅, 시스템 정보 등 유틸리티
│   └── exceptions/       # ⚠️ 커스텀 예외 처리
└── tests/                # 🧪 테스트 코드
```

## 📚 문서

### 개발자 문서
- **[개요 및 시작 가이드](./docs/overview/README.md)** - 프로젝트 소개 및 기본 사용법
- **[API 문서](./docs/api/README.md)** - 상세한 API 명세 및 사용법
- **[아키텍처 가이드](./docs/architecture/README.md)** - 프로젝트 구조 및 개발 가이드
- **[배포 가이드](./docs/deployment/README.md)** - 운영 환경 배포 방법
- **[테스트 가이드](./docs/testing/README.md)** - 테스트 코드 작성 및 실행

### API 테스트 예시
- **[다양한 언어별 API 사용 예시](./docs/api/test-examples.md)** - Python, JavaScript, Java, C#, Go, PHP 등

## 🧪 테스트

```bash
# 모든 테스트 실행
python run_tests.py

# 특정 테스트 실행
pytest tests/test_unit.py

# 커버리지와 함께 실행
pytest --cov=src --cov-report=html
```

## 🐳 Docker 배포

```bash
# Docker 이미지 빌드 및 실행
docker-compose up --build

# 백그라운드 실행
docker-compose up -d

# 서비스 상태 확인
docker-compose ps

# 로그 확인
docker-compose logs -f
```

## 🤝 기여하기

프로젝트에 기여하고 싶으시다면:

1. 이슈를 생성하여 개선사항을 제안
2. Fork 후 Pull Request 생성
3. 테스트 코드 작성 및 실행
4. 코드 리뷰 참여

## 📞 지원

- **문서**: [docs/](./docs/) 폴더의 상세한 개발자 문서 참조
- **이슈**: GitHub Issues를 통해 버그 리포트 및 기능 요청
- **토론**: GitHub Discussions를 통한 질문 및 토론

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

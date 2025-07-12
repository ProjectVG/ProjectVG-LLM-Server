# 테스트 및 품질 관리 가이드

## 개요

LLM Server는 포괄적인 테스트 전략을 통해 코드 품질과 시스템 안정성을 보장합니다. 이 문서는 테스트 구조, 실행 방법, 그리고 품질 관리 프로세스에 대해 설명합니다.

## 테스트 구조

### 테스트 파일 구성

```
tests/
├── test_unit.py          # 단위 테스트
├── test_scenarios.py     # 시나리오 테스트
└── test_input.py         # 테스트 입력 데이터
```

### 테스트 유형

#### 1. 단위 테스트 (`test_unit.py`)
- 개별 컴포넌트의 기능 검증
- 격리된 환경에서 실행
- 빠른 피드백 제공

#### 2. 시나리오 테스트 (`test_scenarios.py`)
- 전체 시스템 흐름 검증
- 실제 사용 시나리오 기반
- 통합 테스트 역할

#### 3. 입력 데이터 (`test_input.py`)
- 테스트용 데이터 및 설정
- 토큰 제한 관리
- 재사용 가능한 테스트 데이터

## 테스트 실행

### 전체 테스트 실행
```bash
python run_tests.py
```

### 개별 테스트 실행
```bash
# 단위 테스트만 실행
python tests/test_unit.py

# 시나리오 테스트만 실행
python tests/test_scenarios.py
```

### 특정 테스트 실행
```bash
# 특정 테스트 메서드 실행
python -m unittest tests.test_unit.TestUnit.test_simple_chat_request
```

## 단위 테스트 상세

### ChatService 테스트

#### 기본 초기화 테스트
```python
def test_chat_service_initialization(self):
    """채팅 서비스 초기화 테스트"""
    self.assertIsNotNone(self.chat_service)
    self.assertIsNotNone(self.chat_service.openai_client)
```

#### 단순 채팅 요청 테스트
```python
def test_simple_chat_request(self):
    """단순 채팅 요청 테스트"""
    request = ChatRequest(
        user_message="안녕하세요",
        max_tokens=get_test_max_tokens(),
        use_user_api_key=False
    )
    
    response = self.chat_service.process_chat_request(request)
    
    self.assertIsNotNone(response)
    self.assertIsNotNone(response.response_text)
    self.assertGreater(len(response.response_text), 0)
```

#### 응답 시간 테스트
```python
def test_response_time(self):
    """응답 시간 테스트"""
    request = ChatRequest(
        user_message="안녕하세요",
        max_tokens=get_test_max_tokens(),
        use_user_api_key=False
    )
    
    response = self.chat_service.process_chat_request(request)
    
    self.assertIsNotNone(response.response_time)
    self.assertGreater(response.response_time, 0)
    self.assertLess(response.response_time, 30)
```

#### 메모리 매개변수 테스트
```python
def test_memory_parameter(self):
    """메모리 매개변수 테스트"""
    request = ChatRequest(
        user_message="메모리에 뭐가 있어?",
        memory_context=["테스트 메모리"],
        max_tokens=get_test_max_tokens(),
        use_user_api_key=False
    )
    
    response = self.chat_service.process_chat_request(request)
    
    self.assertIsNotNone(response)
    self.assertIsNotNone(response.response_text)
    self.assertGreater(len(response.response_text), 0)
```

#### 지시사항 매개변수 테스트
```python
def test_instructions_parameter(self):
    """지시사항 매개변수 테스트"""
    request = ChatRequest(
        user_message="파이썬이 뭐야?",
        instructions="한 문장으로 답해주세요.",
        max_tokens=get_test_max_tokens(),
        use_user_api_key=False
    )
    
    response = self.chat_service.process_chat_request(request)
    
    self.assertIsNotNone(response)
    self.assertIsNotNone(response.response_text)
    self.assertGreater(len(response.response_text), 0)
```

#### MAX_TOKEN 제한 테스트
```python
def test_max_token_limit(self):
    """MAX_TOKEN 제한 테스트"""
    request = ChatRequest(
        user_message="파이썬의 모든 특징과 장점을 자세히 설명해주세요.",
        max_tokens=16,  # OpenAI API 최소값
        use_user_api_key=False
    )
    
    response = self.chat_service.process_chat_request(request)
    response_length = len(response.response_text)
    
    self.assertLessEqual(response_length, 50)
```

#### API Key 기능 테스트
```python
def test_api_key_functionality(self):
    """API Key 기능 테스트"""
    request = ChatRequest(
        user_message="안녕하세요",
        max_tokens=get_test_max_tokens(),
        use_user_api_key=False
    )
    
    response = self.chat_service.process_chat_request(request)
    
    self.assertIsNotNone(response.api_key_source)
    self.assertIn(response.api_key_source, ["default", "user_provided"])
```

#### 사용자 API Key 기능 테스트
```python
def test_use_user_api_key_functionality(self):
    """사용자 API Key 기능 테스트"""
    request = ChatRequest(
        user_message="안녕하세요",
        max_tokens=get_test_max_tokens(),
        use_user_api_key=False
    )
    
    response = self.chat_service.process_chat_request(request)
    
    self.assertIsNotNone(response.api_key_source)
    self.assertTrue(response.success)
```

## 시나리오 테스트 상세

### 기본 대화 시나리오
```python
def test_basic_conversation_scenario(self):
    """기본 대화 시나리오 테스트"""
    request = ChatRequest(
        user_message="안녕하세요",
        max_tokens=get_test_max_tokens(),
        use_user_api_key=False
    )
    
    response = self.chat_service.process_chat_request(request)
    
    self.assertTrue(response.success)
    self.assertIsNotNone(response.response_text)
```

### 역할 기반 대화 시나리오
```python
def test_role_based_conversation_scenario(self):
    """역할 기반 대화 시나리오 테스트"""
    request = ChatRequest(
        user_message="파이썬을 가르쳐주세요",
        role="당신은 친근하고 이해하기 쉬운 프로그래밍 선생님입니다.",
        max_tokens=get_test_max_tokens(),
        use_user_api_key=False
    )
    
    response = self.chat_service.process_chat_request(request)
    
    self.assertTrue(response.success)
    self.assertIsNotNone(response.response_text)
```

### 메모리 컨텍스트 시나리오
```python
def test_memory_context_scenario(self):
    """메모리 컨텍스트 시나리오 테스트"""
    request = ChatRequest(
        user_message="내가 좋아하는 색깔이 뭐였지?",
        memory_context=["사용자가 파란색을 좋아한다고 언급함"],
        max_tokens=get_test_max_tokens(),
        use_user_api_key=False
    )
    
    response = self.chat_service.process_chat_request(request)
    
    self.assertTrue(response.success)
    self.assertIsNotNone(response.response_text)
```

### 지시사항 기반 시나리오
```python
def test_instruction_based_scenario(self):
    """지시사항 기반 시나리오 테스트"""
    request = ChatRequest(
        user_message="파이썬의 장점을 설명해주세요",
        instructions="간단하고 명확하게 3가지 장점만 설명해주세요.",
        max_tokens=get_test_max_tokens(),
        use_user_api_key=False
    )
    
    response = self.chat_service.process_chat_request(request)
    
    self.assertTrue(response.success)
    self.assertIsNotNone(response.response_text)
```

### 대화 히스토리 시나리오
```python
def test_conversation_history_scenario(self):
    """대화 히스토리 시나리오 테스트"""
    request = ChatRequest(
        user_message="그럼 자바는 어떤가요?",
        conversation_history=[
            "user: 파이썬에 대해 설명해주세요",
            "assistant: 파이썬은 간단하고 읽기 쉬운 프로그래밍 언어입니다."
        ],
        max_tokens=get_test_max_tokens(),
        use_user_api_key=False
    )
    
    response = self.chat_service.process_chat_request(request)
    
    self.assertTrue(response.success)
    self.assertIsNotNone(response.response_text)
```

### 복합 시나리오
```python
def test_complex_scenario(self):
    """복합 시나리오 테스트"""
    request = ChatRequest(
        user_message="프로그래밍을 배우고 싶어요",
        role="당신은 경험이 풍부한 프로그래밍 멘토입니다.",
        instructions="초보자에게 친근하고 격려하는 톤으로 답해주세요.",
        memory_context=["사용자가 프로그래밍에 관심을 보임"],
        conversation_history=[
            "user: 안녕하세요",
            "assistant: 안녕하세요! 무엇을 도와드릴까요?"
        ],
        max_tokens=get_test_max_tokens(),
        use_user_api_key=False
    )
    
    response = self.chat_service.process_chat_request(request)
    
    self.assertTrue(response.success)
    self.assertIsNotNone(response.response_text)
```

### 에러 처리 시나리오
```python
def test_error_handling_scenario(self):
    """에러 처리 시나리오 테스트"""
    # 빈 메시지 테스트
    request = ChatRequest(
        user_message="",
        max_tokens=get_test_max_tokens(),
        use_user_api_key=False
    )
    
    try:
        response = self.chat_service.process_chat_request(request)
        self.fail("빈 메시지에 대해 예외가 발생해야 합니다.")
    except ValidationException as e:
        self.assertEqual(e.field, "user_message")
    
    # 잘못된 max_tokens 테스트
    request = ChatRequest(
        user_message="테스트",
        max_tokens=-1,
        use_user_api_key=False
    )
    
    try:
        response = self.chat_service.process_chat_request(request)
        self.fail("잘못된 max_tokens에 대해 예외가 발생해야 합니다.")
    except ValidationException as e:
        self.assertEqual(e.field, "max_tokens")
```

### API Key 시나리오
```python
def test_api_key_and_use_user_api_key_scenarios(self):
    """API Key 및 사용자 API Key 시나리오 테스트"""
    # 기본 API Key 사용 테스트
    request = ChatRequest(
        user_message="안녕하세요",
        max_tokens=get_test_max_tokens(),
        use_user_api_key=False
    )
    
    response = self.chat_service.process_chat_request(request)
    self.assertTrue(response.success)
    
    # 사용자 API Key 사용 테스트 (유효하지 않은 키)
    request = ChatRequest(
        user_message="안녕하세요",
        openai_api_key="invalid-key",
        use_user_api_key=True,
        max_tokens=get_test_max_tokens()
    )
    
    response = self.chat_service.process_chat_request(request)
    self.assertTrue(response.success)
    
    # 일반 모드에서 유효하지 않은 키 사용 테스트
    request = ChatRequest(
        user_message="안녕하세요",
        openai_api_key="invalid-key",
        use_user_api_key=False,
        max_tokens=get_test_max_tokens()
    )
    
    try:
        response = self.chat_service.process_chat_request(request)
        self.fail("유효하지 않은 키에 대해 예외가 발생해야 합니다.")
    except OpenAIClientException as e:
        pass
```

## 테스트 데이터 관리

### 토큰 제한 관리
```python
def get_test_max_tokens() -> int:
    """테스트용 최대 토큰 수 반환"""
    return 100  # 테스트에서는 적은 토큰 사용
```

### 테스트 입력 데이터
```python
def get_test_inputs() -> list[str]:
    """테스트용 입력 데이터"""
    return [
        "안녕하세요",
        "파이썬이 뭐야?",
        "프로그래밍을 배우고 싶어요"
    ]

def get_test_memory() -> list[str]:
    """테스트용 메모리 데이터"""
    return [
        "사용자가 프로그래밍에 관심을 보임",
        "사용자는 초보자임"
    ]
```

## 품질 관리

### 코드 커버리지
```bash
# coverage 설치
pip install coverage

# 테스트 실행 및 커버리지 측정
coverage run --source=src run_tests.py
coverage report
coverage html
```

### 린팅
```bash
# flake8 설치
pip install flake8

# 코드 검사
flake8 src/ tests/
```

### 코드 포맷팅
```bash
# black 설치
pip install black

# 코드 포맷팅
black src/ tests/
```

## CI/CD 통합

### GitHub Actions 예제
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.11
    
    - name: Install dependencies
      run: |
        pip install -r requirement.txt
    
    - name: Run tests
      run: |
        python run_tests.py
```

## 테스트 모범 사례

### 1. 테스트 격리
- 각 테스트는 독립적으로 실행 가능해야 함
- 테스트 간 상태 공유 금지
- 외부 의존성 모킹

### 2. 명확한 테스트 이름
- 테스트 목적을 명확히 표현
- 한글로 테스트 설명 작성
- 동작 중심의 이름 사용

### 3. 적절한 검증
- 실제 동작 검증
- 예외 상황 테스트
- 경계값 테스트

### 4. 테스트 데이터 관리
- 재사용 가능한 테스트 데이터
- 환경별 설정 분리
- 민감한 정보 보호

## 문제 해결

### 일반적인 테스트 문제

#### 1. API Key 관련 오류
```
Error: 유효한 OpenAI API Key가 설정되지 않았습니다.
```
**해결방법:**
- 테스트 환경에서 API Key 설정 확인
- 모킹을 통한 외부 의존성 제거

#### 2. 타임아웃 오류
```
Error: 테스트 시간 초과
```
**해결방법:**
- 테스트용 토큰 제한 설정
- 비동기 테스트 활용

#### 3. 메모리 부족
```
Error: 메모리 부족
```
**해결방법:**
- 테스트 데이터 크기 조정
- 가비지 컬렉션 강제 실행


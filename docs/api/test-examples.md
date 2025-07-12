# API 테스트 예제

이 문서는 LLM Server API를 테스트하기 위한 다양한 예제를 제공합니다.

## 기본 테스트 환경 설정

### Python 환경 설정
```python
import requests
import json
import time

# 기본 설정
BASE_URL = "http://localhost:8000"
CHAT_ENDPOINT = f"{BASE_URL}/api/v1/chat"

# 헤더 설정
headers = {
    "Content-Type": "application/json"
}
```

### cURL 환경 설정
```bash
# 기본 URL 설정
BASE_URL="http://localhost:8000"
CHAT_ENDPOINT="$BASE_URL/api/v1/chat"

# 헤더 설정
HEADERS="-H 'Content-Type: application/json'"
```

## 기본 채팅 테스트

### Python 예제
```python
def basic_chat():
    """기본 채팅 테스트"""
    data = {
        "user_message": "안녕하세요!",
        "max_tokens": 500,
        "use_user_api_key": False
    }
    
    response = requests.post(CHAT_ENDPOINT, json=data, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ 성공: {result['response_text']}")
        print(f"⏱️ 응답 시간: {result['response_time']:.2f}초")
        print(f"🔑 API Key 소스: {result['api_key_source']}")
    else:
        print(f"❌ 실패: {response.status_code} - {response.text}")

# 테스트 실행
basic_chat()
```

### cURL 예제
```bash
curl -X POST "$CHAT_ENDPOINT" \
  $HEADERS \
  -d '{
    "user_message": "안녕하세요!",
    "max_tokens": 500,
    "use_user_api_key": false
  }'
```

## 역할 기반 채팅 테스트

### Python 예제
```python
def role_based_chat():
    """역할 기반 채팅 테스트"""
    data = {
        "user_message": "파이썬을 가르쳐주세요",
        "role": "당신은 친근하고 이해하기 쉬운 프로그래밍 선생님입니다.",
        "instructions": "초보자에게 적합한 설명을 해주세요.",
        "max_tokens": 500,
        "use_user_api_key": False
    }
    
    response = requests.post(CHAT_ENDPOINT, json=data, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ 성공: {result['response_text']}")
        print(f"🎭 역할: {data['role']}")
    else:
        print(f"❌ 실패: {response.status_code} - {response.text}")

# 테스트 실행
role_based_chat()
```

### cURL 예제
```bash
curl -X POST "$CHAT_ENDPOINT" \
  $HEADERS \
  -d '{
    "user_message": "파이썬을 가르쳐주세요",
    "role": "당신은 친근하고 이해하기 쉬운 프로그래밍 선생님입니다.",
    "instructions": "초보자에게 적합한 설명을 해주세요.",
    "max_tokens": 500,
    "use_user_api_key": false
  }'
```

## 메모리 컨텍스트 테스트

### Python 예제
```python
def memory_context_chat():
    """메모리 컨텍스트 테스트"""
    data = {
        "user_message": "내가 좋아하는 색깔이 뭐였지?",
        "memory_context": [
            "사용자가 파란색을 좋아한다고 언급함",
            "사용자는 간단한 설명을 선호함"
        ],
        "max_tokens": 500,
        "use_user_api_key": False
    }
    
    response = requests.post(CHAT_ENDPOINT, json=data, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ 성공: {result['response_text']}")
        print(f"💾 메모리: {data['memory_context']}")
    else:
        print(f"❌ 실패: {response.status_code} - {response.text}")

# 테스트 실행
memory_context_chat()
```

### cURL 예제
```bash
curl -X POST "$CHAT_ENDPOINT" \
  $HEADERS \
  -d '{
    "user_message": "내가 좋아하는 색깔이 뭐였지?",
    "memory_context": [
      "사용자가 파란색을 좋아한다고 언급함",
      "사용자는 간단한 설명을 선호함"
    ],
    "max_tokens": 500,
    "use_user_api_key": false
  }'
```

## 대화 히스토리 테스트

### Python 예제
```python
def conversation_history_chat():
    """대화 히스토리 테스트"""
    data = {
        "user_message": "그럼 자바는 어떤가요?",
        "conversation_history": [
            "user: 파이썬에 대해 설명해주세요",
            "assistant: 파이썬은 간단하고 읽기 쉬운 프로그래밍 언어입니다."
        ],
        "max_tokens": 500,
        "use_user_api_key": False
    }
    
    response = requests.post(CHAT_ENDPOINT, json=data, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ 성공: {result['response_text']}")
        print(f"📝 대화 히스토리: {data['conversation_history']}")
    else:
        print(f"❌ 실패: {response.status_code} - {response.text}")

# 테스트 실행
conversation_history_chat()
```

### cURL 예제
```bash
curl -X POST "$CHAT_ENDPOINT" \
  $HEADERS \
  -d '{
    "user_message": "그럼 자바는 어떤가요?",
    "conversation_history": [
      "user: 파이썬에 대해 설명해주세요",
      "assistant: 파이썬은 간단하고 읽기 쉬운 프로그래밍 언어입니다."
    ],
    "max_tokens": 500,
    "use_user_api_key": false
  }'
```

## 사용자 API Key 테스트

### Python 예제
```python
def user_api_key_chat():
    """사용자 API Key 테스트"""
    data = {
        "user_message": "안녕하세요",
        "openai_api_key": "sk-your-api-key-here",
        "use_user_api_key": True,
        "max_tokens": 500
    }
    
    response = requests.post(CHAT_ENDPOINT, json=data, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ 성공: {result['response_text']}")
        print(f"🔑 API Key 소스: {result['api_key_source']}")
    else:
        print(f"❌ 실패: {response.status_code} - {response.text}")

# 테스트 실행
user_api_key_chat()
```

### cURL 예제
```bash
curl -X POST "$CHAT_ENDPOINT" \
  $HEADERS \
  -d '{
    "user_message": "안녕하세요",
    "openai_api_key": "sk-your-api-key-here",
    "use_user_api_key": true,
    "max_tokens": 500
  }'
```

## 복합 시나리오 테스트

### Python 예제
```python
def complex_scenario_chat():
    """복합 시나리오 테스트"""
    data = {
        "user_message": "프로그래밍을 배우고 싶어요",
        "role": "당신은 경험이 풍부한 프로그래밍 멘토입니다.",
        "instructions": "초보자에게 친근하고 격려하는 톤으로 답해주세요.",
        "memory_context": [
            "사용자가 프로그래밍에 관심을 보임",
            "사용자는 학습에 열정적임"
        ],
        "conversation_history": [
            "user: 안녕하세요",
            "assistant: 안녕하세요! 무엇을 도와드릴까요?"
        ],
        "max_tokens": 500,
        "use_user_api_key": False
    }
    
    response = requests.post(CHAT_ENDPOINT, json=data, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ 성공: {result['response_text']}")
        print(f"🎭 역할: {data['role']}")
        print(f"💾 메모리: {data['memory_context']}")
        print(f"📝 대화 히스토리: {data['conversation_history']}")
    else:
        print(f"❌ 실패: {response.status_code} - {response.text}")

# 테스트 실행
complex_scenario_chat()
```

### cURL 예제
```bash
curl -X POST "$CHAT_ENDPOINT" \
  $HEADERS \
  -d '{
    "user_message": "프로그래밍을 배우고 싶어요",
    "role": "당신은 경험이 풍부한 프로그래밍 멘토입니다.",
    "instructions": "초보자에게 친근하고 격려하는 톤으로 답해주세요.",
    "memory_context": [
      "사용자가 프로그래밍에 관심을 보임",
      "사용자는 학습에 열정적임"
    ],
    "conversation_history": [
      "user: 안녕하세요",
      "assistant: 안녕하세요! 무엇을 도와드릴까요?"
    ],
    "max_tokens": 500,
    "use_user_api_key": false
  }'
```

## 에러 처리 테스트

### Python 예제
```python
def error_handling_tests():
    """에러 처리 테스트"""
    
    # 1. 빈 메시지 테스트
    print("=== 빈 메시지 테스트 ===")
    data = {
        "user_message": "",
        "max_tokens": 500,
        "use_user_api_key": False
    }
    
    response = requests.post(CHAT_ENDPOINT, json=data, headers=headers)
    print(f"상태 코드: {response.status_code}")
    if response.status_code != 200:
        print(f"예상된 에러: {response.json()}")
    
    # 2. 잘못된 max_tokens 테스트
    print("\n=== 잘못된 max_tokens 테스트 ===")
    data = {
        "user_message": "테스트",
        "max_tokens": -1,
        "use_user_api_key": False
    }
    
    response = requests.post(CHAT_ENDPOINT, json=data, headers=headers)
    print(f"상태 코드: {response.status_code}")
    if response.status_code != 200:
        print(f"예상된 에러: {response.json()}")
    
    # 3. 잘못된 temperature 테스트
    print("\n=== 잘못된 temperature 테스트 ===")
    data = {
        "user_message": "테스트",
        "temperature": 3.0,
        "use_user_api_key": False
    }
    
    response = requests.post(CHAT_ENDPOINT, json=data, headers=headers)
    print(f"상태 코드: {response.status_code}")
    if response.status_code != 200:
        print(f"예상된 에러: {response.json()}")

# 테스트 실행
error_handling_tests()
```

### cURL 예제
```bash
# 빈 메시지 테스트
echo "=== 빈 메시지 테스트 ==="
curl -X POST "$CHAT_ENDPOINT" \
  $HEADERS \
  -d '{
    "user_message": "",
    "max_tokens": 500,
    "use_user_api_key": false
  }'

# 잘못된 max_tokens 테스트
echo -e "\n=== 잘못된 max_tokens 테스트 ==="
curl -X POST "$CHAT_ENDPOINT" \
  $HEADERS \
  -d '{
    "user_message": "테스트",
    "max_tokens": -1,
    "use_user_api_key": false
  }'

# 잘못된 temperature 테스트
echo -e "\n=== 잘못된 temperature 테스트 ==="
curl -X POST "$CHAT_ENDPOINT" \
  $HEADERS \
  -d '{
    "user_message": "테스트",
    "temperature": 3.0,
    "use_user_api_key": false
  }'
```

## 성능 테스트

### Python 예제
```python
def performance_test():
    """성능 테스트"""
    test_cases = [
        {"user_message": "안녕하세요", "max_tokens": 100},
        {"user_message": "파이썬이 뭐야?", "max_tokens": 200},
        {"user_message": "프로그래밍을 배우고 싶어요", "max_tokens": 300},
        {"user_message": "자바스크립트에 대해 알려주세요", "max_tokens": 400},
        {"user_message": "데이터베이스란 무엇인가요?", "max_tokens": 500}
    ]
    
    total_time = 0
    success_count = 0
    
    print("=== 성능 테스트 시작 ===")
    
    for i, test_case in enumerate(test_cases, 1):
        test_case["use_user_api_key"] = False
        
        start_time = time.perf_counter()
        response = requests.post(CHAT_ENDPOINT, json=test_case, headers=headers)
        end_time = time.perf_counter()
        
        response_time = end_time - start_time
        total_time += response_time
        
        if response.status_code == 200:
            success_count += 1
            result = response.json()
            print(f"✅ 테스트 {i}: {response_time:.2f}초 - {result['response_text'][:50]}...")
        else:
            print(f"❌ 테스트 {i}: 실패 - {response.status_code}")
    
    print(f"\n=== 성능 테스트 결과 ===")
    print(f"총 테스트: {len(test_cases)}")
    print(f"성공: {success_count}")
    print(f"실패: {len(test_cases) - success_count}")
    print(f"평균 응답 시간: {total_time/len(test_cases):.2f}초")

# 테스트 실행
performance_test()
```

### cURL 예제
```bash
echo "=== 성능 테스트 시작 ==="

# 테스트 1
echo "테스트 1: 안녕하세요"
time curl -X POST "$CHAT_ENDPOINT" \
  $HEADERS \
  -d '{
    "user_message": "안녕하세요",
    "max_tokens": 100,
    "use_user_api_key": false
  }'

# 테스트 2
echo -e "\n테스트 2: 파이썬이 뭐야?"
time curl -X POST "$CHAT_ENDPOINT" \
  $HEADERS \
  -d '{
    "user_message": "파이썬이 뭐야?",
    "max_tokens": 200,
    "use_user_api_key": false
  }'

# 테스트 3
echo -e "\n테스트 3: 프로그래밍을 배우고 싶어요"
time curl -X POST "$CHAT_ENDPOINT" \
  $HEADERS \
  -d '{
    "user_message": "프로그래밍을 배우고 싶어요",
    "max_tokens": 300,
    "use_user_api_key": false
  }'
```

## 시스템 모니터링 테스트

### Python 예제
```python
def system_monitoring_tests():
    """시스템 모니터링 테스트"""
    
    # 헬스체크
    print("=== 헬스체크 ===")
    response = requests.get(f"{BASE_URL}/api/v1/system/status")
    if response.status_code == 200:
        result = response.json()
        print(f"상태: {result['status']}")
        print(f"업타임: {result['uptime']}초")
    
    # 시스템 정보
    print("\n=== 시스템 정보 ===")
    response = requests.get(f"{BASE_URL}/api/v1/system/info")
    if response.status_code == 200:
        result = response.json()
        print(f"플랫폼: {result['system']['platform']}")
        print(f"Python 버전: {result['system']['python_version']}")
        print(f"CPU 사용률: {result['cpu']['usage_percent']}%")
        print(f"메모리 사용률: {result['memory']['usage_percent']}%")
    
    # CPU 정보
    print("\n=== CPU 정보 ===")
    response = requests.get(f"{BASE_URL}/api/v1/system/cpu")
    if response.status_code == 200:
        result = response.json()
        print(f"CPU 사용률: {result['cpu']['usage_percent']}%")
        print(f"CPU 코어 수: {result['cpu']['count']}")
    
    # 메모리 정보
    print("\n=== 메모리 정보 ===")
    response = requests.get(f"{BASE_URL}/api/v1/system/memory")
    if response.status_code == 200:
        result = response.json()
        print(f"총 메모리: {result['memory']['total'] / (1024**3):.2f} GB")
        print(f"사용 중: {result['memory']['used'] / (1024**3):.2f} GB")
        print(f"사용률: {result['memory']['usage_percent']}%")

# 테스트 실행
system_monitoring_tests()
```

### cURL 예제
```bash
echo "=== 헬스체크 ==="
curl "$BASE_URL/api/v1/system/status"

echo -e "\n=== 시스템 정보 ==="
curl "$BASE_URL/api/v1/system/info"

echo -e "\n=== CPU 정보 ==="
curl "$BASE_URL/api/v1/system/cpu"

echo -e "\n=== 메모리 정보 ==="
curl "$BASE_URL/api/v1/system/memory"

echo -e "\n=== 디스크 정보 ==="
curl "$BASE_URL/api/v1/system/disk"
```

## 전체 테스트 스크립트

### Python 전체 테스트
```python
def run_all_tests():
    """전체 테스트 실행"""
    print("🚀 LLM Server API 테스트 시작")
    print("=" * 50)
    
    # 기본 테스트
    print("\n1. 기본 채팅 테스트")
    basic_chat()
    
    # 역할 기반 테스트
    print("\n2. 역할 기반 채팅 테스트")
    role_based_chat()
    
    # 메모리 컨텍스트 테스트
    print("\n3. 메모리 컨텍스트 테스트")
    memory_context_chat()
    
    # 대화 히스토리 테스트
    print("\n4. 대화 히스토리 테스트")
    conversation_history_chat()
    
    # 사용자 API Key 테스트
    print("\n5. 사용자 API Key 테스트")
    user_api_key_chat()
    
    # 복합 시나리오 테스트
    print("\n6. 복합 시나리오 테스트")
    complex_scenario_chat()
    
    # 에러 처리 테스트
    print("\n7. 에러 처리 테스트")
    error_handling_tests()
    
    # 성능 테스트
    print("\n8. 성능 테스트")
    performance_test()
    
    # 시스템 모니터링 테스트
    print("\n9. 시스템 모니터링 테스트")
    system_monitoring_tests()
    
    print("\n✅ 모든 테스트 완료!")

# 전체 테스트 실행
if __name__ == "__main__":
    run_all_tests()
```

### Bash 전체 테스트
```bash
#!/bin/bash

echo "🚀 LLM Server API 테스트 시작"
echo "=================================================="

# 기본 테스트
echo -e "\n1. 기본 채팅 테스트"
curl -X POST "$CHAT_ENDPOINT" \
  $HEADERS \
  -d '{
    "user_message": "안녕하세요!",
    "max_tokens": 500,
    "use_user_api_key": false
  }'

# 역할 기반 테스트
echo -e "\n2. 역할 기반 채팅 테스트"
curl -X POST "$CHAT_ENDPOINT" \
  $HEADERS \
  -d '{
    "user_message": "파이썬을 가르쳐주세요",
    "role": "당신은 친근하고 이해하기 쉬운 프로그래밍 선생님입니다.",
    "instructions": "초보자에게 적합한 설명을 해주세요.",
    "max_tokens": 500,
    "use_user_api_key": false
  }'

# 메모리 컨텍스트 테스트
echo -e "\n3. 메모리 컨텍스트 테스트"
curl -X POST "$CHAT_ENDPOINT" \
  $HEADERS \
  -d '{
    "user_message": "내가 좋아하는 색깔이 뭐였지?",
    "memory_context": [
      "사용자가 파란색을 좋아한다고 언급함",
      "사용자는 간단한 설명을 선호함"
    ],
    "max_tokens": 500,
    "use_user_api_key": false
  }'

# 시스템 모니터링 테스트
echo -e "\n4. 시스템 모니터링 테스트"
curl "$BASE_URL/api/v1/system/status"

echo -e "\n✅ 모든 테스트 완료!"
```

## 문제 해결

### 일반적인 문제

#### 1. 연결 오류
```
ConnectionError: HTTPConnectionPool
```
**해결방법:**
- 서버가 실행 중인지 확인
- 포트 번호 확인 (기본: 8000)
- 방화벽 설정 확인

#### 2. 인증 오류
```
401 Unauthorized
```
**해결방법:**
- API Key 설정 확인
- `use_user_api_key` 값 확인

#### 3. 타임아웃 오류
```
TimeoutError: Request timed out
```
**해결방법:**
- `max_tokens` 값 줄이기
- 네트워크 연결 확인
- 서버 성능 확인

#### 4. 메모리 부족
```
MemoryError
```
**해결방법:**
- 요청 데이터 크기 줄이기
- `conversation_history` 길이 제한
- 서버 리소스 확인

---
# API 테스트 예시

이 문서는 다양한 프로그래밍 언어를 사용한 LLM Server API 테스트 예시를 제공합니다.

## 📋 목차

- [Python](#python)
- [JavaScript (Node.js)](#javascript-nodejs)
- [cURL](#curl)
- [Java](#java)
- [C#](#c)
- [Go](#go)
- [PHP](#php)

---

## 🐍 Python

### 기본 설치

```bash
pip install requests
```

### 1. 기본 채팅 요청

```python
import requests
import json

def basic_chat():
    url = "http://localhost:5601/api/v1/chat"
    
    payload = {
        "session_id": "test_session_001",
        "user_message": "안녕하세요! 파이썬에 대해 알려주세요.",
        "role": "당신은 친근하고 유머러스한 AI 어시스턴트입니다.",
        "max_tokens": 1000,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        result = response.json()
        print(f"응답: {result['response_text']}")
        print(f"토큰 사용량: {result['total_tokens_used']}")
        print(f"응답 시간: {result['response_time']:.2f}초")
        
    except requests.exceptions.RequestException as e:
        print(f"API 호출 오류: {e}")

if __name__ == "__main__":
    basic_chat()
```

### 2. Free 모드 사용

```python
def free_mode_chat():
    url = "http://localhost:5601/api/v1/chat"
    
    payload = {
        "session_id": "test_session_002",
        "user_message": "머신러닝에 대해 설명해주세요",
        "openai_api_key": "sk-your-api-key-here",  # 선택사항
        "free_mode": True,
        "conversation_history": [
            "user:안녕하세요",
            "assistant:안녕하세요! 무엇을 도와드릴까요?",
            "user:AI에 대해 궁금해요"
        ],
        "memory_context": ["사용자는 AI에 관심이 많은 개발자입니다"],
        "max_tokens": 800,
        "temperature": 0.8
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        result = response.json()
        print(f"응답: {result['response_text']}")
        print(f"API Key 소스: {result['api_key_source']}")
        print(f"성공 여부: {result['success']}")
        
    except requests.exceptions.RequestException as e:
        print(f"API 호출 오류: {e}")

free_mode_chat()
```

### 3. 시스템 모니터링

```python
def system_monitoring():
    base_url = "http://localhost:5601/api/v1/system"
    
    # 전체 시스템 정보
    try:
        response = requests.get(f"{base_url}/info")
        response.raise_for_status()
        system_info = response.json()
        
        print("=== 시스템 정보 ===")
        print(f"플랫폼: {system_info['system']['platform']}")
        print(f"CPU 사용률: {system_info['cpu']['usage_percent']}%")
        print(f"메모리 사용률: {system_info['memory']['usage_percent']}%")
        print(f"디스크 사용률: {system_info['disk']['usage_percent']}%")
        
    except requests.exceptions.RequestException as e:
        print(f"시스템 정보 조회 오류: {e}")
    
    # 헬스체크
    try:
        response = requests.get(f"{base_url}/status")
        response.raise_for_status()
        status = response.json()
        
        print(f"\n=== 헬스체크 ===")
        print(f"상태: {status['status']}")
        print(f"CPU 사용률: {status['cpu_usage']}%")
        print(f"메모리 사용률: {status['memory_usage']}%")
        
    except requests.exceptions.RequestException as e:
        print(f"헬스체크 오류: {e}")

system_monitoring()
```

### 4. 에러 처리 예시

```python
def error_handling_example():
    url = "http://localhost:5601/api/v1/chat"
    
    # 잘못된 요청 예시
    invalid_payload = {
        "user_message": "",  # 빈 메시지 (오류 발생)
        "max_tokens": -1,    # 잘못된 토큰 수 (오류 발생)
        "temperature": 3.0   # 잘못된 temperature (오류 발생)
    }
    
    try:
        response = requests.post(url, json=invalid_payload)
        
        if response.status_code == 400:
            error_data = response.json()
            print(f"검증 오류: {error_data['error_message']}")
        elif response.status_code == 422:
            print("요청 데이터 형식 오류")
        else:
            print(f"예상치 못한 오류: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"네트워크 오류: {e}")

error_handling_example()
```

---

## 🟨 JavaScript (Node.js)

### 기본 설치

```bash
npm install axios
```

### 1. 기본 채팅 요청

```javascript
const axios = require('axios');

async function basicChat() {
    const url = 'http://localhost:5601/api/v1/chat';
    
    const payload = {
        session_id: 'test_session_001',
        user_message: '안녕하세요! 자바스크립트에 대해 알려주세요.',
        role: '당신은 친근하고 유머러스한 AI 어시스턴트입니다.',
        max_tokens: 1000,
        temperature: 0.7
    };
    
    try {
        const response = await axios.post(url, payload);
        const result = response.data;
        
        console.log(`응답: ${result.response_text}`);
        console.log(`토큰 사용량: ${result.total_tokens_used}`);
        console.log(`응답 시간: ${result.response_time.toFixed(2)}초`);
        
    } catch (error) {
        if (error.response) {
            console.error('API 오류:', error.response.data);
        } else {
            console.error('네트워크 오류:', error.message);
        }
    }
}

basicChat();
```

### 2. Free 모드 사용

```javascript
async function freeModeChat() {
    const url = 'http://localhost:5601/api/v1/chat';
    
    const payload = {
        session_id: 'test_session_002',
        user_message: '웹 개발에 대해 설명해주세요',
        openai_api_key: 'sk-your-api-key-here', // 선택사항
        free_mode: true,
        conversation_history: [
            'user:안녕하세요',
            'assistant:안녕하세요! 무엇을 도와드릴까요?',
            'user:웹 개발에 관심이 있어요'
        ],
        memory_context: ['사용자는 웹 개발을 배우고 싶어하는 초보자입니다'],
        max_tokens: 800,
        temperature: 0.8
    };
    
    try {
        const response = await axios.post(url, payload);
        const result = response.data;
        
        console.log(`응답: ${result.response_text}`);
        console.log(`API Key 소스: ${result.api_key_source}`);
        console.log(`성공 여부: ${result.success}`);
        
    } catch (error) {
        console.error('오류:', error.response?.data || error.message);
    }
}

freeModeChat();
```

### 3. 시스템 모니터링

```javascript
async function systemMonitoring() {
    const baseUrl = 'http://localhost:5601/api/v1/system';
    
    try {
        // 전체 시스템 정보
        const systemResponse = await axios.get(`${baseUrl}/info`);
        const systemInfo = systemResponse.data;
        
        console.log('=== 시스템 정보 ===');
        console.log(`플랫폼: ${systemInfo.system.platform}`);
        console.log(`CPU 사용률: ${systemInfo.cpu.usage_percent}%`);
        console.log(`메모리 사용률: ${systemInfo.memory.usage_percent}%`);
        console.log(`디스크 사용률: ${systemInfo.disk.usage_percent}%`);
        
        // 헬스체크
        const statusResponse = await axios.get(`${baseUrl}/status`);
        const status = statusResponse.data;
        
        console.log('\n=== 헬스체크 ===');
        console.log(`상태: ${status.status}`);
        console.log(`CPU 사용률: ${status.cpu_usage}%`);
        console.log(`메모리 사용률: ${status.memory_usage}%`);
        
    } catch (error) {
        console.error('시스템 모니터링 오류:', error.response?.data || error.message);
    }
}

systemMonitoring();
```

---

## 🔗 cURL

### 1. 기본 채팅 요청

```bash
curl -X POST "http://localhost:5601/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test_session_001",
    "user_message": "안녕하세요! 리눅스에 대해 알려주세요.",
    "role": "당신은 친근하고 유머러스한 AI 어시스턴트입니다.",
    "max_tokens": 1000,
    "temperature": 0.7
  }'
```

### 2. Free 모드 사용

```bash
curl -X POST "http://localhost:5601/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test_session_002",
    "user_message": "데이터베이스에 대해 설명해주세요",
    "openai_api_key": "sk-your-api-key-here",
    "free_mode": true,
    "conversation_history": [
      "user:안녕하세요",
      "assistant:안녕하세요! 무엇을 도와드릴까요?",
      "user:데이터베이스에 관심이 있어요"
    ],
    "memory_context": ["사용자는 데이터베이스를 배우고 싶어하는 개발자입니다"],
    "max_tokens": 800,
    "temperature": 0.8
  }'
```

### 3. 시스템 모니터링

```bash
# 전체 시스템 정보
curl "http://localhost:5601/api/v1/system/info"

# 헬스체크
curl "http://localhost:5601/api/v1/system/status"

# CPU 정보만
curl "http://localhost:5601/api/v1/system/cpu"

# 메모리 정보만
curl "http://localhost:5601/api/v1/system/memory"

# 디스크 정보만
curl "http://localhost:5601/api/v1/system/disk"
```

### 4. 에러 테스트

```bash
# 잘못된 요청 (빈 메시지)
curl -X POST "http://localhost:5601/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "user_message": "",
    "max_tokens": -1,
    "temperature": 3.0
  }'
```

---

## ☕ Java

### Maven 의존성

```xml
<dependency>
    <groupId>com.squareup.okhttp3</groupId>
    <artifactId>okhttp</artifactId>
    <version>4.9.3</version>
</dependency>
<dependency>
    <groupId>com.google.code.gson</groupId>
    <artifactId>gson</artifactId>
    <version>2.8.9</version>
</dependency>
```

### 1. 기본 채팅 요청

```java
import com.google.gson.Gson;
import okhttp3.*;
import java.io.IOException;

public class LLMServerClient {
    private static final String BASE_URL = "http://localhost:5601";
    private static final OkHttpClient client = new OkHttpClient();
    private static final Gson gson = new Gson();
    
    public static void basicChat() {
        String url = BASE_URL + "/api/v1/chat";
        
        // 요청 데이터
        ChatRequest request = new ChatRequest();
        request.setSessionId("test_session_001");
        request.setUserMessage("안녕하세요! 자바에 대해 알려주세요.");
        request.setRole("당신은 친근하고 유머러스한 AI 어시스턴트입니다.");
        request.setMaxTokens(1000);
        request.setTemperature(0.7);
        
        String jsonBody = gson.toJson(request);
        
        Request httpRequest = new Request.Builder()
            .url(url)
            .post(RequestBody.create(jsonBody, MediaType.get("application/json")))
            .build();
        
        try (Response response = client.newCall(httpRequest).execute()) {
            if (response.isSuccessful()) {
                String responseBody = response.body().string();
                ChatResponse result = gson.fromJson(responseBody, ChatResponse.class);
                
                System.out.println("응답: " + result.getResponseText());
                System.out.println("토큰 사용량: " + result.getTotalTokensUsed());
                System.out.println("응답 시간: " + result.getResponseTime() + "초");
            } else {
                System.out.println("API 오류: " + response.code());
            }
        } catch (IOException e) {
            System.err.println("네트워크 오류: " + e.getMessage());
        }
    }
    
    // 요청 클래스
    public static class ChatRequest {
        private String sessionId;
        private String userMessage;
        private String role;
        private int maxTokens;
        private double temperature;
        
        // Getters and Setters
        public String getSessionId() { return sessionId; }
        public void setSessionId(String sessionId) { this.sessionId = sessionId; }
        
        public String getUserMessage() { return userMessage; }
        public void setUserMessage(String userMessage) { this.userMessage = userMessage; }
        
        public String getRole() { return role; }
        public void setRole(String role) { this.role = role; }
        
        public int getMaxTokens() { return maxTokens; }
        public void setMaxTokens(int maxTokens) { this.maxTokens = maxTokens; }
        
        public double getTemperature() { return temperature; }
        public void setTemperature(double temperature) { this.temperature = temperature; }
    }
    
    // 응답 클래스
    public static class ChatResponse {
        private String responseText;
        private int totalTokensUsed;
        private double responseTime;
        private boolean success;
        private String errorMessage;
        
        // Getters and Setters
        public String getResponseText() { return responseText; }
        public void setResponseText(String responseText) { this.responseText = responseText; }
        
        public int getTotalTokensUsed() { return totalTokensUsed; }
        public void setTotalTokensUsed(int totalTokensUsed) { this.totalTokensUsed = totalTokensUsed; }
        
        public double getResponseTime() { return responseTime; }
        public void setResponseTime(double responseTime) { this.responseTime = responseTime; }
        
        public boolean isSuccess() { return success; }
        public void setSuccess(boolean success) { this.success = success; }
        
        public String getErrorMessage() { return errorMessage; }
        public void setErrorMessage(String errorMessage) { this.errorMessage = errorMessage; }
    }
    
    public static void main(String[] args) {
        basicChat();
    }
}
```

---

## 🔷 C#

### NuGet 패키지

```bash
dotnet add package Newtonsoft.Json
dotnet add package System.Net.Http
```

### 1. 기본 채팅 요청

```csharp
using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;

public class LLMServerClient
{
    private static readonly HttpClient client = new HttpClient();
    private static readonly string BaseUrl = "http://localhost:5601";
    
    public static async Task BasicChatAsync()
    {
        var url = $"{BaseUrl}/api/v1/chat";
        
        var request = new ChatRequest
        {
            SessionId = "test_session_001",
            UserMessage = "안녕하세요! C#에 대해 알려주세요.",
            Role = "당신은 친근하고 유머러스한 AI 어시스턴트입니다.",
            MaxTokens = 1000,
            Temperature = 0.7
        };
        
        var json = JsonConvert.SerializeObject(request);
        var content = new StringContent(json, Encoding.UTF8, "application/json");
        
        try
        {
            var response = await client.PostAsync(url, content);
            var responseBody = await response.Content.ReadAsStringAsync();
            
            if (response.IsSuccessStatusCode)
            {
                var result = JsonConvert.DeserializeObject<ChatResponse>(responseBody);
                Console.WriteLine($"응답: {result.ResponseText}");
                Console.WriteLine($"토큰 사용량: {result.TotalTokensUsed}");
                Console.WriteLine($"응답 시간: {result.ResponseTime:F2}초");
            }
            else
            {
                Console.WriteLine($"API 오류: {response.StatusCode}");
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"네트워크 오류: {ex.Message}");
        }
    }
    
    public class ChatRequest
    {
        [JsonProperty("session_id")]
        public string SessionId { get; set; }
        
        [JsonProperty("user_message")]
        public string UserMessage { get; set; }
        
        [JsonProperty("role")]
        public string Role { get; set; }
        
        [JsonProperty("max_tokens")]
        public int MaxTokens { get; set; }
        
        [JsonProperty("temperature")]
        public double Temperature { get; set; }
    }
    
    public class ChatResponse
    {
        [JsonProperty("response_text")]
        public string ResponseText { get; set; }
        
        [JsonProperty("total_tokens_used")]
        public int TotalTokensUsed { get; set; }
        
        [JsonProperty("response_time")]
        public double ResponseTime { get; set; }
        
        [JsonProperty("success")]
        public bool Success { get; set; }
        
        [JsonProperty("error_message")]
        public string ErrorMessage { get; set; }
    }
    
    public static async Task Main(string[] args)
    {
        await BasicChatAsync();
    }
}
```

---

## 🐹 Go

### 1. 기본 채팅 요청

```go
package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "io/ioutil"
    "net/http"
)

type ChatRequest struct {
    SessionID string   `json:"session_id"`
    UserMessage string `json:"user_message"`
    Role string        `json:"role"`
    MaxTokens int      `json:"max_tokens"`
    Temperature float64 `json:"temperature"`
}

type ChatResponse struct {
    ResponseText string  `json:"response_text"`
    TotalTokensUsed int  `json:"total_tokens_used"`
    ResponseTime float64 `json:"response_time"`
    Success bool         `json:"success"`
    ErrorMessage string  `json:"error_message"`
}

func basicChat() {
    url := "http://localhost:5601/api/v1/chat"
    
    request := ChatRequest{
        SessionID: "test_session_001",
        UserMessage: "안녕하세요! Go 언어에 대해 알려주세요.",
        Role: "당신은 친근하고 유머러스한 AI 어시스턴트입니다.",
        MaxTokens: 1000,
        Temperature: 0.7,
    }
    
    jsonData, err := json.Marshal(request)
    if err != nil {
        fmt.Printf("JSON 마샬링 오류: %v\n", err)
        return
    }
    
    resp, err := http.Post(url, "application/json", bytes.NewBuffer(jsonData))
    if err != nil {
        fmt.Printf("HTTP 요청 오류: %v\n", err)
        return
    }
    defer resp.Body.Close()
    
    body, err := ioutil.ReadAll(resp.Body)
    if err != nil {
        fmt.Printf("응답 읽기 오류: %v\n", err)
        return
    }
    
    if resp.StatusCode == http.StatusOK {
        var result ChatResponse
        err = json.Unmarshal(body, &result)
        if err != nil {
            fmt.Printf("JSON 언마샬링 오류: %v\n", err)
            return
        }
        
        fmt.Printf("응답: %s\n", result.ResponseText)
        fmt.Printf("토큰 사용량: %d\n", result.TotalTokensUsed)
        fmt.Printf("응답 시간: %.2f초\n", result.ResponseTime)
    } else {
        fmt.Printf("API 오류: %s\n", resp.Status)
    }
}

func main() {
    basicChat()
}
```

---

## 🐘 PHP

### 1. 기본 채팅 요청

```php
<?php

function basicChat() {
    $url = 'http://localhost:5601/api/v1/chat';
    
    $data = [
        'session_id' => 'test_session_001',
        'user_message' => '안녕하세요! PHP에 대해 알려주세요.',
        'role' => '당신은 친근하고 유머러스한 AI 어시스턴트입니다.',
        'max_tokens' => 1000,
        'temperature' => 0.7
    ];
    
    $options = [
        'http' => [
            'header' => "Content-type: application/json\r\n",
            'method' => 'POST',
            'content' => json_encode($data)
        ]
    ];
    
    $context = stream_context_create($options);
    $result = file_get_contents($url, false, $context);
    
    if ($result === FALSE) {
        echo "API 호출 오류\n";
        return;
    }
    
    $response = json_decode($result, true);
    
    if ($response['success']) {
        echo "응답: " . $response['response_text'] . "\n";
        echo "토큰 사용량: " . $response['total_tokens_used'] . "\n";
        echo "응답 시간: " . number_format($response['response_time'], 2) . "초\n";
    } else {
        echo "오류: " . $response['error_message'] . "\n";
    }
}

// cURL을 사용한 더 안정적인 방법
function basicChatWithCurl() {
    $url = 'http://localhost:5601/api/v1/chat';
    
    $data = [
        'session_id' => 'test_session_001',
        'user_message' => '안녕하세요! PHP에 대해 알려주세요.',
        'role' => '당신은 친근하고 유머러스한 AI 어시스턴트입니다.',
        'max_tokens' => 1000,
        'temperature' => 0.7
    ];
    
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
    curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    
    if ($httpCode === 200) {
        $result = json_decode($response, true);
        echo "응답: " . $result['response_text'] . "\n";
        echo "토큰 사용량: " . $result['total_tokens_used'] . "\n";
        echo "응답 시간: " . number_format($result['response_time'], 2) . "초\n";
    } else {
        echo "API 오류: HTTP $httpCode\n";
    }
}

// 실행
basicChat();
// 또는
basicChatWithCurl();

?>
```

---

## 📝 테스트 시나리오

### 1. 기본 기능 테스트

```bash
# 1. 서버 상태 확인
curl http://localhost:5601/

# 2. 시스템 정보 확인
curl http://localhost:5601/api/v1/system/status

# 3. 기본 채팅 테스트
curl -X POST "http://localhost:5601/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{"user_message": "안녕하세요!"}'
```

### 2. Free 모드 테스트

```bash
# 유효한 API Key로 테스트
curl -X POST "http://localhost:5601/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "user_message": "테스트 메시지",
    "openai_api_key": "sk-valid-key",
    "free_mode": true
  }'

# 잘못된 API Key로 테스트 (기본 Key로 폴백)
curl -X POST "http://localhost:5601/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "user_message": "테스트 메시지",
    "openai_api_key": "sk-invalid-key",
    "free_mode": true
  }'
```

### 3. 에러 처리 테스트

```bash
# 빈 메시지 테스트
curl -X POST "http://localhost:5601/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{"user_message": ""}'

# 잘못된 토큰 수 테스트
curl -X POST "http://localhost:5601/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "user_message": "테스트",
    "max_tokens": -1
  }'

# 잘못된 temperature 테스트
curl -X POST "http://localhost:5601/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "user_message": "테스트",
    "temperature": 3.0
  }'
```

---

## 🔗 관련 문서

- **[API 문서](./README.md)**: 전체 API 명세
- **[시스템 모니터링](./system-monitoring.md)**: 시스템 모니터링 API 상세 가이드
- **[에러 처리](./error-handling.md)**: 에러 처리 및 디버깅 가이드

---

**문서 버전**: 1.0  
**최종 업데이트**: 2024년 12월  
**작성자**: LLM Server 개발팀 
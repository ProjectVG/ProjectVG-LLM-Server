# System Monitoring API

이 문서는 `/api/v1/system` 이하의 시스템 정보 및 헬스체크 엔드포인트에 대한 설명입니다.

---

## 엔드포인트 목록

### 1. GET `/api/v1/system/info`
- **설명:** 전체 시스템 정보를 반환합니다.
- **Response 예시:**
```json
{
  "timestamp": "2024-01-01T00:00:00",
  "system": {
    "platform": "Windows",
    "platform_version": "10.0.26100",
    "architecture": "AMD64",
    "processor": "Intel64 Family 6",
    "hostname": "DESKTOP-XXXXX",
    "python_version": "3.11.0"
  },
  "cpu": {
    "usage_percent": 15.2,
    "count": 8,
    "frequency_mhz": 2400.0,
    "frequency_max_mhz": 3200.0,
    "load_average": [0.5, 0.3, 0.2]
  },
  "memory": {
    "total_gb": 16.0,
    "available_gb": 8.0,
    "used_gb": 8.0,
    "usage_percent": 50.0,
    "swap_total_gb": 2.0,
    "swap_used_gb": 0.1,
    "swap_usage_percent": 5.0
  },
  "disk": {
    "total_gb": 500.0,
    "used_gb": 200.0,
    "free_gb": 300.0,
    "usage_percent": 40.0,
    "read_bytes": 1024000,
    "write_bytes": 512000,
    "read_count": 100,
    "write_count": 50
  },
  "network": {
    "bytes_sent": 1000000,
    "bytes_recv": 2000000,
    "packets_sent": 1000,
    "packets_recv": 2000,
    "active_connections": 150
  },
  "process": {
    "pid": 1234,
    "name": "python.exe",
    "cpu_percent": 2.5,
    "memory_mb": 128.5,
    "memory_percent": 1.2,
    "num_threads": 8,
    "create_time": "2024-01-01T00:00:00"
  },
  "docker": {
    "is_docker": false,
    "container_id": null,
    "image": null
  }
}
```

### 2. GET `/api/v1/system/status`
- **설명:** 간단한 시스템 상태(헬스체크용)를 반환합니다.
- **Response 예시:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00",
  "cpu_usage": 15.2,
  "memory_usage": 35.0,
  "memory_available_gb": 5.2
}
```

### 3. GET `/api/v1/system/cpu`
- **설명:** CPU 정보만 반환합니다.
- **Response 예시:**
```json
{
  "timestamp": "2024-01-01T00:00:00",
  "cpu": {
    "usage_percent": 15.2,
    "count": 8,
    "frequency_mhz": 2400.0,
    "frequency_max_mhz": 3200.0,
    "load_average": [0.5, 0.3, 0.2]
  }
}
```

### 4. GET `/api/v1/system/memory`
- **설명:** 메모리 정보만 반환합니다.
- **Response 예시:**
```json
{
  "timestamp": "2024-01-01T00:00:00",
  "memory": {
    "total_gb": 16.0,
    "available_gb": 8.0,
    "used_gb": 8.0,
    "usage_percent": 50.0,
    "swap_total_gb": 2.0,
    "swap_used_gb": 0.1,
    "swap_usage_percent": 5.0
  }
}
```

### 5. GET `/api/v1/system/disk`
- **설명:** 디스크 정보만 반환합니다.
- **Response 예시:**
```json
{
  "timestamp": "2024-01-01T00:00:00",
  "disk": {
    "total_gb": 500.0,
    "used_gb": 200.0,
    "free_gb": 300.0,
    "usage_percent": 40.0,
    "read_bytes": 1024000,
    "write_bytes": 512000,
    "read_count": 100,
    "write_count": 50
  }
}
```

---

## 응답 필드 설명

### System 정보
- `platform`: 운영체제 플랫폼 (Windows, Linux, macOS)
- `platform_version`: 운영체제 버전
- `architecture`: 시스템 아키텍처 (AMD64, x86_64 등)
- `processor`: 프로세서 정보
- `hostname`: 호스트명
- `python_version`: Python 버전

### CPU 정보
- `usage_percent`: CPU 사용률 (%)
- `count`: CPU 코어 수
- `frequency_mhz`: 현재 CPU 주파수 (MHz)
- `frequency_max_mhz`: 최대 CPU 주파수 (MHz)
- `load_average`: 시스템 로드 평균 (1분, 5분, 15분)

### Memory 정보
- `total_gb`: 전체 메모리 (GB)
- `available_gb`: 사용 가능한 메모리 (GB)
- `used_gb`: 사용 중인 메모리 (GB)
- `usage_percent`: 메모리 사용률 (%)
- `swap_total_gb`: 스왑 메모리 총량 (GB)
- `swap_used_gb`: 사용 중인 스왑 메모리 (GB)
- `swap_usage_percent`: 스왑 메모리 사용률 (%)

### Disk 정보
- `total_gb`: 전체 디스크 용량 (GB)
- `used_gb`: 사용 중인 디스크 용량 (GB)
- `free_gb`: 사용 가능한 디스크 용량 (GB)
- `usage_percent`: 디스크 사용률 (%)
- `read_bytes`: 읽기 바이트 수
- `write_bytes`: 쓰기 바이트 수
- `read_count`: 읽기 횟수
- `write_count`: 쓰기 횟수

### Network 정보
- `bytes_sent`: 전송된 바이트 수
- `bytes_recv`: 수신된 바이트 수
- `packets_sent`: 전송된 패킷 수
- `packets_recv`: 수신된 패킷 수
- `active_connections`: 활성 연결 수

### Process 정보
- `pid`: 프로세스 ID
- `name`: 프로세스 이름
- `cpu_percent`: 프로세스 CPU 사용률 (%)
- `memory_mb`: 프로세스 메모리 사용량 (MB)
- `memory_percent`: 프로세스 메모리 사용률 (%)
- `num_threads`: 스레드 수
- `create_time`: 프로세스 생성 시간

### Docker 정보
- `is_docker`: Docker 컨테이너 여부
- `container_id`: 컨테이너 ID (Docker 환경에서만)
- `image`: Docker 이미지명 (환경변수에서)

---

## HTTP 상태 코드

- `200 OK`: 성공적인 응답
- `500 Internal Server Error`: 시스템 정보 수집 실패

---

## 에러 응답

시스템 정보 수집 중 오류가 발생하면 다음과 같은 형식으로 응답합니다:

```json
{
  "timestamp": "2024-01-01T00:00:00",
  "error": "시스템 정보 수집 실패: [오류 메시지]"
}
```

---

## 사용 예시

### cURL

```bash
# 전체 시스템 정보
curl http://localhost:5601/api/v1/system/info

# 헬스체크
curl http://localhost:5601/api/v1/system/status

# CPU 정보만
curl http://localhost:5601/api/v1/system/cpu

# 메모리 정보만
curl http://localhost:5601/api/v1/system/memory

# 디스크 정보만
curl http://localhost:5601/api/v1/system/disk
```

### Python

```python
import requests

# 전체 시스템 정보
response = requests.get('http://localhost:5601/api/v1/system/info')
system_info = response.json()
print(f"CPU 사용률: {system_info['cpu']['usage_percent']}%")
print(f"메모리 사용률: {system_info['memory']['usage_percent']}%")

# 헬스체크
response = requests.get('http://localhost:5601/api/v1/system/status')
status = response.json()
print(f"시스템 상태: {status['status']}")
```

### JavaScript

```javascript
const axios = require('axios');

// 전체 시스템 정보
axios.get('http://localhost:5601/api/v1/system/info')
  .then(response => {
    const systemInfo = response.data;
    console.log(`CPU 사용률: ${systemInfo.cpu.usage_percent}%`);
    console.log(`메모리 사용률: ${systemInfo.memory.usage_percent}%`);
  });

// 헬스체크
axios.get('http://localhost:5601/api/v1/system/status')
  .then(response => {
    const status = response.data;
    console.log(`시스템 상태: ${status.status}`);
  });
```

---

## 참고사항

- 모든 응답은 실시간 시스템 상태를 반영합니다.
- Docker 환경에서는 컨테이너 정보도 함께 반환됩니다.
- 과도한 요청은 서버 성능에 영향을 줄 수 있습니다.
- 헬스체크 용도로는 `/status` 엔드포인트를 추천합니다.
- CPU 사용률 측정 시 약간의 지연이 있을 수 있습니다.
- 메모리 정보는 가상 메모리를 포함합니다.
- 디스크 정보는 루트 디렉토리(/) 기준입니다. 
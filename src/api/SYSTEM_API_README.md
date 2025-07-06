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
  "system": { ... },
  "cpu": { ... },
  "memory": { ... },
  "disk": { ... },
  "network": { ... },
  "process": { ... },
  "docker": { ... }
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
    "count": 4,
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
    "total_gb": 8.0,
    "available_gb": 5.2,
    "used_gb": 2.8,
    "usage_percent": 35.0,
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
    "total_gb": 50.0,
    "used_gb": 20.0,
    "free_gb": 30.0,
    "usage_percent": 40.0,
    "read_bytes": 1024000,
    "write_bytes": 512000,
    "read_count": 100,
    "write_count": 50
  }
}
```

---

## 참고사항
- 모든 응답은 실시간 시스템 상태를 반영합니다.
- Docker 환경에서는 컨테이너 정보도 함께 반환됩니다.
- 과도한 요청은 서버 성능에 영향을 줄 수 있습니다.
- 헬스체크 용도로는 `/status` 엔드포인트를 추천합니다. 
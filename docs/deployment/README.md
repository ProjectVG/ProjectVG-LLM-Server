# LLM Server 배포 및 운영 가이드

이 문서는 LLM Server를 다양한 환경에 배포하고 운영하는 방법을 상세히 설명합니다.

## 🚀 배포 개요

### 지원 배포 방식

1. **로컬 실행** - 개발 및 테스트용
2. **Docker 컨테이너** - 권장 배포 방식
3. **Docker Compose** - 다중 서비스 배포
4. **클라우드 배포** - AWS, GCP, Azure 등

### 시스템 요구사항

- **Python**: 3.11 이상
- **메모리**: 최소 512MB (권장 1GB 이상)
- **디스크**: 최소 100MB 여유 공간
- **네트워크**: OpenAI API 접근 가능

---

## 📦 로컬 배포

### 1. 환경 설정

#### Python 가상환경 생성
```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

#### 패키지 설치
```bash
# 의존성 설치
pip install -r requirement.txt

# 개발용 패키지 설치 (선택사항)
pip install pytest black flake8
```

### 2. 환경 변수 설정

#### `.env` 파일 생성
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

#### 환경 변수 직접 설정
```bash
# Windows
set OPENAI_API_KEY=your_openai_api_key_here
set SERVER_HOST=0.0.0.0
set SERVER_PORT=5601

# Linux/Mac
export OPENAI_API_KEY=your_openai_api_key_here
export SERVER_HOST=0.0.0.0
export SERVER_PORT=5601
```

### 3. 서버 실행

#### 기본 실행
```bash
python app.py
```

#### 백그라운드 실행 (Linux/Mac)
```bash
nohup python app.py > app.log 2>&1 &
```

#### PM2를 사용한 프로세스 관리 (Node.js 필요)
```bash
# PM2 설치
npm install -g pm2

# 서버 실행
pm2 start app.py --name "llm-server" --interpreter python

# 상태 확인
pm2 status

# 로그 확인
pm2 logs llm-server

# 서버 중지
pm2 stop llm-server
```

### 4. 서버 확인

```bash
# 서버 상태 확인
curl http://localhost:5601/

# API 문서 확인
curl http://localhost:5601/docs

# 시스템 정보 확인
curl http://localhost:5601/api/v1/system/status
```

---

## 🐳 Docker 배포

### 1. Docker 설치

#### Windows
- Docker Desktop for Windows 설치
- WSL2 활성화 (권장)

#### Linux (Ubuntu)
```bash
# Docker 설치
sudo apt-get update
sudo apt-get install docker.io docker-compose

# Docker 서비스 시작
sudo systemctl start docker
sudo systemctl enable docker

# 사용자를 docker 그룹에 추가
sudo usermod -aG docker $USER
```

#### macOS
- Docker Desktop for Mac 설치

### 2. Docker 이미지 빌드

#### 기본 빌드
```bash
# 이미지 빌드
docker build -t llm-server .

# 이미지 확인
docker images
```

#### 태그 지정 빌드
```bash
# 버전 태그 지정
docker build -t llm-server:v1.0 .

# 최신 태그 추가
docker tag llm-server:v1.0 llm-server:latest
```

### 3. Docker 컨테이너 실행

#### 기본 실행
```bash
# 컨테이너 실행
docker run -d \
  --name llm-server \
  -p 5601:5601 \
  -e OPENAI_API_KEY=your-api-key \
  llm-server

# 컨테이너 상태 확인
docker ps

# 로그 확인
docker logs llm-server
```

#### 환경 변수 파일 사용
```bash
# .env 파일 생성
echo "OPENAI_API_KEY=your-api-key" > .env
echo "SERVER_HOST=0.0.0.0" >> .env
echo "SERVER_PORT=5601" >> .env

# 환경 변수 파일로 실행
docker run -d \
  --name llm-server \
  -p 5601:5601 \
  --env-file .env \
  llm-server
```

#### 볼륨 마운트 (로그 및 설정)
```bash
# 로그 디렉토리 생성
mkdir -p logs

# 볼륨 마운트로 실행
docker run -d \
  --name llm-server \
  -p 5601:5601 \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/.env:/app/.env \
  -e OPENAI_API_KEY=your-api-key \
  llm-server
```

### 4. Docker Compose 사용

#### `docker-compose.yml` 설정
```yaml
version: '3.8'

services:
  llm-server:
    build: .
    container_name: llm-server
    ports:
      - "5601:5601"
    env_file:
      - .env
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5601/"]
      interval: 30s
      timeout: 10s
      retries: 3
```

#### Docker Compose 실행
```bash
# 서비스 시작
docker-compose up -d

# 서비스 상태 확인
docker-compose ps

# 로그 확인
docker-compose logs -f

# 서비스 중지
docker-compose down
```

#### 프로덕션용 Docker Compose
```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  llm-server:
    build: .
    container_name: llm-server-prod
    ports:
      - "5601:5601"
    env_file:
      - .env
    volumes:
      - ./logs:/app/logs
    restart: always
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '0.5'
        reservations:
          memory: 512M
          cpus: '0.25'
    networks:
      - llm-network

networks:
  llm-network:
    driver: bridge
```

---

## ☁️ 클라우드 배포

### 1. AWS 배포

#### EC2 인스턴스 배포
```bash
# EC2 인스턴스에 접속
ssh -i your-key.pem ubuntu@your-ec2-ip

# Docker 설치
sudo apt-get update
sudo apt-get install docker.io docker-compose

# 프로젝트 클론
git clone https://github.com/your-repo/llm-server.git
cd llm-server

# 환경 변수 설정
echo "OPENAI_API_KEY=your-api-key" > .env

# Docker Compose 실행
sudo docker-compose up -d
```

#### ECS 배포
```yaml
# task-definition.json
{
  "family": "llm-server",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "llm-server",
      "image": "your-account.dkr.ecr.region.amazonaws.com/llm-server:latest",
      "portMappings": [
        {
          "containerPort": 5601,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "OPENAI_API_KEY",
          "value": "your-api-key"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/llm-server",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

### 2. Google Cloud Platform 배포

#### Cloud Run 배포
```bash
# 프로젝트 설정
gcloud config set project your-project-id

# Docker 이미지 빌드 및 푸시
docker build -t gcr.io/your-project-id/llm-server .
docker push gcr.io/your-project-id/llm-server

# Cloud Run 배포
gcloud run deploy llm-server \
  --image gcr.io/your-project-id/llm-server \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=your-api-key
```

### 3. Azure 배포

#### Azure Container Instances
```bash
# Azure CLI 로그인
az login

# 리소스 그룹 생성
az group create --name llm-server-rg --location eastus

# 컨테이너 인스턴스 배포
az container create \
  --resource-group llm-server-rg \
  --name llm-server \
  --image your-registry.azurecr.io/llm-server:latest \
  --dns-name-label llm-server \
  --ports 5601 \
  --environment-variables OPENAI_API_KEY=your-api-key
```

---

## 🔧 운영 관리

### 1. 모니터링

#### 시스템 모니터링
```bash
# 시스템 정보 확인
curl http://localhost:5601/api/v1/system/info

# 헬스체크
curl http://localhost:5601/api/v1/system/status

# CPU 사용률 모니터링
watch -n 5 'curl -s http://localhost:5601/api/v1/system/cpu | jq ".cpu.usage_percent"'

# 메모리 정보 확인
curl http://localhost:5601/api/v1/system/memory

# 디스크 정보 확인
curl http://localhost:5601/api/v1/system/disk
```

#### 로그 모니터링
```bash
# 실시간 로그 확인
tail -f logs/app.log

# Docker 로그 확인
docker logs -f llm-server

# Docker Compose 로그 확인
docker-compose logs -f
```

#### 성능 모니터링
```bash
# 메모리 사용량 확인
docker stats llm-server

# 네트워크 연결 확인
netstat -tulpn | grep 5601

# 프로세스 확인
ps aux | grep python
```

### 2. 백업 및 복구

#### 설정 백업
```bash
# 설정 파일 백업
cp .env .env.backup.$(date +%Y%m%d)

# Docker 이미지 백업
docker save llm-server > llm-server-backup.tar

# 로그 백업
tar -czf logs-backup-$(date +%Y%m%d).tar.gz logs/
```

#### 데이터 복구
```bash
# 설정 복구
cp .env.backup.20241201 .env

# Docker 이미지 복구
docker load < llm-server-backup.tar

# 로그 복구
tar -xzf logs-backup-20241201.tar.gz
```

### 3. 업데이트 및 유지보수

#### 애플리케이션 업데이트
```bash
# 코드 업데이트
git pull origin main

# Docker 이미지 재빌드
docker-compose build

# 서비스 재시작
docker-compose up -d

# 이전 버전으로 롤백
docker-compose down
docker tag llm-server:previous llm-server:latest
docker-compose up -d
```

#### 의존성 업데이트
```bash
# Python 패키지 업데이트
pip install --upgrade -r requirement.txt

# Docker 이미지 재빌드
docker build --no-cache -t llm-server .
```

### 4. 보안 관리

#### 환경 변수 보안
```bash
# 민감한 정보 암호화
echo "OPENAI_API_KEY=$(echo -n 'your-api-key' | base64)" >> .env

# 환경 변수 파일 권한 설정
chmod 600 .env

# Docker secrets 사용 (Swarm 모드)
echo "your-api-key" | docker secret create openai_api_key -
```

#### 네트워크 보안
```bash
# 방화벽 설정
sudo ufw allow 5601/tcp

# Docker 네트워크 격리
docker network create --driver bridge llm-network
docker run --network llm-network llm-server
```

---

## 🚨 문제 해결

### 1. 일반적인 문제

#### 서버 시작 실패
```bash
# 포트 충돌 확인
netstat -tulpn | grep 5601

# 프로세스 종료
sudo kill -9 $(lsof -t -i:5601)

# Docker 컨테이너 재시작
docker restart llm-server
```

#### OpenAI API 연결 실패
```bash
# API Key 확인
echo $OPENAI_API_KEY

# 네트워크 연결 확인
curl -I https://api.openai.com/v1/models

# 프록시 설정 (필요시)
export HTTP_PROXY=http://proxy:port
export HTTPS_PROXY=http://proxy:port
```

#### 메모리 부족
```bash
# 메모리 사용량 확인
free -h

# Docker 메모리 제한 설정
docker run --memory=1g llm-server

# 불필요한 컨테이너 정리
docker system prune -a
```

### 2. 로그 분석

#### 오류 로그 검색
```bash
# 오류 로그 확인
grep "ERROR" logs/app.log

# 특정 시간대 로그 확인
grep "2024-12-01" logs/app.log

# 실시간 오류 모니터링
tail -f logs/app.log | grep "ERROR"
```

#### 성능 로그 분석
```bash
# 응답 시간 분석
grep "response_time" logs/app.log | awk '{print $NF}' | sort -n

# 토큰 사용량 분석
grep "total_tokens_used" logs/app.log | awk '{sum+=$NF} END {print sum}'
```

### 3. 디버깅

#### 디버그 모드 실행
```bash
# 로그 레벨 변경
export LOG_LEVEL=DEBUG

# 상세 로그 확인
docker-compose logs -f --tail=100
```

#### API 테스트
```bash
# 기본 연결 테스트
curl -X POST "http://localhost:5601/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{"user_message": "테스트"}'

# 상세 응답 확인
curl -v -X POST "http://localhost:5601/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{"user_message": "테스트"}'
```

---

## 📊 성능 최적화

### 1. 리소스 최적화

#### 메모리 최적화
```python
# app.py에서 메모리 설정
import gc

# 주기적 가비지 컬렉션
gc.collect()

# 메모리 사용량 모니터링
import psutil
process = psutil.Process()
print(f"Memory usage: {process.memory_info().rss / 1024 / 1024} MB")
```

#### CPU 최적화
```python
# 비동기 처리 최적화
import asyncio

# 동시 요청 제한
semaphore = asyncio.Semaphore(10)

async def process_request(request):
    async with semaphore:
        return await chat_service.process_chat(request)
```

### 2. 네트워크 최적화

#### 연결 풀링
```python
import aiohttp

# HTTP 클라이언트 풀 설정
async with aiohttp.ClientSession(
    connector=aiohttp.TCPConnector(
        limit=100,
        limit_per_host=30,
        ttl_dns_cache=300
    )
) as session:
    # API 호출
    pass
```

#### 캐싱 전략
```python
import functools
import time

# 응답 캐싱
@functools.lru_cache(maxsize=1000)
def cache_response(key, ttl=300):
    # 캐시 로직
    pass
```

---

## 🔗 관련 문서

- **[개요 및 시작 가이드](./../overview/README.md)**: 프로젝트 소개 및 기본 사용법
- **[API 문서](./../api/README.md)**: API 명세 및 사용법
- **[아키텍처 가이드](./../architecture/README.md)**: 프로젝트 구조 및 개발 가이드
- **[테스트 가이드](./../testing/README.md)**: 테스트 및 품질 관리

---

**문서 버전**: 1.0  
**최종 업데이트**: 2024년 12월  
**작성자**: LLM Server 개발팀 
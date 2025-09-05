# Python 3.11 slim 이미지 사용
FROM python:3.11-slim

# 작업 디렉토리 생성
WORKDIR /app

# 시스템 패키지 설치 (필요시)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 파이썬 의존성 복사 및 설치
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt

# 소스 코드 복사
COPY . .

# 기본 포트 환경변수
ENV SERVER_PORT=8080
ENV SERVER_HOST=0.0.0.0

# FastAPI 서버 실행 (uvicorn)
CMD ["python", "app.py"] 
@echo off
echo LLM Server 빠른 재시작 (캐시 활용)
echo ======================================

echo 변경사항만 적용 중...
docker-compose up --build -d

echo 컨테이너 상태 확인...
docker-compose ps

echo 빠른 재시작 완료!
echo 로그 확인: docker-compose logs -f
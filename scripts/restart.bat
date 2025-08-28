@echo off
echo LLM Server 재시작 스크립트
echo ========================

echo 기존 컨테이너 중지 및 제거...
docker-compose down

echo 이미지 다시 빌드...
docker-compose build

echo 컨테이너 시작...
docker-compose up -d

echo 컨테이너 상태 확인...
docker-compose ps

echo 더미 이미지 정리...
docker image prune -f

echo 재시작 완료!
echo 로그 확인: docker-compose logs -f
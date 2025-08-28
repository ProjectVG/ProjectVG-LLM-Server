Write-Host "LLM Server 재시작 스크립트" -ForegroundColor Green
Write-Host "========================" -ForegroundColor Green

Write-Host "기존 컨테이너 중지..." -ForegroundColor Yellow
docker-compose stop

Write-Host "변경사항 적용 (빌드 캐시 활용)..." -ForegroundColor Yellow
docker-compose build --no-cache

Write-Host "컨테이너 재시작..." -ForegroundColor Yellow
docker-compose up -d

Write-Host "컨테이너 상태 확인..." -ForegroundColor Yellow
docker-compose ps

Write-Host "재시작 완료!" -ForegroundColor Green
Write-Host "로그 확인: docker-compose logs -f" -ForegroundColor Cyan
Write-Host ""
Write-Host "추가 명령어:" -ForegroundColor Magenta
Write-Host "- 빠른 재시작 (캐시 사용): docker-compose restart" -ForegroundColor Gray
Write-Host "- 완전 정리 후 재빌드: docker-compose down --volumes --rmi all && docker-compose up --build -d" -ForegroundColor Gray
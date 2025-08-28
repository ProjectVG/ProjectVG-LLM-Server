Write-Host "LLM Server 빠른 재시작 (캐시 활용)" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green

Write-Host "변경사항만 적용 중..." -ForegroundColor Yellow
docker-compose up --build -d

Write-Host "컨테이너 상태 확인..." -ForegroundColor Yellow
docker-compose ps

Write-Host "빠른 재시작 완료!" -ForegroundColor Green
Write-Host "로그 확인: docker-compose logs -f" -ForegroundColor Cyan
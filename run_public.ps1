Write-Host "========================================================" -ForegroundColor Yellow
Write-Host "       SunLoop: Public Instant Tunnel Launcher" -ForegroundColor Yellow
Write-Host "========================================================" -ForegroundColor Yellow
Write-Host ""

$running = docker ps | Select-String "sunloop_prototype"
if (-not $running) {
    Write-Host "Starting Docker container..." -ForegroundColor Cyan
    docker compose up -d
} else {
    Write-Host "Docker container is already active on port 8501." -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================================" -ForegroundColor Yellow
Write-Host " Exposing port 8501 via instant public tunnel..." -ForegroundColor Cyan
Write-Host " Share the https link below with any phone or computer!" -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Yellow
Write-Host ""

ssh -p 443 -o StrictHostKeyChecking=no -R0:127.0.0.1:8501 a.pinggy.io

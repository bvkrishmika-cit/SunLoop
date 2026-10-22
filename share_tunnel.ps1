Write-Host "========================================================" -ForegroundColor Yellow
Write-Host "      SunLoop Public Sharing Tunnel Launcher" -ForegroundColor Yellow
Write-Host "========================================================" -ForegroundColor Yellow
Write-Host ""
Write-Host "Launching public tunnel for http://localhost:8501..." -ForegroundColor Cyan

if (Get-Command npx -ErrorAction SilentlyContinue) {
    Write-Host "Using npx localtunnel..." -ForegroundColor Green
    npx localtunnel --port 8501
} else {
    Write-Host "npx not found on host. Launching zero-install SSH tunnel (localhost.run)..." -ForegroundColor Green
    Write-Host "Your public URL will be displayed below:" -ForegroundColor Yellow
    ssh -o StrictHostKeyChecking=no -R 80:localhost:8501 nokey@localhost.run
}

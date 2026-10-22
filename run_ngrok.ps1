param(
    [string]$AuthToken = $env:NGROK_AUTHTOKEN
)

Write-Host "========================================================" -ForegroundColor Yellow
Write-Host "       SunLoop - Ngrok Public Tunnel Launcher" -ForegroundColor Yellow
Write-Host "========================================================" -ForegroundColor Yellow
Write-Host ""

if (-not $AuthToken) {
    Write-Host "ngrok requires a free authtoken from https://dashboard.ngrok.com/get-started/your-authtoken" -ForegroundColor Cyan
    $AuthToken = Read-Host "Paste your ngrok authtoken here"
}

if ($AuthToken) {
    Write-Host "Starting ngrok tunnel for SunLoop on port 8501..." -ForegroundColor Green
    docker run --rm -it -e NGROK_AUTHTOKEN="$AuthToken" -p 4040:4040 ngrok/ngrok http host.docker.internal:8501
} else {
    Write-Host "No authtoken provided. Launching zero-token public tunnel..." -ForegroundColor Yellow
    .\run_public.ps1
}

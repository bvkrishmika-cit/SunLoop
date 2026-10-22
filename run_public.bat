@echo off
echo ========================================================
echo       SunLoop: Public Instant Tunnel Launcher
echo ========================================================
echo.

echo Checking if Docker container is running...
docker ps | findstr sunloop_prototype >nul
if %ERRORLEVEL% neq 0 (
    echo Starting Docker container...
    docker compose up -d
) else (
    echo Docker container is already active on port 8501.
)

echo.
echo ========================================================
echo  Exposing port 8501 via instant public tunnel...
echo  Share the https link below with any phone or computer!
echo ========================================================
echo.

ssh -p 443 -o StrictHostKeyChecking=no -R0:127.0.0.1:8501 a.pinggy.io
pause

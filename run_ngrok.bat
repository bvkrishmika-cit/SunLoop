@echo off
echo ========================================================
echo       SunLoop - Ngrok Public Tunnel Launcher
echo ========================================================
echo.

if "%NGROK_AUTHTOKEN%"=="" (
    echo To use ngrok, you need a free authtoken from https://dashboard.ngrok.com
    set /p NGROK_AUTHTOKEN="Paste your ngrok authtoken here: "
)

echo Starting ngrok tunnel on port 8501...
docker run --rm -it --network=host -e NGROK_AUTHTOKEN=%NGROK_AUTHTOKEN% ngrok/ngrok http 8501
pause

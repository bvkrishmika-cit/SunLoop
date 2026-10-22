@echo off
echo ========================================================
echo       SunLoop Public Sharing Tunnel Launcher
echo ========================================================
echo.
echo Launching public tunnel for http://localhost:8501 ...
echo.

where npx >nul 2>nul
if %ERRORLEVEL% equ 0 (
    echo Using npx localtunnel...
    npx localtunnel --port 8501
) else (
    echo [Notice] npx not found on host. Using zero-install secure SSH tunnel (localhost.run)...
    echo Your public link will appear below:
    echo.
    ssh -o StrictHostKeyChecking=no -R 80:localhost:8501 nokey@localhost.run
)
pause

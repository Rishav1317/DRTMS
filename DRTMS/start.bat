@echo off
echo =====================================================
echo   DRTMS - Starting Backend API
echo =====================================================
cd backend
start "DRTMS API Server" python app.py
timeout /t 2 /nobreak > nul
echo.
echo Backend started at http://localhost:5000
echo.
echo Opening frontend...
start "" "..\frontend\index.html"
echo.
echo DRTMS is running! Press any key to close this window.
pause

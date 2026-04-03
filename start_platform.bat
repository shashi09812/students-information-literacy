@echo off
SETLOCAL EnableDelayedExpansion
cd /d "%~dp0"

echo =============================================
echo   Information Literacy Predictor Platform
echo =============================================
echo.

echo [1] Checking Python installation...
python --version
IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python is not installed or not in PATH.
    pause
    exit /b 1
)

echo.
echo [2] Installing / updating dependencies...
python -m pip install -r requirements.txt
IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install dependencies.
    pause
    exit /b 1
)

echo.
echo [3] Starting Flask application...
echo     Access the platform at: http://localhost:5000
echo ---------------------------------------------
rem If another process is listening on port 5000, terminate it so this script can start cleanly
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5000" ^| findstr LISTENING') do (
    set "PID=%%a"
)
if defined PID (
    echo Found existing process listening on port 5000 (PID=%PID%). Attempting to terminate it.
    taskkill /F /PID %PID% >nul 2>&1
    timeout /t 1 /nobreak >nul
)

python app.py
IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: Flask application failed to start.
    pause
    exit /b 1
)

ENDLOCAL
exit /b 0

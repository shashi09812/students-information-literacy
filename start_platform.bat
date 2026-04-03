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
python app.py

ENDLOCAL
exit /b 0

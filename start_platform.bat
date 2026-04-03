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

rem --- ensure port 5000 is free: PowerShell first, fallback to netstat ---
set "PID="

powershell -NoProfile -Command "try { (Get-NetTCPConnection -LocalPort 5000 -State Listen -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess) -join ',' } catch { }" > "%temp%\ps_pid.txt" 2>nul
for /f "usebackq delims=" %%p in ("%temp%\ps_pid.txt") do set "PID=%%p"
if exist "%temp%\ps_pid.txt" del "%temp%\ps_pid.txt" >nul 2>&1

if not defined PID (
    netstat -ano > "%temp%\net_all.txt" 2>nul
    findstr ":5000" "%temp%\net_all.txt" > "%temp%\net5000.txt" 2>nul
    findstr "LISTENING" "%temp%\net5000.txt" > "%temp%\net5000_l.txt" 2>nul
    if exist "%temp%\net5000_l.txt" (
        for /f "usebackq tokens=5 delims= " %%a in ("%temp%\net5000_l.txt") do set "PID=%%a"
        del "%temp%\net5000_l.txt" >nul 2>&1
    )
    if exist "%temp%\net5000.txt" del "%temp%\net5000.txt" >nul 2>&1
    if exist "%temp%\net_all.txt" del "%temp%\net_all.txt" >nul 2>&1
)

if defined PID (
    echo Found existing process listening on port 5000 (PID=%PID%). Attempting to terminate it.
    taskkill /F /PID %PID% >nul 2>&1
    timeout /t 1 /nobreak >nul
)

python app.py

ENDLOCAL
exit /b 0

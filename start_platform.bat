@echo off
SETLOCAL EnableDelayedExpansion

echo ============================================================
echo      Information Literacy Learning Predictor - Startup
echo ============================================================
echo.

:: 1. Check for Git and pull updates
echo [1/4] Checking for platform updates...
where git >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    git pull
    echo.
) else (
    echo [SKIP] Git not found, skipping auto-update.
)

:: 2. Check and update dependencies
echo [2/4] Updating dependencies...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to update dependencies. Please check your internet connection.
    pause
    exit /b %ERRORLEVEL%
)
echo.

:: 3. Ensure analytical models are present
echo [3/4] Verifying analytical models...
if not exist "models\random_forest.joblib" (
    echo [INFO] Models missing. Training fresh analytical components...
    python ml_models.py
) else (
    echo [OK] Models are ready.
)
echo.

:: 4. Launch the Platform
echo [4/4] Starting the Mentor Platform...
echo.
echo ------------------------------------------------------------
echo PLATFORM IS LIVE AT: http://localhost:5000
echo ------------------------------------------------------------
echo.

:: Use Waitress for professional performance as configured in wsgi.py
python app.py

pause
ENDLOCAL

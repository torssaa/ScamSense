@echo off
setlocal
echo ==========================================
echo    STARTING SCAMSENSE AI PROTECTION
echo ==========================================
echo.
cd /d "%~dp0backend"
echo [1/2] Checking dependencies...
py -m pip install -r requirements.txt >nul 2>&1
echo.
echo [2/2] Starting backend on http://127.0.0.1:8000...
echo.
echo Please Keep This Window Open!
echo Scan Gmail, Outlook, WhatsApp and Telegram with ScamSense.
echo.
py main.py
pause

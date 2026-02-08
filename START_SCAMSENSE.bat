@echo off
echo ==========================================
echo    STARTING SCAMSENSE BACKEND SERVER
echo ==========================================
echo.
cd /d %~dp0backend
echo [1/2] Installing/Checking dependencies...
pip install -r requirements.txt
echo.
echo [2/2] Starting server on http://127.0.0.1:8000...
echo Keep this window open while using the extension!
echo.
python main.py
pause

@echo off
title DocuMind Enterprise Launcher
color 0A

echo.
echo  ==========================================
echo   @@@@  DocuMind Enterprise  @@@@
echo   Local AI Document Intelligence
echo  ==========================================
echo.

REM ── Check Python ───────────────────────────────────────────────
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.10+ from python.org
    pause
    exit /b 1
)

REM ── Check Ollama ────────────────────────────────────────────────
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Ollama does not appear to be running.
    echo           Please open a NEW terminal and run:  ollama serve
    echo           Then press any key to continue launching DocuMind...
    pause
)

REM ── Activate venv if present ────────────────────────────────────
if exist "venv\Scripts\activate.bat" (
    echo [INFO] Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM ── Launch Streamlit ────────────────────────────────────────────
echo [INFO] Starting DocuMind Enterprise...
echo [INFO] Opening at: http://localhost:8501
echo.
echo Press Ctrl+C to stop the server.
echo.

venv\Scripts\streamlit.exe run app.py --server.port 8501

pause

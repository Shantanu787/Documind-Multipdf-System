@echo off
title DocuMind Enterprise — Dependency Installer
color 0B

echo.
echo  ==========================================
echo   DocuMind Enterprise — Setup Wizard
echo  ==========================================
echo.

REM ── Check Python version ────────────────────────────────────────
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python 3.10+ is required.
    echo         Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%v in ('python --version 2^>^&1') do set PYVER=%%v
echo [OK] Python %PYVER% found.

REM ── Create virtual environment ──────────────────────────────────
if not exist "venv" (
    echo.
    echo [STEP 1] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created.
) else (
    echo [OK] Virtual environment already exists.
)

REM ── Activate venv ───────────────────────────────────────────────
call venv\Scripts\activate.bat

REM ── Upgrade pip ─────────────────────────────────────────────────
echo.
echo [STEP 2] Upgrading pip...
python -m pip install --upgrade pip --quiet

REM ── Install CPU-only PyTorch first (critical for low-end HW) ────
echo.
echo [STEP 3] Installing PyTorch (CPU-only)...
echo          This avoids downloading a 2GB+ CUDA build.
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu --quiet
if errorlevel 1 (
    echo [WARNING] PyTorch CPU install had issues. Trying generic install...
    pip install torch --quiet
)
echo [OK] PyTorch installed.

REM ── Install all other dependencies ──────────────────────────────
echo.
echo [STEP 4] Installing DocuMind dependencies...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo [ERROR] Dependency installation failed. Check your internet connection.
    pause
    exit /b 1
)
echo [OK] All dependencies installed.

REM ── Pre-download embedding models ───────────────────────────────
echo.
echo [STEP 5] Pre-downloading embedding model (BAAI/bge-small-en-v1.5)...
echo          This is ~130 MB and only happens once.
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-small-en-v1.5', device='cpu'); print('[OK] Embedding model ready.')"

echo.
echo [STEP 6] Pre-downloading reranker model...
python -c "from sentence_transformers import CrossEncoder; CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2', device='cpu'); print('[OK] Reranker model ready.')"

REM ── Summary ─────────────────────────────────────────────────────
echo.
echo  ==========================================
echo   [SUCCESS] Setup Complete!
echo  ==========================================
echo.
echo  NEXT STEPS:
echo  1. Install Ollama from: https://ollama.com/download
echo  2. Open a terminal and run: ollama pull phi3:mini
echo  3. In another terminal run: ollama serve
echo  4. Double-click start.bat to launch DocuMind
echo.
pause

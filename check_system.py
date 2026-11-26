"""
check_system.py
Run this before starting DocuMind to verify all components are working.
Usage: python check_system.py
"""

import sys
import os
import subprocess
from pathlib import Path

# ── ANSI colours (work in Windows 10+ terminals) ─────────────────────────────
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
BLUE   = "\033[94m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

OK   = f"{GREEN}[  OK  ]{RESET}"
FAIL = f"{RED}[ FAIL ]{RESET}"
WARN = f"{YELLOW}[ WARN ]{RESET}"
INFO = f"{BLUE}[ INFO ]{RESET}"


def header(title: str):
    print(f"\n{BOLD}{'─'*55}{RESET}")
    print(f"{BOLD}  {title}{RESET}")
    print(f"{BOLD}{'─'*55}{RESET}")


def check(label: str, condition: bool, hint: str = ""):
    status = OK if condition else FAIL
    print(f"  {status}  {label}")
    if not condition and hint:
        print(f"         {YELLOW}↳ {hint}{RESET}")
    return condition


# ═══════════════════════════════════════════════════════════════════════════════
header("1. Python Environment")

py_ok = check(
    f"Python {sys.version.split()[0]}",
    sys.version_info >= (3, 10),
    "Python 3.10+ required. Download from https://www.python.org",
)

# ═══════════════════════════════════════════════════════════════════════════════
header("2. Python Dependencies")

deps = {
    "streamlit":             "pip install streamlit",
    "fitz (PyMuPDF)":        "pip install pymupdf",
    "sentence_transformers": "pip install sentence-transformers",
    "chromadb":              "pip install chromadb",
    "numpy":                 "pip install numpy",
    "requests":              "pip install requests",
    "torch":                 "pip install torch --index-url https://download.pytorch.org/whl/cpu",
}

all_deps_ok = True
for mod, install_cmd in deps.items():
    real_mod = mod.split(" ")[0]   # strip display suffix
    try:
        __import__(real_mod)
        check(mod, True)
    except ImportError:
        check(mod, False, install_cmd)
        all_deps_ok = False

# ═══════════════════════════════════════════════════════════════════════════════
header("3. Ollama Service")

import requests as req

ollama_alive = False
try:
    r = req.get("http://localhost:11434/api/tags", timeout=4)
    ollama_alive = r.status_code == 200
    check("Ollama service running", ollama_alive)

    if ollama_alive:
        data   = r.json()
        models = [m["name"] for m in data.get("models", [])]
        if models:
            print(f"  {INFO}  Available models: {', '.join(models)}")
            preferred = ["phi3:mini", "phi3", "mistral", "llama3.2:1b"]
            found = any(
                any(p.split(":")[0] in m for p in preferred)
                for m in models
            )
            check(
                "Preferred model available (phi3:mini / mistral)",
                found,
                "Run: ollama pull phi3:mini",
            )
        else:
            check("At least one model pulled", False, "Run: ollama pull phi3:mini")

except Exception:
    check(
        "Ollama service running",
        False,
        "Install from https://ollama.com/download  then run: ollama serve",
    )

# ═══════════════════════════════════════════════════════════════════════════════
header("4. Embedding Models")

try:
    from sentence_transformers import SentenceTransformer
    print(f"  {INFO}  Checking BAAI/bge-small-en-v1.5 (may download ~130 MB first time)…")
    m = SentenceTransformer("BAAI/bge-small-en-v1.5", device="cpu")
    v = m.encode("test", show_progress_bar=False)
    check(f"bge-small-en-v1.5  (dim={len(v)})", True)
    del m
except Exception as e:
    check("bge-small-en-v1.5", False, str(e))

try:
    from sentence_transformers import CrossEncoder
    print(f"  {INFO}  Checking cross-encoder/ms-marco-MiniLM-L-6-v2…")
    ce = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2", device="cpu")
    check("ms-marco-MiniLM-L-6-v2 (reranker)", True)
    del ce
except Exception as e:
    check("ms-marco-MiniLM-L-6-v2 (reranker)", False, str(e))

# ═══════════════════════════════════════════════════════════════════════════════
header("5. Data Directories")

dirs = ["data/uploads", "data/vectorstore", "data/cache"]
for d in dirs:
    p = Path(d)
    p.mkdir(parents=True, exist_ok=True)
    check(f"Directory: {d}", p.exists())

# ═══════════════════════════════════════════════════════════════════════════════
header("6. Memory Check")

try:
    import psutil
    vm    = psutil.virtual_memory()
    total = vm.total / 1e9
    avail = vm.available / 1e9
    check(
        f"RAM: {total:.1f} GB total, {avail:.1f} GB available",
        avail >= 2.0,
        "Close other applications to free RAM.",
    )
except ImportError:
    print(f"  {WARN}  psutil not installed — skipping RAM check (run: pip install psutil)")

# ═══════════════════════════════════════════════════════════════════════════════
header("Summary")

if all_deps_ok and ollama_alive:
    print(f"\n  {GREEN}{BOLD}✅ System is ready! Run: streamlit run app.py{RESET}\n")
elif all_deps_ok:
    print(f"\n  {YELLOW}{BOLD}⚠️  Dependencies OK but Ollama is not running.{RESET}")
    print(f"     Start Ollama: ollama serve")
    print(f"     Pull model:   ollama pull phi3:mini\n")
else:
    print(f"\n  {RED}{BOLD}❌ Some dependencies are missing.{RESET}")
    print(f"     Run install.bat (Windows) or: pip install -r requirements.txt\n")

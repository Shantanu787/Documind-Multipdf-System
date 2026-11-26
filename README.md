# 🧠 DocuMind Enterprise
### Production-Grade Local RAG System · Optimised for Low-End Hardware

> **Chat with 50–100 PDFs simultaneously · Fully local · No API costs · Runs on 8 GB RAM**

---

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Architecture Overview](#architecture-overview)
3. [Folder Structure](#folder-structure)
4. [Step-by-Step Installation](#step-by-step-installation)
5. [Running the Application](#running-the-application)
6. [How to Use DocuMind](#how-to-use-documind)
7. [Performance Tuning](#performance-tuning)
8. [Troubleshooting Guide](#troubleshooting-guide)
9. [Creating the ZIP File](#creating-the-zip-file)

---

## System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU       | AMD Ryzen 3 3250U (4 threads) | Any 4+ core x64 CPU |
| RAM       | 8 GB (6 GB usable) | 16 GB |
| GPU       | None required | None required |
| Storage   | 5 GB free | 10 GB free |
| OS        | Windows 10 64-bit | Windows 10/11 64-bit |
| Python    | 3.10+ | 3.11 |

---

## Architecture Overview

```
User Query
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│                   Streamlit UI (app.py)                  │
│        Chat Interface · Sidebar · Streaming Display      │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│                  RAG Pipeline (core/)                    │
│                                                          │
│  1. EMBED QUERY                                          │
│     └─ bge-small-en-v1.5 (sentence-transformers, CPU)   │
│                                                          │
│  2. VECTOR SEARCH                                        │
│     └─ ChromaDB (local persistent, cosine similarity)   │
│        ↳ Top-15 candidate chunks retrieved               │
│                                                          │
│  3. RERANK                                               │
│     └─ ms-marco-MiniLM-L-6-v2 (cross-encoder, CPU)      │
│        ↳ Top-8 highest-quality chunks selected           │
│                                                          │
│  4. GENERATE                                             │
│     └─ Ollama → phi3:mini / mistral (streaming)          │
│        ↳ Structured answer with inline citations         │
└─────────────────────────────────────────────────────────┘

PDF Files
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│               Document Processor (core/)                 │
│                                                          │
│  PyMuPDF → Text Extraction → Sentence-Aware Chunking    │
│  Chunk size: 500 tokens · Overlap: 80 tokens             │
│  Metadata: filename, page number, chunk_id               │
│       │                                                  │
│       ▼                                                  │
│  Embedder → ChromaDB (persisted to disk)                 │
└─────────────────────────────────────────────────────────┘
```

---

## Folder Structure

```
documind_enterprise/
│
├── app.py                          ← Main entry point (run this)
├── requirements.txt                ← Python dependencies
├── install.bat                     ← One-click Windows installer
├── start.bat                       ← One-click launcher
├── check_system.py                 ← Pre-flight system check
├── README.md                       ← This file
│
├── .streamlit/
│   └── config.toml                 ← Streamlit server configuration
│
├── config/
│   ├── __init__.py
│   └── settings.py                 ← All system parameters
│
├── core/
│   ├── __init__.py
│   ├── document_processor.py       ← PDF → chunks pipeline
│   ├── embedder.py                 ← Sentence-transformers wrapper
│   ├── vector_store.py             ← ChromaDB interface
│   ├── reranker.py                 ← Cross-encoder reranking
│   ├── llm_client.py               ← Ollama streaming client
│   ├── rag_pipeline.py             ← Full RAG orchestrator
│   └── session.py                  ← Streamlit session management
│
├── ui/
│   ├── __init__.py
│   ├── styles.py                   ← CSS injection (dark theme)
│   ├── sidebar.py                  ← Upload, status, file list
│   └── chat.py                     ← Chat interface + streaming
│
├── utils/
│   ├── __init__.py
│   ├── logger.py                   ← Logging configuration
│   └── cache.py                    ← Disk-based cache utility
│
└── data/                           ← Auto-created at runtime
    ├── uploads/                    ← Saved PDF files
    ├── vectorstore/                ← ChromaDB persistent data
    └── cache/                      ← Model & embedding cache
```

---

## Step-by-Step Installation

### Step 1 — Install Python 3.11

1. Go to **https://www.python.org/downloads/**
2. Download **Python 3.11.x (Windows installer 64-bit)**
3. Run installer. **CHECK ✅ "Add Python to PATH"** before clicking Install
4. Verify: open Command Prompt → type `python --version`

---

### Step 2 — Install Ollama

1. Go to **https://ollama.com/download**
2. Click **Download for Windows**
3. Run the installer (it installs as a background service)
4. Open Command Prompt and verify:
   ```
   ollama --version
   ```

---

### Step 3 — Download an AI Model

Open Command Prompt and run **one** of these (phi3:mini is preferred — smaller, faster):

```bash
# Option A: Phi-3 Mini (RECOMMENDED — 2.3 GB, fastest on low RAM)
ollama pull phi3:mini

# Option B: Mistral 7B (better quality, needs ~5 GB RAM)
ollama pull mistral

# Option C: Tiny fallback (800 MB, limited quality)
ollama pull tinyllama
```

> ⏳ This downloads the model file. Wait for it to complete (may take 10–30 minutes on slow internet).

---

### Step 4 — Install Python Dependencies

**Option A — Automatic (recommended):**
```
Double-click install.bat
```

**Option B — Manual:**

Open Command Prompt **in the documind_enterprise folder**:

```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# Install CPU-only PyTorch first (important — avoids 2 GB CUDA download)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install all other dependencies
pip install -r requirements.txt
```

> ⏳ This will download ~800 MB of packages. It only happens once.

---

### Step 5 — Verify Installation

```bash
python check_system.py
```

You should see all green `[  OK  ]` checks. Fix any failures before continuing.

---

## Running the Application

### Method A — Double-click `start.bat`

### Method B — Command Line

Open two separate Command Prompt windows:

**Window 1 — Start Ollama:**
```bash
ollama serve
```

**Window 2 — Start DocuMind:**
```bash
cd documind_enterprise
venv\Scripts\activate
streamlit run app.py
```

Then open your browser to: **http://localhost:8501**

---

## How to Use DocuMind

### 1. Upload Documents
- Click the **sidebar** on the left
- Drag & drop or click to upload **PDF files** (up to 50 MB each, up to 100 files)
- Click **"⚡ Index Documents"**
- Wait for the progress bar to complete (1–3 minutes per 100-page document)

### 2. Ask Questions
- Type your question in the chat input at the bottom
- Press **Enter** to send
- Watch the response stream in real-time

### 3. Reading Citations
- Inline citations appear as `[filename.pdf, Page X]`
- A **Sources** panel below each response shows all retrieved documents with relevance scores

### 4. Filter to Specific Documents
- In the sidebar under **Indexed Documents**, use the multiselect to restrict search to specific files
- Leave empty to search across all documents

### 5. Example Questions That Work Well
```
"Summarize the main findings across all uploaded documents"
"What does [document name] say about [topic]?"
"Compare the approaches described in the research papers"
"List all key recommendations from the policy documents"
"What evidence supports the argument about [topic]?"
"Explain the methodology used in the study on page 15"
```

---

## Performance Tuning

### For Very Low RAM (6 GB usable)

Edit `config/settings.py`:

```python
EMBEDDING_BATCH = 4      # reduce from 8
TOP_K_RETRIEVE  = 10     # reduce from 15
TOP_K_RERANK    = 6      # reduce from 8
LLM_MAX_TOKENS  = 1024   # reduce from 2048
RERANKER_ENABLED = False  # disable reranker to save ~200 MB RAM
```

### For Faster Responses (sacrifice some quality)

```python
# In config/settings.py
LLM_MAX_TOKENS  = 512    # shorter answers
TOP_K_RETRIEVE  = 8
TOP_K_RERANK    = 4
```

### Ollama Performance Flags

In `core/llm_client.py`, the `num_thread` option is already set to 4 (matching Ryzen 3 3250U thread count). For other CPUs, adjust:

```python
"num_thread": os.cpu_count() or 4,   # auto-detect
```

---

## Troubleshooting Guide

### ❌ "Cannot connect to Ollama"

**Problem:** Ollama service is not running.

**Fix:**
```bash
# Open a new terminal and run:
ollama serve

# Keep this terminal open while using DocuMind
```

---

### ❌ "No models found" / blank responses

**Problem:** No model has been downloaded to Ollama.

**Fix:**
```bash
ollama pull phi3:mini
# Wait for download to complete, then retry
```

---

### ❌ Blank white screen in browser

**Problem:** Streamlit failed to start, or browser cached an error.

**Fix:**
1. Press `Ctrl+C` in the terminal to stop
2. Run: `streamlit cache clear`
3. Delete the `.streamlit/` folder
4. Restart: `streamlit run app.py`
5. Hard refresh browser: `Ctrl+Shift+R`

---

### ❌ "Memory Error" / App crashes during PDF upload

**Problem:** Too many large PDFs processed at once.

**Fix:**
- Upload 10–20 PDFs at a time instead of all at once
- Reduce `EMBEDDING_BATCH = 4` in `config/settings.py`
- Close other applications (browser tabs, Office, etc.)
- Restart DocuMind between large upload batches

---

### ❌ Very slow responses (5+ minutes per answer)

**Problem:** Model is too large for your RAM, causing disk swapping.

**Fix:**
```bash
# Switch to a smaller model
ollama pull phi3:mini       # 2.3 GB — fastest
ollama pull tinyllama       # 800 MB — fallback

# Then update config/settings.py:
DEFAULT_MODEL = "phi3:mini"
```

---

### ❌ "ChromaDB error" / Database corruption

**Problem:** The vector database was interrupted during a write.

**Fix:**
```bash
# Delete the vector store and re-index
# Option 1: Use the "⚠️ Reset DB" button in the sidebar

# Option 2: Manual deletion
cd documind_enterprise
rmdir /s /q data\vectorstore
mkdir data\vectorstore
```

Then re-upload and re-index your PDFs.

---

### ❌ PDFs show no text / empty chunks

**Problem:** Your PDFs are scanned images (not text-based).

**Fix:**
1. Install Tesseract OCR from: **https://github.com/UB-Mannheim/tesseract/wiki**
2. Add Tesseract to your PATH
3. In `config/settings.py`, set:
   ```python
   OCR_ENABLED = True
   ```
4. Restart DocuMind

---

### ❌ `pip install` fails with permission errors

**Fix:**
```bash
# Run Command Prompt as Administrator, or use --user flag:
pip install --user -r requirements.txt
```

---

### ❌ Import errors for `fitz`, `chromadb`, etc.

**Problem:** You ran `streamlit run app.py` without activating the virtual environment.

**Fix:**
```bash
venv\Scripts\activate   # activate first
streamlit run app.py    # then run
```

---

## Creating the ZIP File

### Method A — Windows Explorer
1. Navigate to the folder containing `documind_enterprise/`
2. Right-click on the `documind_enterprise` folder
3. Select **"Send to" → "Compressed (zipped) folder"**
4. Rename the resulting file to `documind_enterprise.zip`

### Method B — Command Line (PowerShell)
```powershell
# Navigate to parent folder of documind_enterprise/
cd C:\Users\YourName\Desktop

# Create the ZIP
Compress-Archive -Path .\documind_enterprise -DestinationPath .\documind_enterprise.zip

# Verify
Get-Item documind_enterprise.zip | Select-Object Name, Length
```

### Method C — Using Python
```python
import shutil
shutil.make_archive("documind_enterprise", "zip", ".", "documind_enterprise")
print("ZIP created: documind_enterprise.zip")
```

### What to Include in the ZIP

```
documind_enterprise.zip
└── documind_enterprise/
    ├── app.py
    ├── requirements.txt
    ├── install.bat
    ├── start.bat
    ├── check_system.py
    ├── README.md
    ├── .streamlit/
    │   └── config.toml
    ├── config/
    │   ├── __init__.py
    │   └── settings.py
    ├── core/
    │   ├── __init__.py
    │   ├── document_processor.py
    │   ├── embedder.py
    │   ├── vector_store.py
    │   ├── reranker.py
    │   ├── llm_client.py
    │   ├── rag_pipeline.py
    │   └── session.py
    ├── ui/
    │   ├── __init__.py
    │   ├── styles.py
    │   ├── sidebar.py
    │   └── chat.py
    └── utils/
        ├── __init__.py
        ├── logger.py
        └── cache.py
```

> **Do NOT include** the `data/`, `venv/`, or `__pycache__/` folders in the ZIP.
> These are generated at runtime and are machine-specific.

---

## Quick Reference Card

```
╔══════════════════════════════════════════════════════════╗
║           DocuMind Enterprise — Quick Start              ║
╠══════════════════════════════════════════════════════════╣
║  1. ollama serve              (keep open in terminal)    ║
║  2. venv\Scripts\activate                                ║
║  3. streamlit run app.py                                 ║
║  4. Open: http://localhost:8501                          ║
║  5. Upload PDFs → Index → Ask questions                  ║
╠══════════════════════════════════════════════════════════╣
║  Models (in another terminal):                           ║
║     ollama pull phi3:mini    ← RECOMMENDED               ║
║     ollama pull mistral      ← Better quality            ║
║     ollama pull tinyllama    ← Minimal RAM               ║
╠══════════════════════════════════════════════════════════╣
║  Config file: config/settings.py                         ║
║  Logs:        documind.log                               ║
║  Vector DB:   data/vectorstore/                          ║
╚══════════════════════════════════════════════════════════╝
```

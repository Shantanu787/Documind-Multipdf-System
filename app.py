"""
DocuMind Enterprise - Production-Grade RAG Application
Optimized for low-end hardware (AMD Ryzen 3, 8GB RAM, no GPU)
"""

import streamlit as st
import os
import sys
import time
import logging
from pathlib import Path

# ── Page config MUST be first Streamlit call ──────────────────────────────────
st.set_page_config(
    page_title="DocuMind Enterprise",
    page_icon="ChatGPT Image Apr 24, 2026, 10_19_37 PM.png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": "DocuMind Enterprise — Local AI Document Intelligence",
    },
)

# ── Path setup ────────────────────────────────────────────────────────────────
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

from ui.styles import inject_styles
from ui.sidebar import render_sidebar
from ui.chat import render_chat_interface
from core.session import init_session_state
from utils.logger import setup_logger

setup_logger()
logger = logging.getLogger(__name__)

# ── Inject CSS ────────────────────────────────────────────────────────────────
inject_styles()

# ── Session bootstrap ─────────────────────────────────────────────────────────
init_session_state()

# ── Layout ────────────────────────────────────────────────────────────────────
render_sidebar()
render_chat_interface()

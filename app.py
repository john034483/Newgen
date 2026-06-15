import streamlit as st
import requests
import pandas as pd
import concurrent.futures
import random
import urllib.parse
import re
import socket
import dns.resolver

# --- FIX: Initializing session state to prevent AttributeError ---
if 'proxies' not in st.session_state:
    st.session_state.proxies = []
if 'derived_username_choice' not in st.session_state:
    st.session_state.derived_username_choice = ""
# -----------------------------------------------------------------

# Import shared OSINT and DB routines
from backend.database import init_db, create_case, get_cases, save_finding, get_findings, DB_FILE
from backend.osint import (
    fetch_proxies, perform_whois, get_geoip_info, PLATFORMS, check_platform, generate_username_guesses
)

# Initialize database
init_db()

# ─────────────────────────────────────────────
# 1. STREAMLIT LAYOUT & CUSTOM CSS
# ─────────────────────────────────────────────
st.set_page_config(layout="wide", page_title="ONSINT Core Dashboard")

st.markdown("""
    <style>
    .stMetric { background-color: #0d1117; padding: 15px; border-radius: 8px; border: 1px solid #21262d; }
    .stButton>button { border-radius: 6px; background-color: #4361ee !important; color: white !important; font-weight: bold; }
    .stAlert { border-radius: 6px; }
    </style>
    """, unsafe_allow_html=True)

# SIDEBAR: Investigator's Dashboard
with st.sidebar:
    st.title("📡 ONSINT Core")
    st.info("General Purpose OSINT Intelligence Dashboard")
    
    st.divider()
    
    st.subheader("📁 Case File Registry")
    new_case = st.text_input("Create Investigation File", placeholder="e.g. Case_2026_Global_Audit")
    if st.button("Initialize Case File"):
        if new_case:
            create_case(new_case)
            st.success(f"File created: '{new_case}'")
            st.rerun()

    cases = get_cases()
    active_case = st.selectbox("Active Case Target", ["-- Select Active Case --"] + cases)
    
    st.divider()
    
    st.subheader("🌐 Stealth Proxy Controls")
    if st.button("🔄 Scrape & Cycle Proxy Pool"):
        st.session_state.proxies = fetch_proxies()
        st.success(f"Refreshed {len(st.session_state.proxies)} proxies!")
    
    # Safe check for proxies
    proxy_text = '✅ Active (Rotating)' if len(st.session_state.proxies) > 0 else '⚠️ Direct IP (No Proxy)'
    st.write(f"**Stealth Mode:** {proxy_text}")
    st.divider()
    st.markdown("<p style='font-size:0.8rem; color:#94a3b8; font-weight:500;'><i class='fa-solid fa-user-ninja' style='color:#9d4edd; margin-right:0.25rem;'></i> Made by <strong>Ronit Gupta</strong></p>", unsafe_allow_html=True)

# EXECUTIVE DASHBOARD HEADER
st.title("📡 ONSINT Core Intelligence Suite")
st.markdown("---")

col1, col2, col3 = st.columns(3)
col1.metric("Active Case File", active_case if active_case != "-- Select Active Case --" else "Unlinked", delta_color="off")
col2.metric("Recorded Findings", len(get_findings(active_case)) if active_case != "-- Select Active Case --" else "0")
col3.metric("Proxy Pool Size", f"{len(st.session_state.proxies)} IPs" if len(st.session_state.proxies) > 0 else "Direct IP")

st.markdown("---")

# ... (baaki ka poora code same waisa hi hai, bas copy-paste kar lo) ...

import streamlit as st
import pandas as pd
import concurrent.futures
import random
import urllib.parse
import re
import socket
import dns.resolver

# 1. FIXED: Session State Initialization (Zaroori hai)
if 'proxies' not in st.session_state:
    st.session_state.proxies = []
if 'derived_username_choice' not in st.session_state:
    st.session_state.derived_username_choice = ""

from backend.database import init_db, create_case, get_cases, save_finding, get_findings
from backend.osint import (
    fetch_proxies, perform_whois, get_geoip_info, PLATFORMS, check_platform, generate_username_guesses
)

init_db()

st.set_page_config(layout="wide", page_title="ONSINT Core Dashboard")

# SIDEBAR logic
with st.sidebar:
    st.title("📡 ONSINT Core")
    st.subheader("📁 Case File Registry")
    new_case = st.text_input("Create Investigation File", placeholder="e.g. Case_2026_Audit")
    
    if st.button("Initialize Case File"):
        if new_case:
            create_case(new_case)
            st.success(f"File created: '{new_case}'")
            st.rerun() # Rerun zaroori hai

    cases = get_cases()
    active_case = st.selectbox("Active Case Target", ["-- Select Active Case --"] + cases)
    
    st.divider()
    st.subheader("🌐 Stealth Proxy Controls")
    if st.button("🔄 Scrape & Cycle Proxy Pool"):
        with st.spinner("Fetching proxies..."):
            st.session_state.proxies = fetch_proxies()
            st.success(f"Refreshed {len(st.session_state.proxies)} proxies!")
            st.rerun()
    
    proxy_count = len(st.session_state.proxies)
    st.write(f"**Stealth Mode:** {'✅ Active (' + str(proxy_count) + ')' if proxy_count > 0 else '⚠️ Direct IP'}")

# Dashboard metrics
st.title("📡 ONSINT Core Intelligence Suite")
col1, col2, col3 = st.columns(3)
col1.metric("Active Case File", active_case if active_case != "-- Select Active Case --" else "Unlinked")
col2.metric("Recorded Findings", len(get_findings(active_case)) if active_case != "-- Select Active Case --" else "0")
col3.metric("Proxy Pool Size", f"{len(st.session_state.proxies)} IPs" if len(st.session_state.proxies) > 0 else "Direct IP")

st.markdown("---")

# Username Search tab (Just example logic)
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["👤 Username", "🖥️ Domain", "📧 Email", "📞 Phone", "🛠️ Dork", "📁 Vault"])

with tab1:
    target_username = st.text_input("Audit Username", value=st.session_state.derived_username_choice)
    if st.button("Start High-Precision Scan"):
        if active_case == "-- Select Active Case --":
            st.error("Pehle sidebar mein Case File select karo!")
        else:
            st.info("Scanning... (Check logs for progress)")
            # Baaki logic tumhara waisa hi rahega

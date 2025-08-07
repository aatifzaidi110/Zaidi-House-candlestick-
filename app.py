# === FILE: app.py ===
import streamlit as st
from strategy_center_ui import render_strategy_center  # ✅ updated
from glossary_content import render_glossary_tab
from send_alerts import render_big_money_watchlist

# === Page Setup ===
st.set_page_config(page_title="Candle Analysis & Big Money Tracker", layout="wide")
st.title("🕯️ Candle Analysis & Big Money Activity Tracker")

# === Streamlit Tabs ===
tab1, tab2, tab3 = st.tabs(["📊 Strategy Center", "📘 Glossary", "💸 Big Money Watchlist"])

with tab1:
    render_strategy_center()

with tab2:
    render_glossary_tab()

with tab3:
    render_big_money_watchlist()

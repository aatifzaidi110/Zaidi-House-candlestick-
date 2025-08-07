# === FILE: app.py ===
import streamlit as st
from strategy_center_ui import render_strategy_center  # ✅ updated
from glossary_content import render_glossary_tab

# === Page Setup ===
st.set_page_config(page_title="Candle Analysis & Big Money Tracker", layout="wide")
st.title("🕯️ Candle Analysis & Big Money Activity Tracker")

tabs = st.tabs(["🧠 Strategy Center", "📘 Glossary"])

with tabs[0]:
    render_strategy_center()  # ✅ updated

with tabs[1]:
    render_glossary_tab()

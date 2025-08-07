# === FILE: big_money_watchlist.py ===

import streamlit as st

# Dummy institutional activity data
def get_big_money_activity():
    return [
        {"ticker": "NVDA", "status": "Buy", "institution": "BlackRock", "amount": 9_200_000},
        {"ticker": "TSLA", "status": "Sell", "institution": "Citadel", "amount": 1_100_000},
        {"ticker": "AAPL", "status": "Hold", "institution": "Vanguard", "amount": 0}
    ]

def render_big_money_watchlist():
    st.header("📈 Big Money Watchlist")
    activity = get_big_money_activity()

    for item in activity:
        ticker = item["ticker"]
        status = item["status"]
        institution = item["institution"]
        amount = item["amount"]

        if status == "Buy":
            st.success(f"🟢 {ticker} — {institution} added ${amount / 1_000_000:.1f}M")
        elif status == "Sell":
            st.error(f"🔴 {ticker} — {institution} sold {amount:,} shares")
        else:
            st.warning(f"🔹 {ticker} — {institution} unchanged")

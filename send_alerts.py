# === FILE: send_alerts.py ===

import smtplib
from email.message import EmailMessage

# === Email Alert ===
def send_email_alert(ticker, message):
    try:
        sender = "your_email@gmail.com"  # 🔒 Replace with your sender
        password = "your_app_password"   # 🔒 Use app password (not your real password)
        recipient = "your_email@gmail.com"

        msg = EmailMessage()
        msg["Subject"] = f"🚨 Alert for {ticker}"
        msg["From"] = sender
        msg["To"] = recipient
        msg.set_content(message)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender, password)
            smtp.send_message(msg)
            print(f"✅ Email alert sent for {ticker}.")
    except Exception as e:
        print(f"❌ Failed to send email for {ticker}: {e}")


# === SMS Alert (Placeholder for integration e.g., Twilio) ===
def send_sms_alert(ticker, message):
    print(f"📲 SMS alert for {ticker}: {message}")


# === Institutional Alert Wrapper ===
def send_email_alert_with_condition(ticker, message, institution_value, enable_alerts=True):
    if enable_alerts and institution_value > 2_000_000:
        send_email_alert(ticker, message)


# === Big Money Watchlist Tab ===
def render_big_money_watchlist():
    import streamlit as st
    import pandas as pd

    st.markdown("## 📈 Big Money Watchlist")

    data = [
        {
            "ticker": "NVDA",
            "action": "Buy",
            "institution": "BlackRock",
            "value": 9_200_000,
            "reason": "13F institutional buy",
            "price": 127.53,
            "volume": 32100000,
            "rsi": 45,
            "note": "Scalp opportunity"
        },
        {
            "ticker": "TSLA",
            "action": "Sell",
            "institution": "Citadel",
            "shares": 1_100_000,
            "reason": "Profit booking",
            "price": 256.12,
            "volume": 28900000,
            "rsi": 61,
            "note": "Spoofing suspected, wait for confirmation"
        },
        {
            "ticker": "AAPL",
            "action": "Hold",
            "institution": "Vanguard",
            "reason": "No major movement",
            "price": 189.22,
            "volume": 35400000,
            "rsi": 52,
            "note": "Neutral, monitor only"
        }
    ]

    df = pd.DataFrame(data)

    # Filter and sort UI
    action_filter = st.multiselect("Filter by Action", options=["Buy", "Sell", "Hold"], default=["Buy", "Sell", "Hold"])
    sort_option = st.selectbox("Sort by", options=["ticker", "price", "volume", "rsi"], index=0)
    sort_asc = st.checkbox("Sort ascending", value=True)

    filtered_df = df[df["action"].isin(action_filter)].sort_values(by=sort_option, ascending=sort_asc)

    for _, row in filtered_df.iterrows():
        desc = f"💬 Reason: {row['reason']}\n💲 Price: ${row['price']:.2f} | 📊 Volume: {row['volume']:,} | 📈 RSI: {row['rsi']}\n📝 Note: {row['note']}"

        if row["action"] == "Buy":
            st.success(f"🟢 {row['ticker']} — {row['institution']} added ${row['value']:,}\n{desc}")
        elif row["action"] == "Sell":
            st.error(f"🔴 {row['ticker']} — {row['institution']} sold {row['shares']:,} shares\n{desc}")
        else:
            st.warning(f"🟡 {row['ticker']} — {row['institution']} unchanged\n{desc}")

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

    st.markdown("## 📈 Big Money Watchlist")

    data = [
        {"ticker": "NVDA", "action": "Buy", "institution": "BlackRock", "value": 9_200_000},
        {"ticker": "TSLA", "action": "Sell", "institution": "Citadel", "shares": 1_100_000},
        {"ticker": "AAPL", "action": "Hold", "institution": "Vanguard"}
    ]

    for row in data:
        if row["action"] == "Buy":
            st.success(f"🟢 {row['ticker']} — {row['institution']} added ${row['value']:,}")
        elif row["action"] == "Sell":
            st.error(f"🔴 {row['ticker']} — {row['institution']} sold {row['shares']:,} shares")
        else:
            st.warning(f"🟡 {row['ticker']} — {row['institution']} unchanged")

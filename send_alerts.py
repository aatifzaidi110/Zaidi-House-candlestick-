# === FILE: send_alerts.py ===

import smtplib
from email.message import EmailMessage
import streamlit as st
import pandas as pd
import datetime

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


# === Spoofing Alert Logger ===
def log_spoofing_event(ticker, confidence):
    with open("spoofing_log.csv", "a") as f:
        f.write(f"{datetime.datetime.now()}, {ticker}, {confidence}\n")


# === Big Money Watchlist Tab ===
def render_big_money_watchlist():
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
            "macd": 1.32,
            "macd_hist": 0.82,
            "ema_50": 126.87,
            "ema_9": 126.05,
            "ema_20": 126.55,
            "obv": 12_340_000,
            "bb_width": 2.1,
            "note": "Scalp opportunity",
            "spoofing": False,
            "spoof_confidence": 0.0,
            "indicator_score": 0.85
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
            "macd": -0.56,
            "macd_hist": -0.22,
            "ema_50": 259.41,
            "ema_9": 257.20,
            "ema_20": 258.05,
            "obv": -1_800_000,
            "bb_width": 3.5,
            "note": "Spoofing suspected, wait for confirmation",
            "spoofing": True,
            "spoof_confidence": 0.83,
            "indicator_score": 0.65
        },
        {
            "ticker": "AAPL",
            "action": "Hold",
            "institution": "Vanguard",
            "reason": "No major movement",
            "price": 189.22,
            "volume": 35400000,
            "rsi": 52,
            "macd": 0.12,
            "macd_hist": 0.08,
            "ema_50": 188.95,
            "ema_9": 189.30,
            "ema_20": 189.10,
            "obv": 800_000,
            "bb_width": 1.6,
            "note": "Neutral, monitor only",
            "spoofing": False,
            "spoof_confidence": 0.0,
            "indicator_score": 0.55
        }
    ]

    df = pd.DataFrame(data)

    # Filter and sort UI
    action_filter = st.multiselect("Filter by Action", options=["Buy", "Sell", "Hold"], default=["Buy", "Sell", "Hold"])
    spoof_filter = st.checkbox("Only Show Spoofing Detected", value=False)
    confidence_threshold = st.slider("Minimum Indicator Confidence (%)", 0, 100, 70)
    sort_option = st.selectbox("Sort by", options=["ticker", "price", "volume", "rsi", "spoof_confidence", "indicator_score"], index=0)
    sort_asc = st.checkbox("Sort ascending", value=True)

    filtered_df = df[df["action"].isin(action_filter)]
    if spoof_filter:
        filtered_df = filtered_df[filtered_df["spoofing"] == True]
    filtered_df = filtered_df[filtered_df["indicator_score"] >= confidence_threshold / 100]
    filtered_df = filtered_df.sort_values(by=sort_option, ascending=sort_asc)

    for _, row in filtered_df.iterrows():
        spoof_info = ""

        if row["spoofing"]:
            spoof_info = f"\n🔍 Spoofing Confidence: {row['spoof_confidence'] * 100:.0f}%"
            spoof_info += "\n⚠️ Note: Spoofing suspected, wait for confirmation"
            spoof_info += "\n🧭 Next Step: Monitor order book — confirm if volume drops after rapid price rise."
            log_spoofing_event(row['ticker'], row['spoof_confidence'])

        indicators_used = (
            f"🧪 Indicators:\n"
            f"• Price > EMA 9: {row['price'] > row['ema_9']}\n"
            f"• Price > EMA 20: {row['price'] > row['ema_20']}\n"
            f"• RSI: {row['rsi']}\n"
            f"• MACD: {row['macd']}\n"
            f"• MACD Histogram: {row['macd_hist']}\n"
            f"• OBV: {row['obv']}\n"
            f"• BB Width: {row['bb_width']:.2f}"
        )

        desc = (
            f"💬 Reason: {row['reason']}\n"
            f"💲 Price: ${row['price']:.2f} | 📊 Volume: {row['volume']:,} | 📈 RSI: {row['rsi']}\n"
            f"📊 Indicator Confidence: {row['indicator_score'] * 100:.0f}%\n"
            f"📝 Note: {row['note']}{spoof_info}\n"
            f"{indicators_used}"
        )

        if row["action"] == "Buy":
            st.success(f"🟢 {row['ticker']} — {row['institution']} added ${row['value']:,}\n{desc}")
        elif row["action"] == "Sell":
            st.error(f"🔴 {row['ticker']} — {row['institution']} sold {row['shares']:,} shares\n{desc}")
        else:
            st.warning(f"🟡 {row['ticker']} — {row['institution']} unchanged\n{desc}")


# === Spoofing History Tab ===
def render_spoofing_log():
    st.markdown("## 📜 Spoofing Alert History")
    try:
        df = pd.read_csv("spoofing_log.csv", names=["Time", "Ticker", "Confidence"])
        df["Time"] = pd.to_datetime(df["Time"])
        df = df.sort_values(by="Time", ascending=False)
        st.dataframe(df)
    except FileNotFoundError:
        st.info("No spoofing alerts logged yet.")

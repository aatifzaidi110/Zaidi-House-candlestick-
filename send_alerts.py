# === FILE: send_alerts.py ===

import smtplib
from email.message import EmailMessage
import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import plotly.graph_objects as go

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


# === Entry/Exit Logging ===
def log_trade_signal(ticker, entry, target, stop, confidence):
    with open("trade_signals_log.csv", "a") as f:
        f.write(f"{datetime.datetime.now()},{ticker},{entry},{target},{stop},{confidence}\n")


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
            "ema_50": 126.87,
            "iv": 32,
            "oi": 1_200_000,
            "obv": 500_000,
            "bb_position": 0.6,
            "note": "Scalp opportunity",
            "spoofing": False,
            "spoof_confidence": 0.0,
            "indicator_score": 0.85,
            "entry": 127.0,
            "target": 132.0,
            "stop": 125.5
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
            "ema_50": 259.41,
            "iv": 50,
            "oi": 900_000,
            "obv": -100_000,
            "bb_position": 0.9,
            "note": "Spoofing suspected, wait for confirmation",
            "spoofing": True,
            "spoof_confidence": 0.83,
            "indicator_score": 0.65,
            "entry": 254.5,
            "target": 245.0,
            "stop": 261.0
        }
    ]

    df = pd.DataFrame(data)

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
            spoof_info += f"\n🔍 Spoofing Confidence: {row['spoof_confidence'] * 100:.0f}%"
            spoof_info += "\n⚠️ Note: Spoofing suspected, wait for confirmation"
            spoof_info += "\n🧭 Next Step: Monitor order book — confirm if volume drops after rapid price rise."
            log_spoofing_event(row['ticker'], row['spoof_confidence'])

        indicators_used = (
            f"🧪 Indicators:\n"
            f"• RSI: {row['rsi']} (⚠️ >70 = Overbought, <30 = Oversold)\n"
            f"• MACD: {row['macd']} (📈 Rising = Bullish)\n"
            f"• EMA-50: {row['ema_50']}\n"
            f"• IV: {row['iv']} (⚠️ High IV = Risky options)\n"
            f"• OI: {row['oi']} (📊 High OI = Institutional Interest)\n"
            f"• BB Pos: {row['bb_position']} (0.5 = middle, >0.9 = breakout zone)"
        )

        desc = (
            f"💬 Reason: {row['reason']}\n"
            f"💲 Price: ${row['price']:.2f} | 📊 Volume: {row['volume']:,} | 📈 RSI: {row['rsi']}\n"
            f"📊 Indicator Confidence: {row['indicator_score'] * 100:.0f}%\n"
            f"📝 Note: {row['note']}{spoof_info}\n"
            f"{indicators_used}\n\n"
            f"🎯 Trade Planner: Entry ${row['entry']}, Target ${row['target']}, Stop ${row['stop']}"
        )

        log_trade_signal(row['ticker'], row['entry'], row['target'], row['stop'], row['indicator_score'])

        radar = go.Figure()
        radar.add_trace(go.Barpolar(
            r=[row['rsi'], row['macd'], row['iv'], row['oi'], row['bb_position'] * 100],
            theta=['RSI', 'MACD', 'IV', 'OI', 'BB Pos'],
            marker_color=['blue', 'orange', 'purple', 'green', 'red'],
            marker_line_color="black",
            marker_line_width=1.5,
            opacity=0.8
        ))
        radar.update_layout(title=f"📊 Confidence Breakdown: {row['ticker']}", polar=dict(radialaxis=dict(visible=True)))
        st.plotly_chart(radar, use_container_width=True)

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

# === FILE: strategy_center_ui.py ===

import streamlit as st
import yfinance as yf
try:
    import mplfinance as mpf
    mpf_available = True
except ImportError:
    mpf_available = False
import matplotlib.pyplot as plt
from strategy_engine import generate_strategy
from indicator_calculator import compute_indicators
from signal_detector import detect_signal_type
from news_blocker import should_block_trade
from economic_calendar import should_block_macro_trades
from backtest_analyzer import get_win_rate

try:
    import pandas_ta as ta
    ta_available = True
except ImportError:
    ta_available = False

# === Candlestick Pattern Detection ===
def detect_candlestick_patterns(df):
    if not ta_available:
        return []
    patterns = []
    df = df.copy()
    df.ta.cdl_pattern(name='all', append=True)
    for col in df.columns:
        if col.startswith("CDL") and df[col].iloc[-1] != 0:
            patterns.append(col.replace("CDL_", ""))
    return patterns

# === Mock Order Book Spoofing Detection ===
def detect_spoofing_activity(df):
    spoof_alerts = []
    last_volume = df["Volume"].iloc[-1]
    mean_volume = df["Volume"].mean()
    if last_volume > 2 * mean_volume:
        spoof_alerts.append({
            "institution": "Unknown Large Entity",
            "order_size": f"{int(last_volume)} shares",
            "action": "Spoofing Alert: Large volume spike detected. Wait for confirmation."
        })
    return spoof_alerts

def render_strategy_center():
    st.header("🧠 Strategy Center — Big Money Activity")

    ticker = st.text_input("Ticker", value="ES=F")

    price = None
    if ticker:
        try:
            df_live = yf.Ticker(ticker).history(period="1d", interval="1m")
            if not df_live.empty:
                price = round(df_live["Close"].iloc[-1], 2)
                st.success(f"📈 Current Price: ${price}")
            else:
                st.warning("⚠️ No price data available.")
        except Exception as e:
            st.error(f"Error fetching price: {e}")

    if st.button("🔍 Analyze Ticker"):
        if price is None:
            st.error("Cannot analyze without valid price.")
        else:
            indicators = compute_indicators(ticker)
            indicators["InstitutionalBuyPrice"] = price * 0.96

            blocked_earnings, msg1 = should_block_trade(ticker)
            blocked_macro, msg2 = should_block_macro_trades()

            if blocked_earnings:
                st.warning(msg1)
            if blocked_macro:
                st.warning(msg2)

            detected_signal, confidence = detect_signal_type(price, indicators)
            st.info(f"🧠 Auto-detected Signal: {detected_signal}  |  Confidence Score: {confidence}%")

            result = generate_strategy(detected_signal, ticker, price, indicators)
            st.success(f"Strategy: {result['strategy']}")
            st.write(f"📌 Why: {result['explanation']}")

            volume_threshold = 1.5 * df_live["Volume"].mean()
            current_volume = df_live["Volume"].iloc[-1]
            next_step = result["next_step"]
            if "volume" in next_step.lower():
                next_step += f" (Current: {int(current_volume)}, Target: {int(volume_threshold)})"
            st.write(f"🔜 Next Step: {next_step}")

            st.code(f"Triggered by: {result['signal_type']} at price ${result['price']}")

            win_rate = get_win_rate(detected_signal)
            st.info(f"📊 Historical Win Rate for {detected_signal}: {win_rate}%")

            # === Historical Chart + Indicators ===
            if mpf_available:
                try:
                    df = yf.Ticker(ticker).history(period="5d", interval="15m")
                    if not df.empty:
                        df["EMA50"] = df["Close"].ewm(span=50).mean()
                        df["VWAP"] = (df["Volume"] * (df["High"] + df["Low"] + df["Close"]) / 3).cumsum() / df["Volume"].cumsum()

                        apds = [
                            mpf.make_addplot(df["EMA50"], color="blue", width=1),
                            mpf.make_addplot(df["VWAP"], color="orange", width=1)
                        ]

                        st.subheader("📈 Historical Chart with EMA & VWAP")
                        fig, ax = mpf.plot(df, type="candle", style="yahoo", addplot=apds, volume=True, returnfig=True)
                        st.pyplot(fig)

                        if ta_available:
                            patterns = detect_candlestick_patterns(df)
                            if patterns:
                                st.warning(f"🕯️ Detected Candlestick Pattern(s): {', '.join(patterns)}")
                                st.caption("Pattern-based suggestion: Confirm with volume or MACD alignment.")
                        else:
                            st.info("ℹ️ Candlestick pattern detection not available. Install `pandas-ta` to enable.")
                except Exception as e:
                    st.warning(f"⚠️ Could not render chart or patterns: {e}")
            else:
                st.warning("⚠️ `mplfinance` not installed. Skipping candlestick chart rendering.")

            # === Spoofing Alerts ===
            st.subheader("🚨 Spoofing & Order Book Alerts")
            spoofing_data = detect_spoofing_activity(df_live)
            if spoofing_data:
                for spoof in spoofing_data:
                    st.error(f"⚠️ {spoof['action']}\n👤 {spoof['institution']} placed approx. {spoof['order_size']}")
            else:
                st.success("✅ No spoofing activity detected in recent data.")

            # === Indicators Used ===
            st.markdown("---")
            st.subheader("📊 Indicators Used")
            for k, v in indicators.items():
                st.write(f"{k}: {v}")

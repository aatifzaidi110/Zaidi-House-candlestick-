# === FILE: indicator_calculator.py ===

import yfinance as yf
import pandas as pd
import ta

def compute_indicators(ticker):
    try:
        df = yf.Ticker(ticker).history(period="5d", interval="5m")
        if df.empty:
            return {}

        df.dropna(inplace=True)

        # Compute indicators
        df["EMA_50"] = ta.trend.ema_indicator(df["Close"], window=50).fillna(method="bfill")
        df["VWAP"] = ta.volume.volume_weighted_average_price(
            high=df["High"], low=df["Low"], close=df["Close"], volume=df["Volume"]
        ).fillna(method="bfill")
        df["ATR"] = ta.volatility.average_true_range(df["High"], df["Low"], df["Close"], window=14).fillna(method="bfill")

        latest = df.iloc[-1]
        return {
            "EMA_50": round(latest["EMA_50"], 2),
            "VWAP": round(latest["VWAP"], 2),
            "ATR": round(latest["ATR"], 2),
            "Support": round(df["Low"].rolling(window=30).min().iloc[-1], 2),
            "Resistance": round(df["High"].rolling(window=30).max().iloc[-1], 2)
        }
    except Exception as e:
        print(f"Error computing indicators for {ticker}: {e}")
        return {}

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
# === FILE: indicator_utils.py ===

# indicator_utils.py

# ... other functions you have in this file

def is_overbought(rsi_value, overbought_threshold=70):
    """
    Checks if a given RSI value indicates an overbought condition.
    
    Args:
        rsi_value (float): The current RSI value.
        overbought_threshold (int): The threshold above which an asset is considered overbought.
    
    Returns:
        bool: True if overbought, False otherwise.
    """
    return rsi_value > overbought_threshold

def is_oversold(rsi_value, oversold_threshold=30):
    """
    Checks if a given RSI value indicates an oversold condition.
    
    Args:
        rsi_value (float): The current RSI value.
        oversold_threshold (int): The threshold below which an asset is considered oversold.
    
    Returns:
        bool: True if oversold, False otherwise.
    """
    return rsi_value < oversold_threshold

# ... other functions you have in this file

def calculate_risk_reward(entry, atr, multiplier=2):
    """Estimate stop loss and target using ATR."""
    stop = entry - atr
    target = entry + atr * multiplier
    rr = (target - entry) / (entry - stop)
    return {
        "stop": round(stop, 2),
        "target": round(target, 2),
        "risk_reward": round(rr, 2)
    }

def price_above_ma(price, ma):
    return price > ma

def price_below_ma(price, ma):
    return price < ma

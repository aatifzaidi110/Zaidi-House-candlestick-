# === FILE: signal_detector.py ===

import pandas as pd
import ta


def detect_signal_type(price, indicators):
    """
    Returns the most relevant signal type and a confidence score (0-100).
    
    Criteria:
    - MACD crossover + RSI alignment
    - Price > EMA50
    - Near support or resistance
    - VWAP position
    """
    signal = None
    score = 0

    rsi = indicators.get("RSI")
    macd = indicators.get("MACD")
    macd_signal = indicators.get("MACD_SIGNAL")
    ema = indicators.get("EMA_50")
    vwap = indicators.get("VWAP")
    atr = indicators.get("ATR")
    support = indicators.get("Support")
    resistance = indicators.get("Resistance")

    if macd and macd_signal:
        if macd > macd_signal and rsi and rsi > 50:
            score += 40  # bullish confirmation
            if price > ema:
                score += 20
            if price > vwap:
                score += 10
            if abs(price - support) / support < 0.02:
                score += 10
            signal = "COT_NET_LONG_SURGE"
        elif macd < macd_signal and rsi and rsi < 50:
            score += 40  # bearish confirmation
            if price < ema:
                score += 20
            if price < vwap:
                score += 10
            if abs(price - resistance) / resistance < 0.02:
                score += 10
            signal = "COT_NET_SHORT_SURGE"

    # Fallback signal types if no MACD/RSI confirmation
    if not signal and price and support and price <= support * 1.01:
        signal = "ORDER_BOOK_BUY_WALL"
        score = 50
    elif not signal and price and resistance and price >= resistance * 0.99:
        signal = "ORDER_BOOK_SELL_WALL"
        score = 50

    # Default fallback
    if not signal:
        signal = "13F_BULLISH_POSITION"
        score = 30

    return signal, score

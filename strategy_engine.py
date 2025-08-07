from thirteenf_parser import get_top_13f_investors
from indicator_utils import (
    is_overbought,
    calculate_risk_reward,
    price_above_ma
)
from price_logic import (
    is_near_level,
    near_institutional_buy_level
)

def generate_strategy(signal_type, ticker, price, indicators=None):
    strategy = "HOLD"
    explanation = "No strong signal."
    next_step = "Re-scan in next session."

    ema50 = indicators.get("EMA_50") if indicators else None
    atr = indicators.get("ATR", 10)
    vwap = indicators.get("VWAP")
    institutional_price = indicators.get("InstitutionalBuyPrice", price * 0.95)  # Optional

    if signal_type == "COT_NET_LONG_SURGE":
        if ema50 and price_above_ma(price, ema50):
            rr = calculate_risk_reward(price, atr)
            if rr["risk_reward"] >= 2:
                strategy = "BUY (Swing Trade)"
                explanation = f"COT surge + price > EMA50 (${ema50}) + R:R = {rr['risk_reward']:.2f}"
                next_step = f"Enter at ${price}, Stop: ${rr['stop']}, Target: ${rr['target']}"
            else:
                strategy = "WAIT"
                explanation = f"Risk/Reward too low: {rr['risk_reward']:.2f}"
                next_step = "Wait for better entry"
        else:
            explanation = "COT surge detected but no bullish confirmation (price below EMA50)"

    elif signal_type == "ORDER_BOOK_SELL_WALL":
        resistance = indicators.get("Resistance", price * 1.02)
        if is_near_level(price, resistance):
            strategy = "WAIT or SHORT"
            explanation = f"Sell wall detected. Price near resistance at ${resistance}"
            next_step = "Short if rejection confirmed by MACD or RSI"
        else:
            explanation = f"Sell wall detected but price is not near resistance (${resistance})"
            next_step = "Monitor for test or breakout"

    elif signal_type == "ORDER_BOOK_BUY_WALL":
        support = indicators.get("Support", price * 0.98)
        if is_near_level(price, support):
            strategy = "BUY SCALP"
            explanation = f"Buy wall detected near support (${support})"
            next_step = "Enter scalp trade if volume confirms"
        else:
            strategy = "WAIT"
            explanation = "Buy wall detected but price far from support"

    elif signal_type == "13F_BULLISH_POSITION":
        investors = get_top_13f_investors(ticker)
        if investors:
            investor_details = "; ".join(
                [f"{i['name']} bought {i['shares']:,} shares (${i['value'] / 1e6:.1f}M)" for i in investors]
            )
            explanation = f"13F filings show bullish positions by: {investor_details}."

            if near_institutional_buy_level(price, institutional_price):
                explanation += f" Price near institutional buy level (${institutional_price})."
                strategy = "BUY (Position Trade)"
                next_step = "Buy near this zone with tight stop"
            else:
                strategy = "WAIT"
                explanation += f" But price (${price}) is far from known institutional buy level (${institutional_price})."
                next_step = "Watch for dip"
        else:
            explanation = f"13F filings show a new institutional position in {ticker}."

    elif signal_type == "COT_NET_SHORT_SURGE":
        support = indicators.get("Support", price * 0.98)
        if price < support:
            strategy = "SELL or BUY PUT"
            explanation = f"Breakdown below support (${support}) + COT short surge"
            next_step = "Enter short on breakdown confirmation"
        else:
            explanation = f"Short surge detected but price still above support (${support})"
            next_step = "Wait for breakdown"

    return {
        "strategy": strategy,
        "explanation": explanation,
        "next_step": next_step,
        "price": price,
        "ticker": ticker,
        "signal_type": signal_type
    }

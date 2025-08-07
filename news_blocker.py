# === FILE: news_blocker.py ===

import yfinance as yf
import datetime


def is_earnings_soon(ticker, days=3):
    try:
        ticker_obj = yf.Ticker(ticker)
        cal = ticker_obj.calendar
        if cal is not None and "Earnings Date" in cal.index:
            ed = cal.loc["Earnings Date"]
            if not ed.empty:
                earnings_date = ed[0] if isinstance(ed[0], datetime.datetime) else ed[0].to_pydatetime()
                diff = (earnings_date - datetime.datetime.now()).days
                return diff >= 0 and diff <= days
    except Exception as e:
        print(f"Error checking earnings: {e}")
    return False


def should_block_trade(ticker):
    if is_earnings_soon(ticker):
        return True, "⏰ Earnings report is coming up — avoid trading near earnings!"
    # Placeholder for news scan logic
    return False, ""

# === FILE: options_fetcher.py ===

import yfinance as yf
import datetime

def fetch_option_trade_ideas(ticker, days_out=14):
    try:
        stock = yf.Ticker(ticker)
        current_price = stock.history(period="1d")["Close"].iloc[-1]

        expiries = stock.options
        if not expiries:
            return []

        # Choose expiry 2 weeks to 1 month out
        target_expiry = next((d for d in expiries if is_valid_expiry(d, days_out)), expiries[-1])
        chain = stock.option_chain(target_expiry)

        def analyze_options(df, option_type):
            ideas = []
            for i, row in df.iterrows():
                if row.impliedVolatility is None or row.impliedVolatility == 0:
                    continue
                rr_ratio = round((row.strike - current_price) / (current_price * 0.03), 2)
                delta = round(abs(row.inTheMoney), 2)
                ideas.append({
                    "type": option_type,
                    "strike": row.strike,
                    "expiry": target_expiry,
                    "delta": row.impliedVolatility,
                    "iv": round(row.impliedVolatility * 100, 2),
                    "target": round(current_price + (current_price * 0.03), 2),
                    "stop": round(current_price - (current_price * 0.02), 2),
                    "rr": rr_ratio
                })
            return sorted(ideas, key=lambda x: -x["delta"])[:1]

        call_ideas = analyze_options(chain.calls, "Call")
        put_ideas = analyze_options(chain.puts, "Put")

        return call_ideas + put_ideas

    except Exception as e:
        print(f"Option fetch error for {ticker}: {e}")
        return []

def is_valid_expiry(expiry_str, min_days):
    try:
        exp_date = datetime.datetime.strptime(expiry_str, "%Y-%m-%d").date()
        today = datetime.date.today()
        delta = (exp_date - today).days
        return delta >= min_days
    except Exception:
        return False

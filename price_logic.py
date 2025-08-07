# === FILE: price_logic.py ===

def is_near_level(price, level, tolerance=0.02):
    """Return True if price is within tolerance % of level."""
    return abs(price - level) / level < tolerance

def validate_support_breakdown(price, support):
    return price < support

def validate_resistance_breakout(price, resistance):
    return price > resistance

def near_institutional_buy_level(price, institutional_price, threshold=0.05):
    return abs(price - institutional_price) / institutional_price <= threshold

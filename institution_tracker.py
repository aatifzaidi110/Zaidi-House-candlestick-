def is_big_institutional_trade(ticker, threshold=1_000_000):
    investors = get_top_13f_investors(ticker)
    for inv in investors:
        if inv["value"] > threshold:
            return inv["name"], inv["shares"], inv["value"]
    return None, None, None

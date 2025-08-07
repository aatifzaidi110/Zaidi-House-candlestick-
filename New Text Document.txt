# === FILE: backtest_analyzer.py ===

import json
import os

BACKTEST_FILE = "signal_performance.json"

def load_backtest_data():
    if os.path.exists(BACKTEST_FILE):
        with open(BACKTEST_FILE, "r") as f:
            return json.load(f)
    return {}

def save_backtest_data(data):
    with open(BACKTEST_FILE, "w") as f:
        json.dump(data, f, indent=2)

def log_signal_result(signal_type, result):
    """
    Log signal result as 'win' or 'loss'.
    result: 'win' or 'loss'
    """
    data = load_backtest_data()
    if signal_type not in data:
        data[signal_type] = {"win": 0, "loss": 0}
    
    if result == "win":
        data[signal_type]["win"] += 1
    elif result == "loss":
        data[signal_type]["loss"] += 1

    save_backtest_data(data)

def get_win_rate(signal_type):
    data = load_backtest_data()
    stats = data.get(signal_type)
    if not stats:
        return 0.0
    total = stats["win"] + stats["loss"]
    if total == 0:
        return 0.0
    return round(stats["win"] / total * 100, 2)

def get_all_win_rates():
    data = load_backtest_data()
    rates = {}
    for sig, stats in data.items():
        total = stats["win"] + stats["loss"]
        if total:
            rates[sig] = round(stats["win"] / total * 100, 2)
    return rates

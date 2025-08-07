# === FILE: test_app.py ===

import importlib

REQUIRED_MODULES = [
    'streamlit', 'yfinance', 'pandas', 'matplotlib', 'mplfinance',
    'ta', 'pandas_ta', 'sec_edgar_downloader', 'schedule',
    'indicator_calculator', 'indicator_utils', 'signal_detector',
    'strategy_engine', 'options_fetcher', 'send_alerts',
    'news_blocker', 'economic_calendar', 'backtest_analyzer',
    'thirteenf_parser', 'glossary_content'
]

print("🔍 Verifying required modules...")

for module in REQUIRED_MODULES:
    try:
        importlib.import_module(module)
        print(f"✅ {module} loaded successfully")
    except ModuleNotFoundError:
        print(f"❌ {module} NOT FOUND")
    except Exception as e:
        print(f"⚠️ Error loading {module}: {e}")

print("\n✔️ Test complete.")

# === FILE: economic_calendar.py ===

import requests
import datetime

# This demo version uses Trading Economics' free endpoint
# You can use other APIs like FRED, FinancialModelingPrep, etc.

def get_upcoming_events(days_ahead=5):
    try:
        today = datetime.datetime.utcnow().date()
        future = today + datetime.timedelta(days=days_ahead)
        url = f"https://calendar.tradingeconomics.com/calendar?start={today}&end={future}"
        return f"⚠️ Events coming up between {today} and {future}: Check calendar manually. (Upgrade needed for full data access)"
    except Exception as e:
        return f"⚠️ Could not fetch calendar events: {e}"


def should_block_macro_trades():
    # Placeholder logic to warn manually — recommend upgrade to full API
    return True, "⚠️ Major economic events may be upcoming. Check FOMC/CPI/Jobs calendar."

# Usage example:
# msg = get_upcoming_events()

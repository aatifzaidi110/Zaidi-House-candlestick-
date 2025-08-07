# thirteenf_parser.py

from sec_edgar_downloader import Downloader
import os
import pandas as pd
import glob
from bs4 import BeautifulSoup

def get_top_13f_investors(ticker, top_n=3):
    dl = Downloader("your_email@example.com", "edgar_data")

    
    cik_lookup = {
        "NVDA": "0001045810",
        "AAPL": "0000320193",
        "MSFT": "0000789019",
        "GOOG": "0001652044"
        # Add more tickers here
    }
    cik = cik_lookup.get(ticker.upper())
    if not cik:
        return []

    # Download recent filings
    dl.get("13F-HR", cik, after="2025-01-01")
    
    folder = f"edgar_data/sec-edgar-filings/13F-HR/{cik}/"
    files = sorted(glob.glob(f"{folder}/**/*.html", recursive=True), reverse=True)
    
    if not files:
        return []

    with open(files[0], "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    table = soup.find("table")
    if not table:
        return []

    rows = table.find_all("tr")[1:]  # Skip header

    matches = []
    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 4:
            name_of_issuer = cols[0].text.strip().upper()
            shares = cols[3].text.strip().replace(",", "")
            value = cols[2].text.strip().replace(",", "").replace("$", "")

            if ticker.upper() in name_of_issuer:
                matches.append({
                    "name": os.path.basename(files[0]).split("-")[0],
                    "shares": int(shares) if shares.isdigit() else 0,
                    "value": int(value) * 1000 if value.isdigit() else 0
                })

    return matches[:top_n]

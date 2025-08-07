# === FILE: glossary_content.py ===

import streamlit as st

GLOSSARY_MARKDOWN = """
### Glossary of Terms

**ES=F** — E-mini S&P 500 Futures. Represents a portion of the S&P 500 futures contract.

**CL=F** — Crude Oil Futures. Used to trade oil based on expected price.

**GC=F** — Gold Futures. Traded on the COMEX exchange.

**BTCUSDT** — Bitcoin Tether trading pair, often used for crypto analysis.

**RSI (Relative Strength Index)** — Momentum oscillator that measures the speed and change of price movements (0–100).

**MACD (Moving Average Convergence Divergence)** — Trend-following indicator showing the relationship between two EMAs (usually 12 and 26). The MACD line is calculated by subtracting the 26-period EMA from the 12-period EMA. A 9-period EMA of the MACD line, called the **signal line**, is plotted on top. 

🔁 *MACD Signal Interpretation:*
- **Bullish Crossover**: MACD line crosses above the signal line → possible **buy** signal.
- **Bearish Crossover**: MACD line crosses below the signal line → possible **sell** signal.

**SMA (Simple Moving Average)** — A basic average of prices over a set period. Each data point is equally weighted. Slower to react to price changes.

**EMA (Exponential Moving Average)** — A moving average that gives more weight to recent prices, making it more responsive to price changes.

**VWAP (Volume Weighted Average Price)** — Used by institutions to judge price fairness throughout the trading day. It averages price weighted by volume.

**ATR (Average True Range)** — A measure of volatility. Often used to set stop-loss or target levels.

**Bollinger Bands** — Volatility bands placed above and below a moving average. Price breaking lower band + RSI < 30 may indicate reversal.

**MFI (Money Flow Index)** — Combines price and volume to detect institutional inflow/outflow. A surge near support may indicate accumulation.

**Put/Call Ratio (PCR)** — Ratio of traded put options to call options. High PCR (> 1.2) is bearish; low (< 0.7) may indicate bullish reversal.

**Volume Profile (Visible Range)** — Displays traded volume at each price level. Useful to identify institutional accumulation zones.

**CCI (Commodity Channel Index)** — Measures price deviation from average. Pro futures traders use it to find trend reversals or continuations.

**COT (Commitments of Traders Report)** — Published weekly by the CFTC, showing positions held by commercial, non-commercial, and retail traders.

**13F Filings** — Quarterly reports filed by institutional investment managers (e.g., hedge funds) disclosing their holdings. Used to identify large investments by firms like BlackRock, Vanguard, Renaissance Technologies, etc.

**Order Book** — A real-time list of buy (bid) and sell (ask) orders for a security.

**Buy Wall / Sell Wall** — Large clusters of limit orders in the order book that may act as support (buy wall) or resistance (sell wall).

**Spoofing** — Illegal practice of placing large fake orders to manipulate market perception.

**Net Long / Short Position** — Indicates whether institutions are overall bullish (long) or bearish (short).

**Swing Trade** — A short-to-medium-term trade strategy, typically lasting a few days to weeks.

**Scalping** — A very short-term strategy involving small, quick trades for small profits.

**Delta (Options Greek)** — Measures how much an option's price will change for every $1 move in the underlying asset.

**IV (Implied Volatility)** — Market forecast of a likely movement in a security’s price.

**Open Interest (OI)** — Total number of outstanding options/futures contracts.

**Support & Resistance** — Key price levels where a stock historically finds buying (support) or selling (resistance) pressure.

**ETF (Exchange-Traded Fund)** — A marketable security that tracks an index, commodity, or asset and is traded like a stock.

**/ES** — ThinkorSwim futures symbol for E-mini S&P 500.
**SPY** — ETF equivalent for E-mini S&P 500.

**/NQ** — ThinkorSwim futures symbol for Nasdaq 100.
**QQQ** — ETF equivalent for Nasdaq 100.

**/YM** — ThinkorSwim futures symbol for Dow Jones.
**DIA** — ETF equivalent for Dow Jones.

**/CL** — ThinkorSwim futures symbol for Crude Oil.
**USO** — ETF equivalent for Crude Oil.

**/GC** — ThinkorSwim futures symbol for Gold.
**GLD** — ETF equivalent for Gold.

**/SI** — ThinkorSwim futures symbol for Silver.
**SLV** — ETF equivalent for Silver.

**/NG** — ThinkorSwim futures symbol for Natural Gas.
**UNG** — ETF equivalent for Natural Gas.

**/ZC** — ThinkorSwim futures symbol for Corn.
**CORN** — ETF equivalent for Corn.

**/ZS** — ThinkorSwim futures symbol for Soybeans.
**SOYB** — ETF equivalent for Soybeans.

**/BTC, /BRR** — ThinkorSwim futures symbols for Bitcoin futures.
**BITO** — ETF equivalent for Bitcoin futures.
----
**Signal Types**

* **COT_NET_LONG_SURGE:** A bullish signal from the Commitments of Traders (COT) report, indicating a significant increase in net long positions by institutional traders.
* **COT_NET_SHORT_SURGE:** A bearish signal from the COT report, indicating a significant increase in net short positions by institutional traders.
* **ORDER_BOOK_BUY_WALL:** A bullish signal indicating a large concentration of buy orders at a specific price, suggesting a strong support level.
* **ORDER_BOOK_SELL_WALL:** A bearish signal indicating a large concentration of sell orders at a specific price, suggesting a strong resistance level.
* **13F_BULLISH_POSITION:** A bullish signal based on 13F filings, showing that institutional investors are taking or increasing a long position.


---

### ✅ ETF Equivalents for Futures (ThinkorSwim Compatible)
| Futures Contract | ThinkorSwim Futures Symbol | ETF Equivalent | ETF Symbol | Notes |
|------------------|-----------------------------|----------------|-------------|-------|
| E-mini S&P 500   | /ES                       | SPDR S&P 500 ETF | SPY     | Most liquid U.S. index ETF |
| Nasdaq 100       | /NQ                       | Invesco QQQ ETF | QQQ     | Tech-heavy exposure |
| Dow Jones        | /YM                       | SPDR Dow Jones Industrial | DIA     | Blue-chip industrials |
| Crude Oil (WTI)  | /CL                       | United States Oil Fund | USO     | Short-term oil exposure |
| Gold             | /GC                       | SPDR Gold Shares | GLD     | Physical gold exposure |
| Silver           | /SI                       | iShares Silver Trust | SLV     | Physical silver exposure |
| Natural Gas      | /NG                       | United States Natural Gas | UNG     | Volatile ETF – high IV |
| Corn             | /ZC                       | Teucrium Corn Fund | CORN    | Tracks corn futures contracts |
| Soybeans         | /ZS                       | Teucrium Soybean Fund | SOYB    | Tracks soybean futures |
| Bitcoin Futures  | /BTC, /BRR              | ProShares Bitcoin Strategy | BITO    | Holds CME Bitcoin Futures |

---

### 🔍 Tips for Using These ETFs in Trading
- Use SPY/QQQ/DIA for equity index exposure when /ES, /NQ, or /YM signals fire.
- GLD/SLV for precious metal moves when /GC, /SI trigger alerts (e.g., COT report bullish gold).
- USO/UNG mirror oil/nat gas futures moves—good for retail-friendly options trading.
- CORN/SOYB for agricultural trends spotted from COT or USDA alerts.
- BITO is your retail-accessible path to Bitcoin futures movement.

-------
🔧 Suggested Additional Indicators to Add:
1. **Bollinger Bands**
Purpose: Detects volatility and overbought/oversold conditions.

Usage: Price touching upper band → possible overbought; lower band → oversold.

Why Add: Enhances confirmation of spoofing or breakout setups.

2. **MACD Histogram**
Purpose: Measures trend strength and momentum.

Usage: Positive histogram rising = bullish momentum, and vice versa.

Why Add: Helps confirm directional signals.

3. **Stochastic RSI**
Purpose: Adds sensitivity to RSI, great for scalping and short-term trades.

Usage: < 20 = oversold; > 80 = overbought.

Why Add: Can refine entries/exits in already-flagged spoof or momentum zones.

4. **ADX (Average Directional Index)**
Purpose: Measures trend strength (not direction).

Usage: ADX > 25 → strong trend. Helps filter out choppy/noisy zones.

Why Add: Prevents false trades in sideways/no trend environments.

5. **OBV (On Balance Volume)**
Purpose: Tracks volume flow to confirm price movement.

Usage: Price up but OBV flat → divergence. Good for confirming spoofing moves.

Why Add: Helps identify if big money is supporting a move or it's a fakeout.

"""

def render_glossary_tab():
    st.header("📘 Glossary")
    st.markdown(GLOSSARY_MARKDOWN)

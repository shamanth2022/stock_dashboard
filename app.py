
import streamlit as st
import pandas as pd
from data import get_price_history
from signals import compute_indicators, generate_signals, detect_support_resistance
from macro import get_macro_regime
from portfolio import Portfolio
from alerts import send_alert

st.set_page_config(layout="wide")
st.title("Institutional Stack v2 - AI Infrastructure Trading Dashboard")

tickers = ["NVDA","TSM","ASML","AMD","AVGO","ETN","CEG","VST","EQIX","CARR"]

# Load data
data = get_price_history(tickers)

# Compute signals
results = []
for t, df in data.items():
    ind = compute_indicators(df)
    sig = generate_signals(ind)
    latest = ind.iloc[-1]
    support, resistance = detect_support_resistance(df)

    results.append({
        "Ticker": t,
        "Price": round(latest["Close"],2),
        "RSI": round(latest["RSI"],1),
        "MA50": round(latest["MA50"],2),
        "MA200": round(latest["MA200"],2),
        "ATR": round(latest["ATR"],2),
        "Support": round(support,2),
        "Resistance": round(resistance,2),
        "Signal": sig
    })

df = pd.DataFrame(results)

# Macro Regime
st.subheader("Macro Regime Engine")
macro = get_macro_regime()
st.json(macro)

# Signals
st.subheader("Live Signals")
st.dataframe(df)

st.subheader("Strong Buy")
st.dataframe(df[df["Signal"]=="STRONG_BUY"])

st.subheader("Buy")
st.dataframe(df[df["Signal"]=="BUY"])

# Portfolio Tracking
st.subheader("Portfolio Tracking")
portfolio = Portfolio()
# Simulate some positions
for row in df.itertuples():
    if row.Signal in ["STRONG_BUY", "BUY"]:
        shares = portfolio.position_size(row.Ticker, row.Price, row.ATR)
        portfolio.buy(row.Ticker, shares, row.Price)

prices = {row.Ticker: row.Price for row in df.itertuples()}
portfolio.update_prices(prices)

st.write(f"Total P&L: ${portfolio.get_pnl():.2f}")
st.write("Allocations:", portfolio.get_allocation())

# Alerts
if st.button("Send Alert for Strong Buys"):
    strong_buys = df[df["Signal"]=="STRONG_BUY"]
    if not strong_buys.empty:
        message = "Strong Buy Signals: " + ", ".join(strong_buys["Ticker"].tolist())
        send_alert("Trading Alert", message, "your_email@example.com")
        st.success("Alert sent!")
    else:
        st.info("No strong buys to alert.")

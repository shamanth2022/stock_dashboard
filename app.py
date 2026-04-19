
import streamlit as st
import pandas as pd
from data import get_price_history
from signals import compute_indicators, generate_signals

st.set_page_config(layout="wide")
st.title("AI Infrastructure Trading Dashboard (Pro)")

tickers = ["NVDA","TSM","ASML","AMD","AVGO","ETN","CEG","VST","EQIX","CARR"]

data = get_price_history(tickers)

results = []
for t, df in data.items():
    ind = compute_indicators(df)
    sig = generate_signals(ind)
    latest = ind.iloc[-1]

    results.append({
        "Ticker": t,
        "Price": round(latest["Close"],2),
        "RSI": round(latest["RSI"],1),
        "MA50": round(latest["MA50"],2),
        "MA200": round(latest["MA200"],2),
        "Signal": sig
    })

df = pd.DataFrame(results)

st.subheader("Live Signals")
st.dataframe(df)

st.subheader("Strong Buy")
st.dataframe(df[df["Signal"]=="STRONG_BUY"])

st.subheader("Buy")
st.dataframe(df[df["Signal"]=="BUY"])

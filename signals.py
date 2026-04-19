
import pandas as pd

def compute_indicators(df):
    df = df.copy()
    df["MA50"] = df["Close"].rolling(50).mean()
    df["MA200"] = df["Close"].rolling(200).mean()

    delta = df["Close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    df["RSI"] = 100 - (100 / (1 + rs))

    return df

def generate_signals(df):
    latest = df.iloc[-1]
    print(latest)
    if latest["RSI"] < 40 and latest["Close"] < latest["MA50"]:
        return "STRONG_BUY"
    elif latest["RSI"] < 50 and latest["Close"] < latest["MA50"]:
        return "BUY"
    else:
        return "HOLD"

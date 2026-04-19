
import pandas as pd
import numpy as np
from scipy.signal import find_peaks

def compute_indicators(df):
    df = df.copy()
    df["MA50"] = df["Close"].rolling(50).mean()
    df["MA200"] = df["Close"].rolling(200).mean()

    delta = df["Close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    df["RSI"] = 100 - (100 / (1 + rs))

    # ATR
    high_low = df['High'] - df['Low']
    high_close = (df['High'] - df['Close'].shift()).abs()
    low_close = (df['Low'] - df['Close'].shift()).abs()
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    df['ATR'] = tr.rolling(14).mean()

    return df

def detect_support_resistance(df, window=20):
    # Simple support/resistance: recent min low and max high
    support = df['Low'].tail(window).min()
    resistance = df['High'].tail(window).max()
    return support, resistance

def generate_signals(df):
    latest = df.iloc[-1]
    
    # Volatility-adjusted: if ATR is high, be more cautious
    atr_factor = latest['ATR'] / latest['Close']  # normalized ATR
    rsi_threshold = 40 + atr_factor * 10  # adjust threshold
    
    if latest["RSI"] < rsi_threshold and latest["Close"] < latest["MA50"]:
        return "STRONG_BUY"
    elif latest["RSI"] < 50 + atr_factor * 5 and latest["Close"] < latest["MA50"]:
        return "BUY"
    else:
        return "HOLD"

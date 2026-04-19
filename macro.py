import yfinance as yf
import pandas as pd
from fredapi import Fred
import os

# Note: Need FRED API key, set as env var FRED_API_KEY

def get_macro_regime():
    # Fed Funds Rate
    fred = Fred(api_key=os.getenv('FRED_API_KEY', 'demo'))  # Use demo if no key
    try:
        fed_rate = fred.get_series('FEDFUNDS').iloc[-1]
    except:
        fed_rate = 5.0  # mock

    # 10Y Treasury Yield
    try:
        yield_10y = fred.get_series('DGS10').iloc[-1]
    except:
        yield_10y = 4.5  # mock

    # Nasdaq trend: 50-day MA vs current
    nasdaq = yf.Ticker('^IXIC')
    hist = nasdaq.history(period='6mo')
    current = hist['Close'].iloc[-1]
    ma50 = hist['Close'].rolling(50).mean().iloc[-1]
    nasdaq_trend = 'Bullish' if current > ma50 else 'Bearish'

    regime = {
        'Fed Rate': fed_rate,
        '10Y Yield': yield_10y,
        'Nasdaq Trend': nasdaq_trend
    }

    # Simple regime: if fed_rate > 5 and yield_10y > 4, Tightening; else Easing
    if fed_rate > 5 and yield_10y > 4:
        regime['Overall'] = 'Tightening'
    elif nasdaq_trend == 'Bullish':
        regime['Overall'] = 'Bullish'
    else:
        regime['Overall'] = 'Neutral'

    return regime

import yfinance as yf

def get_price_history(tickers):
    data = {}
    for t in tickers:
        try:
            df = yf.download(t, period="1y", progress=False)
            data[t] = df
        except:
            pass
    return data


import yfinance as yf

def get_price_history(tickers):
    data = {}
    for t in tickers:
        try:
            df = yf.download(t, period="1y", progress=False)
            df.columns = df.columns.droplevel(1)  # Flatten MultiIndex columns
            # Add description column
            ticker_info = yf.Ticker(t).info
            description = ticker_info.get('longBusinessSummary', 'No description available')
            df['Description'] = description
            data[t] = df
        except:
            pass
    return data

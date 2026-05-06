import requests
import pandas as pd
from datetime import datetime, timedelta
import time


def get_binance_btc_data():

    # data from Binance api

    url = "https://api.binance.com/api/v3/klines"

    symbol = "BTCUSDT"
    interval = "1d"  # 1 day candles
    limit = 90      # Get the last 90 days

    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': limit
    }

    print(f"Fetching data from {limit} to {symbol}\n")

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()

        columns = [
            'Open Time', 'Open', 'High', 'Low', 'Close', 'Volume',
            'Close Time', 'Quote Asset Volume', 'Number of Trades',
            'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore'
        ]

        df = pd.DataFrame(data, columns=columns)

        df = df[['Open Time', 'Close']]
        df['Open Time'] = pd.to_datetime(df['Open Time'], unit='ms')
        df['Open Time'] = df['Open Time'].dt.date

        df['Close'] = df['Close'].astype(float)
        df = df.rename(columns={'Open Time': 'Date',
                       'Close': 'Closing Price (USD)'})

        return df

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Binance: {e}")
        return None


if __name__ == "__main__":
    btc_data = get_binance_btc_data()

    if btc_data is not None:
        for date, price in btc_data.itertuples(index=False):
            print(f"{date}: ${price:.2f}")

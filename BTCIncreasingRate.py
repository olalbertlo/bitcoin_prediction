import pandas as pd

df = pd.read_csv('btc_max_ohlc_yfinance.csv')

df.columns = df.columns.str.strip()

df['change_rate'] = (df['Close'] - df['Open']) / df['Open'] * 100

df[['Date', 'change_rate']].to_csv('btc_change_rate.csv', index=False)

print("store as btc_change_rate.csv")

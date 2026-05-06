import requests
import pandas as pd
import json


def get_binance_daily_ohlc(symbol="BTCUSDT", days=365):
    # Binance API 的 K 線資料端點
    url = "https://api.binance.com/api/v3/klines"

    interval = "1d"  # 1 day candles
    limit = days     # Get the last 365 days

    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': limit
    }

    print(f"正在從 Binance API 獲取 {symbol} 過去 {limit} 天的資料...\n")

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()

        # Binance 回傳的 12 個原始欄位
        columns = [
            'Open Time', 'Open', 'High', 'Low', 'Close', 'Volume',
            'Close Time', 'Quote Asset Volume', 'Number of Trades',
            'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore'
        ]

        df = pd.DataFrame(data, columns=columns)

        df = df[['Open Time', 'Open', 'High', 'Low', 'Close']]

        # 將時間戳轉換為 YYYY-MM-DD 格式的字串
        df['Open Time'] = pd.to_datetime(
            df['Open Time'], unit='ms').dt.strftime('%Y-%m-%d')

        # 將價格資料從字串轉換為浮點數
        for col in ['Open', 'High', 'Low', 'Close']:
            df[col] = df[col].astype(float)

        # 重新命名時間欄位
        df = df.rename(columns={'Open Time': 'Date'})

        return df

    except requests.exceptions.RequestException as e:
        print(f"獲取資料時發生錯誤: {e}")
        return None


if __name__ == "__main__":
    btc_data = get_binance_daily_ohlc(symbol="BTCUSDT", days=365)

    if btc_data is not None:
        output_filename = "btc_1year_ohlc.json"

        # 匯出為 JSON 檔案
        btc_data.to_json(output_filename, orient='records', indent=4)

        print(f"✅ 資料已成功匯出至：{output_filename}")

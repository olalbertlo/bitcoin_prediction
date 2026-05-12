import yfinance as yf
import pandas as pd
import json


def get_yahoo_daily_ohlc(symbol="BTC-USD", period="1y"):
    """
    使用 yfinance 獲取過去一年的 OHLC 資料
    period 可以設定為 "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"
    """
    print(f"正在從 yfinance 獲取 {symbol} 過去 {period} 的資料...\n")

    try:
        # 獲取歷史資料
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period)

        if df.empty:
            print(f"找不到 {symbol} 的資料，請確認商品代碼是否正確。")
            return None

        # yfinance 預設將時間作為 Index，我們需要把它變成一般欄位
        df = df.reset_index()

        # 只保留需要的欄位：Date, Open, High, Low, Close
        df = df[['Date', 'Open', 'High', 'Low', 'Close']]

        # 將 Datetime 格式的時間轉換為 YYYY-MM-DD 的純字串
        df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')

        for col in ['Open', 'High', 'Low', 'Close']:
            df[col] = df[col].astype(float)

        return df

    except Exception as e:
        print(f"獲取資料時發生錯誤: {e}")
        return None


if __name__ == "__main__":
    btc_data = get_yahoo_daily_ohlc(symbol="BTC-USD", period="1y")

    if btc_data is not None:
        output_filename = "btc_1year_ohlc_yfinance.csv"

        # 匯出為 CSV 檔案
        # index=False 避免輸出 DataFrame 的索引欄
        btc_data.to_csv(output_filename, index=False)

        print(f"資料已成功匯出至：{output_filename}")

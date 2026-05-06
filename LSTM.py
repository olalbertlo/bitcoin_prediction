import yfinance as yf
import numpy as np
import torch
import torch.nn as nn
from sklearn.preprocessing import MinMaxScaler


class BitcoinLSTM(nn.Module):
    def __init__(self, input_size=1, hidden_size=64, num_layers=2, output_size=1):
        super(BitcoinLSTM, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size,
                            num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = out[:, -1, :]
        return self.fc(out)


def validate_historical_prediction(target_days_ago=6):
    fetch_days = 100 + target_days_ago + 10

    print(f"Start From Yahoo Finance : {fetch_days} days ago")
    btc = yf.Ticker("BTC-USD")
    df = btc.history(period=f"{fetch_days}d")

    if len(df) < (100 + target_days_ago):
        print("ran out of data")
        return

    prices = df[['Close']].values
    dates = df.index

    # time slice
    actual_price = prices[-target_days_ago][0]
    target_date = dates[-target_days_ago].strftime("%Y-%m-%d")

    start_idx = -(100 + target_days_ago)
    end_idx = -target_days_ago
    input_100_days = prices[start_idx: end_idx]

    # pre-process
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_input = scaler.fit_transform(input_100_days)
    tensor_input = torch.tensor(scaled_input, dtype=torch.float32).unsqueeze(0)

    model = BitcoinLSTM()
    model.eval()
    with torch.no_grad():
        scaled_pred = model(tensor_input)

    predicted_price = scaler.inverse_transform(scaled_pred.numpy())[0][0]

    # backtest
    error = predicted_price - actual_price
    error_percent = (abs(error) / actual_price) * 100

    print("LSTM prediction")
    print(f"target date: {target_date} ({target_days_ago - 1} days ago)")
    print(
        f"data date range: {dates[start_idx].strftime('%Y-%m-%d')} to {dates[end_idx-1].strftime('%Y-%m-%d')}")
    print("-" * 40)
    print(f"prediction price: ${predicted_price:,.2f}")
    print(f"actual price: ${actual_price:,.2f}")
    print("-" * 40)

    if error > 0:
        print(f"overestimated : ${abs(error):,.2f}")
    else:
        print(f"underestimated : ${abs(error):,.2f}")

    print(f"error rate : {error_percent:.2f}%")


if __name__ == "__main__":
    validate_historical_prediction(target_days_ago=6)

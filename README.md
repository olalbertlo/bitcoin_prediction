# Bitcoin Price Prediction

Next-day BTC-USD closing-price forecasting with GRU, Mamba, and Transformer models, evaluated against a naive persistence baseline (tomorrow's price = today's price).

## Repository structure

| Path | Contents |
|---|---|
| `notebooks/stage1/` | Stage 1: GRU, Mamba, and Transformer on closing prices only. `Stage1_Rerun_GRU_Mamba_Transformer.ipynb` is the version used in the report (train-only scaling, common test dates, seeds 0–4, persistence baseline). |
| `notebooks/stage2/` | Stage 2: Transformer with technical indicators. `TransformerForPrediction_v3.ipynb` is the version used in the report (72/8/20 split, 32 indicator-group combinations × 5 seeds). |
| `data/` | Daily BTC-USD data from Yahoo Finance: `btc_max_ohlc_yfinance.csv` (OHLC prices), `btc_indicators_calculated.csv` (SMA, EMA, RSI, MACD, Daily Return), `btc_change_rate.csv` (daily change rate). |

## Experiment results (Google Drive)

All experiment outputs are stored here: [btc_transformer_results](https://drive.google.com/drive/folders/1Sdgu0bI0l2FczlccMIH7PCUjC9cngvH5?usp=sharing)

| Folder | Contents |
|---|---|
| `v3_split_72-8-20/` | Stage 2 results: daily predictions for every run, per-epoch loss, metric tables (Tables II, V, VI), figures, run settings, and environment log (GPU, CUDA, package versions) |
| `stage1_rerun/` | Stage 1 results: daily predictions, per-epoch loss, results table (Table IV), Fig. 3, and environment log |

## How to run

1. Open a notebook in Google Colab and select a T4 GPU runtime.
2. Upload the CSV files from `data/` to the Colab session.
3. Run all cells. Results are saved to Google Drive, and an interrupted run resumes where it stopped.

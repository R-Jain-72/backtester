# Trading Strategy Backtester with Streamlit

A Python-based trading strategy backtester with a Streamlit interface, fetching 1-minute OHLC data from Binance, implementing MACD-based and RSI-EMA strategies, and visualizing trades and performance. Uses `pandas`, `pandas-ta`, `requests`, `streamlit`, and `plotly`, avoiding `backtrader`.

## Project Overview

- **Components**:
  - **backtester.py**: Core logic for data fetching, indicators, strategies, and trade execution.
  - **app.py**: Streamlit interface for running backtests and visualizing results.
  - **requirements.txt**: Dependencies.
- **Features**:
  - Fetches up to 5000 1-minute BTCUSDT candles from Binance API.
  - Strategies:
    - **MACD**: Buy when EMA(12) of MACD line crosses above EMA(26), sell when it crosses below.
    - **RSI-EMA**: Buy when RSI(14) > 30 and close > EMA(21), sell when RSI < 70 or close < EMA(21).
  - Outputs trades to `trades.csv` with: `[Entry Time, Entry Price, Exit Time, Exit Price, Strategy, PnL, Status]`.
  - Streamlit UI: Select symbol, run strategies, view trades, metrics, and visualizations (price chart, P&L).

## Prerequisites

1. **Python 3.8+**:
   - Download from [python.org](https://www.python.org/downloads/).
   - Check "Add Python to PATH".
   - Verify:
     ```cmd
     python --version
     ```

2. **Windows 10/11**:
   - Tested on Windows with Command Prompt.

3. **Project Files**:
   - Place in `C:\Users\ghisu\Desktop\Code\BackEND\Tusta-backend-backtester-engine`:
     - `backtester.py`
     - `app.py`
     - `requirements.txt`
     - `README.md`

## Setup Instructions

1. **Create Directory**:
   - Ensure `C:\Users\ghisu\Desktop\Code\BackEND\Tusta-backend-backtester-engine` contains project files.

2. **Create Virtual Environment**:
   - Open Command Prompt.
   - Navigate to:
     ```cmd
     cd C:\Users\ghisu\Desktop\Code\BackEND\Tusta-backend-backtester-engine
     ```
   - Create:
     ```cmd
     python -m venv virt
     ```
   - Activate:
     ```cmd
     virt\Scripts\activate
     ```

3. **Install Dependencies**:
   - Install:
     ```cmd
     pip install -r requirements.txt
     ```

4. **Run Streamlit App**:
   - Run:
     ```cmd
     python -m streamlit run app.py
     ```
   - Open `http://localhost:8501`.

5. **Run Standalone Backtester**:
   - Run:
     ```cmd
     python backtester.py
     ```
   - Outputs `trades.csv`.

## Testing the Application

1. **Run Backtest**:
   - **Streamlit**: Open `http://localhost:8501`.
     - **Symbol**: Enter `BTCUSDT`.
     - **Interval**: Fixed at `1m`.
     - **Candles**: Set up to 5000.
     - **Strategies**: Select `MACD`, `RSI-EMA`, or both.
     - Click **Run Backtest**.
   - **Standalone**: Run `python backtester.py`.

2. **View Results**:
   - **Trades**: DataFrame (Streamlit) or `trades.csv` with entry/exit times, prices, strategy, P&L, status.
   - **Metrics** (Streamlit): Total trades, win rate, total P&L.
   - **Visualizations** (Streamlit): Candlestick chart with entry/exit points, cumulative P&L plot.
   - **trades.csv**: In project directory.

3. **Example Output**:
   - `trades.csv`:
     ```csv
     Entry Time,Entry Price,Exit Time,Exit Price,Strategy,PnL,Status
     2025-05-31 22:00:00,50000.0,2025-05-31 22:10:00,50500.0,MACD,500.0,Win
     2025-05-31 22:15:00,50500.0,2025-05-31 22:30:00,50200.0,RSI-EMA,-300.0,Loss
     ```
   - Metrics: Total Trades: 10, Win Rate: 60%, Total P&L: 200 USDT

4. **Test Strategies**:
   - **MACD**: Verify trades on MACD EMA crossovers.
   - **RSI-EMA**: Confirm buys on RSI > 30 and close > EMA(21), sells on RSI < 70 or close < EMA(21).

## Notes

- **Data**: Up to 5000 1-minute BTCUSDT candles.
- **Position Size**: 1 BTC.
- **Environment**: Use virtual environment to avoid conflicts.
- **Time**: Valid as of May 31, 2025, 11:29 PM IST.

For support, check logs or contact the developer.

## DEMO
https://github.com/user-attachments/assets/b62f4b66-9d02-4dbb-9307-84750e724262

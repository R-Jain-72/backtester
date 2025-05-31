import pandas as pd
import pandas_ta as ta
import requests
import json
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_binance_data(symbol="BTCUSDT", interval="1m", limit=5000):
    """
    Fetch OHLC data from Binance API.
    """
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume',
                   'number_of_trades', 'taker_buy_base', 'taker_buy_quote', 'ignore']
        df = pd.DataFrame(data, columns=columns)
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].astype(float)
        logging.info(f"Fetched {len(df)} candles for {symbol}")
        return df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
    except requests.RequestException as e:
        logging.error(f"Failed to fetch data: {e}")
        return None

def calculate_indicators(df):
    """
    Calculate MACD, RSI, and EMA indicators.
    """
    df['macd'] = ta.macd(df['close'])['MACD_12_26_9']
    df['macd_ema_fast'] = ta.ema(df['macd'], length=12)
    df['macd_ema_slow'] = ta.ema(df['macd'], length=26)
    df['rsi'] = ta.rsi(df['close'], length=14)
    df['ema_21'] = ta.ema(df['close'], length=21)
    return df

def macd_strategy(df):
    """
    MACD-based strategy: Buy when MACD EMA (fast) crosses above MACD EMA (slow), sell when it crosses below.
    """
    df['signal'] = 0
    # Compute crossover conditions
    buy_signal = (df['macd_ema_fast'] > df['macd_ema_slow']) & (df['macd_ema_fast'].shift(1) <= df['macd_ema_slow'].shift(1))
    sell_signal = (df['macd_ema_fast'] < df['macd_ema_slow']) & (df['macd_ema_fast'].shift(1) >= df['macd_ema_slow'].shift(1))
    # Assign signals where conditions are met and data is valid
    df.loc[buy_signal & df['macd_ema_fast'].notna() & df['macd_ema_slow'].notna(), 'signal'] = 1
    df.loc[sell_signal & df['macd_ema_fast'].notna() & df['macd_ema_slow'].notna(), 'signal'] = -1
    return df

def rsi_ema_strategy(df):
    """
    RSI-EMA strategy: Buy when RSI > 30 and close > EMA(21), sell when RSI < 70 or close < EMA(21).
    """
    df['signal'] = 0
    # Compute buy and sell conditions
    buy_signal = (df['rsi'] > 30) & (df['rsi'].shift(1) <= 30) & (df['close'] > df['ema_21'])
    sell_signal = ((df['rsi'] < 70) & (df['rsi'].shift(1) >= 70)) | ((df['close'] < df['ema_21']) & (df['close'].shift(1) >= df['ema_21']))
    # Assign signals where conditions are met and data is valid
    df.loc[buy_signal & df['rsi'].notna() & df['ema_21'].notna(), 'signal'] = 1
    df.loc[sell_signal & df['rsi'].notna() & df['ema_21'].notna(), 'signal'] = -1
    return df

def execute_trades(df, strategy_name, strategy_func):
    """
    Execute trades based on strategy signals.
    """
    df = strategy_func(df.copy())
    trades = []
    position = None
    position_size = 1  # 1 BTC
    
    for i in range(1, len(df)):
        if df['signal'].iloc[i] == 1 and position is None:
            position = {
                'entry_time': df['timestamp'].iloc[i],
                'entry_price': df['close'].iloc[i],
                'strategy': strategy_name
            }
            logging.info(f"[{strategy_name}] Entered trade at {position['entry_time']} with price {position['entry_price']}")
        
        elif df['signal'].iloc[i] == -1 and position is not None:
            exit_price = df['close'].iloc[i]
            exit_time = df['timestamp'].iloc[i]
            pnl = (exit_price - position['entry_price']) * position_size
            status = 'Win' if pnl > 0 else 'Loss'
            trades.append({
                'Entry Time': position['entry_time'],
                'Entry Price': position['entry_price'],
                'Exit Time': exit_time,
                'Exit Price': exit_price,
                'Strategy': strategy_name,
                'PnL': pnl,
                'Status': status
            })
            logging.info(f"[{strategy_name}] Exited trade at {exit_time} with price {exit_price}, PnL: {pnl}, Status: {status}")
            position = None
    
    return pd.DataFrame(trades)

def main():
    """
    Run the backtester standalone.
    """
    df = fetch_binance_data()
    if df is None:
        return
    
    df = calculate_indicators(df)
    macd_trades = execute_trades(df, "MACD", macd_strategy)
    rsi_ema_trades = execute_trades(df, "RSI-EMA", rsi_ema_strategy)
    trades_df = pd.concat([macd_trades, rsi_ema_trades], ignore_index=True)
    
    trades_df.to_csv('trades.csv', index=False)
    logging.info(f"Saved {len(trades_df)} trades to trades.csv")
    logging.info(f"Sample trades:\n{trades_df.head().to_string()}")

if __name__ == '__main__':
    main()
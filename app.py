import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from backtester import fetch_binance_data, calculate_indicators, execute_trades, macd_strategy, rsi_ema_strategy

# Streamlit configuration
st.set_page_config(page_title="Strategy Backtester", layout="wide")

st.title("Trading Strategy Backtester")

# Input parameters
st.sidebar.header("Parameters")
symbol = st.sidebar.text_input("Symbol", value="BTCUSDT")
interval = st.sidebar.selectbox("Interval", ["1m"], disabled=True)  # Fixed to 1m
limit = st.sidebar.number_input("Number of Candles (max 5000)", min_value=100, max_value=5000, value=5000)
strategies = st.sidebar.multiselect("Strategies", ["MACD", "RSI-EMA"], default=["MACD", "RSI-EMA"])

# Fetch data button
if st.button("Run Backtest"):
    with st.spinner("Fetching data and running backtest..."):
        # Fetch data
        df = fetch_binance_data(symbol=symbol, interval=interval, limit=limit)
        if df is None:
            st.error("Failed to fetch data from Binance.")
        else:
            # Calculate indicators
            df = calculate_indicators(df)
            
            # Run selected strategies
            trades_dfs = []
            if "MACD" in strategies:
                macd_trades = execute_trades(df, "MACD", macd_strategy)
                trades_dfs.append(macd_trades)
            if "RSI-EMA" in strategies:
                rsi_ema_trades = execute_trades(df, "RSI-EMA", rsi_ema_strategy)
                trades_dfs.append(rsi_ema_trades)
            
            # Combine trades
            if trades_dfs:
                trades_df = pd.concat(trades_dfs, ignore_index=True)
                
                # Display trades
                st.header("Trades")
                st.dataframe(trades_df)
                
                # Summary metrics
                st.header("Performance Metrics")
                total_trades = len(trades_df)
                win_trades = len(trades_df[trades_df['Status'] == 'Win'])
                win_rate = win_trades / total_trades * 100 if total_trades > 0 else 0
                total_pnl = trades_df['PnL'].sum()
                st.write(f"Total Trades: {total_trades}")
                st.write(f"Win Rate: {win_rate:.2f}%")
                st.write(f"Total P&L: {total_pnl:.2f} USDT")
                
                # Save trades
                trades_df.to_csv('trades.csv', index=False)
                st.success("Trades saved to trades.csv")
                
                # Visualizations
                st.header("Visualizations")
                
                # Price chart with entry/exit points
                fig_price = go.Figure()
                fig_price.add_trace(go.Candlestick(
                    x=df['timestamp'],
                    open=df['open'],
                    high=df['high'],
                    low=df['low'],
                    close=df['close'],
                    name='OHLC'
                ))
                for _, trade in trades_df.iterrows():
                    fig_price.add_trace(go.Scatter(
                        x=[trade['Entry Time'], trade['Exit Time']],
                        y=[trade['Entry Price'], trade['Exit Price']],
                        mode='markers+lines',
                        name=f"{trade['Strategy']} Trade",
                        marker=dict(size=10)
                    ))
                fig_price.update_layout(title="Price Chart with Trades", xaxis_title="Time", yaxis_title="Price (USDT)")
                st.plotly_chart(fig_price)
                
                # Cumulative P&L
                trades_df['Cumulative PnL'] = trades_df['PnL'].cumsum()
                fig_pnl = go.Figure()
                fig_pnl.add_trace(go.Scatter(
                    x=trades_df['Exit Time'],
                    y=trades_df['Cumulative PnL'],
                    mode='lines+markers',
                    name='Cumulative P&L'
                ))
                fig_pnl.update_layout(title="Cumulative P&L Over Time", xaxis_title="Time", yaxis_title="P&L (USDT)")
                st.plotly_chart(fig_pnl)
            else:
                st.warning("No strategies selected.")
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Step 1: Download historical data
# -----------------------------
ticker = "SPY"
data = yf.download(ticker, start="2018-01-01", end="2023-01-01")
data = data[['Close']]
data.columns = ['price']

# -----------------------------
# Step 2: Compute rolling statistics
# -----------------------------
window = 20
data['rolling_mean'] = data['price'].rolling(window=window).mean()
data['rolling_std'] = data['price'].rolling(window=window).std()

# -----------------------------
# Step 3: Compute Z-score
# -----------------------------
data['z_score'] = (data['price'] - data['rolling_mean']) / data['rolling_std']

# -----------------------------
# Step 4: Generate basic trading signals (original version)
# -----------------------------
data['signal_basic'] = 0
data.loc[data['z_score'] < -1, 'signal_basic'] = 1   # BUY
data.loc[data['z_score'] > 1, 'signal_basic'] = -1   # SELL

# -----------------------------
# Step 5: Advanced trading signals (±2 + trend filter)
# -----------------------------
data['long_ma'] = data['price'].rolling(100).mean()
data['signal_advanced'] = 0
# Buy only if price above long-term average
data.loc[(data['z_score'] < -2) & (data['price'] > data['long_ma']), 'signal_advanced'] = 1
# Sell only if price below long-term average
data.loc[(data['z_score'] > 2) & (data['price'] < data['long_ma']), 'signal_advanced'] = -1

# -----------------------------
# Step 6: Compute positions
# -----------------------------
# Basic
data['position_basic'] = data['signal_basic'].shift(1).fillna(0)
# Advanced
data['position_advanced'] = data['signal_advanced'].shift(1).fillna(0)

# -----------------------------
# Step 7: Compute returns
# -----------------------------
data['returns'] = data['price'].pct_change()
data['strategy_basic_returns'] = data['position_basic'] * data['returns']
data['strategy_advanced_returns'] = data['position_advanced'] * data['returns']

# -----------------------------
# Step 8: Compute cumulative returns
# -----------------------------
data['cumulative_returns'] = (1 + data['returns']).cumprod()
data['strategy_basic_cum'] = (1 + data['strategy_basic_returns']).cumprod()
data['strategy_advanced_cum'] = (1 + data['strategy_advanced_returns']).cumprod()

# -----------------------------
# Step 9: Compute Sharpe ratio
# -----------------------------
sharpe_basic = (data['strategy_basic_returns'].mean() / data['strategy_basic_returns'].std()) * np.sqrt(252)
sharpe_advanced = (data['strategy_advanced_returns'].mean() / data['strategy_advanced_returns'].std()) * np.sqrt(252)

# -----------------------------
# Step 10: Compute Max Drawdown
# -----------------------------
def max_drawdown(cum_returns):
    rolling_max = cum_returns.cummax()
    drawdown = (cum_returns - rolling_max) / rolling_max
    return drawdown.min()

drawdown_basic = max_drawdown(data['strategy_basic_cum'])
drawdown_advanced = max_drawdown(data['strategy_advanced_cum'])

# -----------------------------
# Step 11: Print metrics
# -----------------------------
print(f"Basic strategy: Sharpe = {sharpe_basic:.2f}, Max Drawdown = {drawdown_basic:.2%}")
print(f"Advanced strategy: Sharpe = {sharpe_advanced:.2f}, Max Drawdown = {drawdown_advanced:.2%}")

# -----------------------------
# Step 12: Plot cumulative returns
# -----------------------------
plt.figure(figsize=(12,6))
plt.plot(data.index, data['cumulative_returns'], label='Buy & Hold')
plt.plot(data.index, data['strategy_basic_cum'], label='Basic Strategy')
plt.plot(data.index, data['strategy_advanced_cum'], label='Advanced Strategy')
plt.title('Strategy Comparison')
plt.xlabel('Date')
plt.ylabel('Cumulative Returns')
plt.legend()
plt.show()
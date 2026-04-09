# main_stochastic_advanced_confidence.py

import numpy as np
import pandas as pd
import yfinance as yf

# ----------------------------
# 1. Download historical data
# ----------------------------
data = yf.download("SPY", start="2018-01-01", end="2023-01-01")[['Close']]
data.columns = ['price']

# Compute daily returns
data['returns'] = data['price'].pct_change()

# Rolling window for drift and volatility
window = 20
data['drift'] = data['returns'].rolling(window).mean()
data['vol'] = data['returns'].rolling(window).std()

# ----------------------------
# 2. Multi-step stochastic simulation with logistic modulation
# ----------------------------
dt = 1/252
np.random.seed(42)

signals = []
sim_positions = []

n_sim = 100     # Monte Carlo paths
horizon = 5     # predict 5 days ahead
k = 10          # logistic steepness
confidence_threshold = 0.2  # threshold for strong signal

for t in range(window, len(data)-horizon):
    mu_t = data['drift'].iloc[t]
    sigma_t = data['vol'].iloc[t]
    S_t = data['price'].iloc[t]
    
    # Monte Carlo multi-step simulation
    S_future = np.zeros(n_sim)
    for i in range(n_sim):
        S_temp = S_t
        for h in range(horizon):
            S_temp = S_temp * np.exp((mu_t - 0.5*sigma_t**2)*dt + sigma_t*np.sqrt(dt)*np.random.randn())
        S_future[i] = S_temp
    
    # Signal strength = deviation from current price normalized by volatility
    expected_price = S_t * np.exp(mu_t*dt*horizon)
    signal_strength = (np.mean(S_future) - S_t) / sigma_t
    
    # Logistic modulation for probability of long
    P_long = 1 / (1 + np.exp(-k * signal_strength))
    P_short = 1 - P_long
    
    # Compute confidence
    signal_confidence = P_long - P_short
    
    # Generate position based on threshold
    if signal_confidence > confidence_threshold:
        position = 1
    elif signal_confidence < -confidence_threshold:
        position = -1
    else:
        position = 0
    
    signals.append([P_long, P_short, signal_confidence])
    sim_positions.append(position)

# ----------------------------
# 3. Convert signals to DataFrame
# ----------------------------
signal_df = pd.DataFrame(signals, columns=['P_long','P_short','signal_confidence'], index=data.index[window:len(data)-horizon])
signal_df['position'] = sim_positions

# ----------------------------
# 4. Strategy returns
# ----------------------------
data_trading = data.iloc[window:len(data)-horizon].copy()
data_trading['position'] = signal_df['position'].values
data_trading['strategy_returns'] = data_trading['position'] * data_trading['returns']

# Cumulative returns
data_trading['cumulative_strategy'] = (1 + data_trading['strategy_returns']).cumprod()
data_trading['cumulative_asset'] = (1 + data_trading['returns']).cumprod()

# ----------------------------
# 5. Performance metrics
# ----------------------------
sharpe = data_trading['strategy_returns'].mean() / data_trading['strategy_returns'].std() * np.sqrt(252)
max_drawdown = (data_trading['cumulative_strategy'].cummax() - data_trading['cumulative_strategy']).max()

print("Sharpe Ratio:", sharpe)
print("Max Drawdown:", max_drawdown)
print("Last generated signals:")
print(signal_df.tail())

# notebook_visualization_english.ipynb

import matplotlib.pyplot as plt
import seaborn as sns

# Assume 'data_trading' and 'signal_df' are already loaded from the advanced main
# data_trading contains 'cumulative_strategy' and 'cumulative_asset'
# signal_df contains 'P_long', 'P_short', 'signal_confidence'

# ----------------------------
# 1. Heatmap of trading signals
# ----------------------------
plt.figure(figsize=(12,4))
sns.heatmap(
    signal_df[['P_long','P_short','signal_confidence']].T,  # transpose to have signal types on rows
    cmap="RdYlGn",
    cbar_kws={'label': 'Probability / Confidence'}
)
plt.title("Heatmap of Trading Signals (Long / Short / Confidence)")
plt.xlabel("Date Index")
plt.ylabel("Signal Type")
plt.show()

# ----------------------------
# 2. Compare cumulative returns: Strategy vs Buy & Hold
# ----------------------------
plt.figure(figsize=(12,6))
plt.plot(data_trading['cumulative_asset'], label="Buy & Hold", color='blue')
plt.plot(data_trading['cumulative_strategy'], label="Strategy", color='green')
plt.title("Cumulative Returns: Strategy vs Buy & Hold")
plt.xlabel("Date Index")
plt.ylabel("Cumulative Returns")
plt.legend()
plt.grid(True)
plt.show()
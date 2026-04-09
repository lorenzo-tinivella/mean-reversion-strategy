# Mean Reversion Strategy on SPY

## Overview

This project implements a **mean-reversion trading strategy** on the SPDR S&P 500 ETF (SPY) using Python.  
It explores both **basic** and **advanced** approaches and evaluates performance with professional metrics.

The goal is to demonstrate **quantitative finance skills**:
- Python coding  
- Data analysis  
- Backtesting trading strategies  
- Performance metrics (Sharpe ratio, drawdown)  
- Visualization of results  

---

## Project Structure
```
mean-reversion-strategy/
├── src/
│ └── main.py # Complete final strategy code
├── notebooks/
│ ├── basic_strategy.ipynb # Original ±1 Z-score version
│ └── advanced_strategy.ipynb # ±2 Z-score + trend filter
├── README.md # This file
└── requirements.txt # Required Python libraries
```

---

## Strategy Logic

1. **Data Collection**  
   - Download historical SPY data using `yfinance`.

2. **Feature Calculation**  
   - Compute **rolling mean** and **standard deviation** over a 20-day window.  
   - Calculate **Z-score** to measure deviation from the mean.

3. **Signal Generation**  
   - **Basic Strategy:** Buy when Z-score < -1, Sell when Z-score > +1  
   - **Advanced Strategy:** Buy when Z-score < -2 and price > 100-day moving average,  
     Sell when Z-score > +2 and price < 100-day moving average  

4. **Backtesting**  
   - Shift signals by one day to avoid **look-ahead bias**.  
   - Compute daily returns and strategy returns.  
   - Calculate cumulative returns.

5. **Performance Metrics**  
   - **Sharpe Ratio**: Measures risk-adjusted return.  
   - **Max Drawdown**: Maximum observed loss from a peak.  

6. **Visualization**  
   - Compare **Buy & Hold**, **Basic Strategy**, and **Advanced Strategy** cumulative returns.

---

## How to Run

1. Clone the repository:
```bash
git clone https://github.com/lorenzo-tinivella/mean-reversion-strategy.git
cd mean-reversion-strategy
```


2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the final strategy:
```bash
python src/main.py
```

4. View results:
- Terminal outputs Sharpe ratio and max drawdown for both strategies.
- Equity curve plot compares strategies versus Buy & Hold.


## Key Learnings
- Mean reversion strategies can perform poorly in trending markets.
- Z-score thresholds and trend filters significantly impact performance.
- Backtesting with proper look-ahead bias control is     essential.
- The project demonstrates full pipeline: data → signals → backtest → evaluation.

## Future Improvements
- Add stop-loss and take-profit rules
- Test on other ETFs or stocks
- Include transaction costs for realistic backtest
- Optimize parameters using walk-forward analysis
- Explore machine learning-based signal prediction


# Advanced Stochastic Trading Strategy

## Overview
This repository contains an **advanced stochastic trading strategy** implemented in Python.  
The goal is to generate probabilistic trading signals using adaptive drift, volatility, and Monte Carlo simulation to improve risk-adjusted performance.

## Project Structure
```
project_root/
│
├── main_stochastic_advanced_confidence.py # Main strategy script
├── data/ # Folder containing CSV outputs
│ ├── data_trading.csv # Trading metrics and cumulative returns
│ └── signal_df.csv # Probabilistic signals and positions
├── notebooks/
│ └── visualization.ipynb # Notebook for visualization and analysis
├── README.md # Project documentation
└── .gitignore # Git ignore file
```


## How It Works
1. **Adaptive Drift and Volatility**  
   - Daily drift and volatility are computed using rolling windows to capture changing market conditions.

2. **Monte Carlo Simulation**  
   - Multi-step future price simulations generate probabilities of the asset moving up or down.

3. **Logistic Modulation & Confidence Threshold**  
   - Signals are converted to probabilities of going long or short.  
   - Positions are only taken if `P_long - P_short` exceeds a threshold (e.g., ±0.2), reducing noise and risk.

4. **Position Assignment**  
   - Long (+1), Short (-1), or Flat (0) based on the probabilistic signal.

5. **CSV Outputs for Visualization**  
   - `data/data_trading.csv` → cumulative returns, strategy returns, and positions  
   - `data/signal_df.csv` → P_long, P_short, confidence, positions  
   - The notebook reads these files to generate plots and metrics.

## How to Run
1. Execute the main strategy script:

```bash
python main_stochastic.py
```
2. Open the notebook:
```bash
jupyter notebook notebooks/stochastic_strategy.ipynb
```
3. Explore:

- Heatmaps of probabilistic signals
- Cumulative returns comparison with buy & hold
- Daily positions
- Sharpe ratio and maximum drawdown
 
## Metrics
- Sharpe Ratio: Measures risk-adjusted returns
- Max Drawdown: Measures maximum drop from peak
- Visual Analysis: Positions, confidence, and cumulative returns

## Notes
- The project structure keeps all generated CSVs in the data/ folder for clarity.
- The strategy can be extended by adding multi-factor signals, momentum, or mean-reversion indicators.

## Contact / Author
Name: Lorenzo Tinivella
GitHub: [lorenzo-tinivella](https://github.com/lorenzo-tinivella)
Email: lorenzo.tinivella@outlook.it


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

## Contact / Author
Name: Lorenzo Tinivella
GitHub: [lorenzo-tinivella](https://github.com/lorenzo-tinivella)
Email: lorenzo.tinivella@outlook.it

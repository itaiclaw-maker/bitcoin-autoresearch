# Trading Strategy Research Program: Bitcoin Auto-Research 🛰️

## Objective
Maximize the **annualized Sharpe Ratio** on BTC-USD daily bars.
Target: Sharpe > 2.0, Max Drawdown < 15%.

## Rules for strategy.py
- You MAY edit: Signal logic, indicator parameters, position sizing, SL/TP rules.
- You MUST NOT edit: Data loading interfaces, the `evaluate()` signature, or `backtest.py`.

## Strategy Constraints
- Minimum trades: 30 (to avoid statistical insignificance).
- Annual trade cap: 250 (to avoid over-trading/slippage rot).
- Deterministic: Code must yield the same result on every run.

## Research Priorities
1. Combined Momentum (e.g., SMA/EMA) + Mean Reversion (e.g., Bollinger/RSI).
2. Volatility-scaled entry thresholds (using ATR).
3. Rolling Sharpe consistency over 2020-2024.

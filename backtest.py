import pandas as pd
import numpy as np
import importlib.util
import sys
import os

def load_data():
    # Placeholder for actual BTC-USD data loading
    # In a real run, this loads a fixed CSV from /data
    dates = pd.date_range(start="2020-01-01", end="2024-01-01", freq='D')
    df = pd.DataFrame(index=dates)
    np.random.seed(42)
    df['close'] = 100 * (1 + np.random.normal(0.001, 0.02, len(dates))).accumprod()
    df['high'] = df['close'] * 1.01
    df['low'] = df['close'] * 0.99
    df['open'] = df['close'].shift(1).fillna(100)
    df['volume'] = np.random.uniform(1000, 5000, len(dates))
    return df

def evaluate(strategy_file="strategy.py"):
    df = load_data()
    
    # Dynamic import of the agent-generated strategy
    spec = importlib.util.spec_from_file_location("strategy", strategy_file)
    strat_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(strat_mod)
    
    signals = strat_mod.generate_signals(df)
    
    # Compute Returns
    df['returns'] = df['close'].pct_change()
    df['strat_returns'] = signals.shift(1) * df['returns']
    
    # Metrics
    n_trades = len(signals[signals.diff() != 0])
    if n_trades < 30:
        return {"score": -1.0, "reason": "Insufficient trades"}
        
    sharpe = (df['strat_returns'].mean() / df['strat_returns'].std()) * np.sqrt(365)
    max_dd = (df['strat_returns'].cumsum().cummax() - df['strat_returns'].cumsum()).max()
    
    return {
        "score": float(sharpe),
        "sharpe": float(sharpe),
        "max_drawdown": float(max_dd),
        "n_trades": int(n_trades)
    }

if __name__ == "__main__":
    print(evaluate())

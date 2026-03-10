import pandas as pd
import numpy as np
import importlib.util
import sys
import os

def load_data():
    csv_path = os.path.join(os.path.dirname(__file__), "data/btc_daily.csv")
    if os.path.exists(csv_path):
        # YFinance CSVs sometimes have multi-line headers (Ticker row + blank row)
        df = pd.read_csv(csv_path, index_col=0, parse_dates=True, skiprows=[1, 2])
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        df.columns = [c.lower() for c in df.columns]
        
        # Ensure numeric
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df = df.dropna()
        return df
    
    # Fallback to placeholder
    dates = pd.date_range(start="2020-01-01", end="2024-01-01", freq='D')
    df = pd.DataFrame(index=dates)
    np.random.seed(42)
    df['close'] = 100 * (1 + np.random.normal(0.001, 0.02, len(dates))).accumprod()
    df['high'] = df['close'] * 1.01
    df['low'] = df['close'] * 0.99
    df['open'] = df['close'].shift(1).fillna(100)
    df['volume'] = np.random.uniform(1000, 5000, len(dates))
    return df

def evaluate(strategy_file=None):
    if strategy_file is None:
        strategy_file = os.path.join(os.path.dirname(__file__), "strategy.py")
        
    df = load_data()
    
    # Dynamic import
    spec = importlib.util.spec_from_file_location("strategy", strategy_file)
    strat_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(strat_mod)
    
    signals = strat_mod.generate_signals(df)
    
    # Compute Returns
    df['returns'] = df['close'].pct_change()
    df['strat_returns'] = signals.shift(1) * df['returns']
    
    # Metrics
    n_trades = len(signals[signals.diff() != 0])
    if n_trades < 10:
        return {"score": -1.0, "reason": f"Insufficient trades: {n_trades}"}
        
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

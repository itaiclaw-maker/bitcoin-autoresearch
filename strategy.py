import pandas as pd
import numpy as np

def generate_signals(df):
    """
    Agent-editable signal logic.
    Returns a series of -1 (short), 0 (flat), or 1 (long).
    """
    # Base strategy: Simple Moving Average Crossover
    fast_ma = df['close'].rolling(window=20).mean()
    slow_ma = df['close'].rolling(window=50).mean()
    
    signals = np.where(fast_ma > slow_ma, 1, 0)
    return pd.Series(signals, index=df.index)

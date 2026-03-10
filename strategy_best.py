import pandas as pd
import numpy as np

def generate_signals(df):
    """
    Improved Strategy: EMA Crossover + RSI Filter
    """
    # 1. EMA Crossover
    ema_fast = df['close'].ewm(span=12, adjust=False).mean()
    ema_slow = df['close'].ewm(span=26, adjust=False).mean()
    
    # 2. RSI Filter (14 period)
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    # Logic: 
    # Long: EMA Fast > EMA Slow AND RSI > 50
    # Flat: Otherwise
    signals = np.where((ema_fast > ema_slow) & (rsi > 50), 1, 0)
    
    return pd.Series(signals, index=df.index)

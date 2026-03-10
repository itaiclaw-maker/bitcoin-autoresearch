import pandas as pd
import numpy as np

def generate_signals(df):
    """
    Iteration 2: Volatility-Adjusted EMA Crossover
    Uses ATR to scale entry thresholds and avoid whipsaws in low-volatility regimes.
    """
    # 1. EMAs
    ema_fast = df['close'].ewm(span=10, adjust=False).mean()
    ema_slow = df['close'].ewm(span=30, adjust=False).mean()
    
    # 2. ATR (Volatility)
    high_low = df['high'] - df['low']
    high_close = np.abs(df['high'] - df['close'].shift())
    low_close = np.abs(df['low'] - df['close'].shift())
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = tr.rolling(14).mean()
    
    # 3. RSI Filter (14 period)
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    # Logic: 
    # Long if EMA cross AND current price is 0.2*ATR above the slow EMA
    # AND RSI is bullish (> 50)
    buffer = 0.2 * atr
    signals = np.where((ema_fast > (ema_slow + buffer)) & (rsi > 50), 1, 0)
    
    return pd.Series(signals, index=df.index)

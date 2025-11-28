import ta, numpy as np

def compute_indicators(df):
    close = df['close']
    high = df['high']
    low = df['low']

    try:
        rsi = float(ta.momentum.RSIIndicator(close=close, window=14).rsi().iloc[-1])
    except Exception:
        rsi = None

    macd_ind = ta.trend.MACD(close=close, window_slow=26, window_fast=12, window_sign=9)
    macd = macd_ind.macd().iloc[-1] if not macd_ind.macd().isnull().all() else None
    macd_signal = macd_ind.macd_signal().iloc[-1] if not macd_ind.macd_signal().isnull().all() else None

    ema8 = ta.trend.EMAIndicator(close=close, window=8).ema_indicator().iloc[-1]
    ema21 = ta.trend.EMAIndicator(close=close, window=21).ema_indicator().iloc[-1]
    sma50 = ta.trend.SMAIndicator(close=close, window=50).sma_indicator().iloc[-1]
    adx = ta.trend.ADXIndicator(high=high, low=low, close=close, window=14).adx().iloc[-1]

    bb = ta.volatility.BollingerBands(close=close, window=20, window_dev=2)
    bb_h = bb.bollinger_hband().iloc[-1]
    bb_l = bb.bollinger_lband().iloc[-1]

    stoch = ta.momentum.StochasticOscillator(high=high, low=low, close=close, window=14, smooth_window=3)
    stoch_k = stoch.stoch().iloc[-1]
    stoch_d = stoch.stoch_signal().iloc[-1]

    last_close = float(close.iloc[-1])

    return {
        'rsi': None if rsi is None else float(rsi),
        'macd': None if macd is None else float(macd),
        'macd_signal': None if macd_signal is None else float(macd_signal),
        'ema8': float(ema8),
        'ema21': float(ema21),
        'sma50': float(sma50),
        'adx': float(adx),
        'bb_h': float(bb_h),
        'bb_l': float(bb_l),
        'stoch_k': float(stoch_k),
        'stoch_d': float(stoch_d),
        'last_close': last_close
    }

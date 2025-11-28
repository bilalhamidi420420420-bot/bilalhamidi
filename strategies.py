def vote_signal(ind):
    votes_long = 0
    votes_short = 0
    if ind.get('rsi') is not None:
        if ind['rsi'] < 30: votes_long += 1
        elif ind['rsi'] > 70: votes_short += 1
    if ind.get('macd') is not None and ind.get('macd_signal') is not None:
        if ind['macd'] > ind['macd_signal']: votes_long += 1
        else: votes_short += 1
    if ind.get('ema8') and ind.get('ema21'):
        if ind['ema8'] > ind['ema21']: votes_long += 1
        else: votes_short += 1
    if ind.get('last_close') and ind.get('sma50'):
        if ind['last_close'] > ind['sma50']: votes_long += 1
        else: votes_short += 1
    if ind.get('adx') and ind['adx'] < 20:
        votes_long = max(0, votes_long-1); votes_short = max(0, votes_short-1)
    if ind.get('bb_h') and ind.get('bb_l') and ind.get('last_close'):
        if ind['last_close'] >= ind['bb_h']: votes_short += 1
        elif ind['last_close'] <= ind['bb_l']: votes_long += 1
    if ind.get('stoch_k') and ind.get('stoch_d'):
        if ind['stoch_k'] > ind['stoch_d'] and ind['stoch_k'] < 80: votes_long +=1
        elif ind['stoch_k'] < ind['stoch_d'] and ind['stoch_k'] > 20: votes_short +=1
    if votes_long >= votes_short + 2:
        signal = 'LONG'
    elif votes_short >= votes_long + 2:
        signal = 'SHORT'
    else:
        signal = 'HOLD'
    total = votes_long + votes_short
    confidence = round(abs(votes_long - votes_short) / total, 3) if total>0 else 0.0
    return {'signal':signal,'votes_long':votes_long,'votes_short':votes_short,'confidence':confidence}

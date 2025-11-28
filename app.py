from flask import Flask, request, jsonify
from data_fetcher import fetch_klines
from indicators import compute_indicators
from strategies import vote_signal
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({'status':'ok','service':'CryptoProBot API'})

@app.route('/analyze', methods=['GET','POST'])
def analyze():
    params = request.get_json(silent=True) or request.args.to_dict()
    symbol = params.get('symbol','BTCUSDT')
    timeframe = params.get('timeframe','15m')
    limit = int(params.get('limit',500))
    try:
        df = fetch_klines(symbol=symbol, interval=timeframe, limit=limit)
    except Exception as e:
        return jsonify({'error':'fetch_failed','detail':str(e)}), 502
    try:
        ind = compute_indicators(df)
        vote = vote_signal(ind)
    except Exception as e:
        return jsonify({'error':'indicator_failed','detail':str(e)}), 500
    return jsonify({'symbol':symbol,'timeframe':timeframe,'indicators':ind,'vote':vote})

if __name__ == '__main__':
    port = int(os.environ.get('PORT',8000))
    app.run(host='0.0.0.0', port=port)

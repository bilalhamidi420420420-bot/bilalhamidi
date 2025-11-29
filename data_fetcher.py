import requests
import pandas as pd

OKX_CANDLES_URL = "https://www.okx.com/api/v5/market/candles"

TF_MAP = {
    "1m": "1m",
    "3m": "3m",
    "5m": "5m",
    "15m": "15m",
    "30m": "30m",
    "1h": "1H",
    "4h": "4H",
    "1d": "1D"
}

def fetch_klines(symbol="BTCUSDT", interval="15m", limit=200):

    # تبدیل سمبل بایننس به OKX
    if "-" in symbol:
        inst_id = symbol
    else:
        if symbol.endswith("USDT"):
            inst_id = symbol[:-4] + "-USDT"
        else:
            inst_id = symbol[:-3] + "-" + symbol[-3:]

    bar = TF_MAP.get(interval.lower(), interval)

    params = {
        "instId": inst_id,
        "bar": bar,
        "limit": str(limit)
    }

    r = requests.get(OKX_CANDLES_URL, params=params)
    data = r.json()

    if data.get("code") != "0":
        raise Exception(f"OKX Error: {data}")

    rows = []
    for item in data["data"]:
        ts = int(item[0])
        o = float(item[1])
        h = float(item[2])
        l = float(item[3])
        c = float(item[4])
        v = float(item[5])
        rows.append([ts, o, h, l, c, v])

    rows.reverse()

    df = pd.DataFrame(rows, columns=["timestamp","open","high","low","close","volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)

    return df

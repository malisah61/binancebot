"""Binance herkese açık piyasa verisi (API anahtarı gerekmez)."""
import time
import requests

# GitHub Actions sunucuları ABD'de; api.binance.com oradan 451 verir.
# data-api.binance.vision herkese açık piyasa verisi için Binance'in resmi aynasıdır.
HOSTS = ["https://data-api.binance.vision", "https://api.binance.com", "https://api1.binance.com"]
STABLE = {"USDC", "FDUSD", "TUSD", "BUSD", "DAI", "USDP", "EUR", "EURI", "AEUR", "USDE", "XUSD",
          "PAXG", "WBTC", "WBETH", "BFUSD", "USD1", "TRY", "BRL", "GBP", "XAUT", "RLUSD", "PYUSD", "USDS"}
# Kripto olmayan varlıklar (tokenize hisse/emtia) — farklı piyasa saatleri ve dinamikleri var
NON_CRYPTO = {"MSTRB", "SPCXB", "TSLAB", "NVDAB", "AAPLB", "COINB", "HOODB", "AMZNB", "GOOGLB", "METAB", "MSFTB",
              "CRCLB", "SPYB", "QQQB", "XAU", "XAG"}
_session = requests.Session()


def get(path, params=None, tries=3):
    err = None
    for host in HOSTS:
        for i in range(tries):
            try:
                r = _session.get(host + path, params=params, timeout=15)
                if r.status_code == 200:
                    return r.json()
                if r.status_code in (418, 429):
                    time.sleep(2 + i * 3)
                    continue
                err = f"{host} {r.status_code}"
                break
            except requests.RequestException as e:
                err = str(e)
                time.sleep(1)
    raise RuntimeError(f"Binance isteği başarısız: {path} ({err})")


def top_usdt(n=100):
    t = get("/api/v3/ticker/24hr")
    rows = []
    for x in t:
        s = x["symbol"]
        if not s.endswith("USDT"):
            continue
        base = s[:-4]
        if base in STABLE or base in NON_CRYPTO or base.endswith(("UP", "DOWN", "BULL", "BEAR")):
            continue
        if float(x["quoteVolume"]) <= 0 or int(x.get("count", 0)) == 0:
            continue
        rows.append(x)
    rows.sort(key=lambda x: float(x["quoteVolume"]), reverse=True)
    return rows[:n]


def klines(symbol, interval="1h", limit=1000):
    raw = get("/api/v3/klines", {"symbol": symbol, "interval": interval, "limit": limit})
    return [{"t": int(r[0]), "o": float(r[1]), "h": float(r[2]), "l": float(r[3]), "c": float(r[4]),
             "v": float(r[5]), "qv": float(r[7]), "tb": float(r[9]), "tq": float(r[10])} for r in raw]


def depth(symbol, limit=500):
    return get("/api/v3/depth", {"symbol": symbol, "limit": limit})


def agg_trades(symbol, limit=1000):
    return get("/api/v3/aggTrades", {"symbol": symbol, "limit": limit})


def prices():
    return {x["symbol"]: float(x["price"]) for x in get("/api/v3/ticker/price")}

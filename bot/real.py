"""GERÇEK Binance Futures hesabı — yalnızca Hetzner sunucusunda çalışır (GitHub Actions'ta çalışmayı reddeder).

Ne yapar (her 5 dakikada bir, systemd zamanlayıcısıyla):
  1) Açık/bekleyen emirleri senkronize eder (executor.sync): limit dolduysa stop + TP1 (yarısı) + TP2 koyar, TP1 sonrası
     stop girişe çekilir, süre dolunca kapatır, kapanan işlemin gerçek kâr/zararını yazar.
  2) Yalnız TEST dönemini geçmiş ("doğrulandı") uç-hareket kurulumlarını arar (state/extreme.json → picks[*].adopted).
     Olay son kapanmış 1s mumda olmuşsa, kurulumun limit emrini (ör. düşüşün %38.2 tepkisine SHORT) koyar.

Sınırlar (sabit): 3x kaldıraç, işlem başı marjin bakiyenin %15'i, en çok 3 açık/bekleyen işlem, günlük %5 zarar limiti,
izole marjin. Bakiye = Futures cüzdanına aktardığın tutar; bot bundan fazlasını kullanamaz.
Kontrol: Telegram /gercekdur · /gercekdevam · /gercekkapat (bot-loop yazar → state/gercek_kontrol.json → sunucu çeker).
"""
from __future__ import annotations

import json
import os
import sys
import time

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
import executor  # noqa: E402
import extreme as X  # noqa: E402
import telegram  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.environ.get("GERCEK_STATE", os.path.expanduser("~/gercek.json"))
DRY = os.environ.get("GERCEK_DRY") == "1"
LIMITS = {"lev": 3, "margin_frac": 0.15, "max_pos": 3, "daily_loss": 0.05}
REAL_HOST = "https://fapi.binance.com"


class Real(executor.Demo):
    def __init__(self):
        super().__init__()
        self.s.headers["X-MBX-APIKEY"] = os.environ.get("BINANCE_REAL_KEY", "").strip()
        self.secret = os.environ.get("BINANCE_REAL_SECRET", "").strip()

    def _find_base(self):
        r = self.s.get(REAL_HOST + "/fapi/v1/time", timeout=10)
        r.raise_for_status()
        self.base = REAL_HOST
        self.offset = r.json()["serverTime"] - int(time.time() * 1000)

    def req(self, method, path, params=None, signed=True):
        if DRY and method != "GET":
            print("[DENEME] gönderilmedi:", method, path, params)
            return {"orderId": -1, "status": "NEW", "executedQty": "0", "avgPrice": "0", "algoId": -1}
        old = executor.SECRET
        executor.SECRET = self.secret          # imzayı gerçek anahtarla at
        try:
            return super().req(method, path, params, signed)
        finally:
            executor.SECRET = old


def klines(R, sym, n=800):
    raw = R.req("GET", "/fapi/v1/klines", {"symbol": sym, "interval": "1h", "limit": n}, signed=False)
    k = pd.DataFrame([{"t": int(r[0]), "o": float(r[1]), "h": float(r[2]), "l": float(r[3]), "c": float(r[4]),
                       "qv": float(r[7]), "tq": float(r[10])} for r in raw])
    return k


def candidates(R, picks, rank, done):
    """Doğrulanmış kurulumlar için son kapanmış mumda olay var mı → limit emir planları."""
    now = int(time.time() * 1000)
    bk = klines(R, "BTCUSDT", 800)
    bk = bk[bk["t"] + 3600_000 <= now].reset_index(drop=True)
    btc30 = float(bk["c"].iloc[-1] / bk["c"].iloc[-721] - 1) * 100
    regime = "BTC düşüşte" if btc30 < 0 else "BTC yükselişte"
    out = []
    for ev, p in picks.items():
        if p["regime"] not in ("tümü", regime):
            continue
        syms = [s for s, r in rank.items() if "tümü" in p["tiers"] or X.tier_of(r) in p["tiers"]]
        for s in syms:
            try:
                k = klines(R, s)
            except Exception:
                continue
            k = k[k["t"] + 3600_000 <= now].reset_index(drop=True)      # yalnız kapanmış mumlar
            if len(k) < 800:
                continue
            for e in X.events(s, k, "fut", rank[s], label=False):
                if e["ev"] != ev or e["th"] != p["th"] or now - (e["t"] + 3600_000) > 2 * 3600_000:
                    continue
                key = f"{s}|{ev}|{e['t']}"
                if key in done:
                    continue
                o, h, l, c = (k[q].values.astype(float) for q in "ohlc")
                i = int(np.where(k["t"].values == e["t"])[0][0])
                pl = X.plan(ev, p["name"], o, h, l, c, i, e["atr"], e["lo24"], e["hi24"])
                done[key] = now
                if pl is None:
                    continue
                entry, stop, mode, j = pl
                d = X.VARIANTS[ev][p["name"]][0]
                after_h, after_l = h[i + 1:], l[i + 1:]
                if len(after_h) and ((d == -1 and after_h.max() >= entry) or (d == 1 and after_l.min() <= entry)):
                    continue                                              # seviye çoktan görülmüş → kaçırıldı, kovalanmaz
                risk = abs(entry - stop)
                wait_h = X.FIB_WAIT if mode == "fib" else X.WAIT
                out.append({"sym": s, "dir": d, "desc": X.VARIANTS[ev][p["name"]][2],
                            "plan": {"entry": entry, "sl": stop, "tp1": entry + d * 1.5 * risk, "tp2": entry + d * 3 * risk,
                                     "expire_t": e["t"] + 3600_000 + wait_h * 3600_000, "until_ms": X.HOLD * 3600_000,
                                     "score": round(e["size"], 1)}})
    return out, regime


def main():
    if os.environ.get("GITHUB_ACTIONS"):
        raise SystemExit("Gerçek hesap modülü GitHub Actions'ta çalıştırılamaz.")
    chat = os.environ.get("TELEGRAM_CHAT_ID")
    executor.CFG.update(LIMITS)
    R = Real()
    ds = json.load(open(STATE)) if os.path.exists(STATE) else executor.new_state() | {"done": {}}
    ds.setdefault("done", {})
    ctl = {}
    try:
        ctl = json.load(open(os.path.join(ROOT, "state", "gercek_kontrol.json")))
    except Exception:
        pass
    ds["paused"] = bool(ctl.get("paused", False))
    close_all = ctl.get("close_all_t", 0) > ds.get("close_all_done", 0)
    msgs = []
    executor.sync(R, ds, msgs, close_all=close_all)
    if close_all:
        ds["close_all_done"] = ctl["close_all_t"]
        ds["paused"] = True
        msgs.append("⏹ Tüm gerçek pozisyonlar ve bekleyen emirler kapatıldı; bot duraklatıldı.")
    eq, last = ds.get("equity", 0), ds.get("eq_reported")
    if ctl.get("rapor_t", 0) > ds.get("rapor_done", 0) or last is None or abs(eq - last) > max(1.0, 0.1 * last):
        ds["eq_reported"], ds["rapor_done"] = eq, ctl.get("rapor_t", 0)
        min_need = 5 / (LIMITS["margin_frac"] * LIMITS["lev"]) * 1.1
        msgs.append(f"💰 Gerçek Futures bakiyesi: {eq:.2f} USDT · açık {len(ds['positions'])} · bekleyen {len(ds['pending'])}"
                    f"{' · ⏸ duraklatıldı' if ds['paused'] else ''}"
                    + (f"\n⚠️ Binance'in en küçük emir tutarı (~5 $) nedeniyle bot en az ~{min_need:.0f} USDT ile işlem açabilir." if eq < min_need else ""))
    rep = json.load(open(os.path.join(ROOT, "state", "extreme.json")))
    picks = {ev: p for ev, p in rep.get("picks", {}).items() if p.get("adopted")}
    rank = rep.get("rank_hist") or {}
    if not rank:
        msgs.append("ℹ️ extreme.json'da katman bilgisi yok, bu tur atlandı.")
    elif picks and not ds["paused"] and not ds.get("halted") and ds.get("equity", 0) >= 5 / (LIMITS["margin_frac"] * LIMITS["lev"]):
        cands, regime = candidates(R, picks, rank, ds["done"])
        for c in cands:
            try:
                executor.place_limit(R, ds, c["sym"], c["dir"], c["plan"], msgs)
            except executor.BinanceError as e:
                ds["errors"].append(f"{c['sym']} limit hatası: {e}")
        cutoff = int(time.time() * 1000) - 7 * 86400_000
        ds["done"] = {k: v for k, v in ds["done"].items() if v > cutoff}
    json.dump(ds, open(STATE + ".tmp", "w"), ensure_ascii=False, default=float)
    os.replace(STATE + ".tmp", STATE)
    msgs = [m.replace("🧪", "💰").replace("DEMO", "GERÇEK") for m in msgs]
    hour = time.gmtime().tm_hour
    if msgs:
        telegram.send(chat, "\n".join(msgs))
    if hour == 5 and time.gmtime().tm_min < 5:                     # her sabah 08:00 (TR) özet
        cl = ds["closed"]
        telegram.send(chat, f"💰 <b>Gerçek hesap</b> — bakiye {ds.get('equity', 0):.2f} USDT{' · ⏸ duraklatıldı' if ds['paused'] else ''}\n"
                            f"Açık {len(ds['positions'])} · bekleyen {len(ds['pending'])} · kapanan {len(cl)} · toplam {sum(x['pnl'] for x in cl):+.2f}$\n"
                            f"Kurulumlar: {', '.join(p['desc'] for p in picks.values()) or 'doğrulanmış kurulum yok (işlem açılmaz)'}")
    print("\n".join(msgs) or "değişiklik yok")


if __name__ == "__main__":
    main()

// KANTİTATİF KARAR MOTORU V5 — saf JavaScript, bağımlılık yok.
// Ağırlıklar: Trend 20, Momentum 18, Open Interest 15, Hacim 10, Funding+L/S 10,
// Emir defteri 10, FVG+Likidite avı 10, VWAP 5. Eksik veri (ör. futures yok) varsa
// ağırlıklar kalan bileşenlere göre yeniden ölçeklenir.
(function (G) {
  const N = (a) => a.length;
  const last = (a, i = 1) => a[a.length - i];
  const clip = (x, a = -1, b = 1) => Math.max(a, Math.min(b, x));
  const sign = Math.sign;
  const avg = (a) => (a.length ? a.reduce((x, y) => x + y, 0) / a.length : 0);
  function ema(x, n) { const o = new Array(N(x)); const a = 2 / (n + 1); o[0] = x[0]; for (let i = 1; i < N(x); i++) o[i] = a * x[i] + (1 - a) * o[i - 1]; return o; }
  function rma(x, n) { const o = new Array(N(x)); const a = 1 / n; o[0] = x[0]; for (let i = 1; i < N(x); i++) o[i] = a * x[i] + (1 - a) * o[i - 1]; return o; }
  function sma(x, n) { const o = new Array(N(x)).fill(NaN); let s = 0; for (let i = 0; i < N(x); i++) { s += x[i]; if (i >= n) s -= x[i - n]; if (i >= n - 1) o[i] = s / n; } return o; }
  function rstd(x, n) { const o = new Array(N(x)).fill(NaN); for (let i = n - 1; i < N(x); i++) { let m = 0; for (let j = i - n + 1; j <= i; j++) m += x[j]; m /= n; let v = 0; for (let j = i - n + 1; j <= i; j++) v += (x[j] - m) ** 2; o[i] = Math.sqrt(v / n); } return o; }
  const diff = (x) => x.map((v, i) => (i ? v - x[i - 1] : 0));
  function rsi(c, n = 14) { const d = diff(c); const g = rma(d.map((v) => Math.max(v, 0)), n), l = rma(d.map((v) => Math.max(-v, 0)), n); return g.map((v, i) => 100 - 100 / (1 + v / (l[i] || 1e-12))); }
  function macd(c) { const f = ema(c, 12), s = ema(c, 26); const m = f.map((v, i) => v - s[i]); const sg = ema(m, 9); return { m, sg, h: m.map((v, i) => v - sg[i]) }; }
  function trange(h, l, c) { return h.map((v, i) => { const pc = i ? c[i - 1] : c[0]; return Math.max(v - l[i], Math.abs(v - pc), Math.abs(l[i] - pc)); }); }
  function obv(c, v) { let s = 0; return c.map((x, i) => (s += (i ? sign(x - c[i - 1]) : 0) * v[i])); }
  function slopeNorm(y, n = 20) { y = y.slice(-n); const m = N(y); const xm = (m - 1) / 2, ym = avg(y); let nu = 0, de = 0; for (let i = 0; i < m; i++) { nu += (i - xm) * (y[i] - ym); de += (i - xm) ** 2; } let sc = 0; for (let i = 1; i < m; i++) sc += Math.abs(y[i] - y[i - 1]); sc = sc / (m - 1) || 1e-12; return nu / de / sc; }
  function percentile(a, p) { a = a.filter((x) => !isNaN(x)).sort((x, y) => x - y); if (!a.length) return NaN; const k = (a.length - 1) * p / 100, f = Math.floor(k); return f + 1 < a.length ? a[f] + (a[f + 1] - a[f]) * (k - f) : a[f]; }

  function resample(k, ms) { const out = []; let cur = null, key = null; for (const c of k) { const g = Math.floor(c.t / ms); if (g !== key) { if (cur) out.push(cur); key = g; cur = { ...c }; } else { cur.h = Math.max(cur.h, c.h); cur.l = Math.min(cur.l, c.l); cur.c = c.c; for (const f of ["v", "qv", "tb", "tq"]) cur[f] += c[f]; } } if (cur) out.push(cur); return out; }

  // ---- Akıllı para yapıları
  function findFvg(k, look = 60) {
    const out = []; const n = N(k);
    for (let i = Math.max(2, n - look); i < n; i++) {
      const a = k[i - 2], c = k[i];
      if (c.l > a.h) { // boğa boşluğu: [a.h, c.l]
        let filled = false; for (let j = i + 1; j < n; j++) if (k[j].l <= a.h) { filled = true; break; }
        out.push({ type: "bull", bottom: a.h, top: c.l, i, t: c.t, filled });
      } else if (c.h < a.l) { // ayı boşluğu: [c.h, a.l]
        let filled = false; for (let j = i + 1; j < n; j++) if (k[j].h >= a.l) { filled = true; break; }
        out.push({ type: "bear", bottom: c.h, top: a.l, i, t: c.t, filled });
      }
    }
    return out;
  }
  function findSweeps(k, look = 20, recent = 3) {
    const out = []; const n = N(k);
    for (let i = Math.max(look, n - recent); i < n; i++) {
      let ph = -Infinity, pl = Infinity; for (let j = i - look; j < i; j++) { ph = Math.max(ph, k[j].h); pl = Math.min(pl, k[j].l); }
      if (k[i].h > ph && k[i].c < ph) out.push({ type: "BSL", level: ph, i, ago: n - 1 - i });
      if (k[i].l < pl && k[i].c > pl) out.push({ type: "SSL", level: pl, i, ago: n - 1 - i });
    }
    return out;
  }

  // ---- Destek/direnç (pivot kümeleri + hacim profili) ve Fibonacci
  function srLevels(h, l, c, v, A) {
    const pts = []; const K = 5;
    for (let i = K; i < N(h) - K; i++) { let mh = -Infinity, ml = Infinity; for (let j = i - K; j <= i + K; j++) { mh = Math.max(mh, h[j]); ml = Math.min(ml, l[j]); } if (h[i] === mh) pts.push(h[i]); if (l[i] === ml) pts.push(l[i]); }
    pts.sort((a, b) => a - b); const tol = Math.max(A * 0.6, last(c) * 0.002); const cl = [];
    for (const p of pts) { const z = cl[cl.length - 1]; if (z && p - z.last <= tol) { z.sum += p; z.n++; z.last = p; } else cl.push({ sum: p, n: 1, last: p }); }
    const levels = cl.map((z) => ({ price: z.sum / z.n, touches: z.n, src: "pivot" }));
    const m = Math.min(300, N(c)); const lo = Math.min(...l.slice(-m)), hi = Math.max(...h.slice(-m)); let poc = null;
    if (hi > lo) { const bins = 40, hist = new Array(bins).fill(0); for (let i = N(c) - m; i < N(c); i++) { const tp = (h[i] + l[i] + c[i]) / 3; hist[Math.min(bins - 1, Math.max(0, Math.floor((tp - lo) / (hi - lo) * bins)))] += v[i]; }
      const cen = (i) => lo + (i + 0.5) * (hi - lo) / bins; let mi = 0; hist.forEach((x, i) => { if (x > hist[mi]) mi = i; }); poc = cen(mi);
      hist.map((x, i) => [x, i]).sort((a, b) => a[0] - b[0]).slice(-5).forEach(([, i]) => levels.push({ price: cen(i), touches: 2, src: "hacim" })); }
    const p = last(c);
    return { sup: levels.filter((x) => x.price < p).sort((a, b) => b.price - a.price).slice(0, 4), res: levels.filter((x) => x.price > p).sort((a, b) => a.price - b.price).slice(0, 4), poc };
  }
  function fibonacci(h, l, n = 150) {
    const hh = h.slice(-n), ll = l.slice(-n); let ih = 0, il = 0; hh.forEach((x, i) => { if (x > hh[ih]) ih = i; }); ll.forEach((x, i) => { if (x < ll[il]) il = i; });
    const hi = hh[ih], lo = ll[il], up = ih > il, r = hi - lo, levels = {};
    for (const q of [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1, 1.272, 1.618]) levels[q] = up ? hi - r * q : lo + r * q;
    return { up, high: hi, low: lo, levels };
  }

  const WEIGHTS = { trend: 20, momentum: 18, oi: 15, volume: 10, deriv: 10, book: 10, smc: 10, vwap: 5 };
  const GROUP_NAMES = { trend: "Trend", momentum: "Momentum", oi: "Open Interest", volume: "Hacim", deriv: "Funding + L/S", book: "Emir defteri", smc: "FVG + Likidite avı", vwap: "VWAP" };

  function decision(s, lt = 58, st = 42.99) { const sl = Math.max(70, lt + 10), ss = Math.min(30, st - 10); return s >= sl ? "GÜÇLÜ LONG" : s >= lt ? "LONG" : s > st ? "NEUTRAL" : s >= ss ? "SHORT" : "GÜÇLÜ SHORT"; }

  // opt: {htfMs, oi:[{t,oi}], gls:[{t,r}], tls:[{t,r}], funding, book:{bids,asks}, trades:[{p,q,m,T}]}
  function analyze(k, opt = {}) {
    const h = k.map((x) => x.h), l = k.map((x) => x.l), c = k.map((x) => x.c), o = k.map((x) => x.o), v = k.map((x) => x.v), qv = k.map((x) => x.qv), tq = k.map((x) => x.tq);
    const price = last(c); const M = {}; const T = []; // M: metrikler, T: tetikleyiciler
    const trig = (dir, text) => T.push({ dir, text });
    const e20 = ema(c, 20), e50 = ema(c, 50), e200 = ema(c, 200);
    const A = last(rma(trange(h, l, c), 14)); M.atr = A; M.atrPct = A / price * 100;
    const parts = {};

    // 1) TREND
    const t1 = (sign(price - last(e50)) + sign(price - last(e200)) + sign(last(e20) - last(e50)) + sign(last(e50) - last(e50, 6))) / 4;
    M.ema20 = last(e20); M.ema50 = last(e50); M.ema200 = last(e200);
    M.emaOrder = last(e20) > last(e50) && last(e50) > last(e200) ? "boğa" : last(e20) < last(e50) && last(e50) < last(e200) ? "ayı" : "karışık";
    let t4 = null; const k4 = resample(k, opt.htfMs || 4 * 3600e3);
    if (N(k4) >= 60) { const c4 = k4.map((x) => x.c), a4 = ema(c4, 21), b4 = ema(c4, 55); t4 = (sign(last(c4) - last(a4)) + sign(last(a4) - last(b4)) + sign(last(a4) - last(a4, 4))) / 3; }
    M.htf = t4;
    parts.trend = t4 === null ? t1 : 0.6 * t1 + 0.4 * t4;
    if (M.emaOrder === "boğa" && price > last(e20)) trig(1, "EMA20 > EMA50 > EMA200: tam boğa dizilimi");
    if (M.emaOrder === "ayı" && price < last(e20)) trig(-1, "EMA20 < EMA50 < EMA200: tam ayı dizilimi");
    for (let i = 1; i <= 3; i++) { if (last(e50, i) > last(e200, i) && last(e50, i + 1) <= last(e200, i + 1)) trig(1, "Golden cross (EMA50 EMA200'ü yukarı kesti)"); if (last(e50, i) < last(e200, i) && last(e50, i + 1) >= last(e200, i + 1)) trig(-1, "Death cross (EMA50 EMA200'ü aşağı kesti)"); }

    // 2) MOMENTUM: RSI + MACD + Z-Score
    const r = rsi(c); const R = last(r); M.rsi = R;
    let rP = R > 78 ? -0.6 : R > 65 ? 0.3 : R >= 50 ? 0.7 : R >= 40 ? -0.4 : R >= 25 ? -0.6 : 0.4; rP += last(r) > last(r, 4) ? 0.3 : -0.3;
    const MC = macd(c), mh = MC.h; M.macdH = last(mh); M.macdUp = last(mh) > last(mh, 2);
    let mP = (last(mh) > 0 ? 0.5 : -0.5) + (M.macdUp ? 0.5 : -0.5); M.macdCross = null;
    for (let i = 1; i < 4; i++) { if (last(mh, i) > 0 && last(mh, i + 1) <= 0) { mP += 0.3; M.macdCross = "AL"; break; } if (last(mh, i) < 0 && last(mh, i + 1) >= 0) { mP -= 0.3; M.macdCross = "SAT"; break; } }
    const bm = sma(c, 20), bs = rstd(c, 20); const z = (price - last(bm)) / (last(bs) || 1e-12); M.z = z;
    const bu = bm.map((x, i) => x + 2 * bs[i]), bl = bm.map((x, i) => x - 2 * bs[i]); M.pb = (price - last(bl)) / ((last(bu) - last(bl)) || 1e-12);
    const bw = bm.map((x, i) => (bu[i] - bl[i]) / x); M.bbw = last(bw) * 100; M.squeeze = last(bw) < percentile(bw.slice(-120), 20);
    const zP = Math.abs(z) > 2.5 ? -sign(z) * 0.6 : clip(z / 2) * 0.5;
    parts.momentum = clip(0.35 * clip(rP) + 0.45 * clip(mP) + 0.2 * zP);
    if (R > 75) trig(-1, `RSI ${R.toFixed(0)}: aşırı alım`); if (R < 25) trig(1, `RSI ${R.toFixed(0)}: aşırı satım (tepki ihtimali)`);
    if (M.macdCross === "AL") trig(1, "MACD yeni AL kesişimi"); if (M.macdCross === "SAT") trig(-1, "MACD yeni SAT kesişimi");
    if (z > 2.5) trig(-1, `Z-Score +${z.toFixed(1)}: fiyat ortalamadan aşırı uzaklaştı`); if (z < -2.5) trig(1, `Z-Score ${z.toFixed(1)}: aşırı satılmış, ortalamaya dönüş ihtimali`);
    if (M.squeeze) trig(0, "Bollinger sıkışması: sert hareket yakın olabilir");

    // 3) OPEN INTEREST + REJİM
    M.regime = null;
    if (opt.oi && N(opt.oi) >= 7) {
      const oi = opt.oi; const dOI = last(oi).oi / oi[N(oi) - 7].oi - 1; const dP = price / c[Math.max(0, N(c) - 7)] - 1;
      M.oiChg = dOI * 100; M.oiVal = last(oi).oi; M.pChg = dP * 100;
      const mag = clip(Math.abs(dOI) / 0.05, 0.2, 1);
      let s = 0;
      if (Math.abs(dOI) < 0.005) { M.regime = "Nötr (OI değişmiyor)"; s = 0; }
      else if (dP >= 0 && dOI > 0) { M.regime = "Long Baskısı"; s = mag; }
      else if (dP < 0 && dOI > 0) { M.regime = "Short Baskısı"; s = -mag; }
      else if (dP >= 0 && dOI < 0) { M.regime = "Short Squeeze"; s = 0.5 * mag; }
      else { M.regime = "Long Tasfiyesi"; s = -0.5 * mag; }
      parts.oi = s;
      if (M.regime !== "Nötr (OI değişmiyor)") trig(sign(s), `Fiyat ${dP >= 0 ? "↑" : "↓"} OI ${dOI >= 0 ? "↑" : "↓"} (${(dOI * 100).toFixed(1)}%): ${M.regime}`);
    }

    // 4) HACİM: RVOL + taker + OBV (+ büyük işlemler)
    const vAvg = avg(v.slice(-21, -1)); M.rvol = last(v) / (vAvg || 1e-12);
    const sum = (a, n) => a.slice(-n).reduce((x, y) => x + y, 0);
    M.taker = sum(tq, 6) / (sum(qv, 6) || 1e-12); M.taker24 = sum(tq, 24) / (sum(qv, 24) || 1e-12);
    const so = slopeNorm(obv(c, v), 20); M.obv = so;
    const rv = Math.max(M.rvol, sum(v, 3) / 3 / (vAvg || 1e-12));
    const rvP = rv > 1.5 ? sign(price - c[N(c) - 4]) * clip((rv - 1) / 2, 0, 1) : 0;
    let vP = 0.4 * clip((M.taker - 0.5) * 10) + 0.3 * Math.tanh(so * 3) + 0.3 * rvP;
    if (opt.trades && N(opt.trades) > 20) {
      const vals = opt.trades.map((x) => x.p * x.q); const thr = Math.max(percentile(vals, 95), 5000); let b = 0, s = 0; const list = [];
      opt.trades.forEach((x, i) => { if (vals[i] >= thr) { if (x.m) s += vals[i]; else b += vals[i]; list.push({ t: x.T, p: x.p, val: vals[i], side: x.m ? "SAT" : "AL" }); } });
      M.whales = { buy: b, sell: s, thr, list: list.slice(-20).reverse() }; const wn = (b - s) / ((b + s) || 1e-12); vP = 0.8 * vP + 0.2 * wn;
    }
    parts.volume = clip(vP);
    if (rv > 2) trig(sign(price - c[N(c) - 4]), `RVOL ${rv.toFixed(1)}x: hacim patlaması (${price >= c[N(c) - 4] ? "yükselişte" : "düşüşte"})`);
    if (M.taker > 0.58) trig(1, `Agresif alıcılar baskın (taker alım %${(M.taker * 100).toFixed(0)})`); if (M.taker < 0.42) trig(-1, `Agresif satıcılar baskın (taker alım %${(M.taker * 100).toFixed(0)})`);

    // 5) FUNDING + L/S
    const dP_ = [];
    if (opt.funding !== undefined && opt.funding !== null) { const f = opt.funding; M.funding = f * 100; dP_.push(f > 0.0005 ? -1 : f > 0.0002 ? -0.5 : f < -0.0003 ? 0.8 : f < 0 ? 0.3 : 0); if (f > 0.0005) trig(-1, `Funding %${(f * 100).toFixed(3)}: long'lar aşırı kalabalık`); if (f < -0.0003) trig(1, `Funding %${(f * 100).toFixed(3)}: short'lar kalabalık, squeeze ihtimali`); }
    if (opt.gls && N(opt.gls)) { const g = last(opt.gls).r; M.gls = g; M.glsChg = N(opt.gls) > 6 ? g - opt.gls[N(opt.gls) - 7].r : 0; dP_.push(g > 2.5 ? -0.8 : g > 1.8 ? -0.4 : g < 0.7 ? 0.6 : g < 1 ? 0.3 : 0); if (g > 2.5) trig(-1, `Global L/S ${g.toFixed(2)}: küçük yatırımcı aşırı long`); if (g < 0.7) trig(1, `Global L/S ${g.toFixed(2)}: küçük yatırımcı aşırı short`); }
    if (opt.tls && N(opt.tls)) { const t = last(opt.tls).r; M.tls = t; dP_.push(t > 1.3 ? 0.6 : t < 0.8 ? -0.6 : clip((t - 1) * 1.5)); if (t > 1.3) trig(1, `Top trader L/S ${t.toFixed(2)}: büyük oyuncular long`); if (t < 0.8) trig(-1, `Top trader L/S ${t.toFixed(2)}: büyük oyuncular short`); }
    if (N(dP_)) parts.deriv = clip(avg(dP_));

    // 6) EMİR DEFTERİ (OBI, ±%1)
    if (opt.book) { let b = 0, a = 0; for (const [p, q] of opt.book.bids) if (p >= price * 0.99) b += p * q; for (const [p, q] of opt.book.asks) if (p <= price * 1.01) a += p * q;
      M.obi = (b - a) / ((b + a) || 1e-12); M.bookBid = b; M.bookAsk = a; parts.book = clip(M.obi * 2);
      const walls = (arr) => arr.slice().sort((x, y) => y[0] * y[1] - x[0] * x[1]).slice(0, 3).map(([p, q]) => ({ p, val: p * q }));
      M.bidWalls = walls(opt.book.bids); M.askWalls = walls(opt.book.asks);
      if (M.obi > 0.3) trig(1, `Emir defteri alış ağırlıklı (OBI +${(M.obi * 100).toFixed(0)}%)`); if (M.obi < -0.3) trig(-1, `Emir defteri satış ağırlıklı (OBI ${(M.obi * 100).toFixed(0)}%)`); }

    // 7) FVG + LİKİDİTE AVI
    const fv = findFvg(k).filter((x) => !x.filled); const sw = findSweeps(k); M.fvg = fv.slice(-6).reverse(); M.sweeps = sw;
    let sP = 0;
    for (const s of sw) { if (s.type === "SSL") { sP += 0.7; trig(1, `SSL likidite avı: ${fmt(s.level)} altı süpürüldü, fiyat geri döndü`); } else { sP -= 0.7; trig(-1, `BSL likidite avı: ${fmt(s.level)} üstü süpürüldü, fiyat geri döndü`); } }
    const bullNear = fv.filter((x) => x.type === "bull" && x.top <= price * 1.001 && price - x.top < 2 * A).sort((a, b) => b.top - a.top)[0];
    const bearNear = fv.filter((x) => x.type === "bear" && x.bottom >= price * 0.999 && x.bottom - price < 2 * A).sort((a, b) => a.bottom - b.bottom)[0];
    const inside = fv.find((x) => price >= x.bottom && price <= x.top);
    if (bullNear) { sP += 0.3; trig(1, `Altında doldurulmamış boğa FVG: ${fmt(bullNear.bottom)}–${fmt(bullNear.top)} (destek)`); }
    if (bearNear) { sP -= 0.3; trig(-1, `Üstünde doldurulmamış ayı FVG: ${fmt(bearNear.bottom)}–${fmt(bearNear.top)} (direnç)`); }
    if (inside) sP += inside.type === "bull" ? 0.2 : -0.2;
    parts.smc = clip(sP);

    // 8) VWAP (son ~24 saat)
    const nV = Math.max(20, Math.min(N(c), Math.round(864e5 / (opt.tfMs || 36e5)))); let pv = 0, vv = 0; for (let i = N(c) - nV; i < N(c); i++) { pv += (h[i] + l[i] + c[i]) / 3 * v[i]; vv += v[i]; }
    M.vwap = pv / (vv || 1e-12); parts.vwap = Math.tanh((price - M.vwap) / (A || 1) / 2);

    // ---- SKOR
    // Ağırlıklar: öğrenilmiş model (opt.weights, işaretli olabilir) ya da varsayılan
    const W = opt.weights || WEIGHTS; let tw = 0, ts = 0, cov = 0; const comps = [];
    for (const key of Object.keys(WEIGHTS)) { const w = W[key] || 0; if (parts[key] === undefined || !w) continue; tw += Math.abs(w); ts += w * parts[key]; cov += WEIGHTS[key]; comps.push({ key, name: GROUP_NAMES[key], weight: Math.round(w * 10) / 10, score: Math.round(parts[key] * 100) / 100 }); }
    const total = ts / (tw || 1); const score = Math.round((50 + 50 * total) * 10) / 10; const dec = decision(score, opt.longTh, opt.shortTh);
    const agreement = comps.filter((x) => x.score * Math.sign(x.weight) * total > 0.05).length / (N(comps) || 1);
    const dir = score >= 50 ? 1 : -1;
    const plan = { dir, entry: price, sl: price - dir * 1.5 * A, tp1: price + dir * 1.5 * A, tp2: price + dir * 3 * A, rr1: 1, rr2: 2 };
    const SR = srLevels(h, l, c, v, A); const fib = fibonacci(h, l);
    return { price, score, decision: dec, agreement, components: comps, coverage: opt.weights ? Math.round(tw / Object.values(opt.weights).reduce((a, x) => a + Math.abs(x), 0) * 100) : cov, triggers: T, metrics: M, plan, sr: SR, fib, change: N(c) > 24 ? price / last(c, 25) - 1 : 0 };
  }

  function fmt(x) { if (x === null || x === undefined || isNaN(x)) return "-"; const a = Math.abs(x); if (a >= 1000) return x.toLocaleString("tr-TR", { maximumFractionDigits: 2 }); if (a >= 1) return x.toFixed(4); if (a === 0) return "0"; return x.toPrecision(5); }
  function money(x) { const a = Math.abs(x); return a >= 1e9 ? (x / 1e9).toFixed(2) + "B$" : a >= 1e6 ? (x / 1e6).toFixed(2) + "M$" : a >= 1e3 ? (x / 1e3).toFixed(1) + "K$" : x.toFixed(0) + "$"; }

  // ---- Fiyatlanmamış coin bulucu: liderlerle ortak hareket edip geride kalanlar
  // series: {SYM: kline dizisi}; win: lider penceresi (mum); return: liste
  function laggards(series, win, opt = {}) {
    const syms = Object.keys(series).filter((s) => N(series[s]) > 120);
    if (N(syms) < 10) return { leaders: [], list: [] };
    const tset = new Map(); for (const s of syms) for (const x of series[s].slice(-201)) tset.set(x.t, (tset.get(x.t) || 0) + 1);
    const times = [...tset.entries()].filter(([, n]) => n >= N(syms) * 0.8).map(([t]) => t).sort((a, b) => a - b);
    const ret = {}; // log getiri serileri (ortak zamanlarda)
    for (const s of syms) { const m = new Map(series[s].map((x) => [x.t, x.c])); const r = []; for (let i = 1; i < N(times); i++) { const a = m.get(times[i - 1]), b = m.get(times[i]); r.push(a && b ? Math.log(b / a) : 0); } ret[s] = r; }
    const winRet = (s) => { const k = series[s]; return last(k).c / k[Math.max(0, N(k) - 1 - win)].c - 1; };
    const ranked = syms.map((s) => [s, winRet(s)]).sort((a, b) => b[1] - a[1]);
    const leaders = ranked.slice(0, opt.nLeaders || 8).filter((x) => x[1] > 0);
    if (!N(leaders)) return { leaders: [], list: [] };
    const L = N(ret[syms[0]]); const basket = new Array(L).fill(0); for (const [s] of leaders) ret[s].forEach((x, i) => (basket[i] += x / N(leaders)));
    const basketWin = leaders.reduce((a, x) => a + x[1], 0) / N(leaders);
    const corr = (a, b) => { const ma = avg(a), mb = avg(b); let cv = 0, va = 0, vb = 0; for (let i = 0; i < N(a); i++) { cv += (a[i] - ma) * (b[i] - mb); va += (a[i] - ma) ** 2; vb += (b[i] - mb) ** 2; } return { r: cv / Math.sqrt(va * vb || 1e-24), beta: cv / (vb || 1e-24) }; };
    const lset = new Set(leaders.map((x) => x[0])); const list = [];
    for (const s of syms) {
      if (lset.has(s)) continue;
      const cb = corr(ret[s], basket); let best = null;
      for (const [ls, lr] of leaders) { const c1 = corr(ret[s], ret[ls]); if (!best || c1.r > best.r) best = { sym: ls, r: c1.r, ret: lr }; }
      const actual = winRet(s); const expected = cb.beta * basketWin; const gap = expected - actual;
      list.push({ symbol: s, corr: cb.r, beta: cb.beta, expected, actual, gap, best });
    }
    list.sort((a, b) => b.gap * Math.max(b.corr, 0) - a.gap * Math.max(a.corr, 0));
    return { leaders: leaders.map(([s, r]) => ({ symbol: s, ret: r })), basketWin, list };
  }

  G.TA = { analyze, laggards, resample, fmt, money, decision, WEIGHTS, GROUP_NAMES };
  if (typeof module !== "undefined") module.exports = G.TA;
})(typeof window !== "undefined" ? window : globalThis);

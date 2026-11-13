// Teknik analiz motoru — bot/analysis.py ile aynı mantık.
(function (G) {
  const N = (a) => a.length;
  const last = (a, i = 1) => a[a.length - i];
  function ema(x, n) { const o = new Array(N(x)); const a = 2 / (n + 1); o[0] = x[0]; for (let i = 1; i < N(x); i++) o[i] = a * x[i] + (1 - a) * o[i - 1]; return o; }
  function rma(x, n) { const o = new Array(N(x)); const a = 1 / n; o[0] = x[0]; for (let i = 1; i < N(x); i++) o[i] = a * x[i] + (1 - a) * o[i - 1]; return o; }
  function sma(x, n) { const o = new Array(N(x)).fill(NaN); let s = 0; for (let i = 0; i < N(x); i++) { s += x[i]; if (i >= n) s -= x[i - n]; if (i >= n - 1) o[i] = s / n; } return o; }
  function rstd(x, n) { const o = new Array(N(x)).fill(NaN); for (let i = n - 1; i < N(x); i++) { let m = 0; for (let j = i - n + 1; j <= i; j++) m += x[j]; m /= n; let v = 0; for (let j = i - n + 1; j <= i; j++) v += (x[j] - m) ** 2; o[i] = Math.sqrt(v / n); } return o; }
  const diff = (x) => x.map((v, i) => (i ? v - x[i - 1] : 0));
  function rsi(c, n = 14) { const d = diff(c); const g = rma(d.map((v) => Math.max(v, 0)), n), l = rma(d.map((v) => Math.max(-v, 0)), n); return g.map((v, i) => 100 - 100 / (1 + v / (l[i] || 1e-12))); }
  function macd(c) { const f = ema(c, 12), s = ema(c, 26); const m = f.map((v, i) => v - s[i]); const sg = ema(m, 9); return { m, sg, h: m.map((v, i) => v - sg[i]) }; }
  function tr(h, l, c) { return h.map((v, i) => { const pc = i ? c[i - 1] : c[0]; return Math.max(v - l[i], Math.abs(v - pc), Math.abs(l[i] - pc)); }); }
  function atr(h, l, c, n = 14) { return rma(tr(h, l, c), n); }
  function adx(h, l, c, n = 14) {
    const pdm = [], ndm = [];
    for (let i = 0; i < N(h); i++) { const up = i ? h[i] - h[i - 1] : 0, dn = i ? l[i - 1] - l[i] : 0; pdm.push(up > dn && up > 0 ? up : 0); ndm.push(dn > up && dn > 0 ? dn : 0); }
    const t = rma(tr(h, l, c), n).map((v) => v || 1e-12); const p = rma(pdm, n).map((v, i) => 100 * v / t[i]); const q = rma(ndm, n).map((v, i) => 100 * v / t[i]);
    const dx = p.map((v, i) => 100 * Math.abs(v - q[i]) / ((v + q[i]) || 1e-12)); return { adx: rma(dx, n), pdi: p, ndi: q };
  }
  function stochRsi(c, n = 14) { const r = rsi(c, n); const o = r.map(() => 50); for (let i = n - 1; i < N(r); i++) { let lo = Infinity, hi = -Infinity; for (let j = i - n + 1; j <= i; j++) { lo = Math.min(lo, r[j]); hi = Math.max(hi, r[j]); } o[i] = hi > lo ? 100 * (r[i] - lo) / (hi - lo) : 50; } const k = sma(o, 3); return { k, d: sma(k.map((v) => (isNaN(v) ? 50 : v)), 3) }; }
  function obv(c, v) { let s = 0; return c.map((x, i) => (s += (i ? Math.sign(x - c[i - 1]) : 0) * v[i])); }
  function mfi(h, l, c, v, n = 14) { const tp = h.map((x, i) => (x + l[i] + c[i]) / 3); let ps = 0, ns = 0; for (let i = N(tp) - n; i < N(tp); i++) { const d = tp[i] - tp[i - 1], mf = tp[i] * v[i]; if (d > 0) ps += mf; else if (d < 0) ns += mf; } return ns === 0 ? 100 : 100 - 100 / (1 + ps / ns); }
  function slopeNorm(y, n = 20) { y = y.slice(-n); const m = N(y); const xm = (m - 1) / 2; const ym = y.reduce((a, b) => a + b, 0) / m; let nu = 0, de = 0; for (let i = 0; i < m; i++) { nu += (i - xm) * (y[i] - ym); de += (i - xm) ** 2; } let sc = 0; for (let i = 1; i < m; i++) sc += Math.abs(y[i] - y[i - 1]); sc = sc / (m - 1) || 1e-12; return nu / de / sc; }
  function percentile(a, p) { a = a.filter((x) => !isNaN(x)).sort((x, y) => x - y); if (!a.length) return NaN; const k = (a.length - 1) * p / 100, f = Math.floor(k); return f + 1 < a.length ? a[f] + (a[f + 1] - a[f]) * (k - f) : a[f]; }
  const clip = (x, a = -1, b = 1) => Math.max(a, Math.min(b, x));
  const sign = Math.sign;

  function resample(k, ms) { const out = []; let cur = null, key = null; for (const c of k) { const g = Math.floor(c.t / ms); if (g !== key) { if (cur) out.push(cur); key = g; cur = { ...c }; } else { cur.h = Math.max(cur.h, c.h); cur.l = Math.min(cur.l, c.l); cur.c = c.c; for (const f of ["v", "qv", "tb", "tq"]) cur[f] += c[f]; } } if (cur) out.push(cur); return out; }

  function pivots(h, l, k = 5) { const hi = [], lo = []; for (let i = k; i < N(h) - k; i++) { let mh = -Infinity, ml = Infinity; for (let j = i - k; j <= i + k; j++) { mh = Math.max(mh, h[j]); ml = Math.min(ml, l[j]); } if (h[i] === mh) hi.push([i, h[i]]); if (l[i] === ml) lo.push([i, l[i]]); } return { hi, lo }; }

  function srLevels(h, l, c, v, A) {
    const pv = pivots(h, l); const pts = pv.hi.map((x) => x[1]).concat(pv.lo.map((x) => x[1])).sort((a, b) => a - b);
    const tol = Math.max(A * 0.6, last(c) * 0.002); const cl = [];
    for (const p of pts) { const z = cl[cl.length - 1]; if (z && p - z.last <= tol) { z.sum += p; z.n++; z.last = p; } else cl.push({ sum: p, n: 1, last: p }); }
    const levels = cl.map((z) => ({ price: z.sum / z.n, touches: z.n, src: "pivot" }));
    const m = Math.min(300, N(c)); const hh = h.slice(-m), ll = l.slice(-m), cc = c.slice(-m), vv = v.slice(-m);
    const lo = Math.min(...ll), hi = Math.max(...hh); let poc = null, profile = null;
    if (hi > lo) {
      const bins = 40; const hist = new Array(bins).fill(0);
      for (let i = 0; i < m; i++) { const tp = (hh[i] + ll[i] + cc[i]) / 3; const ix = Math.min(bins - 1, Math.max(0, Math.floor((tp - lo) / (hi - lo) * bins))); hist[ix] += vv[i]; }
      const centers = hist.map((_, i) => lo + (i + 0.5) * (hi - lo) / bins);
      let mi = 0; hist.forEach((x, i) => { if (x > hist[mi]) mi = i; }); poc = centers[mi];
      const top = hist.map((x, i) => [x, i]).sort((a, b) => a[0] - b[0]).slice(-5);
      for (const [, i] of top) levels.push({ price: centers[i], touches: 2, src: "hacim" });
      profile = { centers, hist };
    }
    const price = last(c);
    const sup = levels.filter((x) => x.price < price).sort((a, b) => price - a.price - (price - b.price)).slice(0, 4);
    const res = levels.filter((x) => x.price > price).sort((a, b) => a.price - price - (b.price - price)).slice(0, 4);
    return { sup, res, poc, profile };
  }

  function fibonacci(h, l, n = 150) {
    const hh = h.slice(-n), ll = l.slice(-n); let ih = 0, il = 0;
    hh.forEach((x, i) => { if (x > hh[ih]) ih = i; }); ll.forEach((x, i) => { if (x < ll[il]) il = i; });
    const hi = hh[ih], lo = ll[il], up = ih > il, rng = hi - lo; const levels = {};
    for (const r of [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1, 1.272, 1.618]) levels[r] = up ? hi - rng * r : lo + rng * r;
    return { up, high: hi, low: lo, levels, ih: N(h) - Math.min(n, N(h)) + ih, il: N(h) - Math.min(n, N(h)) + il };
  }

  function analyze(k, book, trades, htfMs) {
    const h = k.map((x) => x.h), l = k.map((x) => x.l), c = k.map((x) => x.c), v = k.map((x) => x.v), qv = k.map((x) => x.qv), tq = k.map((x) => x.tq);
    const price = last(c);
    const e20 = ema(c, 20), e50 = ema(c, 50), e200 = ema(c, 200); const r = rsi(c); const M = macd(c); const mh = M.h;
    const at = atr(h, l, c); const A = last(at); const D = adx(h, l, c); const S = stochRsi(c); const ob = obv(c, v); const mf = mfi(h, l, c, v);
    const bm = sma(c, 20), bs = rstd(c, 20); const bu = bm.map((x, i) => x + 2 * bs[i]), bl = bm.map((x, i) => x - 2 * bs[i]);
    const pb = last(bu) > last(bl) ? (price - last(bl)) / (last(bu) - last(bl)) : 0.5; const bw = bm.map((x, i) => (bu[i] - bl[i]) / x);
    let sv = 0, sp = 0; for (let i = N(c) - 24; i < N(c); i++) { sp += (h[i] + l[i] + c[i]) / 3 * v[i]; sv += v[i]; } const vw = sp / Math.max(sv, 1e-12);
    const comp = [];
    const add = (name, s, w, text) => comp.push({ name, score: Math.round(s * 100) / 100, weight: w, text });
    const f = (x) => fmt(x);

    const t = (sign(price - last(e50)) + sign(price - last(e200)) + sign(last(e20) - last(e50)) + sign(last(e50) - last(e50, 6))) / 4;
    add("Trend (EMA20/50/200)", t, 2.0, `Fiyat ${price > last(e200) ? "EMA200 üstünde" : "EMA200 altında"}, EMA20 ${last(e20) > last(e50) ? ">" : "<"} EMA50`);

    const k4 = resample(k, htfMs || 4 * 3600e3);
    if (N(k4) >= 60) { const c4 = k4.map((x) => x.c); const a4 = ema(c4, 21), b4 = ema(c4, 55); const t4 = (sign(last(c4) - last(a4)) + sign(last(a4) - last(b4)) + sign(last(a4) - last(a4, 4))) / 3; add("Üst zaman dilimi trendi", t4, 1.5, "4 kat büyük zaman diliminde EMA21/55 " + (t4 > 0 ? "yükseliş" : t4 < 0 ? "düşüş" : "yatay")); }

    let s = (last(mh) > 0 ? 0.5 : -0.5) + (last(mh) > last(mh, 2) ? 0.5 : -0.5); let cross = "";
    for (let i = 1; i < 4; i++) { if (last(mh, i) > 0 && last(mh, i + 1) <= 0) { s += 0.3; cross = " (yeni AL kesişimi)"; break; } if (last(mh, i) < 0 && last(mh, i + 1) >= 0) { s -= 0.3; cross = " (yeni SAT kesişimi)"; break; } }
    add("MACD", clip(s), 1.5, `Histogram ${last(mh) >= 0 ? "+" : ""}${f(last(mh))}, ${last(mh) > last(mh, 2) ? "artıyor" : "azalıyor"}${cross}`);

    const R = last(r);
    s = R > 78 ? -0.6 : R > 65 ? 0.2 : R >= 50 ? 0.7 : R >= 40 ? -0.3 : R >= 28 ? -0.5 : 0.4; s += last(r) > last(r, 4) ? 0.3 : -0.3;
    add("RSI(14)", clip(s), 1.0, `RSI ${R.toFixed(1)}${R > 70 ? " aşırı alım" : R < 30 ? " aşırı satım" : ""}`);

    const AD = last(D.adx); s = AD > 18 ? (last(D.pdi) > last(D.ndi) ? 1 : -1) * Math.min(AD / 40, 1) : 0;
    add("ADX/DMI", s, 1.0, `ADX ${AD.toFixed(0)} (${AD > 25 ? "güçlü trend" : "zayıf trend"}), +DI ${last(D.pdi).toFixed(0)} / -DI ${last(D.ndi).toFixed(0)}`);

    const K = last(S.k), Dd = last(S.d), K1 = last(S.k, 2), D1 = last(S.d, 2);
    s = K > Dd && K1 <= D1 && K < 30 ? 1 : K < Dd && K1 >= D1 && K > 70 ? -1 : K > 85 ? -0.4 : K < 15 ? 0.4 : K > Dd ? 0.3 : -0.3;
    add("Stoch RSI", s, 0.5, `K ${K.toFixed(0)} / D ${Dd.toFixed(0)}`);

    const sq = last(bw) < percentile(bw.slice(-120), 20);
    s = pb > 1 ? (t > 0 ? 0.3 : -0.3) : pb < 0 ? 0.3 : (pb - 0.5) * 0.8;
    add("Bollinger", clip(s), 0.5, `%B ${pb.toFixed(2)}${sq ? " — sıkışma (sert hareket yakın)" : ""}`);

    const so = slopeNorm(ob, 20); add("OBV (hacim akışı)", Math.tanh(so * 3), 1.0, "OBV " + (so > 0 ? "yükseliyor: birikim" : "düşüyor: dağıtım"));
    s = mf > 20 && mf < 80 ? clip((mf - 50) / 30) : mf >= 80 ? -0.5 : 0.5; add("MFI(14)", s, 0.5, `MFI ${mf.toFixed(0)}`);
    const dv = A ? (price - vw) / A : 0; add("VWAP (24 mum)", Math.tanh(dv / 2), 0.5, `Fiyat VWAP'ın ${price > vw ? "üstünde" : "altında"} (${f(vw)})`);

    const sum = (a, n) => a.slice(-n).reduce((x, y) => x + y, 0);
    const trr = sum(tq, 24) / Math.max(sum(qv, 24), 1e-12), tr6 = sum(tq, 6) / Math.max(sum(qv, 6), 1e-12);
    add("Alıcı/Satıcı baskısı", clip((trr - 0.5) * 12 + (tr6 - 0.5) * 6), 1.5, `Son 24 mum agresif alım %${(trr * 100).toFixed(1)}, son 6 mum %${(tr6 * 100).toFixed(1)}`);

    const va = N(v) > 25 ? v.slice(-23, -3).reduce((a, b) => a + b, 0) / 20 : v.reduce((a, b) => a + b, 0) / N(v);
    const spike = (sum(v, 3) / 3) / Math.max(va, 1e-12); const ret3 = price / last(c, 4) - 1;
    s = spike > 1.2 ? (ret3 > 0 ? 1 : -1) * clip((spike - 1.2) / 2, 0, 1) : 0;
    add("Hacim patlaması", s, 1.0, `Hacim ortalamanın ${spike.toFixed(1)} katı, son 3 mum ${(ret3 * 100).toFixed(2)}%`);

    const SR = srLevels(h, l, c, v, A); const ns = SR.sup.length ? SR.sup[0].price : price - 3 * A; const nr = SR.res.length ? SR.res[0].price : price + 3 * A;
    const rr = (nr - price) / Math.max(price - ns, A * 0.2);
    add("Destek/Direnç", clip(Math.tanh(Math.log(Math.max(rr, 1e-3)))), 1.0, `En yakın destek ${f(ns)}, direnç ${f(nr)} (yer oranı ${rr.toFixed(2)})`);

    const fb = fibonacci(h, l); const lv = fb.levels; s = 0;
    if (fb.up) { if (lv[0.618] <= price && price <= lv[0.5]) s = last(mh) > last(mh, 2) ? 0.6 : 0.2; else if (price < lv[0.786]) s = -0.6; else if (price > lv[0.236]) s = 0.4; }
    else { if (lv[0.5] <= price && price <= lv[0.618]) s = last(mh) < last(mh, 2) ? -0.6 : -0.2; else if (price > lv[0.786]) s = 0.6; else if (price < lv[0.236]) s = -0.4; }
    let near = null; for (const key in lv) if (!near || Math.abs(lv[key] - price) < Math.abs(near[1] - price)) near = [key, lv[key]];
    add("Fibonacci", s, 0.5, `${fb.up ? "Yükseliş" : "Düşüş"} dalgası, en yakın seviye ${near[0]} = ${f(near[1])}`);

    let bookInfo = null;
    if (book) {
      let bid = 0, ask = 0; for (const [p, q] of book.bids) if (+p >= price * 0.98) bid += p * q; for (const [p, q] of book.asks) if (+p <= price * 1.02) ask += p * q;
      const imb = (bid - ask) / Math.max(bid + ask, 1e-12); bookInfo = { bid, ask, imb };
      add("Emir defteri (±%2)", clip(imb * 2), 1.0, `Alış duvarı ${money(bid)} / Satış duvarı ${money(ask)}`);
    }
    let whales = null;
    if (trades && trades.length > 20) {
      const vals = trades.map((x) => x.p * x.q); const thr = Math.max(percentile(vals, 95), 5000); let buy = 0, sell = 0; const list = [];
      trades.forEach((x, i) => { if (vals[i] >= thr) { if (x.m) sell += vals[i]; else buy += vals[i]; list.push({ t: x.T, p: +x.p, val: vals[i], side: x.m ? "SAT" : "AL" }); } });
      const net = (buy - sell) / Math.max(buy + sell, 1e-12); whales = { buy, sell, thr, list: list.slice(-30).reverse() };
      add("Büyük işlemler", clip(net * 1.5), 1.0, `Büyük alım ${money(buy)} / büyük satım ${money(sell)} (eşik ${money(thr)})`);
    }

    const tw = comp.reduce((a, x) => a + x.weight, 0); const total = comp.reduce((a, x) => a + x.score * x.weight, 0) / tw;
    const score = Math.round((50 + 50 * total) * 10) / 10; const agreement = comp.filter((x) => x.score * total > 0.05).length / comp.length;
    let stop = price - 1.5 * A; if (SR.sup.length && price - SR.sup[0].price < 1.5 * A) stop = Math.min(stop, SR.sup[0].price - 0.3 * A);
    const tp1 = nr - price > A ? nr : price + 2 * A, tp2 = price + 3.5 * A;
    const label = score >= 65 ? "YÜKSELİŞ ihtimali yüksek" : score >= 55 ? "Hafif yükseliş eğilimi" : score > 45 ? "Nötr / kararsız" : score > 35 ? "Hafif düşüş eğilimi" : "DÜŞÜŞ ihtimali yüksek";
    return { price, score, label, agreement, atr: A, rsi: R, adx: AD, taker: trr, spike, components: comp, supports: SR.sup, resistances: SR.res, poc: SR.poc, profile: SR.profile, fib: fb, whales, book: bookInfo,
      plan: { entry: price, stop, tp1, tp2 }, change24: N(c) > 25 ? price / last(c, 25) - 1 : 0,
      series: { e20, e50, e200, bu, bl, bm, rsi: r, macd: M, stK: S.k, stD: S.d, adx: D.adx } };
  }
  function fmt(x) { if (x === null || x === undefined || isNaN(x)) return "-"; const a = Math.abs(x); if (a >= 1000) return x.toLocaleString("tr-TR", { maximumFractionDigits: 2 }); if (a >= 1) return x.toFixed(4); if (a === 0) return "0"; return x.toPrecision(5); }
  function money(x) { return x >= 1e9 ? (x / 1e9).toFixed(2) + "B$" : x >= 1e6 ? (x / 1e6).toFixed(2) + "M$" : x >= 1e3 ? (x / 1e3).toFixed(1) + "K$" : x.toFixed(0) + "$"; }
  G.TA = { analyze, resample, ema, rsi, macd, fmt, money };
  if (typeof module !== "undefined") module.exports = G.TA;
})(typeof window !== "undefined" ? window : globalThis);

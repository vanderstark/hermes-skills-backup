#!/usr/bin/env python3
"""
Market Report Fast v4 — IDX + US + Crypto
FIXED: OBV trend, entry zone, scoring, swing clustering, RSI filter
Entry/SL/TP + Support/Resistance + OBV + Weekly + CoinGecko + Indodax
no_agent cron job (~12s) — v4 2026-08-07
"""
import json, urllib.request, time, sys
from datetime import datetime, timezone, timedelta

TZ_WIB = 7 * 3600
UA = {"User-Agent": "Mozilla/5.0"}

IDX_UNIVERSE = ["BBRI.JK","BMRI.JK","BBCA.JK","TLKM.JK","ICBP.JK","ASII.JK","UNVR.JK","BRPT.JK","SMGR.JK","ADRO.JK"]
US_UNIVERSE = ["NVDA","GOOGL","AVGO","JPM","AMZN","MSFT","AAPL"]
CRYPTO_UNIVERSE = ["BTC-USD","ETH-USD","BNB-USD","SOL-USD","ADA-USD"]

def fetch(url, headers=None):
    req = urllib.request.Request(url, headers={**UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode())

def chart(sym, rng, interval):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range={rng}&interval={interval}"
    try:
        data = fetch(url)
        result = data["chart"]["result"][0]
        ts = result["timestamp"]
        q = result["indicators"]["quote"][0]
        closes = q.get("close", [])
        highs = q.get("high", [])
        lows = q.get("low", [])
        vols = q.get("volume", [])
        return list(zip(ts, closes)), list(zip(ts, highs)), list(zip(ts, lows)), list(zip(ts, vols))
    except Exception:
        return None, None, None, None

def unzip(arr):
    if not arr:
        return [], []
    return [x[1] for x in arr if x[1] is not None], [x[0] for x in arr if x[1] is not None]

def sma(c, n):
    return sum(c[-n:]) / n if len(c) >= n else None

def rsi(c, n=14):
    if len(c) < n + 1:
        return None
    gains = losses = 0.0
    for i in range(1, n + 1):
        ch = c[-n-1+i] - c[-n+i-1]
        if ch >= 0: gains += ch
        else: losses -= ch
    if losses == 0: return 100
    rs = (gains / n) / (losses / n)
    return round(100 - 100 / (1 + rs), 1)

def macd(c):
    if len(c) < 26: return None, None, None
    e12 = e26 = c[0]
    for p in c[1:]:
        e12 = e12 + 0.1818 * (p - e12)
        e26 = e26 + 0.074 * (p - e26)
    macd_line = e12 - e26
    signal = macd_line * 0.2  # approx
    hist = macd_line - signal
    return round(macd_line, 2), round(signal, 2), round(hist, 2)

def obv_analysis(closes, vols):
    if not closes or len(closes) != len(vols): return 0, "FLAT", "NEUTRAL"
    val = 0.0
    series = [0.0]
    for i in range(1, len(closes)):
        if closes[i] > closes[i-1]: val += vols[i]
        elif closes[i] < closes[i-1]: val -= vols[i]
        series.append(val)
    obv_now = series[-1]
    obv_5 = series[-6] if len(series) >= 6 else series[0]
    obv_20 = series[-21] if len(series) >= 21 else series[0]
    short = "UP" if obv_now > obv_5 else ("DOWN" if obv_now < obv_5 else "FLAT")
    med = "ACCUMULATION" if obv_now > obv_20 else ("DISTRIBUTION" if obv_now < obv_20 else "NEUTRAL")
    return round(obv_now), short, med

def swing_levels(highs, lows, window=5):
    """Find swing highs/lows with MULTIPLE windows (3,5,8) for robust clustering."""
    piv_l, piv_h = [], []
    for w in [3, 5, 8]:
        if len(highs) < 2*w+1: continue
        for i in range(w, len(lows)-w):
            if lows[i] == min(lows[i-w:i+w+1]): piv_l.append(lows[i])
        for i in range(w, len(highs)-w):
            if highs[i] == max(highs[i-w:i+w+1]): piv_h.append(highs[i])
    return list(set(piv_l)), list(set(piv_h))

def cluster(levels, tol_pct=0.025):
    """Cluster levels (±2.5%). Returns (levels, touch_counts) — touch count = cluster size."""
    if not levels: return [], []
    levels = sorted(levels)
    groups = [[levels[0]]]
    for lv in levels[1:]:
        if abs(lv - groups[-1][-1]) / groups[-1][-1] <= tol_pct:
            groups[-1].append(lv)
        else:
            groups.append([lv])
    scored = sorted(groups, key=lambda g: -len(g))
    return [round(sum(g)/len(g), 2) for g in scored], [len(g) for g in scored]

def strongest_support(levels, touches, px):
    """Support terkuat = level < harga dgn JML TOUCH terbanyak (bukan terdekat)."""
    best_lvl, best_cnt = None, 0
    for lvl, cnt in zip(levels, touches):
        if lvl < px and cnt > best_cnt:
            best_lvl, best_cnt = lvl, cnt
    return best_lvl, best_cnt

def strongest_resistance(levels, touches, px):
    """Resistance terkuat = level > harga dgn JML TOUCH terbanyak."""
    best_lvl, best_cnt = None, 0
    for lvl, cnt in zip(levels, touches):
        if lvl > px and cnt > best_cnt:
            best_lvl, best_cnt = lvl, cnt
    return best_lvl, best_cnt

def entry_zone(s1, s2, r1, px, is_crypto=False):
    if not s1: return round(px * 0.97, 2), round(px * 0.99, 2)
    buffer = 0.01 if not is_crypto else 0.02
    entry_low = round(s1 * (1 + buffer), 2)
    entry_high = round(min(s1 * 1.03, px * 0.98), 2)
    if entry_high <= entry_low:
        entry_high = round(entry_low * 1.01, 2)
    return entry_low, entry_high

def sl_tp(s1, s2, r1, r2, px, is_crypto=False):
    sl_buffer = 0.05 if is_crypto else 0.03
    sl = round(s1 * (1 - sl_buffer), 2) if s1 else round(px * 0.95, 2)
    tp1 = r1 if r1 else round(px * 1.05, 2)
    tp2 = r2 if r2 else round(tp1 * 1.05, 2)
    if r1 and r2:
        ext = (r2 - r1) * 0.618
        tp3 = round(r2 + ext, 2)
    else:
        tp3 = round(px * 1.10, 2) if not is_crypto else round(px * 1.15, 2)
    return sl, tp1, tp2, tp3

def risk_reward(entry_low, sl, tp1):
    risk = entry_low - sl
    reward = tp1 - entry_low
    if risk <= 0: return 0
    return round(reward / risk, 1)

def analyze_symbol(sym, is_idx=True, is_crypto=False):
    closes_raw, highs_raw, lows_raw, vols_raw = chart(sym, "1y", "1d")
    if not closes_raw or len(closes_raw) < 50: return None
    closes, _ = unzip(closes_raw)
    highs, _ = unzip(highs_raw)
    lows, _ = unzip(lows_raw)
    vols, _ = unzip(vols_raw)
    px = closes[-1]
    prev = closes[-2] if len(closes) > 1 else px
    chg = round((px / prev - 1) * 100, 2)

    s20 = sma(closes, 20)
    s50 = sma(closes, 50)
    s200 = sma(closes, 200)
    rsi14 = rsi(closes)
    macd_l, macd_s, macd_h = macd(closes)
    obv_val, obv_short, obv_med = obv_analysis(closes, vols)

    # Weekly alignment
    cw_raw, hw_raw, lw_raw, vw_raw = chart(sym, "2y", "1wk")
    if cw_raw and len(cw_raw) > 20:
        cw, _ = unzip(cw_raw)
        w20 = sma(cw, 20)
        w50 = sma(cw, 50)
        w_above = cw[-1] > w20 if w20 else False
        w_above50 = cw[-1] > w50 if w50 else False
        weekly_align = "ALIGN" if (s20 and w_above and w_above50) else \
                       "MISALIGN" if (s20 and not w_above) else "N/A"
    else:
        w20, w50, weekly_align = None, None, "N/A"

    # Support/Resistance
    piv_l, piv_h = swing_levels(highs, lows)
    sup, sup_touches = cluster(piv_l)
    res, res_touches = cluster(piv_h)
    below = [x for x in sup if x < px]
    above = [x for x in res if x > px]
    s1 = max(below) if below else None
    s2 = sorted(below)[-2] if len(below) >= 2 else None
    r1 = min(above) if above else None
    r2 = sorted(above)[1] if len(above) >= 2 else None

    strong_lvl, strong_cnt = strongest_support(sup, sup_touches, px)
    strong_dist = round((px - strong_lvl) / px * 100, 1) if strong_lvl else None
    strong_res_lvl, strong_res_cnt = strongest_resistance(res, res_touches, px)
    strong_res_dist = round((strong_res_lvl - px) / px * 100, 1) if strong_res_lvl else None

    entry_low, entry_high = entry_zone(s1, s2, r1, px, is_crypto)
    sl, tp1, tp2, tp3 = sl_tp(s1, s2, r1, r2, px, is_crypto)
    rr = risk_reward(entry_low, sl, tp1)

    score = 0; reasons = []
    if s20 and px > s20: score += 15; reasons.append("px>SMA20")
    if s50 and px > s50: score += 15; reasons.append("px>SMA50")
    if s200 and px > s200: score += 10; reasons.append("px>SMA200")
    if s20 and s50 and s20 > s50: score += 5; reasons.append("SMA20>SMA50")
    if rsi14:
        if 40 <= rsi14 <= 65: score += 10; reasons.append(f"RSI={rsi14}(optimal)")
        elif 65 < rsi14 <= 72: score += 5; reasons.append(f"RSI={rsi14}(warm)")
        elif rsi14 > 72: score -= 10; reasons.append(f"RSI={rsi14}(OVERBOUGHT!)")
        elif rsi14 < 40: score += 5; reasons.append(f"RSI={rsi14}(oversold)")
    if macd_h and macd_h > 0: score += 5; reasons.append("MACD↑")
    if obv_short == "UP" and obv_med == "ACCUMULATION": score += 15; reasons.append("OBV↑↑")
    elif obv_short == "UP": score += 8; reasons.append("OBV↑")
    elif obv_short == "DOWN": score -= 8; reasons.append("OBV↓")
    if weekly_align == "ALIGN": score += 10; reasons.append("WeeklyALIGN")
    elif weekly_align == "MISALIGN": score -= 5; reasons.append("WeeklyMISALIGN")
    if s200 and px < s200 * 1.3: score += 5; reasons.append("Near52wLow")
    if vols and sum(vols[-5:])/5 > sum(vols[-20:])/20 * 1.2: score += 5; reasons.append("Vol↑")

    return {
        "sym": sym, "px": px, "chg": chg,
        "s20": round(s20,2) if s20 else None,
        "s50": round(s50,2) if s50 else None,
        "s200": round(s200,2) if s200 else None,
        "rsi": rsi14, "macd_l": macd_l, "macd_h": macd_h,
        "obv": obv_val, "obv_s": obv_short, "obv_m": obv_med,
        "w20": round(w20,2) if w20 else None,
        "w_align": weekly_align,
        "s1": s1, "s2": s2, "r1": r1, "r2": r2,
        "strong_sup": strong_lvl, "strong_touch": strong_cnt,
        "strong_dist": strong_dist,
        "strong_res": strong_res_lvl, "strong_res_touch": strong_res_cnt,
        "strong_res_dist": strong_res_dist,
        "entry": (entry_low, entry_high),
        "sl": sl, "tp1": tp1, "tp2": tp2, "tp3": tp3,
        "rr": rr, "score": score,
        "reasons": reasons
    }

def fetch_coingecko(sym):
    cg_id = sym.replace("-USD", "").lower()
    mapping = {"btc": "bitcoin", "eth": "ethereum", "bnb": "binancecoin", "sol": "solana", "ada": "cardano"}
    cg_id = mapping.get(cg_id, cg_id)
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={cg_id}&vs_currencies=usd"
        data = fetch(url)
        return data.get(cg_id, {}).get("usd")
    except Exception:
        return None

def fetch_indodax(sym):
    """BTC-USD -> btc_idr"""
    pair = sym.replace("-USD", "").lower() + "_idr"
    try:
        url = f"https://indodax.com/api/{pair}/ticker"
        data = fetch(url)
        t = data.get("ticker", {})
        return float(t.get("last", 0)), float(t.get("vol_idr", 0))
    except Exception:
        return None, None

def fetch_ihsg_usdidr():
    try:
        ihsg = fetch("https://query1.finance.yahoo.com/v8/finance/chart/%5EJKSE?range=1d&interval=1d")
        usd = fetch("https://query1.finance.yahoo.com/v8/finance/chart/IDR%3DX?range=1d&interval=1d")
        ihsg_px = ihsg["chart"]["result"][0]["indicators"]["quote"][0]["close"][-1]
        usd_px = usd["chart"]["result"][0]["indicators"]["quote"][0]["close"][-1]
        ihsg_prev = ihsg["chart"]["result"][0]["indicators"]["quote"][0]["close"][-2]
        usd_prev = usd["chart"]["result"][0]["indicators"]["quote"][0]["close"][-2]
        return {"px": round(ihsg_px), "chg": round((ihsg_px/ihsg_prev-1)*100, 2)}, \
               {"px": round(usd_px), "chg": round((usd_px/usd_prev-1)*100, 2)}
    except Exception:
        return None, None

# =========== MAIN ===========
print("🔄 Fetching live data...")
ihsg, usd_idr = fetch_ihsg_usdidr()

idx_results = [r for s in IDX_UNIVERSE if (r := analyze_symbol(s, is_idx=True))]
us_results = [r for s in US_UNIVERSE if (r := analyze_symbol(s, is_idx=False))]
crypto_results = []
for s in CRYPTO_UNIVERSE:
    r = analyze_symbol(s, is_idx=False, is_crypto=True)
    if r:
        cg_px = fetch_coingecko(s)
        idr_px, vol_idr = fetch_indodax(s)
        r["cg_px"] = cg_px
        r["idr"] = int(idr_px) if idr_px else None
        r["vol_idr"] = vol_idr
        r["avg"] = round((r["px"] + cg_px) / 2, 2) if cg_px else r["px"]
        r["diff"] = round(abs(r["px"] - cg_px) / cg_px * 100, 1) if cg_px else 0
        crypto_results.append(r)

idx_top = sorted(idx_results, key=lambda x: -x["score"])[:10]
us_top = sorted(us_results, key=lambda x: -x["score"])[:7]
crypto_top = sorted(crypto_results, key=lambda x: -x["score"])[:5]

now = datetime.now(timezone(timedelta(seconds=TZ_WIB))).strftime("%A, %d %B %Y — %H:%M WIB")
sent = "🟢 RISK-ON" if ihsg and ihsg["chg"] > 0 else "🔴 RISK-OFF"

print("=" * 80)
print(f"   📊 REPORT MARKET — {now}")
print("=" * 80)
print(f"   Sentimen: {sent}")
if ihsg: print(f"   IHSG: {ihsg['px']:,} ({ihsg['chg']:+.2f}%)")
if usd_idr: print(f"   USD/IDR: {usd_idr['px']:,} ({usd_idr['chg']:+.2f}%)")

# ====== IDX ======
print("\n" + "=" * 80)
print("   🇮🇩 SAHAM IDX — TOP 10 RANKED BY SCORE")
print("=" * 80)
for i, r in enumerate(idx_top, 1):
    e_low, e_high = r["entry"]
    sk1, sk2 = r["s1"] or 0, r["s2"] or 0
    rk1, rk2 = r["r1"] or 0, r["r2"] or 0
    print(f"\n  {i}. {r['sym'][:5]} — Score {r['score']} ({r['chg']:+.2f}%)")
    print(f"     🛡️ SL: {r['sl']:,.0f}  |  🎯 TP1: {r['tp1']:,.0f}  |  TP2: {r['tp2']:,.0f}  |  TP3: {r['tp3']:,.0f}")
    print(f"     ✅ Entry: {e_low:,.0f} – {e_high:,.0f}")
    print(f"     🔵 S.KUAT-1: {sk1:,.0f}  |  🔵 S.KUAT-2: {sk2:,.0f}  |  🔴 R.KUAT-1: {rk1:,.0f}  |  🔴 R.KUAT-2: {rk2:,.0f}")
    print(f"     💰 HARGA SEKARANG: {r['px']:,.0f}  |  RR 1:{r['rr']}")

# ====== US ======
print("\n" + "=" * 80)
print("   🇺🇸 SAHAM US — TOP 7 RANKED BY SCORE")
print("=" * 80)
for i, r in enumerate(us_top, 1):
    e_low, e_high = r["entry"]
    sk1, sk2 = r["s1"] or 0, r["s2"] or 0
    rk1, rk2 = r["r1"] or 0, r["r2"] or 0
    print(f"\n  {i}. {r['sym']} — Score {r['score']} ({r['chg']:+.2f}%)")
    print(f"     🛡️ SL: ${r['sl']:,.2f}  |  🎯 TP1: ${r['tp1']:,.2f}  |  TP2: ${r['tp2']:,.2f}  |  TP3: ${r['tp3']:,.2f}")
    print(f"     ✅ Entry: ${e_low:,.2f} – ${e_high:,.2f}")
    print(f"     🔵 S.KUAT-1: ${sk1:,.2f}  |  🔵 S.KUAT-2: ${sk2:,.2f}  |  🔴 R.KUAT-1: ${rk1:,.2f}  |  🔴 R.KUAT-2: ${rk2:,.2f}")
    print(f"     💰 HARGA SEKARANG: ${r['px']:,.2f}  |  RR 1:{r['rr']}")

# ====== CRYPTO ======
print("\n" + "=" * 80)
print("   🪙 CRYPTO — TOP 5 RANKED BY SCORE")
print("=" * 80)
for i, r in enumerate(crypto_top, 1):
    e_low, e_high = r["entry"]
    sk1, sk2 = r["s1"] or 0, r["s2"] or 0
    rk1, rk2 = r["r1"] or 0, r["r2"] or 0
    print(f"\n  {i}. {r['sym'].replace('-USD','')} — Score {r['score']} ({r['chg']:+.2f}%)")
    print(f"     🛡️ SL: ${r['sl']:,.2f}  |  🎯 TP1: ${r['tp1']:,.2f}  |  TP2: ${r['tp2']:,.2f}  |  TP3: ${r['tp3']:,.2f}")
    print(f"     ✅ Entry: ${e_low:,.2f} – ${e_high:,.2f}")
    print(f"     🔵 S.KUAT-1: ${sk1:,.2f}  |  🔵 S.KUAT-2: ${sk2:,.2f}  |  🔴 R.KUAT-1: ${rk1:,.2f}  |  🔴 R.KUAT-2: ${rk2:,.2f}")
    print(f"     💰 HARGA SEKARANG: ${r['px']:,.2f}  |  RR 1:{r['rr']}")

# ====== INSIGHTS ======
print("\n" + "=" * 80)
print("   💡 KIAT HARI INI")
print("=" * 80)
strong_idx = [r for r in idx_top if r["obv_s"] == "UP" and r["w_align"] == "ALIGN" and r["score"] >= 40]
if strong_idx:
    best = max(strong_idx, key=lambda x: x["score"])
    print(f"   🔥 IDX terkuat (OBV↑ + Weekly ALIGN + Score≥40): {best['sym'][:5]}.")
strong_us = [r for r in us_top if r["obv_s"] == "UP" and r["score"] >= 40]
if strong_us:
    best = max(strong_us, key=lambda x: x["score"])
    print(f"   🇺🇸 US terkuat (OBV↑ + Score≥40): {best['sym']}")
overbought = [r for r in idx_top + us_top + crypto_top if r["rsi"] and r["rsi"] > 72]
if overbought:
    print(f"   ⚠️ OVERBOUGHT (RSI>72): {', '.join(r['sym'][:5] for r in overbought)} — waspada koreksi")
print(f"   🪙 Crypto akumulasi kuat: {', '.join(r['sym'].replace('-USD','') for r in crypto_top if r['obv_s']=='UP')}")
print()
print("   ⚠️ SL wajib. Entry harus di ZONA, bukan market order. RR min 1:2.")
print("   ⭐ DISCLAIMER: Analisa teknikal, BUKAN nasihat investasi.")
print("=" * 80)
print(f"   ✅ Generated in ~12s — market-report-fast v4")
print("=" * 80)
#!/usr/bin/env python3
"""
Market Report Fast v4 — IDX + US + Crypto
FIXED: OBV trend, entry zone, scoring, swing clustering, RSI filter
Entry/SL/TP + Support/Resistance + OBV + Weekly + CoinGecko + Indodax
Runs in ~90-120 seconds. No LLM reasoning loop.
"""

import json, urllib.request, time, sys
from datetime import datetime

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
TZ_WIB = 7 * 3600
start = time.time()

def fetch_json(url):
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except Exception as e:
        print(f"  ⚠️ fetch error {url[:60]}: {e}")
        return None

def chart(sym, rng="1y", iv="1d"):
    d = fetch_json(f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range={rng}&interval={iv}")
    if not d or not d.get("chart",{}).get("result"): return None,None,None,None
    res = d["chart"]["result"][0]
    q = res["indicators"]["quote"][0]
    ts = res.get("timestamp", [])
    def clean(arr, ts_arr):
        """Pair timestamp with value, drop None pairs."""
        return [(t,v) for t,v in zip(ts_arr, arr) if v is not None]
    closes_raw = clean(q["close"], ts)
    highs_raw = clean(q["high"], ts)
    lows_raw = clean(q["low"], ts)
    vols_raw = clean(q["volume"], ts)
    return closes_raw, highs_raw, lows_raw, vols_raw

def unzip(data):
    if not data: return [], []
    return [x[1] for x in data], [x[0] for x in data]

def sma(c, n):
    if len(c) < n: return None
    return sum(c[-n:]) / n

def ema(c, n):
    if len(c) < n: return None
    k = 2 / (n+1)
    e = sum(c[:n]) / n
    for p in c[n:]: e = p * k + e * (1-k)
    return e

def rsi(c, n=14):
    if len(c) < n+1: return None
    gains, losses = [], []
    for i in range(len(c)-n, len(c)):
        ch = c[i] - c[i-1]
        gains.append(max(ch, 0))
        losses.append(max(-ch, 0))
    avg_g = sum(gains) / n
    avg_l = sum(losses) / n
    if avg_l == 0: return 100.0
    rs = avg_g / avg_l
    return round(100 - 100/(1+rs), 1)

def macd_signal(c):
    """Return (macd_line, signal_line, histogram)."""
    if len(c) < 35: return None, None, None
    e12 = [sum(c[:12])/12]
    e26 = [sum(c[:26])/26]
    k12, k26 = 2/13, 2/27
    for p in c[12:]:
        e12.append(p * k12 + e12[-1] * (1-k12))
    for p in c[26:]:
        e26.append(p * k26 + e26[-1] * (1-k26))
    macd_line = [a-b for a,b in zip(e12[-len(e26):], e26)]
    signal = [sum(macd_line[:9])/9]
    ks = 2/10
    for v in macd_line[9:]:
        signal.append(v * ks + signal[-1] * (1-ks))
    ml = macd_line[-1]
    sl = signal[-1]
    hist = ml - sl
    return round(ml,4), round(sl,4), round(hist,4)

def obv_analysis(closes, vols):
    """OBV with trend detection over 20-bar window."""
    if not closes or len(closes) != len(vols) or len(closes) < 25: return 0, "N/A", "NEUTRAL"
    series = [0.0]
    for i in range(1, len(closes)):
        if closes[i] > closes[i-1]: series.append(series[-1] + vols[i])
        elif closes[i] < closes[i-1]: series.append(series[-1] - vols[i])
        else: series.append(series[-1])
    # trend: compare last 20 bars
    win = min(20, len(series)-1)
    obv_now = series[-1]
    obv_prev = series[-win-1]
    obv_5 = series[-6] if len(series) >= 6 else series[0]
    obv_10 = series[-11] if len(series) >= 11 else series[0]
    # Short trend (5 bars)
    if obv_now > obv_5: short_trend = "UP"
    elif obv_now < obv_5: short_trend = "DOWN"
    else: short_trend = "FLAT"
    # Medium trend (20 bars)
    if obv_now > obv_prev: med_trend = "ACCUMULATION"
    elif obv_now < obv_prev: med_trend = "DISTRIBUTION"
    else: med_trend = "NEUTRAL"
    # OBV slope (momentum)
    slope = (obv_now - obv_prev) / abs(obv_prev) * 100 if obv_prev != 0 else 0
    return round(obv_now), short_trend, med_trend

def swing_levels(highs, lows, window=5):
    """Find swing highs and lows with multiple window sizes for better clustering."""
    if len(highs) < 2*window+1: return [], []
    piv_l, piv_h = [], []
    # Use multiple windows for more robust detection
    for w in [3, 5, 8]:
        if len(highs) < 2*w+1: continue
        for i in range(w, len(lows)-w):
            if lows[i] == min(lows[i-w:i+w+1]): piv_l.append(lows[i])
        for i in range(w, len(highs)-w):
            if highs[i] == max(highs[i-w:i+w+1]): piv_h.append(highs[i])
    return list(set(piv_l)), list(set(piv_h))

def cluster(levels, tol_pct=0.025):
    """Cluster nearby levels with 2.5% tolerance. Returns (levels, touch_count)."""
    if not levels: return [], []
    levels = sorted(levels)
    groups = [[levels[0]]]
    for lv in levels[1:]:
        if abs(lv - groups[-1][-1]) / groups[-1][-1] <= tol_pct:
            groups[-1].append(lv)
        else:
            groups.append([lv])
    # Score clusters by number of touches, keep avg level + touch count
    scored = sorted(groups, key=lambda g: -len(g))
    return [round(sum(g)/len(g), 2) for g in scored], [len(g) for g in scored]

def strongest_support(levels, touches, px):
    """Find strongest support below current price.
    Returns (level, touch_count) of the support with most touches."""
    best_lvl, best_cnt = None, 0
    for lvl, cnt in zip(levels, touches):
        # Only supports clearly below price (we want the strongest magnet below)
        if lvl < px and cnt > best_cnt:
            best_lvl, best_cnt = lvl, cnt
    return best_lvl, best_cnt

def strongest_resistance(levels, touches, px):
    """Find strongest resistance above current price.
    Returns (level, touch_count) of the resistance with most touches."""
    best_lvl, best_cnt = None, 0
    for lvl, cnt in zip(levels, touches):
        if lvl > px and cnt > best_cnt:
            best_lvl, best_cnt = lvl, cnt
    return best_lvl, best_cnt

def entry_zone(s1, s2, r1, px, is_crypto=False):
    """Calculate realistic entry zone based on support distance."""
    if not s1: return round(px * 0.97, 2), round(px * 0.99, 2)
    # Entry: between S1 and 1-2% above S1 (tighter = better RR)
    buffer = 0.01 if not is_crypto else 0.02
    entry_low = round(s1 * (1 + buffer), 2)
    entry_high = round(min(s1 * 1.03, px * 0.98), 2)
    if entry_high <= entry_low:
        entry_high = round(entry_low * 1.01, 2)
    return entry_low, entry_high

def sl_tp(s1, s2, r1, r2, px, is_crypto=False):
    """Calculate SL and TP levels based on support/resistance."""
    # SL: below S1 with buffer
    sl_buffer = 0.05 if is_crypto else 0.03
    sl = round(s1 * (1 - sl_buffer), 2) if s1 else round(px * 0.95, 2)
    # TP1 = R1, TP2 = R2, TP3 = R2 + extension
    tp1 = r1 if r1 else round(px * 1.05, 2)
    tp2 = r2 if r2 else round(tp1 * 1.05, 2)
    if r1 and r2:
        ext = (r2 - r1) * 0.618  # Fibonacci extension
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
    """Return dict with all metrics for one symbol — IMPROVED."""
    closes_raw, highs_raw, lows_raw, vols_raw = chart(sym, "1y", "1d")
    if not closes_raw or len(closes_raw) < 50: return None
    closes, _ = unzip(closes_raw)
    highs, _ = unzip(highs_raw)
    lows, _ = unzip(lows_raw)
    vols, _ = unzip(vols_raw)
    px = closes[-1]
    prev = closes[-2] if len(closes) > 1 else px
    chg = round((px / prev - 1) * 100, 2)

    # Daily indicators
    s20 = sma(closes, 20)
    s50 = sma(closes, 50)
    s200 = sma(closes, 200)
    rsi14 = rsi(closes)
    macd_l, macd_s, macd_h = macd_signal(closes)
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

    # Strongest support = support level with most touch count below price
    strong_lvl, strong_cnt = strongest_support(sup, sup_touches, px)
    # Distance from current price to strongest support (positive = below)
    strong_dist = round((px - strong_lvl) / px * 100, 1) if strong_lvl else None

    # Strongest resistance = resistance level with most touch count above price
    strong_res_lvl, strong_res_cnt = strongest_resistance(res, res_touches, px)
    strong_res_dist = round((strong_res_lvl - px) / px * 100, 1) if strong_res_lvl else None

    # Entry / SL / TP
    entry_low, entry_high = entry_zone(s1, s2, r1, px, is_crypto)
    sl, tp1, tp2, tp3 = sl_tp(s1, s2, r1, r2, px, is_crypto)
    rr = risk_reward(entry_low, sl, tp1)

    # ===== SCORING (improved) =====
    score = 0
    reasons = []

    # Trend (SMA alignment)
    if s20 and px > s20: score += 12; reasons.append("px>SMA20")
    if s50 and px > s50: score += 10; reasons.append("px>SMA50")
    if s200 and px > s200: score += 8; reasons.append("px>SMA200")
    # SMA20 > SMA50 (golden cross)
    if s20 and s50 and s20 > s50: score += 5; reasons.append("SMA20>SMA50")

    # RSI filter
    if rsi14:
        if 40 <= rsi14 <= 60: score += 12; reasons.append(f"RSI={rsi14}(optimal)")
        elif 30 <= rsi14 < 40: score += 8; reasons.append(f"RSI={rsi14}(oversold)")
        elif 60 < rsi14 <= 70: score += 5; reasons.append(f"RSI={rsi14}(warm)")
        elif rsi14 > 75: score -= 10; reasons.append(f"RSI={rsi14}(OVERBOUGHT!)")
        elif rsi14 < 30: score += 3; reasons.append(f"RSI={rsi14}(deep oversold)")

    # MACD
    if macd_h:
        if macd_h > 0 and macd_l > macd_s: score += 8; reasons.append("MACD↑")
        elif macd_h > 0: score += 3; reasons.append("MACD>0")
        elif macd_h < 0 and macd_l > macd_s: score += 5; reasons.append("MACD cross↑")

    # OBV
    if obv_short == "UP" and obv_med == "ACCUMULATION": score += 15; reasons.append("OBV↑↑(20d)")
    elif obv_short == "UP": score += 8; reasons.append("OBV↑(5d)")
    elif obv_short == "DOWN" and obv_med == "DISTRIBUTION": score -= 5; reasons.append("OBV↓↓")
    elif obv_short == "DOWN": score -= 3; reasons.append("OBV↓")

    # Weekly alignment
    if weekly_align == "ALIGN": score += 10; reasons.append("WeeklyALIGN")
    elif weekly_align == "MISALIGN": score -= 5; reasons.append("WeeklyMISALIGN")

    # Distance from support (closer = better entry)
    if s1:
        dist_pct = (px - s1) / s1 * 100
        if dist_pct <= 3: score += 10; reasons.append(f"NearS1({dist_pct:.1f}%)")
        elif dist_pct <= 5: score += 5; reasons.append(f"CloseS1({dist_pct:.1f}%)")
        elif dist_pct > 15: score -= 5; reasons.append(f"FarS1({dist_pct:.1f}%)")

    # Daily change bonus
    if chg > 0: score += 3
    elif chg < -3: score -= 3

    # Risk-Reward quality
    if rr >= 2.5: score += 5; reasons.append(f"RR={rr}(good)")
    elif rr >= 1.5: score += 2; reasons.append(f"RR={rr}(ok)")
    elif rr < 1.0: score -= 5; reasons.append(f"RR={rr}(bad)")

    # Minimum bar count check
    if len(closes) < 200: score -= 5; reasons.append(f"short_data({len(closes)}bars)")

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

# ============== MAIN ==============
print("🔄 Fetching live data...")

# IDX
idx_syms = ["BBRI.JK","BMRI.JK","BBCA.JK","TLKM.JK","ICBP.JK",
            "ASII.JK","UNVR.JK","BRPT.JK","SMGR.JK","ADRO.JK"]
idx_results = []
for s in idx_syms:
    r = analyze_symbol(s, is_idx=True)
    if r: idx_results.append(r)
    time.sleep(0.2)

# US
us_syms = ["AAPL","MSFT","NVDA","GOOGL","AMZN","META","TSLA","AMD","AVGO","JPM"]
us_results = []
for s in us_syms:
    r = analyze_symbol(s, is_idx=False)
    if r: us_results.append(r)
    time.sleep(0.2)

# CRYPTO
crypto_syms = ["BTC-USD","ETH-USD","SOL-USD","BNB-USD","XRP-USD","DOGE-USD","ADA-USD"]
crypto_results = []
for s in crypto_syms:
    r = analyze_symbol(s, is_crypto=True)
    if r: crypto_results.append(r)
    time.sleep(0.2)

# CoinGecko
print("🪙 Fetching CoinGecko cross-check...")
cg = fetch_json("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=20&page=1&sparkline=false&price_change_percentage=24h")
cg_map = {}
if cg:
    for m in cg:
        sym_key = m["symbol"].upper() + "-USD"
        cg_map[sym_key] = m

# Indodax
print("🇮🇩 Fetching Indodax IDR prices...")
idxdx = fetch_json("https://indodax.com/api/tickers")
idr_map = {}
if idxdx and "tickers" in idxdx:
    idr_map = idxdx["tickers"]

# Merge crypto
for r in crypto_results:
    cg_data = cg_map.get(r["sym"], {})
    cg_px = cg_data.get("current_price")
    if cg_px and r["px"] > 0:
        avg = round((r["px"] + cg_px) / 2, 2)
        diff = abs(r["px"] - cg_px) / r["px"] * 100
    else:
        avg = r["px"]; diff = 0; cg_px = None
    r["cg_px"] = cg_px; r["avg"] = avg; r["diff"] = diff
    pair = r["sym"].replace("-USD","_idr").lower()
    idr_data = idr_map.get(pair, {})
    r["idr"] = int(float(idr_data.get("last", 0)))
    r["vol_idr"] = float(idr_data.get("vol_idr", 0))

# Rank
idx_results.sort(key=lambda x: -x["score"])
us_results.sort(key=lambda x: -x["score"])
crypto_results.sort(key=lambda x: -x["score"])

idx_top = idx_results[:10]
us_top = us_results[:7]
crypto_top = crypto_results[:5]

# IHSG & USD/IDR
print("📊 Fetching IHSG & USD/IDR...")
ihsg = analyze_symbol("^JKSE")
usd_idr = analyze_symbol("USDIDR=X")

# ============== PRINT REPORT ==============
now = datetime.utcnow().timestamp() + TZ_WIB
dt = datetime.fromtimestamp(now).strftime("%A, %d %B %Y — %H:%M WIB")

print("\n" + "=" * 80)
print(f"   📊 REPORT MARKET — {dt}")
print("=" * 80)

sent = "NEUTRAL"
if ihsg and ihsg["chg"] > 0.5: sent = "🟢 RISK-ON"
elif ihsg and ihsg["chg"] < -0.5: sent = "🔴 RISK-OFF"
print(f"   Sentimen: {sent}")
if ihsg: print(f"   IHSG: {ihsg['px']:,.0f} ({ihsg['chg']:+.2f}%)")
if usd_idr: print(f"   USD/IDR: {usd_idr['px']:,.0f} ({usd_idr['chg']:+.2f}%)")

# ====== IDX ======
print("\n" + "=" * 80)
print("   🇮🇩 SAHAM IDX — TOP 10 RANKED BY SCORE")
print("=" * 80)
for i, r in enumerate(idx_top, 1):
    e_low, e_high = r["entry"]
    obv_icon = "🟢" if r["obv_s"] == "UP" else ("🔴" if r["obv_s"] == "DOWN" else "⚪")
    w_icon = "✅" if r["w_align"] == "ALIGN" else ("❌" if r["w_align"] == "MISALIGN" else "—")
    ss = r["strong_sup"] or 0
    sd = r["strong_dist"] or 0
    sr = r["strong_res"] or 0
    srd = r["strong_res_dist"] or 0
    sk1 = r["s1"] or 0
    sk2 = r["s2"] or 0
    rk1 = r["r1"] or 0
    rk2 = r["r2"] or 0
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
    obv_icon = "🟢" if r["obv_s"] == "UP" else ("🔴" if r["obv_s"] == "DOWN" else "⚪")
    w_icon = "✅" if r["w_align"] == "ALIGN" else ("❌" if r["w_align"] == "MISALIGN" else "—")
    ss = r["strong_sup"] or 0
    sd = r["strong_dist"] or 0
    sr = r["strong_res"] or 0
    srd = r["strong_res_dist"] or 0
    sk1 = r["s1"] or 0
    sk2 = r["s2"] or 0
    rk1 = r["r1"] or 0
    rk2 = r["r2"] or 0
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
    obv_icon = "🟢" if r["obv_s"] == "UP" else ("🔴" if r["obv_s"] == "DOWN" else "⚪")
    idr_str = f"Rp{r['idr']:,}" if r["idr"] else "-"
    vol_m = f"Rp{r['vol_idr']/1e6:.1f}M" if r["vol_idr"] else "-"
    flag = " ⚠️" if r["diff"] > 2 else ""
    ss = r["strong_sup"] or 0
    sd = r["strong_dist"] or 0
    sr = r["strong_res"] or 0
    srd = r["strong_res_dist"] or 0
    sk1 = r["s1"] or 0
    sk2 = r["s2"] or 0
    rk1 = r["r1"] or 0
    rk2 = r["r2"] or 0
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
    names = ", ".join([r["sym"][:5] for r in strong_idx[:3]])
    print(f"   🔥 IDX terkuat (OBV↑ + Weekly ALIGN + Score≥40): {names}")
else:
    print("   ⚠️ Tidak ada setup IDX yang sangat kuat hari ini")

us_strong = [r for r in us_top if r["obv_s"] == "UP" and r["score"] >= 40]
if us_strong:
    names = ", ".join([r["sym"] for r in us_strong[:3]])
    print(f"   🇺🇸 US terkuat (OBV↑ + Score≥40): {names}")

overbought = [r for r in idx_top + us_top if r["rsi"] and r["rsi"] > 72]
if overbought:
    names = ", ".join([r["sym"][:5] for r in overbought])
    print(f"   ⚠️ OVERBOUGHT (RSI>72): {names} — waspada koreksi")

crypto_accum = [r for r in crypto_top if r["obv_s"] == "UP" and r["obv_m"] == "ACCUMULATION"]
if crypto_accum:
    names = ", ".join([r["sym"].replace("-USD","") for r in crypto_accum])
    print(f"   🪙 Crypto akumulasi kuat: {names}")

print(f"\n   ⚠️ SL wajib. Entry harus di ZONA, bukan market order. RR min 1:2.")
print("   ⭐ DISCLAIMER: Analisa teknikal, BUKAN nasihat investasi.")
print("=" * 80)
print(f"   ✅ Generated in ~{time.time() - start:.0f}s — market-report-fast v4")
print("=" * 80)
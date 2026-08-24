# Production Script Reference: market_report_fast.py

**Path:** `/opt/data/.hermes/scripts/market_report_fast.py`  
**Version:** v4 (2026-08-07)  
**Runtime:** ~12s, no_agent cron compatible

---

## Key Features Implemented

| Feature | Implementation |
|---|---|
| **Entry Zone** | `S1 * 1.01` to `min(S1*1.03, px*0.98)` |
| **S.KUAT / R.KUAT** | Touch-count based: multi-window [3,5,8] + cluster tolerance 2.5% |
| **TP3** | Fibonacci extension: `r2 + (r2-r1)*0.618` |
| **Cross-check CoinGecko** | `api.coingecko.com/api/v3/simple/price` for crypto USD |
| **Cross-check Indodax** | `indodax.com/api/summaries` for crypto IDR |
| **IHSG** | Yahoo `^JKSE` |
| **USD/IDR** | exchangerate.host → Yahoo `IDR=X` fallback |
| **Overbought filter** | RSI > 72 excluded from ranking |
| **OBV trend** | 20-bar (medium) + 5-bar (short) |

---

## Canonical Output Format (5 lines per asset)

```
  {i}. {SYM} — Score {score} ({chg:+.2f}%)
     🛡️ SL: {sl}  |  🎯 TP1: {tp1}  |  TP2: {tp2}  |  TP3: {tp3}
     ✅ Entry: {e_low} – {e_high}
     🔵 S.KUAT-1: {s1}  |  🔵 S.KUAT-2: {s2}  |  🔴 R.KUAT-1: {r1}  |  🔴 R.KUAT-2: {r2}
     💰 HARGA SEKARANG: {px}  |  RR 1:{rr}
```

**Column order is fixed:** SL → TP1 → TP2 → TP3 → Entry → S.KUAT-1 → S.KUAT-2 → R.KUAT-1 → R.KUAT-2 → Harga Sekarang → RR

---

## Cron Integration

Wrapper: `~/.hermes/scripts/market_report_run.sh`
```bash
cd /opt/data && python3 .hermes/scripts/market_report_fast.py
```

Cronjob config: `no_agent=true`, `deliver=telegram`, `model=hermes provider=custom` (pinned)

---

## Verification Command

Always run after any change:
```bash
cd /opt/data && python3 .hermes/scripts/market_report_fast.py
```

---

## Related

- Governing skill: `daily-market-report-cron` (hub-installed, defines format & rules)
- Experimental pipeline: `/opt/data/iidx-predict/` (R&D only — not for daily reports)
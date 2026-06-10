# Formal Classification — generated from prices/ only

Generated 2026-06-10. Rules as specified by user. Stock = AVGO; sector proxy = SMH (XLK shown as alternate); "all sectors" = 11 SPDRs; broad indices = SPY, QQQ (IWM, EFA shown); safe assets = BIL, TLT, GLD, DXY. Breadth measured on the 25-name semi basket (XLK full membership not in files).

## Rule 1 — IDIOSYNCRATIC (underperform sector by ≥3pp/1d, or ≥5pp/5d, or ≥5pp/1mo)
**Verdict: TRUE — triggers on all three horizons, vs both sector proxies.**

| Horizon    | AVGO    | SMH    | Spread       | XLK    | Spread   | Trigger |
| ---------- | ------- | ------ | ------------ | ------ | -------- | ------- |
| 1d (Jun 4) | −12.59% | −1.63% | **−10.96pp** | −1.56% | −11.03pp | ✓ (≥3)  |
| 5d         | −18.57% | −6.52% | **−12.05pp** | −8.80% | −9.77pp  | ✓ (≥5)  |
| 1mo        | −8.80%  | +4.32% | **−13.12pp** | +2.99% | −11.79pp | ✓ (≥5)  |

Daily spreads vs SMH, last 5 sessions: Jun 3 −1.39 / **Jun 4 −10.96** / Jun 5 +1.30 / Jun 8 −2.18 / Jun 9 +0.08.
Only Jun 4 breaches the 1-day threshold — the entire idiosyncratic component is one session.

## Rule 2 — SECTOR-DRIVEN (sector bottom-3 of 11 AND breadth <35%)
**Verdict: TRUE on 1d and 5d; FALSE on 1mo.**

| Horizon | XLK return | Rank from bottom | Bottom-3? | Breadth (semis up) | <35%? | Verdict |
|---|---|---|---|---|---|---|
| 1d | −1.85% | 1/11 | ✓ | 8/25 = 32% | ✓ | **TRUE** |
| 5d | −8.80% | 1/11 | ✓ | 3/25 = 12% | ✓ | **TRUE** |
| 1mo | +2.99% | 9/11 | ✗ | 17/25 = 68% | ✗ | **FALSE** |

Caveat: breadth uses the 25-semi basket as proxy for sector membership.

## Rule 3 — MARKET STRESS (broad indices negative while ≥3 of 4 safe assets — BIL, TLT, GLD, DXY — positive)
**Verdict: FALSE on every horizon.** (Definition resolved 2026-06-10: safe assets must behave as a group, ≥3 of 4 positive.)

Broad indices (1d / 5d / 1mo / 3mo %):
- SPY −0.29 / −2.96 / −0.08 / +9.14 — negative on 1d, 5d, 1mo
- QQQ −1.15 / −5.14 / −0.48 / +16.61 — negative on 1d, 5d, 1mo
- IWM +0.32 / −2.28 / +0.30 / +12.70 — NOT negative across horizons
- EFA +0.02 / −2.02 / −1.02 / +3.71 — mixed

Safe assets (1d / 5d / 1mo %):
- BIL +0.00 / +0.08 / +0.29 — positive (cash works)
- DXY −0.02 / +0.86 / +1.83 — positive 5d/1mo
- TLT +0.59 / −0.62 / −0.73 — NEGATIVE 5d/1mo
- GLD −1.63 / −5.14 / −9.91 — NEGATIVE everywhere

Safe assets positive, count of 4:
- 1d: TLT only (BIL flat 0.00, DXY −0.02, GLD −1.63) → 1/4 → **FALSE**
- 5d: BIL, DXY (TLT −0.62, GLD −5.14) → 2/4 → **FALSE**
- 1mo: BIL, DXY (TLT −0.73, GLD −9.91) → 2/4 → **FALSE**

## Rule 4 — RATE-FEAR REPRICING (indices negative; cash AND dollar positive; long bonds AND gold falling)
**Verdict: TRUE on 5d and 1mo; FALSE on 1d.**

| Horizon | SPY/QQQ negative | BIL positive | DXY positive | TLT falling | GLD falling | Verdict |
|---|---|---|---|---|---|---|
| 1d | ✓ (−0.29/−1.15) | ✗ (0.00 flat) | ✗ (−0.02) | ✗ (+0.59) | ✓ (−1.63) | **FALSE** |
| 5d | ✓ (−2.96/−5.14) | ✓ (+0.08) | ✓ (+0.86) | ✓ (−0.62) | ✓ (−5.14) | **TRUE** |
| 1mo | ✓ (−0.08/−0.48) | ✓ (+0.29) | ✓ (+1.83) | ✓ (−0.73) | ✓ (−9.91) | **TRUE** |

Corroborating context (news-and-flows.md): Dec rate-hike odds 70% post-payrolls (CME FedWatch via Motley Fool/Fortune), 10Y through 4.53% (CNBC), gold unwind on hike expectations + strong dollar (StoneX).

## Final combined verdict (definitions as resolved 2026-06-10)
**IDIOSYNCRATIC ✓ (all horizons) + SECTOR-DRIVEN ✓ (1d, 5d; not 1mo) + MARKET STRESS ✗ + RATE-FEAR REPRICING ✓ (5d, 1mo).**

In words: a one-day Broadcom-specific repricing (Jun 4, −10.96pp vs sector) inside a sharp, broad sector drawdown (XLK last of 11, breadth 12% on the week), occurring during a rate-fear regime where money is parking in cash and the dollar while long bonds and gold fall — not a flight-to-safety market stress event.

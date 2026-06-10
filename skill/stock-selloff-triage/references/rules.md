# Classification Rules — Formal Spec

Resolved 2026-06-10 during the AVGO selloff triage. These definitions are fixed;
change them only if the user explicitly amends a rule.

## Measurement conventions
- All returns from **Adj Close** in the fetched CSVs. Horizons: 1d = last close
  vs prior close; 5d = last close vs close 5 trading days earlier; 1mo = 21
  trading days.
- "Positive" means strictly > 0 (a flat T-bill print of 0.00 is NOT positive).
- "Negative"/"falling" means strictly < 0.
- Broad indices = SPY and QQQ (both must be negative for Rules 3 and 4; IWM and
  EFA are reported as context but don't gate).
- Safe assets = BIL (T-bills), TLT (long bonds), GLD (gold), DXY (dollar index).
- Sector proxy for Rule 1 = the closest industry ETF if one exists (e.g. SMH),
  with the sector SPDR as alternate; report both, trigger on the primary.
- Breadth basket = ~15–25 liquid same-industry names including the subject stock.

## Rule 1 — IDIOSYNCRATIC
Stock return minus sector-proxy return:
- ≤ −3pp on **any single day** within the last 5 sessions, OR
- ≤ −5pp over **5 days**, OR
- ≤ −5pp over **1 month**.
Any one trigger → TRUE. Also report the daily spread series: one breaching
session (event repricing) reads differently from persistent bleed.

## Rule 2 — SECTOR-DRIVEN (evaluated per horizon)
BOTH required at the same horizon:
- Sector SPDR ranks in the **bottom 3 of the 11 sector SPDRs** by return, AND
- Breadth: **< 35%** of the basket names are up.
Known blind spot (by design, keep noting it): no trend/base-rate component — a
violent week inside an intact uptrend still fires. Always report sector ETF vs
50DMA and % off highs alongside.

## Rule 3 — MARKET STRESS (evaluated per horizon)
- SPY < 0 AND QQQ < 0, AND
- **≥ 3 of 4** safe assets (BIL, TLT, GLD, DXY) positive — safe assets must
  behave *as a group* (this threshold was set deliberately to exclude weeks when
  only cash and the dollar work).

## Rule 4 — RATE-FEAR REPRICING (evaluated per horizon)
- SPY < 0 AND QQQ < 0, AND
- BIL > 0 AND DXY > 0 (money parking in cash and the dollar), AND
- TLT < 0 AND GLD < 0 (rate fear poisons duration and gold).
Mutually exclusive with Rule 3 at the same horizon by construction.
Expect Rule 4 to fail at 1d even in a true rate-fear week — single sessions have
bond bounces; it is a multi-day regime test. That is normal, not a bug.

## Verdict horizon
Rules 2–4 flip across horizons by construction. The final combined call is made
at one pre-declared horizon, **default 5d**. Report all horizons in the tables;
verdict at the declared one.

## Worked example (AVGO, 2026-06-10 — figures from files)
- R1: spreads vs SMH −10.96pp (Jun 4 single day), −12.05pp (5d), −13.12pp (1mo)
  → TRUE all horizons; entire excess move was one session (Jun 4).
- R2: XLK rank 1/11 with breadth 12% (5d) → TRUE; 1mo rank 9/11, breadth 68% → FALSE.
- R3: 5d safe-asset count 2/4 (BIL +0.08, DXY +0.86; TLT −0.62, GLD −5.14) → FALSE.
- R4: 5d SPY −2.96/QQQ −5.14, BIL +0.08, DXY +0.86, TLT −0.62, GLD −5.14 → TRUE.
- Combined at 5d: IDIOSYNCRATIC + SECTOR-DRIVEN + RATE-FEAR REPRICING; no MARKET STRESS.

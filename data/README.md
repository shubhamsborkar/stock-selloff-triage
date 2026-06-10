> Note for this public repo: this is the provenance README copied verbatim from the working analysis folder. The `prices/` CSVs it describes are **not redistributed here** (Yahoo Finance data); the fetch script in `../skill/` reproduces them in one command. Paths refer to the original working folder.

# 2026-06-10 Tech Selloff Data Folder

Rule for this analysis: **every number used must come from these files.**

## Contents
- `prices/` — 50 CSVs, daily OHLCV + Adj Close, 2026-03-10 → 2026-06-09 (64 trading days).
- `news-and-flows.md` — dated news timeline and ETF-flow findings, every item sourced.
- `computed/` — derived tables (returns, breadth, beta) generated from `prices/` only.
- `stock-selloff-triage/` — the reusable skill distilled from this analysis (workflow, formal rules, fetch/classify scripts). Shareable; install by copying into `~/.claude/skills/`.
- `stock-selloff-triage.skill` — the same skill packaged as a single installable file.

## Tickers
- AVGO + peers: AVGO, NVDA, AMD, MRVL, TSM, MU, QCOM
- Semi breadth basket (18 more): INTC, TXN, ADI, AMAT, LRCX, KLAC, ASML, NXPI, MCHP, ON, MPWR, TER, SWKS, QRVO, ENTG, GFS, ARM, COHR
- Tech/semi ETFs + benchmarks: SMH, SOXX, XLK, QQQ, SPY, RSPT
- All 11 sector SPDRs: XLK, XLF, XLE, XLV, XLP, XLU, XLI, XLY, XLB, XLRE, XLC
- Rotation destinations: TLT, GLD, IWM, EFA, BIL
- Macro: TNX_10Y_YIELD (^TNX, 10y yield ×10... value IS the yield in %), VIX (^VIX), DXY (DX-Y.NYB ICE dollar index), BTCUSD (BTC-USD)

## Provenance & caveats
- Source: Yahoo Finance via `yfinance` 1.4.1, pulled 2026-06-10 ~12:10–12:25 IST (markets closed, marketState PREPRE).
- Stooq was the first-choice source but is now behind a JS challenge; raw Yahoo REST endpoints were rate-limited (429). yfinance worked.
- **2026-06-09 row patch:** Yahoo's chart API had not yet backfilled the Jun 9 close at pull time (returned NaN). The Jun 9 OHLC+Volume for all 48 US-listed series was patched from Yahoo's quote endpoint (`regularMarketOpen/DayHigh/DayLow/Price/Volume`), after verifying `regularMarketTime` fell on 2026-06-09 ET. `Adj Close` for Jun 9 is set equal to Close (no same-day adjustment events assumed).
- VIX and TNX_10Y_YIELD: chart history ended 2026-06-08; the 2026-06-09 row for each was appended from the quote endpoint the same way.
- DXY ends 2026-06-08 (Jun 9 quote not patched — futures session boundary ambiguity); BTCUSD ends 2026-06-09 (in-progress Jun 10 bar trimmed).
- Volume column: for Jun 9 this is the quote endpoint's `regularMarketVolume` (regular session); earlier rows are chart-API daily volume. Mixing is noted in case of small definitional differences.
- Prices are split/dividend-unadjusted in OHLC; use `Adj Close` for total-return-ish comparisons. Over a 3-month window the difference is small except around ex-div dates (sector ETFs went ex ~mid-June/March quarters).

## Reproduce
Pull script logic: `yf.download(sym, period="3mo", interval="1d", auto_adjust=False)` + quote-endpoint patch for the final bar.

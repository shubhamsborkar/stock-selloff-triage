---
name: stock-selloff-triage
description: >-
  Classify why a stock is selling off: is the stock weak on its own, is its
  sector breaking down, is it broad market stress, or a rate-fear repricing —
  and where the money is going. Fetches ~3 months of daily prices to CSVs,
  builds a sourced news/flows timeline, and applies four formal classification
  rules (IDIOSYNCRATIC, SECTOR-DRIVEN, MARKET STRESS, RATE-FEAR REPRICING) with
  exact figures, all traceable to fetched files. Use this whenever the user
  asks "is my stock weak or is its sector breaking?", "why is TICKER down",
  "is this drop idiosyncratic or sector-wide", "classify this selloff",
  "is the whole sector breaking down", "where is the money rotating", or names
  a stock that dropped sharply and wants to understand the cause — even if
  they don't say "triage" or "classify".
---

# Stock Selloff Triage

Answer three questions about a falling stock with formal, reproducible classifications:
1. Is the stock weak on its own? (IDIOSYNCRATIC)
2. Is its sector breaking down? (SECTOR-DRIVEN)
3. Where is the money going? (MARKET STRESS vs RATE-FEAR REPRICING)

## Non-negotiable principles

- **Every figure traces to fetched files.** All numbers in the final answer come
  from CSVs/markdown written to the dated data folder — never from memory or
  directly from a web page. News articles supply *narrative and catalysts*, with a
  source link per item; if a news figure conflicts with the price files, the files
  win and the discrepancy is noted (news outlets often quote intraday or
  different-baseline moves).
- **Fix the verdict horizon up front.** The rules below evaluate at 1-day, 5-day,
  and 1-month, and they routinely disagree across horizons by construction. Before
  reporting, state which horizon carries the verdict. **Default: 5-day** — it
  matches the "what happened this week" question and smooths single-session
  noise. Use a different horizon only if the user asks for one (don't block to
  ask; state the default and proceed).
- **No investment advice.** These are classifications of realized price behavior.

## The four rules (resolved definitions — do not improvise)

Full spec with worked example: [references/rules.md](references/rules.md). Summary:

1. **IDIOSYNCRATIC** — stock underperforms its sector ETF by ≥3pp on any single
   day in the window, or ≥5pp over 5 days, or ≥5pp over 1 month.
2. **SECTOR-DRIVEN** — the stock's sector SPDR ranks bottom-3 of the 11 SPDRs at
   that horizon AND breadth (% of the peer/industry basket up) is below 35%.
3. **MARKET STRESS** — SPY and QQQ both negative at that horizon while at least
   3 of 4 safe assets (BIL, TLT, GLD, DXY) are positive (safe assets behaving
   as a group; flat = not positive).
4. **RATE-FEAR REPRICING** — SPY and QQQ both negative; BIL AND DXY positive;
   TLT AND GLD both falling. (Looks like stress, but money hides in cash and
   the dollar because rate fear poisons long bonds and gold too.)

More than one can be true. Report each rule's verdict per horizon with exact
figures, then the combined call at the verdict horizon.

## Workflow

### 1. Set up
- Identify the ticker, its sector SPDR, the closest industry ETF (e.g. SMH for a
  semiconductor name — use it as the Rule 1 sector proxy when one exists, with the
  SPDR as alternate), and a peer/breadth basket of ~15–25 liquid names in the same
  industry. Choose these from your own knowledge; they are inputs, not outputs.
- Create a dated folder: `output/YYYY-MM-DD-<ticker>-triage/` (or the user's
  preferred location), with `prices/` and `computed/` inside.

### 2. Fetch prices → `prices/*.csv`
Run `scripts/fetch_prices.py` (needs a venv with `yfinance` and `pandas`; create
one if absent: `python3 -m venv /tmp/yf_env && /tmp/yf_env/bin/pip install -q yfinance pandas`):

```bash
/tmp/yf_env/bin/python scripts/fetch_prices.py \
  --ticker AVGO --sector-etf SMH --sector-spdr XLK \
  --peers NVDA,AMD,MRVL,TSM,MU,QCOM \
  --breadth INTC,TXN,ADI,AMAT,LRCX,KLAC,ASML,NXPI,MCHP,ON,MPWR,TER,SWKS,QRVO,ENTG,GFS,ARM,COHR \
  --outdir <folder>/prices
```

The script always also fetches the 11 SPDRs, SPY/QQQ/IWM/EFA, BIL/TLT/GLD/DXY,
^TNX and ^VIX. It patches the final bar from the quote endpoint when Yahoo's
chart API hasn't backfilled the latest close (common within hours of the close —
verify it reports "ALL FILES CLEAN" at the end; if not, investigate before
proceeding). Write a short `README.md` in the folder noting pull time, source,
and any patches the script reported — provenance is part of the deliverable.

### 3. News & flows → `news-and-flows.md`
Web-search the catalyst story: the stock's earnings/guidance/analyst actions in
the window, the sector-wide narrative, the macro overlay (jobs/CPI/Fed
repricing), and fund-flow data. Structure as a dated timeline; **every item gets
its source link**. Known limitation to check and state: official weekly flow data
(ICI) lags ~1–2 weeks, so flow conclusions are usually price-inferred — say so,
and list the publication date to re-pull as an open item.

### 4. Classify → `computed/`
```bash
/tmp/yf_env/bin/python scripts/classify.py \
  --ticker AVGO --sector-etf SMH --sector-spdr XLK \
  --breadth NVDA,AMD,...,COHR \
  --dir <folder> --verdict-horizon 5d
```
Writes `computed/returns-summary.csv` and `computed/classification.md` (verdict
tables per rule per horizon, with exact figures) and prints the summary.

### 5. Report
Lead with the combined verdict at the verdict horizon, then one short paragraph
per rule quoting the exact figures from `classification.md`. Then add what the
rules can't see — read the computed output critically:
- Rule 2 has no trend component: note whether the sector is above/below its
  50DMA and how far off highs (the script prints this), so a sharp week inside a
  steep uptrend isn't oversold as a "breakdown".
- Check the daily spread series: is the idiosyncratic component one repricing
  session or persistent underperformance? They mean different things.
- Note any news-vs-files numeric discrepancies.
End by noting where the formal verdicts and the narrative diverge, and include
no investment advice.

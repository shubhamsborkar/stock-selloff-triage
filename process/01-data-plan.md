# Move 01 — Demand the data plan before any data

The instruction, exactly as typed:

```text
Tech is selling off this week and Broadcom has dropped around 20 percent in five days. I want to answer three questions: Is Broadcom weak on its own? Is the whole sector breaking down? And where is the money actually going? Before you do anything, tell me exactly what data you would need to answer these three questions properly, and where you would get it from.
```

## Claude's output

Here's the data plan, question by question.

### 1. Is Broadcom weak on its own? (idiosyncratic vs. market-driven)

The test is whether AVGO's drop is explained by the sector move or exceeds it.

**Data needed:**
- **Daily OHLCV for AVGO** over the past 1–3 months — to measure the actual 5-day drawdown, whether it broke key moving averages, and crucially whether the selling came on elevated volume (conviction) or thin volume (drift).
- **The same series for direct peers**: NVDA, AMD, MRVL, TSM, MU, QCOM. If AVGO is down 20% while peers are down 8–10%, that's idiosyncratic. If everything AI-adjacent is down 15–20%, it's the sector.
- **Beta context**: AVGO's beta to SMH/SOX is well above 1, so a 12% sector drop "explains" maybe 15–18% of AVGO's move. The residual is the company-specific part.
- **Company-specific news flow for the past 5–10 days**: earnings or guidance (AVGO reported fiscal Q2 in early June — timing matters a lot here), analyst downgrades or price-target cuts, custom-ASIC customer news (Google, Meta, OpenAI commitments), any insider selling or lockup/secondary activity.
- **Valuation snapshot**: forward P/E now vs. 3 months ago vs. peers — was AVGO the most stretched name going in? The most expensive names fall hardest in a derating regardless of fundamentals.

**Sources:** Stooq or Yahoo Finance for free daily price/volume history (pullable via curl). Web search for the news flow, analyst actions, and the earnings transcript/guidance if the drop straddles the print.

### 2. Is the whole sector breaking down?

One stock falling isn't a sector break; the question is breadth and structure.

**Data needed:**
- **Sector and industry ETFs**: SMH and SOXX (semis), XLK (broad tech), QQQ — 5-day and 1-month returns vs. SPY. The semis-vs-broad-tech split matters: an AI/semi-specific unwind looks very different from a tech-wide derating.
- **Breadth inside the sector**: what fraction of SOX constituents are down over the window, and equal-weight vs. cap-weight performance (RSPT vs. XLK). If cap-weight is down hard but equal-weight is flat, it's a megacap/AI problem, not a sector problem.
- **Technical structure**: did SMH/XLK break their 50-day and 200-day moving averages, or is this a pullback within an uptrend? Distance from highs vs. typical drawdowns this cycle.
- **Rates and vol context**: 10-year Treasury yield over the same window (long-duration tech sells off when yields spike) and VIX (orderly rotation vs. fear event).

**Sources:** Same price endpoints (Stooq/Yahoo) for all ETFs, the yield (^TNX), and VIX. Constituent-level breadth I'd compute myself by pulling the ~30 SOX members' prices.

### 3. Where is the money actually going?

One honest caveat first: every share sold is a share bought, so "where money goes" is really two measurable things — **relative performance** (what's catching a bid) and **fund flows** (where net new ETF/mutual fund dollars land).

**Data needed:**
- **5-day returns for all 11 S&P sector ETFs** (XLK, XLF, XLE, XLV, XLP, XLU, XLI, XLY, XLB, XLRE, XLC) — if XLU/XLP/XLV are green while XLK bleeds, that's a defensive rotation; if XLF/XLE lead, it's a value/cyclical rotation; if everything is red, it's de-grossing, not rotation.
- **Non-equity destinations over the same window**: TLT or the 10-year yield (bonds catching a bid?), gold (GLD), the dollar (DXY), Bitcoin, and short-duration cash proxies (BIL/SGOV flows). If bonds and gold are also down, money is going to cash, full stop.
- **Actual ETF flow data**: net creations/redemptions for SMH, QQQ, XLK vs. defensive and bond ETFs over the past week. This is the only direct evidence of flows rather than inference from prices. Caveat: published flow data lags 1–2 days.
- **Small caps and international** (IWM, EFA/VGK): a rotation out of US megacap tech into "everything else" looks very different from a global risk-off.

**Sources:** Prices again from Stooq/Yahoo. Flow data is the one thing without a clean free API — I'd scrape/search etf.com's fund-flow tool and recent financial press coverage (FT, Bloomberg via search) for the weekly flow numbers.

### What I'd actually compute

A single comparison table: AVGO vs. peers vs. SMH vs. XLK vs. SPY vs. the rotation destinations, over 5-day / 1-month / 3-month windows, plus a breadth count and the news timeline for AVGO specifically. The three answers fall out of that: (1) AVGO's excess drop vs. beta-implied, (2) breadth + trend-break evidence for the sector, (3) what's green and where flows went.

Say the word and I'll pull all of it.

---
Related file: [data/README.md](../data/README.md) — the data plan became the provenance README once the pull was done.

# Move 02 — Pull everything as files, then answer only from the files

The instruction, exactly as typed:

```text
Good. Pull all of it. Two rules. First, everything lands as files in a dated data folder: daily closing prices and volumes as CSVs going back about three months for every ticker and ETF you listed, and the news timeline and any ETF flow findings as a markdown file with the source of every item. Second, from here on, every number we use must come from these files, not from memory or a web page.
```

## Claude's output

(After downloading 50 price CSVs — surviving a Stooq bot-wall, a Yahoo rate limit, and a missing-final-close data glitch that had to be patched from the quote endpoint — plus six web searches for the news timeline and an ICI flows lookup:)

Done. Everything lives in `output/2026-06-10-tech-selloff/` — 50 price CSVs in `prices/` (Mar 10 → Jun 9 closes, with provenance and the one data patch documented in the README), the sourced timeline in `news-and-flows.md`, and derived tables in `computed/`. All numbers below come from those files.

**1. Is Broadcom weak on its own? Yes — most of this drop is Broadcom-specific.** AVGO fell 18.6% over the five days (481.57 → 392.16). Its beta to SMH over the pre-event sample implies only a −4.9% move given SMH's −6.5% week, leaving a **−13.6 point idiosyncratic residual**, on volume running 2.2× its three-month average. The catalyst is in the timeline: a fiscal Q2 beat on June 3 but Q3 AI-chip guidance of ~$16B vs ~$17.2B expected and an unraised $100B full-year AI target, followed by a Macquarie downgrade citing Google insourcing risk. No peer is close — NVDA −6.5%, TSM −4.2%; only QCOM (−14.4%) and MU (−12.0%, memory-pricing story) are in the same zip code. One nuance: AVGO was *not* the most extended name going in — it's up just 14.7% over three months vs SMH +48.7%, so this isn't simply froth coming off.

**2. Is the sector breaking down? Pullback, not breakdown — so far.** Breadth is genuinely weak (22 of 25 semis down on the week, median −6.3%, six names down ≥10%), and equal-weight tech fell as much as cap-weight (RSPT −8.9 vs XLK −8.8), so it's not just a megacap problem. But no trend damage yet: SMH, SOXX, XLK, QQQ and SPY all remain **above their 50-day averages**, semis are only 7–9% off highs after a +49–66% three-month run, and VIX at 19.9 is elevated, not panicked. AVGO is the only one on that list below its 50DMA. The real risk is the macro overlay: the June 5 jobs shock (+172k vs +80k) pushed December rate-hike odds to 70% — that's what turned a Broadcom problem into a market problem.

**3. Where is the money going? Defensive equities and cash — not bonds, not gold.** Within the week, health care +5.6%, real estate +3.4%, staples +2.8% and financials +1.9% were green while XLK fell 8.8% — a genuine intra-equity rotation, not pure de-grossing. But the usual havens were sold too: gold −5.1%, TLT −0.6% with the 10-year up to 4.53%, Bitcoin −3.4%, while the dollar rose and T-bills sat flat. With a hot CPI print expected today (~4.2%), money is hiding in defensives and cash, because rate-hike risk poisons both long bonds and gold. Caveat from the flows file: hard ETF flow data still lags (ICI's latest week is May 27, pre-selloff), so this is price-inferred until the selloff-week flows publish.

---
Related files: [data/news-and-flows.md](../data/news-and-flows.md) (the sourced timeline) and [outputs/key-stats.md](../outputs/key-stats.md) (every figure above, derived from the price files).

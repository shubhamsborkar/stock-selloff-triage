# Move 05 — Package the method as a reusable skill

The instruction, exactly as typed:

```text
This worked. Package everything you just did as a reusable skill, so next time I can ask "is my stock weak or is its sector breaking?" in one line and get the same analysis for any ticker. Write the SKILL.md and the scripts into a folder. Encode the resolved classification rules including RATE-FEAR REPRICING, and your own design note: the skill must ask for or default to a verdict horizon up front, with 5-day as the default lens. Also keep the rule that every figure must trace to fetched files.
```

## Claude's output

The skill is built, installed, and verified. It lives at `~/.claude/skills/stock-selloff-triage/`:

- **SKILL.md** — the workflow: set up a dated folder, fetch prices to CSVs, build a sourced news/flows timeline, run the classifier, report. It encodes both of your rules as non-negotiable principles: every figure must trace to fetched files (news wins narrative, files win numbers, discrepancies get noted), and the verdict horizon is declared up front with **5-day as the default lens** — stated and proceeded with rather than blocking to ask.
- **references/rules.md** — the formal spec of all four rules exactly as resolved today, including MARKET STRESS as ≥3-of-4 safe assets, RATE-FEAR REPRICING (cash+dollar up, bonds+gold down), the "Rule 4 normally fails at 1d, that's not a bug" note, and the AVGO case as a worked example.
- **scripts/fetch_prices.py** — generalizes today's pull: takes ticker/sector ETF/peers/breadth basket, always adds the 11 SPDRs, SPY/QQQ/IWM/EFA, BIL/TLT/GLD/DXY, ^TNX and ^VIX, auto-patches the stale-final-bar glitch from the quote endpoint (with session-date verification), trims in-progress 24h bars, and exits nonzero unless every file passes the integrity scan.
- **scripts/classify.py** — applies all four rules per horizon, prints exact figures for every trigger, adds the trend context Rule 2 is blind to (50DMA, % off high), distinguishes single-session repricing from persistent bleed in the daily spreads, and writes `classification.md` + `returns-summary.csv`.

Both scripts are tested. The regression test ran `classify.py` against a copy of today's AVGO data and reproduced every figure and verdict from our hand-built classification exactly (−10.96pp Jun 4, breadth 12%, R4 true at 5d/1mo, false at 1d). The end-to-end test fetched fresh data for MU and worked unattended — including auto-patching the same Yahoo backfill glitch we hit manually today — and produced a sensible verdict (MU: idiosyncratic at 1d/5d but +21pp *ahead* of its sector at 1mo, which is the horizon discipline doing its job).

Next time, "is MU weak or is its sector breaking?" in one line will trigger it — the skill is already registered in this session.

*(A volume-conviction line — 5-day average volume vs the prior window, as a ratio and z-score — was added to classify.py when this repo was assembled, carrying the session's 2.2× volume check into the skill.)*

---
Related file: [skill/stock-selloff-triage/SKILL.md](../skill/stock-selloff-triage/SKILL.md) — the skill itself; rules spec in [skill/stock-selloff-triage/references/rules.md](../skill/stock-selloff-triage/references/rules.md).

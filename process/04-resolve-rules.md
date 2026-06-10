# Move 04 — Resolve the ambiguous rule, add the missing category

The instruction, exactly as typed:

```text
Good catch on the market stress rule. Resolve it like this: MARKET STRESS requires safe assets behaving as a group, meaning at least three of the four (T-bills, long bonds, gold, dollar) positive while broad indices are negative. And add a fourth classification: RATE-FEAR REPRICING, for when indices are negative, cash and the dollar are positive, but long bonds and gold are falling too. That is what this week is. Update the classification file with the final verdict using these definitions.
```

## Claude's output

`computed/classification.md` is updated with the resolved definitions. Final verdict:

- **IDIOSYNCRATIC — TRUE** on all three horizons (−10.96pp vs SMH on Jun 4; −12.05pp on 5d; −13.12pp on 1mo), with the note that the entire excess move is the single Jun 4 session.
- **SECTOR-DRIVEN — TRUE on 1d and 5d** (XLK last of 11 both times; breadth 32% and 12%), **FALSE on 1mo** (XLK 3rd best, breadth 68%).
- **MARKET STRESS — FALSE on every horizon** under the resolved ≥3-of-4 rule. The safe-asset count never gets past 2 of 4: on 5d and 1mo it's BIL and DXY positive with TLT and GLD negative; on 1d it's TLT alone.
- **RATE-FEAR REPRICING — TRUE on 5d and 1mo, FALSE on 1d.** The 5-day row reads exactly as you defined it: SPY/QQQ −2.96/−5.14, BIL +0.08, DXY +0.86, TLT −0.62, GLD −5.14. Same shape at 1 month. The 1-day failure is just because the most recent session (Jun 9) had TLT bouncing +0.59 and DXY flat — the regime test is a multi-day construct, and it behaves that way.

The file also keeps the corroborating non-price context pinned to the verdict (70% December hike odds, 10-year through 4.53%, the gold unwind), each with its source from news-and-flows.md. One classification-design note worth keeping in mind: SECTOR-DRIVEN and RATE-FEAR both flip between horizons by construction, so when you reuse these rules on a future event it's worth fixing in advance which horizon is the "verdict" horizon — this week, 5-day is clearly the right lens, and on that lens the combined answer is: idiosyncratic Broadcom repricing + sector drawdown + rate-fear regime, no market stress.

---
Related file: [outputs/classification.md](../outputs/classification.md) — the final resolved verdict, including the RATE-FEAR REPRICING table.

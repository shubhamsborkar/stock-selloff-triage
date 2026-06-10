# Move 03 — Replace narrative with formal classification rules

The instruction, exactly as typed:

```text
Now apply formal classification rules to what you found. IDIOSYNCRATIC if the stock underperforms its sector by 3 points or more on 1 day or 5 or more on 5 days or 1 month. SECTOR-DRIVEN if the sector ranks bottom three of all sectors with breadth below 35 percent. MARKET STRESS if broad indices are negative across horizons while safe assets like T-bills, long bonds, gold or the dollar are positive. More than one can be true. Give me the verdict per rule with the exact figures, and note where the rules disagree with your earlier narrative, if anywhere. No investment advice.
```

## Claude's output

Verdicts, all figures from the files (full workings saved to `computed/classification.md`):

**IDIOSYNCRATIC — TRUE, and it triggers on every horizon.** Vs SMH: −10.96pp on the single day Jun 4 (AVGO −12.59% vs SMH −1.63%; threshold 3), −12.05pp on 5 days (−18.57% vs −6.52%; threshold 5), −13.12pp on 1 month (−8.80% vs +4.32%; threshold 5). Using XLK as the sector instead, it still triggers everywhere (−11.03 / −9.77 / −11.79pp).

**SECTOR-DRIVEN — TRUE on 1-day and 5-day, FALSE on 1-month.** XLK ranks dead last of the 11 SPDRs on both 1d (−1.85%) and 5d (−8.80%), and breadth is below the 35% line both times: 8 of 25 semis up on the day (32%) and 3 of 25 up on the week (12%). On 1 month the rule fails outright — XLK ranks 9th from the bottom (i.e., 3rd best, +2.99%) with 68% breadth. Caveat: breadth is measured on the 25-name semi basket, since full XLK membership isn't in the files.

**MARKET STRESS — depends on how you read your own rule.** SPY and QQQ are negative on 1d, 5d, and 1mo (SPY −0.29/−2.96/−0.08; QQQ −1.15/−5.14/−0.48). On the safe-asset side the four named assets split two-and-two over 5 days: BIL +0.08% and DXY +0.86% positive; TLT −0.62% and GLD −5.14% negative. If "T-bills, long bonds, gold or the dollar" means *any* of them positive, the rule fires. If it means safe assets behaving as a group, it fails — and note IWM is actually *up* on 1d and 1mo, and everything is strongly positive at 3 months. You'd want to pin down the intended reading before this rule goes in a playbook.

**Where the rules disagree with my earlier narrative:**

1. **The rules say SECTOR-DRIVEN; I said "pullback, not breakdown."** Both are computed from the same files — the rule measures relative rank and breadth over a window (both awful), while my narrative leaned on trend state (SMH/XLK still above their 50-day averages, semis +49–66% over 3 months). Your rule set has no trend or base-rate component, so it will classify any sharp week inside a strong uptrend as a sector event. The 1-month FALSE is the rule itself hinting at this.

2. **The daily spreads sharpen — and partly correct — my AVGO story.** I framed Jun 9 (−4.68%... actually −1.12% close-to-close in the files; the −4.68% from the news item doesn't match the file and the file wins) as "the fade resumes" for AVGO. But the spread vs SMH that day was +0.08pp — Jun 9 was a sector move, not a Broadcom move. The entire idiosyncratic component sits in one session, Jun 4; on the other four days AVGO traded within ±2.2pp of its sector. One repricing event, then beta.

3. **Market stress is where rule and narrative genuinely diverge.** My narrative said "not classic risk-off" because gold and long bonds were falling. The loose reading of your rule fires anyway, on the strength of cash and the dollar alone — which is technically consistent with my "money went to cash" finding but stretches the label "stress" over what the strict reading (and the gold/TLT signs) says is a rate-fear repricing, not a flight to safety.

Note on the data: one discrepancy surfaced — the TradingKey news item reported AVGO −4.68% on Jun 9, but the files show −1.12% close-to-close. Per your rule, the file number is the one used; the news figure may reference an intraday or different-baseline move. I've left both visible (news in news-and-flows.md, price in the CSVs).

No investment advice in any of the above — these are classifications of realized price behavior only.

---
Related file: [outputs/classification.md](../outputs/classification.md) — the full verdict tables with every figure.

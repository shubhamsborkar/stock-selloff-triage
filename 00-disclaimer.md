# Disclaimer

**Educational and research purposes only.**

Nothing in this repository — including the classification rules, the verdicts, the computed statistics, the news timeline, and the bundled skill — is investment advice, a recommendation, an offer, or a solicitation to buy or sell any security or other financial instrument. The classifications describe *realized, historical* price behavior under fixed written rules; they say nothing about future returns.

Specifics worth understanding before you reuse any of this:

- **The rules are arbitrary by design.** Thresholds like "3 points on 1 day" or "3 of 4 safe assets" were chosen for clarity and reproducibility, not optimized or backtested. Different thresholds give different verdicts. The verdict-horizon choice alone (1-day vs 5-day vs 1-month) flips several classifications in the worked example.
- **The data is third-party and best-effort.** Prices come from Yahoo Finance via the `yfinance` library, unofficially and without warranty. The provenance README in `data/` documents a real data defect encountered during the build (a missing final close, patched from a secondary endpoint) — assume similar defects can occur on any run. Verify independently before relying on any figure.
- **News items reflect their sources.** Every timeline item links to its source; figures quoted by news outlets occasionally conflict with the price files (one such discrepancy is documented in the process logs). Where they conflict, this project uses the files — but neither is guaranteed correct.
- **Fund-flow conclusions are partly inferred.** Official weekly flow data lags by one to two weeks; "where the money went" conclusions drawn within the event week are price-inferred, as stated in the analysis.
- **No fitness for purpose.** The authors and contributors accept no liability for any loss arising from use of this repository. Markets involve risk, including loss of principal. Consult a qualified, licensed financial adviser before making investment decisions.

The AVGO/June 2026 case study is a snapshot of a specific moment, produced the morning of 2026-06-10 with data through the 2026-06-09 US close. It was not updated afterward.

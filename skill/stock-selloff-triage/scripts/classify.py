#!/usr/bin/env python3
"""Apply the four selloff-classification rules to fetched price CSVs.

Reads <dir>/prices/*.csv (produced by fetch_prices.py), writes
<dir>/computed/returns-summary.csv and <dir>/computed/classification.md,
and prints the verdict summary. Every figure derives from the CSVs only.

Rules (see references/rules.md for the spec):
  1 IDIOSYNCRATIC      stock vs sector ETF: <=-3pp any 1d (last 5), <=-5pp 5d, <=-5pp 1mo
  2 SECTOR-DRIVEN      sector SPDR bottom-3 of 11 AND basket breadth <35% (per horizon)
  3 MARKET STRESS      SPY<0 AND QQQ<0 AND >=3 of {BIL,TLT,GLD,DXY} > 0 (per horizon)
  4 RATE-FEAR REPRICING SPY<0 AND QQQ<0 AND BIL>0 AND DXY>0 AND TLT<0 AND GLD<0

Usage:
  classify.py --ticker AVGO --sector-etf SMH --sector-spdr XLK \
      --breadth NVDA,AMD,... --dir <folder> [--verdict-horizon 5d]
"""
import argparse
import glob
import os

import numpy as np
import pandas as pd

SPDRS = ["XLK", "XLF", "XLE", "XLV", "XLP", "XLU", "XLI", "XLY", "XLB", "XLRE", "XLC"]
HORIZONS = [("1d", 1), ("5d", 5), ("1mo", 21)]


def load(prices_dir):
    data = {}
    for f in glob.glob(os.path.join(prices_dir, "*.csv")):
        data[os.path.basename(f)[:-4]] = (
            pd.read_csv(f, index_col=0, parse_dates=True).sort_index()["Adj Close"].dropna()
        )
    return data


def ret(data, t, days):
    s = data[t]
    days = min(days, len(s) - 1)
    return (s.iloc[-1] / s.iloc[-1 - days] - 1) * 100


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ticker", required=True)
    ap.add_argument("--sector-etf", required=True)
    ap.add_argument("--sector-spdr", required=True)
    ap.add_argument("--breadth", required=True, help="comma list; subject ticker auto-included")
    ap.add_argument("--dir", required=True)
    ap.add_argument("--verdict-horizon", default="5d", choices=["1d", "5d", "1mo"])
    args = ap.parse_args()

    data = load(os.path.join(args.dir, "prices"))
    tkr, setf, spdr = args.ticker, args.sector_etf, args.sector_spdr
    basket = sorted({t for t in args.breadth.split(",") if t} | {tkr})
    missing = [t for t in [tkr, setf, spdr] + basket if t not in data]
    if missing:
        raise SystemExit(f"missing price files for: {missing}")

    outdir = os.path.join(args.dir, "computed")
    os.makedirs(outdir, exist_ok=True)

    # returns summary for everything we have
    rows = [{"ticker": t, **{h: round(ret(data, t, d), 2) for h, d in HORIZONS},
             "full_window": round(ret(data, t, len(data[t]) - 1), 2),
             "last_date": str(data[t].index[-1].date())} for t in sorted(data)]
    pd.DataFrame(rows).set_index("ticker").to_csv(os.path.join(outdir, "returns-summary.csv"))

    L = []  # markdown lines

    # ---- Rule 1
    s, m = data[tkr], data[setf]
    vol = pd.read_csv(os.path.join(args.dir, "prices", f"{tkr}.csv"),
                      index_col=0, parse_dates=True)["Volume"].dropna()
    v5, vprior = vol.iloc[-5:].mean(), vol.iloc[:-5]
    vz = (v5 - vprior.mean()) / vprior.std()
    daily = []
    for i in range(-5, 0):
        a = (s.iloc[i] / s.iloc[i - 1] - 1) * 100
        b = (m.iloc[i] / m.iloc[i - 1] - 1) * 100
        daily.append((s.index[i].date(), a, b, a - b))
    worst_day = min(daily, key=lambda r: r[3])
    sp5 = ret(data, tkr, 5) - ret(data, setf, 5)
    sp21 = ret(data, tkr, 21) - ret(data, setf, 21)
    r1 = {"1d": worst_day[3] <= -3, "5d": sp5 <= -5, "1mo": sp21 <= -5}
    r1_true = any(r1.values())
    n_breach = sum(1 for r in daily if r[3] <= -3)
    L += [f"## Rule 1 — IDIOSYNCRATIC vs {setf}",
          f"**Verdict: {'TRUE' if r1_true else 'FALSE'}** "
          f"(1d {r1['1d']}, 5d {r1['5d']}, 1mo {r1['1mo']})", "",
          f"- Worst 1d spread: {worst_day[3]:+.2f}pp on {worst_day[0]} "
          f"({tkr} {worst_day[1]:+.2f}% vs {setf} {worst_day[2]:+.2f}%); threshold -3pp",
          f"- 5d spread: {sp5:+.2f}pp ({tkr} {ret(data, tkr, 5):+.2f}% vs {setf} {ret(data, setf, 5):+.2f}%); threshold -5pp",
          f"- 1mo spread: {sp21:+.2f}pp ({tkr} {ret(data, tkr, 21):+.2f}% vs {setf} {ret(data, setf, 21):+.2f}%); threshold -5pp",
          f"- Daily spreads (last 5): " + " / ".join(f"{d} {v:+.2f}" for d, _, _, v in daily),
          f"- Sessions breaching -3pp: {n_breach} of 5 "
          f"({'single-session repricing' if n_breach == 1 else 'persistent underperformance' if n_breach > 1 else 'no single-day breach'})",
          f"- Volume conviction: 5d avg {v5/1e6:.0f}M/day vs prior avg {vprior.mean()/1e6:.0f}M "
          f"({v5/vprior.mean():.1f}x, z-score {vz:+.1f})", ""]

    # ---- Rule 2
    L += [f"## Rule 2 — SECTOR-DRIVEN ({spdr} rank + basket breadth)", ""]
    r2 = {}
    for h, d in HORIZONS:
        r = {t: ret(data, t, d) for t in SPDRS if t in data}
        rank = sorted(r, key=r.get).index(spdr) + 1  # 1 = worst
        up = sum(1 for t in basket if ret(data, t, d) > 0)
        breadth = up / len(basket) * 100
        r2[h] = rank <= 3 and breadth < 35
        L.append(f"- {h}: {spdr} {r[spdr]:+.2f}%, rank {rank}/11 from bottom "
                 f"(bottom-3: {rank <= 3}); breadth {up}/{len(basket)} up = {breadth:.0f}% "
                 f"(<35%: {breadth < 35}) -> **{'TRUE' if r2[h] else 'FALSE'}**")
    # trend context (rule has no trend component by design)
    L.append("")
    for t in [setf, spdr]:
        full = pd.read_csv(os.path.join(args.dir, "prices", f"{t}.csv"),
                           index_col=0, parse_dates=True)["Adj Close"].dropna()
        dma = full.rolling(50).mean().iloc[-1]
        L.append(f"- Trend context: {t} close {full.iloc[-1]:.2f} vs 50DMA {dma:.2f} "
                 f"({'BELOW' if full.iloc[-1] < dma else 'above'}), "
                 f"{(full.iloc[-1] / full.max() - 1) * 100:+.1f}% off window high")
    L.append("")

    # ---- Rules 3 & 4
    safe = ["BIL", "TLT", "GLD", "DXY"]
    L += ["## Rule 3 — MARKET STRESS (>=3 of 4 safe assets positive) & "
          "Rule 4 — RATE-FEAR REPRICING", ""]
    r3, r4 = {}, {}
    for h, d in HORIZONS:
        idx_neg = ret(data, "SPY", d) < 0 and ret(data, "QQQ", d) < 0
        vals = {t: ret(data, t, d) for t in safe}
        pos = [t for t in safe if vals[t] > 0]
        r3[h] = idx_neg and len(pos) >= 3
        r4[h] = (idx_neg and vals["BIL"] > 0 and vals["DXY"] > 0
                 and vals["TLT"] < 0 and vals["GLD"] < 0)
        L.append(f"- {h}: SPY {ret(data, 'SPY', d):+.2f}% QQQ {ret(data, 'QQQ', d):+.2f}% "
                 f"(both neg: {idx_neg}); safe assets "
                 + " ".join(f"{t} {vals[t]:+.2f}" for t in safe)
                 + f" -> positive {len(pos)}/4 -> R3 **{'TRUE' if r3[h] else 'FALSE'}**, "
                 f"R4 **{'TRUE' if r4[h] else 'FALSE'}**")
    L.append("")

    # ---- combined verdict
    vh = args.verdict_horizon
    combo = []
    if r1_true:
        combo.append("IDIOSYNCRATIC")
    if r2[vh]:
        combo.append("SECTOR-DRIVEN")
    if r3[vh]:
        combo.append("MARKET STRESS")
    if r4[vh]:
        combo.append("RATE-FEAR REPRICING")
    verdict = " + ".join(combo) if combo else "NONE OF THE FOUR (no rule fires at this horizon)"
    L += [f"## Final verdict at declared horizon ({vh})", "", f"**{verdict}**", "",
          "Rule-by-rule at all horizons: R1 "
          + ", ".join(f"{h}:{v}" for h, v in r1.items())
          + " | R2 " + ", ".join(f"{h}:{v}" for h, v in r2.items())
          + " | R3 " + ", ".join(f"{h}:{v}" for h, v in r3.items())
          + " | R4 " + ", ".join(f"{h}:{v}" for h, v in r4.items()), "",
          "_Classifications of realized price behavior only; not investment advice._"]

    head = [f"# Selloff Classification — {tkr}", "",
            f"Generated from `prices/*.csv` only (Adj Close). Window ends "
            f"{data[tkr].index[-1].date()}. Verdict horizon: **{vh}** (default 5d). "
            f"Sector proxy {setf}; SPDR {spdr}; basket of {len(basket)}.", ""]
    md = "\n".join(head + L) + "\n"
    with open(os.path.join(outdir, "classification.md"), "w") as f:
        f.write(md)
    print(md)


if __name__ == "__main__":
    main()

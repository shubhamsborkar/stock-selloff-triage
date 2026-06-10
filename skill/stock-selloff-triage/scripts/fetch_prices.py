#!/usr/bin/env python3
"""Fetch ~3 months of daily OHLCV to CSVs for a selloff-triage run.

Always fetches, beyond the requested ticker/peers/breadth basket:
  - the 11 sector SPDRs, SPY/QQQ/IWM/EFA (indices)
  - BIL/TLT/GLD + DXY (safe assets), ^TNX (10y yield), ^VIX

Yahoo's chart API often hasn't backfilled the latest session's close for a few
hours after the close (the bar comes back with NaN Close). When that happens,
this script patches the final bar from the quote endpoint after verifying the
quote's regularMarketTime falls on that session's date (US/Eastern). In-progress
bars (24h markets like BTC, or futures-session products) dated after the last
settled US session are trimmed.

Exit code is nonzero if any file still has missing Open/Close after patching.
Usage:
  fetch_prices.py --ticker AVGO --sector-etf SMH --sector-spdr XLK \
      --peers NVDA,AMD --breadth INTC,TXN,... --outdir <dir>/prices
"""
import argparse
import os
import sys
import time
from datetime import datetime
from zoneinfo import ZoneInfo

import pandas as pd
import yfinance as yf

SPDRS = ["XLK", "XLF", "XLE", "XLV", "XLP", "XLU", "XLI", "XLY", "XLB", "XLRE", "XLC"]
INDICES = ["SPY", "QQQ", "IWM", "EFA"]
SAFE = ["BIL", "TLT", "GLD"]
# filename -> yahoo symbol for non-equity series
SPECIAL = {"DXY": "DX-Y.NYB", "TNX_10Y_YIELD": "^TNX", "VIX": "^VIX"}
ET = ZoneInfo("America/New_York")
COLS = ["Open", "High", "Low", "Close", "Adj Close", "Volume"]


def download(sym):
    df = yf.download(sym, period="3mo", interval="1d", auto_adjust=False, progress=False)
    if df is None or df.empty:
        return None
    if hasattr(df.columns, "levels"):
        df.columns = df.columns.get_level_values(0)
    return df[COLS].sort_index()


def patch_last_bar(name, sym, df):
    """If the last bar's Close is NaN, rebuild it from the quote endpoint."""
    if not pd.isna(df["Close"].iloc[-1]):
        return df, None
    info = yf.Ticker(sym).get_info()
    ts = info.get("regularMarketTime")
    if not ts:
        return df, f"{name}: last Close NaN and no quote timestamp"
    qdate = datetime.fromtimestamp(ts, ET).date()
    bardate = df.index[-1].date()
    if qdate != bardate:
        # quote is for a different session; drop the broken bar instead
        return df.iloc[:-1], f"{name}: dropped broken bar {bardate} (quote is for {qdate})"
    row = {
        "Open": info.get("regularMarketOpen"),
        "High": info.get("regularMarketDayHigh"),
        "Low": info.get("regularMarketDayLow"),
        "Close": info.get("regularMarketPrice"),
        "Adj Close": info.get("regularMarketPrice"),  # no same-day adjustment events assumed
        "Volume": info.get("regularMarketVolume"),
    }
    if any(v is None for v in row.values()):
        return df, f"{name}: quote endpoint incomplete, last bar still broken"
    for col, val in row.items():
        df.loc[df.index[-1], col] = val
    return df, f"{name}: patched {bardate} from quote endpoint (close={row['Close']})"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ticker", required=True)
    ap.add_argument("--sector-etf", required=True, help="industry ETF, e.g. SMH")
    ap.add_argument("--sector-spdr", required=True, help="one of the 11 SPDRs")
    ap.add_argument("--peers", default="", help="comma-separated peer tickers")
    ap.add_argument("--breadth", default="", help="comma-separated extra basket tickers")
    ap.add_argument("--outdir", required=True)
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    equities = {args.ticker, args.sector_etf, args.sector_spdr}
    equities |= {t for t in args.peers.split(",") if t}
    equities |= {t for t in args.breadth.split(",") if t}
    equities |= set(SPDRS) | set(INDICES) | set(SAFE)

    syms = {t: t for t in sorted(equities)}
    syms.update(SPECIAL)

    notes, failed = [], []
    # last settled US session = max bar date across SPY (used to trim 24h markets)
    spy_last = None
    for name, sym in syms.items():
        try:
            df = download(sym)
            if df is None:
                failed.append(name)
                continue
            df, note = patch_last_bar(name, sym, df)
            if note:
                notes.append(note)
            if name == "SPY":
                spy_last = df.index[-1]
            df.to_csv(os.path.join(args.outdir, f"{name}.csv"))
            print(f"{name}: {len(df)} rows -> {df.index[-1].date()}")
            time.sleep(0.3)
        except Exception as e:
            failed.append(f"{name} ({e})")

    # trim bars newer than the last settled US session (in-progress 24h/futures bars)
    if spy_last is not None:
        for name in syms:
            path = os.path.join(args.outdir, f"{name}.csv")
            if not os.path.exists(path):
                continue
            df = pd.read_csv(path, index_col=0, parse_dates=True)
            if df.index[-1] > spy_last:
                df = df[df.index <= spy_last]
                df.to_csv(path)
                notes.append(f"{name}: trimmed in-progress bar(s) after {spy_last.date()}")

    # integrity scan
    dirty = []
    for name in syms:
        path = os.path.join(args.outdir, f"{name}.csv")
        if not os.path.exists(path):
            continue
        df = pd.read_csv(path, index_col=0, parse_dates=True)
        if df["Open"].isna().any() or df["Close"].isna().any():
            dirty.append(name)

    print("\n--- provenance notes ---")
    for n in notes:
        print(" *", n)
    if failed:
        print("FAILED DOWNLOADS:", ", ".join(failed))
    if dirty:
        print("DIRTY FILES (missing Open/Close):", ", ".join(dirty))
        sys.exit(1)
    print("ALL FILES CLEAN" if not failed else "CLEAN EXCEPT FAILED DOWNLOADS ABOVE")
    sys.exit(2 if failed else 0)


if __name__ == "__main__":
    main()

"""H-033: pick the dollar size of a counted deposit before any outcome is computed.

Rule, fixed before this script was run: the highest of $10 000, $5 000, $1 000, $500 at which at least 75 wallets
(three times the minimum of 25) have 5+ events in the selection window and those wallets have at least 300 events
in the test period; if none qualifies, $500. Only counts are used: prices convert GRAM to dollars, and an event
must have a close on its day and 7 days later to exist. No return is computed or looked at.

    python scripts/h033_threshold.py datasets/gram_gate_deposits.csv.gz
"""
import sys

import pandas as pd

from crl.data.store import DataStore
from crl.engine import wallets as W

CANDIDATES = [10_000, 5_000, 1_000, 500]
FILTERS = {"min_value": 1, "merge_days": 7, "max_monthly": 100}
SELECTION = {"start": "2023-03-13", "end": "2024-12-24", "min_events": 5, "horizon_days": 7}
TEST_START = "2025-01-01"


def counts(raw: pd.DataFrame, close: pd.Series, min_usd: float) -> tuple[int, int]:
    """(wallets with 5+ selection events, their test-period events) — the same filters as engine/wallets.py."""
    df = raw[raw["value"] >= FILTERS["min_value"]]
    svc = W.services(df, SELECTION["start"], SELECTION["end"], FILTERS["max_monthly"])
    df = df[~df["wallet"].isin(svc)]
    px = close.reindex(pd.to_datetime(df["ts"], unit="s").dt.normalize()).to_numpy()
    df = df[df["value"].to_numpy() * px >= min_usd]
    df = W.merge_close(df, FILTERS["merge_days"]).copy()
    day = pd.to_datetime(df["ts"], unit="s").dt.normalize()
    exists = day.isin(close.index) & (day + pd.Timedelta(days=SELECTION["horizon_days"])).isin(close.index)
    df, day = df[exists.to_numpy()], day[exists]
    in_sel = (day >= pd.Timestamp(SELECTION["start"])) & (day <= pd.Timestamp(SELECTION["end"]))
    n = df[in_sel.to_numpy()].groupby("wallet").size()
    elig = set(n[n >= SELECTION["min_events"]].index)
    in_test = (day >= pd.Timestamp(TEST_START)).to_numpy() & df["wallet"].isin(elig).to_numpy()
    return len(elig), int(in_test.sum())


def main(path: str) -> int:
    raw = pd.read_csv(path)
    close = DataStore().close("GRAMUSDT")
    close = close[close > 0]
    chosen = None
    for usd in CANDIDATES:
        wallets, events = counts(raw, close, usd)
        ok = wallets >= 75 and events >= 300
        print(f"${usd:>6}: {wallets:>5} eligible wallets, {events:>6} test-period events {'✓' if ok else ''}")
        if ok and chosen is None:
            chosen = usd
    chosen = chosen or CANDIDATES[-1]
    print(f"chosen: ${chosen}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))

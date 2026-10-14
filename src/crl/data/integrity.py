"""Data integrity checks run by the data steward before any study touches the data."""
from dataclasses import dataclass

import pandas as pd

MAX_STALE_DAYS = 3
MAX_DAILY_MOVE = 0.6  # |return| above 60 % in a day is flagged for manual review


@dataclass
class Finding:
    series: str
    level: str  # "error" blocks studies, "warn" is reported only
    message: str


def check_series(name: str, s: pd.Series, today: pd.Timestamp, is_price: bool = False,
                 max_stale: int = MAX_STALE_DAYS) -> list[Finding]:
    out: list[Finding] = []
    s = s.dropna()
    if s.empty:
        return [Finding(name, "error", "series is empty")]
    if s.index.has_duplicates:
        out.append(Finding(name, "error", f"{int(s.index.duplicated().sum())} duplicate dates"))
    age = (today.normalize() - s.index.max()).days
    if age > max_stale:
        out.append(Finding(name, "error", f"stale: last value {s.index.max().date()} ({age} days old)"))
    full = pd.date_range(s.index.min(), s.index.max(), freq="D")
    missing = full.difference(s.index)
    if len(missing):
        level = "error" if is_price else "warn"
        out.append(Finding(name, level, f"{len(missing)} missing days, first {missing[0].date()}"))
    if is_price:
        if (s <= 0).any():
            out.append(Finding(name, "error", "non-positive prices"))
        jumps = s.pct_change().abs()
        big = jumps[jumps > MAX_DAILY_MOVE]
        if len(big):
            out.append(Finding(name, "warn", f"{len(big)} daily moves > {MAX_DAILY_MOVE:.0%}, "
                                             f"e.g. {big.index[0].date()}"))
    return out

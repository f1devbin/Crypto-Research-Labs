"""Timing rules. Each rule returns a 0/1 'risk-on' flag decided at the close of each day.

Price rules see only closes up to and including day t. Feature rules lag the external
series by `lag` days (default 1) to allow for publication delay, so a value dated D
is used no earlier than the close of D+1. NaN means "rule not defined yet" — those
days are excluded from evaluation rather than counted as flat.
"""
from typing import Callable

import numpy as np
import pandas as pd


def _flag(cond: pd.Series, defined: pd.Series) -> pd.Series:
    return cond.astype(float).where(defined)


def price_above_sma(close: pd.Series, window: int) -> pd.Series:
    sma = close.rolling(window).mean()
    return _flag(close > sma, sma.notna())


def sma_cross(close: pd.Series, fast: int, slow: int) -> pd.Series:
    f, s = close.rolling(fast).mean(), close.rolling(slow).mean()
    return _flag(f > s, s.notna())


def tsmom(close: pd.Series, lookback: int) -> pd.Series:
    past = close.shift(lookback)
    return _flag(close / past - 1 > 0, past.notna())


def donchian(close: pd.Series, entry: int) -> pd.Series:
    """Enter above the prior `entry`-day high, exit below the prior entry//2-day low."""
    hi = close.rolling(entry).max().shift(1).to_numpy()
    lo = close.rolling(entry // 2).min().shift(1).to_numpy()
    c = close.to_numpy()
    out = np.full(len(c), np.nan)
    state = 0.0
    for i in range(len(c)):
        if np.isnan(hi[i]):
            continue
        if state == 0 and c[i] > hi[i]:
            state = 1.0
        elif state == 1 and not np.isnan(lo[i]) and c[i] < lo[i]:
            state = 0.0
        out[i] = state
    return pd.Series(out, index=close.index)


def feature_threshold(x: pd.Series, threshold: float, long_when: str, lag: int = 1) -> pd.Series:
    v = x.shift(lag)
    cond = {"above": v > threshold, "below": v < threshold}[long_when]
    return _flag(cond, v.notna())


def feature_vs_rolling_quantile(x: pd.Series, q: float, long_when: str, lookback: int = 365,
                                min_periods: int = 180, lag: int = 1) -> pd.Series:
    """Compare the lagged feature with its own trailing quantile (computed strictly before)."""
    v = x.shift(lag)
    ref = v.shift(1).rolling(lookback, min_periods=min_periods).quantile(q)
    cond = {"above": v > ref, "not_above": v <= ref}[long_when]
    return _flag(cond, v.notna() & ref.notna())


def vol_target(close: pd.Series, target: float, lookback: int = 30, cap: float = 1.0) -> pd.Series:
    """Volatility scaling: position = target / realised volatility (annualised, trailing
    `lookback` days up to and including t), capped at `cap` (1.0 = no leverage). Continuous 0..cap."""
    vol = close.pct_change().rolling(lookback).std() * np.sqrt(365)
    return (target / vol).clip(upper=cap).where(vol.notna() & (vol > 0))


def day_of_week(close: pd.Series, days: list) -> pd.Series:
    """In the market on the given UTC weekdays (0 = Monday). The flag at close t sets the
    position for day t+1, so it looks at tomorrow's weekday."""
    nxt = close.index + pd.Timedelta(days=1)
    return pd.Series(np.isin(nxt.weekday, list(days)).astype(float), index=close.index)


def turn_of_month(close: pd.Series, last: int, first: int) -> pd.Series:
    """In the market on the last `last` and the first `first` calendar days of each month."""
    nxt = close.index + pd.Timedelta(days=1)
    from_end = nxt.days_in_month - nxt.day  # 0 on the last day
    return pd.Series(((nxt.day <= first) | (from_end < last)).astype(float), index=close.index)


def asset_above_sma(other: pd.Series, window: int) -> pd.Series:
    """Risk-on while ANOTHER asset (e.g. BTC) closes above its SMA — a market-regime filter."""
    return price_above_sma(other, window)


PRICE_RULES: dict[str, Callable] = {
    "price_above_sma": price_above_sma,
    "sma_cross": sma_cross,
    "tsmom": tsmom,
    "donchian": donchian,
    "vol_target": vol_target,
}
# depend only on the calendar: positions never use returns, so a permutation test is valid
CALENDAR_RULES: dict[str, Callable] = {
    "day_of_week": day_of_week,
    "turn_of_month": turn_of_month,
}
# use another asset's prices; spec carries `asset`
CROSS_RULES: dict[str, Callable] = {
    "asset_above_sma": asset_above_sma,
}
FEATURE_RULES: dict[str, Callable] = {
    "feature_threshold": feature_threshold,
    "feature_vs_rolling_quantile": feature_vs_rolling_quantile,
}
RULE_TYPES = set(PRICE_RULES) | set(FEATURE_RULES) | set(CALENDAR_RULES) | set(CROSS_RULES)


def lookback_days(spec: dict) -> int:
    """How much history a price rule needs before it is defined."""
    return int(max([v for k, v in spec.items() if isinstance(v, int) and not isinstance(v, bool)] + [1]))


def build(spec: dict, store, symbol: str) -> pd.Series:
    """Flag for `symbol` from a rule spec like {"type": "price_above_sma", "window": 50}."""
    spec = dict(spec)
    kind = spec.pop("type")
    close = store.close(symbol)
    if kind in PRICE_RULES or kind in CALENDAR_RULES:
        return (PRICE_RULES.get(kind) or CALENDAR_RULES[kind])(close, **spec)
    if kind in CROSS_RULES:
        other = store.close(spec.pop("asset"))
        full = other.reindex(pd.date_range(min(other.index.min(), close.index.min()), close.index.max(), freq="D"))
        return CROSS_RULES[kind](full, **spec).reindex(close.index)
    if kind in FEATURE_RULES:
        feat = store.feature(spec.pop("feature"))
        # align on the full calendar first so lags count days, then onto trading days
        full = feat.reindex(pd.date_range(min(feat.index.min(), close.index.min()), close.index.max(), freq="D"))
        return FEATURE_RULES[kind](full, **spec).reindex(close.index)
    raise ValueError(f"unknown rule type '{kind}', known: {sorted(RULE_TYPES)}")


def price_rule_fn(spec: dict) -> Callable[[pd.Series], pd.Series]:
    """Closure over a price rule — used by the bootstrap, which rebuilds prices."""
    spec = dict(spec)
    kind = spec.pop("type")
    if kind not in PRICE_RULES:
        raise ValueError(f"bootstrap significance needs a price rule, got '{kind}'")
    fn = PRICE_RULES[kind]
    return lambda c: fn(c, **spec)

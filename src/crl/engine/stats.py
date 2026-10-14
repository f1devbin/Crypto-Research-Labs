"""Significance tests. Both return a one-sided p-value: the share of null worlds where the
strategy scores at least as well as in reality (with the +1 correction, never exactly 0)."""
from typing import Callable

import numpy as np
import pandas as pd

from crl.engine.backtest import run, sharpe

MIN_SHIFT = 30


def _strategy_returns(pos: np.ndarray, r: np.ndarray, fee: float) -> np.ndarray:
    turn = np.abs(np.diff(pos, prepend=pos[0]))
    return pos * r - turn * fee


def circular_shift_p(pos: np.ndarray, r: np.ndarray, fee: float, rng: np.random.Generator,
                     n: int = 2000) -> float:
    """Null: the timing is unrelated to returns. Rotating the position series keeps its
    exposure and trade frequency but breaks any link to the dates it was meant for."""
    pos = np.asarray(pos, dtype=float)
    r = np.asarray(r, dtype=float)
    L = len(pos)
    if L < 3 * MIN_SHIFT:
        return 1.0
    actual = sharpe(_strategy_returns(pos, r, fee))
    ks = rng.integers(MIN_SHIFT, L - MIN_SHIFT, size=n)
    better = sum(sharpe(_strategy_returns(np.roll(pos, k), r, fee)) >= actual for k in ks)
    return float((better + 1) / (n + 1))


def permutation_p(pos: np.ndarray, r: np.ndarray, fee: float, rng: np.random.Generator,
                  n: int = 2000) -> float:
    """Null: returns do not depend on the date. Shuffling the daily returns under a fixed
    calendar position breaks any day-of-week / day-of-month link. Valid only for rules whose
    positions don't depend on returns (calendar rules); for those a circular shift would
    just reproduce the same weekly pattern."""
    pos = np.asarray(pos, dtype=float)
    r = np.asarray(r, dtype=float)
    if len(pos) < 90:
        return 1.0
    actual = sharpe(_strategy_returns(pos, r, fee))
    better = sum(sharpe(_strategy_returns(pos, rng.permutation(r), fee)) >= actual for _ in range(n))
    return float((better + 1) / (n + 1))


def bootstrap_p(rule: Callable[[pd.Series], pd.Series], hist: np.ndarray, oos_close: np.ndarray,
                fee: float, mode: str, rng: np.random.Generator, n: int = 400) -> float:
    """Null: there is no trend to catch. Resampling out-of-sample daily returns (iid) keeps
    drift and volatility but destroys serial structure; the same rule is re-run on each
    synthetic path, warmed up on the real history before the period."""
    def oos_sharpe(prices: np.ndarray) -> float:
        c = pd.Series(np.concatenate([hist, prices]))
        flag = rule(c)
        dec = flag if mode == "long_flat" else 2 * flag - 1
        s, _ = run(dec.fillna(0.0), c.pct_change().fillna(0.0), fee)
        return sharpe(s.iloc[len(hist):])

    actual = oos_sharpe(oos_close)
    r_oos = np.diff(np.concatenate([[hist[-1]], oos_close])) / np.concatenate([[hist[-1]], oos_close[:-1]])
    better = 0
    for _ in range(n):
        rb = rng.choice(r_oos, size=len(r_oos), replace=True)
        better += oos_sharpe(hist[-1] * np.cumprod(1 + rb)) >= actual
    return float((better + 1) / (n + 1))


def spearman_ic(x: np.ndarray, fwd: np.ndarray) -> float:
    m = ~(np.isnan(x) | np.isnan(fwd))
    if m.sum() < 30:
        return float("nan")
    a = pd.Series(x[m]).rank().to_numpy()
    b = pd.Series(fwd[m]).rank().to_numpy()
    return float(np.corrcoef(a, b)[0, 1])

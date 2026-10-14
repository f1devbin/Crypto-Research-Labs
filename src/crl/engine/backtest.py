"""Daily backtest. The decision taken at the close of day t is held during day t+1."""
import numpy as np
import pandas as pd

DAYS_PER_YEAR = 365  # crypto trades every day


def run(decision: pd.Series, r: pd.Series, fee: float) -> tuple[pd.Series, pd.Series]:
    """Strategy daily returns and turnover.

    decision[t] — target position (0..1 long/flat, -1..1 long/short) decided at the close of t.
    r[t]        — asset return from close t-1 to close t.
    fee         — cost per unit of turnover (one side).
    """
    pos = decision.shift(1).fillna(0.0)
    turnover = pos.diff().abs()
    turnover.iloc[0] = abs(pos.iloc[0])
    return pos * r - turnover * fee, turnover


def sharpe(x) -> float:
    x = np.asarray(x, dtype=float)
    sd = x.std(ddof=1) if len(x) > 1 else 0.0
    return float(x.mean() / sd * np.sqrt(DAYS_PER_YEAR)) if sd > 0 else 0.0


def metrics(s: pd.Series) -> dict:
    """CAGR, Sharpe and max drawdown of a daily return series."""
    if len(s) == 0:
        return {"cagr": 0.0, "sharpe": 0.0, "max_dd": 0.0}
    eq = (1 + s).cumprod()
    years = len(s) / DAYS_PER_YEAR
    final = float(eq.iloc[-1])
    cagr = final ** (1 / years) - 1 if final > 0 else -1.0
    return {"cagr": float(cagr), "sharpe": sharpe(s), "max_dd": float((eq / eq.cummax() - 1).min())}


def to_position(flag: pd.Series, mode: str) -> pd.Series:
    """Map a 0/1 'risk-on' flag to a position: long_flat → 0/1, long_short → -1/+1. NaN is kept."""
    if mode == "long_flat":
        return flag
    if mode == "long_short":
        return 2 * flag - 1
    raise ValueError(f"unknown mode '{mode}'")


def evaluate_period(decision: pd.Series, close: pd.Series, mask: np.ndarray, fee: float) -> dict:
    """Strategy vs buy-and-hold on the days selected by mask where the position is defined."""
    r = close.pct_change().fillna(0.0)
    d = decision.reindex(close.index)
    s, turn = run(d.fillna(0.0), r, fee)
    pos = d.shift(1)
    m = np.asarray(mask) & pos.notna().to_numpy()
    n = int(m.sum())
    strat, hold = metrics(s[m]), metrics(r[m])
    years = max(n / DAYS_PER_YEAR, 1e-9)
    return {
        "days": n,
        "start": str(close.index[m][0].date()) if n else None,
        "end": str(close.index[m][-1].date()) if n else None,
        "sharpe": strat["sharpe"], "cagr": strat["cagr"], "max_dd": strat["max_dd"],
        "hold_sharpe": hold["sharpe"], "hold_cagr": hold["cagr"], "hold_max_dd": hold["max_dd"],
        "exposure": float(pos[m].abs().mean()) if n else 0.0,
        "trades_per_year": float(turn[m].sum() / 2 / years),
        "_pos": pos[m].to_numpy(),
        "_r": r[m].to_numpy(),
    }

"""Cross-sectional studies: each day rank the coins of a universe and hold a few of them.

Decision at the close of day t, held during day t+1 (same convention as backtest.run). Coins enter
the ranking only once they have enough history, so the universe grows as coins get listed.

Signal types
  momentum  score = mean cross-sectional percentile rank of the returns over `lookbacks` days.
            Ranking by return relative to BTC gives the same order (the BTC return is subtracted
            from every coin), so "relative strength" is this rule.
  reversal  the same score with the sign flipped: hold the biggest recent losers.

Optional filters
  overheat_z     skip a coin whose last daily return is more than z standard deviations of its own
                 previous `z_window` days (|z| for reversal), i.e. an extreme one-day jump.
  market_filter  hold nothing while `asset` closes below its `window`-day average.
"""
import numpy as np
import pandas as pd

from crl.engine.backtest import DAYS_PER_YEAR, metrics, sharpe

MIN_SHIFT = 30


def panel(store, universe: list[str]) -> pd.DataFrame:
    return pd.DataFrame({s: store.close(s) for s in universe}).sort_index()


def weights(spec: dict, closes: pd.DataFrame, store=None) -> pd.DataFrame:
    sig, sel = spec["signal"], spec["select"]
    r = closes.pct_change(fill_method=None)
    ranks = [(closes / closes.shift(lb) - 1).rank(axis=1, pct=True) for lb in sig["lookbacks"]]
    score = sum(ranks) / len(ranks)
    if sig["type"] == "reversal":
        score = -score
    elif sig["type"] != "momentum":
        raise ValueError(f"unknown cross-section signal {sig['type']}")
    if sig.get("overheat_z"):
        sd = r.rolling(int(sig.get("z_window", 30))).std().shift(1)
        z = r / sd
        hot = z.abs() > sig["overheat_z"] if sig["type"] == "reversal" else z > sig["overheat_z"]
        score = score.mask(hot)
    top = int(sel["top"])
    # rank 1 = best score; ties broken by column order, deterministic
    order = score.rank(axis=1, ascending=False, method="first")
    w = (order <= top).astype(float) / top
    w = w.where(score.notna(), 0.0)
    mf = sig.get("market_filter")
    if mf:
        base = store.close(mf["asset"]).reindex(closes.index) if store is not None else closes[mf["asset"]]
        on = (base > base.rolling(int(mf["window"])).mean()).astype(float)
        w = w.mul(on, axis=0)
    defined = score.notna().any(axis=1)
    return w.where(defined, np.nan)


def portfolio_returns(w: np.ndarray, r: np.ndarray, fee: float) -> np.ndarray:
    """w, r: (days, coins); w[t] decided at close t is held on day t+1."""
    pos = np.vstack([np.zeros((1, w.shape[1])), w[:-1]])
    turn = np.abs(np.diff(pos, axis=0, prepend=np.zeros((1, w.shape[1])))).sum(axis=1)
    return (pos * r).sum(axis=1) - turn * fee, turn


def shift_p(w: np.ndarray, r: np.ndarray, fee: float, rng: np.random.Generator, n: int) -> float:
    """Null: the choice of coins is unrelated to the days it was made for. Rotating the whole
    weight matrix in time keeps how many coins are held and how often they change."""
    L = len(w)
    if L < 3 * MIN_SHIFT:
        return 1.0
    actual = sharpe(portfolio_returns(w, r, fee)[0])
    ks = rng.integers(MIN_SHIFT, L - MIN_SHIFT, size=n)
    better = sum(sharpe(portfolio_returns(np.roll(w, k, axis=0), r, fee)[0]) >= actual for k in ks)
    return float((better + 1) / (n + 1))


def evaluate_period(w: pd.DataFrame, closes: pd.DataFrame, mask: np.ndarray, fee: float) -> dict:
    r = closes.pct_change(fill_method=None)
    # benchmark: equal weight in every coin that trades that day, rebalanced daily, no fees (generous)
    bench = r.mean(axis=1, skipna=True)
    m = np.asarray(mask) & w.shift(1).notna().any(axis=1).to_numpy() & bench.notna().to_numpy()
    W = w.fillna(0.0).to_numpy()
    R = r.fillna(0.0).to_numpy()
    strat, turn = portfolio_returns(W, R, fee)
    idx = closes.index
    n = int(m.sum())
    s, b = metrics(pd.Series(strat[m], index=idx[m])), metrics(bench[m])
    years = max(n / DAYS_PER_YEAR, 1e-9)
    held = np.vstack([np.zeros((1, W.shape[1])), W[:-1]])[m]
    return {
        "days": n, "start": str(idx[m][0].date()) if n else None, "end": str(idx[m][-1].date()) if n else None,
        "sharpe": s["sharpe"], "cagr": s["cagr"], "max_dd": s["max_dd"],
        "hold_sharpe": b["sharpe"], "hold_cagr": b["cagr"], "hold_max_dd": b["max_dd"],
        "exposure": float(held.sum(axis=1).mean()) if n else 0.0,
        "trades_per_year": float(turn[m].sum() / 2 / years),
        "_w": W[m], "_r": R[m], "_strat": strat[m], "_bench": bench[m].to_numpy(), "_idx": idx[m],
    }

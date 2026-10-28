"""Smart wallets (H-032): do the wallets whose deposits to an exchange came before the biggest price drops in a
selection period keep doing so later, more than wallets picked at random?

Input: datasets/<dataset> from crl.data.everscale — one row per transfer from a user's wallet into an exchange
deposit address (ts, wallet, deposit, value, first_sweep_ts). Prices: daily closes of `asset`.

1. Transfers below `min_value` are dust. A wallet with more than `max_monthly` transfers in any calendar month of
   the selection period is a service (another exchange, a bot) and is dropped everywhere.
2. A transfer counts only if its deposit address had already been swept into the hot wallet before it (so an
   observer at that moment could know the address belongs to the exchange). Transfers of one wallet less than
   `merge_days` after its previous counted transfer join that event.
3. Event outcome: log return from the close of the event's UTC day to the close `horizon_days` later.
4. Selection: wallets with at least `min_events` events in the selection window; their score is the mean outcome;
   "smart" = the lowest `smart_share` (prices fell most after their deposits). The window ends `horizon_days`
   before the test starts, so selection uses no later prices.
5. Test: the mean outcome of the smart wallets' events from `test.start` on, against `null.n` random sets of
   eligible wallets matched on the number of selection events (same bucket). One-sided p: the share of random sets
   whose mean is as low or lower.
6. Rule (reported, not the verdict): hold the coin, but stay out for `exit_days` after any smart-wallet event in
   the test period, decided at the close of the event's day; costs per side = fee + slippage.
"""
from pathlib import Path

import numpy as np
import pandas as pd

from crl.engine.backtest import evaluate_period
from crl.engine.stats import circular_shift_p

DAY = 86400


def load(spec: dict, root: Path | None = None) -> pd.DataFrame:
    from crl.config import DATASETS_DIR
    path = Path(root or DATASETS_DIR) / spec["dataset"]
    if not path.exists():
        raise FileNotFoundError(f"{path} missing — run `crl data everscale`")
    return pd.read_csv(path)


def services(df: pd.DataFrame, start, end, max_monthly: int) -> set:
    """Wallets with more than `max_monthly` transfers in a calendar month inside [start, end]."""
    d = pd.to_datetime(df["ts"], unit="s")
    m = (d >= pd.Timestamp(start)) & (d < pd.Timestamp(end) + pd.Timedelta(days=1))
    per = df[m].groupby([df.loc[m, "wallet"], d[m].dt.to_period("M")]).size()
    return set(per[per > max_monthly].index.get_level_values(0))


def merge_close(df: pd.DataFrame, days: int) -> pd.DataFrame:
    """Keep a wallet's transfer only if it comes at least `days` after its previous kept one."""
    df = df.sort_values(["wallet", "ts"])
    keep = np.zeros(len(df), dtype=bool)
    last_w, last_t = None, None
    for i, (w, ts) in enumerate(zip(df["wallet"].to_numpy(), df["ts"].to_numpy())):
        if w != last_w or ts - last_t >= days * DAY:
            keep[i] = True
            last_w, last_t = w, ts
    return df[keep]


def events(spec: dict, raw: pd.DataFrame, close: pd.Series) -> pd.DataFrame:
    f, sel = spec["filters"], spec["selection"]
    df = raw[raw["value"] >= float(f["min_value"])]
    svc = services(df, sel["start"], sel["end"], int(f["max_monthly"]))
    df = df[~df["wallet"].isin(svc)]
    if f.get("swept_before", True):
        df = df[df["first_sweep_ts"] < df["ts"]]
    df = merge_close(df, int(f["merge_days"])).copy()
    df["date"] = pd.to_datetime(df["ts"], unit="s").dt.normalize()
    h = int(sel["horizon_days"])
    c = close[close > 0]
    entry = c.reindex(df["date"]).to_numpy()
    exit_ = c.reindex(df["date"] + pd.Timedelta(days=h)).to_numpy()
    df["ret"] = np.log(exit_ / entry)
    return df[np.isfinite(df["ret"])]


def _bucket(n: np.ndarray, edges: list[int]) -> np.ndarray:
    return np.searchsorted(np.asarray(edges[1:]), n, side="right")


def evaluate(spec: dict, store, rng: np.random.Generator, root: Path | None = None) -> dict:
    sel, test, null = spec["selection"], spec["test"], spec["null"]
    alpha = float(spec["significance"]["alpha"])
    close = store.close(spec["asset"]).astype(float)
    ev = events(spec, load(spec, root), close)
    s0, s1, t0 = pd.Timestamp(sel["start"]), pd.Timestamp(sel["end"]), pd.Timestamp(test["start"])
    in_sel = ev[(ev["date"] >= s0) & (ev["date"] <= s1)]
    in_test = ev[ev["date"] >= t0]
    counts = in_sel.groupby("wallet")["ret"].agg(["count", "mean"])
    elig = counts[counts["count"] >= int(sel["min_events"])].reset_index()
    elig = elig.sort_values(["mean", "wallet"], kind="mergesort").reset_index(drop=True)   # lowest mean first
    n_smart = int(np.floor(float(sel["smart_share"]) * len(elig)))
    row_sel = {"symbol": spec["asset"], "period": "selection", "start": str(s0.date()), "end": str(s1.date()),
               "wallets": int(len(elig)), "smart": n_smart,
               "events": int(in_sel["wallet"].isin(elig["wallet"]).sum()),
               "all_mean": float(in_sel[in_sel["wallet"].isin(elig["wallet"])]["ret"].mean()) if len(elig) else None}
    if row_sel["all_mean"] is not None and not np.isfinite(row_sel["all_mean"]):
        row_sel["all_mean"] = None
    if len(elig) < int(sel["min_wallets"]):
        return {"verdict": "FAIL", "rows": [row_sel],
                "summary": f"insufficient data: {len(elig)} wallets with {sel['min_events']}+ events in the selection "
                           f"window, need {sel['min_wallets']}"}
    smart = set(elig["wallet"].iloc[:n_smart])
    row_sel["smart_mean"] = float(in_sel[in_sel["wallet"].isin(smart)]["ret"].mean())
    st = in_test[in_test["wallet"].isin(smart)]
    row_test = {"symbol": spec["asset"], "period": "test", "start": str(t0.date()),
                "end": str(in_test["date"].max().date()) if len(in_test) else None,
                "events": int(len(st)), "smart": int(st["wallet"].nunique())}
    if len(st) < int(test["min_events"]):
        return {"verdict": "FAIL", "rows": [row_sel, row_test],
                "summary": f"insufficient data: {len(st)} smart-wallet events from {t0.date()}, need {test['min_events']}"}
    smart_mean = float(st["ret"].mean())

    # null: random sets of eligible wallets, matched on the number of selection events
    tsum = in_test.groupby("wallet")["ret"].sum().reindex(elig["wallet"]).fillna(0.0).to_numpy()
    tcnt = in_test.groupby("wallet")["ret"].count().reindex(elig["wallet"]).fillna(0).to_numpy()
    bucket = _bucket(elig["count"].to_numpy(), list(null["buckets"]))
    by_bucket = {b: np.flatnonzero(bucket == b) for b in np.unique(bucket)}
    need = pd.Series(bucket[:n_smart]).value_counts().to_dict()
    means = []
    for _ in range(int(null["n"])):
        idx = np.concatenate([rng.choice(by_bucket[b], size=k, replace=k > len(by_bucket[b])) for b, k in need.items()])
        c = tcnt[idx].sum()
        if c > 0:
            means.append(tsum[idx].sum() / c)
    means = np.asarray(means)
    p = float((1 + np.sum(means <= smart_mean)) / (1 + len(means)))
    row_test.update(smart_mean=smart_mean, random_mean=float(means.mean()), p=p, win=p < alpha)

    # the rule: out of the coin for exit_days after a smart-wallet deposit (decided at that day's close)
    rule = spec["rule"]
    cost = float(rule["fee"]) + float(rule["slippage"])
    c = close[close > 0]
    decision = pd.Series(1.0, index=c.index)
    for d in st["date"].unique():
        decision.loc[pd.Timestamp(d):pd.Timestamp(d) + pd.Timedelta(days=int(rule["exit_days"]) - 1)] = 0.0
    mask = (c.index >= t0)
    e = evaluate_period(decision, c, np.asarray(mask), cost)
    rp = circular_shift_p(e["_pos"], e["_r"], cost, rng, 2000) if e["days"] else None
    row_rule = {"symbol": spec["asset"], "period": "rule", **{k: v for k, v in e.items() if not k.startswith("_")},
                "p": rp, "beats_hold": bool(e["days"] and e["sharpe"] > e["hold_sharpe"]), "win": False}

    verdict = "PASS" if p < alpha else ("WEAK" if smart_mean < means.mean() else "FAIL")
    summary = (f"{n_smart} smart wallets of {len(elig)}; from {t0.date()} their {len(st)} deposits were followed by a "
               f"mean {int(sel['horizon_days'])}-day log return of {smart_mean:+.4f} vs {means.mean():+.4f} for random "
               f"matched wallets (p = {p:.3f}, need p < {alpha}); exit rule Sharpe {e['sharpe']:.2f} vs hold "
               f"{e['hold_sharpe']:.2f}")
    rows = [{k: (round(v, 6) if isinstance(v, float) else v) for k, v in r.items()} for r in (row_sel, row_test, row_rule)]
    return {"verdict": verdict, "summary": summary, "rows": rows}

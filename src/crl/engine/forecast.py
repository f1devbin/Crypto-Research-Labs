"""Daily probabilistic forecasts (H-027 … H-030).

At the close of day D one pooled logistic regression gives, for every coin,

  direction  P(the return from close D to close D+1 is larger than the round-trip cost)
  risk       P(|log return D → D+1| is larger than the coin's median absolute daily move over the
             past 365 days, measured up to D)

Inputs: prices up to and including the close of D; external series (funding, Fear & Greed,
stablecoin supply, exchange flows) up to D−1, for their publication delay. Every input becomes a
rolling 365-day z-score of its own past, so coins with very different volatility share one model.
The model is refitted on the first day of every month on rows whose outcome was already known.

Scoring: Brier skill against the coin's base rate in the training window; a circular-shift null
that rotates forecasts against outcomes (one shift for all coins, so their correlation is kept);
for direction, a paper portfolio that holds a share of the coin equal to the forecast probability,
trading only when the share moves by at least `band`.

Live forecasts (`crl forecast`, H-029/H-030) reuse the same features and fitting. Each month's
model is stored once in datasets/forecast_models/ and never refitted; every forecast is appended
to datasets/forecast_log.csv and committed before 12:00 UTC, when the paper portfolio trades at
the open of the 12:00 hourly candle (datasets/noon_prices.csv).
"""
import datetime as dt
import json
from pathlib import Path

import numpy as np
import pandas as pd

from crl.engine.backtest import metrics

PRICE_FEATURES = ("r1", "r3", "r7", "r30", "d50", "d200", "v7", "v30")
MARKET_FEATURES = ("btc_r1", "btc_r7", "funding", "fear_greed", "stable30", "flow7")
EXTERNAL = {"funding": "funding_btc_7d", "fear_greed": "fear_greed", "stable30": "stablecoin_growth_30d",
            "flow7": "exnetflow_btc_7d"}
TARGETS = ("direction", "risk")
MIN_SHIFT = 30
MIN_TRAIN = 500        # rows needed before a model is fitted
MIN_COIN_BASE = 30     # rows a coin needs for its own base rate (otherwise the pooled one)
LOG_COLUMNS = ["published", "date", "decision_date", "symbol", "p_direction", "p_risk", "base_direction",
               "base_risk", "med_move", "w_target", "w_exec", "model", "on_time"]


def cost_of(spec: dict, sym: str) -> float:
    c = spec["costs"]
    return float(c.get(sym, c["default"]))


# ── features and targets ────────────────────────────────────────────

def _z(x: pd.Series, m: dict) -> pd.Series:
    w, mp = int(m["zscore_window"]), int(m["zscore_min_periods"])
    mu = x.rolling(w, min_periods=mp).mean()
    sd = x.rolling(w, min_periods=mp).std()
    return ((x - mu) / sd.where(sd > 0)).clip(-float(m["clip"]), float(m["clip"]))


def price_features(close: pd.Series) -> pd.DataFrame:
    """Raw price inputs at the close of each day; each uses closes up to that day only."""
    lc = np.log(close)
    r1 = lc.diff()
    f = pd.DataFrame({
        "r1": r1, "r3": lc.diff(3), "r7": lc.diff(7), "r30": lc.diff(30),
        "d50": lc - np.log(close.rolling(50).mean()),
        "d200": lc - np.log(close.rolling(200).mean()),
        "v7": np.log(r1.rolling(7).std()), "v30": np.log(r1.rolling(30).std()),
    })
    return f.replace([np.inf, -np.inf], np.nan)


def market_features(store, m: dict) -> pd.DataFrame:
    """Inputs shared by every coin. External series are lagged by `external_lag` days."""
    btc = np.log(store.close("BTCUSDT").astype(float))
    out = {"btc_r1": btc.diff(), "btc_r7": btc.diff(7)}
    lag, lim = int(m["external_lag"]), int(m["ffill_limit"])
    for name, key in EXTERNAL.items():
        s = store.feature(key).astype(float)
        s = s[~s.index.duplicated(keep="last")].sort_index()
        s = s.asfreq("D").ffill(limit=lim)
        out[name] = s.shift(lag, freq="D")
    return pd.DataFrame(out)


def panel(spec: dict, store) -> pd.DataFrame:
    """One row per (coin, day): z-scored inputs at the close of D, both targets for D → D+1, the
    next-day return and the coin's median absolute daily move (the risk threshold)."""
    m = spec["model"]
    feats = list(m["features"])
    mkz = market_features(store, m).apply(lambda s: _z(s, m))
    parts = []
    for sym in spec["universe"]:
        close = store.close(sym).astype(float)
        close = close[close > 0]
        if close.empty:
            continue
        z = price_features(close).apply(lambda s: _z(s, m)).join(mkz.reindex(close.index))
        nxt = close.shift(-1) / close - 1
        nlog = np.log(close.shift(-1) / close)
        med = np.log(close).diff().abs().rolling(365, min_periods=180).median()
        cost = cost_of(spec, sym)
        df = z[feats].copy()
        df["y_direction"] = (nxt > 2 * cost).astype(float).where(nxt.notna())
        df["y_risk"] = (nlog.abs() > med).astype(float).where(nlog.notna() & med.notna())
        df["ret_next"] = nxt
        df["med_move"] = med
        df["symbol"] = sym
        df.index.name = "date"
        parts.append(df.reset_index())
    if not parts:
        raise FileNotFoundError("no prices for the forecast universe")
    return pd.concat(parts, ignore_index=True)


# ── model ───────────────────────────────────────────────────────────

def fit_logit(X: np.ndarray, y: np.ndarray, l2: float, iters: int = 100) -> np.ndarray:
    """Logistic regression by Newton steps; L2 penalty on the slopes, not on the intercept."""
    n, k = X.shape
    Xb = np.hstack([np.ones((n, 1)), X])
    pen = np.full(k + 1, float(l2))
    pen[0] = 0.0
    w = np.zeros(k + 1)
    for _ in range(iters):
        p = 1.0 / (1.0 + np.exp(-np.clip(Xb @ w, -30, 30)))
        g = Xb.T @ (p - y) + pen * w
        H = (Xb * (p * (1 - p))[:, None]).T @ Xb + np.diag(pen) + 1e-9 * np.eye(k + 1)
        step = np.linalg.solve(H, g)
        w -= step
        if np.max(np.abs(step)) < 1e-10:
            break
    return w


def predict(w: np.ndarray, X: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip(w[0] + X @ np.asarray(w[1:]), -30, 30)))


def month_cutoff(month: pd.Period) -> pd.Timestamp:
    """Last decision date whose outcome is known when the month's model is fitted (its first day)."""
    return month.to_timestamp() - pd.Timedelta(days=2)


def fit_month(pnl: pd.DataFrame, feats: list[str], target: str, month: pd.Period, l2: float) -> dict | None:
    ycol = f"y_{target}"
    tr = pnl[pnl[feats].notna().all(axis=1) & pnl[ycol].notna() & (pnl["date"] <= month_cutoff(month))]
    if len(tr) < MIN_TRAIN:
        return None
    w = fit_logit(tr[feats].to_numpy(float), tr[ycol].to_numpy(float), l2)
    g = tr.groupby("symbol")[ycol]
    pooled = float(tr[ycol].mean())
    base = {s: float(v) for s, v in g.mean().items() if g.count()[s] >= MIN_COIN_BASE}
    return {"w": [float(x) for x in w], "base": base, "pooled": pooled, "n_train": int(len(tr)),
            "cutoff": str(month_cutoff(month).date())}


def walk_forward(spec: dict, pnl: pd.DataFrame, target: str, start, end=None) -> pd.DataFrame:
    """Out-of-sample forecasts: decisions in month M use the model fitted on the first day of M."""
    m = spec["model"]
    feats = list(m["features"])
    ok = pnl[feats].notna().all(axis=1) & (pnl["date"] >= pd.Timestamp(start))
    if end:
        ok &= pnl["date"] <= pd.Timestamp(end)
    oos = pnl[ok]
    out = []
    for month, chunk in oos.groupby(oos["date"].dt.to_period("M")):
        mod = fit_month(pnl, feats, target, month, float(m["l2"]))
        if mod is None:
            continue
        p = predict(np.asarray(mod["w"]), chunk[feats].to_numpy(float))
        b = chunk["symbol"].map(mod["base"]).fillna(mod["pooled"]).to_numpy(float)
        out.append(chunk.assign(p=p, b=b, model=str(month)))
    cols = list(pnl.columns) + ["p", "b", "model"]
    return pd.concat(out, ignore_index=True) if out else pd.DataFrame(columns=cols)


# ── scoring ─────────────────────────────────────────────────────────

def brier(p, y, b) -> tuple[float, float, float]:
    """(Brier skill, Brier of the forecast, Brier of the base rate)."""
    p, y, b = (np.asarray(a, float) for a in (p, y, b))
    bm, br = float(np.mean((p - y) ** 2)), float(np.mean((b - y) ** 2))
    return (1 - bm / br if br > 0 else 0.0), bm, br


def shift_p(groups: list[tuple[np.ndarray, np.ndarray, np.ndarray]], rng: np.random.Generator,
            n: int = 2000) -> float:
    """Null: the forecasts are unrelated to the days they were made for. Rotating each coin's
    forecast series by the same number of days keeps their distribution and autocorrelation
    but breaks the link to outcomes. One-sided p of the pooled Brier skill."""
    groups = [(np.asarray(p, float), np.asarray(y, float), np.asarray(b, float)) for p, y, b in groups if len(p)]
    if not groups:
        return 1.0
    L = min(len(g[0]) for g in groups)
    if L < 3 * MIN_SHIFT:
        return 1.0
    den = sum(float(np.sum((b - y) ** 2)) for _, y, b in groups)
    if den <= 0:
        return 1.0
    actual = 1 - sum(float(np.sum((p - y) ** 2)) for p, y, _ in groups) / den
    ks = rng.integers(MIN_SHIFT, L - MIN_SHIFT, size=n)
    better = 0
    for k in ks:
        num = sum(float(np.sum((np.roll(p, k) - y) ** 2)) for p, y, _ in groups)
        better += (1 - num / den) >= actual
    return float((better + 1) / (n + 1))


def bh_q(ps: list[float]) -> list[float]:
    """Benjamini–Hochberg adjusted p-values (q-values)."""
    ps = np.asarray(ps, float)
    if not len(ps):
        return []
    order = np.argsort(ps)
    ranked = ps[order] * len(ps) / (np.arange(len(ps)) + 1)
    q = np.minimum.accumulate(ranked[::-1])[::-1].clip(max=1.0)
    out = np.empty(len(ps))
    out[order] = q
    return [float(x) for x in out]


def paper(p: np.ndarray, r_next: np.ndarray, cost: float, band: float) -> tuple[np.ndarray, np.ndarray]:
    """Share of the coin held after each decision and the portfolio return over the next day.
    The share follows the forecast probability but trades only when it moves by at least `band`;
    a missing forecast (NaN) keeps the current share. Costs are charged on every change."""
    w, rets, cur = np.full(len(p), np.nan), np.zeros(len(p)), None
    for i, pi in enumerate(p):
        new = cur
        if not np.isnan(pi):
            tgt = min(max(float(pi), 0.0), 1.0)
            if cur is None or abs(tgt - cur) >= band:
                new = tgt
        held = 0.0 if new is None else new
        rets[i] = held * r_next[i] - abs(held - (0.0 if cur is None else cur)) * cost
        w[i], cur = (np.nan if new is None else new), new
    return w, rets


def _monthly(days: pd.Series, port: np.ndarray, hold: np.ndarray, w: np.ndarray, r: np.ndarray) -> list[dict]:
    """$100 at the start of each month: the model's paper portfolio, holding, and a constant share
    equal to the model's average share that month (no costs for the constant share)."""
    df = pd.DataFrame({"m": (days + pd.Timedelta(days=1)).dt.to_period("M").astype(str).to_numpy(),
                       "port": port, "hold": hold, "w": w, "r": r})
    out = []
    for m, g in df.groupby("m", sort=True):
        wbar = float(np.nanmean(g["w"])) if g["w"].notna().any() else 0.0
        out.append({"month": m, "days": int(len(g)),
                    "model": round(100 * float(np.prod(1 + g["port"])), 2),
                    "hold": round(100 * float(np.prod(1 + g["hold"])), 2),
                    "const": round(100 * float(np.prod(1 + wbar * g["r"])), 2),
                    "share": round(wbar, 4)})
    return out


def calibration(p: np.ndarray, y: np.ndarray, bins: int = 10) -> list[dict]:
    p, y = np.asarray(p, float), np.asarray(y, float)
    idx = np.clip((p * bins).astype(int), 0, bins - 1)
    return [{"lo": i / bins, "hi": (i + 1) / bins, "n": int((idx == i).sum()),
             "p": round(float(p[idx == i].mean()), 4), "y": round(float(y[idx == i].mean()), 4)}
            for i in range(bins) if (idx == i).any()]


def score(spec: dict, fc: pd.DataFrame, target: str, rng: np.random.Generator, period: str) -> dict:
    """Rows per coin and pooled, monthly $100 table and calibration for scored forecasts.
    `fc` needs date, symbol, p, b, y_<target>, ret_next (consecutive days per coin; p may be NaN)."""
    sig = spec["significance"]
    n_null, alpha = int(sig.get("n", 2000)), float(sig["alpha"])
    band = float((spec.get("portfolio") or {}).get("band", 0.10))
    ycol = f"y_{target}"
    rows, groups, monthly = [], [], []
    for sym in spec["universe"]:
        g = fc[fc["symbol"] == sym].sort_values("date")
        g = g[g["ret_next"].notna()]
        if g.empty or g["p"].notna().sum() == 0:
            continue
        g = g.iloc[int(np.argmax(g["p"].notna().to_numpy())):]   # from the first forecast on
        s = g[g["p"].notna() & g[ycol].notna()]
        if s.empty:
            continue
        bss, bm, br = brier(s["p"], s[ycol], s["b"])
        groups.append((s["p"].to_numpy(), s[ycol].to_numpy(), s["b"].to_numpy()))
        row = {"symbol": sym, "period": period, "days": int(len(s)),
               "start": str(s["date"].iloc[0].date()), "end": str(s["date"].iloc[-1].date()),
               "bss": bss, "brier": bm, "brier_ref": br, "hits": float(((s["p"] > 0.5) == (s[ycol] > 0.5)).mean()),
               "p": shift_p([groups[-1]], rng, n_null)}
        if target == "direction" and spec.get("portfolio"):
            cost = cost_of(spec, sym)
            r = g["ret_next"].to_numpy(float)
            w, port = paper(g["p"].to_numpy(float), r, cost, band)
            hold = r.copy()
            hold[0] -= cost
            wbar = float(np.nanmean(w))
            const = wbar * r
            ms, mh, mc = metrics(pd.Series(port)), metrics(pd.Series(hold)), metrics(pd.Series(const))
            years = max(len(r) / 365, 1e-9)
            row.update(sharpe=ms["sharpe"], cagr=ms["cagr"], max_dd=ms["max_dd"],
                       hold_sharpe=mh["sharpe"], hold_cagr=mh["cagr"], hold_max_dd=mh["max_dd"],
                       const_sharpe=mc["sharpe"], const_cagr=mc["cagr"], exposure=wbar,
                       trades_per_year=float(np.sum(np.abs(np.diff(np.nan_to_num(w), prepend=0.0))) / 2 / years),
                       beats_hold=ms["sharpe"] > mh["sharpe"], beats_const=ms["sharpe"] > mc["sharpe"])
            for x in _monthly(g["date"].reset_index(drop=True), port, hold, w, r):
                monthly.append({"symbol": sym, **x})
        rows.append(row)
    if not rows:
        return {"verdict": "FAIL", "summary": "no forecasts could be made", "rows": []}
    for row, q in zip(rows, bh_q([r["p"] for r in rows])):
        row["q"] = q
    allp = np.concatenate([g[0] for g in groups])
    ally = np.concatenate([g[1] for g in groups])
    allb = np.concatenate([g[2] for g in groups])
    bss, bm, br = brier(allp, ally, allb)
    p = shift_p(groups, rng, n_null)
    pooled = {"symbol": "ALL", "period": period, "days": int(len(allp)),
              "start": min(r["start"] for r in rows), "end": max(r["end"] for r in rows),
              "bss": bss, "brier": bm, "brier_ref": br, "hits": float(((allp > 0.5) == (ally > 0.5)).mean()), "p": p}
    for row in rows:
        row["win"] = row["bss"] > 0 and row["q"] < 0.10
    pooled["win"] = bss > 0 and p < alpha
    verdict = "PASS" if pooled["win"] else ("WEAK" if bss > 0 else "FAIL")
    pos = sum(r["bss"] > 0 for r in rows)
    summary = (f"pooled Brier skill {bss:+.4f} (p = {p:.3f}, need p < {alpha}); skill above zero on "
               f"{pos}/{len(rows)} coins")
    if target == "direction" and spec.get("portfolio"):
        bh = sum(r["beats_hold"] for r in rows)
        bc = sum(r["beats_const"] for r in rows)
        summary += f"; paper portfolio beats holding on {bh}/{len(rows)} and the constant share on {bc}/{len(rows)}"
    return {"verdict": verdict, "summary": summary, "rows": rows + [pooled],
            "monthly": monthly, "calibration": calibration(allp, ally)}


def evaluate(spec: dict, store, rng: np.random.Generator) -> dict:
    """H-027 / H-028: walk-forward out-of-sample forecasts on history."""
    pnl = panel(spec, store)
    per = spec["periods"][0]
    fc = walk_forward(spec, pnl, spec["target"], per.get("start"), per.get("end"))
    if fc.empty:
        return {"verdict": "FAIL", "summary": "not enough history to fit the model", "rows": []}
    # keep every day with a known next return so the paper portfolio carries its share over gaps
    base = pnl[(pnl["date"] >= fc["date"].min()) & pnl["ret_next"].notna()]
    base = base[["date", "symbol", "ret_next", f"y_{spec['target']}"]]
    fc = base.merge(fc[["date", "symbol", "p", "b"]], on=["date", "symbol"], how="left")
    return score(spec, fc, spec["target"], rng, per["name"])


# ── live forecasts ──────────────────────────────────────────────────

def read_log(root: Path) -> pd.DataFrame:
    p = Path(root) / "forecast_log.csv"
    if not p.exists():
        return pd.DataFrame(columns=LOG_COLUMNS)
    df = pd.read_csv(p, parse_dates=["date", "decision_date"])
    return df


def read_noon(root: Path) -> pd.DataFrame:
    p = Path(root) / "noon_prices.csv"
    if not p.exists():
        return pd.DataFrame(columns=["date", "symbol", "price"])
    return pd.read_csv(p, parse_dates=["date"])


def live_frame(spec: dict, log: pd.DataFrame, noon: pd.DataFrame) -> pd.DataFrame:
    """Scored live forecasts: on-time rows from the period start, with the noon-to-noon return.
    Days without an on-time forecast stay in the frame with p = NaN (the share is carried)."""
    target = spec["target"]
    start = pd.Timestamp(spec["periods"][0]["start"])
    px = noon.pivot_table(index="date", columns="symbol", values="price").sort_index()
    out = []
    for sym in spec["universe"]:
        if sym not in px:
            continue
        s = px[sym].dropna()
        s = s[s.index >= start]
        if len(s) < 2:
            continue
        nxt = s.shift(-1, freq="D").reindex(s.index)
        ret = (nxt / s - 1)
        lg = log[(log["symbol"] == sym) & (log["on_time"] == 1)].set_index("date")
        lg = lg[~lg.index.duplicated(keep="first")]
        df = pd.DataFrame({"date": s.index, "symbol": sym, "ret_next": ret.to_numpy()})
        df["p"] = lg[f"p_{target}"].reindex(s.index).to_numpy()
        df["b"] = lg[f"base_{target}"].reindex(s.index).to_numpy()
        cost = cost_of(spec, sym)
        if target == "direction":
            df["y_direction"] = (df["ret_next"] > 2 * cost).astype(float).where(df["ret_next"].notna())
        else:
            med = lg["med_move"].reindex(s.index).to_numpy()
            mv = np.abs(np.log1p(df["ret_next"].to_numpy(float)))
            df["y_risk"] = np.where(np.isnan(mv) | np.isnan(med), np.nan, (mv > med).astype(float))
        out.append(df)
    return pd.concat(out, ignore_index=True) if out else pd.DataFrame()


def evaluate_live(spec: dict, store, rng: np.random.Generator, root: Path | None = None) -> dict:
    """H-029 / H-030: the same scoring on forecasts published before 12:00 UTC, noon to noon."""
    from crl.config import DATASETS_DIR
    root = root or DATASETS_DIR
    fc = live_frame(spec, read_log(root), read_noon(root))
    if fc.empty:
        raise FileNotFoundError("no live forecasts or noon prices yet")
    return score(spec, fc, spec["target"], rng, spec["periods"][0]["name"])


def _load_live_specs() -> tuple[dict, dict]:
    from crl import registry
    specs = {h["spec"]["target"]: h["spec"] for h in registry.load_all()
             if (h.get("spec") or {}).get("kind") == "forecast_live" and h.get("status") != "draft"}
    if set(specs) != set(TARGETS):
        raise KeyError("registered forecast_live hypotheses for both targets are required")
    d, r = specs["direction"], specs["risk"]
    if d["model"] != r["model"] or d["universe"] != r["universe"]:
        raise ValueError("live direction and risk specs must share the model and the universe")
    return d, r


def publish(store=None, now: dt.datetime | None = None, root: Path | None = None,
            specs: tuple[dict, dict] | None = None, fetch_noon: bool = True) -> dict:
    """Append today's forecasts to the log (once per UTC day: the first publication is final)."""
    from crl.config import DATASETS_DIR
    from crl.data.store import DataStore
    root = Path(root or DATASETS_DIR)
    now = now or dt.datetime.now(dt.timezone.utc)
    store = store or DataStore()
    spec_d, _ = specs or _load_live_specs()
    today = pd.Timestamp(now.date())
    log = read_log(root)
    if len(log) and (log["date"] == today).any():
        return {"status": "already published", "date": str(today.date())}
    decision = today - pd.Timedelta(days=1)
    m = spec_d["model"]
    feats = list(m["features"])
    pnl = panel(spec_d, store)
    month = decision.to_period("M")
    models = root / "forecast_models"
    path = models / f"{month}.json"
    if path.exists():
        mod = json.loads(path.read_text())
    else:
        mod = {t: fit_month(pnl, feats, t, month, float(m["l2"])) for t in TARGETS}
        if any(v is None for v in mod.values()):
            return {"status": "not enough history to fit the model"}
        mod.update(month=str(month), features=feats, fitted_at=now.strftime("%Y-%m-%dT%H:%M:%SZ"))
        models.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(mod, indent=1))
    rows = pnl[(pnl["date"] == decision) & pnl[feats].notna().all(axis=1)]
    if rows.empty:
        return {"status": f"no inputs for {decision.date()} yet"}
    on_time = int(now < dt.datetime.combine(now.date(), dt.time(12, 0), tzinfo=dt.timezone.utc))
    band = float(spec_d["portfolio"]["band"])
    X = rows[feats].to_numpy(float)
    p_dir = predict(np.asarray(mod["direction"]["w"]), X)
    p_risk = predict(np.asarray(mod["risk"]["w"]), X)
    stamp = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    new = []
    for (_, r), pd_, pr_ in zip(rows.iterrows(), p_dir, p_risk):
        sym = r["symbol"]
        prev = log[(log["symbol"] == sym) & (log["on_time"] == 1)]["w_exec"].dropna()
        w_prev = float(prev.iloc[-1]) if len(prev) else None
        tgt = min(max(float(pd_), 0.0), 1.0)
        if on_time and (w_prev is None or abs(tgt - w_prev) >= band):
            w_exec = tgt
        else:
            w_exec = w_prev
        new.append({"published": stamp, "date": today.date(), "decision_date": decision.date(), "symbol": sym,
                    "p_direction": round(float(pd_), 6), "p_risk": round(float(pr_), 6),
                    "base_direction": round(mod["direction"]["base"].get(sym, mod["direction"]["pooled"]), 6),
                    "base_risk": round(mod["risk"]["base"].get(sym, mod["risk"]["pooled"]), 6),
                    "med_move": round(float(r["med_move"]), 6) if pd.notna(r["med_move"]) else None,
                    "w_target": round(tgt, 6), "w_exec": None if w_exec is None else round(w_exec, 6),
                    "model": str(month), "on_time": on_time})
    out = pd.concat([log, pd.DataFrame(new)], ignore_index=True)[LOG_COLUMNS]
    out["date"] = pd.to_datetime(out["date"]).dt.date
    out["decision_date"] = pd.to_datetime(out["decision_date"]).dt.date
    root.mkdir(parents=True, exist_ok=True)
    out.to_csv(root / "forecast_log.csv", index=False)
    if fetch_noon:
        update_noon(root, spec_d["universe"], pd.Timestamp(spec_d["periods"][0]["start"]), today)
    return {"status": "published", "date": str(today.date()), "coins": len(new), "on_time": bool(on_time)}


def _noon_binance(sym: str, day: dt.date) -> float | None:
    import io
    import zipfile

    from crl.data.http import get
    from crl.data.sources import VISION
    res = get(f"{VISION}/spot/daily/klines/{sym}/1h/{sym}-1h-{day}.zip")
    if not res.ok:
        return None
    try:
        with zipfile.ZipFile(io.BytesIO(res.body)) as z, z.open(z.namelist()[0]) as fh:
            df = pd.read_csv(fh, header=None, usecols=[0, 1])
    except (zipfile.BadZipFile, ValueError, IndexError):
        return None
    df = df.apply(pd.to_numeric, errors="coerce").dropna()
    t = df[0].astype("int64")
    t = np.where(t > 10**14, t // 1000, t)
    noon = int(dt.datetime.combine(day, dt.time(12, 0), tzinfo=dt.timezone.utc).timestamp() * 1000)
    hit = df[1][t == noon]
    return float(hit.iloc[0]) if len(hit) else None


def _noon_gate(pair: str, days: list[dt.date]) -> dict:
    from crl.data.http import get
    from crl.data.sources import GATE
    if not days:
        return {}
    f = int(dt.datetime.combine(days[0], dt.time(12, 0), tzinfo=dt.timezone.utc).timestamp())
    t = int(dt.datetime.combine(days[-1], dt.time(12, 0), tzinfo=dt.timezone.utc).timestamp())
    res = get(f"{GATE}?currency_pair={pair}&interval=1h&from={f}&to={t}")
    try:
        data = json.loads(res.body) if res.ok else []
    except ValueError:
        data = []
    out = {}
    for r in data if isinstance(data, list) else []:
        ts = dt.datetime.fromtimestamp(int(r[0]), dt.timezone.utc)
        if ts.hour == 12 and ts.minute == 0:
            out[ts.date()] = float(r[5])   # Gate rows: [t, quote_vol, close, high, low, open, ...]
    return out


def update_noon(root: Path, universe: list[str], start: pd.Timestamp, today: pd.Timestamp) -> None:
    """Open of the 12:00 UTC hourly candle for every coin and day from `start` to yesterday."""
    from crl.data.sources import OTHER_EXCHANGES
    noon = read_noon(root)
    have = {(str(d.date()), s) for d, s in zip(noon["date"], noon["symbol"])}
    first = max(start, today - pd.Timedelta(days=40)).date()
    days = [d.date() for d in pd.date_range(first, today - pd.Timedelta(days=1))]
    add = []
    for sym in universe:
        todo = [d for d in days if (str(d), sym) not in have]
        if not todo:
            continue
        if sym in OTHER_EXCHANGES:
            got = _noon_gate(OTHER_EXCHANGES[sym][1], todo)
        else:
            got = {d: v for d in todo if (v := _noon_binance(sym, d)) is not None}
        add += [{"date": d, "symbol": sym, "price": v} for d, v in got.items()]
    if add:
        noon = pd.concat([noon, pd.DataFrame(add)], ignore_index=True)
        noon["date"] = pd.to_datetime(noon["date"]).dt.date
        noon = noon.drop_duplicates(["date", "symbol"], keep="first").sort_values(["date", "symbol"])
        noon.to_csv(Path(root) / "noon_prices.csv", index=False)

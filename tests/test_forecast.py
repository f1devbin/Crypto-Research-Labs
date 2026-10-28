import datetime as dt
import json

import numpy as np
import pandas as pd
import pytest

from crl.data.store import MemoryStore
from crl.engine import forecast as F
from tests.conftest import random_walk

SYMS = ["BTCUSDT", "ETHUSDT", "EVERUSDT"]
MODEL = {"type": "pooled_logit", "features": list(F.PRICE_FEATURES) + list(F.MARKET_FEATURES),
         "zscore_window": 365, "zscore_min_periods": 180, "clip": 5, "l2": 1.0, "refit": "monthly",
         "external_lag": 1, "ffill_limit": 3}


def spec(target="direction", kind="forecast", start="2021-06-01"):
    s = {"kind": kind, "target": target, "model": MODEL, "universe": SYMS,
         "costs": {"default": 0.001, "EVERUSDT": 0.004}, "periods": [{"name": "oos", "start": start}],
         "significance": {"method": "circular_shift", "n": 50, "alpha": 0.025}}
    if target == "direction":
        s["portfolio"] = {"weight": "probability", "band": 0.10}
    return s


def make_store(seed=0, n=1600, start="2019-01-01"):
    closes = {s: random_walk(n=n, seed=i + seed, start=start) for i, s in enumerate(SYMS)}
    idx = pd.date_range(start, periods=n, freq="D")
    rng = np.random.default_rng(seed + 10)
    feats = {"funding_btc_7d": pd.Series(rng.normal(1e-4, 1e-4, n), idx),
             "fear_greed": pd.Series(rng.uniform(10, 90, n), idx),
             "stablecoin_growth_30d": pd.Series(rng.normal(0.01, 0.02, n), idx),
             "exnetflow_btc_7d": pd.Series(rng.normal(0, 1000, n), idx)}
    return MemoryStore(closes, feats)


@pytest.mark.parametrize("target", F.TARGETS)
def test_changing_the_future_does_not_change_past_forecasts(target):
    s = spec(target)
    cut = pd.Timestamp("2022-03-15")
    a = F.walk_forward(s, F.panel(s, make_store()), target, s["periods"][0]["start"])
    st = make_store()
    rng = np.random.default_rng(7)
    for c in st._closes.values():                       # rewrite every price after the cut-off …
        m = c.index > cut
        c[m] = c[m] * rng.uniform(0.5, 2.0, m.sum())
    for f in st._features.values():                     # … and every external value
        m = f.index > cut
        f[m] = rng.permutation(f[m].to_numpy()) * 3
    b = F.walk_forward(s, F.panel(s, st), target, s["periods"][0]["start"])
    key = ["date", "symbol"]
    past_a = a[a["date"] <= cut].set_index(key)["p"]
    past_b = b[b["date"] <= cut].set_index(key)["p"].reindex(past_a.index)
    assert len(past_a) > 300
    np.testing.assert_allclose(past_a.to_numpy(), past_b.to_numpy(), rtol=0, atol=1e-12)
    later_a = a[a["date"] > cut + pd.Timedelta(days=40)].set_index(key)["p"]
    later_b = b[b["date"] > cut + pd.Timedelta(days=40)].set_index(key)["p"].reindex(later_a.index)
    assert not np.allclose(later_a.to_numpy(), later_b.to_numpy())  # the test does see changed data


def test_model_of_a_month_uses_only_outcomes_known_on_its_first_day():
    s = spec()
    pnl = F.panel(s, make_store())
    month = pd.Period("2022-02", "M")
    cutoff = F.month_cutoff(month)
    assert cutoff == pd.Timestamp("2022-01-30")
    # the outcome of the decision on Jan 30 is the close of Jan 31, known when February starts
    mod = F.fit_month(pnl, MODEL["features"], "direction", month, 1.0)
    assert mod["cutoff"] == "2022-01-30"
    tr = pnl[pnl[MODEL["features"]].notna().all(axis=1) & pnl["y_direction"].notna() & (pnl["date"] <= cutoff)]
    assert mod["n_train"] == len(tr)


def test_brier_skill_and_null():
    rng = np.random.default_rng(0)
    y = (rng.random(600) < 0.5).astype(float)
    b = np.full(600, 0.5)
    assert F.brier(y, y, b)[0] == pytest.approx(1.0)
    assert F.brier(b, y, b)[0] == pytest.approx(0.0)
    good = np.clip(0.5 + 0.3 * (2 * y - 1) + rng.normal(0, 0.05, 600), 0, 1)
    assert F.shift_p([(good, y, b)], rng, 200) < 0.02
    noise = rng.random(600)
    assert F.shift_p([(noise, y, b)], rng, 200) > 0.2


def test_paper_portfolio_trades_only_on_big_moves_and_pays_costs():
    p = np.array([0.6, 0.65, 0.75, np.nan, 0.2])
    r = np.array([0.01, -0.02, 0.03, 0.01, -0.01])
    w, ret = F.paper(p, r, cost=0.001, band=0.10)
    np.testing.assert_allclose(w, [0.6, 0.6, 0.75, 0.75, 0.2])
    expected = [0.6 * 0.01 - 0.6 * 0.001, 0.6 * -0.02, 0.75 * 0.03 - 0.15 * 0.001, 0.75 * 0.01,
                0.2 * -0.01 - 0.55 * 0.001]
    np.testing.assert_allclose(ret, expected)


def test_history_evaluation_reports_every_coin_and_the_pool():
    s = spec()
    res = F.evaluate(s, make_store(), np.random.default_rng(1))
    syms = [r["symbol"] for r in res["rows"]]
    assert syms == SYMS + ["ALL"] and res["verdict"] in ("PASS", "WEAK", "FAIL")
    ever = next(r for r in res["rows"] if r["symbol"] == "EVERUSDT")
    assert {"bss", "p", "q", "sharpe", "hold_sharpe", "const_sharpe", "exposure"} <= set(ever)
    assert res["monthly"] and {"model", "hold", "const"} <= set(res["monthly"][0])
    assert sum(b["n"] for b in res["calibration"]) == next(r for r in res["rows"] if r["symbol"] == "ALL")["days"]
    risk = F.evaluate(spec("risk"), make_store(), np.random.default_rng(1))
    assert "sharpe" not in risk["rows"][0] and risk["rows"][-1]["symbol"] == "ALL"


def live_specs():
    d = spec("direction", "forecast_live", "2023-01-01")
    r = spec("risk", "forecast_live", "2023-01-01")
    for x in (d, r):
        x["execution"] = {"time_utc": "12:00"}
    return d, r


def test_publish_once_per_day_with_a_frozen_monthly_model(tmp_path):
    st = make_store(n=1700)
    utc = dt.timezone.utc
    first = F.publish(st, dt.datetime(2023, 6, 1, 8, 0, tzinfo=utc), tmp_path, live_specs(), fetch_noon=False)
    assert first["status"] == "published" and first["on_time"] and first["coins"] == len(SYMS)
    model_file = tmp_path / "forecast_models" / "2023-05.json"   # decision on May 31 → May's model
    frozen = model_file.read_text()
    again = F.publish(st, dt.datetime(2023, 6, 1, 9, 0, tzinfo=utc), tmp_path, live_specs(), fetch_noon=False)
    assert again["status"] == "already published"
    late = F.publish(st, dt.datetime(2023, 6, 2, 13, 0, tzinfo=utc), tmp_path, live_specs(), fetch_noon=False)
    assert late["status"] == "published" and not late["on_time"]
    log = F.read_log(tmp_path)
    assert len(log) == 2 * len(SYMS)
    d1, d2 = log[log["date"] == "2023-06-01"], log[log["date"] == "2023-06-02"]
    assert (d1["on_time"] == 1).all() and (d2["on_time"] == 0).all()
    # a late forecast never trades: the paper share stays where the last on-time one put it
    np.testing.assert_allclose(d2["w_exec"].to_numpy(), d1["w_exec"].to_numpy())
    assert model_file.read_text() == frozen and json.loads(frozen)["direction"]["cutoff"] == "2023-04-29"
    assert set(log["model"]) == {"2023-05", "2023-06"}
    assert (tmp_path / "forecast_models" / "2023-06.json").exists()


def test_live_scoring_runs_noon_to_noon(tmp_path):
    days = pd.date_range("2024-01-01", periods=200, freq="D")
    rng = np.random.default_rng(3)
    noon = pd.DataFrame([{"date": d.date(), "symbol": s, "price": v}
                         for s in SYMS for d, v in zip(days, random_walk(n=200, seed=hash(s) % 100))])
    noon.to_csv(tmp_path / "noon_prices.csv", index=False)
    px = noon.pivot_table(index="date", columns="symbol", values="price")
    rows = []
    for s in SYMS:
        nxt = px[s].shift(-1) / px[s] - 1
        for d in days[:-1]:
            up = float(nxt.loc[d.date()] > 0.002)
            rows.append({"published": f"{d.date()}T06:00:00Z", "date": d.date(), "decision_date": (d - pd.Timedelta(days=1)).date(),
                         "symbol": s, "p_direction": 0.9 if up else 0.1, "p_risk": 0.5, "base_direction": 0.5,
                         "base_risk": 0.5, "med_move": 0.02, "w_target": 0.5, "w_exec": 0.5, "model": "2023-12",
                         "on_time": 1})
    pd.DataFrame(rows, columns=F.LOG_COLUMNS).to_csv(tmp_path / "forecast_log.csv", index=False)
    d, _ = live_specs()
    d["periods"] = [{"name": "forward", "start": "2024-01-01"}]
    res = F.evaluate_live(d, None, rng, tmp_path)
    pooled = res["rows"][-1]
    assert pooled["symbol"] == "ALL" and pooled["bss"] > 0.5 and res["verdict"] == "PASS"

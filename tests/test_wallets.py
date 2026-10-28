import numpy as np
import pandas as pd

from crl.data.store import MemoryStore
from crl.engine import wallets as W
from tests.conftest import random_walk

SPEC = {"kind": "wallet_deposits", "asset": "EVERUSDT", "universe": ["EVERUSDT"], "dataset": "deposits.csv",
        "filters": {"min_value": 10, "swept_before": True, "merge_days": 7, "max_monthly": 100},
        "selection": {"start": "2022-01-01", "end": "2023-12-24", "min_events": 5, "horizon_days": 7,
                      "smart_share": 0.2, "min_wallets": 25},
        "test": {"start": "2024-01-01", "min_events": 30},
        "null": {"method": "random_wallets_matched", "n": 300, "buckets": [5, 6, 8, 11, 16, 26]},
        "significance": {"alpha": 0.05}, "rule": {"exit_days": 7, "fee": 0.002, "slippage": 0.002}}


def price(seed=3):
    return random_walk(n=1900, seed=seed, start="2021-06-01", vol=0.05)


def ts(day, hour=10):
    return int((pd.Timestamp(day) + pd.Timedelta(hours=hour)).timestamp())


def dataset(close, informed=20, n=120, seed=0):
    """`informed` wallets deposit just before the 7-day drops (in both periods); the rest deposit at random."""
    rng = np.random.default_rng(seed)
    fwd = np.log(close.shift(-7) / close)
    rows = []
    for period in (("2022-01-01", "2023-12-20"), ("2024-01-01", "2026-06-01")):
        days = close.index[(close.index >= period[0]) & (close.index <= period[1])]
        worst = fwd.reindex(days).sort_values().index[:300]
        for w in range(n):
            pool = worst if w < informed else days
            for d in rng.choice(pool, size=8, replace=False):
                rows.append({"ts": ts(d), "wallet": f"w{w:03d}", "deposit": f"d{w:03d}", "value": 500.0,
                             "first_sweep_ts": ts("2021-06-02")})
    return pd.DataFrame(rows)


def run(tmp_path, df, close, seed=1):
    df.to_csv(tmp_path / "deposits.csv", index=False)
    return W.evaluate(SPEC, MemoryStore({"EVERUSDT": close}), np.random.default_rng(seed), tmp_path)


def test_wallets_that_deposit_before_drops_are_found_and_confirmed(tmp_path):
    close = price()
    res = run(tmp_path, dataset(close), close)
    sel, test, rule = res["rows"]
    assert sel["wallets"] == 120 and sel["smart"] == 24
    assert test["smart_mean"] < test["random_mean"] and test["p"] < 0.01 and res["verdict"] == "PASS"
    assert rule["period"] == "rule" and 0 < rule["exposure"] < 1


def test_without_informed_wallets_the_null_holds(tmp_path):
    """No wallet knows anything: p should be roughly uniform, so a pass is rare (about alpha)."""
    ps = []
    for seed in range(20):
        close = price(seed=100 + seed)
        ps.append(run(tmp_path, dataset(close, informed=0, seed=seed), close, seed=seed)["rows"][1]["p"])
    assert np.mean(np.array(ps) < 0.05) <= 0.15 and np.median(ps) > 0.25


def test_selection_never_sees_later_prices(tmp_path):
    close = price()
    df = dataset(close)
    a = run(tmp_path, df, close)["rows"][0]
    later = close.copy()
    m = later.index >= pd.Timestamp("2024-01-01")
    later[m] = later[m] * np.random.default_rng(9).uniform(0.3, 3, m.sum())
    b = run(tmp_path, df, later)["rows"][0]
    assert a == b


def test_filters_dust_sweeps_merging_and_services():
    close = price()
    base = {"wallet": "w", "deposit": "d", "value": 100.0, "first_sweep_ts": ts("2021-12-01")}
    raw = pd.DataFrame([
        {**base, "ts": ts("2022-03-01")},
        {**base, "ts": ts("2022-03-05")},                      # 4 days later: same event
        {**base, "ts": ts("2022-03-09")},                      # 8 days after the kept one: new event
        {**base, "ts": ts("2022-04-01"), "value": 5.0},        # dust
        {**base, "ts": ts("2022-05-01"), "first_sweep_ts": ts("2022-06-01")},   # address not swept yet
    ])
    svc = pd.DataFrame([{**base, "wallet": "bot", "ts": ts("2022-07-01") + i * 60} for i in range(101)])
    ev = W.events(SPEC, pd.concat([raw, svc]), close)
    assert list(ev["date"].dt.strftime("%m-%d")) == ["03-01", "03-09"] and set(ev["wallet"]) == {"w"}


def test_too_few_wallets_is_reported_as_insufficient(tmp_path):
    close = price()
    res = run(tmp_path, dataset(close, n=10, informed=2), close)
    assert res["verdict"] == "FAIL" and res["summary"].startswith("insufficient data")

import numpy as np
import pandas as pd

from crl.data.store import MemoryStore
from crl.engine import rules as R
from crl.engine.stats import permutation_p
from tests.conftest import random_walk
from tests.test_registry import SPEC, make
from crl import registry


def test_day_of_week_sets_position_for_tomorrow():
    c = random_walk(14, start="2024-01-01")  # 2024-01-01 is a Monday
    flag = R.day_of_week(c, [0])
    # decided on Sunday 2024-01-07 for Monday 2024-01-08; the backtest shifts it by one day
    assert flag[pd.Timestamp("2024-01-07")] == 1.0 and flag.sum() == 2  # set on Sundays Jan 7 and Jan 14
    pos = flag.shift(1)
    assert set(pos[pos == 1].index.weekday) == {0}


def test_turn_of_month_window():
    c = random_walk(70, start="2024-01-01")
    pos = R.turn_of_month(c, last=2, first=3).shift(1).dropna()
    held = pos[pos == 1].index
    assert {d.day for d in held if d.month == 2} == {1, 2, 3, 28, 29}  # 2024 is a leap year


def test_vol_target_is_capped_and_inverse_to_vol():
    calm = random_walk(300, vol=0.005, seed=1)
    wild = random_walk(300, vol=0.08, seed=1)
    assert R.vol_target(calm, 0.3).dropna().max() <= 1.0
    assert R.vol_target(wild, 0.3).dropna().mean() < 0.3


def test_cross_rule_uses_other_asset():
    btc = pd.Series(np.r_[np.linspace(100, 50, 300), np.linspace(50, 200, 300)],
                    index=pd.date_range("2020-01-01", periods=600))
    alt = random_walk(600, start="2020-01-01")
    flag = R.build({"type": "asset_above_sma", "asset": "BTC", "window": 200}, MemoryStore({"BTC": btc, "ALT": alt}),
                   "ALT")
    assert flag.iloc[250] == 0.0 and flag.iloc[-1] == 1.0


def test_permutation_p_detects_calendar_effect_and_not_noise():
    rng = np.random.default_rng(3)
    idx = pd.date_range("2018-01-01", periods=1400)
    r = rng.normal(0, 0.03, len(idx))
    pos = (idx.weekday == 0).astype(float)
    assert permutation_p(pos, r, 0.0, rng, 300) > 0.05
    r2 = r + np.where(idx.weekday == 0, 0.02, 0.0)
    assert permutation_p(pos, r2, 0.0, rng, 300) < 0.01


def test_calendar_rules_need_permutation(tmp_registry):
    hyp, _ = tmp_registry
    spec = {**SPEC, "rule": {"type": "day_of_week", "days": [0]},
            "significance": {"method": "circular_shift", "alpha": 0.05}}
    assert any("permutation" in e for e in registry.validate(make(hyp, spec=spec)))
    spec["significance"]["method"] = "permutation"
    assert registry.validate(make(hyp, "H-101", spec=spec)) == []
    spec2 = {**SPEC, "significance": {"method": "permutation", "alpha": 0.05}}
    assert any("only valid for calendar" in e for e in registry.validate(make(hyp, "H-102", spec=spec2)))


def test_breadth_counts_coins_above_their_average():
    from crl.agents import regime_watch
    idx = pd.date_range("2020-01-01", periods=400)
    up = pd.Series(np.linspace(1, 2, 400), index=idx)
    down = pd.Series(np.linspace(2, 1, 400), index=idx)
    store = MemoryStore({"A": up, "B": up, "C": down, "D": down})
    s = regime_watch.series(store, {"metric": "breadth", "params": {"window": 200, "symbols": ["A", "B", "C", "D", "X"]}})
    assert s.iloc[-1] == 0.5 and s.index[0] == idx[199]

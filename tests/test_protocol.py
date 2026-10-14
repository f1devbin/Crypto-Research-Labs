"""The protocol must find planted effects and must not find effects in noise."""
import numpy as np
import pandas as pd

from crl.data.store import MemoryStore
from crl.engine import protocol
from crl.engine.stats import circular_shift_p
from tests.conftest import random_walk, trending

CANDS = {"SMA50": {"type": "price_above_sma", "window": 50},
         "TSMOM90": {"type": "tsmom", "lookback": 90}}


def search_spec(universe):
    return {"kind": "rule_search", "candidates": CANDS, "mode": "long_flat", "fee": 0.001,
            "universe": universe, "in_sample": {"start": "2018-03-01", "end": "2021-12-31"},
            "out_of_sample": {"start": "2022-01-01"},
            "significance": {"method": "bootstrap", "n": 100, "alpha_family": 0.05},
            "criterion": {"min_strict_wins": 2}}


def test_rule_search_finds_planted_trend():
    store = MemoryStore({"A": trending(seed=3), "B": trending(seed=4)})
    res = protocol.evaluate(search_spec(["A", "B"]), store)
    assert res["verdict"] == "PASS", res["summary"]
    assert all(r["p"] < 0.025 for r in res["rows"])


def test_rule_search_rejects_noise():
    store = MemoryStore({"A": random_walk(seed=5), "B": random_walk(seed=6)})
    res = protocol.evaluate(search_spec(["A", "B"]), store)
    assert res["verdict"] in ("FAIL", "WEAK")
    assert sum(r["win"] for r in res["rows"]) == 0


def test_timing_rule_with_feature_and_shift_test():
    c = random_walk(1800, vol=0.02, seed=7)
    r = c.pct_change().shift(-1)  # tomorrow's return — an oracle feature, known one day late
    oracle = r.shift(-1)  # dated one day earlier so that after lag=1 it lines up with tomorrow
    spec = {"kind": "timing_rule",
            "rule": {"type": "feature_threshold", "feature": "oracle", "threshold": 0, "long_when": "above",
                     "lag": 1},
            "mode": "long_flat", "fee": 0.001, "universe": ["X"],
            "periods": [{"name": "oos", "start": "2020-01-01"}],
            "significance": {"method": "circular_shift", "n": 300, "alpha": 0.0125},
            "criterion": {"min_wins": {"oos": 1}, "require_significance": True}}
    store = MemoryStore({"X": c}, {"oracle": oracle})
    res = protocol.evaluate(spec, store)
    assert res["verdict"] == "PASS"

    store_noise = MemoryStore({"X": c}, {"oracle": pd.Series(np.random.default_rng(0).normal(size=len(c)),
                                                             index=c.index)})
    assert protocol.evaluate(spec, store_noise)["verdict"] in ("FAIL", "WEAK")


def test_circular_shift_p_is_roughly_uniform_under_null():
    rng = np.random.default_rng(11)
    ps = []
    for i in range(30):
        r = rng.normal(0, 0.02, 600)
        pos = (rng.random(600) > 0.5).astype(float)
        ps.append(circular_shift_p(pos, r, 0.0, rng, 200))
    assert 0.25 < np.mean(ps) < 0.75
    assert np.mean(np.array(ps) < 0.05) < 0.2


def test_markdown_renders():
    store = MemoryStore({"A": trending(seed=3), "B": trending(seed=4)})
    res = protocol.evaluate(search_spec(["A", "B"]), store)
    md = protocol.to_markdown({"id": "H-999", "title": "t"}, res)
    assert "H-999" in md and "| A | oos |" in md

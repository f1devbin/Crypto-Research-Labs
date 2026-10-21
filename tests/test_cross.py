import numpy as np
import pandas as pd

from crl import registry
from crl.data.store import MemoryStore
from crl.engine import cross as X
from crl.engine.protocol import evaluate
from tests.conftest import random_walk

U = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT"]


def spec(**sig):
    return {"kind": "cross_section", "signal": {"type": "momentum", "lookbacks": [1, 3], **sig},
            "select": {"top": 2}, "fee": 0.001, "universe": U,
            "periods": [{"name": "all", "start": "2019-01-01"}],
            "significance": {"method": "circular_shift", "n": 200, "alpha": 0.05},
            "criterion": {"min_wins": {"all": 1}, "require_significance": True}}


def test_no_lookahead_weights_use_only_past_closes():
    store = MemoryStore({s: random_walk(seed=i, start="2018-01-01", n=1500) for i, s in enumerate(U)})
    closes = X.panel(store, U)
    w1 = X.weights(spec(), closes, store)
    cut = closes.copy()
    cut.iloc[1000:] = cut.iloc[1000:] * 3.0  # change the future only
    w2 = X.weights(spec(), cut, store)
    assert w1.iloc[:1000].equals(w2.iloc[:1000])
    assert np.allclose(w1.dropna().sum(axis=1).max(), 1.0)


def test_random_data_does_not_pass():
    # no signal in random walks: the rotation must not look significant
    store = MemoryStore({s: random_walk(seed=10 + i, start="2018-01-01", n=2000) for i, s in enumerate(U)})
    res = evaluate(spec(overheat_z=2.5, market_filter={"asset": "BTCUSDT", "window": 200}), store)
    assert res["verdict"] in ("FAIL", "WEAK") and res["rows"][0]["p"] > 0.05


def test_registered_cross_section_specs_are_valid():
    for h in registry.load_all():
        if (h.get("spec") or {}).get("kind") == "cross_section":
            assert not registry.validate(h), h.id

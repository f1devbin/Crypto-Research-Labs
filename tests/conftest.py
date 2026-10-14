import numpy as np
import pandas as pd
import pytest


def random_walk(n=2500, drift=0.0005, vol=0.03, seed=1, start="2017-08-17"):
    rng = np.random.default_rng(seed)
    r = rng.normal(drift, vol, n)
    return pd.Series(100 * np.cumprod(1 + r), index=pd.date_range(start, periods=n, freq="D"))


def trending(n=2500, seed=2, start="2017-08-17", regime_days=120, strength=0.006):
    """Persistent up/down regimes: a trend rule should catch them."""
    rng = np.random.default_rng(seed)
    signs = np.repeat(rng.choice([-1.0, 1.0], size=n // regime_days + 1), regime_days)[:n]
    r = signs * strength + rng.normal(0, 0.02, n)
    return pd.Series(100 * np.cumprod(1 + r), index=pd.date_range(start, periods=n, freq="D"))


@pytest.fixture
def tmp_registry(tmp_path, monkeypatch):
    hyp, res = tmp_path / "hypotheses", tmp_path / "results"
    hyp.mkdir()
    res.mkdir()
    import crl.config as cfg
    import crl.registry as reg
    monkeypatch.setattr(cfg, "HYPOTHESES_DIR", hyp)
    monkeypatch.setattr(reg, "HYPOTHESES_DIR", hyp)
    monkeypatch.setattr(reg, "RESULTS_DIR", res)
    return hyp, res

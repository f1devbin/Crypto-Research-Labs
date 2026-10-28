import copy
import datetime as dt

import pytest

from crl import registry
from crl.config import HYPOTHESES_DIR

SPEC = {"kind": "timing_rule", "rule": {"type": "price_above_sma", "window": 50}, "mode": "long_flat",
        "fee": 0.001, "universe": ["BTCUSDT"], "periods": [{"name": "oos", "start": "2022-01-01"}],
        "criterion": {"min_wins": {"oos": 1}}}


def make(path, hid="H-100", status="draft", spec=None, **extra):
    data = {"id": hid, "title": "test", "status": status, "family": "trend", "created": "2026-10-14",
            "rationale": "r", "spec": copy.deepcopy(spec or SPEC), **extra}
    h = registry.Hypothesis(path / f"{hid}.yaml", data)
    registry.save(h)
    return h


def test_shipped_registry_is_valid():
    hyps = registry.load_all(HYPOTHESES_DIR)
    assert len(hyps) >= 10
    for h in hyps:
        assert registry.validate(h) == [], h.id
        assert registry.duplicates(h, hyps) == [], h.id


def test_register_locks_spec(tmp_registry):
    hyp, _ = tmp_registry
    h = make(hyp)
    registry.register(h, dt.date(2026, 10, 14))
    assert h["status"] == "registered" and registry.validate(h) == []
    h.data["spec"]["rule"]["window"] = 51  # silent post-registration tweak
    assert any("sha256 mismatch" in e for e in registry.validate(h))


def test_draft_needs_no_hash_but_registered_does(tmp_registry):
    hyp, _ = tmp_registry
    assert registry.validate(make(hyp)) == []
    errs = registry.validate(make(hyp, "H-101", status="registered"))
    assert any("prereg_sha256" in e for e in errs)


def test_duplicates_ignore_wording(tmp_registry):
    hyp, _ = tmp_registry
    a = make(hyp, "H-100")
    b = make(hyp, "H-101", title="totally different words")
    c_spec = copy.deepcopy(SPEC)
    c_spec["universe"] = ["ETHUSDT"]
    c = make(hyp, "H-102", spec=c_spec)
    assert registry.duplicates(b, [a, b, c]) == ["H-100"]
    assert registry.duplicates(c, [a, b, c]) == []


@pytest.mark.parametrize("rule,needle", [
    ({"type": "price_above_sma"}, "missing params"),
    ({"type": "price_above_sma", "window": 5, "colour": 1}, "unknown params"),
    ({"type": "feature_threshold", "feature": "moon_phase", "threshold": 1, "long_when": "above"}, "feature"),
    ({"type": "astrology"}, "unknown rule"),
])
def test_bad_rules_rejected(tmp_registry, rule, needle):
    hyp, _ = tmp_registry
    spec = copy.deepcopy(SPEC)
    spec["rule"] = rule
    assert any(needle in e for e in registry.validate(make(hyp, spec=spec)))


def test_due_logic(tmp_registry):
    hyp, res = tmp_registry
    h = make(hyp, retest_every_days=30)
    registry.register(h)
    today = dt.date(2026, 10, 14)
    assert registry.is_due(h, today)
    registry.store_result(h, {"verdict": "FAIL", "run_at": "2026-10-01T00:00:00Z", "summary": "", "rows": []}, res)
    assert h["status"] == "rejected"
    assert not registry.is_due(h, today, res)
    assert registry.is_due(h, dt.date(2026, 11, 1), res)


def test_test_after_postpones_the_first_run(tmp_registry):
    hyp, res = tmp_registry
    h = make(hyp, test_after="2027-10-15")
    registry.register(h)
    assert not registry.is_due(h, dt.date(2027, 10, 14), res)
    assert registry.is_due(h, dt.date(2027, 10, 15), res)


def test_declared_replication_is_not_a_duplicate(tmp_registry):
    hyp, _ = tmp_registry
    a = make(hyp, "H-100")
    b = make(hyp, "H-101", replicates="H-100")
    c = make(hyp, "H-102")
    assert registry.duplicates(b, [a, b, c]) == ["H-102"]


def test_forecast_model_options_are_checked(tmp_registry):
    import copy
    hyp, _ = tmp_registry
    from crl import registry
    spec = {"kind": "forecast_live", "target": "direction", "log_suffix": "_v2",
            "model": {"type": "pooled_logit", "features": ["r1"], "zscore_window": 365, "zscore_min_periods": 180,
                      "clip": 5, "l2": 1.0, "refit": "monthly", "external_lag": 1, "ffill_limit": 3,
                      "coin_intercepts": True, "calibration": "platt_365"},
            "universe": ["BTCUSDT"], "costs": {"default": 0.001}, "portfolio": {"weight": "probability", "band": 0.1},
            "execution": {"time_utc": "12:00"}, "periods": [{"name": "forward", "start": "2026-11-01"}],
            "significance": {"method": "circular_shift", "n": 2000, "alpha": 0.0125}}
    good = registry.Hypothesis(hyp / "H-901.yaml", {"id": "H-901", "title": "t", "status": "draft", "family": "forecast",
                                                    "created": "2026-10-28", "rationale": "r", "spec": spec,
                                                    "test_after": "2027-11-01"})
    assert registry.validate(good) == []
    bad = copy.deepcopy(good.data)
    bad["spec"]["model"]["calibration"] = "isotonic"
    bad["spec"]["log_suffix"] = "v2"
    bad["spec"]["model"]["magic"] = 1
    errs = " ".join(registry.validate(registry.Hypothesis(hyp / "H-901.yaml", bad)))
    assert "calibration" in errs and "log_suffix" in errs and "unknown keys" in errs

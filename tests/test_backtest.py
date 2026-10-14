import numpy as np
import pandas as pd
import pytest

from crl.engine.backtest import evaluate_period, metrics, run, sharpe, to_position
from crl.engine import rules as R


def test_decision_applies_to_next_day_only():
    idx = pd.date_range("2024-01-01", periods=4, freq="D")
    r = pd.Series([0.0, 0.10, -0.20, 0.05], index=idx)
    decision = pd.Series([0, 1, 0, 0], index=idx, dtype=float)  # long decided at close of day 1
    s, _ = run(decision, r, fee=0.0)
    assert s.tolist() == pytest.approx([0.0, 0.0, -0.20, 0.0])  # earns day 2 only


def test_fees_charged_on_turnover():
    idx = pd.date_range("2024-01-01", periods=4, freq="D")
    r = pd.Series(0.0, index=idx)
    s, turn = run(pd.Series([1, 1, 0, 0], index=idx, dtype=float), r, fee=0.001)
    assert turn.sum() == pytest.approx(2.0)  # enter + exit
    assert s.sum() == pytest.approx(-0.002)


def test_long_short_mapping_and_nan():
    f = pd.Series([1.0, 0.0, np.nan])
    assert to_position(f, "long_short").tolist()[:2] == [1.0, -1.0]
    assert np.isnan(to_position(f, "long_flat").iloc[2])


def test_metrics_drawdown():
    s = pd.Series([0.1, -0.5, 0.0])
    m = metrics(s)
    assert m["max_dd"] == pytest.approx(-0.5)
    assert sharpe(np.zeros(10)) == 0.0


def test_price_rules_never_look_ahead():
    """Changing tomorrow's price must not change today's flag."""
    from tests.conftest import random_walk
    c = random_walk(400)
    for spec in ({"window": 50}, ):
        a = R.price_above_sma(c, **spec)
        c2 = c.copy()
        c2.iloc[300:] *= 3
        b = R.price_above_sma(c2, **spec)
        pd.testing.assert_series_equal(a.iloc[:300], b.iloc[:300])
    d1 = R.donchian(c, 20)
    c3 = c.copy()
    c3.iloc[250:] *= 0.1
    pd.testing.assert_series_equal(d1.iloc[:250], R.donchian(c3, 20).iloc[:250])


def test_feature_rule_lags_publication():
    idx = pd.date_range("2024-01-01", periods=5, freq="D")
    x = pd.Series([0, 0, 10, 0, 0], index=idx, dtype=float)
    flag = R.feature_threshold(x, 5, "above", lag=1)
    assert flag.tolist()[1:] == [0.0, 0.0, 1.0, 0.0]  # value of day 3 usable from day 4


def test_undefined_days_excluded_from_evaluation():
    from tests.conftest import random_walk
    c = random_walk(300)
    flag = R.price_above_sma(c, 200)
    e = evaluate_period(flag, c, np.ones(len(c), dtype=bool), 0.001)
    assert e["days"] == len(c) - 200  # first day with a defined position is day 200

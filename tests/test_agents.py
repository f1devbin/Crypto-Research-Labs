import datetime as dt
import json

import pandas as pd

from crl.agents import regime_watch
from crl.data.integrity import check_series
from crl.llm import proposer
from crl import registry
from tests.test_registry import SPEC, make


def test_band_and_transitions():
    bands = {"low": [None, 0.04], "high": [0.04, None]}
    assert regime_watch.band(0.01, bands) == "low" and regime_watch.band(0.2, bands) == "high"
    monitors = {"carry": {"label": "Carry", "bands": bands, "format": "{:.0%}", "notes": {"high": "look"}}}
    prev = {"carry": {"band": "low"}}
    assert regime_watch.transitions({"carry": {"value": 0.1, "band": "high"}}, prev, monitors) == \
        ["Carry: low → high (10%). look"]
    # no alert on first run, on unchanged band, or when a source is down
    assert regime_watch.transitions({"carry": {"value": 0.1, "band": "high"}}, {}, monitors) == []
    assert regime_watch.transitions({"carry": {"value": None, "band": "unavailable"}}, prev, monitors) == []


def test_integrity_flags_gaps_staleness_and_duplicates():
    idx = pd.to_datetime(["2026-10-01", "2026-10-02", "2026-10-02", "2026-10-05"])
    s = pd.Series([1.0, 2.0, 2.0, 3.0], index=idx)
    msgs = " | ".join(f.message for f in check_series("X", s, pd.Timestamp("2026-10-14"), is_price=True))
    assert "duplicate" in msgs and "stale" in msgs and "missing" in msgs


def test_proposer_drafts_every_coin_with_a_gate_line_and_rejects_duplicates_and_junk(tmp_path):
    existing = make(tmp_path, "H-001", spec={**SPEC, "universe": list(proposer.BINANCE_COINS)})
    good = {"title": "ETH SMA100", "family": "trend", "rationale": "r",
            "spec": {**SPEC, "rule": {"type": "price_above_sma", "window": 100}, "universe": ["ETHUSDT"],
                     "significance": {"method": "circular_shift", "n": 500, "alpha": 0.05}}}
    dup = {"title": "same as H-001, picked one coin", "family": "trend", "rationale": "r", "spec": SPEC}
    junk = {"title": "moon", "family": "x", "rationale": "r", "spec": {"kind": "magic"}}
    written, rejected = proposer.accept([good, dup, junk], [existing], tmp_path, dt.date(2026, 11, 4), "m")
    assert written == ["H-002", "H-003"] and len(rejected) == 2
    main, gate = registry.load_all(tmp_path)[1:]
    assert len(proposer.COINS) == 13 and set(proposer.GATE_COINS) == {"EVERUSDT", "GRAMUSDT"}
    assert main["spec"]["universe"] == proposer.BINANCE_COINS and main["spec"]["fee"] == 0.001
    assert gate["spec"]["universe"] == proposer.GATE_COINS and gate["spec"]["fee"] == 0.004
    assert gate["spec"]["periods"] == [{"name": "gate", "start": "2023-03-13"}] and "H-002" in gate["rationale"]
    for h in (main, gate):
        assert h["status"] == "draft" and h["author"] == "llm:m" and not registry.validate(h)
        assert h["spec"]["significance"]["alpha"] <= 0.05 / 13 and h["spec"]["criterion"]["require_significance"]
    short, gate_line = proposer.all_coins({**SPEC, "mode": "long_short", "fee": 0.0005})
    assert short["mode"] == "long_short" and short["fee"] == 0.0005
    assert gate_line["mode"] == "long_flat" and gate_line["fee"] == 0.004  # Gate.io spot cannot short


def test_proposer_extracts_json_from_chatty_reply():
    text = 'Sure! Here you go:\n[{"title": "a"}]\nGood luck.'
    assert proposer._extract_json(text) == [{"title": "a"}]
    assert json.loads(json.dumps(proposer.EXAMPLE))  # example stays serialisable


def test_alerts_follow_telegram_lang(monkeypatch):
    from crl import notify
    from crl.i18n import LANGS
    from crl.i18n_alerts import A
    for code in LANGS:
        assert set(A[code]) == set(A["en"]), code
    monkeypatch.setenv("TELEGRAM_LANG", "ru")
    monitors = {"btc_trend": {"label": "BTC vs SMA200", "bands": {"below": [None, 0], "above": [0, None]},
                              "format": "{:+.1%}"}}
    msg = regime_watch.transitions({"btc_trend": {"value": 0.05, "band": "above"}},
                                   {"btc_trend": {"band": "below"}}, monitors)[0]
    assert msg.startswith("BTC относительно 200-дневной средней") or "→" in msg
    assert "ниже → выше" in msg and notify.site_url().endswith("/ru/")
    monkeypatch.setenv("TELEGRAM_LANG", "xx")
    assert notify.lang() == "en"

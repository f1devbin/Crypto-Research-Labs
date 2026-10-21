import datetime as dt

from crl import scan, site
from crl.data.store import MemoryStore
from tests.conftest import random_walk
from tests.test_site import SYMBOLS


def test_bh_qvalues_monotone_and_bounded():
    q = scan.bh_qvalues([0.01, 0.04, 0.03, 0.5])
    assert q[0] == 0.04 and all(0 <= x <= 1 for x in q)
    assert q[0] <= q[2] <= q[1] <= q[3]


def test_scan_covers_every_rule_and_coin(tmp_path, monkeypatch):
    store = MemoryStore({s: random_walk(seed=i, start="2017-08-17", n=3350) for i, s in enumerate(SYMBOLS)})
    res = scan.run(store, n=50)
    ids = {r["id"] for r in res["rules"]}
    assert "H-005" in ids and "H-018" not in ids  # same rule as H-005: folded in
    assert len(res["cells"]) == len(res["rules"]) * len(res["coins"])
    assert sum(res["counts"].values()) == len(res["cells"])
    sol = next(c for c in res["cells"] if c["rule"] == "H-014" and c["symbol"] == "SOLUSDT")
    assert sol["official"] and sol["status"] in scan.STATUSES
    # the dashboard renders the matrix, the per-rule and per-coin tables and the diagnosis
    monkeypatch.setattr(scan, "OUT_JSON", tmp_path / "coverage.json")
    (tmp_path / "coverage.json").write_text(__import__("json").dumps(res, default=str))
    monkeypatch.setattr(scan, "load", lambda path=None: res)
    out = site.build(store, tmp_path / "_site", dt.datetime(2026, 10, 21, tzinfo=dt.timezone.utc), "https://x.test/")
    home = (out / "ru" / "index.html").read_text(encoding="utf-8")
    assert "Какое правило на какой монете работает" in home and 'class="sortable rt"' in home and 'data-label=' in home
    assert (out / "sort.js").exists()
    assert "Это же правило на всех монетах" in (out / "ru" / "hypotheses" / "H-005.html").read_text(encoding="utf-8")
    coin = (out / "ru" / "coins" / "SOLUSDT.html").read_text(encoding="utf-8")
    assert "Диагноз простыми словами" in coin and "Какие проверенные правила сработали" in coin
    h22 = (out / "ru" / "hypotheses" / "H-022.html").read_text(encoding="utf-8")
    assert "Собрано форвардных данных: 6 из 365 дней" in h22


def test_diagnosis_needs_a_clear_majority():
    def mon(i, v, band):
        return {"id": i, "value": v, "band": band}
    reg = [mon("btc_trend", 0.14, "above"), mon("btc_volatility", 0.33, "calm"), mon("fear_greed", 63, "greed"),
           mon("stablecoin_growth", -0.01, "contracting"), mon("h020_rule", 1, "rule_in")]
    coins = [{"vs200": x} for x in (0.1,) * 8 + (-0.1,) * 5]
    d = site.diagnosis(reg, coins)
    assert (d["up"], d["down"], d["neutral"]) == (2, 1, 3) and d["level"] == "mixed"
    reg[3] = mon("stablecoin_growth", 0.03, "expanding")
    assert site.diagnosis(reg, coins)["level"] == "up"


def test_plain_weekly_summary_without_model(monkeypatch):
    from crl.agents import regime_watch
    from crl.llm import digest as D
    monkeypatch.setattr(regime_watch, "evaluate", lambda store, m: {
        "btc_trend": {"value": 0.14, "band": "above"}, "fear_greed": {"value": 63, "band": "greed"},
        "stablecoin_growth": {"value": -0.01, "band": "contracting"}})
    store = MemoryStore({s: random_walk(seed=i, start="2017-08-17", n=3350) for i, s in enumerate(SYMBOLS)})
    text = D.plain_summary("ru", store)
    assert text.startswith(("Рост", "Смешанная", "Спад")) and "▲ Биткоин на 14.0% выше" in text
    assert "|" not in text and "#" not in text  # no markdown tables or headings in Telegram

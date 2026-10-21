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
    assert "Какое правило на какой монете работает" in home and 'class="sortable"' in home
    assert (out / "sort.js").exists()
    assert "Это же правило на всех монетах" in (out / "ru" / "hypotheses" / "H-005.html").read_text(encoding="utf-8")
    coin = (out / "ru" / "coins" / "SOLUSDT.html").read_text(encoding="utf-8")
    assert "Диагноз простыми словами" in coin and "Какие проверенные правила сработали" in coin
    h22 = (out / "ru" / "hypotheses" / "H-022.html").read_text(encoding="utf-8")
    assert "Собрано форвардных данных: 6 из 365 дней" in h22

import datetime as dt
import json
import re

from crl import site
from crl.data.store import MemoryStore
from crl.i18n import LANGS, T
from tests.conftest import random_walk

SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT", "LTCUSDT", "LINKUSDT", "DOGEUSDT",
           "XLMUSDT", "TRXUSDT"]


def test_site_builds_every_language_with_seo_basics(tmp_path, monkeypatch):
    monkeypatch.setenv("GOOGLE_SITE_VERIFICATION", "abc123")
    store = MemoryStore({s: random_walk(seed=i, start="2017-08-17", n=3350) for i, s in enumerate(SYMBOLS)})
    out = site.build(store, tmp_path / "_site", dt.datetime(2026, 10, 14, tzinfo=dt.timezone.utc), "https://x.test/")
    for lang in LANGS:
        index = out / ("index.html" if lang == "en" else f"{lang}/index.html")
        html = index.read_text(encoding="utf-8")
        assert f'<html lang="{LANGS[lang][1]}">' in html
        assert html.count('rel="alternate" hreflang=') == len(LANGS) + 1
        assert '<link rel="canonical"' in html and 'google-site-verification" content="abc123"' in html
        assert html.count("<h1>") == 1 and "application/ld+json" in html
        assert (out / ("" if lang == "en" else f"{lang}/") / "hypotheses" / "H-003.html").exists()
    sitemap = (out / "sitemap.xml").read_text()
    d = json.loads((out / "data.json").read_text())
    assert sitemap.count("<url>") == len(LANGS) * (len(d["hypotheses"]) + len(d["coins"]) + 2)
    course = (out / "ru" / "course.html").read_text(encoding="utf-8")
    assert "Курс для новичков" in course and '"@type": "Course"' in course.replace('":"', '": "') or '"Course"' in course
    assert "{" not in course.split("<main>")[1].split("</main>")[0]  # every placeholder filled
    assert "/ru/coins/SOLUSDT.html" in sitemap and (out / "ru" / "coins" / "SOLUSDT.html").exists()
    sol = (out / "coins" / "SOLUSDT.html").read_text(encoding="utf-8")
    assert "Solana (SOL)" in sol and "H-014" in sol and 'href="../#coins"' in sol
    assert "Sitemap: https://x.test/sitemap.xml" in (out / "robots.txt").read_text()
    data = json.loads((out / "data.json").read_text())
    assert data["btc"] and any(h["curves"] for h in data["hypotheses"])
    # every text node is rendered server-side: the hypotheses table is in the HTML, not built by JS
    assert re.search(r"H-011", (out / "ru" / "index.html").read_text(encoding="utf-8"))


def test_translations_cover_english_keys():
    for lang in LANGS:
        missing = [k for k in T["en"] if k not in T[lang] and k != "titles"]
        assert not missing, (lang, missing)
        assert len(T[lang]["glossary"]) == len(T["en"]["glossary"])
        assert len(T[lang]["how"]) == len(T["en"]["how"])


def test_course_is_complete_in_every_language():
    from crl import course as C
    en = C.LESSONS["en"]
    for lang in LANGS:
        assert lang in C.LESSONS and lang in C.UI, lang
        assert len(C.LESSONS[lang]) == len(en), lang
        for (_, a), (_, b) in zip(en, C.LESSONS[lang]):
            assert C.placeholders(a) == C.placeholders(b), lang
            assert ("[[flow]]" in a) == ("[[flow]]" in b), lang
    html = C.md_to_html("**a** [b](c)\n\n1. x\n2. y\n\n| h |\n| --- |\n| v |\n\n- [ ] t")
    assert "<strong>a</strong>" in html and '<a href="c">b</a>' in html and "<ol>" in html and "<table>" in html
    assert 'type="checkbox"' in html

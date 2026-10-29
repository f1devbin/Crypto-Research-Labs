import datetime as dt
import json
import re
from html import unescape as html_unescape

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
    assert sitemap.count("<url>") == len(LANGS) * (len(d["hypotheses"]) + len(d["coins"]) + 8)
    course = (out / "ru" / "course.html").read_text(encoding="utf-8")
    assert "Курс для новичков" in course and '"@type": "Course"' in course.replace('":"', '": "') or '"Course"' in course
    assert "{" not in course.split("<main>")[1].split("</main>")[0]  # every placeholder filled
    setup = (out / "ru" / "setup.html").read_text(encoding="utf-8")
    assert "TELEGRAM_LANG" in setup and "ANTHROPIC_API_KEY" in setup and 'href="../charts.js"' not in setup
    assert "/ru/setup.html" in sitemap and 'setup.html">' in (out / "ru" / "index.html").read_text(encoding="utf-8")
    assert "/ru/coins/SOLUSDT.html" in sitemap and (out / "ru" / "coins" / "SOLUSDT.html").exists()
    sol = (out / "coins" / "SOLUSDT.html").read_text(encoding="utf-8")
    assert "Solana (SOL)" in sol and "H-014" in sol and 'href="../market.html#coins"' in sol
    assert "Sitemap: https://x.test/sitemap.xml" in (out / "robots.txt").read_text()
    assert re.findall(r"<loc>([^<]+)</loc>", sitemap) and all(
        u.startswith("https://x.test/") for u in re.findall(r'(?:<loc>|href=")([^<"]+)', sitemap))
    for f in out.rglob("*.html"):  # search engines get absolute links, short titles and whole descriptions
        html = f.read_text(encoding="utf-8")
        if f.name == "404.html" or "<title>" not in html:  # search-engine verification files have no head
            continue
        links = re.findall(r'<link rel="(?:canonical|alternate)"[^>]*href="([^"]+)"', html)
        links += re.findall(r'<meta property="og:(?:url|image)" content="([^"]+)"', html)
        assert len(links) == len(LANGS) + 4 and all(u.startswith("https://x.test/") for u in links), (f, links)
        title = re.search(r"<title>(.*?)</title>", html).group(1)
        desc = re.search(r'<meta name="description" content="([^"]*)"', html).group(1)
        short = (8, 25) if "/zh/" in str(f) else (20, 50)  # Chinese needs about half the characters
        assert short[0] <= len(html_unescape(title)) <= 80 and short[1] <= len(html_unescape(desc)) <= 160, (f, title)
    btc = (out / "ru" / "coins" / "BTCUSDT.html").read_text(encoding="utf-8")
    assert "<h1>Биткоин (BTC):" in btc and "<title>Биткоин (BTC) сегодня:" in btc
    h20 = (out / "hypotheses" / "H-020.html").read_text(encoding="utf-8")
    assert "<title>Do Bitcoin exchange inflows predict price drops?" in h20
    assert '<p class="plain"><strong>Do Bitcoin exchange inflows predict price drops?</strong>' in h20
    data = json.loads((out / "data.json").read_text())
    assert data["btc"] and any(h["curves"] for h in data["hypotheses"])
    # every text node is rendered server-side: the hypotheses table is in the HTML, not built by JS
    assert re.search(r"H-011", (out / "ru" / "research.html").read_text(encoding="utf-8"))


def test_site_address_is_absolute_even_if_the_variable_is_empty(tmp_path, monkeypatch):
    import importlib

    import pytest

    from crl import config
    monkeypatch.setenv("CRL_SITE_URL", "")  # an Actions variable that is not set arrives as ""
    assert importlib.reload(config).SITE_URL == "https://f1devbin.github.io/Crypto-Research-Labs/"
    monkeypatch.setenv("CRL_SITE_URL", "https://example.org/lab")
    assert importlib.reload(config).SITE_URL == "https://example.org/lab/"
    monkeypatch.delenv("CRL_SITE_URL")
    importlib.reload(config)
    with pytest.raises(ValueError):
        site.build(MemoryStore({}), tmp_path / "_site", base="/")


def test_every_hypothesis_has_a_search_question_in_every_language():
    from crl.config import HYPOTHESES_DIR
    from crl.i18n_seo import QUESTIONS
    ids = sorted(p.stem for p in HYPOTHESES_DIR.glob("H-*.yaml"))
    assert ids and set(ids) <= set(QUESTIONS["en"]), set(ids) - set(QUESTIONS["en"])
    for lang in LANGS:
        assert set(QUESTIONS[lang]) == set(QUESTIONS["en"]), lang
        assert all(len(q) <= 66 for q in QUESTIONS[lang].values()), [q for q in QUESTIONS[lang].values() if len(q) > 66]


def test_one_question_per_page(tmp_path):
    store = MemoryStore({s: random_walk(seed=i, start="2017-08-17", n=3350) for i, s in enumerate(SYMBOLS)})
    out = site.build(store, tmp_path / "_site", dt.datetime(2026, 10, 14, tzinfo=dt.timezone.utc), "https://x.test/")
    for lang in LANGS:
        root = out if lang == "en" else out / lang
        for name in ("index.html", "market.html", "research.html", "forecast.html", "about.html", "course.html",
                     "coins/BTCUSDT.html"):
            html = (root / name).read_text(encoding="utf-8")
            menu = html.split('<nav class="menu"', 1)[1].split("</nav>", 1)[0]
            assert menu.count("<a ") == 5 and "#" not in menu, (lang, name)  # five pages, no in-page anchors
        home = (root / "index.html").read_text(encoding="utf-8").split("<main>")[1].split("</main>")[0]
        assert "<table" not in home and 'id="glossary"' not in home and 'href="course.html"' in home
        assert 'id="glossary"' in (root / "course.html").read_text(encoding="utf-8")
        assert 'id="data"' in (root / "about.html").read_text(encoding="utf-8")
        assert 'class="matrix"' in (root / "research.html").read_text(encoding="utf-8")
    assert "'#hypotheses':'research.html#all'" in (out / "ui.js").read_text()


def _lum(hex_):
    rgb = [int(hex_[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def test_text_tokens_keep_high_contrast():
    from crl.site_render import CSS
    dark = dict(re.findall(r"--(\w+):(#[0-9a-f]{6})", CSS.split("@media")[0]))
    light = dict(re.findall(r"--(\w+):(#[0-9a-f]{6})", CSS.split("prefers-color-scheme:light")[1].split("}}")[0]))
    for theme in (dark, light):
        for fg in ("text", "text2", "link"):
            for bg in ("bg", "panel", "raised"):
                a, b = sorted((_lum(theme[fg]), _lum(theme[bg])), reverse=True)
                assert (a + 0.05) / (b + 0.05) >= 7, (fg, bg)  # WCAG AAA for body text


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


def test_setup_guide_is_complete_in_every_language():
    from crl import setup_guide as SG
    keys = set(SG.GUIDE["en"])
    for lang in LANGS:
        g = SG.GUIDE[lang]
        assert set(g) == keys and len(g["sections"]) == len(SG.GUIDE["en"]["sections"]), lang
        text = " ".join(md for _, md in g["sections"])
        for name in ("TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID", "TELEGRAM_LANG", "ANTHROPIC_API_KEY", "test_alert"):
            assert name in text, (lang, name)


def test_digest_page_shows_model_written_weeks(tmp_path, monkeypatch):
    import datetime as _dt
    from crl.llm import digest as D
    D.write("facts", {"ru": "Рынок спокоен.\n\n- BTC выше средней", "en": "Calm market."}, "llama-x",
            _dt.date(2026, 10, 19), tmp_path)
    D.write("facts only", {}, None, _dt.date(2026, 10, 26), tmp_path)  # no model: not shown
    weeks = D.load(tmp_path)
    assert [w["week"] for w in weeks] == ["2026-W43"] and weeks[0]["model"] == "llama-x"
    monkeypatch.setattr(D, "load", lambda root=None, limit=12: weeks)
    store = MemoryStore({s: random_walk(seed=i, start="2017-08-17", n=3350) for i, s in enumerate(SYMBOLS)})
    out = site.build(store, tmp_path / "_site", dt.datetime(2026, 10, 21, tzinfo=dt.timezone.utc), "https://x.test/")
    ru = (out / "ru" / "digest.html").read_text(encoding="utf-8")
    assert "Неделя 2026-W42: 2026-10-12 – 2026-10-18" in ru and "<li>BTC выше средней</li>" in ru
    es = (out / "es" / "digest.html").read_text(encoding="utf-8")
    assert "Calm market." in es and "se muestra en inglés" in es
    assert "Недельная сводка: 2026-10-12 – 2026-10-18" in (out / "ru" / "index.html").read_text(encoding="utf-8")

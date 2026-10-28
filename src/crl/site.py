"""Static dashboard for GitHub Pages: `crl site` writes _site/index.html + data.json.

Everything shown is computed from the same cache and results the agents use, so the
page can never disagree with reports/: regime monitors with a year of history, BTC vs
its 200-day average, every hypothesis with its latest rows and equity curves, and the
freshness of each data series.
"""
import datetime as dt
import json
import logging
import math
import os
import shutil
from pathlib import Path

import numpy as np
import pandas as pd

from crl import __version__, registry
from crl.agents import regime_watch
from crl.config import ROOT, RESULTS_DIR
from crl.data.store import FEATURES, DataStore
from crl.engine import rules as R
from crl.engine.backtest import run, to_position
from crl.engine.protocol import MARK, _mask
from crl.i18n import LANGS

log = logging.getLogger(__name__)

SITE_DIR = Path(os.environ.get("CRL_SITE_DIR", ROOT / "_site"))
REPO_URL = "https://github.com/f1devbin/Crypto-Research-Labs"
ROW_FIELDS = ("symbol", "period", "selected", "sharpe", "hold_sharpe", "cagr", "hold_cagr", "max_dd",
              "hold_max_dd", "exposure", "trades_per_year", "p", "alpha", "beats_hold", "win", "start", "end")


def _num(v, nd=4):
    if v is None or (isinstance(v, float) and not math.isfinite(v)):
        return None
    return round(float(v), nd)


def _points(s: pd.Series, step: int = 1, nd: int = 4) -> dict:
    """{"d": [...dates], "v": [...values]} keeping every `step`-th point and the last one."""
    s = s.dropna()
    if step > 1 and len(s) > 1:
        idx = list(range(0, len(s) - 1, step)) + [len(s) - 1]
        s = s.iloc[idx]
    return {"d": [str(i.date()) for i in s.index], "v": [_num(x, nd) for x in s.to_numpy()]}


def regime(store: DataStore, monitors: dict, days: int = 365) -> list[dict]:
    current = regime_watch.evaluate(store, monitors)
    out = []
    for name, m in monitors.items():
        cur = current[name]
        item = {"id": name, "label": m["label"], "metric": m["metric"], "format": m.get("format", "{:.4f}"),
                "value": _num(cur["value"], 6), "band": cur["band"], "error": cur.get("error"),
                "bands": m["bands"], "explain": m.get("explain", ""), "note": m.get("notes", {}).get(cur["band"], ""), "history": None}
        try:
            s = regime_watch.series(store, m)
            item["history"] = _points(s[s.index > s.index[-1] - pd.Timedelta(days=days)], nd=6)
        except Exception as e:  # history is decoration; the current value is what matters
            log.warning("no history for %s: %s", name, e)
        out.append(item)
    return out


COIN_NAMES = {"BTCUSDT": "Bitcoin", "ETHUSDT": "Ethereum", "SOLUSDT": "Solana", "BNBUSDT": "BNB",
              "XRPUSDT": "XRP", "ADAUSDT": "Cardano", "LTCUSDT": "Litecoin", "LINKUSDT": "Chainlink",
              "DOGEUSDT": "Dogecoin", "XLMUSDT": "Stellar", "TRXUSDT": "TRON", "EVERUSDT": "Everscale",
              "GRAMUSDT": "Gram (ex-Toncoin)"}


def _chg(c: pd.Series, days: int):
    return _num(c.iloc[-1] / c.iloc[-1 - days] - 1, 6) if len(c) > days else None


def _rule_states(store: DataStore, hyps: list[dict], sym: str) -> list[dict]:
    """Today's position of each data-driven timing rule tested on `sym` (decided at the last close,
    so it applies to the next day). The 4 generic price rules are shown separately."""
    out = []
    for h in hyps:
        spec = h.get("spec") or {}
        rule = spec.get("rule") or {}
        if (h.get("replicates") or spec.get("kind") != "timing_rule" or sym not in spec.get("universe", [])
                or rule.get("type") not in set(R.FEATURE_RULES) | set(R.CROSS_RULES) | set(R.CALENDAR_RULES)):
            continue
        try:
            flag = R.build(rule, store, sym).dropna()
            state = float(flag.iloc[-1]) if len(flag) else None
            day = str(flag.index[-1].date()) if len(flag) else None
        except (FileNotFoundError, KeyError, ValueError):
            state, day = None, None
        out.append({"id": h["id"], "verdict": h["verdict"], "state": state, "date": day})
    rank = {"PASS": 0, "WEAK": 1, "FAIL": 2}
    return sorted(out, key=lambda r: (rank.get(r["verdict"], 3), r["id"]))  # proven rules first


def coins(store: DataStore, hyps: list[dict], days: int = 365) -> list[dict]:
    """Per-coin snapshot: price, changes, trend, volatility, 12-month chart and today's state of each
    tested rule. Rule states are descriptive only: none of these rules has passed its test."""
    from crl.data.sources import OTHER_EXCHANGES

    symbols = sorted({s for h in hyps for s in (h.get("spec") or {}).get("universe", [])} | {"BTCUSDT"},
                     key=lambda x: list(COIN_NAMES).index(x) if x in COIN_NAMES else 99)
    try:
        btc = store.close("BTCUSDT")
        btc_on = bool(btc.iloc[-1] > btc.rolling(200).mean().iloc[-1])
        btc_r = btc.pct_change()
    except (FileNotFoundError, KeyError):
        btc_on, btc_r = None, None
    out = []
    for sym in symbols:
        try:
            c = store.close(sym).dropna()
        except (FileNotFoundError, KeyError):  # source down or coin not cached yet
            continue
        sma50, sma200 = c.rolling(50).mean(), c.rolling(200).mean()
        vol = c.pct_change().rolling(30).std() * np.sqrt(365)
        last, v = float(c.iloc[-1]), _num(vol.iloc[-1], 6)
        peak_i = c.idxmax()
        r = c.pct_change()
        corr = None
        if btc_r is not None and sym != "BTCUSDT":
            j = pd.concat([r, btc_r], axis=1, join="inner").dropna().iloc[-90:]
            corr = _num(j.iloc[:, 0].corr(j.iloc[:, 1]), 4) if len(j) >= 60 else None
        recent = c.index > c.index[-1] - pd.Timedelta(days=days)
        out.append({
            "symbol": sym, "ticker": sym.removesuffix("USDT"), "name": COIN_NAMES.get(sym, sym),
            "exchange": "Gate.io" if sym in OTHER_EXCHANGES else "Binance",
            "date": str(c.index[-1].date()), "price": last,
            "ch7": _chg(c, 7), "ch30": _chg(c, 30), "ch365": _chg(c, 365),
            "vs50": _num(last / sma50.iloc[-1] - 1, 6) if sma50.notna().iloc[-1] else None,
            "vs200": _num(last / sma200.iloc[-1] - 1, 6) if sma200.notna().iloc[-1] else None,
            "vol": v,
            # distance from the highest close in our history (Binance since 2017, Gate.io since 2022)
            "dd_peak": _num(last / float(c.max()) - 1, 6), "peak": float(c.max()), "peak_date": str(peak_i.date()),
            "since": str(c.index[0].date()),
            "usd100": _num(100 * last / float(c.iloc[-366]), 2) if len(c) > 365 else None,
            "corr_btc": corr,
            "signals": {
                "sma50": None if pd.isna(sma50.iloc[-1]) else bool(last > sma50.iloc[-1]),
                "mom7": None if len(c) <= 7 else bool(last > c.iloc[-8]),
                "vol": None if not v else _num(min(1.0, 0.3 / v), 4),
                "btc": btc_on,
            },
            "rule_states": _rule_states(store, hyps, sym),
            "studies": [{"id": h["id"], "verdict": h["verdict"]} for h in hyps
                        if sym in (h.get("spec") or {}).get("universe", [])],
            "chart": {"close": _points(c[recent], nd=8), "sma50": _points(sma50[recent], nd=8),
                      "sma200": _points(sma200[recent], nd=8)},
        })
    return out


def diagnosis(reg: list[dict], coins_: list[dict]) -> dict | None:
    """Market diagnosis from the regime monitors and the coin table. Language-neutral: each item is
    a message key, a tone (+1 up, 0 neutral, -1 down) and raw values; site_render words it."""
    m = {x["id"]: x for x in reg if x.get("value") is not None and not x.get("error")}
    items = []

    def add(key, tone, **kw):
        items.append({"key": key, "tone": tone, **kw})

    if "btc_trend" in m:
        v = m["btc_trend"]["value"]
        add("d_trend_up" if v >= 0 else "d_trend_down", 1 if v >= 0 else -1, v=abs(v))
    with200 = [c for c in coins_ if c.get("vs200") is not None]
    if with200:
        k, n = sum(c["vs200"] > 0 for c in with200), len(with200)
        share = k / n
        band = "strong" if share >= 0.7 else ("weak" if share < 0.3 else "mixed")
        add(f"d_breadth_{band}", {"strong": 1, "weak": -1}.get(band, 0), k=k, n=n)
    if "btc_volatility" in m:
        b = m["btc_volatility"]["band"]
        add(f"d_vol_{b}", -1 if b == "stressed" else 0, v=m["btc_volatility"]["value"])
    if "fear_greed" in m:
        add("d_mood", 0, v=m["fear_greed"]["value"], band=m["fear_greed"]["band"])
    if "stablecoin_growth" in m:
        b = m["stablecoin_growth"]["band"]
        add(f"d_money_{b}", {"expanding": 1, "contracting": -1}.get(b, 0), v=abs(m["stablecoin_growth"]["value"]))
    if "h020_rule" in m:
        on = m["h020_rule"]["band"] == "rule_in"
        add("d_rule_in" if on else "d_rule_out", 1 if on else -1)
    if not items:
        return None
    # the long-term BTC trend counts double: it is what most tested rules follow. "up"/"down" needs a clear
    # majority of the non-neutral signals, e.g. 3 up, 0 down with the trend up -> score 4
    score = sum(i["tone"] for i in items) + next((i["tone"] for i in items if i["key"].startswith("d_trend")), 0)
    level = "up" if score >= 3 else ("down" if score <= -3 else "mixed")
    return {"level": level, "score": score, "items": items,
            "up": sum(i["tone"] > 0 for i in items), "down": sum(i["tone"] < 0 for i in items),
            "neutral": sum(i["tone"] == 0 for i in items)}


def progress(h: dict, today: dt.date) -> dict | None:
    """Forward-data counter for hypotheses that wait for new data (`test_after`)."""
    if not h.get("test_after") or h.get("verdict"):
        return None
    periods = (h.get("spec") or {}).get("periods") or []
    start = periods[0].get("start") if periods else None
    try:
        a, b = dt.date.fromisoformat(start or h.get("registered") or ""), dt.date.fromisoformat(h["test_after"])
    except ValueError:
        return None
    total = max((b - a).days, 1)
    done = min(max((today - a).days, 0), total)
    return {"done": done, "total": total, "share": round(done / total, 4), "date": h["test_after"]}


def scan_data() -> dict | None:
    from crl import scan
    res = scan.load()
    if not res:
        return None
    keep = ("rule", "symbol", "official", "status", "sharpe", "hold_sharpe", "cagr", "hold_cagr", "start", "p", "q")
    return {"generated_at": res.get("generated_at"), "start": res.get("start"), "fdr_q": res.get("fdr_q"),
            "coins": res.get("coins", []), "counts": res.get("counts", {}),
            "rules": [{"id": r["id"], "also": r.get("also", []), "tested_on": r.get("tested_on", [])}
                      for r in res.get("rules", [])],
            "cells": [{k: c.get(k) for k in keep if k in c} for c in res.get("cells", [])]}


def course_values(data: dict, lang: str, site: str) -> dict:
    """Live numbers for the course text, formatted for the language."""
    from crl.course import COMMA_DECIMAL
    from crl.i18n import t

    def loc(x: str) -> str:
        return x.replace(".", ",") if lang in COMMA_DECIMAL else x

    def pc(v, signed=True):
        return "—" if v is None else loc(f"{v:+.0%}" if signed else f"{v:.0%}")

    coins_by = {c["symbol"]: c for c in data.get("coins", [])}
    hyps = {h["id"]: h for h in data["hypotheses"]}

    def row(hid, sym):
        return next((r for r in hyps.get(hid, {}).get("rows", []) if r.get("symbol") == sym), {})

    n, n_pass = len(data["hypotheses"]), sum(h["verdict"] == "PASS" for h in data["hypotheses"])
    mom, ever = row("H-014", "SOLUSDT"), row("H-018", "EVERUSDT")
    vol = lambda s: pc(coins_by.get(s, {}).get("vol"), signed=False)
    return {
        "site": site, "update_utc": "03:00–07:00", "n_hyps": n, "n_coins": len(coins_by),
        "verdict_line": t(lang, "verdict_some", p=n_pass, n=n) if n_pass else t(lang, "verdict_none", n=n),
        "btc_vol": vol("BTCUSDT"), "sol_vol": vol("SOLUSDT"), "ever_vol": vol("EVERUSDT"),
        "sol_mom_sharpe": loc(f"{mom['sharpe']:.2f}") if mom.get("sharpe") is not None else "—",
        "sol_mom_hold": loc(f"{mom['hold_sharpe']:.2f}") if mom.get("hold_sharpe") is not None else "—",
        "sol_dd_peak": pc(coins_by.get("SOLUSDT", {}).get("dd_peak")),
        "sol_100": "—" if coins_by.get("SOLUSDT", {}).get("usd100") is None else f"${coins_by['SOLUSDT']['usd100']:,.0f}",
        "sol_corr": "—" if coins_by.get("SOLUSDT", {}).get("corr_btc") is None
                    else loc(f"{coins_by['SOLUSDT']['corr_btc']:.2f}"),
        "ever_rule_cagr": pc(ever.get("cagr")), "ever_hold_cagr": pc(ever.get("hold_cagr")),
        "ever_rule_dd": pc(ever.get("max_dd")), "ever_hold_dd": pc(ever.get("hold_max_dd")),
    }


def btc_chart(store: DataStore, since: str = "2020-01-01") -> dict | None:
    try:
        c = store.close("BTCUSDT")
    except FileNotFoundError:
        return None
    sma = c.rolling(200).mean()
    m = c.index >= pd.Timestamp(since)
    return {"close": _points(c[m], step=2, nd=2), "sma200": _points(sma[m], step=2, nd=2)}


def _rule_for(spec: dict, row: dict) -> tuple[dict, dict] | None:
    """(rule, period) that produced a result row."""
    if spec["kind"] == "rule_search":
        return spec["candidates"].get(row.get("selected")), spec["out_of_sample"]
    per = next((p for p in spec.get("periods", []) if p["name"] == row.get("period")), None)
    return spec["rule"], per


def equity_curves(spec: dict, rows: list[dict], store: DataStore, step: int = 5) -> list[dict]:
    """Strategy vs buy-and-hold growth of 1 for each result row, fees included."""
    out = []
    if spec.get("kind") == "cross_section":
        from crl.engine import cross as X
        try:
            closes = X.panel(store, spec["universe"])
            w = X.weights(spec, closes, store)
        except (FileNotFoundError, KeyError, ValueError) as e:
            log.warning("no cross-section curve: %s", e)
            return out
        for per in spec["periods"]:
            ev = X.evaluate_period(w, closes, _mask(closes.index, per.get("start"), per.get("end")), spec["fee"])
            if not ev["days"]:
                continue
            eq_s = pd.Series((1 + ev["_strat"]).cumprod(), index=ev["_idx"])
            eq_h = pd.Series((1 + ev["_bench"]).cumprod(), index=ev["_idx"])
            ps, ph = _points(eq_s, step), _points(eq_h, step)
            out.append({"symbol": "PORTFOLIO", "period": per["name"], "rule": None,
                        "d": ps["d"], "strategy": ps["v"], "hold": ph["v"]})
        return out
    for row in rows:
        rule, per = _rule_for(spec, row) or (None, None)
        if not rule or not per:
            continue
        try:
            close = store.close(row["symbol"])
            decision = to_position(R.build(rule, store, row["symbol"]), spec["mode"]).reindex(close.index)
        except (FileNotFoundError, KeyError, ValueError) as e:
            log.warning("no curve for %s/%s: %s", row["symbol"], row.get("period"), e)
            continue
        r = close.pct_change().fillna(0.0)
        strat, _ = run(decision.fillna(0.0), r, spec["fee"])
        m = _mask(close.index, per.get("start"), per.get("end")) & decision.shift(1).notna().to_numpy()
        if not m.any():
            continue
        eq_s, eq_h = (1 + strat[m]).cumprod(), (1 + r[m]).cumprod()
        pts_s, pts_h = _points(eq_s, step), _points(eq_h, step)
        out.append({"symbol": row["symbol"], "period": row.get("period"), "rule": row.get("selected"),
                    "d": pts_s["d"], "strategy": pts_s["v"], "hold": pts_h["v"]})
    return out


def hypotheses(store: DataStore, curves: bool = True) -> list[dict]:
    out = []
    for h in registry.load_all():
        res = registry.latest_result(h.id, RESULTS_DIR)
        hist = h.get("history") or []
        verdict = res["verdict"] if res else (hist[-1]["verdict"] if hist else None)
        item = {"id": h.id, "title": h["title"], "status": h["status"], "family": h["family"],
                "rationale": h.get("rationale", ""), "rerunnable": h.get("rerunnable", True),
                "verdict": verdict, "mark": MARK.get(verdict, ""),
                "summary": res["summary"] if res else (hist[-1].get("summary", "") if hist else ""),
                "run_at": res.get("run_at") if res else None, "data_end": res.get("data_end") if res else None,
                "source": "engine" if res else (hist[-1].get("source") if hist else None),
                "history": [{"date": x.get("date"), "verdict": x.get("verdict"), "source": x.get("source")}
                            for x in hist],
                "spec": h.get("spec"), "rows": [], "curves": [], "test_after": h.get("test_after"),
                "registered": h.get("registered"),
                "replicates": h.get("replicates")}
        if res:
            item["rows"] = [{k: (_num(r[k], 6) if isinstance(r.get(k), float) else r.get(k))
                             for k in ROW_FIELDS if k in r} for r in res["rows"]]
            if curves and h.get("spec"):
                item["curves"] = equity_curves(h["spec"], res["rows"], store)
        out.append(item)
    return out


def data_health(store: DataStore, today: dt.date) -> list[dict]:
    """Last available day per series: what the page is based on."""
    series = {}
    symbols = sorted({s for h in registry.load_all() for s in (h.get("spec") or {}).get("universe", [])}
                     | {"BTCUSDT"})
    for sym in symbols:
        series[sym] = lambda st, s=sym: st.close(s)
    series["funding BTCUSDT"] = lambda st: st.funding_daily("BTCUSDT")
    series["stablecoins USDT+USDC"] = lambda st: st.stablecoin_supply()
    series["fear & greed"] = lambda st: st.fear_greed()
    series["BTC ETF flows"] = lambda st: st.etf_flow()
    out = []
    for name, fn in series.items():
        try:
            s = fn(store).dropna()
            last = s.index[-1].date()
            out.append({"series": name, "first": str(s.index[0].date()), "last": str(last),
                        "lag_days": (today - last).days, "points": int(len(s))})
        except Exception as e:
            out.append({"series": name, "first": None, "last": None, "lag_days": None, "points": 0,
                        "error": f"{type(e).__name__}"})
    return out


SITE_URL = os.environ.get("CRL_SITE_URL", "https://f1devbin.github.io/Crypto-Research-Labs/").rstrip("/") + "/"
STATIC = ROOT / "site"


def _w(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def build(store: DataStore | None = None, out_dir: Path = SITE_DIR, now: dt.datetime | None = None,
          base: str = SITE_URL) -> Path:
    from crl import site_render as H
    store = store or DataStore()
    now = now or dt.datetime.now(dt.timezone.utc)
    verification = os.environ.get("GOOGLE_SITE_VERIFICATION", "").strip()
    data = {
        "generated_at": now.strftime("%Y-%m-%d %H:%M UTC"),
        "engine_version": __version__,
        "repo": REPO_URL,
        "site": base,
        "regime": regime(store, regime_watch.load_monitors()),
        "btc": btc_chart(store),
        "hypotheses": hypotheses(store),
        "data": data_health(store, now.date()),
    }
    data["coins"] = coins(store, data["hypotheses"])
    data["diagnosis"] = diagnosis(data["regime"], data["coins"])
    data["scan"] = scan_data()
    from crl.llm import digest as D
    data["digests"] = D.load()
    for h in data["hypotheses"]:
        h["progress"] = progress(h, now.date())
    if out_dir.exists():
        shutil.rmtree(out_dir)
    today = now.date().isoformat()
    entries = ([(None, today)] + [(h["id"], (h.get("run_at") or today)[:10]) for h in data["hypotheses"]]
               + [(f"coin:{c['symbol']}", c["date"]) for c in data["coins"]] + [("market", today), ("research", today),
                  ("about", today), ("course", today), ("setup", today),
                  ("digest", data["digests"][0]["date"] if data["digests"] else today)])
    pages = 0
    for lang in LANGS:
        for hid, _ in entries:
            path = out_dir / H.page_path(lang, hid)
            path.parent.mkdir(parents=True, exist_ok=True)
            if hid is None:
                html = H.index_page(lang, data, base, verification)
            elif hid in ("market", "research", "about"):
                html = getattr(H, f"{hid}_page")(lang, data, base, verification)
            elif hid == "digest":
                html = H.digest_page(lang, data, base, verification)
            elif hid == "setup":
                html = H.setup_page(lang, data, base, verification)
            elif hid == "course":
                html = H.course_page(lang, course_values(data, lang, "./"), data, base, verification)
            elif hid.startswith("coin:"):
                coin = next(x for x in data["coins"] if x["symbol"] == hid[5:])
                html = H.coin_page(lang, coin, data, base, verification)
            else:
                html = H.hypothesis_page(lang, next(x for x in data["hypotheses"] if x["id"] == hid), data, base,
                                         verification)
            _w(path, html)
            pages += 1
    _w(out_dir / "sitemap.xml", H.sitemap(base, entries))
    _w(out_dir / "robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {base}sitemap.xml\n")
    _w(out_dir / "charts.js", H.CHART_SCRIPT)
    _w(out_dir / "sort.js", H.SORT_SCRIPT)
    _w(out_dir / "ui.js", H.UI_SCRIPT)
    _w(out_dir / "favicon.svg", H.FAVICON)
    _w(out_dir / "404.html", H.NOT_FOUND)
    _w(out_dir / ".nojekyll", "")
    for f in STATIC.iterdir():  # og.png, search-engine verification files, ...
        if not f.is_file():
            continue
        shutil.copyfile(f, out_dir / f.name)
    _w(out_dir / "data.json", json.dumps(data, separators=(",", ":"), allow_nan=False, default=str))
    log.info("site: %d pages, data.json %d KB -> %s", pages, (out_dir / "data.json").stat().st_size // 1024,
             out_dir)
    return out_dir


def main() -> int:
    build()
    return 0

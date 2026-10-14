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
                "spec": h.get("spec"), "rows": [], "curves": []}
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
    if out_dir.exists():
        shutil.rmtree(out_dir)
    today = now.date().isoformat()
    entries = [(None, today)] + [(h["id"], (h.get("run_at") or today)[:10]) for h in data["hypotheses"]]
    pages = 0
    for lang in LANGS:
        for hid, _ in entries:
            path = out_dir / H.page_path(lang, hid)
            path.parent.mkdir(parents=True, exist_ok=True)
            h = next((x for x in data["hypotheses"] if x["id"] == hid), None)
            _w(path, H.hypothesis_page(lang, h, data, base, verification) if hid
                            else H.index_page(lang, data, base, verification))
            pages += 1
    _w(out_dir / "sitemap.xml", H.sitemap(base, entries))
    _w(out_dir / "robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {base}sitemap.xml\n")
    _w(out_dir / "charts.js", H.CHART_SCRIPT)
    _w(out_dir / "favicon.svg", H.FAVICON)
    _w(out_dir / "404.html", H.NOT_FOUND)
    _w(out_dir / ".nojekyll", "")
    for f in STATIC.glob("*.png"):
        shutil.copyfile(f, out_dir / f.name)
    _w(out_dir / "data.json", json.dumps(data, separators=(",", ":"), allow_nan=False, default=str))
    log.info("site: %d pages, data.json %d KB -> %s", pages, (out_dir / "data.json").stat().st_size // 1024,
             out_dir)
    return out_dir


def main() -> int:
    build()
    return 0

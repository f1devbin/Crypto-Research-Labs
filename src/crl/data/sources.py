"""Fetchers for public data sources. Every fetch is incremental: files already on disk are kept.

Layout under DATA_DIR:
  klines/1d/<SYMBOL>/<SYMBOL>-1d-YYYY-MM[-DD].zip   Binance spot daily candles (data.binance.vision)
  funding/<SYMBOL>/<SYMBOL>-fundingRate-YYYY-MM.zip Binance USD-M funding archives
  funding/<SYMBOL>/recent.json                      last ~1000 funding prints (API, with fallbacks)
  external/<name>.json                              DefiLlama stablecoins, Fear & Greed, ETF flows
"""
import datetime as dt
import json
import logging
import os
import time
from dataclasses import dataclass, field
from pathlib import Path

from crl.config import DATA_DIR
from crl.data.http import get

log = logging.getLogger(__name__)

VISION = "https://data.binance.vision/data"

EXTERNAL = {
    # name: (url, max_age_hours)
    "stable_usdt": ("https://stablecoins.llama.fi/stablecoincharts/all?stablecoin=1", 12),
    "stable_usdc": ("https://stablecoins.llama.fi/stablecoincharts/all?stablecoin=2", 12),
    "fear_greed": ("https://api.alternative.me/fng/?limit=0&format=json", 12),
    # BGeometrics: 8 requests/hour, 15/day on the free tier — cache for a day
    "etf_flow_btc": ("https://bitcoin-data.com/v1/etf-flow-btc", 24),
}


@dataclass
class FetchReport:
    name: str
    files_ok: int = 0
    files_missing: int = 0
    errors: list = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors and self.files_ok > 0


def _write_atomic(path: Path, body: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".part")
    tmp.write_bytes(body)
    os.replace(tmp, path)


def _next_month(d: dt.date) -> dt.date:
    return dt.date(d.year + (d.month == 12), d.month % 12 + 1, 1)


def _download(url: str, dest: Path) -> str:
    """'ok' — file present; '404' — not on server; 'err' — network failure."""
    if dest.exists() and dest.stat().st_size > 0:
        return "ok"
    res = get(url)
    if res.ok:
        _write_atomic(dest, res.body)
        return "ok"
    return "404" if res.status == 404 else "err"


def fetch_daily_klines(symbol: str, start: dt.date = dt.date(2017, 8, 1),
                       root: Path = DATA_DIR) -> FetchReport:
    """Monthly archives; the last ~2 months (not yet archived) are filled with daily files."""
    rep = FetchReport(f"klines {symbol}")
    today = dt.datetime.now(dt.timezone.utc).date()
    last = today - dt.timedelta(days=1)
    recent = (last.replace(day=1) - dt.timedelta(days=1)).replace(day=1)
    base = root / "klines" / "1d" / symbol
    m, listed = start, False
    while m <= last:
        p = m.strftime("%Y-%m")
        st = _download(f"{VISION}/spot/monthly/klines/{symbol}/1d/{symbol}-1d-{p}.zip",
                       base / f"{symbol}-1d-{p}.zip")
        if st == "ok":
            rep.files_ok += 1
            listed = True
        elif m >= recent:
            d = m
            while d < _next_month(m) and d <= last:
                ds = d.isoformat()
                if _download(f"{VISION}/spot/daily/klines/{symbol}/1d/{symbol}-1d-{ds}.zip",
                             base / f"{symbol}-1d-{ds}.zip") == "ok":
                    rep.files_ok += 1
                else:
                    rep.files_missing += 1
                d += dt.timedelta(days=1)
        elif st == "err":
            rep.errors.append(f"network error for {p}")
        elif listed:
            rep.files_missing += 1  # a hole in the middle of history
        m = _next_month(m)
    # the newest daily file is often published a few hours late — not an error
    if rep.files_missing <= 2:
        rep.files_missing = 0
    return rep


def fetch_funding(symbol: str = "BTCUSDT", start: dt.date = dt.date(2020, 1, 1),
                  root: Path = DATA_DIR) -> FetchReport:
    """Monthly funding archives plus the latest prints from a live API.

    fapi.binance.com answers HTTP 451 from US IPs (including GitHub-hosted runners),
    so OKX (same 8-hour funding interval) is tried as a fallback for the recent window.
    """
    rep = FetchReport(f"funding {symbol}")
    base = root / "funding" / symbol
    today = dt.datetime.now(dt.timezone.utc).date()
    m = start
    while m < today.replace(day=1):
        p = m.strftime("%Y-%m")
        st = _download(f"{VISION}/futures/um/monthly/fundingRate/{symbol}/{symbol}-fundingRate-{p}.zip",
                       base / f"{symbol}-fundingRate-{p}.zip")
        if st == "ok":
            rep.files_ok += 1
        elif st == "err":
            rep.errors.append(f"network error for {p}")
        m = _next_month(m)

    recent = base / "recent.json"
    if recent.exists() and time.time() - recent.stat().st_mtime < 6 * 3600:
        return rep
    rows = _recent_funding(symbol)
    if rows:
        _write_atomic(recent, json.dumps(rows).encode())
    else:
        rep.errors.append("no live source for recent funding (Binance/OKX)")
    return rep


def _recent_funding(symbol: str) -> list:
    """List of {"t": unix_ms, "rate": float} from the first source that answers."""
    res = get(f"https://fapi.binance.com/fapi/v1/fundingRate?symbol={symbol}&limit=1000")
    if res.ok:
        return [{"t": int(x["fundingTime"]), "rate": float(x["fundingRate"])} for x in json.loads(res.body)]
    coin = symbol.removesuffix("USDT")
    res = get(f"https://www.okx.com/api/v5/public/funding-rate-history?instId={coin}-USDT-SWAP&limit=100")
    if res.ok:
        data = json.loads(res.body).get("data", [])
        if data:
            return [{"t": int(x["fundingTime"]), "rate": float(x["realizedRate"] or x["fundingRate"])}
                    for x in data]
    log.warning("Binance and OKX funding unavailable for %s", symbol)
    return []


def fetch_external(name: str, root: Path = DATA_DIR) -> FetchReport:
    rep = FetchReport(name)
    url, max_age = EXTERNAL[name]
    path = root / "external" / f"{name}.json"
    if path.exists() and time.time() - path.stat().st_mtime < max_age * 3600:
        rep.files_ok = 1
        return rep
    res = get(url)
    try:
        json.loads(res.body)
    except ValueError:
        if path.exists():
            rep.files_ok = 1  # keep serving the stale copy, integrity check reports staleness
            log.warning("%s: HTTP %s, using cached copy", name, res.status)
        else:
            rep.errors.append(f"HTTP {res.status}, not JSON")
        return rep
    _write_atomic(path, res.body)
    rep.files_ok = 1
    return rep

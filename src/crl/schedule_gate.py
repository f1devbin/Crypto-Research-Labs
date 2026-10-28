"""Decides whether a scheduled research-agents run should do the work, and which kind.

GitHub starts scheduled workflows hours late and unpredictably, so the workflow is scheduled every
hour of the morning and this gate lets the first run that finds yesterday's data published at every
source do the job; the rest exit in seconds. On Mondays the first ready run is the weekly (full) one.
Standard library only: it runs before the project's dependencies are installed.

Usage in the workflow: python -m crl.schedule_gate  -> writes go=true|false, full=true|false to $GITHUB_OUTPUT
"""
import datetime as dt
import json
import os
import subprocess
import sys
import urllib.request

SITE = os.environ.get("CRL_SITE_URL") or "https://f1devbin.github.io/Crypto-Research-Labs/"
LAST_HOUR = 11  # the 11:17 UTC slot runs even if a source is still late, so the site is never skipped for a day
UA = {"User-Agent": "crl-schedule-gate"}


def _get(url: str, method: str = "GET") -> tuple[int, bytes]:
    req = urllib.request.Request(url, headers=UA, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read() if method == "GET" else b""
    except Exception:
        return 0, b""


def binance_ready(day: dt.date) -> bool:
    url = (f"https://data.binance.vision/data/spot/daily/klines/BTCUSDT/1d/"
           f"BTCUSDT-1d-{day.isoformat()}.zip")
    return _get(url, "HEAD")[0] == 200


def coinmetrics_ready(day: dt.date) -> bool:
    st, body = _get("https://community-api.coinmetrics.io/v4/timeseries/asset-metrics?assets=btc"
                    "&metrics=FlowInExNtv&frequency=1d&page_size=1&paging_from=end")
    try:
        return st == 200 and json.loads(body)["data"][-1]["time"][:10] >= day.isoformat()
    except (ValueError, KeyError, IndexError):
        return False


def fear_greed_ready(today: dt.date) -> bool:
    st, body = _get("https://api.alternative.me/fng/?limit=1")
    try:
        ts = int(json.loads(body)["data"][0]["timestamp"])
        return st == 200 and dt.datetime.fromtimestamp(ts, dt.timezone.utc).date() >= today
    except (ValueError, KeyError, IndexError):
        return False


def stablecoins_ready(today: dt.date) -> bool:
    st, body = _get("https://stablecoins.llama.fi/stablecoincharts/all?stablecoin=1")
    try:
        ts = int(json.loads(body)[-1]["date"])
        return st == 200 and dt.datetime.fromtimestamp(ts, dt.timezone.utc).date() >= today
    except (ValueError, KeyError, IndexError):
        return False


def missing_sources(today: dt.date) -> list[str]:
    """Sources that have not yet published the data for yesterday (UTC)."""
    y = today - dt.timedelta(days=1)
    checks = {"binance": lambda: binance_ready(y), "coinmetrics": lambda: coinmetrics_ready(y),
              "fear_greed": lambda: fear_greed_ready(today), "stablecoins": lambda: stablecoins_ready(today)}
    return [name for name, ok in checks.items() if not ok()]


def site_built_on(today: dt.date) -> bool:
    st, body = _get(SITE.rstrip("/") + "/data.json")
    try:
        return st == 200 and json.loads(body)["generated_at"][:10] == today.isoformat()
    except (ValueError, KeyError):
        return False


def weekly_done_on(today: dt.date) -> bool:
    out = subprocess.run(["git", "log", "-20", "--format=%s"], capture_output=True, text=True).stdout
    return f"chore(results): scheduled run {today.isoformat()}" in out


def decide(now: dt.datetime, *, missing: list[str], site_today: bool, weekly_today: bool) -> tuple[bool, bool, str]:
    """(go, full, reason) for a scheduled run."""
    monday = now.weekday() == 0
    if monday and not weekly_today:
        full = True
    elif not site_today:
        full = False
    else:
        return False, False, "already done today"
    if missing and now.hour < LAST_HOUR:
        return False, full, "waiting for " + ", ".join(missing)
    return True, full, ("weekly" if full else "daily") + (f" (late sources: {', '.join(missing)})" if missing else "")


def main() -> int:
    now = dt.datetime.now(dt.timezone.utc)
    event = os.environ.get("GITHUB_EVENT_NAME", "schedule")
    if event != "schedule":
        go, full, reason = True, os.environ.get("FULL_INPUT") == "true", f"{event} run"
    else:
        today = now.date()
        site_today, weekly_today = site_built_on(today), weekly_done_on(today)
        need = (now.weekday() == 0 and not weekly_today) or not site_today
        go, full, reason = decide(now, missing=missing_sources(today) if need else [],
                                  site_today=site_today, weekly_today=weekly_today)
    print(f"go={go} full={full}: {reason}")
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a") as f:
            f.write(f"go={str(go).lower()}\nfull={str(full).lower()}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())

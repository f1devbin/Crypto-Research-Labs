"""Decides whether a scheduled research-agents run should do the work, and which kind.

GitHub starts scheduled workflows hours late and unpredictably, so the workflow is scheduled every
hour of the morning and this gate lets the first run that finds yesterday's data published at every
source do the job; the rest exit in seconds. The day's job is done once today's forecast is in the committed
log and the site was built today: a rebuild after a merge (a push run) does not count, and push runs never
publish a forecast. On Mondays the first ready run is the weekly (full) one; so is the next run after a
missed weekly digest. Standard library only: it runs before the project's dependencies are installed.

Usage in the workflow: python -m crl.schedule_gate  -> writes go=true|false, full=true|false to $GITHUB_OUTPUT
"""
import csv
import datetime as dt
import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

SITE = os.environ.get("CRL_SITE_URL") or "https://f1devbin.github.io/Crypto-Research-Labs/"
LAST_HOUR = 11  # the 11:17 UTC slot runs even if a source is still late, so the site is never skipped for a day
UA = {"User-Agent": "crl-schedule-gate"}
FORECAST_LOG = Path("datasets/forecast_log.csv")  # paths in the checkout the gate runs from
DIGEST_DIR = Path("reports/digest")


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


def forecast_logged_on(today: dt.date, log: Path = FORECAST_LOG) -> bool:
    """Today's forecast is in the committed log (it is published before 12:00 UTC, once a day)."""
    try:
        with log.open(newline="") as f:
            return any(row.get("date") == today.isoformat() for row in csv.DictReader(f))
    except OSError:
        return False


def digest_missed(today: dt.date, root: Path = DIGEST_DIR) -> bool:
    """Weekly digests exist, but none was written in the last 7 days: the next run catches up."""
    dates = []
    for meta in root.glob("*/meta.json"):
        try:
            dates.append(dt.date.fromisoformat(json.loads(meta.read_text(encoding="utf-8"))["date"]))
        except (OSError, ValueError, KeyError):
            continue
    return bool(dates) and (today - max(dates)).days > 7


def weekly_done_on(today: dt.date) -> bool:
    out = subprocess.run(["git", "log", "-20", "--format=%s"], capture_output=True, text=True).stdout
    return f"chore(results): scheduled run {today.isoformat()}" in out


def decide(now: dt.datetime, *, missing: list[str], daily_today: bool, weekly_today: bool,
           digest_late: bool = False) -> tuple[bool, bool, str]:
    """(go, full, reason) for a scheduled run."""
    monday = now.weekday() == 0
    if (monday or digest_late) and not weekly_today:
        full = True
    elif not daily_today:
        full = False
    else:
        return False, False, "already done today"
    if missing and now.hour < LAST_HOUR:
        return False, full, "waiting for " + ", ".join(missing)
    kind = ("weekly" if monday else "weekly (catch-up: the last digest is over a week old)") if full else "daily"
    return True, full, kind + (f" (late sources: {', '.join(missing)})" if missing else "")


def main() -> int:
    now = dt.datetime.now(dt.timezone.utc)
    event = os.environ.get("GITHUB_EVENT_NAME", "schedule")
    if event != "schedule":
        go, full, reason = True, os.environ.get("FULL_INPUT") == "true", f"{event} run"
    else:
        today = now.date()
        # after 12:00 UTC no forecast can be published any more, so a site built today is enough
        daily_today = site_built_on(today) and (forecast_logged_on(today) or now.hour >= 12)
        weekly_today, late = weekly_done_on(today), digest_missed(today)
        need = ((now.weekday() == 0 or late) and not weekly_today) or not daily_today
        go, full, reason = decide(now, missing=missing_sources(today) if need else [],
                                  daily_today=daily_today, weekly_today=weekly_today, digest_late=late)
    print(f"go={go} full={full}: {reason}")
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a") as f:
            f.write(f"go={str(go).lower()}\nfull={str(full).lower()}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())

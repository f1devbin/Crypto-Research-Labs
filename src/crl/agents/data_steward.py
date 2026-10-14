"""Data steward: keeps the shared cache fresh and refuses to let studies run on broken data.

Fixes: every F1MEBOT study re-downloaded its own copy of the data, and nothing
checked gaps, duplicates or staleness before a backtest ran.
"""
import datetime as dt
import logging
from pathlib import Path

import pandas as pd

from crl import registry
from crl.config import DATA_DIR, REPORTS_DIR
from crl.data import sources
from crl.data.integrity import Finding, check_series
from crl.data.store import DataStore
from crl.notify import alert

log = logging.getLogger(__name__)

FEATURE_SOURCES = {
    "stablecoin_growth_7d": [("external", "stable_usdt"), ("external", "stable_usdc")],
    "funding_btc_7d": [("funding", "BTCUSDT")],
    "fear_greed": [("external", "fear_greed")],
    "etf_flow_btc_5d": [("external", "etf_flow_btc")],
    "exnetflow_btc_7d": [("exflows", "coinmetrics")],
    "exnetflow_eth_7d": [("exflows", "coinmetrics")],
}
FEATURE_MAX_STALE = {"etf_flow_btc_5d": 6, "funding_btc_7d": 3, "exnetflow_btc_7d": 4, "exnetflow_eth_7d": 4}
WATCH_SYMBOLS = ["BTCUSDT"]
# always collected, even before any hypothesis uses them (exchange flows can't be backfilled later)
WATCH_FEATURES = ["stablecoin_growth_7d", "funding_btc_7d", "fear_greed", "exnetflow_btc_7d", "exnetflow_eth_7d"]


def required_inputs(hyps: list) -> tuple[set, set]:
    symbols, features = set(WATCH_SYMBOLS), set(WATCH_FEATURES)
    for h in hyps:
        spec = h.get("spec") or {}
        if not h.get("rerunnable", True) or h.get("status") == "archived":
            continue
        symbols.update(spec.get("universe", []))
        rules = [spec.get("rule")] + list((spec.get("candidates") or {}).values())
        features.update(r["feature"] for r in rules if isinstance(r, dict) and "feature" in r)
        symbols.update(r["asset"] for r in rules if isinstance(r, dict) and "asset" in r)
    return symbols, features


def refresh(root: Path = DATA_DIR, today: dt.date | None = None) -> tuple[list, list[Finding]]:
    today = today or dt.datetime.now(dt.timezone.utc).date()
    symbols, features = required_inputs(registry.load_all())
    reports = [sources.fetch_daily_klines(s, root=root) for s in sorted(symbols)]
    done = set()
    for f in sorted(features):
        for kind, name in FEATURE_SOURCES[f]:
            if (kind, name) in done:
                continue
            done.add((kind, name))
            if kind == "funding":
                reports.append(sources.fetch_funding(name, root=root))
            elif kind == "exflows":
                reports.append(sources.fetch_exchange_flows())
            else:
                reports.append(sources.fetch_external(name, root=root))

    store = DataStore(root)
    now = pd.Timestamp(today)
    findings: list[Finding] = []
    for s in sorted(symbols):
        try:
            findings += check_series(s, store.close(s), now, is_price=True)
        except FileNotFoundError as e:
            findings.append(Finding(s, "error", str(e)))
    for f in sorted(features):
        try:
            findings += [Finding(x.series, "warn", x.message)  # feature problems never block price studies
                         for x in check_series(f, store.feature(f), now,
                                               max_stale=FEATURE_MAX_STALE.get(f, 3))]
        except (FileNotFoundError, KeyError, ValueError) as e:
            findings.append(Finding(f, "warn", f"cannot load: {e}"))
    return reports, findings


def write_report(reports, findings, path: Path = REPORTS_DIR / "data_health.md") -> str:
    lines = ["# Data health", "", f"Checked {dt.datetime.now(dt.timezone.utc):%Y-%m-%d %H:%M} UTC", "",
             "| source | files | missing | errors |", "|---|---|---|---|"]
    for r in reports:
        lines.append(f"| {r.name} | {r.files_ok} | {r.files_missing} | {'; '.join(r.errors) or '—'} |")
    lines += ["", "## Findings", ""]
    lines += [f"- **{f.level}** `{f.series}`: {f.message}" for f in findings] or ["- none"]
    md = "\n".join(lines) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(md)
    return md


def main() -> int:
    reports, findings = refresh()
    write_report(reports, findings)
    # price data is mandatory; external feature sources are best-effort (reported, not fatal)
    errors = [f for f in findings if f.level == "error"] + \
             [f"{r.name}: {e}" for r in reports if r.name.startswith("klines") for e in r.errors]
    if errors:
        alert("data steward: problems", [str(e) if isinstance(e, str) else f"{e.series}: {e.message}"
                                         for e in errors])
        return 1
    log.info("data OK: %d sources, %d warnings", len(reports), len(findings))
    return 0

"""Regime watch: tracks the market conditions that killed past ideas and alerts when they change.

Fixes: F1MEBOT measured funding-carry yield once (≈1.5 %/yr, not worth the risk) and
stopped looking. If carry returned to 2021 levels (≈15 %/yr) nobody would know.
Each monitor maps a live metric to a band; an alert fires only when the band changes,
so the channel stays quiet unless something actually moved.
"""
import datetime as dt
import json
import logging
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from crl.config import CONFIG_DIR, REPORTS_DIR, STATE_DIR
from crl.data.store import DataStore
from crl.notify import alert

log = logging.getLogger(__name__)


def _funding_carry(store: DataStore, p: dict) -> float:
    """Annualised yield on capital of spot-long / perp-short, no leverage (half the capital
    on each leg), after one round trip amortised over a year."""
    f = store.funding_daily(p.get("symbol", "BTCUSDT")).dropna()
    window = f[f.index > f.index[-1] - pd.Timedelta(days=int(p.get("days", 30)))]
    annual = float(window.mean() * 3 * 365)  # 3 prints a day
    return (annual - float(p.get("round_trip_cost", 0.003))) / 2


def _stablecoin_growth(store: DataStore, p: dict) -> float:
    s = store.stablecoin_supply().dropna()
    days = int(p.get("days", 30))
    return float(s.iloc[-1] / s.iloc[-1 - days] - 1)


def _fear_greed(store: DataStore, p: dict) -> float:
    return float(store.fear_greed().dropna().iloc[-1])


def _price_vs_sma(store: DataStore, p: dict) -> float:
    c = store.close(p.get("symbol", "BTCUSDT"))
    return float(c.iloc[-1] / c.rolling(int(p.get("window", 200))).mean().iloc[-1] - 1)


def _realized_vol(store: DataStore, p: dict) -> float:
    r = store.close(p.get("symbol", "BTCUSDT")).pct_change().dropna()
    return float(r.iloc[-int(p.get("days", 30)):].std() * np.sqrt(365))


METRICS = {
    "funding_carry": _funding_carry,
    "stablecoin_growth": _stablecoin_growth,
    "fear_greed": _fear_greed,
    "price_vs_sma": _price_vs_sma,
    "realized_vol": _realized_vol,
}


def band(value: float, bands: dict) -> str:
    """bands: {name: [low, high)}; null bounds are open-ended. First match wins."""
    for name, (lo, hi) in bands.items():
        if (lo is None or value >= lo) and (hi is None or value < hi):
            return name
    return "unknown"


def evaluate(store: DataStore, monitors: dict) -> dict:
    out = {}
    for name, m in monitors.items():
        try:
            v = METRICS[m["metric"]](store, m.get("params", {}))
            out[name] = {"value": v, "band": band(v, m["bands"])}
        except Exception as e:  # one broken source must not hide the other monitors
            out[name] = {"value": None, "band": "unavailable", "error": f"{type(e).__name__}: {e}"}
    return out


def transitions(current: dict, previous: dict, monitors: dict) -> list[str]:
    msgs = []
    for name, cur in current.items():
        old = previous.get(name, {}).get("band")
        if cur["band"] in ("unavailable",) or old is None or old == cur["band"]:
            continue
        m = monitors[name]
        fmt = m.get("format", "{:.4f}")
        note = m.get("notes", {}).get(cur["band"], "")
        msgs.append(f"{m['label']}: {old} → {cur['band']} ({fmt.format(cur['value'])}). {note}".strip())
    return msgs


def main(config: Path = CONFIG_DIR / "watch.yaml", state_path: Path = STATE_DIR / "watch_state.json") -> int:
    monitors = yaml.safe_load(config.read_text())["monitors"]
    current = evaluate(DataStore(), monitors)
    previous = json.loads(state_path.read_text()) if state_path.exists() else {}
    msgs = transitions(current, previous, monitors)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(current, indent=1))

    lines = ["# Regime watch", "", f"Updated {dt.datetime.now(dt.timezone.utc):%Y-%m-%d %H:%M} UTC", "",
             "| monitor | value | band |", "|---|---|---|"]
    for name, cur in current.items():
        m = monitors[name]
        v = "—" if cur["value"] is None else m.get("format", "{:.4f}").format(cur["value"])
        lines.append(f"| {m['label']} | {v} | {cur['band']}{' — ' + cur['error'] if 'error' in cur else ''} |")
    (REPORTS_DIR / "regime.md").parent.mkdir(parents=True, exist_ok=True)
    (REPORTS_DIR / "regime.md").write_text("\n".join(lines) + "\n")

    if msgs:
        alert("regime change", msgs)
    log.info("%d monitors, %d transitions", len(current), len(msgs))
    return 0

"""Coverage scan: every distinct timing rule that has been tested, applied to every coin.

A hypothesis is tested on the coins it names. Whether the same rule works on the other coins is
a separate question, and answering it by looking at many coin x rule pairs is exactly how chance
"discoveries" are made. So this scan is exploratory by design:

* one common window (2022-01-01 onwards, or from the first day a coin has data), fees included;
* a significance test per cell (circular shift; permutation for calendar rules);
* Benjamini-Hochberg false-discovery control over the whole matrix (q = 0.10);
* a cell that survives is only a *candidate*: to become a verdict it must be pre-registered as a
  new hypothesis and tested on data collected after registration (`test_after`).

Output: reports/coverage.json (read by the dashboard) and reports/COVERAGE.md.
"""
import datetime as dt
import json
import logging
from pathlib import Path

import numpy as np

from crl import __version__, registry
from crl.config import ROOT
from crl.data.store import DataStore
from crl.engine import rules as R
from crl.engine.backtest import evaluate_period, to_position
from crl.engine.protocol import _mask
from crl.engine.stats import circular_shift_p, permutation_p

log = logging.getLogger(__name__)

OUT_JSON = ROOT / "reports" / "coverage.json"
OUT_MD = ROOT / "reports" / "COVERAGE.md"
START = "2022-01-01"
MIN_DAYS = 365
FDR_Q = 0.10
CALENDAR = {"day_of_week", "turn_of_month"}
STATUSES = ("works", "better", "worse", "nodata")


def coin_list() -> list[str]:
    from crl.site import COIN_NAMES
    return list(COIN_NAMES)


def coin_fee(sym: str) -> float:
    from crl.data.sources import OTHER_EXCHANGES
    return 0.002 if sym in OTHER_EXCHANGES else 0.001


def distinct_rules(hyps) -> list[dict]:
    """One entry per distinct (rule, mode) among timing_rule hypotheses, labelled by the first
    hypothesis that tested it; replications are folded into the original."""
    seen: dict[str, dict] = {}
    for h in hyps:
        spec = h.get("spec") or {}
        if spec.get("kind") != "timing_rule":
            continue
        key = json.dumps([spec["rule"], spec.get("mode", "long_flat")], sort_keys=True)
        if key not in seen:
            seen[key] = {"id": h.id, "rule": spec["rule"], "mode": spec.get("mode", "long_flat"),
                         "also": [], "tested_on": set()}
        else:
            seen[key]["also"].append(h.id)
        seen[key]["tested_on"].update(spec.get("universe", []))
    out = list(seen.values())
    for r in out:
        r["tested_on"] = sorted(r["tested_on"])
    return out


def bh_qvalues(p: list[float]) -> list[float]:
    """Benjamini-Hochberg adjusted p-values (q-values), same order as the input."""
    n = len(p)
    if not n:
        return []
    order = np.argsort(p)
    ranked = np.asarray(p, dtype=float)[order] * n / np.arange(1, n + 1)
    q = np.minimum.accumulate(ranked[::-1])[::-1].clip(max=1.0)
    out = np.empty(n)
    out[order] = q
    return out.tolist()


def run(store: DataStore | None = None, n: int = 500, seed: int = 2026) -> dict:
    store = store or DataStore()
    rng = np.random.default_rng(seed)
    rules = distinct_rules(registry.load_all())
    cells = []
    for rd in rules:
        method = "permutation" if rd["rule"]["type"] in CALENDAR else "circular_shift"
        for sym in coin_list():
            cell = {"rule": rd["id"], "symbol": sym, "official": sym in rd["tested_on"], "status": "nodata"}
            try:
                close = store.close(sym)
                decision = to_position(R.build(rd["rule"], store, sym), rd["mode"])
            except (FileNotFoundError, KeyError, ValueError) as e:
                cell["error"] = type(e).__name__
                cells.append(cell)
                continue
            fee = coin_fee(sym)
            ev = evaluate_period(decision, close, _mask(close.index, START), fee)
            if ev["days"] < MIN_DAYS:
                cell["days"] = ev["days"]
                cells.append(cell)
                continue
            fn = permutation_p if method == "permutation" else circular_shift_p
            p = fn(ev["_pos"], ev["_r"], fee, rng, n)
            cell.update({k: (round(v, 6) if isinstance(v, float) else v) for k, v in ev.items()
                         if not k.startswith("_")})
            cell.update(p=round(float(p), 6), fee=fee, beats=bool(ev["sharpe"] > ev["hold_sharpe"]))
            cells.append(cell)
    tested = [c for c in cells if "p" in c]
    for c, q in zip(tested, bh_qvalues([c["p"] for c in tested])):
        c["q"] = round(q, 6)
        c["status"] = "works" if c["beats"] and q <= FDR_Q else ("better" if c["beats"] else "worse")
    return {
        "generated_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "engine_version": __version__, "start": START, "fdr_q": FDR_Q, "n_shuffles": n,
        "rules": [{k: v for k, v in r.items()} for r in rules],
        "coins": coin_list(), "cells": cells,
        "counts": {s: sum(c["status"] == s for c in cells) for s in STATUSES},
    }


MARKS = {"works": "✅", "better": "↑", "worse": "✗", "nodata": "—"}


def to_markdown(res: dict) -> str:
    coins = res["coins"]
    by = {(c["rule"], c["symbol"]): c for c in res["cells"]}
    head = "| Rule | " + " | ".join(s.removesuffix("USDT") for s in coins) + " |"
    lines = [
        "# Coverage scan: every tested rule on every coin",
        "",
        f"Generated {res['generated_at']} · window {res['start']} → latest · fees included · "
        f"Benjamini-Hochberg FDR q = {res['fdr_q']} over {sum('p' in c for c in res['cells'])} cells.",
        "",
        "Exploratory, not verdicts. ✅ beats buy-and-hold and survives the false-discovery control; "
        "↑ better Sharpe than holding but could be chance; ✗ worse than holding; — not enough data. "
        "**Bold** = the coin was in the original hypothesis. A ✅ on a new coin is a candidate for a new "
        "pre-registered hypothesis tested on future data.",
        "",
        head, "|" + "---|" * (len(coins) + 1),
    ]
    for r in res["rules"]:
        marks = []
        for s in coins:
            c = by.get((r["id"], s), {"status": "nodata", "official": False})
            m = MARKS[c["status"]]
            marks.append(f"**{m}**" if c.get("official") else m)
        lines.append(f"| {r['id']} | " + " | ".join(marks) + " |")
    lines += ["", "Counts: " + ", ".join(f"{k} {v}" for k, v in res["counts"].items()), ""]
    return "\n".join(lines)


def main() -> int:
    res = run()
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(res, indent=1, default=str), encoding="utf-8")
    OUT_MD.write_text(to_markdown(res), encoding="utf-8")
    log.info("coverage scan: %s -> %s", res["counts"], OUT_JSON)
    return 0


def load(path: Path = OUT_JSON) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None

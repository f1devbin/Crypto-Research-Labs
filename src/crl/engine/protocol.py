"""The evaluation protocol: turns a pre-registered spec into a verdict.

Two kinds of studies are supported:

timing_rule  one fixed rule, tested on a universe over one or more periods
             (e.g. "full history" and "2022+"); the hypothesis passes when the
             rule beats buy-and-hold on at least `min_wins` assets per period
             (optionally requiring per-asset significance).

rule_search  a set of candidate rules; for each asset the best candidate is chosen
             on the in-sample period only and then judged out of sample against
             a bootstrap null, Bonferroni-corrected for the number of selections.

forecast, forecast_live  daily probabilities from a pooled model, scored by Brier skill
             (see engine/forecast.py).

Verdicts: PASS (criterion met), WEAK (beats buy-and-hold more often than not, but the
pre-registered bar is not met — never evidence on its own), FAIL.
"""
import datetime as dt

import numpy as np
import pandas as pd

from crl import __version__
from crl.engine import rules as R
from crl.engine.backtest import evaluate_period, to_position
from crl.engine.stats import bootstrap_p, circular_shift_p, permutation_p

MARK = {"PASS": "✅", "WEAK": "◐", "FAIL": "❌"}


def _mask(index: pd.DatetimeIndex, start=None, end=None) -> np.ndarray:
    m = np.ones(len(index), dtype=bool)
    if start:
        m &= index >= pd.Timestamp(start)
    if end:
        m &= index <= pd.Timestamp(end)
    return m


def _public(row: dict) -> dict:
    return {k: (round(v, 6) if isinstance(v, float) else v) for k, v in row.items() if not k.startswith("_")}


def evaluate(spec: dict, store, seed: int = 2026) -> dict:
    kind = spec["kind"]
    if kind == "timing_rule":
        res = _timing_rule(spec, store, np.random.default_rng(seed))
    elif kind == "rule_search":
        res = _rule_search(spec, store, np.random.default_rng(seed))
    elif kind == "cross_section":
        res = _cross_section(spec, store, np.random.default_rng(seed))
    elif kind == "forecast":
        from crl.engine import forecast as F
        res = F.evaluate(spec, store, np.random.default_rng(seed))
    elif kind == "forecast_live":
        from crl.engine import forecast as F
        res = F.evaluate_live(spec, store, np.random.default_rng(seed))
    else:
        raise ValueError(f"unknown study kind '{kind}'")
    ends = [r["end"] for r in res["rows"] if r.get("end")]
    res.update(kind=kind, engine_version=__version__, data_end=max(ends) if ends else None,
               run_at=dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    return res


def _timing_rule(spec: dict, store, rng) -> dict:
    mode, fee = spec.get("mode", "long_flat"), float(spec["fee"])
    sig = spec.get("significance", {"method": "none"})
    crit = spec["criterion"]
    rows = []
    for sym in spec["universe"]:
        close = store.close(sym)
        decision = to_position(R.build(spec["rule"], store, sym), mode)
        for per in spec["periods"]:
            e = evaluate_period(decision, close, _mask(close.index, per.get("start"), per.get("end")), fee)
            p = None
            if e["days"] and sig.get("method") == "circular_shift":
                p = circular_shift_p(e["_pos"], e["_r"], fee, rng, int(sig.get("n", 2000)))
            elif e["days"] and sig.get("method") == "permutation":
                p = permutation_p(e["_pos"], e["_r"], fee, rng, int(sig.get("n", 2000)))
            beats = e["days"] > 0 and e["sharpe"] > e["hold_sharpe"]
            win = beats and (not crit.get("require_significance") or (p is not None and p < sig["alpha"]))
            rows.append({"symbol": sym, "period": per["name"], **e, "p": p, "beats_hold": beats, "win": win})

    verdict, lines = "PASS", []
    weak_ok = True
    for per in spec["periods"]:
        pr = [r for r in rows if r["period"] == per["name"]]
        wins = sum(r["win"] for r in pr)
        beats = sum(r["beats_hold"] for r in pr)
        need = crit["min_wins"][per["name"]]
        lines.append(f"{per['name']}: wins {wins}/{len(pr)} (need {need}), beats buy-and-hold {beats}/{len(pr)}")
        if wins < need:
            verdict = "FAIL"
        if beats * 2 <= len(pr):
            weak_ok = False
    if verdict == "FAIL" and weak_ok:
        verdict = "WEAK"
    return {"verdict": verdict, "summary": "; ".join(lines), "rows": [_public(r) for r in rows]}


def _cross_section(spec: dict, store, rng) -> dict:
    """Daily ranking of a universe; the portfolio passes a period when its Sharpe beats an
    equal-weight basket of the same coins (no fees for the basket) and, if required, the
    rotation null (cross.shift_p)."""
    from crl.engine import cross as X
    fee = float(spec["fee"])
    sig = spec.get("significance", {"method": "none"})
    crit = spec["criterion"]
    closes = X.panel(store, spec["universe"])
    w = X.weights(spec, closes, store)
    rows = []
    for per in spec["periods"]:
        e = X.evaluate_period(w, closes, _mask(closes.index, per.get("start"), per.get("end")), fee)
        p = None
        if e["days"] and sig.get("method") == "circular_shift":
            p = X.shift_p(e["_w"], e["_r"], fee, rng, int(sig.get("n", 1000)))
        beats = e["days"] > 0 and e["sharpe"] > e["hold_sharpe"]
        win = beats and (not crit.get("require_significance") or (p is not None and p < sig["alpha"]))
        rows.append({"symbol": "PORTFOLIO", "period": per["name"], **e, "p": p, "beats_hold": beats, "win": win})
    verdict, lines, weak_ok = "PASS", [], True
    for per in spec["periods"]:
        pr = [r for r in rows if r["period"] == per["name"]]
        wins, beats = sum(r["win"] for r in pr), sum(r["beats_hold"] for r in pr)
        need = crit["min_wins"][per["name"]]
        lines.append(f"{per['name']}: {'beats' if beats else 'does not beat'} the equal-weight basket"
                     f"{' (significant)' if wins else ''}")
        if wins < need:
            verdict = "FAIL"
        if not beats:
            weak_ok = False
    if verdict == "FAIL" and weak_ok:
        verdict = "WEAK"
    return {"verdict": verdict, "summary": "; ".join(lines), "rows": [_public(r) for r in rows]}


def _rule_search(spec: dict, store, rng) -> dict:
    mode, fee = spec.get("mode", "long_flat"), float(spec["fee"])
    cands = spec["candidates"]
    sig = spec.get("significance", {"method": "bootstrap", "n": 400, "alpha_family": 0.05})
    is_p, oos_p = spec["in_sample"], spec["out_of_sample"]
    warmup = max(R.lookback_days({k: v for k, v in c.items() if k != "type"}) for c in cands.values()) + 5
    alpha = sig.get("alpha_family", 0.05) / len(spec["universe"])
    rows = []
    for sym in spec["universe"]:
        close = store.close(sym)
        is_m = _mask(close.index, is_p.get("start"), is_p.get("end"))
        oos_m = _mask(close.index, oos_p.get("start"), oos_p.get("end"))
        scored = []
        for name, rule in cands.items():
            dec = to_position(R.build(rule, store, sym), mode)
            scored.append((evaluate_period(dec, close, is_m, fee)["sharpe"], name, dec))
        is_sharpe, best, dec = max(scored, key=lambda x: x[0])  # chosen on in-sample ONLY
        e = evaluate_period(dec, close, oos_m, fee)
        i0 = int(np.argmax(oos_m))
        c = close.to_numpy()
        p = None
        if e["days"] and sig.get("method") == "bootstrap":
            p = bootstrap_p(R.price_rule_fn(cands[best]), c[max(0, i0 - warmup):i0], c[i0:],
                            fee, mode, rng, int(sig.get("n", 400)))
        elif e["days"] and sig.get("method") == "circular_shift":
            p = circular_shift_p(e["_pos"], e["_r"], fee, rng, int(sig.get("n", 2000)))
        beats = e["days"] > 0 and e["sharpe"] > 0 and e["sharpe"] > e["hold_sharpe"]
        strict = beats and p is not None and p < alpha
        rows.append({"symbol": sym, "period": "oos", "selected": best, "is_sharpe": is_sharpe, **e,
                     "p": p, "alpha": alpha, "beats_hold": beats, "win": strict})

    strict = sum(r["win"] for r in rows)
    beats = sum(r["beats_hold"] for r in rows)
    need = spec["criterion"]["min_strict_wins"]
    verdict = "PASS" if strict >= need else ("WEAK" if beats * 2 > len(rows) else "FAIL")
    summary = (f"significant after Bonferroni (p < {alpha:.4f}) on {strict}/{len(rows)} assets "
               f"(need {need}); beats buy-and-hold on {beats}/{len(rows)}")
    return {"verdict": verdict, "summary": summary, "rows": [_public(r) for r in rows]}


def to_markdown(hyp: dict, res: dict) -> str:
    if res.get("kind") in ("forecast", "forecast_live"):
        return _forecast_markdown(hyp, res)
    out = [f"### {MARK[res['verdict']]} {hyp['id']} — {hyp['title']}",
           "",
           f"Verdict **{res['verdict']}** · data to {res['data_end']} · engine {res['engine_version']} · "
           f"run {res['run_at']}",
           "",
           res["summary"],
           "",
           "| asset | period | rule | days | Sharpe | hold Sharpe | CAGR | hold CAGR | max DD | hold DD | "
           "in market | p |",
           "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in res["rows"]:
        p = "—" if r["p"] is None else f"{r['p']:.4f}"
        rule = r.get("selected", "fixed")
        out.append(f"| {r['symbol']} | {r['period']} | {rule} | {r['days']} | {r['sharpe']:.2f} | "
                   f"{r['hold_sharpe']:.2f} | {r['cagr']:+.0%} | {r['hold_cagr']:+.0%} | {r['max_dd']:.0%} | "
                   f"{r['hold_max_dd']:.0%} | {r['exposure']:.0%} | {p} |")
    return "\n".join(out) + "\n"


def _forecast_markdown(hyp: dict, res: dict) -> str:
    def f(v, fmt):
        return "—" if v is None else format(v, fmt)
    out = [f"### {MARK[res['verdict']]} {hyp['id']} — {hyp['title']}", "",
           f"Verdict **{res['verdict']}** · data to {res['data_end']} · engine {res['engine_version']} · "
           f"run {res['run_at']}", "", res["summary"], "",
           "| asset | days | Brier skill | p | q | hits | Sharpe | hold Sharpe | constant-share Sharpe | in market |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    for r in res["rows"]:
        out.append(f"| {r['symbol']} | {r['days']} | {r['bss']:+.4f} | {r['p']:.4f} | {f(r.get('q'), '.3f')} | "
                   f"{r['hits']:.1%} | {f(r.get('sharpe'), '.2f')} | {f(r.get('hold_sharpe'), '.2f')} | "
                   f"{f(r.get('const_sharpe'), '.2f')} | {f(r.get('exposure'), '.0%')} |")
    return "\n".join(out) + "\n"

"""Hypothesis proposer: an LLM drafts new testable ideas, the registry decides if they are allowed.

Guardrails — the model can only *propose*:
  * output must parse into the registry schema (validate()) or it is dropped;
  * anything with the same fingerprint as an existing study (tested or not) is dropped;
  * proposals land as status `draft`, unlocked and unrun; a human reviews the pull
    request and runs `crl registry register` to lock the spec before any test;
  * the model never picks coins (rule 7 in CLAUDE.md): each idea is drafted on every Binance coin, with a
    companion draft for the Gate.io coins at Gate's fee and slippage, and alpha is split across all coins.
This keeps the pre-registration discipline intact: no model ever sees a result
and then tunes the rule that produced it.
"""
import copy
import datetime as dt
import json
import logging
import re
from pathlib import Path

import yaml

from crl import registry
from crl.config import HYPOTHESES_DIR, REPORTS_DIR
from crl.data.sources import OTHER_EXCHANGES
from crl.data.store import FEATURES
from crl.engine.rules import FEATURE_RULES, PRICE_RULES
from crl.llm import client
from crl.site import COIN_NAMES

log = logging.getLogger(__name__)

COINS = list(COIN_NAMES)  # every coin the lab tracks (the dashboard's list)
GATE_COINS = [s for s in COINS if OTHER_EXCHANGES.get(s, ("",))[0] == "gate"]
BINANCE_COINS = [s for s in COINS if s not in GATE_COINS]
ALPHA = round(0.05 / len(COINS), 4)  # Bonferroni across all coins, both lines together
GATE_COST = 0.004  # per side: Gate.io fee 0.2 % + slippage 0.2 %, as in the forecast studies' costs
GATE_START = "2023-03-13"  # first day with Gate.io prices for every Gate coin (GRAM)

SYSTEM = """You are a sceptical quantitative researcher for a small, single-owner crypto research lab.
Your job is to propose NEW, falsifiable, pre-registrable timing hypotheses that the lab's engine can test
on daily data. You never see results of your proposals before they are locked, so do not overfit.
Prefer ideas with an economic rationale and a clear null. Respect retail fees (spot 0.10% per side).
Every idea is tested on every coin the lab tracks: never choose coins.
Reply with JSON only — no prose, no markdown fences."""

EXAMPLE = {
    "title": "Coins held only while stablecoin supply grows faster than its 1-year median",
    "family": "flows",
    "rationale": "New stablecoin issuance is dry powder entering crypto; growth above normal may precede demand.",
    "spec": {
        "kind": "timing_rule",
        "rule": {"type": "feature_vs_rolling_quantile", "feature": "stablecoin_growth_7d",
                 "q": 0.5, "long_when": "above", "lookback": 365, "min_periods": 180, "lag": 1},
        "mode": "long_flat", "fee": 0.001, "universe": BINANCE_COINS,
        "periods": [{"name": "oos", "start": "2022-01-01"}],
        "significance": {"method": "circular_shift", "n": 2000, "alpha": ALPHA},
        "criterion": {"min_wins": {"oos": 1}, "require_significance": True},
    },
}


def build_prompt(hyps: list, regime_md: str, n: int) -> str:
    tested = [{"id": h.id, "title": h["title"], "status": h["status"], "family": h["family"],
               "rule": (h.get("spec") or {}).get("rule"),
               "last": (h.get("history") or [{}])[-1].get("summary") if h.get("history") else None}
              for h in hyps]
    return f"""Propose {n} new hypotheses as a JSON array. Each element must look like this example:
{json.dumps(EXAMPLE, indent=1)}

Engine capabilities (use nothing else):
- spec.kind: "timing_rule" only (one fixed rule; periods + criterion.min_wins per period, counting the coins
  where the rule beats holding with p < alpha).
- price rule types: {sorted(PRICE_RULES)} (params: window | fast,slow | lookback | entry)
- feature rule types: {sorted(FEATURE_RULES)} with feature in {sorted(FEATURES)}
  feature_threshold params: threshold, long_when ("above"|"below"), lag
  feature_vs_rolling_quantile params: q, long_when ("above"|"not_above"), lookback, min_periods, lag
- mode: "long_flat" (spot) or "long_short"; fee is per side (spot 0.001, futures taker 0.0005)
- universe: always all of the lab's Binance coins, exactly {BINANCE_COINS}. The lab adds a second line
  for the Gate.io coins {GATE_COINS} with Gate's fee and slippage: never list them, never pick a subset.
- significance: circular_shift (permutation for day_of_week / turn_of_month rules), alpha {ALPHA}
  (Bonferroni across all {len(COINS)} coins), criterion.require_significance: true.

Already in the registry — do NOT repeat these or trivially re-parametrise them:
{json.dumps(tested, indent=1)}

Current market regime (for context, not for fitting):
{regime_md or "n/a"}
"""


def _extract_json(text: str):
    text = text.strip()
    m = re.search(r"\[.*\]", text, re.S)
    return json.loads(m.group(0) if m else text)


def next_id(hyps: list) -> int:
    nums = [int(h.id.split("-")[1]) for h in hyps if re.fullmatch(r"H-\d{3,}", h.id)]
    return max(nums, default=0) + 1


def all_coins(spec) -> tuple[dict, dict] | str:
    """The proposed rule on every Binance coin and its Gate.io line (rule 7), or why it cannot be drafted."""
    if not isinstance(spec, dict) or spec.get("kind") != "timing_rule":
        return "the proposer drafts timing rules only"
    calendar = (spec.get("rule") or {}).get("type") in ("day_of_week", "turn_of_month")
    sig = dict(spec.get("significance") or {})
    sig.setdefault("method", "permutation" if calendar else "circular_shift")
    sig.setdefault("n", 2000)
    try:
        sig["alpha"] = min(float(sig.get("alpha", ALPHA)), ALPHA)
        wins = {k: max(1, int(v)) for k, v in (spec.get("criterion") or {}).get("min_wins", {}).items()}
    except (TypeError, ValueError, AttributeError):
        return "significance.alpha and criterion.min_wins must be numbers"
    crit = {**spec.get("criterion", {}), "min_wins": wins, "require_significance": True}
    main = {**copy.deepcopy(spec), "universe": list(BINANCE_COINS), "significance": sig, "criterion": crit}
    gate = {**copy.deepcopy(main), "universe": list(GATE_COINS), "fee": GATE_COST,
            "periods": [{"name": "gate", "start": GATE_START}],
            "criterion": {**crit, "min_wins": {"gate": 1}}}
    return main, gate


def accept(proposals: list, hyps: list, root: Path, today: dt.date, model: str) -> tuple[list, list]:
    """Validate, de-duplicate and write proposals as draft files, each as a pair: the Binance coins and the
    Gate.io coins. Returns (written ids, rejections)."""
    written, rejected = [], []
    known = list(hyps)
    n = next_id(hyps)
    gate_names = ", ".join(s.removesuffix("USDT") for s in GATE_COINS)
    for prop in proposals:
        title = str(prop.get("title", "")).strip()
        specs = all_coins(prop.get("spec"))
        if isinstance(specs, str):
            rejected.append({"title": title, "reasons": [specs]})
            continue
        main_id, gate_id = f"H-{n:03d}", f"H-{n + 1:03d}"
        rationale = str(prop.get("rationale", "")).strip()
        common = {"status": "draft", "family": str(prop.get("family", "other")), "created": str(today),
                  "author": f"llm:{model}", "retest_every_days": 90}
        pair = [registry.Hypothesis(root / f"{main_id}.yaml",
                                    {"id": main_id, "title": title, **common, "rationale": rationale,
                                     "spec": specs[0]}),
                registry.Hypothesis(root / f"{gate_id}.yaml",
                                    {"id": gate_id, "title": f"{title} — Gate.io coins ({gate_names})", **common,
                                     "rationale": f"Gate.io line of {main_id} (rule 7: the Gate coins are tested on "
                                                  f"their own line, with Gate's fee 0.2 % and slippage 0.2 % per side, "
                                                  f"from {GATE_START} when all of them have prices). {rationale}",
                                     "spec": specs[1]})]
        errs = [e for h in pair for e in registry.validate(h)]
        errs += [f"duplicate of {d}" for h in pair for d in registry.duplicates(h, known)]
        if errs or not title:
            rejected.append({"title": title, "reasons": errs or ["no title"]})
            continue
        for h in pair:
            registry.save(h)
            known.append(h)
            written.append(h.id)
        n += 2
    return written, rejected


def main(n: int = 3, root: Path = HYPOTHESES_DIR) -> int:
    if not client.available():
        log.warning("ANTHROPIC_API_KEY not set — proposer skipped")
        return 0
    hyps = registry.load_all(root)
    regime = REPORTS_DIR / "regime.md"
    text = client.complete(SYSTEM, build_prompt(hyps, regime.read_text() if regime.exists() else "", n))
    try:
        proposals = _extract_json(text)
    except ValueError:
        log.error("model did not return JSON:\n%s", text[:2000])
        return 1
    written, rejected = accept(proposals if isinstance(proposals, list) else [], hyps, root,
                               dt.datetime.now(dt.timezone.utc).date(), client.model_name())
    for r in rejected:
        log.info("rejected proposal '%s': %s", r["title"], "; ".join(r["reasons"]))
    print(yaml.safe_dump({"written": written, "rejected": rejected}, allow_unicode=True))
    return 0

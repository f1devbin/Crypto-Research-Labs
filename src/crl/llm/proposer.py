"""Hypothesis proposer: an LLM drafts new testable ideas, the registry decides if they are allowed.

Guardrails — the model can only *propose*:
  * output must parse into the registry schema (validate()) or it is dropped;
  * anything with the same fingerprint as an existing study (tested or not) is dropped;
  * proposals land as status `draft`, unlocked and unrun; a human reviews the pull
    request and runs `crl registry register` to lock the spec before any test.
This keeps the pre-registration discipline intact: no model ever sees a result
and then tunes the rule that produced it.
"""
import datetime as dt
import json
import logging
import re
from pathlib import Path

import yaml

from crl import registry
from crl.config import HYPOTHESES_DIR, REPORTS_DIR
from crl.data.store import FEATURES
from crl.engine.rules import FEATURE_RULES, PRICE_RULES
from crl.llm import client

log = logging.getLogger(__name__)

SYSTEM = """You are a sceptical quantitative researcher for a small, single-owner crypto research lab.
Your job is to propose NEW, falsifiable, pre-registrable timing hypotheses that the lab's engine can test
on daily data. You never see results of your proposals before they are locked, so do not overfit.
Prefer ideas with an economic rationale and a clear null. Respect retail fees (spot 0.10% per side).
Reply with JSON only — no prose, no markdown fences."""

EXAMPLE = {
    "title": "BTC long only when stablecoin supply grows faster than its 1-year median",
    "family": "flows",
    "rationale": "New stablecoin issuance is dry powder entering crypto; growth above normal may precede demand.",
    "spec": {
        "kind": "timing_rule",
        "rule": {"type": "feature_vs_rolling_quantile", "feature": "stablecoin_growth_7d",
                 "q": 0.5, "long_when": "above", "lookback": 365, "min_periods": 180, "lag": 1},
        "mode": "long_flat", "fee": 0.001, "universe": ["BTCUSDT"],
        "periods": [{"name": "oos", "start": "2022-01-01"}],
        "significance": {"method": "circular_shift", "n": 2000, "alpha": 0.0125},
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
- spec.kind: "timing_rule" (fixed rule; periods + criterion.min_wins per period) or "rule_search"
  (candidates chosen in-sample; needs in_sample, out_of_sample, criterion.min_strict_wins).
- price rule types: {sorted(PRICE_RULES)} (params: window | fast,slow | lookback | entry)
- feature rule types: {sorted(FEATURE_RULES)} with feature in {sorted(FEATURES)}
  feature_threshold params: threshold, long_when ("above"|"below"), lag
  feature_vs_rolling_quantile params: q, long_when ("above"|"not_above"), lookback, min_periods, lag
- mode: "long_flat" (spot) or "long_short"; fee is per side (spot 0.001, futures taker 0.0005)
- universe: Binance spot USDT pairs, e.g. BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT, ADAUSDT, LTCUSDT,
  LINKUSDT, DOGEUSDT, XLMUSDT, TRXUSDT
- significance: circular_shift (any rule) or bootstrap (price rules only); Bonferroni-correct alpha
  for the number of assets/hypotheses you claim.
- Confirmation on independent coins (not used to design the rule) is strongly preferred.

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


def accept(proposals: list, hyps: list, root: Path, today: dt.date, model: str) -> tuple[list, list]:
    """Validate, de-duplicate and write proposals as draft files. Returns (written ids, rejections)."""
    written, rejected = [], []
    known = list(hyps)
    n = next_id(hyps)
    for prop in proposals:
        hid = f"H-{n:03d}"
        data = {"id": hid, "title": str(prop.get("title", "")).strip(), "status": "draft",
                "family": str(prop.get("family", "other")), "created": str(today),
                "author": f"llm:{model}", "rationale": str(prop.get("rationale", "")).strip(),
                "spec": prop.get("spec"), "retest_every_days": 90}
        h = registry.Hypothesis(root / f"{hid}.yaml", data)
        errs = registry.validate(h)
        dups = registry.duplicates(h, known)
        if errs or dups or not data["title"]:
            rejected.append({"title": data["title"], "reasons": errs + [f"duplicate of {d}" for d in dups]})
            continue
        registry.save(h)
        known.append(h)
        written.append(hid)
        n += 1
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

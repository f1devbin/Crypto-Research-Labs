"""Hypothesis registry: one YAML file per idea under hypotheses/.

Life cycle:  draft → registered (spec locked by sha256) → passed / weak / rejected
             (re-tested on schedule; a status can change as new data arrives).
Anything with rerunnable: false is historical and never executed again.
"""
import datetime as dt
import hashlib
import inspect
import json
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from crl.config import HYPOTHESES_DIR, RESULTS_DIR
from crl.engine.rules import RULE_TYPES

STATUSES = {"draft", "registered", "passed", "weak", "rejected", "archived"}
VERDICT_STATUS = {"PASS": "passed", "WEAK": "weak", "FAIL": "rejected"}
REQUIRED = ("id", "title", "status", "family", "created", "rationale")


@dataclass
class Hypothesis:
    path: Path
    data: dict = field(default_factory=dict)

    def __getitem__(self, k):
        return self.data[k]

    def get(self, k, default=None):
        return self.data.get(k, default)

    @property
    def id(self) -> str:
        return self.data["id"]


def spec_hash(spec: dict) -> str:
    canon = json.dumps(spec, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canon.encode()).hexdigest()


def fingerprint(spec: dict) -> str:
    """What makes two ideas 'the same test' regardless of wording or metadata."""
    core = {
        "kind": spec.get("kind"),
        "mode": spec.get("mode", "long_flat"),
        "universe": sorted(spec.get("universe", [])),
        "rule": spec.get("rule"),
        "candidates": sorted(json.dumps(c, sort_keys=True) for c in (spec.get("candidates") or {}).values()),
    }
    return spec_hash(core)[:16]


def load_all(root: Path = HYPOTHESES_DIR) -> list[Hypothesis]:
    out = []
    for p in sorted(Path(root).glob("*.yaml")):
        out.append(Hypothesis(p, yaml.safe_load(p.read_text()) or {}))
    return out


def save(h: Hypothesis) -> None:
    h.path.write_text(yaml.safe_dump(h.data, sort_keys=False, allow_unicode=True, width=100))


def validate(h: Hypothesis) -> list[str]:
    errs = [f"missing field '{k}'" for k in REQUIRED if k not in h.data]
    if h.get("status") not in STATUSES:
        errs.append(f"status must be one of {sorted(STATUSES)}")
    if h.get("id") and h.path.stem != h["id"]:
        errs.append(f"file name must be {h['id']}.yaml")
    if not h.get("rerunnable", True):
        return errs  # historical record: spec is documentation only
    spec = h.get("spec")
    if not isinstance(spec, dict):
        return errs + ["missing 'spec'"]
    kind = spec.get("kind")
    if kind not in ("timing_rule", "rule_search"):
        return errs + ["spec.kind must be timing_rule or rule_search"]
    for k in ("fee", "universe", "criterion"):
        if k not in spec:
            errs.append(f"spec.{k} is required")
    if not 0 <= float(spec.get("fee", 0)) < 0.05:
        errs.append("spec.fee must be a fraction per side, e.g. 0.001")
    rules = [spec.get("rule")] if kind == "timing_rule" else list((spec.get("candidates") or {}).values())
    for r in rules:
        if not isinstance(r, dict) or r.get("type") not in RULE_TYPES:
            errs.append(f"unknown rule {r!r}; known types: {sorted(RULE_TYPES)}")
            continue
        errs += _check_rule_params(r)
    if kind == "timing_rule":
        names = [p.get("name") for p in spec.get("periods", [])]
        if not names:
            errs.append("spec.periods is required for timing_rule")
        missing = set(names) - set(spec.get("criterion", {}).get("min_wins", {}))
        if missing:
            errs.append(f"criterion.min_wins lacks periods {sorted(missing)}")
        sig = spec.get("significance", {})
        if spec.get("criterion", {}).get("require_significance") and "alpha" not in sig:
            errs.append("require_significance needs significance.alpha")
    else:
        for k in ("in_sample", "out_of_sample", "candidates"):
            if k not in spec:
                errs.append(f"spec.{k} is required for rule_search")
        if spec.get("significance", {}).get("method") == "bootstrap":
            if any(r.get("type") not in ("price_above_sma", "sma_cross", "tsmom", "donchian") for r in rules):
                errs.append("bootstrap significance supports price rules only; use circular_shift")
    if h.get("status") != "draft":
        if not h.get("prereg_sha256"):
            errs.append("registered hypothesis has no prereg_sha256 — run `crl registry register`")
        elif h["prereg_sha256"] != spec_hash(spec):
            errs.append("spec changed after registration (sha256 mismatch) — results would be invalid")
    return errs


def _check_rule_params(rule: dict) -> list[str]:
    from crl.data.store import FEATURES
    from crl.engine.rules import FEATURE_RULES, PRICE_RULES

    fn = PRICE_RULES.get(rule["type"]) or FEATURE_RULES[rule["type"]]
    params = list(inspect.signature(fn).parameters.values())[1:]  # first arg is the series
    given = {k for k in rule if k not in ("type", "feature")}
    allowed = {p.name for p in params}
    required = {p.name for p in params if p.default is inspect.Parameter.empty}
    errs = []
    if given - allowed:
        errs.append(f"{rule['type']}: unknown params {sorted(given - allowed)}")
    if required - given:
        errs.append(f"{rule['type']}: missing params {sorted(required - given)}")
    if rule["type"] in FEATURE_RULES and rule.get("feature") not in FEATURES:
        errs.append(f"{rule['type']}: feature must be one of {sorted(FEATURES)}")
    if rule.get("long_when") not in (None, "above", "below", "not_above"):
        errs.append(f"{rule['type']}: bad long_when '{rule.get('long_when')}'")
    return errs


def duplicates(h: Hypothesis, others: list[Hypothesis]) -> list[str]:
    if not h.get("spec") or not h.get("rerunnable", True):
        return []
    fp = fingerprint(h["spec"])
    return [o.id for o in others
            if o.id != h.id and o.get("spec") and o.get("rerunnable", True) and fingerprint(o["spec"]) == fp]


def register(h: Hypothesis, today: dt.date | None = None) -> None:
    if h.get("status") != "draft":
        raise ValueError(f"{h.id} is already {h['status']}")
    errs = [e for e in validate(Hypothesis(h.path, {**h.data, "status": "registered",
                                                    "prereg_sha256": spec_hash(h["spec"])}))]
    if errs:
        raise ValueError(f"{h.id}: " + "; ".join(errs))
    h.data["status"] = "registered"
    h.data["registered"] = str(today or dt.date.today())
    h.data["prereg_sha256"] = spec_hash(h["spec"])
    save(h)


# ── results ──────────────────────────────────────────────────────────

def latest_result(hid: str, root: Path = RESULTS_DIR) -> dict | None:
    p = Path(root) / hid / "latest.json"
    return json.loads(p.read_text()) if p.exists() else None


def store_result(h: Hypothesis, res: dict, root: Path = RESULTS_DIR) -> dict | None:
    """Save the run; returns the previous result (for change detection)."""
    prev = latest_result(h.id, root)
    d = Path(root) / h.id
    d.mkdir(parents=True, exist_ok=True)
    body = json.dumps({"id": h.id, "prereg_sha256": h.get("prereg_sha256"), **res}, indent=1)
    (d / f"{res['run_at'][:10]}.json").write_text(body)
    (d / "latest.json").write_text(body)
    h.data["status"] = VERDICT_STATUS[res["verdict"]]
    h.data["last_run"] = res["run_at"][:10]
    save(h)
    return prev


def is_due(h: Hypothesis, today: dt.date, root: Path = RESULTS_DIR) -> bool:
    if not h.get("rerunnable", True) or h.get("status") in ("draft", "archived"):
        return False
    last = latest_result(h.id, root)
    if last is None:
        return True
    every = h.get("retest_every_days")
    if not every:
        return False
    return (today - dt.date.fromisoformat(last["run_at"][:10])).days >= int(every)

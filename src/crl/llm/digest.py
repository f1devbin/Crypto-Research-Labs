"""Weekly digest: what changed in data, regime and results. Deterministic by default;
with ANTHROPIC_API_KEY the model rewrites it as a short plain-English briefing, but
numbers always come from the deterministic part (the model is told not to add any)."""
import datetime as dt
import logging

from crl.config import REPORTS_DIR
from crl.llm import client
from crl.notify import alert

log = logging.getLogger(__name__)

SYSTEM = """You write short, sober research briefings. Use ONLY facts and numbers present in the input.
Never recommend trades. Flag uncertainty. Maximum 200 words, plain text, no tables."""


def collect(days: int = 7) -> str:
    today = dt.datetime.now(dt.timezone.utc).date()
    parts = []
    for name in ("regime.md", "data_health.md"):
        p = REPORTS_DIR / name
        if p.exists():
            parts.append(p.read_text())
    runs = REPORTS_DIR / "runs"
    if runs.exists():
        for p in sorted(runs.glob("*.md")):
            try:
                if (today - dt.date.fromisoformat(p.stem)).days <= days:
                    parts.append(p.read_text())
            except ValueError:
                continue
    return "\n\n".join(parts)


def main() -> int:
    facts = collect()
    if not facts:
        log.info("nothing to report")
        return 0
    week = dt.datetime.now(dt.timezone.utc).date().isocalendar()
    text = facts
    if client.available():
        try:
            from crl.notify import a
            text = client.complete(SYSTEM + f" Write in {a('digest_lang')}.",
                                   "Write this week's briefing from these reports:\n\n" + facts, 800)
        except Exception as e:
            log.warning("LLM digest failed (%s), sending deterministic version", type(e).__name__)
    path = REPORTS_DIR / "digest" / f"{week.year}-W{week.week:02d}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text + "\n")
    from crl.notify import a
    alert(a("t_digest", week=f"{week.year}-W{week.week:02d}"), [text[:3500]])
    return 0

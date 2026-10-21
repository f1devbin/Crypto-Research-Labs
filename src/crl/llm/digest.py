"""Weekly digest: what changed in data, regime and results.

The facts are deterministic (regime, data health and run reports of the last 7 days). With an LLM key
(LLM_API_KEY or ANTHROPIC_API_KEY) a model retells them for beginners in every dashboard language;
the numbers always come from the facts (the model is told not to add any and never to suggest trades).

Files: reports/digest/<year>-W<week>/facts.md, <lang>.md for each language written, meta.json.
Telegram gets the TELEGRAM_LANG version (or the facts when no model is configured).
"""
import datetime as dt
import json
import logging
from pathlib import Path

from crl.config import REPORTS_DIR
from crl.i18n import LANGS
from crl.llm import client
from crl.notify import a, alert, lang as alert_lang

log = logging.getLogger(__name__)

LANG_NAMES = {"en": "English", "ru": "Russian", "es": "Spanish", "pt": "Brazilian Portuguese", "tr": "Turkish",
              "vi": "Vietnamese", "zh": "Simplified Chinese"}

SYSTEM = """You write a short weekly briefing for beginners about a crypto research dashboard.
Use ONLY facts and numbers present in the input; never invent or round differently. Never recommend trades,
never predict prices. Explain jargon in plain words. Flag uncertainty.
Format: one short opening paragraph with the overall picture, then 3-6 lines starting with "- ",
then one closing sentence on what changed in the tested hypotheses (or that nothing changed).
No headings, no tables, no emojis, at most 220 words."""

DIGEST_DIR = REPORTS_DIR / "digest"


def collect(days: int = 7) -> str:
    today = dt.datetime.now(dt.timezone.utc).date()
    parts = []
    for name in ("regime.md", "data_health.md", "COVERAGE.md"):
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


def week_id(day: dt.date) -> str:
    y, w, _ = day.isocalendar()
    return f"{y}-W{w:02d}"


def write(facts: str, texts: dict[str, str], model: str | None, day: dt.date, root: Path = DIGEST_DIR) -> Path:
    d = root / week_id(day)
    d.mkdir(parents=True, exist_ok=True)
    (d / "facts.md").write_text(facts + "\n", encoding="utf-8")
    for code, text in texts.items():
        (d / f"{code}.md").write_text(text.strip() + "\n", encoding="utf-8")
    (d / "meta.json").write_text(json.dumps({"week": week_id(day), "date": str(day), "model": model,
                                             "languages": sorted(texts)}, indent=1), encoding="utf-8")
    return d


def load(root: Path = DIGEST_DIR, limit: int = 12) -> list[dict]:
    """Newest first: [{"week", "date", "model", "texts": {lang: markdown}}], only weeks written by a model."""
    out = []
    for d in sorted((p for p in root.glob("*-W*") if p.is_dir()), reverse=True):
        try:
            meta = json.loads((d / "meta.json").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        texts = {c: (d / f"{c}.md").read_text(encoding="utf-8") for c in LANGS if (d / f"{c}.md").exists()}
        if texts:
            out.append({**meta, "texts": texts})
        if len(out) >= limit:
            break
    return out


def main() -> int:
    facts = collect()
    if not facts:
        log.info("nothing to report")
        return 0
    today = dt.datetime.now(dt.timezone.utc).date()
    texts: dict[str, str] = {}
    if client.available():
        for code in LANGS:
            try:
                texts[code] = client.complete(SYSTEM + f" Write in {LANG_NAMES[code]}.",
                                              "This week's reports:\n\n" + facts, 900)
            except Exception as e:  # one language failing must not lose the others
                log.warning("digest in %s failed: %s", code, type(e).__name__)
    write(facts, texts, client.model_name() if texts else None, today)
    body = texts.get(alert_lang()) or texts.get("en") or facts
    alert(a("t_digest", week=week_id(today)), [body[:3500]])
    return 0

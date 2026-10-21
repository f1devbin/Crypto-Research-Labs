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
from crl.notify import a, alert, job_summary, lang as alert_lang

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


def _why(e: Exception) -> str:
    """Short, secret-free reason for a failed model call (shown in meta.json and the job summary)."""
    import urllib.error
    if isinstance(e, urllib.error.HTTPError):
        try:
            body = e.read().decode("utf-8", "replace")[:200]
        except Exception:
            body = ""
        return f"HTTP {e.code}: {body}".strip()
    return f"{type(e).__name__}: {e}"[:200]


def write(facts: str, texts: dict[str, str], model: str | None, day: dt.date, root: Path = DIGEST_DIR,
          errors: dict | None = None) -> Path:
    d = root / week_id(day)
    d.mkdir(parents=True, exist_ok=True)
    (d / "facts.md").write_text(facts + "\n", encoding="utf-8")
    for code, text in texts.items():
        (d / f"{code}.md").write_text(text.strip() + "\n", encoding="utf-8")
    (d / "meta.json").write_text(json.dumps({"week": week_id(day), "date": str(day), "model": model,
                                             "languages": sorted(texts), "errors": errors or {}},
                                            indent=1, ensure_ascii=False), encoding="utf-8")
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


def plain_summary(code: str, store=None) -> str:
    """Model-free weekly message: today's market diagnosis in plain words (same as the dashboard)."""
    from crl import site
    from crl.agents import regime_watch
    from crl.data.store import DataStore
    from crl.i18n import t
    from crl.site_render import diag_item_text
    store = store or DataStore()
    cur = regime_watch.evaluate(store, regime_watch.load_monitors())
    reg = [{"id": k, "value": v["value"], "band": v["band"], "error": v.get("error")} for k, v in cur.items()]
    coins = []
    for sym in site.COIN_NAMES:
        try:
            c = store.close(sym).dropna()
        except (FileNotFoundError, KeyError):
            continue
        sma = c.rolling(200).mean()
        coins.append({"vs200": None if sma.isna().iloc[-1] else float(c.iloc[-1] / sma.iloc[-1] - 1)})
    d = site.diagnosis(reg, coins)
    if not d:
        return ""
    mark = {1: "▲", -1: "▼", 0: "•"}
    lines = [t(code, "diag_level_" + d["level"]), ""]
    lines += [f"{mark[i['tone']]} {diag_item_text(code, i)}" for i in d["items"]]
    lines += ["", t(code, "diag_means_" + d["level"]), "", t(code, "diag_disclaimer")]
    return "\n".join(lines)


def main() -> int:
    facts = collect()
    if not facts:
        log.info("nothing to report")
        return 0
    today = dt.datetime.now(dt.timezone.utc).date()
    texts: dict[str, str] = {}
    errors: dict[str, str] = {}
    if not client.available():
        errors["_"] = "no LLM key: set LLM_API_KEY (free, e.g. Groq) or ANTHROPIC_API_KEY"
    else:
        for code in LANGS:
            try:
                texts[code] = client.complete(SYSTEM + f" Write in {LANG_NAMES[code]}.",
                                              "This week's reports:\n\n" + facts, 900)
            except Exception as e:  # one language failing must not lose the others
                errors[code] = _why(e)
                log.warning("digest in %s failed: %s", code, errors[code])
    write(facts, texts, client.model_name() if texts else None, today, errors=errors)
    if errors:
        job_summary("## Weekly digest: model errors\n\n" + "\n".join(f"- {k}: {v}" for k, v in errors.items()))
    body = texts.get(alert_lang())
    if not body:
        try:
            body = plain_summary(alert_lang())
        except Exception as e:  # the weekly message must not depend on every data source
            log.warning("plain summary failed: %s", e)
            body = ""
    if not body:
        return 0
    alert(a("t_digest", week=week_id(today)), [body[:3500]])
    return 0

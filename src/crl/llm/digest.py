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
import re
from pathlib import Path

from crl.config import REPORTS_DIR
from crl.i18n import LANGS
from crl.llm import client
from crl.notify import a, alert, job_summary, lang as alert_lang

log = logging.getLogger(__name__)

LANG_NAMES = {"en": "English", "ru": "Russian", "es": "Spanish", "pt": "Brazilian Portuguese", "tr": "Turkish",
              "vi": "Vietnamese", "zh": "Simplified Chinese"}

SYSTEM = """You write a short weekly briefing for beginners about a crypto research dashboard.
Use ONLY facts and numbers present in the input; copy them exactly, never round differently, never do new
arithmetic. Never recommend trades, never predict prices. Explain jargon in plain words.

Facts are measurements, not explanations. Never say why something happened and never join two facts as cause
and effect ("because", "due to", "thanks to", "after X, Y followed"). If the input does not state a cause, say
the reports do not explain it, or leave it out.

When a tested idea passed or failed, say it was locked before the test and that one week is not proof either way.

Format: one or two opening sentences with the overall picture, then 3-5 lines starting with "- ", each one a
measured fact, then one closing sentence about the tested hypotheses (or that nothing changed). No headings, no
tables, no emojis, at most 200 words.

Bad: "Fees fell because traders left the market." Good: "Fees fell to 0.2 % from 0.4 %; the reports do not say why."
Bad: "Stablecoin inflows pushed BTC up." Good: "Stablecoin growth was 1.2 %, BTC rose 3.4 % the same week."
"""

TRANSLATE = """Translate the user's text into {lang}. Keep every number, sign, percent, ticker and hypothesis id
exactly as written, keep the paragraph and "- " line structure, add nothing, omit nothing. Output only the translation."""

DIGEST_DIR = REPORTS_DIR / "digest"

_NUM = re.compile(r"\d[\d.,]*\s?%?")


def _numbers(text: str) -> set[str]:
    """Numeric tokens, spaces removed, so "1.5 %" and "1.5%" compare equal."""
    return {m.group(0).replace(" ", "").rstrip(".,") for m in _NUM.finditer(text)}


def _invented(text: str, facts: str) -> list[str]:
    """Numbers in the draft that do not appear in the facts. The weekly text must never invent one."""
    known = _numbers(facts)
    return sorted({n for n in _numbers(text) if n not in known})



def collect(days: int = 7) -> str:
    today = dt.datetime.now(dt.timezone.utc).date()
    parts = []
    for name in ("regime.md", "data_health.md"):
        p = REPORTS_DIR / name
        if p.exists():
            text = p.read_text()
            if name == "data_health.md":  # only problems matter; the per-file table is noise for a briefing
                text = "\n".join(ln for ln in text.splitlines() if ln.startswith(("#", "- **error", "- **warn"))
                                  and "daily moves" not in ln)
            parts.append(text)
    cov = REPORTS_DIR / "COVERAGE.md"
    if cov.exists():  # the matrix is big; its counts line says enough
        counts = [ln for ln in cov.read_text().splitlines() if ln.startswith("Counts:")]
        parts.append("Coverage scan (every tested rule on every coin, exploratory): " + (counts[0] if counts else ""))
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
          errors: dict | None = None, warnings: dict | None = None) -> Path:
    d = root / week_id(day)
    d.mkdir(parents=True, exist_ok=True)
    for old in d.glob("*.md"):  # a rerun replaces the whole week, no stale languages
        old.unlink()
    (d / "facts.md").write_text(facts + "\n", encoding="utf-8")
    for code, text in texts.items():
        (d / f"{code}.md").write_text(text.strip() + "\n", encoding="utf-8")
    (d / "meta.json").write_text(json.dumps({"week": week_id(day), "date": str(day), "model": model,
                                             "languages": sorted(texts), "errors": errors or {},
                                             "warnings": warnings or {}},
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
    warnings: dict[str, str] = {}
    if not client.available():
        errors["_"] = "no LLM key: set LLM_API_KEY (free, e.g. Groq) or ANTHROPIC_API_KEY"
    else:
        # write once in English from the facts, then translate the short text: 7x fewer input tokens,
        # which keeps free tiers under their per-minute limits, and the numbers stay identical
        try:
            prompt = "This week's reports:\n\n" + facts
            texts["en"] = client.complete(SYSTEM, prompt, 4000)
            bad = _invented(texts["en"], facts)
            if bad:  # free models do invent numbers; one corrective retry, then keep and record it
                note = ("\n\nYour previous draft used numbers that are not in the reports: "
                        + ", ".join(bad[:10]) + ". Rewrite it using only numbers from the reports.")
                again = client.complete(SYSTEM, prompt + note, 4000)
                left = _invented(again, facts)
                texts["en"] = again
                if left:
                    warnings["en"] = "numbers not in the facts after a retry: " + ", ".join(left[:10])
                    log.warning("digest numbers: %s", warnings["en"])
        except Exception as e:
            errors["en"] = _why(e)
            log.warning("digest failed: %s", errors["en"])
        for code in LANGS:
            if code == "en" or "en" not in texts:
                continue
            try:
                texts[code] = client.complete(TRANSLATE.format(lang=LANG_NAMES[code]), texts["en"], 4000)
            except Exception as e:  # one language failing must not lose the others
                errors[code] = _why(e)
                log.warning("digest in %s failed: %s", code, errors[code])
    write(facts, texts, client.model_name() if texts else None, today, errors=errors, warnings=warnings)
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

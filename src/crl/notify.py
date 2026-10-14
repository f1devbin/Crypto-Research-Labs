"""Alerts: Telegram (if configured) and the GitHub Actions job summary (if running in Actions)."""
import json
import logging
import os
import urllib.parse
import urllib.request

log = logging.getLogger(__name__)
TELEGRAM_LIMIT = 4000


def telegram(text: str) -> bool:
    token, chat = os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("TELEGRAM_CHAT_ID")
    if not (token and chat):
        log.info("Telegram not configured, skipping alert")
        return False
    data = urllib.parse.urlencode({"chat_id": chat, "text": text[:TELEGRAM_LIMIT],
                                   "disable_web_page_preview": "true"}).encode()
    try:
        with urllib.request.urlopen(f"https://api.telegram.org/bot{token}/sendMessage", data, timeout=30) as r:
            return json.loads(r.read()).get("ok", False)
    except Exception as e:  # alerts must never break a workflow
        log.warning("Telegram send failed: %s", type(e).__name__)
        return False


def job_summary(markdown: str) -> None:
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if path:
        with open(path, "a", encoding="utf-8") as f:
            f.write(markdown + "\n")


def alert(title: str, lines: list[str]) -> None:
    body = "\n".join(lines)
    telegram(f"🔬 Crypto Research Labs — {title}\n\n{body}")
    job_summary(f"## {title}\n\n" + "\n".join(f"- {line}" for line in lines))
    log.info("%s: %s", title, body)

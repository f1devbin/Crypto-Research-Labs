"""Minimal HTTP client with retries (standard library only)."""
import logging
import time
import urllib.error
import urllib.request

from crl.config import USER_AGENT

log = logging.getLogger(__name__)


class HttpResult:
    def __init__(self, status: int, body: bytes):
        self.status = status
        self.body = body

    @property
    def ok(self) -> bool:
        return self.status == 200 and bool(self.body)


def get(url: str, timeout: int = 60, retries: int = 3) -> HttpResult:
    """GET with retries. 404/451/403/429 are returned immediately: retrying does not help."""
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return HttpResult(r.status, r.read())
        except urllib.error.HTTPError as e:
            if e.code in (403, 404, 429, 451):
                return HttpResult(e.code, b"")
            log.warning("HTTP %s for %s (attempt %d/%d)", e.code, url, attempt, retries)
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            log.warning("network error for %s: %s (attempt %d/%d)", url, e, attempt, retries)
        time.sleep(2 * attempt)
    return HttpResult(0, b"")

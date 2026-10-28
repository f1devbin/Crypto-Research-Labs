"""Screenshots of the built dashboard for the README: `python scripts/screenshots.py _site docs/screenshots`.
Needs `pip install playwright && python -m playwright install --with-deps chromium`."""
import functools
import http.server
import sys
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

SHOTS = [  # path, file, width, colour scheme, full page — English only
    ("", "dashboard", 1280, "dark", False),
    ("market.html", "market", 1280, "dark", False),
    ("research.html", "research", 1280, "dark", False),
    ("hypotheses/H-020.html#equity", "hypothesis", 1280, "light", False),
    ("coins/SOLUSDT.html", "coin", 1280, "dark", False),
    ("", "mobile", 390, "dark", False),
]


def main(site: str, out: str) -> None:
    Path(out).mkdir(parents=True, exist_ok=True)
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=site)
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{httpd.server_port}/"
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for path, name, width, scheme, full in SHOTS:
            ctx = browser.new_context(viewport={"width": width, "height": 860 if width > 500 else 844},
                                      color_scheme=scheme, device_scale_factor=1)
            page = ctx.new_page()
            page.goto(base + path, wait_until="networkidle")
            page.wait_for_timeout(800)
            page.screenshot(path=f"{out}/{name}.png", full_page=full)
            ctx.close()
        browser.close()
    httpd.shutdown()


if __name__ == "__main__":
    main(*sys.argv[1:3])

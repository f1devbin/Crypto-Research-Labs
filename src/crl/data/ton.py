"""Deposits of GRAM (prev. Toncoin) into Gate.io's TON deposit wallet, by sending wallet (H-033).

On TON, Gate.io takes deposits on one shared wallet (tonapi labels it "Gate.io", whitelisted): users send GRAM
straight to it and write their Gate account number in the comment. So the chain is just: Gate's deposit wallet ←
the user's wallet, with no sweeps. This module reads every text-comment transfer into that wallet from the public
toncenter v3 `messages` index (no key needed; TONCENTER_API_KEY raises the rate limit) and writes one row per
transfer:

  datasets/gram_gate_deposits.csv.gz   ts, wallet, deposit, value, first_sweep_ts

`wallet` and `deposit` are short SHA-256 ids of the raw addresses (as in everscale.py), so the file lists no
address. The index only answers newest-first queries reliably (time filters time out, ascending order is not
strict), so it is paged backwards with an `end_lt` cursor and de-duplicated by message hash. Kept: text-comment
transfers (Gate's deposit format) of at least `min_value` GRAM that did not bounce. Dropped: the deposit wallet
itself, other Gate.io-labelled accounts and addresses in CRL_EXCLUDE_WALLETS (raw `0:…` or user-friendly form).
There are no sweeps on TON, so `first_sweep_ts` is 0 (the study does not use it).
"""
import base64
import json
import logging
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import pandas as pd

from crl.data.everscale import addr_id

log = logging.getLogger(__name__)

MESSAGES = "https://toncenter.com/api/v3/messages"
GATE_TON = "0:b496b8f73b469ff06a2d89e62c4d70a103fc228c821537b49dff092060bc281f"
GATE_LABELLED = {GATE_TON}   # tonapi accounts named "Gate.io" (search, 2026-10-28): only the deposit wallet itself
PAGE = 1000


def raw(addr: str) -> str:
    """Normalise a TON address to lower-case raw form `wc:hex` (accepts raw or user-friendly base64)."""
    a = addr.strip()
    if ":" in a:
        wc, h = a.split(":", 1)
        return f"{int(wc)}:{h.lower()}"
    b = base64.urlsafe_b64decode(a + "=" * (-len(a) % 4))
    if len(b) != 36:
        raise ValueError(f"not a TON address: {addr}")
    wc = int.from_bytes(b[1:2], "big", signed=True)
    return f"{wc}:{b[2:34].hex()}"


def _messages(params: dict) -> list[dict]:
    from crl.config import USER_AGENT
    headers = {"User-Agent": USER_AGENT}
    if os.environ.get("TONCENTER_API_KEY"):
        headers["X-API-Key"] = os.environ["TONCENTER_API_KEY"]
    url = MESSAGES + "?" + urllib.parse.urlencode(params)
    for attempt in range(1, 9):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=120) as r:
                return json.loads(r.read())["messages"]
        except (urllib.error.URLError, TimeoutError, ConnectionError, ValueError, KeyError) as e:
            log.warning("toncenter messages failed (%s), attempt %d/8", e, attempt)
            time.sleep(4 * attempt)
    raise ConnectionError("toncenter unavailable")


def deposits(account: str, pause: float = 1.1, max_pages: int | None = None) -> list[dict]:
    """Every text-comment transfer into `account`, newest first, paged backwards by created_lt."""
    out, seen, end, pages = [], set(), None, 0
    while True:
        params = {"destination": account, "opcode": "0x00000000", "limit": PAGE, "sort": "desc"}
        if end is not None:
            params["end_lt"] = end
        msgs = _messages(params)
        fresh = [m for m in msgs if m["hash"] not in seen]   # ties on the boundary lt come back once more
        seen.update(m["hash"] for m in fresh)
        out += fresh
        pages += 1
        if len(msgs) < PAGE or not fresh or (max_pages and pages >= max_pages):
            return out
        end = min(int(m["created_lt"]) for m in msgs)
        if pages % 10 == 0:
            log.info("ton: %d pages, %d transfers, back to %s", pages, len(out),
                     pd.Timestamp(int(msgs[-1]["created_at"]), unit="s").date())
        time.sleep(pause)


def parse(msgs: list[dict], account: str, min_value: float = 1.0, exclude: set[str] | None = None) -> pd.DataFrame:
    """Non-bounced transfers of at least `min_value` GRAM into `account`, without excluded senders."""
    account = raw(account)
    drop = {account} | GATE_LABELLED | {raw(a) for a in (exclude or ())}
    rows = [(int(m["created_at"]), raw(m["source"]), int(m.get("value") or 0) / 1e9) for m in msgs
            if m.get("source") and not m.get("bounced")]
    df = pd.DataFrame(rows, columns=["ts", "src", "value"])
    df = df[(df["value"] >= min_value) & ~df["src"].isin(drop)]
    out = pd.DataFrame({"ts": df["ts"], "wallet": df["src"].map(addr_id), "deposit": addr_id(account),
                        "value": df["value"].round(9), "first_sweep_ts": 0})
    return out.sort_values(["ts", "wallet"]).reset_index(drop=True)


def build(account: str = GATE_TON, min_value: float = 1.0, max_pages: int | None = None) -> pd.DataFrame:
    exclude = {a for a in os.environ.get("CRL_EXCLUDE_WALLETS", "").split(",") if a.strip()}
    return parse(deposits(account, max_pages=max_pages), account, min_value, exclude)


def main(path: Path | None = None) -> int:
    from crl.config import DATASETS_DIR
    path = path or DATASETS_DIR / "gram_gate_deposits.csv.gz"
    df = build()
    df.to_csv(path, index=False)
    log.info("ton: %d transfers from %d wallets -> %s", len(df), df["wallet"].nunique(), path)
    return 0

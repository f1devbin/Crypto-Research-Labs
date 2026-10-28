"""Deposits into Gate.io's Everscale hot wallet, traced back to the wallets that made them (H-032).

Users send EVER to personal deposit addresses; Gate later sweeps each deposit address into its hot wallet.
So the chain is: hot wallet ← sweep ← deposit address ← the user's own wallet. This module reads it from the
public Everscale GraphQL API (no key) and writes one row per transfer into a deposit address:

  datasets/ever_gate_deposits.csv.gz   ts, wallet, deposit, value, first_sweep_ts

`wallet` and `deposit` are short SHA-256 ids of the addresses, so the file lists no address, while anyone can
rebuild it from the chain with this code. A deposit address is a sender to the hot wallet that forwarded at least
90 % of everything it sent out to the hot wallet; transfers that come from the hot wallet or from another deposit
address are Gate's own and are dropped. Addresses in CRL_EXCLUDE_WALLETS (comma-separated, e.g. the owner's)
never appear.

The API returns at most 50 messages per query, so histories are paged with the `blockchain` API's cursors (no
overlaps or gaps, unlike paging by created_at), and many addresses are packed into one request with aliases.
"""
import hashlib
import json
import logging
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

import pandas as pd

log = logging.getLogger(__name__)

API = "https://mainnet.evercloud.dev/graphql"
GATE_HOT = "0:3addd84bf73267312a477049fd9b8db761bf39c585c150f8e6f9451347af2b6c"
PAGE = 50
BATCH = 20
SWEEP_SHARE = 0.9
FIELDS = "id src dst value(format:DEC) created_at"


def addr_id(addr: str) -> str:
    return hashlib.sha256(addr.encode()).hexdigest()[:16]


def _q(query: str, retries: int = 5) -> dict:
    from crl.config import USER_AGENT
    body = json.dumps({"query": query}).encode()
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(API, data=body, headers={"Content-Type": "application/json",
                                                                  "User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=120) as r:
                res = json.loads(r.read())
            if "errors" in res:
                raise ValueError(res["errors"][0].get("message", "graphql error"))
            return res["data"]
        except (urllib.error.URLError, TimeoutError, ConnectionError, ValueError) as e:
            log.warning("everscale query failed (%s), attempt %d/%d", e, attempt, retries)
            time.sleep(3 * attempt)
    raise ConnectionError("Everscale GraphQL unavailable")


def _chunks(xs: list, n: int):
    for i in range(0, len(xs), n):
        yield xs[i:i + n]


def paged(queries: dict[str, tuple[str, str]]) -> dict[str, list[dict]]:
    """All messages of many (address, msg_type) pairs, oldest first, via the cursor-paged `blockchain` API.
    Every round asks for the next page of every unfinished pair, BATCH pairs per request."""
    out = {k: [] for k in queries}
    cursor: dict[str, str | None] = {k: None for k in queries}
    pending = list(queries)
    rnd = 0
    while pending:
        rnd += 1
        nxt = []
        for chunk in _chunks(pending, BATCH):
            parts = []
            for i, k in enumerate(chunk):
                addr, msg_type = queries[k]
                after = f', after:"{cursor[k]}"' if cursor[k] else ""
                parts.append(f'a{i}: account(address:"{addr}"){{messages(msg_type:[{msg_type}], first:{PAGE}{after})'
                             f'{{edges{{node{{{FIELDS}}}}} pageInfo{{hasNextPage endCursor}}}}}}')
            data = _q("{blockchain{" + " ".join(parts) + "}}")["blockchain"]
            for i, k in enumerate(chunk):
                acc = data.get(f"a{i}")
                if not acc:
                    continue
                page = acc["messages"]
                out[k] += [e["node"] for e in page["edges"]]
                if page["pageInfo"]["hasNextPage"]:
                    cursor[k] = page["pageInfo"]["endCursor"]
                    nxt.append(k)
        if rnd % 20 == 0 or not nxt:
            log.info("everscale: round %d, %d still paging", rnd, len(nxt))
        pending = nxt
    return out


def outgoing_sums(addrs: list[str]) -> dict[str, int]:
    """Total value (nanoEVER) each address has sent in internal messages."""
    out = {}
    for chunk in _chunks(addrs, BATCH):
        parts = [f'a{i}: aggregateMessages(filter:{{src:{{eq:"{a}"}}, msg_type:{{eq:0}}}}, '
                 f'fields:[{{field:"value", fn:SUM}}])' for i, a in enumerate(chunk)]
        data = _q("{" + " ".join(parts) + "}")
        for i, a in enumerate(chunk):
            out[a] = int(data[f"a{i}"][0] or 0)
    return out


def hot_incoming(hot: str) -> list[dict]:
    """Every internal transfer into the hot wallet, oldest first."""
    return paged({"hot": (hot, "IntIn")})["hot"]


def build(hot: str = GATE_HOT, exclude: set[str] | None = None, limit: int | None = None) -> pd.DataFrame:
    exclude = set(exclude or ()) | {a.strip() for a in os.environ.get("CRL_EXCLUDE_WALLETS", "").split(",")
                                    if a.strip()}
    inc = hot_incoming(hot)
    to_hot: dict[str, int] = {}
    first_sweep: dict[str, int] = {}
    for m in inc:
        to_hot[m["src"]] = to_hot.get(m["src"], 0) + int(m["value"])
        first_sweep[m["src"]] = min(first_sweep.get(m["src"], m["created_at"]), m["created_at"])
    senders = sorted(set(to_hot) - exclude - {hot})
    if limit:
        senders = senders[:limit]
    log.info("everscale: %d transfers into the hot wallet from %d senders", len(inc), len(senders))
    sent = outgoing_sums(senders)
    deposits = [s for s in senders if sent[s] > 0 and to_hot[s] >= SWEEP_SHARE * sent[s]]
    log.info("everscale: %d of them are deposit addresses (>= %.0f %% of outflow swept into the hot wallet)",
             len(deposits), 100 * SWEEP_SHARE)
    incoming = paged({s: (s, "IntIn") for s in deposits})
    gate = set(deposits) | {hot}
    rows = [(m["created_at"], m["src"], s, int(m["value"]) / 1e9, first_sweep[s])
            for s, ms in incoming.items() for m in ms if m["src"] not in gate and m["src"] not in exclude]
    df = pd.DataFrame(rows, columns=["ts", "src", "deposit", "value", "first_sweep_ts"])
    df["wallet"] = df["src"].map(addr_id)
    df["deposit"] = df["deposit"].map(addr_id)
    return df[["ts", "wallet", "deposit", "value", "first_sweep_ts"]].sort_values(["ts", "wallet"]).reset_index(drop=True)


def main(path: Path | None = None) -> int:
    from crl.config import DATASETS_DIR
    path = path or DATASETS_DIR / "ever_gate_deposits.csv.gz"
    df = build()
    df.to_csv(path, index=False)
    log.info("everscale: %d transfers from %d wallets into %d deposit addresses -> %s",
             len(df), df["wallet"].nunique(), df["deposit"].nunique(), path)
    return 0

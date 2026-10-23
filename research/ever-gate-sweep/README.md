# EVER: Gate.io hot-wallet watch

Preparation for a planned study of "smart wallets" on Everscale (EVER).

Exchanges collect coins from personal deposit addresses into one shared hot wallet (a *sweep*).
Once we see a sweep from a known Gate.io deposit address, the receiving address is Gate's hot wallet.
Its incoming transfers since 2022 are the raw data for the study:

1. collect deposits into the hot wallet since 2022;
2. pick "smart" wallets using 2022–2023 only;
3. test them on 2024+ against random wallets;
4. register the whole thing as a pre-registered hypothesis before looking at 2024+ data.

## Log

`sweep_log.csv` is appended once a week by a scheduled check (public Everscale GraphQL, `mainnet.evercloud.dev`).

| Column | Meaning |
|---|---|
| `date` | date of the check (UTC) |
| `swept` | `no` — no outgoing transfer yet; `yes` — the deposit address has sent coins out |
| `hot_wallet` | receiving address of the sweep (Gate.io hot wallet), empty until found |
| `sweep_date` | time of the sweep transfer (UTC), empty until found |

The deposit address itself and its balance are private and are not published.

# Workflows

| Workflow | File | Trigger | Needs |
|----------|------|---------|-------|
| CI | `.github/workflows/ci.yml` | push, PR | — |
| Research agents + dashboard | `.github/workflows/research-agents.yml` | daily 06:17 UTC; weekly Mon 07:41 UTC; push to site code; manual | Pages source = GitHub Actions; optional Telegram secrets |
| Hypothesis proposer | `.github/workflows/propose.yml` | 1st of month; manual | `ANTHROPIC_API_KEY` |

Every step is a single `crl` command, so you can run the same thing locally or from cron.

## Daily: data steward → regime watch

1. The `data/` cache is restored from `actions/cache` (key `crl-data-<run>`, newest prefix match).
2. `crl data refresh` fetches only what's missing, then checks every series.
   Price problems fail the job and send an alert. Problems in optional sources
   (sentiment, flows) are warnings.
3. `crl watch` computes each monitor in `config/watch.yaml`, assigns it to a band and
   compares it with yesterday's state (`data/state/watch_state.json`). An alert goes
   out **only** on a band change. The first run and unavailable sources stay silent.
4. `crl site` builds the dashboard into `_site/`: 7 languages (`/`, `/ru/`, `/es/`, `/pt/`, `/tr/`,
   `/vi/`, `/zh/`), one page per hypothesis, `sitemap.xml` with `hreflang` alternates, `robots.txt`,
   JSON-LD and `data.json`. The `deploy-pages` job publishes it to GitHub Pages.
   Set the repository variable `GOOGLE_SITE_VERIFICATION` to add the Search Console tag.
5. The cache is saved, including the watch state.

## Weekly: + runner → digest → commit

6. `crl run` executes every hypothesis that is `registered` or has a verdict, is
   `rerunnable`, and is due (`retest_every_days` since its last result). Each result
   goes to `results/<ID>/<date>.json` and `latest.json`, then `reports/RESULTS.md`
   and `reports/runs/<date>.md` are regenerated. An alert goes out when a verdict
   changes, when anything passes (with a reminder of the steps required before
   real money) and on errors.
7. `crl digest` writes `reports/digest/<year>-W<week>.md`. With an API key, Claude
   rewrites it into a short briefing. It's told to use only numbers from the input
   and never to recommend trades.
8. README screenshots are refreshed (`scripts/screenshots.py`), then `results/`, `reports/`,
   `hypotheses/` and `docs/screenshots/` are committed by `crl-bot`.

Manual run: *Actions → research-agents → Run workflow* (`force` re-tests everything).

## Monthly: proposer (optional)

`crl propose -n 3` sends Claude the rule catalogue, every existing spec (marked as
"do not repeat") and the current regime. The reply must be JSON. Each proposal is
schema-validated (rule type, parameter names, feature names) and checked against
the registry by fingerprint. Survivors become `status: draft` files with
`author: llm:<model>`, and the workflow opens a PR.

Guardrails:
- The runner never tests drafts.
- Only a human can lock a draft: `crl registry register H-0NN` writes the sha256.
- The model never sees results it could fit to: only specs and the current regime.

## Hypothesis format

```yaml
id: H-012
title: ETH long above SMA100, confirmed on 8 alts
status: draft            # draft → registered → passed | weak | rejected
family: trend            # trend | flows | sentiment | carry | intraday | other
created: '2026-10-14'
author: F1DevBin
rationale: Why this should work economically, written before testing.
retest_every_days: 90    # how often the runner re-tests it
rerunnable: true         # false for studies the engine can't reproduce (kept for the record)
spec:
  kind: timing_rule
  rule: {type: price_above_sma, window: 100}
  mode: long_flat        # long_flat (spot) | long_short
  fee: 0.001             # per side
  universe: [BNBUSDT, XRPUSDT, ADAUSDT, LTCUSDT, LINKUSDT, DOGEUSDT, XLMUSDT, TRXUSDT]
  periods:
    - {name: full, start: '2019-01-01'}
    - {name: recent, start: '2022-01-01'}
  significance: {method: circular_shift, n: 2000, alpha: 0.00625}   # optional
  criterion:
    min_wins: {full: 6, recent: 6}
    require_significance: false
```

A `rule_search` spec replaces `rule`/`periods` with:

```yaml
  kind: rule_search
  candidates:
    SMA50: {type: price_above_sma, window: 50}
    TSMOM90: {type: tsmom, lookback: 90}
  in_sample: {start: '2018-01-01', end: '2021-12-31'}
  out_of_sample: {start: '2022-01-01'}
  significance: {method: bootstrap, n: 400, alpha_family: 0.05}   # alpha = 0.05 / len(universe)
  criterion: {min_strict_wins: 2}
```

### Rules

| Type | Params | Long when |
|------|--------|-----------|
| `price_above_sma` | `window` | close > SMA(window) |
| `sma_cross` | `fast`, `slow` | SMA(fast) > SMA(slow) |
| `tsmom` | `lookback` | return over `lookback` days > 0 |
| `donchian` | `entry` | breakout above `entry`-day high, exit below `entry/2`-day low |
| `vol_target` | `target`, `lookback`, `cap` | always in; position = target ÷ realised volatility, capped (0…`cap`) |
| `day_of_week` | `days` (0 = Monday) | tomorrow's UTC weekday is in `days` |
| `turn_of_month` | `last`, `first` | tomorrow is one of the last `last` or first `first` days of the month |
| `asset_above_sma` | `asset`, `window` | **another** asset (e.g. BTCUSDT) closes above its SMA |
| `feature_threshold` | `feature`, `threshold`, `long_when` (`above`/`below`), `lag` | feature vs a fixed level |
| `feature_vs_rolling_quantile` | `feature`, `q`, `long_when` (`above`/`not_above`), `lookback`, `min_periods`, `lag` | feature vs its own rolling quantile |

Significance for `timing_rule`: `circular_shift` (any rule except calendar rules) or `permutation`
(calendar rules only: shuffles daily returns under the fixed calendar position; a circular shift
would just repeat the weekly pattern).

Features: `stablecoin_growth_7d`, `funding_btc_7d`, `fear_greed`, `etf_flow_btc_5d`.

### Data sources

| Series | Source | Notes |
|--------|--------|-------|
| Spot daily klines | data.binance.vision | monthly archives, plus daily files for the last two months |
| Coins not on Binance (EVER) | Gate.io API v4 | full history re-read each run (one request per year); listed in `OTHER_EXCHANGES` in `sources.py` |
| BTC funding | data.binance.vision (archive), fapi.binance.com, OKX as fallback | fapi answers 451 from US IPs |
| USDT/USDC supply | DefiLlama stablecoins API | |
| Fear & Greed | alternative.me | |
| BTC spot-ETF flows | BGeometrics | rate-limited (8 requests/hour); cached for 24 h |

If a source is unreachable, the steward falls back to the last cached copy and reports it as stale.

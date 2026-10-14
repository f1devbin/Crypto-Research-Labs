# Crypto Research Labs

Pre-registered, reproducible research on crypto trading ideas, run by a small set of
scheduled agents that keep the data fresh, re-test old ideas as markets change and
tell you when something actually moves.

> **Not financial advice.** This is a research tool. Nothing here places orders.
> A PASS verdict means "worth a closer look", not "trade this".

## Why this exists

This project grew out of a year of work on a Telegram signal bot (F1MEBOT). The bot
itself didn't hold up under testing: 7,649 live signals did *worse* than random once
replayed on real prices. The research process around it was costly in its own way:
every idea was a hand-written one-off script, data was downloaded again for each
study, results lived in loose text files, and rejected ideas were never re-checked.
[docs/INEFFICIENCIES.md](docs/INEFFICIENCIES.md) lists the six biggest problems and
what replaces each one.

## What we know so far

| ID | Hypothesis | Last verdict |
|----|------------|--------------|
| H-001 | Minute-level TA ensemble predicts 1–4 h direction | ❌ FAIL |
| H-002 | Inverted minute signals are profitable after fees | ❌ FAIL |
| H-003 | Best daily trend rule (chosen 2018–2021) beats buy-and-hold out of sample | ◐ WEAK |
| H-004 | Same, long/short futures | ◐ WEAK on Sharpe, but drawdowns down to −87 % |
| H-005 | SMA50 long/flat beats buy-and-hold on 8 independent coins | ❌ FAIL |
| H-006 | BTC long when stablecoin growth is above its 1-year median | ◐ WEAK |
| H-007 | BTC out of the market when funding is in its top 20 % | ❌ FAIL |
| H-008 | BTC out of the market when Fear & Greed ≥ 75 | ❌ FAIL |
| H-009 | BTC long only after positive 5-day spot-ETF flow | ◐ WEAK |
| H-010 | Stablecoin timing beats buy-and-hold on 8 independent coins | ❌ FAIL |
| H-011 | BTC funding carry (spot long + perp short) | ❌ FAIL (~1.5 %/yr recently) |

**No idea has passed so far.** Daily trend rules cut drawdowns but don't beat
buy-and-hold with statistical significance; most of the drawdown improvement comes
from spending less time in the market. Details are in [docs/FINDINGS.md](docs/FINDINGS.md).
The live table, updated by the runner, is in [reports/RESULTS.md](reports/RESULTS.md).

## The agents

| Agent | Schedule | What it does | It replaces |
|-------|----------|--------------|-------------|
| **Data steward** | daily | Updates a shared cache of Binance klines, funding, stablecoin supply, Fear & Greed and ETF flows; checks for gaps, stale series, duplicates and outliers | re-downloading data for every study; silent data holes |
| **Regime watch** | daily | Watches funding carry, stablecoin growth, sentiment, BTC trend and volatility; alerts **only when a reading moves to a different band** | nobody checking whether a rejected idea (e.g. carry) has become interesting |
| **Hypothesis runner** | weekly | Runs every due hypothesis with the shared protocol; stores JSON results; alerts on verdict changes | one hand-written 20–27 KB installer script per idea |
| **Digest** | weekly | Short summary of data health, regime and results (optionally rewritten by Claude) | reading scattered text reports |
| **Proposer** *(optional LLM)* | monthly | Claude drafts new hypotheses, which are schema-checked and de-duplicated against the registry, then opened as a PR | re-testing the same idea in new words |

The deterministic core needs no API key. The LLM layer can't run tests and can't
change verdicts. It can only open draft pull requests, and a human must lock a draft
(sha256) before it is ever tested. See [docs/WORKFLOWS.md](docs/WORKFLOWS.md).

## Quickstart

```bash
git clone https://github.com/f1devbin/Crypto-Research-Labs
cd crypto-research-labs
python -m venv .venv && . .venv/bin/activate
pip install -e ".[dev]"

pytest -q                 # engine tests: planted effects found, noise rejected, no look-ahead
crl registry check        # every hypothesis valid, locked, not a duplicate
crl data refresh          # build the local cache in ./data (first run: a few minutes)
crl run --force           # re-test all rerunnable hypotheses
crl watch                 # current regime -> reports/regime.md
```

### Adding a hypothesis

1. Copy a file in `hypotheses/` to the next free ID and set `status: draft`.
2. Describe the rule, universe, periods, significance test and pass criterion **before** looking at results.
3. `crl registry check`, then `crl registry register H-0NN`. This writes the spec's sha256.
   After that, any edit to the spec makes the registry check fail.
4. `crl run H-0NN`.

The format and the available rules are in [docs/WORKFLOWS.md](docs/WORKFLOWS.md#hypothesis-format).
The statistics are in [docs/METHODOLOGY.md](docs/METHODOLOGY.md).

## GitHub setup

Secrets (*Settings → Secrets and variables → Actions*). All of them are optional:

| Name | Kind | Purpose |
|------|------|---------|
| `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` | secret | alerts to Telegram (otherwise alerts go to the job summary only) |
| `ANTHROPIC_API_KEY` | secret | enables the proposer and the LLM digest rewrite |
| `CRL_LLM_MODEL` | variable | model override (default `claude-sonnet-5-5`) |

For the proposer to open PRs, turn on *Settings → Actions → General → Allow GitHub
Actions to create and approve pull requests*.

**Geoblocking:** GitHub runners are in the US. `fapi.binance.com` answers HTTP 451
there, so recent funding comes from OKX instead. Historical archives come from
`data.binance.vision`, which isn't blocked. Running locally outside the US needs
no workaround.

## Layout

```
src/crl/data/      http, sources (fetchers), store (cached series), integrity checks
src/crl/engine/    rules, backtest, statistics, protocol (spec -> verdict)
src/crl/agents/    data_steward, regime_watch, runner
src/crl/llm/       client (Anthropic API), proposer, digest
hypotheses/        the registry: one YAML per idea, sha256-locked
results/           machine-readable results per hypothesis (committed by the runner)
reports/           RESULTS.md, regime.md, data_health.md, runs/, digest/
config/watch.yaml  regime monitors and bands
```

## Lessons we kept

- **One clock: UTC.** A UTC vs UTC+3 mix-up in the old bot created a 30-minute
  blind window. Every timestamp here is UTC, and a decision at close *t* is applied to day *t+1*.
- **Stops live on the exchange.** A stop held in a bot's memory is no stop at all
  when the bot is down. The project doesn't trade. If you build on it, keep this rule.
- **Infrastructure follows evidence.** Prove the edge cheaply first, then automate.

## License

MIT. See [LICENSE](LICENSE).

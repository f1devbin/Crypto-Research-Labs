# Changelog

All notable changes. Versions follow [Semantic Versioning](https://semver.org/). The engine version is
stored with every result (`engine_version` in `results/*/latest.json`).

## [Unreleased]

### Added
- `research/ever-gate-sweep/`: weekly log of an on-chain watch for a Gate.io sweep of EVER, to find the exchange's hot wallet for the planned EVER "smart wallets" study.

## [0.3.0] - 2026-10-21

Plain-language dashboard, every rule checked on every coin, weekly digest and alerts in 7 languages,
a free LLM option, and a redesign that works on phones.

### Added
- Coin pages on the dashboard (`coins/<SYMBOL>.html`, 7 languages): price, changes, trend, volatility,
  12-month chart and today's state of each tested rule; a Coins table on the home page.
- Translated titles for H-012…H-019.
- Coin pages: distance from the highest close, value today of $100 invested a year ago, 90-day correlation with Bitcoin.
- Exchange flows (Coin Metrics community, BTC since 2011, ETH since 2015) stored in `datasets/exchange_flows.csv` and refreshed daily; BTC net-flow regime card; H-020/H-021 (heavy exchange deposits).
- Coin pages show today's state of every data-driven rule tested on the coin (e.g. H-020 on BTC); an "H-020 rule today" regime card alerts when the rule switches.
- H-022: forward replication of H-020 on as-published flow data (rows older than 14 days are never rewritten), first test 2027-10-15.
- Gram (GRAM, prev. Toncoin) from Gate.io: coin page, market breadth (now 13 coins), H-023 (SMA50 trend rule, same as H-018 for EVER).
- Market diagnosis in plain words on the home page (7 languages) and a diagnosis on every coin page.
- Coverage scan (`crl scan`, weekly): every tested rule on every coin with FDR control; matrix on the home page, per-rule tables on hypothesis pages, per-coin tables on coin pages, `reports/COVERAGE.md`.
- Sortable tables (coins, hypotheses, scan); forward-data progress bar for hypotheses waiting for new data (H-022).
- Cross-section studies (`kind: cross_section`, daily ranking vs an equal-weight basket, rotation null). H-024…H-026 from a ChatGPT proposal: all fail.
- Weekly digest page (`digest.html`, 7 languages) and the latest digest on the home page: the model writes each week's digest in every dashboard language; files in `reports/digest/<week>/`.
- Free LLM option: any OpenAI-compatible provider via `LLM_API_KEY` (+ `CRL_LLM_BASE_URL`), Groq by default.
- Setup page on the dashboard (`setup.html`, 7 languages): Telegram alerts, alert language, the optional AI model key (what it does, how to get it), running your own copy, all settings in one table.
- Telegram alerts in 7 languages: repository variable `TELEGRAM_LANG`; alerts end with a link to the dashboard in that language.
- Telegram test: *Run workflow* with `test_alert`, or `crl notify-test`.
- New look: IBM Plex Sans, deep-navy palette with high-contrast text, brand header, diagnosis panel with a signal meter, chip matrix; on phones every table turns into labelled cards and the matrix into one chip grid per rule (no horizontal scrolling).
- `replicates` field: a declared replication is not flagged as a duplicate.
- `test_after` field: a hypothesis is not run (even with `--force`) before its pre-registered start date.
- Market breadth monitor: share of the 13 coins above their 200-day average (regime card + alerts).
- Course for beginners on the website (`course.html`), 10 lessons in 7 languages, live numbers, Course structured data.

### Fixed
- `research-agents` stopped parsing after duplicated env keys; a test now loads every workflow with a strict YAML loader.
- Weekly Telegram message without a model is the plain-language diagnosis, not a dump of raw reports.
- LLM model is discovered from the provider's `/models` list (Groq retired the hard-coded one); the digest is written
  once in English and translated, retries rate limits and never publishes a cut-off answer.
- Diagnosis says "uptrend"/"downtrend" only with a clear majority of signals.

## [0.2.0] - 2026-10-14

First public release.

### Research engine
- Pre-registered hypotheses with SHA-256 lock and duplicate detection (`crl registry`).
- Protocol for `timing_rule` and `rule_search` studies: out-of-sample periods, fees, bootstrap,
  circular-shift and permutation tests with Bonferroni correction, confirmation on independent coins.
- Rules: SMA, SMA cross, time-series momentum, Donchian, volatility targeting, day of week,
  turn of month, cross-asset trend filter, feature thresholds and rolling quantiles.
- Data: Binance spot klines and funding archives, OKX funding fallback, Gate.io candles for coins
  not on Binance (EVER), DefiLlama stablecoins, Fear & Greed, BTC ETF flows.

### Agents (GitHub Actions)
- Data steward (daily), regime watch with alerts on band changes (daily), hypothesis runner and
  digest (weekly), optional Claude proposer that opens draft PRs (monthly).

### Dashboard
- Static site on GitHub Pages, 7 languages (en, ru, es, pt, tr, vi, zh), beginner explanations
  and glossary, one page per hypothesis with equity curves, sitemap with hreflang, JSON-LD.

### Hypotheses
- H-001…H-011 ported from F1MEBOT and re-tested.
- H-012…H-019 from the literature and user requests: volatility targeting, 1-week momentum,
  Monday and turn-of-month effects, BTC regime filter for altcoins, Everscale (EVER).
- Regime watch monitors EVER vs its 50-day average (the H-018 rule) with alerts on change.
- No hypothesis has passed so far. See [docs/FINDINGS.md](docs/FINDINGS.md).

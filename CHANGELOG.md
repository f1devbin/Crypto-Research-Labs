# Changelog

All notable changes. Versions follow [Semantic Versioning](https://semver.org/). The engine version is
stored with every result (`engine_version` in `results/*/latest.json`).

## [Unreleased]

### Added
- Daily model forecast for all 13 coins (idea by F1DevBin), pre-registered as H-027 (direction: chance of a rise
  above fees), H-028 (risk: chance of a bigger move than usual) on history from 2022, and H-029/H-030, their live
  replications. New study kinds `forecast` / `forecast_live` (`engine/forecast.py`): one pooled logistic
  regression, inputs lagged and z-scored on their own past, refitted monthly on known outcomes; Brier skill vs base
  rate with a circular-shift null; paper portfolio vs holding and vs a constant share, fees and Gate slippage
  included. Tests check that rewriting future prices and external data changes no past forecast.
- `crl forecast` appends today's forecasts to `datasets/forecast_log.csv` once per UTC day, freezes each month's
  model in `datasets/forecast_models/` and records 12:00 UTC prices; the workflow commits them at once so the time
  proves they came before noon. New page "Today's model forecast" (7 languages), linked from home and Research.
- `research-agents` manual runs can skip the weekly digest (`digest: false`).
- H-031 (registered 2026-10-28, live only from 2026-11-01): an improved direction model with a separate intercept
  per coin and Platt recalibration on a held-out year, designed after H-027 failed and therefore never judged on
  the history it was designed from. Forecast models get the options `coin_intercepts` and `calibration:
  platt_365`; live variants publish their own columns in the same log (`log_suffix`, here `_v2`) with their own
  frozen monthly models. The forecast page shows the improved model's chance of a rise and its live score.
  H-027…H-030 compute exactly as before (checked against a saved fingerprint of the engine's output).
- H-032 (registered 2026-10-28): EVER "smart wallets" on Gate.io. `crl data everscale` traces deposits on-chain
  (hot wallet ← sweep ← deposit address ← wallet) through the public Everscale GraphQL API with cursor paging and
  batched aliases, storing only short hashes of addresses (`datasets/ever_gate_deposits.csv.gz`; the owner's
  addresses are excluded via `CRL_EXCLUDE_WALLETS`). New study kind `wallet_deposits` (`engine/wallets.py`):
  dust, sweep-before-event, 7-day merge and service filters; selection on 2022–23 with no later prices; test from
  2024 against 1000 random matched wallet sets; exit-rule line with Gate fee and slippage. Tests include the
  null's calibration (about 5 % passes when no wallet knows anything) and that later prices never change the
  selection.
- H-033 (registered 2026-10-29): GRAM "smart wallets" on Gate.io, the H-032 question on TON. `crl data ton` reads
  text-comment transfers into Gate.io's shared TON deposit wallet (users add their account number as a memo, so
  there are no sweeps) from the public toncenter v3 index, paging back by logical time, and stores only short
  hashes of the senders (`datasets/gram_gate_deposits.csv.gz`; Gate.io-labelled accounts and the owner's addresses
  are dropped). `wallet_deposits` gets an optional `filters.min_usd`: a transfer counts only if it was worth that
  many dollars at the close of its day. The $500 size was picked by a rule fixed before counting
  (`scripts/h033_threshold.py`, counts only, no returns).

### Changed
- SEO (docs/SEO.md, target queries chosen 2026-10-29): page titles now start with what people search for and stay
  under 80 characters ("Crypto market today: trend, funding, Fear & Greed, stablecoins", "Free crypto course for
  beginners…"), descriptions are cut at a word boundary to 160 characters (90 in Chinese). Every hypothesis page is
  titled by a short search question in 7 languages ("Do Bitcoin exchange inflows predict price drops? (Pass)"),
  which also opens the page above the plain-words verdict; the precise statement stays the heading. Russian and
  Chinese coin pages use local coin names (Биткоин, 比特币). New `src/crl/i18n_seo.py`; tests check title and
  description lengths, absolute links on every page and a question for every hypothesis.

### Results
- H-027 (direction) failed: pooled Brier skill −0.009, overconfident. H-028 (size of the next move) passed:
  Brier skill +0.038, p < 0.001, skill on all 13 coins, well calibrated — the second pass in the project and the
  first that forecasts risk rather than direction.
- H-032 failed: 17 "smart" wallets picked on 2022–23 (EVER −8.7 % in the 7 days after their deposits) — only 6 still
  deposited from 2024, and after their 33 deposits EVER moved −1.5 % vs −3.7 % for random matched wallets
  (p = 0.93); the exit rule did not beat holding.
- H-033 failed like H-032: 36 "smart" wallets picked on 2023–24 (GRAM −3.8 % in the 7 days after their $500+
  deposits) — only 12 still deposited from 2025, and after their 144 deposits GRAM moved −0.5 % vs −1.9 % for
  random matched wallets (p = 0.77); the exit rule did not beat holding (Sharpe −1.80 vs −0.71).

### Fixed
- Canonical, hreflang, sitemap, Open Graph and JSON-LD links were relative ("/") since 2026-10-14: the unset
  Actions variable `CRL_SITE_URL` arrives as an empty string, which replaced the default address. Every page told
  search engines that its canonical address was the host root `f1devbin.github.io`, and the sitemap was invalid.
  The address now comes from `config.SITE_URL` (empty means the default), the build refuses a relative one, and
  Telegram alerts get the same fix.
- Home page: each idea that passed showed "the only one of N ideas"; the text now counts the passes, a risk
  forecast says it predicts the size of moves, not their direction, and each card carries its live re-check.
- The forecast-log commit failed when the data refresh had changed other tracked files (`git pull --rebase`
  refused); it now autostashes, and a failed commit no longer blocks the dashboard.
- The forecast log, noon prices and monthly models are reset to their committed versions after the Actions cache
  is restored: git is their only source, so a forecast that failed to be pushed is re-published (marked late after
  12:00 UTC) instead of being committed later with its earlier timestamp.

## [0.4.0] - 2026-10-28

A dashboard that answers one question per page, a 3D look that keeps high contrast, and daily updates that
start as soon as every data source has published.

### Changed
- Dashboard restructured into five pages, one question each, with the same five-item menu everywhere
  (Market · Research · Digest · New here? · About; a menu button on phones, languages in a drop-down).
  The home page now holds only the answer so far, a short market diagnosis and what passed; how-to-read and
  the glossary moved to the beginners' page, the hypotheses table and the rule × coin matrix to Research,
  methodology and data freshness to About. Nothing was removed; old home-page anchors redirect to the new pages.
- New visual style with depth: raised cards, a 3D field of hypothesis blocks (height = verdict), a 3D gauge for
  the diagnosis, verdict blocks that filter the hypotheses table. Text and charts stay flat; a test keeps text
  contrast at WCAG AAA (7:1) in both themes; motion respects "reduce motion".
- Market indicators are grouped by question (trend, nervousness, money flows) with explanations folded under
  "What is this?"; EVER is shown as a watched coin under Coins.
- Course lesson 3 describes the new pages; README screenshots are English only (`market`, `research`, `coin`).
- `research-agents` schedule: GitHub starts scheduled runs 4–7 hours late, so the workflow now wakes every hour
  from 00:17 to 11:17 UTC and a gate job (`crl.schedule_gate`) lets the first run that finds yesterday's data
  published by Binance, Coin Metrics, alternative.me and DefiLlama do the work (the weekly run on Mondays);
  the other runs exit in seconds. The 11:17 slot runs even if a source is late.

### Fixed
- The weekly digest was labelled with the week that had just started; it now shows the seven days it covers.

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

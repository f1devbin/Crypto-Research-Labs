# Changelog

All notable changes. Versions follow [Semantic Versioning](https://semver.org/). The engine version is
stored with every result (`engine_version` in `results/*/latest.json`).

## [Unreleased]

### Added
- Coin pages on the dashboard (`coins/<SYMBOL>.html`, 7 languages): price, changes, trend, volatility,
  12-month chart and today's state of each tested rule; a Coins table on the home page.
- Translated titles for H-012…H-019.
- Coin pages: distance from the highest close, value today of $100 invested a year ago, 90-day correlation with Bitcoin.
- Market breadth monitor: share of the 12 coins above their 200-day average (regime card + alerts).
- Course for beginners on the website (`course.html`), 10 lessons in 7 languages, live numbers, Course structured data.

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

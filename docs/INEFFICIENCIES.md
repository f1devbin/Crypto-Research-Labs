# The six biggest inefficiencies, and what replaced them

Audit of the F1MEBOT research process (2025–2026) before this repository existed.

## 1. Infrastructure was built before the edge was proven

A full trading bot came first: Telegram UI, database, signal engine, monitoring. Only
afterwards was its core assumption checked, and 7,649 live signals turned out worse
than random (H-001). Months of engineering went into a strategy with no edge.

**Fix:** research and execution are separate. This repository holds research only.
An idea must pass a pre-registered test before anyone builds tooling around it.

## 2. Every hypothesis was a one-off installer script

Each study was a 20–27 KB shell script with an embedded Python program, and each one
re-implemented loading, backtesting, statistics and reporting. That cost a day per
idea and made inconsistencies likely, because each copy of the method could drift.

**Fix:** one engine (`crl.engine`) and one protocol. A hypothesis is a ~40-line YAML
spec (`hypotheses/`), and **runner** executes all of them the same way.

## 3. Data was re-downloaded for every study

Each script pulled years of klines and auxiliary data again, nothing checked the
data, and a gap or duplicate in an archive went straight into the backtest.

**Fix:** **data steward** keeps one incremental cache (monthly archives are fetched
once, then only new days) and checks every series for gaps, staleness, duplicates,
non-positive prices and outliers. Results go to `reports/data_health.md`.

## 4. Results were scattered and only humans could read them

Verdicts lived in Russian-language text reports and chat messages. There was no list
of what had been tested, so new ideas risked repeating old ones in other words.

**Fix:** a machine-readable registry with JSON results per run (`results/`), a
generated table (`reports/RESULTS.md`) and duplicate detection by spec fingerprint.
Wording doesn't matter, so "SMA50 on BTC" can't be registered twice.

## 5. Rejected ideas were never re-checked

Funding carry (H-011) was rejected at ~1.5 %/yr. In 2021 the same trade paid
15 %. Nobody would have noticed it coming back. Likewise, a verdict could quietly go
stale as years of new data piled up.

**Fix:** **regime watch** tracks the conditions behind past rejections every day and
alerts only on band changes. **runner** re-tests each hypothesis on its
`retest_every_days` schedule and alerts when a verdict flips.

## 6. Time handling and risk control were fragile

The bot mixed UTC and UTC+3, which left a 30-minute window where signals were
generated against the wrong candle. Stop-losses lived in the bot's memory instead
of on the exchange.

**Fix:** UTC everywhere. Decisions are made at the daily close and applied to the
next day, a rule that tests enforce (`test_decision_applies_to_next_day_only`,
`test_price_rules_never_look_ahead`, `test_feature_rule_lags_publication`).
There is no execution code here. Anyone who builds on top of it should place
stops on the exchange.

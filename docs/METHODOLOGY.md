# Methodology

## Pre-registration

A hypothesis is written as a spec **before** results are seen. `crl registry register`
stores the sha256 of the canonical JSON of the spec (`prereg_sha256`). From then on,
`crl registry check` (and CI) fails if the spec changes. To change a test, create a
new hypothesis. That keeps the number of attempts honest.

## Timing

- Daily bars, UTC, Binance spot klines.
- The decision is made at close *t* and earns the return of day *t+1* (`position = decision.shift(1)`).
- External features are lagged by their publication delay (`lag`, default 1 day).
- Only days where the rule is fully defined are counted (no warm-up days as "flat").
- Fees are charged per unit of turnover: 0.1 % per side for spot, 0.05 % for futures taker.

## Study kinds

### `timing_rule`

One fixed rule on a universe, over one or more named periods. It passes when it beats
buy-and-hold (by Sharpe) on at least `min_wins[period]` assets in **every** period.
With `require_significance`, each win also needs a p-value below `alpha`.

### `rule_search`

Several candidate rules. For each asset, the best candidate by Sharpe is chosen on
the **in-sample** period only (2018–2021) and judged on the **out-of-sample** period
(2022+). The selection itself is part of what gets tested: the bootstrap re-runs the
same choice on synthetic data.

## Significance

- **Circular-shift null** (any rule). The position series is rotated against returns
  by 30 … n−30 days. This keeps the rule's exposure and autocorrelation but breaks
  its timing. p = share of shifts whose excess Sharpe ≥ the real one.
- **Bootstrap null** (price rules). Out-of-sample returns are resampled iid into
  synthetic price paths, with the real history kept as warm-up. The rule is run on
  each path. The null contains no predictable structure, so a trend rule only wins
  on synthetic data by luck.
- **Bonferroni:** `alpha = alpha_family / number of claims` (e.g. 0.05 / 4 for the
  four flow hypotheses H-006..H-009).

## Confirmation

A rule found on BTC/ETH/SOL is confirmed on eight coins that were not used to
design it: BNB, XRP, ADA, LTC, LINK, DOGE, XLM, TRX.

## Verdicts

| Verdict | Meaning |
|---------|---------|
| ✅ PASS | the pre-registered criterion is met |
| ◐ WEAK | beats buy-and-hold more often than not, but the bar is not met; never evidence by itself |
| ❌ FAIL | neither |

## Engine self-tests

`tests/test_protocol.py` plants a real trend effect and checks that the protocol
finds it, checks that the protocol finds nothing in random walks, and checks that
circular-shift p-values are roughly uniform under the null.
`tests/test_backtest.py` checks for look-ahead.

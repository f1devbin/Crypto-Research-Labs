# Findings

Historical results ported from F1MEBOT (2026). Each hypothesis file keeps them under
`history:`, and the runner adds new results under `results/<ID>/`.

## Intraday signals: dead end

- **H-001 ❌** Replaying 7,649 live signals (Jun–Sep 2026) on real prices gave a 33.9 %
  win rate at 2:1 reward:risk and EV −0.019 %/trade **before** fees. Direction was worse
  than random in all 12 TP/SL × timeout scenarios (−1.7 … −3.8 σ). A meta-labelling
  model reached AUC 0.53.
- **H-002 ❌** Inverting the signals wins by the same margin, but the best case
  is +0.024 %/trade against a 0.04 % minimum fee (futures maker). It is negative after
  fees everywhere.

At minute horizons, fees are larger than any edge the indicators carry.

## Daily trend: lower risk, no proven excess return

- **H-003 ◐** Out of sample (2022+), the in-sample pick beat buy-and-hold on BTC, ETH
  and SOL with lower drawdowns (SMA50 Sharpe: BTC 0.80 vs 0.51, ETH 0.82 vs 0.25,
  SOL 0.86 vs 0.39). None of these is significant after Bonferroni (best p 0.10–0.15).
- **H-004 ❌** In the long/short version, drawdowns reached −81 … −97 %. Shorts in bull
  phases destroy the result.
- **H-005 ❌** SMA50 on 8 independent coins beat holding on 4/8 (6 needed) over the
  full history and on 3/8 (4 needed) since 2022. The lower drawdown came from less time
  in the market, not from timing.

## Flows and sentiment: nothing significant

Four BTC timing rules, out of sample 2022+, circular-shift test at α = 0.0125:

| ID | Rule | Sharpe | Hold | p | In market |
|----|------|-------:|-----:|--:|----------:|
| H-006 ◐ | long when 7-d stablecoin growth > 1-y median | 0.68 | 0.50 | 0.100 | 46 % |
| H-007 ❌ | out when 7-d funding > 1-y 80th pct | 0.24 | 0.50 | 0.859 | 83 % |
| H-008 ❌ | out when Fear & Greed ≥ 75 | 0.45 | 0.50 | 0.575 | 93 % |
| H-009 ◐ | long after positive 5-d ETF flow (since 2024) | 0.76 | 0.79 | 0.239 | 60 % |

- **H-010 ❌** The stablecoin rule beat holding on 3/8 coins since 2022 and on 1/8 in
  2019–2021 (7/8 needed).

## Funding carry: real but small

- **H-011 ❌** Spot long + perp short, no leverage, half of the capital per leg. Yield on
  capital by year: 2020 +8.6 %, 2021 +15.3 %, 2022 +2.1 %, 2023 +3.9 %, 2024 +6.0 %,
  2025 +2.6 %, 2026 (9 mo) +1.1 %. The last 365 days returned about +1.5 %, which doesn't
  justify putting the full capital on one exchange. **Regime watch** tracks this and
  alerts if carry moves back above 8 %/yr.

## Re-run with this engine (2026-10-14)

The first scheduled run on GitHub Actions re-tested all eight rerunnable studies from
scratch, and every verdict except one matched F1MEBOT:

- H-006 reproduced exactly (Sharpe 0.68 vs 0.50, p = 0.10).
- H-005 reproduced exactly (4/8 full history, 3/8 since 2022).
- **H-004 is now WEAK instead of FAIL.** The pre-registered criterion counts Sharpe wins
  and significance. Long/short beats holding on BTC and SOL by Sharpe (not
  significantly), but drawdowns reach −63 … −87 %. F1MEBOT rejected it on drawdown;
  the engine reports it, but drawdown is not part of the criterion.
- H-010 since 2022: 5/8 coins beat holding (3/8 in F1MEBOT, which had less data); 7/8 are still needed.

Live numbers: [reports/RESULTS.md](../reports/RESULTS.md).

## Ideas from the literature (H-012…H-019, tested 2026-10-14)

All eight were written and locked before testing. Out of sample means after the cited paper's data
ended, or 2022+.

| ID | Idea and source | Result |
|----|-----------------|--------|
| H-012 ◐ | Volatility targeting at 30 %/yr (Man Group; Harvey et al. 2018) on BTC/ETH/SOL | Sharpe BTC 0.54 vs 0.50, ETH 0.32 vs 0.22, SOL 0.45 vs 0.36; drawdowns −47…−52 % vs −67…−95 %. p = 0.17–0.25, not significant |
| H-013 ◐ | Same on 8 independent coins | Beats holding on **8/8 since 2022**, but 5/8 since 2019 (6 needed): in the 2019–2021 bull run it gave up too much upside |
| H-014 ◐ | 1-week time-series momentum (Liu & Tsyvinski 2021) | SOL 0.79 vs 0.36 (p = 0.02, just above the 0.0167 bar); ETH 0.36 vs 0.22; BTC 0.08 vs 0.50. Not consistent |
| H-015 ❌ | Monday effect (Caporale & Plastun 2019) | Monday-only BTC: Sharpe 0.25 vs 0.65 holding since 2018. The effect did not persist after publication |
| H-016 ❌ | Turn of the month | Sharpe 0.53 vs 0.65, p = 0.13 |
| H-017 ❌ | Altcoins only while BTC > SMA200 | 7/8 better since 2022, but 1/8 since 2019: in 2019–2021 the filter left the market during alt rallies |
| H-018 ◐ | **Everscale (EVER)**: SMA50 trend rule, Gate.io, 0.2 % fee | −10 %/yr vs **−70 %/yr** holding since mid-2022; max drawdown −84 % vs −100 %. Sharpe 0.23 vs −0.17, p = 0.14 |
| H-019 ◐ | EVER only while BTC > SMA200 | −37 %/yr vs −70 %/yr, drawdown −98 %, p = 0.19 |
| H-023 ◐ | **Gram (GRAM, prev. Toncoin)**: SMA50 trend rule, Gate.io, 0.2 % fee | +17 %/yr vs −9 %/yr holding since 2023-06; max drawdown −56 % vs −85 %. Sharpe 0.55 vs 0.26, p = 0.11 |
| H-024 ❌ | Relative-strength rotation of 11 coins: top 3 by 1- and 3-day return, skip one-day jumps > 2.5 σ, only while BTC > SMA200 (ChatGPT proposal, daily) | Since 2020: Sharpe 0.76 vs 1.13 for an equal-weight basket, +32 %/yr vs +76 %/yr. Since 2022: 0.44 vs 0.41, drawdown −49 % vs −67 %, p = 0.04 (needed 0.0167). The filters, not the ranking, did the work |
| H-025 ❌ | Same ranking, no filters | Sharpe 0.91 vs 1.13 (2020+), 0.19 vs 0.41 (2022+), drawdown −78 %; the null rejects it (p = 0.003) only because it is *anti*-random in 2020-21 bull runs, not better than the basket |
| H-026 ❌ | 1-day reversal: hold the 3 biggest losers | −22 %/yr (2020+), −54 %/yr (2022+), 264 rebalances a year: whatever reversal exists is far smaller than 0.1 % fees |

**What it means.** Volatility targeting is the most promising so far. It never beat holding by a
significant margin, but it beat it on 11 of 11 coins since 2022 with roughly half the drawdown.
Re-testing it as data accumulates is exactly what the runner does every 90 days. Calendar effects
look like artefacts of their original samples. For EVER, every rule "beats" holding only because
holding lost almost everything. With ~$12k daily turnover, none of this is tradable at size.

Sources: [Man Group: Crypto, too hot to handle?](https://www.man.com/insights/crypto-too-hot-to-handle) ·
[Liu & Tsyvinski, Risks and Returns of Cryptocurrency (NBER w24877)](https://www.nber.org/system/files/working_papers/w24877/w24877.pdf) ·
[Quantpedia: Day of the week effect in crypto](https://quantpedia.com/the-day-of-the-week-effect-in-the-crypto-currency-market/) ·
[End-of-month effect in Bitcoin](https://valuelytica.substack.com/p/end-of-month-effect-in-bitcoin)

## Exchange deposits (H-020…H-022, tested 2026-10-14)

Idea by F1DevBin: coins moved to exchanges carry information about the next price move. Data: Coin Metrics
community exchange flows (BTC since 2011, ETH since 2015). Rule: stay out of the market for a day when the 7-day
net deposit to exchanges is above its trailing one-year 80th percentile.

| ID | Coin | Sharpe vs hold | CAGR vs hold | Max drawdown vs hold | In market | p (needed) |
|----|------|----------------|--------------|----------------------|-----------|------------|
| H-020 ✅ | BTC, 2022+ | 0.83 vs 0.50 | +30.6 % vs +13.1 % | −44 % vs −67 % | 83 % | 0.010 (< 0.025) |
| H-021 ◐ | ETH, 2022+ | 0.40 vs 0.22 | +6.6 % vs −7.8 % | −79 % vs −74 % | 80 % | 0.082 (< 0.025) |

**The first pass in the project, with two reasons for caution.**

1. **Look-ahead in the data.** Exchange addresses are often identified long after they were used, and data providers
   label them retroactively. Historical flows can therefore look more informative than they were in real time.
   H-022 repeats the exact rule on flows recorded day by day from 2026-10-15 and never rewritten later; it is
   tested on 2027-10-15.
2. **ETH only partly confirms it.** The direction is the same, but it is not significant, and the drawdown is not better.

Wallet-level analysis (which wallets deposit before moves) needs labelled exchange addresses; for Everscale it
waits for an Evercloud API key.

## Daily model forecast (H-027…H-030, registered 2026-10-28)

Idea by F1DevBin: an honest service publishes a daily view with a confidence level for every coin and keeps
score. One logistic regression shared by all 13 coins gives, every morning, two probabilities per coin: the next
day's return beats the round-trip cost (direction, H-027) and the next day's move is bigger than the coin's
usual one (risk, H-028). Inputs are prices to yesterday's close and external series to the day before, each a
rolling z-score of its own past year; the model is refitted monthly on outcomes already known. Scored by Brier
skill against each coin's base rate with a circular-shift null; a paper portfolio (share of the coin = chance of
a rise, 10-point band, fees and Gate slippage) is compared with holding and with a constant share.

History test, 2022-01-01 → 2026-10-26, 21 612 coin-days, walk-forward with monthly refits:

| ID | Question | Brier skill (pooled) | p (needed) | Coins with skill | Calibration |
|----|----------|----------------------|------------|------------------|-------------|
| H-027 ❌ | Next day's return beats the round-trip cost | −0.0089 | 0.012 (< 0.025, but skill must be above zero) | 5/13 | overconfident: says 53 %, happens 46 %; says 38 %, happens 44 % |
| H-028 ✅ | Next day's move bigger than the coin's usual one | +0.0383 | < 0.001 (< 0.025) | 13/13 | close: says 74 %, happens 74 %; says 84 %, happens 84 % |

- **Direction is not forecastable this way.** The forecasts carry a trace of information (rotating them in time
  makes them worse, hence p = 0.012), but they are biased and overconfident, so they lose to simply quoting each
  coin's base rate. The pooled model also ignores that Gate.io coins need a larger move to beat their costs, which
  costs it most on EVER (−0.10) and GRAM (−0.03). The paper portfolio held about half a position on average: much
  smaller drawdowns, but its Sharpe beat holding on only 4 of 13 coins; on Sharpe a constant half position is the
  same as holding, so there is no timing skill.
- **Improved direction model, live only (H-031).** Designed after seeing these results, so it may not be judged on
  them: a separate intercept per coin (fixes the Gate.io bias) and Platt recalibration on a held-out year (fixes the
  overconfidence). Its forecasts are published next to H-029's from 2026-11-01 (log columns `_v2`) and first
  tested on 2027-11-01 at α = 0.0125. Expectation written before any result: the bias goes, the skill moves to
  about zero.
- **The size of moves is forecastable**, on every coin and well calibrated: calm and nervous stretches persist.
  This is the second pass in the project and the first that is not a trading rule. It helps size positions and
  judge risk; it says nothing about which way the price will go.
- Live (H-029/H-030): every forecast is committed to `datasets/forecast_log.csv` before 12:00 UTC and scored from
  the 12:00 UTC price to the next day's; first test 2027-11-01. Today's numbers:
  [forecast page](https://f1devbin.github.io/Crypto-Research-Labs/forecast.html).
- Expectation written before any result: direction close to luck, risk with real skill (volatility clusters).
  That is what happened.

## EVER "smart wallets" on Gate.io (H-032, registered 2026-10-28)

Idea by F1DevBin. Gate.io's Everscale hot wallet was found from a withdrawal to the owner's wallet. Deposits are
traced on-chain: hot wallet ← sweep ← deposit address ← the user's wallet (`crl data everscale`, addresses stored only
as short hashes, the owner's excluded). Wallets whose 2022–23 deposits were followed by the biggest 7-day EVER drops
are the "smart" 20 %; from 2024 their deposits are compared with those of 1000 random matched sets of wallets.
Expectation written before any result: they were lucky, not smart.

Data: 34 327 transfers from 3 062 wallets into 2 528 deposit addresses, 2021-10 → 2026-08.

| Step | Result |
|------|--------|
| Selection 2022-01-01 → 2023-12-24 | 85 wallets with 5+ events (889 events); 17 "smart": EVER moved −8.7 % in the 7 days after their deposits vs −3.1 % after all eligible wallets' deposits |
| Test from 2024-01-01 | only 6 of the 17 still deposited (33 events): −1.5 % after them vs −3.7 % after random matched wallets; p = 0.93 (needed < 0.05) |
| Exit rule (out 7 days after a smart deposit, 0.4 % per side) | Sharpe −0.19 vs −0.08 holding; −73 %/yr vs −72 %/yr; in the coin 81 % of days |

❌ **Fail.** The wallets that looked best informed in 2022–23 did no better than random ones afterwards; most of
them stopped depositing. Deposits in general came before falls only because EVER kept falling (−72 %/yr from
2024). Wallet-level timing on this exchange shows no persistent skill.

## Bottom line

Apart from H-020 (pending its forward replication) and H-028 (risk, not direction), none of these ideas has a
statistically reliable edge after fees — including following "smart" on-chain wallets (H-032). Daily trend rules
are a risk-reduction tool, not an alpha source. Further work should only go to ideas
with a clear economic reason, tested on independent assets.

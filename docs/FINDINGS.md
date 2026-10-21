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

## Bottom line

Apart from H-020 (pending its forward replication), none of these ideas has a statistically reliable edge after fees. Daily trend rules
are a risk-reduction tool, not an alpha source. Further work should only go to ideas
with a clear economic reason, tested on independent assets.

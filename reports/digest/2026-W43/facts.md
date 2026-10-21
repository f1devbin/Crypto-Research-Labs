# Regime watch

Updated 2026-10-21 04:50 UTC

| monitor | value | band |
|---|---|---|
| BTC funding carry, yield on capital (30 d, annualised, after costs) | +1.8% | low |
| USDT+USDC supply growth (30 d) | -1.02% | contracting |
| Crypto Fear & Greed index | 63 | greed |
| BTC vs its 200-day average | +14.2% | above |
| BTC realised volatility (30 d, annualised) | 33% | calm |
| BTC net flow to exchanges (7 days) | +1,173 BTC | deposits |
| H-020 rule today: BTC in or out of the market | 1 | rule_in |
| Market breadth (coins above their 200-day average) | 62% | mixed |
| Everscale (EVER) vs its 50-day average | -23.4% | below |


# Data health
## Findings

Coverage scan (every tested rule on every coin, exploratory): Counts: works 0, better 70, worse 86, nodata 0

# Run 2026-10-14

### ✅ H-020 — BTC out of the market when 7-day net deposits to exchanges are in their top 20%

Verdict **PASS** · data to 2026-10-13 · engine 0.2.0 · run 2026-10-14T19:44:43Z

oos: wins 1/1 (need 1), beats buy-and-hold 1/1

| asset | period | rule | days | Sharpe | hold Sharpe | CAGR | hold CAGR | max DD | hold DD | in market | p |
|---|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | oos | fixed | 1747 | 0.83 | 0.50 | +31% | +13% | -44% | -67% | 83% | 0.0100 |

### ◐ H-021 — ETH out of the market when 7-day net deposits to exchanges are in their top 20%

Verdict **WEAK** · data to 2026-10-13 · engine 0.2.0 · run 2026-10-14T19:44:43Z

oos: wins 0/1 (need 1), beats buy-and-hold 1/1

| asset | period | rule | days | Sharpe | hold Sharpe | CAGR | hold CAGR | max DD | hold DD | in market | p |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ETHUSDT | oos | fixed | 1747 | 0.40 | 0.22 | +7% | -8% | -79% | -74% | 80% | 0.0820 |


# Run 2026-10-21

### ❌ H-024 — Relative strength rotation: hold the 3 strongest coins (1- and 3-day), skip extreme one-day jumps, only while BTC is above its 200-day average

Verdict **FAIL** · data to 2026-10-20 · engine 0.2.0 · run 2026-10-21T03:34:41Z

since_2020: does not beat the equal-weight basket; since_2022: beats the equal-weight basket

| asset | period | rule | days | Sharpe | hold Sharpe | CAGR | hold CAGR | max DD | hold DD | in market | p |
|---|---|---|---|---|---|---|---|---|---|---|---|
| PORTFOLIO | since_2020 | fixed | 2485 | 0.76 | 1.13 | +32% | +76% | -80% | -77% | 59% | 0.1019 |
| PORTFOLIO | since_2022 | fixed | 1754 | 0.44 | 0.41 | +11% | +6% | -49% | -67% | 52% | 0.0400 |

### ❌ H-025 — Plain momentum rotation: hold the 3 strongest coins over 1 and 3 days

Verdict **FAIL** · data to 2026-10-20 · engine 0.2.0 · run 2026-10-21T03:34:41Z

since_2020: does not beat the equal-weight basket; since_2022: does not beat the equal-weight basket

| asset | period | rule | days | Sharpe | hold Sharpe | CAGR | hold CAGR | max DD | hold DD | in market | p |
|---|---|---|---|---|---|---|---|---|---|---|---|
| PORTFOLIO | since_2020 | fixed | 2485 | 0.91 | 1.13 | +51% | +76% | -87% | -77% | 100% | 0.0030 |
| PORTFOLIO | since_2022 | fixed | 1754 | 0.19 | 0.41 | -10% | +6% | -78% | -67% | 100% | 0.0030 |

### ❌ H-026 — Short-term reversal: hold the 3 coins that fell the most yesterday

Verdict **FAIL** · data to 2026-10-20 · engine 0.2.0 · run 2026-10-21T03:34:42Z

since_2020: does not beat the equal-weight basket; since_2022: does not beat the equal-weight basket

| asset | period | rule | days | Sharpe | hold Sharpe | CAGR | hold CAGR | max DD | hold DD | in market | p |
|---|---|---|---|---|---|---|---|---|---|---|---|
| PORTFOLIO | since_2020 | fixed | 2485 | 0.17 | 1.13 | -22% | +76% | -99% | -77% | 100% | 0.9081 |
| PORTFOLIO | since_2022 | fixed | 1754 | -0.82 | 0.41 | -54% | +6% | -98% | -67% | 100% | 0.9900 |


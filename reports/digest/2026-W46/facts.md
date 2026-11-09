# Regime watch

Updated 2026-11-09 06:26 UTC

| monitor | value | band |
|---|---|---|
| BTC funding carry, yield on capital (30 d, annualised, after costs) | +3.0% | low |
| USDT+USDC supply growth (30 d) | -3.76% | contracting |
| Crypto Fear & Greed index | 29 | fear |
| BTC vs its 200-day average | +2.2% | above |
| BTC realised volatility (30 d, annualised) | 35% | calm |
| BTC net flow to exchanges (7 days) | -12,123 BTC | withdrawals |
| H-020 rule today: BTC in or out of the market | 1 | rule_in |
| Market breadth (coins above their 200-day average) | 23% | weak |
| Everscale (EVER) vs its 50-day average | -30.6% | below |


# Data health
## Findings

Coverage scan (every tested rule on every coin, exploratory): Counts: works 0, better 84, worse 111, nodata 0

# Run 2026-11-04

### ◐ H-034 — Hold coins when 7-day stablecoin growth tops its 2-year 80th percentile

Verdict **WEAK** · data to 2026-11-03 · engine 0.4.0 · run 2026-11-04T15:39:13Z

oos: wins 0/11 (need 1), beats buy-and-hold 10/11

| asset | period | rule | days | Sharpe | hold Sharpe | CAGR | hold CAGR | max DD | hold DD | in market | p |
|---|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | oos | fixed | 1768 | 0.53 | 0.46 | +9% | +11% | -21% | -67% | 15% | 0.1714 |
| ETHUSDT | oos | fixed | 1768 | 0.50 | 0.19 | +10% | -9% | -32% | -74% | 15% | 0.1224 |
| SOLUSDT | oos | fixed | 1768 | 0.42 | 0.33 | +9% | -12% | -51% | -95% | 15% | 0.2284 |
| BNBUSDT | oos | fixed | 1768 | 1.07 | 0.39 | +26% | +7% | -20% | -63% | 15% | 0.0060 |
| XRPUSDT | oos | fixed | 1768 | 1.10 | 0.50 | +40% | +9% | -31% | -72% | 15% | 0.0150 |
| ADAUSDT | oos | fixed | 1768 | 0.72 | -0.03 | +23% | -33% | -49% | -91% | 15% | 0.0465 |
| LTCUSDT | oos | fixed | 1768 | 0.64 | 0.09 | +17% | -19% | -31% | -73% | 15% | 0.0370 |
| LINKUSDT | oos | fixed | 1768 | 0.55 | 0.29 | +15% | -11% | -46% | -82% | 15% | 0.1104 |
| DOGEUSDT | oos | fixed | 1768 | 0.51 | 0.25 | +14% | -16% | -56% | -85% | 15% | 0.1369 |
| XLMUSDT | oos | fixed | 1768 | 0.68 | 0.29 | +26% | -10% | -46% | -76% | 15% | 0.0560 |
| TRXUSDT | oos | fixed | 1768 | 0.37 | 0.73 | +6% | +35% | -33% | -51% | 15% | 0.3478 |

### ❌ H-035 — Short coins when 7-day BTC funding tops its 3-year 90th percentile, long otherwise

Verdict **FAIL** · data to 2026-11-03 · engine 0.4.0 · run 2026-11-04T15:39:14Z

oos: wins 0/11 (need 1), beats buy-and-hold 0/11

| asset | period | rule | days | Sharpe | hold Sharpe | CAGR | hold CAGR | max DD | hold DD | in market | p |
|---|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | oos | fixed | 1763 | 0.30 | 0.49 | +2% | +13% | -67% | -67% | 100% | 0.8226 |
| ETHUSDT | oos | fixed | 1763 | 0.05 | 0.21 | -18% | -9% | -77% | -72% | 100% | 0.8101 |
| SOLUSDT | oos | fixed | 1763 | 0.20 | 0.35 | -22% | -10% | -94% | -94% | 100% | 0.7911 |
| BNBUSDT | oos | fixed | 1763 | 0.03 | 0.42 | -13% | +8% | -63% | -60% | 100% | 0.9970 |
| XRPUSDT | oos | fixed | 1763 | -0.19 | 0.51 | -39% | +11% | -94% | -72% | 100% | 0.9965 |
| ADAUSDT | oos | fixed | 1763 | -0.27 | -0.02 | -46% | -32% | -97% | -91% | 100% | 0.9390 |
| LTCUSDT | oos | fixed | 1763 | -0.21 | 0.11 | -35% | -17% | -91% | -73% | 100% | 0.9825 |
| LINKUSDT | oos | fixed | 1763 | -0.14 | 0.23 | -39% | -16% | -95% | -82% | 100% | 0.9720 |
| DOGEUSDT | oos | fixed | 1763 | 0.09 | 0.26 | -26% | -14% | -86% | -85% | 100% | 0.8621 |
| XLMUSDT | oos | fixed | 1763 | -0.44 | 0.29 | -55% | -10% | -98% | -75% | 100% | 0.9905 |
| TRXUSDT | oos | fixed | 1763 | 0.34 | 0.75 | -31% | +37% | -97% | -51% | 100% | 0.9885 |

### ❌ H-036 — Hold coins when 7-day stablecoin growth tops its 2-year 80th percentile — Gate.io coins (EVER, GRAM)

Verdict **FAIL** · data to 2026-11-03 · engine 0.4.0 · run 2026-11-04T15:39:15Z

gate: wins 0/2 (need 1), beats buy-and-hold 1/2

| asset | period | rule | days | Sharpe | hold Sharpe | CAGR | hold CAGR | max DD | hold DD | in market | p |
|---|---|---|---|---|---|---|---|---|---|---|---|
| EVERUSDT | gate | fixed | 1332 | -0.06 | -0.16 | -20% | -72% | -81% | -99% | 20% | 0.3683 |
| GRAMUSDT | gate | fixed | 1331 | 0.07 | 0.12 | -4% | -18% | -63% | -86% | 20% | 0.2934 |

### ❌ H-037 — Out of EVER and GRAM when 7-day BTC funding tops its 3-year 90th percentile — Gate.io line of H-035

Verdict **FAIL** · data to 2026-11-03 · engine 0.4.0 · run 2026-11-04T15:39:15Z

gate: wins 0/2 (need 1), beats buy-and-hold 0/2

| asset | period | rule | days | Sharpe | hold Sharpe | CAGR | hold CAGR | max DD | hold DD | in market | p |
|---|---|---|---|---|---|---|---|---|---|---|---|
| EVERUSDT | gate | fixed | 1332 | -0.20 | -0.16 | -72% | -72% | -99% | -99% | 95% | 0.6462 |
| GRAMUSDT | gate | fixed | 1331 | -0.17 | 0.12 | -31% | -18% | -88% | -86% | 95% | 0.9835 |


# Regime watch

Updated 2026-10-21 04:35 UTC

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

Checked 2026-10-21 04:35 UTC

| source | files | missing | errors |
|---|---|---|---|
| klines ADAUSDT | 122 | 0 | — |
| klines BNBUSDT | 127 | 0 | — |
| klines BTCUSDT | 130 | 0 | — |
| klines DOGEUSDT | 107 | 0 | — |
| klines ETHUSDT | 130 | 0 | — |
| klines EVERUSDT (gate) | 5 | 0 | — |
| klines GRAMUSDT (gate) | 4 | 0 | — |
| klines LINKUSDT | 113 | 0 | — |
| klines LTCUSDT | 126 | 0 | — |
| klines SOLUSDT | 94 | 0 | — |
| klines TRXUSDT | 120 | 0 | — |
| klines XLMUSDT | 121 | 0 | — |
| klines XRPUSDT | 121 | 0 | — |
| etf_flow_btc | 1 | 0 | — |
| exchange flows (Coin Metrics) | 1 | 0 | — |
| fear_greed | 1 | 0 | — |
| funding BTCUSDT | 81 | 0 | — |
| stable_usdt | 1 | 0 | — |
| stable_usdc | 1 | 0 | — |

## Findings

- **warn** `ADAUSDT`: 1 daily moves > 60%, e.g. 2025-03-02
- **warn** `BNBUSDT`: 2 daily moves > 60%, e.g. 2018-01-05
- **warn** `DOGEUSDT`: 3 daily moves > 60%, e.g. 2021-01-02
- **warn** `EVERUSDT`: 4 daily moves > 60%, e.g. 2023-01-30
- **warn** `LINKUSDT`: 1 daily moves > 60%, e.g. 2019-06-13
- **warn** `TRXUSDT`: 1 daily moves > 60%, e.g. 2024-12-03
- **warn** `XLMUSDT`: 2 daily moves > 60%, e.g. 2021-01-06
- **warn** `XRPUSDT`: 1 daily moves > 60%, e.g. 2023-07-13


# Coverage scan: every tested rule on every coin

Generated 2026-10-21T04:35:53Z · window 2022-01-01 → latest · fees included · Benjamini-Hochberg FDR q = 0.1 over 156 cells.

Exploratory, not verdicts. ✅ beats buy-and-hold and survives the false-discovery control; ↑ better Sharpe than holding but could be chance; ✗ worse than holding; — not enough data. **Bold** = the coin was in the original hypothesis. A ✅ on a new coin is a candidate for a new pre-registered hypothesis tested on future data.

| Rule | BTC | ETH | SOL | BNB | XRP | ADA | LTC | LINK | DOGE | XLM | TRX | EVER | GRAM |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| H-005 | ↑ | ↑ | ↑ | **↑** | **✗** | **↑** | **✗** | **✗** | **↑** | **✗** | **✗** | **↑** | **↑** |
| H-006 | **↑** | ↑ | ↑ | **↑** | **↑** | **✗** | **↑** | **↑** | **✗** | **↑** | **✗** | ✗ | ↑ |
| H-007 | **✗** | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| H-008 | **✗** | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ↑ | ↑ | ✗ |
| H-009 | **↑** | ↑ | ✗ | ↑ | ✗ | ✗ | ↑ | ✗ | ↑ | ✗ | ✗ | ✗ | ↑ |
| H-012 | **↑** | **↑** | **↑** | **↑** | **↑** | **↑** | **↑** | **↑** | **↑** | **↑** | **↑** | ✗ | ✗ |
| H-014 | **✗** | **↑** | **↑** | ✗ | ✗ | ✗ | ✗ | ✗ | ↑ | ↑ | ✗ | ↑ | ✗ |
| H-015 | **✗** | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| H-016 | **✗** | ✗ | ✗ | ✗ | ✗ | ↑ | ↑ | ✗ | ✗ | ✗ | ✗ | ↑ | ✗ |
| H-017 | ↑ | ↑ | ↑ | **↑** | **↑** | **↑** | **↑** | **↑** | **↑** | **↑** | **✗** | **↑** | ✗ |
| H-020 | **↑** | ↑ | ↑ | ↑ | ↑ | ↑ | ↑ | ↑ | ↑ | ↑ | ↑ | ✗ | ✗ |
| H-021 | ↑ | **↑** | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ↑ | ↑ | ✗ |

Counts: works 0, better 70, worse 86, nodata 0


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


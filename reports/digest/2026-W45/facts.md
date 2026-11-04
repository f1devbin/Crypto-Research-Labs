# Regime watch

Updated 2026-11-04 06:21 UTC

| monitor | value | band |
|---|---|---|
| BTC funding carry, yield on capital (30 d, annualised, after costs) | +2.7% | low |
| USDT+USDC supply growth (30 d) | -72.53% | contracting |
| Crypto Fear & Greed index | 34 | fear |
| BTC vs its 200-day average | +5.8% | above |
| BTC realised volatility (30 d, annualised) | 28% | calm |
| BTC net flow to exchanges (7 days) | -31,599 BTC | withdrawals |
| H-020 rule today: BTC in or out of the market | 1 | rule_in |
| Market breadth (coins above their 200-day average) | 54% | mixed |
| Everscale (EVER) vs its 50-day average | -29.5% | below |


# Data health
## Findings

Coverage scan (every tested rule on every coin, exploratory): Counts: works 0, better 71, worse 85, nodata 0

# Run 2026-10-28

### ❌ H-033 — Gate.io GRAM 'smart wallets': deposits of $500+ by wallets picked on 2023-24 foretell 7-day drops better than random wallets

Verdict **FAIL** · data to 2026-10-27 · engine 0.4.0 · run 2026-10-28T22:06:00Z

36 smart wallets of 183; from 2025-01-01 their 144 deposits were followed by a mean 7-day log return of -0.0050 vs -0.0196 for random matched wallets (p = 0.768, need p < 0.05); exit rule Sharpe -1.80 vs hold -0.71

- selection: start 2023-03-13, end 2024-12-24, wallets 183, smart 36, events 1565, all_mean 0.013326, smart_mean -0.039224
- test: start 2025-01-01, end 2026-10-20, events 144, smart 12, smart_mean -0.004982, random_mean -0.01964, p 0.768232, win False
- rule: days 665, start 2025-01-01, end 2026-10-27, sharpe -1.800317, cagr -0.382399, max_dd -0.591485, hold_sharpe -0.709164, hold_cagr -0.560568, hold_max_dd -0.792826, exposure 0.160902, trades_per_year 12.075188, p 0.934533, beats_hold False, win False


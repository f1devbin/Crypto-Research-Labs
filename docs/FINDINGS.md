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

## Bottom line

None of these ideas has a statistically reliable edge after fees. Daily trend rules
are a risk-reduction tool, not an alpha source. Further work should only go to ideas
with a clear economic reason, tested on independent assets.

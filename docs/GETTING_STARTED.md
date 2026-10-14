# Getting started (no finance or coding background needed)

> The full step-by-step **course for beginners** is on the website in 7 languages, with numbers updated
> every day: [English](https://f1devbin.github.io/Crypto-Research-Labs/course.html) ·
> [Русский](https://f1devbin.github.io/Crypto-Research-Labs/ru/course.html). This page is the short version.

## What is this project?

People keep inventing trading rules: "buy when the price crosses its average", "sell when everyone
is greedy". Most of these rules are never tested properly. Crypto Research Labs tests them the way
a scientist would:

1. **Write the idea down first**, as an exact rule with a clear pass/fail bar.
2. **Lock it** with a digital fingerprint (SHA-256), so nobody can change it after seeing results.
3. **Test it on years of real prices**, including fees, on a period the rule has never seen.
4. **Compare it with doing nothing smart**: buying the coin and holding it.
5. **Check it wasn't luck** with statistical tests.
6. **Re-test it automatically** as new data arrives.

## How to read the dashboard

Open the [live dashboard](https://f1devbin.github.io/Crypto-Research-Labs/) and pick your language at the top.

- **Market regime**: five numbers that describe today's market. Each card explains in one
  sentence what its number means. They describe the market. They don't tell you to buy or sell.
- **Hypotheses**: every idea tested so far, with a coloured verdict:
  - **Pass** (green): met the bar that was set in advance. Worth a closer, independent look.
  - **Weak** (amber): did a bit better than holding, but it could be luck.
  - **Fail** (red): didn't beat holding.
- Click a hypothesis to see its numbers and a chart of how $1 would have grown with the rule
  compared with simply holding.

## The words you will meet

| Word | Meaning |
|---|---|
| Buy-and-hold | Buy once and keep the coin. The baseline every rule must beat. |
| Sharpe ratio | Return per unit of bumpiness, per year. Higher is better; ~0.5 is normal for holding Bitcoin. |
| CAGR | Average growth per year. |
| Max drawdown | The worst fall from a peak. −50% means the account halved at some point. |
| p-value | The chance a result this good happens by luck. Lower is better. |
| Out of sample | Judged on data the rule was not chosen on. The only fair test. |
| SMA200 | The average price of the last 200 days. Above it usually means an uptrend. |
| Funding rate | A fee futures traders pay each other every 8 hours. |
| Stablecoin | A coin pegged to the US dollar (USDT, USDC). |

## I want to try it myself

You don't need to understand the code to run it.

**On GitHub (no installation):** fork the repository, then turn on *Settings → Pages → Source:
GitHub Actions* and click *Actions → research-agents → Run workflow*. Your own dashboard appears
about 20 minutes later.

**On your computer:** install [Python](https://www.python.org/downloads/) 3.10 or newer and
[git](https://git-scm.com/downloads), then follow the [Quickstart](../README.md#quickstart).

## I have an idea to test

Open an issue with the **Hypothesis idea** template. Describe the rule in plain words, and someone
can turn it into a hypothesis file. Or write the file yourself: [CONTRIBUTING.md](../CONTRIBUTING.md).

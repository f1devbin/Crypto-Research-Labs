# Security policy

Crypto Research Labs is a research project. It reads public market data, runs pre-registered
tests and publishes the results. It has no accounts, no payments and no trading with real money.

## Supported versions

Only the latest `main` and the latest release tag are supported. Older commits stay for
reproducibility, they are not maintained.

## In scope

- The Python code in `src/`, `scripts/` and `tests/`: data download, backtest engine, site build.
- The GitHub Actions workflows: secrets handling, permissions, third-party actions, supply chain.
- The published site: generated HTML and JS, links, anything where outside data ends up in markup.
- The integrity of the research: changing locked hypotheses, results or digests after the fact.

## Out of scope

- A research result that looks wrong. Methodology and data questions belong in
  [Discussions](https://github.com/f1devbin/Crypto-Research-Labs/discussions).
- GitHub itself, the data providers (Binance, Coin Metrics, Gate.io, Alternative.me, DefiLlama),
  browsers and GitHub Pages.
- Denial of service, social engineering, physical access, and anything that needs the owner's
  private keys.

## How to report

Use GitHub's private vulnerability reporting: open the repository's **Security** tab and press
**Report a vulnerability**. It opens a private advisory that only the maintainers can read.

Please do **not** open a public issue with the details. If the button is not available, open an
issue titled "Security contact" without any details and wait for a private channel.

Include what is affected (file, workflow or URL), how to reproduce it, what an attacker gains,
and the commit or release you tested. A proof of concept helps; an exploit against production
does not.

## What to expect

- An acknowledgement within 7 days.
- An assessment and, for a valid report, a fix in a private fork or branch.
- Public disclosure together with the fix, with credit if you want it.
- No bug bounty: this is an unfunded project.

## Safe harbour

Good-faith research on your own copies is welcome. Do not read other people's data, do not
change results, and do not publish details before a fix is available. We will not pursue legal
action for research that follows this policy.

## Secrets

The repository stores no API keys, exchange credentials or wallet private keys. Workflows get
their secrets from GitHub Actions secrets; the local runner gets them from its own environment.
The project never asks for seed phrases or private keys: anyone who does is impersonating it.
The owner's wallet addresses are never published.

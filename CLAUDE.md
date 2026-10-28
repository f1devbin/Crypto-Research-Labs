# CLAUDE.md — instructions for Claude working on Crypto Research Labs

Owner: Max (f1devbin). Talk to him in **Russian**, short and to the point, technical names in English.
End every reply with one line «Готово». Do only what he asks; small fixes along the way and keeping docs current are fine.
Anything that runs on its own (scheduled tasks, new repos, new services) — propose in one line, wait for «да».

## What the project is

Open, pre-registered crypto trading research. Every idea (hypothesis) is written as a YAML spec, locked with a
SHA-256 hash *before* it is tested, then tested by a fixed engine and re-tested automatically on new data by
GitHub Actions. Results, a market diagnosis and a beginners' course are published as a static dashboard in 7
languages: <https://f1devbin.github.io/Crypto-Research-Labs/> (en at root, `/ru/ /es/ /pt/ /tr/ /vi/ /zh/`).

Current state: 32 hypotheses (H-001…H-032), two passed: H-020 (BTC exchange deposits; H-022 is its forward
replication, first test 2027-10-15) and H-028 (the daily model forecasts the size of the next move, not its
direction — H-027 failed). H-029/H-030 replicate H-027/H-028 live (forecast page, published before 12:00 UTC,
first test 2027-11-01); H-031 is a live-only improved direction model (coin intercepts + Platt, log columns `_v2`).
H-032 (failed: the "smart" 2022–23 wallets were no better than random from 2024): EVER "smart wallets" on Gate.io (on-chain deposits, `engine/wallets.py`, data `crl data everscale` →
`datasets/ever_gate_deposits.csv.gz`; hot wallet 0:3addd84b…; never store or publish the owner's own addresses). Version 0.4.0. Honest negative results are the point of the project.

## Layout

| Path | What |
|---|---|
| `hypotheses/H-0xx.yaml` | one spec per idea; `status`, `spec`, `prereg_sha256`, optional `test_after`, `replicates` |
| `src/crl/engine/` | `rules.py` (timing rules), `protocol.py` (timing_rule, rule_search, cross_section, forecast), `cross.py`, `backtest.py`, `stats.py`, `forecast.py` (pooled daily model, Brier skill, paper portfolio, live log) |
| `src/crl/registry.py` | validation, SHA-256 lock, duplicates, `is_due` |
| `src/crl/agents/` | `data_steward` (data refresh + integrity), `regime_watch` (monitors, alerts), `runner` (due hypotheses) |
| `src/crl/data/` | `sources.py` (Binance vision, Gate.io for EVER/GRAM, OKX funding, Coin Metrics flows, DefiLlama, alternative.me, BGeometrics), `store.py`, `everscale.py` (Gate.io EVER deposits traced on-chain, H-032) |
| `src/crl/scan.py` | coverage scan: every tested timing rule × every coin, BH-FDR q=0.10 → `reports/coverage.json`, `COVERAGE.md` |
| `src/crl/llm/` | `client.py` (OpenAI-compatible: Groq via `LLM_API_KEY`, model auto-discovered; or Anthropic), `digest.py` (weekly digest: English from facts, then translated), `proposer.py` (monthly drafts) |
| `src/crl/site.py`, `site_render.py` | dashboard build (`crl site` → `_site/`): home, market, research, about, hypothesis pages, coin pages, course, setup, digest |
| `src/crl/i18n.py`, `i18n_diag.py`, `i18n_alerts.py`, `course.py`, `setup_guide.py` | all UI text, 7 languages |
| `config/watch.yaml` | regime monitors and bands |
| `results/`, `reports/`, `datasets/` | written by the bot (`crl-bot`) on the weekly run; don't hand-edit. `datasets/forecast_log.csv`, `noon_prices.csv`, `forecast_models/` are written daily by `crl forecast` and must never be edited |
| `docs/` | FINDINGS, METHODOLOGY, WORKFLOWS, GETTING_STARTED, INEFFICIENCIES |

## Commands

```bash
pip install -e . && python -m pytest -q        # all tests must pass before any PR
crl registry check                              # validate every hypothesis
crl registry register H-0xx                     # lock a draft (writes registered date + sha256)
crl data refresh | crl watch | crl forecast | crl run [ids] [--force] | crl scan | crl digest | crl site | crl notify-test
```

Real data is not available in the cloud container (network allowlist). Run studies on GitHub Actions
(`research-agents` → Run workflow, input `full=true`) or on skynuc (`/var/www/crypto-research-labs`, venv `.venv`).
For site previews use `MemoryStore` with `tests.conftest.random_walk` and Playwright screenshots.

## Research rules (never break these)

1. A registered spec is never edited. The hash check fails, and editing after seeing results is exactly what the
   project exists to prevent. To change an idea: new hypothesis id, `replicates:` if it is a replication.
2. Register (and merge) the spec **before** the first run. Write the rationale before looking at results.
3. Several related hypotheses tested together share alpha (Bonferroni), e.g. 0.05/3 = 0.0167.
4. Coverage-scan hits are exploratory only; a ✓ on a new coin becomes a new hypothesis with `test_after` in the future.
5. Fees always included (Binance 0.1 %, Gate 0.2 %). No look-ahead: features lag ≥ 1 day; add a test for any new rule
   that changing the future does not change past decisions.
6. Never recommend trades in any text, digest or alert. The model only retells numbers from reports.
7. Every new study uses all coins we track (13 now: BTC, ETH, SOL, BNB, XRP, ADA, LTC, LINK, DOGE, XLM, TRX,
   EVER, GRAM, plus any added later), never a hand-picked subset. Correct for multiple testing across coins;
   Gate coins (EVER, GRAM) are reported on their own line with the Gate fee and slippage.

## Dashboard rules

- Every string in all 7 languages (tests check completeness). English is the fallback, never leave a key only in English.
- Accessibility first: high contrast, no grey text on dark backgrounds, no horizontal page scroll; on phones tables
  become labelled cards (`responsive_tables`), the rule × coin matrix becomes chip grids.
- Design tokens live in `site_render.CSS` (IBM Plex Sans, deep navy). Check desktop and 390 px screenshots before a PR.
- SEO: prerendered HTML, hreflang, sitemap, JSON-LD (Dataset needs creator + license). The host root
  `f1devbin.github.io` (separate repo) owns `robots.txt`, which lists this project's sitemap.

## Git workflow

- Every change goes through a branch → PR → merge (GitHub achievements: Pull Shark). Never push to `main` directly.
- Commit trailer: `Co-Authored-By: Claude <noreply@anthropic.com>`; PR body ends with the Claude Code line.
- Keep README.md, CHANGELOG.md (`[Unreleased]`) and docs/FINDINGS.md current in the same PR as the change.
- Workflows: `ci` (tests), `research-agents` (daily data/watch/site; weekly run/scan/digest/commit; deploys Pages),
  `propose` (monthly LLM drafts as PR), `release` (manual: tag from pyproject version on the merge commit).
  `tests/test_workflows.py` rejects duplicated YAML keys — GitHub silently refuses such workflows.
- Release: bump `pyproject.toml`, `src/crl/__init__.py`, user agent in `config.py`; move `[Unreleased]` to a dated
  section; PR; then dispatch `release`.

## Settings (Settings → Secrets and variables → Actions)

Secrets: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `LLM_API_KEY` (Groq), optional `ANTHROPIC_API_KEY`.
Variables: `TELEGRAM_LANG=ru`, optional `CRL_LLM_MODEL`, `CRL_LLM_BASE_URL`, `GOOGLE_SITE_VERIFICATION`, `CRL_SITE_URL`.
Never print or commit secrets; if one appears in a screenshot, say so and suggest rotating it.

## Around the project

- A copy of the repo runs on the owner's home server for local checks; servers are reached through ssh-mcp profiles
  he has configured. Don't delete or reboot anything without «да»; back up configs before editing.
- Open tasks, only when he says so:
  - `SECURITY.md` and how to turn on private vulnerability reporting (Settings → Code security).
  - GitHub Developer Program: he registers himself; Claude prepares the project description (it uses the GitHub API
    in workflows: `gh release`, `gh pr`).
  - Promotion for stars: texts for Practical AI, Habr, Reddit r/algotrading, Show HN; PRs to awesome-lists
    (awesome-quant and similar).
  - Discussions are on: answer beginners' questions about the course.
  - Google Search Console API report via a service account, once he creates the secret `GSC_SERVICE_ACCOUNT`.
  - Better digest prompt (the free model sometimes misreads cause and effect).
- No automated commits, PRs or posts made only for GitHub achievements.

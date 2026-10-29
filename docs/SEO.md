# SEO: what the dashboard should be found by

Chosen on 2026-10-29. The site's unique content is a set of pre-registered tests of popular trading ideas with
honest verdicts. Head terms ("bitcoin price", "crypto trading") are out of reach for a young GitHub Pages site. But
questions like "does X work?" are answered today mostly by blog, Medium and Substack posts that use no
out-of-sample test and often no fees. A page with a real test and a verdict can rank for those questions, in
English and in Russian first (the other five languages follow the same plan).

## Target queries → pages

| Query cluster (en / ru) | Page |
|---|---|
| do crypto trading strategies work, crypto trading strategy backtest / проверка торговых стратегий для криптовалют, бэктест | home, Research |
| do exchange inflows predict bitcoin price / приток биткоинов на биржи и падение цены | H-020, H-021, H-022 |
| fear and greed index strategy backtest / индекс страха и жадности стратегия | H-008, Market |
| funding rate strategy, funding rate arbitrage / фандинг, арбитраж фандинга | H-007, H-011 |
| bitcoin 200-day moving average strategy, 50-day moving average crypto / 200-дневная скользящая средняя биткоин | H-005, H-017–H-019, H-023, coin pages |
| bitcoin ETF flows, stablecoin supply and bitcoin price / потоки в ETF, стейблкоины и цена биткоина | H-009, H-006, H-010 |
| monday effect bitcoin, turn of the month effect / эффект понедельника биткоин | H-015, H-016 |
| crypto momentum strategy, volatility targeting, short-term reversal / моментум, таргетирование волатильности | H-012–H-014, H-024–H-026 |
| RSI MACD strategy backtest crypto / стратегия RSI MACD | H-001, H-002 |
| crypto forecast today, bitcoin volatility forecast / прогноз криптовалют на сегодня | Forecast, H-027–H-031 |
| smart money wallets crypto / умные деньги, кошельки | H-032, H-033 |
| crypto market today, fear and greed today / крипторынок сегодня | Market |
| free crypto course for beginners / бесплатный курс по криптовалюте для начинающих | Course |
| backtest overfitting, p-hacking, pre-registered backtest / подгонка под историю | About |
| {coin} trend, 200-day average, volatility / биткоин тренд сегодня | coin pages (Russian and Chinese pages use local coin names) |

## Rules for new pages

- Titles put the query words first and stay at most 80 characters (tests check every page). Inner pages carry no
  brand suffix: search results show the site name separately.
- Descriptions: `site_render.clip` cuts them at a word boundary to 160 characters (90 in Chinese).
- Every hypothesis needs a question in `src/crl/i18n_seo.py` (`QUESTIONS`), in all 7 languages (tests check it).
  Write it the way people search ("Does X work on Y?"), at most 66 characters, and never as advice. The question
  is the page title and the first line of the page; the precise statement stays the H1.
- Canonical, hreflang, sitemap, Open Graph and JSON-LD links are absolute, built from `config.SITE_URL`. An empty
  `CRL_SITE_URL` falls back to the default. (From 2026-10-14 to 2026-10-29 they were relative, so every canonical
  pointed at the host root `f1devbin.github.io` and the sitemap was invalid.)

## Outside the repository (owner)

- Google Search Console (the project URL is verified by the `google…html` file in `site/`): resubmit
  `https://f1devbin.github.io/Crypto-Research-Labs/sitemap.xml` and request indexing of the home page, Research,
  Forecast and the H-020 / H-028 pages.
- Yandex Webmaster (the host root has a `yandex-verification` tag): add the same sitemap. Bing Webmaster Tools can
  import the site from Search Console.
- GitHub repository "About": a description with the main queries and topics (backtesting, cryptocurrency,
  trading-strategies, pre-registration, quantitative-finance).
- Links: the open promotion tasks in CLAUDE.md (Habr, Reddit r/algotrading, Show HN, awesome-quant) are the main
  source of links; each H-0xx page is a ready answer to link to.

"""Dashboard translations. English is the source and the fallback for any missing key.

Languages are chosen by crypto adoption and audience size: English (global), Russian (CIS),
Spanish (Latin America, Spain), Portuguese (Brazil), Turkish, Vietnamese, Chinese.
Engine output (summaries, rationales, specs) stays in English — it is technical and
generated; every page says so and gives a plain-language verdict in the page language.
"""

LANGS = {  # code: (native name, html lang / hreflang, og:locale)
    "en": ("English", "en", "en_US"),
    "ru": ("Русский", "ru", "ru_RU"),
    "es": ("Español", "es", "es_ES"),
    "pt": ("Português", "pt-BR", "pt_BR"),
    "tr": ("Türkçe", "tr", "tr_TR"),
    "vi": ("Tiếng Việt", "vi", "vi_VN"),
    "zh": ("中文", "zh-Hans", "zh_CN"),
}
DEFAULT = "en"
VERDICT_WORD_KEYS = {"PASS": "Pass", "WEAK": "Weak", "FAIL": "Fail"}

T = {
# ---------------------------------------------------------------- English
"en": {
 'nav_coins': 'Coins',
 'coins_title': 'Coins',
 'coins_intro': "Every coin used in the studies: today's price, trend and volatility. Open a coin to see its chart and what each tested rule says about it today.",
 'th_coin': 'Coin',
 'th_price': 'Price',
 'th_7d': '7 days',
 'th_30d': '30 days',
 'th_vs200': 'vs 200-day average',
 'th_vol': 'Volatility (30 d)',
 'coin_title': '{name} ({ticker}): price, trend, volatility and tested rules',
 'coin_desc': '{name} ({ticker}) today: {price}, {ch30} in 30 days, {vs200} against its 200-day average. Trend, volatility and the state of every tested trading rule, updated daily.',
 'coin_lead': 'Daily closes from {exchange} (UTC). Last day: {date}.',
 'back_coins': '← All coins',
 'chart12_h': 'Last 12 months',
 'close_label': '{ticker} close',
 'sma50': '50-day average',
 'stats_h': 'Numbers',
 'st_price': 'Price',
 'st_7d': 'Change, 7 days',
 'st_30d': 'Change, 30 days',
 'st_1y': 'Change, 1 year',
 'st_sma50': 'vs 50-day average',
 'st_sma200': 'vs 200-day average',
 'st_vol': 'Volatility (30 days, yearly)',
 'signals_h': 'What the tested rules say today',
 'signals_warn': "These are today's states of rules from the hypotheses. None of them has passed its test, so they are not buy or sell signals. They show what each rule would do, so you can watch how it behaves.",
 'sig_sma50': 'Trend: price above its 50-day average',
 'sig_mom7': '1-week momentum: price higher than 7 days ago',
 'sig_vol': 'Volatility targeting (30%/yr): share of a full position',
 'sig_btc': 'Market regime: Bitcoin above its 200-day average',
 'state_in': 'in the market',
 'state_out': 'out of the market',
 'th_rule': 'Rule',
 'th_state': 'Today',
 'th_tested_in': 'Tested in',
 'coin_studies_h': 'Studies that include this coin',
 'no_studies': 'This coin is only used as a market filter.',
 'thin_note': 'This coin trades on {exchange}, not Binance. Liquidity is low, so prices can jump on small trades.',
 'th_peak': 'From peak',
 'th_100': '$100 a year ago →',
 'st_peak': 'From the highest close since {since} ({peak} on {date})',
 'st_100': '$100 invested a year ago is now',
 'st_corr': 'Correlation with Bitcoin (90 days)',
 'corr_note': 'Correlation: 1 = moves exactly with Bitcoin, 0 = no link, −1 = moves opposite. Most coins are above 0.6, so owning several of them is not much safer than owning one.',
 "plain_scheduled": 'Data is being collected. The pre-registered test runs on {date}, once a year of data has accumulated.',
 "sig_rule": 'Rule {id}',
 "site_title": "Crypto Research Labs: open, pre-registered crypto trading research",
 "site_desc": "Open, pre-registered crypto trading research: {verdict} Live market regime (BTC funding carry, "
              "stablecoin supply, Fear & Greed, trend, volatility) and every hypothesis re-tested automatically.",
 "hyp_desc": "{id} ({verdict}): {title}. {plain}",
 "nav_dashboard": "Dashboard", "nav_new": "New here?", "nav_regime": "Market regime", "nav_hyp": "Hypotheses",
 "nav_glossary": "Glossary", "nav_method": "Methodology", "lang_label": "Language",
 "updated": "Updated {t} · data from Binance, OKX, DefiLlama, alternative.me, BGeometrics",
 "h1": "Crypto Research Labs: open, pre-registered crypto trading research",
 "lead": "Every trading idea is written down, locked with a hash and only then tested on real market data, out of "
         "sample and against a statistical null. Scheduled agents refresh the data daily, watch market conditions "
         "and re-test old ideas as new data arrives. {verdict}",
 "verdict_none": "None of the {n} hypotheses tested so far has passed its pre-registered test.",
 "verdict_some": "{p} of {n} hypotheses pass their pre-registered test.",
 "how_title": "New here? How to read this page",
 "how": [
  "<strong>The question.</strong> Can a simple, published rule beat just buying a coin and holding it, after "
  "trading fees? Most people who try find that it cannot. This project checks that honestly.",
  "<strong>Market regime</strong> shows what the crypto market looks like today: is Bitcoin trending, how nervous "
  "is it, is new money arriving. It describes the market; it is not a buy or sell signal.",
  "<strong>Hypotheses</strong> lists every idea tested so far. {pass} means it met the bar set in advance, {weak} "
  "means “a bit better, but could be luck”, {fail} means it did not beat holding.",
  "Open any hypothesis to see its numbers and a chart of how 1 dollar would have grown with the rule versus simply "
  "holding.",
  "Unfamiliar word? See the <a href=\"#glossary\">glossary</a> below.",
 ],
 "regime_title": "Market regime today",
 "regime_intro": "The conditions that decided past verdicts, recomputed every day. An alert is sent only when a "
                 "reading moves to a different band.",
 "source_down": "Source unavailable",
 "btc_title": "Bitcoin vs its 200-day average",
 "btc_text": "BTC closed at <strong>{price}</strong> on {date}, {diff} against its 200-day moving average ({sma}). "
             "Log scale, daily closes since 2020.",
 "btc_close": "BTC/USDT close", "sma200": "200-day average",
 "hyp_title": "Hypotheses tested",
 "hyp_intro": "{pass} = the pre-registered criterion is met. {weak} = beats buy-and-hold more often than not, but "
              "not significantly. {fail} = neither. Open a hypothesis for its full results and equity curves.",
 "th_id": "ID", "th_hyp": "Hypothesis", "th_family": "Family", "th_verdict": "Verdict", "th_tested": "Tested",
 "th_plain": "What it means",
 "glossary_title": "Glossary for beginners",
 "method_title": "Methodology",
 "method": [
  "<strong>Pre-registration.</strong> A study's specification is hashed (SHA-256) before it is run. Any later change "
  "breaks the check, so parameters cannot be tuned after seeing results.",
  "<strong>No look-ahead.</strong> All times are UTC; a decision at the daily close is applied to the next day; "
  "external data is lagged by its publication delay.",
  "<strong>Out of sample.</strong> Rules are chosen on 2018–2021 and judged on 2022 onwards, with trading fees.",
  "<strong>Against a null.</strong> Bootstrap and circular-shift tests with Bonferroni correction, then "
  "confirmation on eight coins that were not used to design the rule.",
 ],
 "method_more": "Full write-up (English)",
 "data_title": "Data freshness", "th_series": "Series", "th_from": "From", "th_last": "Last day",
 "th_behind": "Days behind",
 "footer_disclaimer": "<strong>Not financial advice.</strong> Crypto Research Labs is an open research project. It "
                      "does not trade, does not manage money and does not sell signals. A “pass” means a result is "
                      "worth a closer look, not that it will make money.",
 "footer_source": "Source code, data pipeline and every hypothesis", "footer_data": "machine-readable data",
 "Pass": "Pass", "Weak": "Weak", "Fail": "Fail",
 "plain_PASS": "This idea met the bar that was set before testing. It deserves a closer, independent look. It is "
               "not a promise of profit.",
 "plain_WEAK": "The idea did a bit better than simply buying and holding, but not by enough to rule out luck. Treat "
               "it as unproven.",
 "plain_FAIL": "The idea did not beat simply buying the coin and holding it. It is rejected.",
 "plain_none": "Not tested yet.",
 "in_plain": "In plain words",
 "back": "← All hypotheses", "family": "Family", "status": "Status",
 "result_h": "Result", "en_note": "Technical details are generated by the engine and shown in English.",
 "metrics_note": "Sharpe: return per unit of risk (higher is better). CAGR: average yearly growth. Max drawdown: "
                 "worst fall from a peak. p-value: chance the result is luck (lower is better). “Hold” columns are "
                 "buy-and-hold for the same asset and days.",
 "no_results": "No engine results yet: this study is kept for the record and is not re-run.",
 "c_asset": "Asset", "c_period": "Period", "c_rule": "Rule (chosen in-sample)", "c_sharpe": "Sharpe",
 "c_hsharpe": "Hold Sharpe", "c_cagr": "CAGR", "c_hcagr": "Hold CAGR", "c_dd": "Max drawdown",
 "c_hdd": "Hold drawdown", "c_exp": "In market", "c_p": "p-value", "c_beats": "Beats hold", "c_win": "Counts as win",
 "yes": "yes", "no": "no",
 "equity_h": "Equity curves",
 "equity_note": "Growth of 1 unit, log scale, fees included. Only days on which the rule is fully defined are "
                "counted.",
 "select_label": "Asset and period", "strategy": "Strategy (after fees)", "hold": "Buy and hold",
 "why_h": "Why it might work", "history_h": "Verdict history", "engine_src": "this engine, data to {d}",
 "spec_h": "Pre-registered specification",
 "caution": "This hypothesis passed its pre-registered test. That is a reason for independent confirmation and "
            "paper trading, not for trading real money.",
 "families": {"trend": "trend", "flows": "flows", "sentiment": "sentiment", "carry": "carry",
              "intraday": "intraday", "other": "other", "risk": "risk", "calendar": "calendar"},
 "statuses": {"draft": "draft", "registered": "registered", "passed": "passed", "weak": "weak",
              "rejected": "rejected", "archived": "archived"},
 "glossary": [
  ("What is buy-and-hold?", "Buying a coin once and keeping it. Every strategy here is compared with this, because a "
   "strategy that cannot beat doing nothing is not worth the effort or the fees."),
  ("What is a hypothesis?", "A trading idea written as a precise rule, for example “hold Bitcoin only while its "
   "price is above the 50-day average”. It is written down and locked before it is tested."),
  ("What is the Sharpe ratio?", "Return divided by how bumpy the ride was, per year. Higher is better. Around 0.5 "
   "is typical for holding Bitcoin; 1.0 or more over many years is rare."),
  ("What are CAGR and max drawdown?", "CAGR is the average yearly growth. Max drawdown is the worst fall from a "
   "peak, e.g. −50% means the account was at one point half of its best value."),
  ("What is a p-value?", "The chance of seeing a result this good if the idea had no real edge. Small is better. "
   "Because many ideas are tested, the bar is set lower than the usual 0.05 (Bonferroni correction)."),
  ("What does out of sample mean?", "Rules are chosen using one period of history (2018–2021) and judged on a later "
   "period they have never seen (2022 onwards). Doing well only on the data used to choose a rule proves nothing."),
  ("What is pre-registration?", "Writing the rule, the data and the pass criterion down before testing, and storing "
   "a SHA-256 fingerprint of it. Nobody can quietly adjust the test after seeing the result."),
  ("What is a moving average (SMA)?", "The average closing price over the last N days. “SMA200” is the 200-day "
   "average; price above it usually means a long-term uptrend."),
  ("What is the funding rate?", "A fee that futures traders pay each other every eight hours to keep futures "
   "prices close to the real price. When most traders bet on a rise, they pay the ones betting on a fall."),
  ("Can I trade with this?", "No. This is research, not advice and not a signal service. Nothing here has passed so "
   "far, and even a pass would need independent confirmation and paper trading first."),
 ],
 "monitors": {
  "h020_rule": ('H-020 rule today: BTC in or out of the market', 'The only rule that has passed its test. It stays out of Bitcoin while net deposits to exchanges are in their top 20% of the past year. Not a trading signal: it is still being verified (H-022).'),
  "btc_exchange_flow": ('BTC net flow to exchanges (7 days)', 'Bitcoin moved onto exchanges minus bitcoin moved off them over the last 7 days. Plus means net deposits (often read as coming sales), minus means net withdrawals to private wallets.'),
  "breadth": ('Market breadth: coins above their 200-day average', 'Share of the 13 coins whose price is above their own 200-day average. High means most of the market is in an uptrend; low means most coins are falling.'),
  "ever_trend": ('Everscale (EVER) vs its 50-day average', 'How far EVER trades above (+) or below (−) its 50-day average on Gate.io. This is the H-018 rule: above = in the market, below = out.'),
  "funding_carry": ("BTC funding carry: yearly yield after costs",
                    "What you would earn per year by holding BTC and shorting the same amount of BTC futures, so the "
                    "price itself does not matter. When most futures traders are long, shorts get paid."),
  "stablecoin_growth": ("Stablecoin supply growth (30 days)",
                        "How fast the supply of dollar-pegged coins (USDT, USDC) is growing. New stablecoins are "
                        "often money waiting to buy crypto; shrinking supply means money is leaving."),
  "fear_greed": ("Crypto Fear & Greed index",
                 "A 0–100 mood score built from price moves, volatility and social media. Low = fear, high = greed."),
  "btc_trend": ("BTC vs its 200-day average",
                "How far the price is above (+) or below (−) its average over the last 200 days. Above usually "
                "means a long-term uptrend."),
  "btc_volatility": ("BTC volatility (30 days, yearly)",
                     "How much the price swings, scaled to a year. 40% means a typical yearly move of about 40% up "
                     "or down."),
 },
 "bands": {"rule_in": 'in the market', "rule_out": 'out of the market', "deposits": 'deposits', "withdrawals": 'withdrawals', "weak": 'weak', "mixed": 'mixed', "strong": 'strong', "negative": "negative", "low": "low", "moderate": "moderate", "attractive": "attractive",
           "contracting": "contracting", "flat": "flat", "expanding": "expanding", "extreme_fear": "extreme fear",
           "fear": "fear", "neutral": "neutral", "greed": "greed", "extreme_greed": "extreme greed",
           "below": "below", "above": "above", "calm": "calm", "normal": "normal", "stressed": "stressed",
           "unavailable": "unavailable"},
 "notes": {
  ("h020_rule", "rule_out"): 'Heavy deposits to exchanges: the rule is out of the market.',
  ("btc_exchange_flow", "deposits"): 'Heavy deposits are tested in H-020 (BTC) and H-021 (ETH).',
  ("ever_trend", "above"): 'H-018 rule is in the market. Better than holding so far, but not significant; very thin liquidity.',
  ("ever_trend", "below"): 'H-018 rule is out of the market.',
  ("funding_carry", "attractive"): "Rejected in H-011 at ~1.5% a year. Carry this high is worth re-checking.",
  ("funding_carry", "negative"): "Shorts pay longs: crowded bearish positioning.",
  ("stablecoin_growth", "expanding"): "Money is entering crypto. H-006/H-010 found no reliable timing edge in this.",
  ("fear_greed", "extreme_greed"): "Exiting at ≥ 75 (H-008) did not beat holding.",
 },
 "titles": {},
},
# ---------------------------------------------------------------- Russian
"ru": {
 'nav_coins': 'Монеты',
 'coins_title': 'Монеты',
 'coins_intro': 'Все монеты из исследований: цена, тренд и волатильность на сегодня. Откройте монету, чтобы увидеть график и что каждое проверенное правило говорит о ней сегодня.',
 'th_coin': 'Монета',
 'th_price': 'Цена',
 'th_7d': '7 дней',
 'th_30d': '30 дней',
 'th_vs200': 'к 200-дневной средней',
 'th_vol': 'Волатильность (30 д)',
 'coin_title': '{name} ({ticker}): цена, тренд, волатильность и проверенные правила',
 'coin_desc': '{name} ({ticker}) сегодня: {price}, {ch30} за 30 дней, {vs200} к 200-дневной средней. Тренд, волатильность и состояние каждого проверенного торгового правила, обновляется ежедневно.',
 'coin_lead': 'Дневные закрытия с {exchange} (UTC). Последний день: {date}.',
 'back_coins': '← Все монеты',
 'chart12_h': 'Последние 12 месяцев',
 'close_label': 'Закрытие {ticker}',
 'sma50': 'Средняя за 50 дней',
 'stats_h': 'Цифры',
 'st_price': 'Цена',
 'st_7d': 'Изменение за 7 дней',
 'st_30d': 'Изменение за 30 дней',
 'st_1y': 'Изменение за год',
 'st_sma50': 'К 50-дневной средней',
 'st_sma200': 'К 200-дневной средней',
 'st_vol': 'Волатильность (30 дней, годовая)',
 'signals_h': 'Что сегодня говорят проверенные правила',
 'signals_warn': 'Это сегодняшнее состояние правил из гипотез. Ни одно из них не прошло проверку, поэтому это не сигналы купить или продать. Они показывают, что сделало бы каждое правило, — чтобы можно было наблюдать за его поведением.',
 'sig_sma50': 'Тренд: цена выше 50-дневной средней',
 'sig_mom7': 'Недельный моментум: цена выше, чем 7 дней назад',
 'sig_vol': 'Контроль волатильности (30% в год): доля от полной позиции',
 'sig_btc': 'Режим рынка: биткоин выше 200-дневной средней',
 'state_in': 'в рынке',
 'state_out': 'вне рынка',
 'th_rule': 'Правило',
 'th_state': 'Сегодня',
 'th_tested_in': 'Проверено в',
 'coin_studies_h': 'Исследования с этой монетой',
 'no_studies': 'Эта монета используется только как фильтр рынка.',
 'thin_note': 'Эта монета торгуется на {exchange}, а не на Binance. Ликвидность низкая, поэтому цена может скакать даже от небольших сделок.',
 'th_peak': 'От пика',
 'th_100': '$100 год назад →',
 'st_peak': 'От максимума закрытия с {since} ({peak}, {date})',
 'st_100': '$100, вложенные год назад, сейчас',
 'st_corr': 'Связь с биткоином (корреляция, 90 дней)',
 'corr_note': 'Корреляция: 1 — движется точно как биткоин, 0 — связи нет, −1 — движется наоборот. У большинства монет выше 0,6, поэтому несколько монет в портфеле почти не надёжнее одной.',
 "plain_scheduled": 'Данные копятся. Заранее назначенная проверка пройдёт {date}, когда накопится год данных.',
 "sig_rule": 'Правило {id}',
 "site_title": "Crypto Research Labs: открытые исследования торговых стратегий для криптовалют",
 "site_desc": "Открытые исследования торговых идей для криптовалют с предварительной регистрацией: {verdict} "
              "Состояние рынка в реальном времени (доходность фандинга BTC, стейблкоины, индекс страха и жадности, "
              "тренд, волатильность) и автоматическая перепроверка каждой гипотезы.",
 "hyp_desc": "{id} ({verdict}): {title}. {plain}",
 "nav_dashboard": "Главная", "nav_new": "Новичкам", "nav_regime": "Рынок сейчас", "nav_hyp": "Гипотезы",
 "nav_glossary": "Словарь", "nav_method": "Методика", "lang_label": "Язык",
 "updated": "Обновлено {t} · данные Binance, OKX, DefiLlama, alternative.me, BGeometrics",
 "h1": "Crypto Research Labs: честная проверка торговых идей для криптовалют",
 "lead": "Каждая торговая идея сначала записывается и фиксируется хешем, и только потом проверяется на реальных "
         "данных: на периоде, который не использовался для её подбора, и против статистического «нуля». "
         "Автоматические агенты ежедневно обновляют данные, следят за рынком и перепроверяют старые идеи на новых "
         "данных. {verdict}",
 "verdict_none": "Ни одна из {n} гипотез пока не прошла заранее заданный тест.",
 "verdict_some": "Заранее заданный тест прошли {p} из {n} гипотез.",
 "how_title": "Впервые здесь? Как читать эту страницу",
 "how": [
  "<strong>Главный вопрос.</strong> Может ли простое публичное правило обыграть обычную покупку монеты «купил и "
  "держи» с учётом комиссий? Чаще всего — нет. Этот проект проверяет это честно.",
  "<strong>Рынок сейчас</strong> показывает состояние крипторынка сегодня: есть ли тренд у биткоина, насколько он "
  "нервный, приходят ли новые деньги. Это описание рынка, а не сигнал купить или продать.",
  "<strong>Гипотезы</strong> — все проверенные идеи. {pass} — идея прошла планку, заданную заранее; {weak} — "
  "«чуть лучше, но это может быть везением»; {fail} — не обыграла простое удержание.",
  "Откройте любую гипотезу: там цифры и график — как вырос бы 1 доллар по правилу и при простом удержании.",
  "Непонятное слово? Загляните в <a href=\"#glossary\">словарь</a> ниже.",
 ],
 "regime_title": "Рынок сейчас",
 "regime_intro": "Условия, от которых зависели прошлые вердикты, пересчитываются каждый день. Уведомление "
                 "отправляется, только когда показатель переходит в другую зону.",
 "source_down": "Источник недоступен",
 "btc_title": "Биткоин и его 200-дневная средняя",
 "btc_text": "BTC закрылся на <strong>{price}</strong> {date}: {diff} к 200-дневной скользящей средней ({sma}). "
             "Логарифмическая шкала, дневные закрытия с 2020 года.",
 "btc_close": "Закрытие BTC/USDT", "sma200": "Средняя за 200 дней",
 "hyp_title": "Проверенные гипотезы",
 "hyp_intro": "{pass} — заранее заданный критерий выполнен. {weak} — чаще обгоняет «купил и держи», но без "
              "статистической значимости. {fail} — ни то, ни другое. Откройте гипотезу, чтобы увидеть все цифры "
              "и графики.",
 "th_id": "ID", "th_hyp": "Гипотеза", "th_family": "Тип", "th_verdict": "Вердикт", "th_tested": "Проверено",
 "th_plain": "Что это значит",
 "glossary_title": "Словарь для новичков",
 "method_title": "Методика",
 "method": [
  "<strong>Предварительная регистрация.</strong> Перед запуском от описания теста считается хеш SHA-256. Любое "
  "изменение потом ломает проверку — подогнать параметры под результат нельзя.",
  "<strong>Без заглядывания в будущее.</strong> Всё время — UTC; решение на дневном закрытии исполняется на "
  "следующий день; внешние данные сдвигаются на задержку их публикации.",
  "<strong>Вне выборки.</strong> Правила выбираются на 2018–2021 годах, а оцениваются с 2022 года, с комиссиями.",
  "<strong>Против «нуля».</strong> Бутстрэп и тест циклического сдвига с поправкой Бонферрони, затем "
  "подтверждение на восьми монетах, которые не использовались при создании правила.",
 ],
 "method_more": "Подробное описание (на английском)",
 "data_title": "Свежесть данных", "th_series": "Ряд", "th_from": "С", "th_last": "Последний день",
 "th_behind": "Отставание, дней",
 "footer_disclaimer": "<strong>Не является финансовой рекомендацией.</strong> Crypto Research Labs — открытый "
                      "исследовательский проект. Он не торгует, не управляет деньгами и не продаёт сигналы. "
                      "«Прошла» означает, что результат стоит изучить внимательнее, а не что он принесёт прибыль.",
 "footer_source": "Исходный код, сбор данных и все гипотезы", "footer_data": "данные в машиночитаемом виде",
 "Pass": "Прошла", "Weak": "Слабо", "Fail": "Не прошла",
 "plain_PASS": "Идея прошла планку, заданную до проверки. Её стоит независимо перепроверить. Это не обещание "
               "прибыли.",
 "plain_WEAK": "Идея сработала немного лучше, чем просто купить и держать, но недостаточно, чтобы исключить "
               "везение. Считайте её недоказанной.",
 "plain_FAIL": "Идея не обыграла простую покупку монеты с удержанием. Она отклонена.",
 "plain_none": "Ещё не проверялась.",
 "in_plain": "Простыми словами",
 "back": "← Все гипотезы", "family": "Тип", "status": "Статус",
 "result_h": "Результат", "en_note": "Технические подробности формирует движок, они показаны на английском.",
 "metrics_note": "Sharpe — доходность на единицу риска (больше — лучше). CAGR — средний годовой рост. Макс. "
                 "просадка — худшее падение от пика. p-value — вероятность, что результат случаен (меньше — "
                 "лучше). Столбцы «Удержание» — «купил и держи» для той же монеты и тех же дней.",
 "no_results": "Результатов движка пока нет: исследование сохранено для истории и не перезапускается.",
 "c_asset": "Монета", "c_period": "Период", "c_rule": "Правило (выбрано в выборке)", "c_sharpe": "Sharpe",
 "c_hsharpe": "Sharpe удержания", "c_cagr": "CAGR", "c_hcagr": "CAGR удержания", "c_dd": "Макс. просадка",
 "c_hdd": "Просадка удержания", "c_exp": "В рынке", "c_p": "p-value", "c_beats": "Лучше удержания",
 "c_win": "Засчитано", "yes": "да", "no": "нет",
 "equity_h": "Кривые капитала",
 "equity_note": "Рост 1 единицы, логарифмическая шкала, с комиссиями. Учитываются только дни, когда правило "
                "полностью определено.",
 "select_label": "Монета и период", "strategy": "Стратегия (после комиссий)", "hold": "Купил и держи",
 "why_h": "Почему это могло бы работать", "history_h": "История вердиктов", "engine_src": "этот движок, данные по {d}",
 "spec_h": "Зарегистрированная спецификация",
 "caution": "Гипотеза прошла заранее заданный тест. Это повод для независимой проверки и торговли на бумаге, а не "
            "для торговли реальными деньгами.",
 "families": {"trend": "тренд", "flows": "потоки", "sentiment": "настроение", "carry": "керри",
              "intraday": "внутри дня", "other": "другое", "risk": "риск", "calendar": "календарь"},
 "statuses": {"draft": "черновик", "registered": "зарегистрирована", "passed": "прошла", "weak": "слабо",
              "rejected": "отклонена", "archived": "в архиве"},
 "glossary": [
  ("Что такое «купил и держи»?", "Купить монету один раз и просто держать. Каждая стратегия сравнивается с этим: "
   "если она не обыгрывает бездействие, она не стоит усилий и комиссий."),
  ("Что такое гипотеза?", "Торговая идея, записанная как точное правило, например «держать биткоин, только пока цена "
   "выше 50-дневной средней». Её записывают и фиксируют до проверки."),
  ("Что такое коэффициент Шарпа?", "Доходность, делённая на то, насколько «трясло» по пути, в пересчёте на год. "
   "Больше — лучше. Около 0,5 — обычное значение для удержания биткоина; 1,0 и выше на многих годах — редкость."),
  ("Что такое CAGR и максимальная просадка?", "CAGR — средний годовой рост. Максимальная просадка — худшее падение "
   "от пика: −50% значит, что в какой-то момент счёт стоил половину своего максимума."),
  ("Что такое p-value?", "Вероятность увидеть такой хороший результат, если у идеи нет настоящего преимущества. "
   "Меньше — лучше. Так как проверяется много идей, планка ниже обычных 0,05 (поправка Бонферрони)."),
  ("Что значит «вне выборки»?", "Правило выбирают на одном отрезке истории (2018–2021), а оценивают на более "
   "позднем, которого оно не видело (с 2022). Успех только на данных, по которым правило подбирали, ничего не "
   "доказывает."),
  ("Что такое предварительная регистрация?", "Правило, данные и критерий успеха записываются до проверки, и от "
   "записи сохраняется отпечаток SHA-256. Никто не может тихо подправить тест после того, как увидел результат."),
  ("Что такое скользящая средняя (SMA)?", "Средняя цена закрытия за последние N дней. SMA200 — средняя за 200 дней; "
   "цена выше неё обычно означает долгосрочный рост."),
  ("Что такое ставка фандинга?", "Плата, которую трейдеры фьючерсов платят друг другу каждые восемь часов, чтобы "
   "цена фьючерса держалась рядом с реальной. Когда большинство ставит на рост, они платят тем, кто ставит на "
   "падение."),
  ("Можно ли по этому торговать?", "Нет. Это исследование, а не совет и не сигналы. Пока ничего не прошло, и даже "
   "прошедшей идее нужна независимая проверка и торговля на бумаге."),
 ],
 "monitors": {
  "h020_rule": ('Правило H-020 сегодня: BTC в рынке или вне', 'Единственное правило, прошедшее проверку. Оно не держит биткоин, пока чистый завод на биржи в верхних 20% за год. Это не торговый сигнал: правило ещё перепроверяется (H-022).'),
  "btc_exchange_flow": ('Чистый приток BTC на биржи (7 дней)', 'Сколько биткоинов завели на биржи минус сколько вывели за 7 дней. Плюс — чистый завод (часто читают как будущие продажи), минус — вывод в личные кошельки.'),
  "breadth": ('Ширина рынка: монеты выше 200-дневной средней', 'Доля из 13 монет, у которых цена выше собственной 200-дневной средней. Много — большая часть рынка в росте; мало — большинство монет падает.'),
  "ever_trend": ('Everscale (EVER) относительно 50-дневной средней', 'Насколько EVER на Gate.io выше (+) или ниже (−) своей средней за 50 дней. Это правило H-018: выше — в рынке, ниже — вне рынка.'),
  "funding_carry": ("Керри на фандинге BTC: годовая доходность после издержек",
                    "Сколько можно заработать за год, держа BTC и одновременно продав столько же фьючерсов BTC, — "
                    "цена при этом не важна. Когда большинство на фьючерсах в лонге, шортам платят."),
  "stablecoin_growth": ("Рост стейблкоинов (30 дней)",
                        "Как быстро растёт выпуск монет, привязанных к доллару (USDT, USDC). Новые стейблкоины — "
                        "часто деньги, готовые к покупке крипты; сокращение — деньги уходят."),
  "fear_greed": ("Индекс страха и жадности",
                 "Оценка настроения рынка от 0 до 100 по движению цены, волатильности и соцсетям. Мало — страх, "
                 "много — жадность."),
  "btc_trend": ("BTC относительно 200-дневной средней",
                "Насколько цена выше (+) или ниже (−) средней за последние 200 дней. Выше обычно означает "
                "долгосрочный рост."),
  "btc_volatility": ("Волатильность BTC (30 дней, годовая)",
                     "Насколько сильно скачет цена в пересчёте на год. 40% — типичное годовое движение примерно на "
                     "40% вверх или вниз."),
 },
 "bands": {"rule_in": 'в рынке', "rule_out": 'вне рынка', "deposits": 'завод на биржи', "withdrawals": 'вывод с бирж', "weak": 'слабая', "mixed": 'смешанная', "strong": 'сильная', "negative": "отрицательная", "low": "низкая", "moderate": "умеренная", "attractive": "привлекательная",
           "contracting": "сокращение", "flat": "без изменений", "expanding": "рост",
           "extreme_fear": "крайний страх", "fear": "страх", "neutral": "нейтрально", "greed": "жадность",
           "extreme_greed": "крайняя жадность", "below": "ниже", "above": "выше", "calm": "спокойно",
           "normal": "обычно", "stressed": "напряжённо", "unavailable": "нет данных"},
 "notes": {
  ("h020_rule", "rule_out"): 'Сильный завод на биржи: правило вне рынка.',
  ("btc_exchange_flow", "deposits"): 'Сильный завод на биржи проверяется в H-020 (BTC) и H-021 (ETH).',
  ("ever_trend", "above"): 'Правило H-018 в рынке. Пока лучше удержания, но не значимо; ликвидность очень низкая.',
  ("ever_trend", "below"): 'Правило H-018 вне рынка.',
  ("funding_carry", "attractive"): "В H-011 отклонено при ~1,5% в год. Такую доходность стоит перепроверить.",
  ("funding_carry", "negative"): "Шорты платят лонгам: рынок перегружен медвежьими позициями.",
  ("stablecoin_growth", "expanding"): "Деньги заходят в крипту. H-006/H-010 не нашли в этом надёжного сигнала.",
  ("fear_greed", "extreme_greed"): "Выход при ≥ 75 (H-008) не обыграл удержание.",
 },
 "titles": {
  "H-022": 'Повторная проверка H-020 на данных, собранных после 15.10.2026',
  "H-023": 'Gram (GRAM, бывший Toncoin): правило SMA50 обыгрывает удержание с 2023 года',
  "H-024": 'Ротация по относительной силе: 3 самые сильные монеты (1 и 3 дня), без резких скачков, только пока BTC выше 200-дневной средней',
  "H-025": 'Простая ротация по импульсу: 3 самые сильные монеты за 1 и 3 дня',
  "H-026": 'Краткосрочный возврат: 3 монеты, сильнее всех упавшие вчера',
  "H-020": 'BTC вне рынка, когда 7-дневный чистый завод на биржи в верхних 20%',
  "H-021": 'ETH вне рынка, когда 7-дневный чистый завод на биржи в верхних 20%',
  "H-012": 'Контроль волатильности (30% в год) обыгрывает удержание на BTC, ETH, SOL',
  "H-013": 'Контроль волатильности (30% в год) обыгрывает удержание на 8 независимых монетах',
  "H-014": 'Недельный моментум: держать только после роста за 7 дней (BTC, ETH, SOL)',
  "H-015": 'Эффект понедельника: BTC только по понедельникам (UTC) обыгрывает удержание',
  "H-016": 'Эффект смены месяца: BTC только в последние 2 и первые 3 дня месяца',
  "H-017": 'Фильтр по биткоину: альткоины только пока BTC выше 200-дневной средней',
  "H-018": 'Everscale (EVER): правило SMA50 обыгрывает удержание с 2022 года',
  "H-019": 'Everscale (EVER): держать только пока BTC выше 200-дневной средней',
  "H-001": "Ансамбль минутных индикаторов (RSI, MACD, EMA, моментум) предсказывает направление на 1–4 часа",
  "H-002": "Перевёрнутые минутные сигналы прибыльны после комиссий",
  "H-003": "Лучшее дневное трендовое правило (выбрано на 2018–2021) обыгрывает удержание вне выборки, спот",
  "H-004": "Лучшее дневное трендовое правило, лонг/шорт на фьючерсах, обыгрывает удержание",
  "H-005": "SMA50 (лонг или вне рынка, спот) обыгрывает удержание на 8 независимых монетах",
  "H-006": "Лонг BTC, когда 7-дневный рост USDT+USDC выше своей годовой медианы",
  "H-007": "BTC вне рынка, когда 7-дневный фандинг выше 80-го перцентиля за год",
  "H-008": "BTC вне рынка, когда индекс страха и жадности ≥ 75",
  "H-009": "Лонг BTC, только когда 5-дневный чистый приток в спотовые ETF положительный",
  "H-010": "Тайминг по росту стейблкоинов (H-006) обыгрывает удержание на 8 независимых монетах",
  "H-011": "Керри на фандинге BTC (спот в лонг + бессрочный фьючерс в шорт) окупает риск",
 },
},
# ---------------------------------------------------------------- Spanish
"es": {
 'nav_coins': 'Monedas',
 'coins_title': 'Monedas',
 'coins_intro': 'Todas las monedas de los estudios: precio, tendencia y volatilidad de hoy. Abre una moneda para ver su gráfico y qué dice hoy cada regla probada.',
 'th_coin': 'Moneda',
 'th_price': 'Precio',
 'th_7d': '7 días',
 'th_30d': '30 días',
 'th_vs200': 'vs media de 200 días',
 'th_vol': 'Volatilidad (30 d)',
 'coin_title': '{name} ({ticker}): precio, tendencia, volatilidad y reglas probadas',
 'coin_desc': '{name} ({ticker}) hoy: {price}, {ch30} en 30 días, {vs200} frente a su media de 200 días. Tendencia, volatilidad y estado de cada regla de trading probada, actualizado a diario.',
 'coin_lead': 'Cierres diarios de {exchange} (UTC). Último día: {date}.',
 'back_coins': '← Todas las monedas',
 'chart12_h': 'Últimos 12 meses',
 'close_label': 'Cierre {ticker}',
 'sma50': 'Media de 50 días',
 'stats_h': 'Cifras',
 'st_price': 'Precio',
 'st_7d': 'Cambio, 7 días',
 'st_30d': 'Cambio, 30 días',
 'st_1y': 'Cambio, 1 año',
 'st_sma50': 'vs media de 50 días',
 'st_sma200': 'vs media de 200 días',
 'st_vol': 'Volatilidad (30 días, anual)',
 'signals_h': 'Qué dicen hoy las reglas probadas',
 'signals_warn': 'Estos son los estados de hoy de las reglas de las hipótesis. Ninguna ha superado su prueba, así que no son señales de compra o venta. Muestran qué haría cada regla, para que puedas observar su comportamiento.',
 'sig_sma50': 'Tendencia: precio por encima de su media de 50 días',
 'sig_mom7': 'Momentum semanal: precio mayor que hace 7 días',
 'sig_vol': 'Objetivo de volatilidad (30%/año): parte de una posición completa',
 'sig_btc': 'Régimen de mercado: Bitcoin por encima de su media de 200 días',
 'state_in': 'dentro del mercado',
 'state_out': 'fuera del mercado',
 'th_rule': 'Regla',
 'th_state': 'Hoy',
 'th_tested_in': 'Probada en',
 'coin_studies_h': 'Estudios que incluyen esta moneda',
 'no_studies': 'Esta moneda solo se usa como filtro de mercado.',
 'thin_note': 'Esta moneda cotiza en {exchange}, no en Binance. La liquidez es baja y el precio puede saltar con operaciones pequeñas.',
 'th_peak': 'Desde el máximo',
 'th_100': '$100 hace un año →',
 'st_peak': 'Desde el cierre más alto desde {since} ({peak} el {date})',
 'st_100': '$100 invertidos hace un año valen hoy',
 'st_corr': 'Correlación con Bitcoin (90 días)',
 'corr_note': 'Correlación: 1 = se mueve igual que Bitcoin, 0 = sin relación, −1 = se mueve al revés. La mayoría de las monedas están por encima de 0,6, así que tener varias no es mucho más seguro que tener una.',
 "plain_scheduled": 'Se están recogiendo datos. La prueba prerregistrada se hará el {date}, cuando haya un año de datos.',
 "sig_rule": 'Regla {id}',
 "site_title": "Crypto Research Labs: investigación abierta y prerregistrada de trading de criptomonedas",
 "site_desc": "Investigación abierta y prerregistrada de estrategias de trading cripto: {verdict} Régimen de mercado "
              "en vivo (carry de funding de BTC, stablecoins, Fear & Greed, tendencia, volatilidad) y cada hipótesis "
              "se vuelve a probar automáticamente.",
 "hyp_desc": "{id} ({verdict}): {title}. {plain}",
 "nav_dashboard": "Panel", "nav_new": "¿Eres nuevo?", "nav_regime": "Mercado hoy", "nav_hyp": "Hipótesis",
 "nav_glossary": "Glosario", "nav_method": "Metodología", "lang_label": "Idioma",
 "updated": "Actualizado {t} · datos de Binance, OKX, DefiLlama, alternative.me, BGeometrics",
 "h1": "Crypto Research Labs: investigación abierta y prerregistrada de trading cripto",
 "lead": "Cada idea de trading se escribe, se bloquea con un hash y solo después se prueba con datos reales del "
         "mercado, fuera de muestra y frente a una hipótesis nula estadística. Agentes programados actualizan los "
         "datos cada día, vigilan el mercado y vuelven a probar ideas antiguas con datos nuevos. {verdict}",
 "verdict_none": "Ninguna de las {n} hipótesis probadas hasta ahora ha superado su prueba prerregistrada.",
 "verdict_some": "{p} de {n} hipótesis superan su prueba prerregistrada.",
 "how_title": "¿Eres nuevo? Cómo leer esta página",
 "how": [
  "<strong>La pregunta.</strong> ¿Puede una regla sencilla y pública ganar a simplemente comprar una moneda y "
  "mantenerla, después de comisiones? La mayoría descubre que no. Este proyecto lo comprueba con honestidad.",
  "<strong>Mercado hoy</strong> muestra cómo está el mercado cripto: si Bitcoin tiene tendencia, cuán nervioso está, "
  "si entra dinero nuevo. Describe el mercado; no es una señal de compra o venta.",
  "<strong>Hipótesis</strong> enumera todas las ideas probadas. {pass} significa que cumplió el listón fijado de "
  "antemano, {weak} significa “algo mejor, pero puede ser suerte”, {fail} significa que no ganó a mantener.",
  "Abre cualquier hipótesis para ver sus cifras y un gráfico de cómo habría crecido 1 dólar con la regla frente a "
  "simplemente mantener.",
  "¿Una palabra desconocida? Consulta el <a href=\"#glossary\">glosario</a> más abajo.",
 ],
 "regime_title": "El mercado hoy",
 "regime_intro": "Las condiciones que decidieron veredictos anteriores, recalculadas cada día. Solo se envía una "
                 "alerta cuando un indicador cambia de zona.",
 "source_down": "Fuente no disponible",
 "btc_title": "Bitcoin frente a su media de 200 días",
 "btc_text": "BTC cerró en <strong>{price}</strong> el {date}, {diff} respecto a su media móvil de 200 días ({sma}). "
             "Escala logarítmica, cierres diarios desde 2020.",
 "btc_close": "Cierre BTC/USDT", "sma200": "Media de 200 días",
 "hyp_title": "Hipótesis probadas",
 "hyp_intro": "{pass} = se cumple el criterio prerregistrado. {weak} = gana a comprar y mantener más veces que no, "
              "pero sin significación. {fail} = ninguna de las dos. Abre una hipótesis para ver todos sus resultados.",
 "th_id": "ID", "th_hyp": "Hipótesis", "th_family": "Tipo", "th_verdict": "Veredicto", "th_tested": "Probada",
 "th_plain": "Qué significa",
 "glossary_title": "Glosario para principiantes",
 "method_title": "Metodología",
 "method": [
  "<strong>Prerregistro.</strong> La especificación del estudio se convierte en un hash (SHA-256) antes de "
  "ejecutarlo. Cualquier cambio posterior rompe la verificación, así que no se pueden ajustar parámetros tras ver "
  "los resultados.",
  "<strong>Sin mirar al futuro.</strong> Todas las horas en UTC; una decisión al cierre diario se aplica al día "
  "siguiente; los datos externos se retrasan según su publicación.",
  "<strong>Fuera de muestra.</strong> Las reglas se eligen con 2018–2021 y se juzgan desde 2022, con comisiones.",
  "<strong>Frente a una nula.</strong> Pruebas bootstrap y de desplazamiento circular con corrección de Bonferroni, "
  "y luego confirmación en ocho monedas que no se usaron para diseñar la regla.",
 ],
 "method_more": "Descripción completa (en inglés)",
 "data_title": "Actualidad de los datos", "th_series": "Serie", "th_from": "Desde", "th_last": "Último día",
 "th_behind": "Días de retraso",
 "footer_disclaimer": "<strong>No es asesoramiento financiero.</strong> Crypto Research Labs es un proyecto de "
                      "investigación abierto. No opera, no gestiona dinero y no vende señales. “Supera” significa que "
                      "un resultado merece un análisis más detallado, no que vaya a ganar dinero.",
 "footer_source": "Código fuente, recogida de datos y todas las hipótesis", "footer_data": "datos legibles por máquina",
 "Pass": "Supera", "Weak": "Débil", "Fail": "No supera",
 "plain_PASS": "La idea alcanzó el listón fijado antes de la prueba. Merece una revisión independiente. No es una "
               "promesa de beneficio.",
 "plain_WEAK": "La idea funcionó algo mejor que comprar y mantener, pero no lo bastante para descartar la suerte. "
               "Considérala no demostrada.",
 "plain_FAIL": "La idea no superó a simplemente comprar la moneda y mantenerla. Queda rechazada.",
 "plain_none": "Aún no se ha probado.",
 "in_plain": "En pocas palabras",
 "back": "← Todas las hipótesis", "family": "Tipo", "status": "Estado",
 "result_h": "Resultado", "en_note": "Los detalles técnicos los genera el motor y se muestran en inglés.",
 "metrics_note": "Sharpe: rentabilidad por unidad de riesgo (más es mejor). CAGR: crecimiento anual medio. Caída "
                 "máxima: la peor caída desde un pico. p-valor: probabilidad de que el resultado sea suerte (menos "
                 "es mejor). Las columnas “Mantener” son comprar y mantener el mismo activo en los mismos días.",
 "no_results": "Aún no hay resultados del motor: este estudio se conserva como registro y no se vuelve a ejecutar.",
 "c_asset": "Activo", "c_period": "Periodo", "c_rule": "Regla (elegida en muestra)", "c_sharpe": "Sharpe",
 "c_hsharpe": "Sharpe mantener", "c_cagr": "CAGR", "c_hcagr": "CAGR mantener", "c_dd": "Caída máxima",
 "c_hdd": "Caída mantener", "c_exp": "En mercado", "c_p": "p-valor", "c_beats": "Gana a mantener",
 "c_win": "Cuenta como acierto", "yes": "sí", "no": "no",
 "equity_h": "Curvas de capital",
 "equity_note": "Crecimiento de 1 unidad, escala logarítmica, con comisiones. Solo cuentan los días en que la regla "
                "está plenamente definida.",
 "select_label": "Activo y periodo", "strategy": "Estrategia (tras comisiones)", "hold": "Comprar y mantener",
 "why_h": "Por qué podría funcionar", "history_h": "Historial de veredictos", "engine_src": "este motor, datos hasta {d}",
 "spec_h": "Especificación prerregistrada",
 "caution": "Esta hipótesis superó su prueba prerregistrada. Es motivo para una confirmación independiente y "
            "trading simulado, no para operar con dinero real.",
 "families": {"trend": "tendencia", "flows": "flujos", "sentiment": "sentimiento", "carry": "carry",
              "intraday": "intradía", "other": "otro", "risk": "riesgo", "calendar": "calendario"},
 "statuses": {"draft": "borrador", "registered": "registrada", "passed": "superada", "weak": "débil",
              "rejected": "rechazada", "archived": "archivada"},
 "glossary": [
  ("¿Qué es comprar y mantener?", "Comprar una moneda una vez y conservarla. Cada estrategia se compara con esto: si "
   "no gana a no hacer nada, no vale el esfuerzo ni las comisiones."),
  ("¿Qué es una hipótesis?", "Una idea de trading escrita como regla precisa, por ejemplo “mantener Bitcoin solo "
   "mientras su precio esté por encima de la media de 50 días”. Se escribe y se bloquea antes de probarla."),
  ("¿Qué es el ratio de Sharpe?", "La rentabilidad dividida por lo accidentado del camino, por año. Más es mejor. "
   "Alrededor de 0,5 es típico al mantener Bitcoin; 1,0 o más durante muchos años es raro."),
  ("¿Qué son el CAGR y la caída máxima?", "El CAGR es el crecimiento anual medio. La caída máxima es la peor caída "
   "desde un pico: −50% significa que la cuenta llegó a valer la mitad de su máximo."),
  ("¿Qué es un p-valor?", "La probabilidad de ver un resultado tan bueno si la idea no tuviera ventaja real. Menos "
   "es mejor. Como se prueban muchas ideas, el listón es más bajo que el 0,05 habitual (corrección de Bonferroni)."),
  ("¿Qué significa fuera de muestra?", "Las reglas se eligen con un periodo de la historia (2018–2021) y se juzgan en "
   "uno posterior que nunca han visto (desde 2022). Acertar solo con los datos usados para elegir no demuestra nada."),
  ("¿Qué es el prerregistro?", "Escribir la regla, los datos y el criterio de éxito antes de probar, y guardar su "
   "huella SHA-256. Nadie puede ajustar la prueba en silencio después de ver el resultado."),
  ("¿Qué es una media móvil (SMA)?", "El precio de cierre medio de los últimos N días. “SMA200” es la media de 200 "
   "días; un precio por encima suele indicar una tendencia alcista de largo plazo."),
  ("¿Qué es la tasa de funding?", "Una comisión que los traders de futuros se pagan cada ocho horas para mantener el "
   "precio del futuro cerca del real. Cuando la mayoría apuesta al alza, paga a quienes apuestan a la baja."),
  ("¿Puedo operar con esto?", "No. Es investigación, no asesoramiento ni un servicio de señales. Nada ha superado "
   "la prueba hasta ahora, e incluso un aprobado necesitaría confirmación independiente y trading simulado."),
 ],
 "monitors": {
  "h020_rule": ('Regla H-020 hoy: BTC dentro o fuera del mercado', 'La única regla que ha superado su prueba. No mantiene Bitcoin mientras los depósitos netos a exchanges estén en su 20% superior del último año. No es una señal: aún se está verificando (H-022).'),
  "btc_exchange_flow": ('Flujo neto de BTC a exchanges (7 días)', 'Bitcoin enviado a exchanges menos bitcoin retirado en los últimos 7 días. Positivo = depósitos netos (suele leerse como ventas próximas); negativo = retiros a carteras privadas.'),
  "breadth": ('Amplitud del mercado: monedas sobre su media de 200 días', 'Parte de las 13 monedas cuyo precio está por encima de su propia media de 200 días. Alto = la mayor parte del mercado sube; bajo = la mayoría cae.'),
  "ever_trend": ('Everscale (EVER) frente a su media de 50 días', 'Cuánto cotiza EVER en Gate.io por encima (+) o por debajo (−) de su media de 50 días. Es la regla H-018: encima = dentro, debajo = fuera.'),
  "funding_carry": ("Carry de funding de BTC: rendimiento anual tras costes",
                    "Lo que ganarías al año manteniendo BTC y vendiendo en corto la misma cantidad en futuros, de modo "
                    "que el precio no importa. Cuando la mayoría está en largo, a los cortos se les paga."),
  "stablecoin_growth": ("Crecimiento de stablecoins (30 días)",
                        "Lo rápido que crece la oferta de monedas ligadas al dólar (USDT, USDC). Las nuevas suelen ser "
                        "dinero esperando para comprar cripto; si se reducen, el dinero se va."),
  "fear_greed": ("Índice Fear & Greed cripto",
                 "Una puntuación de ánimo de 0 a 100 basada en precio, volatilidad y redes sociales. Bajo = miedo, "
                 "alto = codicia."),
  "btc_trend": ("BTC frente a su media de 200 días",
                "Cuánto está el precio por encima (+) o por debajo (−) de su media de los últimos 200 días. Encima "
                "suele indicar tendencia alcista de largo plazo."),
  "btc_volatility": ("Volatilidad de BTC (30 días, anualizada)",
                     "Cuánto oscila el precio, escalado a un año. 40% significa un movimiento anual típico de un 40% "
                     "arriba o abajo."),
 },
 "bands": {"rule_in": 'dentro del mercado', "rule_out": 'fuera del mercado', "deposits": 'depósitos', "withdrawals": 'retiros', "weak": 'débil', "mixed": 'mixta', "strong": 'fuerte', "negative": "negativo", "low": "bajo", "moderate": "moderado", "attractive": "atractivo",
           "contracting": "contracción", "flat": "estable", "expanding": "expansión", "extreme_fear": "miedo extremo",
           "fear": "miedo", "neutral": "neutral", "greed": "codicia", "extreme_greed": "codicia extrema",
           "below": "por debajo", "above": "por encima", "calm": "tranquilo", "normal": "normal",
           "stressed": "tenso", "unavailable": "sin datos"},
 "notes": {
  ("h020_rule", "rule_out"): 'Depósitos fuertes a exchanges: la regla está fuera del mercado.',
  ("btc_exchange_flow", "deposits"): 'Los depósitos fuertes se prueban en H-020 (BTC) y H-021 (ETH).',
  ("ever_trend", "above"): 'La regla H-018 está dentro. Mejor que mantener, pero no significativo; liquidez muy baja.',
  ("ever_trend", "below"): 'La regla H-018 está fuera del mercado.',
  ("funding_carry", "attractive"): "Rechazado en H-011 con ~1,5% anual. Un carry tan alto merece revisarse.",
  ("funding_carry", "negative"): "Los cortos pagan a los largos: posicionamiento bajista saturado.",
  ("stablecoin_growth", "expanding"): "Entra dinero en cripto. H-006/H-010 no hallaron una señal fiable en esto.",
  ("fear_greed", "extreme_greed"): "Salir en ≥ 75 (H-008) no superó a mantener.",
 },
 "titles": {
  "H-022": 'Réplica de H-020 con datos recogidos después del 15-10-2026',
  "H-023": 'Gram (GRAM, antes Toncoin): la regla SMA50 gana a mantener desde 2023',
  "H-024": 'Rotación por fuerza relativa: las 3 monedas más fuertes (1 y 3 días), sin subidas extremas, solo con BTC sobre su media de 200 días',
  "H-025": 'Rotación de momentum simple: las 3 monedas más fuertes en 1 y 3 días',
  "H-026": 'Reversión de corto plazo: las 3 monedas que más cayeron ayer',
  "H-020": 'BTC fuera del mercado cuando los depósitos netos de 7 días a exchanges están en su 20% superior',
  "H-021": 'ETH fuera del mercado cuando los depósitos netos de 7 días a exchanges están en su 20% superior',
  "H-012": 'Objetivo de volatilidad (30%/año) gana a mantener en BTC, ETH, SOL',
  "H-013": 'Objetivo de volatilidad (30%/año) gana a mantener en 8 monedas independientes',
  "H-014": 'Momentum semanal: mantener solo tras una subida de 7 días (BTC, ETH, SOL)',
  "H-015": 'Efecto lunes: BTC solo los lunes (UTC) gana a mantener',
  "H-016": 'Cambio de mes: BTC solo los últimos 2 y primeros 3 días del mes',
  "H-017": 'Filtro de Bitcoin: altcoins solo mientras BTC esté sobre su media de 200 días',
  "H-018": 'Everscale (EVER): la regla SMA50 gana a mantener desde 2022',
  "H-019": 'Everscale (EVER): mantener solo mientras BTC esté sobre su media de 200 días',
  "H-001": "Un conjunto de indicadores de minutos (RSI, MACD, EMA, momentum) predice la dirección a 1–4 h",
  "H-002": "Las señales de minutos invertidas son rentables tras comisiones",
  "H-003": "La mejor regla de tendencia diaria (elegida en 2018–2021) gana a mantener fuera de muestra, spot",
  "H-004": "La mejor regla de tendencia diaria, largo/corto en futuros, gana a mantener",
  "H-005": "SMA50 (largo o fuera, spot) gana a mantener en 8 monedas independientes",
  "H-006": "Largo en BTC cuando el crecimiento de 7 días de USDT+USDC supera su mediana anual",
  "H-007": "BTC fuera del mercado cuando el funding de 7 días supera su percentil 80 anual",
  "H-008": "BTC fuera del mercado cuando Fear & Greed ≥ 75",
  "H-009": "Largo en BTC solo cuando el flujo neto de 5 días a los ETF spot es positivo",
  "H-010": "El timing por stablecoins (H-006) gana a mantener en 8 monedas independientes",
  "H-011": "El carry de funding de BTC (spot largo + perpetuo corto) compensa el riesgo",
 },
},
# ---------------------------------------------------------------- Portuguese (Brazil)
"pt": {
 'nav_coins': 'Moedas',
 'coins_title': 'Moedas',
 'coins_intro': 'Todas as moedas dos estudos: preço, tendência e volatilidade de hoje. Abra uma moeda para ver o gráfico e o que cada regra testada diz hoje.',
 'th_coin': 'Moeda',
 'th_price': 'Preço',
 'th_7d': '7 dias',
 'th_30d': '30 dias',
 'th_vs200': 'vs média de 200 dias',
 'th_vol': 'Volatilidade (30 d)',
 'coin_title': '{name} ({ticker}): preço, tendência, volatilidade e regras testadas',
 'coin_desc': '{name} ({ticker}) hoje: {price}, {ch30} em 30 dias, {vs200} em relação à média de 200 dias. Tendência, volatilidade e estado de cada regra de trading testada, atualizado diariamente.',
 'coin_lead': 'Fechamentos diários da {exchange} (UTC). Último dia: {date}.',
 'back_coins': '← Todas as moedas',
 'chart12_h': 'Últimos 12 meses',
 'close_label': 'Fechamento {ticker}',
 'sma50': 'Média de 50 dias',
 'stats_h': 'Números',
 'st_price': 'Preço',
 'st_7d': 'Variação, 7 dias',
 'st_30d': 'Variação, 30 dias',
 'st_1y': 'Variação, 1 ano',
 'st_sma50': 'vs média de 50 dias',
 'st_sma200': 'vs média de 200 dias',
 'st_vol': 'Volatilidade (30 dias, anual)',
 'signals_h': 'O que as regras testadas dizem hoje',
 'signals_warn': 'Estes são os estados de hoje das regras das hipóteses. Nenhuma passou no teste, então não são sinais de compra ou venda. Mostram o que cada regra faria, para você acompanhar o comportamento dela.',
 'sig_sma50': 'Tendência: preço acima da média de 50 dias',
 'sig_mom7': 'Momentum semanal: preço maior que há 7 dias',
 'sig_vol': 'Meta de volatilidade (30%/ano): fração de uma posição cheia',
 'sig_btc': 'Regime de mercado: Bitcoin acima da média de 200 dias',
 'state_in': 'no mercado',
 'state_out': 'fora do mercado',
 'th_rule': 'Regra',
 'th_state': 'Hoje',
 'th_tested_in': 'Testada em',
 'coin_studies_h': 'Estudos com esta moeda',
 'no_studies': 'Esta moeda é usada apenas como filtro de mercado.',
 'thin_note': 'Esta moeda é negociada na {exchange}, não na Binance. A liquidez é baixa, então o preço pode saltar com negócios pequenos.',
 'th_peak': 'Desde o pico',
 'th_100': '$100 há um ano →',
 'st_peak': 'Desde o maior fechamento desde {since} ({peak} em {date})',
 'st_100': '$100 investidos há um ano valem hoje',
 'st_corr': 'Correlação com o Bitcoin (90 dias)',
 'corr_note': 'Correlação: 1 = se move igual ao Bitcoin, 0 = sem relação, −1 = se move ao contrário. A maioria das moedas fica acima de 0,6, então ter várias não é muito mais seguro do que ter uma.',
 "plain_scheduled": 'Os dados estão sendo coletados. O teste pré-registrado será feito em {date}, quando houver um ano de dados.',
 "sig_rule": 'Regra {id}',
 "site_title": "Crypto Research Labs: pesquisa aberta e pré-registrada de trading de criptomoedas",
 "site_desc": "Pesquisa aberta e pré-registrada de estratégias de trading cripto: {verdict} Regime de mercado ao vivo "
              "(carry de funding do BTC, stablecoins, Fear & Greed, tendência, volatilidade) e cada hipótese é "
              "retestada automaticamente.",
 "hyp_desc": "{id} ({verdict}): {title}. {plain}",
 "nav_dashboard": "Painel", "nav_new": "Novo aqui?", "nav_regime": "Mercado hoje", "nav_hyp": "Hipóteses",
 "nav_glossary": "Glossário", "nav_method": "Metodologia", "lang_label": "Idioma",
 "updated": "Atualizado {t} · dados de Binance, OKX, DefiLlama, alternative.me, BGeometrics",
 "h1": "Crypto Research Labs: pesquisa aberta e pré-registrada de trading cripto",
 "lead": "Cada ideia de trading é escrita, travada com um hash e só então testada com dados reais de mercado, fora da "
         "amostra e contra uma hipótese nula estatística. Agentes agendados atualizam os dados todos os dias, "
         "acompanham o mercado e retestam ideias antigas com dados novos. {verdict}",
 "verdict_none": "Nenhuma das {n} hipóteses testadas até agora passou no teste pré-registrado.",
 "verdict_some": "{p} de {n} hipóteses passam no teste pré-registrado.",
 "how_title": "Novo aqui? Como ler esta página",
 "how": [
  "<strong>A pergunta.</strong> Uma regra simples e pública consegue vencer simplesmente comprar uma moeda e segurar, "
  "depois das taxas? A maioria descobre que não. Este projeto verifica isso com honestidade.",
  "<strong>Mercado hoje</strong> mostra como está o mercado cripto: se o Bitcoin está em tendência, quão nervoso está, "
  "se há dinheiro novo entrando. Descreve o mercado; não é sinal de compra ou venda.",
  "<strong>Hipóteses</strong> lista todas as ideias testadas. {pass} significa que atingiu a meta definida antes, "
  "{weak} significa “um pouco melhor, mas pode ser sorte”, {fail} significa que não venceu segurar.",
  "Abra qualquer hipótese para ver os números e um gráfico de como 1 dólar teria crescido com a regra versus apenas "
  "segurar.",
  "Palavra desconhecida? Veja o <a href=\"#glossary\">glossário</a> abaixo.",
 ],
 "regime_title": "O mercado hoje",
 "regime_intro": "As condições que decidiram veredictos passados, recalculadas todo dia. Um alerta só é enviado quando "
                 "um indicador muda de faixa.",
 "source_down": "Fonte indisponível",
 "btc_title": "Bitcoin versus sua média de 200 dias",
 "btc_text": "O BTC fechou em <strong>{price}</strong> em {date}, {diff} em relação à média móvel de 200 dias ({sma}). "
             "Escala logarítmica, fechamentos diários desde 2020.",
 "btc_close": "Fechamento BTC/USDT", "sma200": "Média de 200 dias",
 "hyp_title": "Hipóteses testadas",
 "hyp_intro": "{pass} = o critério pré-registrado foi atendido. {weak} = vence comprar e segurar na maioria das vezes, "
              "mas sem significância. {fail} = nenhum dos dois. Abra uma hipótese para ver todos os resultados.",
 "th_id": "ID", "th_hyp": "Hipótese", "th_family": "Tipo", "th_verdict": "Veredicto", "th_tested": "Testada",
 "th_plain": "O que significa",
 "glossary_title": "Glossário para iniciantes",
 "method_title": "Metodologia",
 "method": [
  "<strong>Pré-registro.</strong> A especificação do estudo vira um hash (SHA-256) antes de rodar. Qualquer mudança "
  "posterior quebra a verificação, então não dá para ajustar parâmetros depois de ver os resultados.",
  "<strong>Sem olhar o futuro.</strong> Todos os horários em UTC; uma decisão no fechamento diário vale para o dia "
  "seguinte; dados externos são atrasados conforme sua publicação.",
  "<strong>Fora da amostra.</strong> As regras são escolhidas em 2018–2021 e avaliadas a partir de 2022, com taxas.",
  "<strong>Contra uma nula.</strong> Testes bootstrap e de deslocamento circular com correção de Bonferroni, depois "
  "confirmação em oito moedas que não foram usadas para criar a regra.",
 ],
 "method_more": "Descrição completa (em inglês)",
 "data_title": "Atualização dos dados", "th_series": "Série", "th_from": "Desde", "th_last": "Último dia",
 "th_behind": "Dias de atraso",
 "footer_disclaimer": "<strong>Não é recomendação financeira.</strong> O Crypto Research Labs é um projeto de "
                      "pesquisa aberto. Não opera, não administra dinheiro e não vende sinais. “Passou” significa que "
                      "um resultado merece uma análise mais detalhada, não que vá dar lucro.",
 "footer_source": "Código-fonte, coleta de dados e todas as hipóteses", "footer_data": "dados legíveis por máquina",
 "Pass": "Passou", "Weak": "Fraca", "Fail": "Reprovada",
 "plain_PASS": "A ideia atingiu a meta definida antes do teste. Merece uma verificação independente. Não é promessa "
               "de lucro.",
 "plain_WEAK": "A ideia foi um pouco melhor do que comprar e segurar, mas não o bastante para descartar a sorte. "
               "Considere-a não comprovada.",
 "plain_FAIL": "A ideia não venceu simplesmente comprar a moeda e segurar. Ela foi rejeitada.",
 "plain_none": "Ainda não testada.",
 "in_plain": "Em poucas palavras",
 "back": "← Todas as hipóteses", "family": "Tipo", "status": "Status",
 "result_h": "Resultado", "en_note": "Os detalhes técnicos são gerados pelo motor e mostrados em inglês.",
 "metrics_note": "Sharpe: retorno por unidade de risco (maior é melhor). CAGR: crescimento anual médio. Drawdown "
                 "máximo: pior queda a partir de um pico. p-valor: chance de o resultado ser sorte (menor é melhor). "
                 "As colunas “Segurar” são comprar e segurar o mesmo ativo nos mesmos dias.",
 "no_results": "Ainda sem resultados do motor: este estudo é mantido como registro e não é executado de novo.",
 "c_asset": "Ativo", "c_period": "Período", "c_rule": "Regra (escolhida na amostra)", "c_sharpe": "Sharpe",
 "c_hsharpe": "Sharpe segurar", "c_cagr": "CAGR", "c_hcagr": "CAGR segurar", "c_dd": "Drawdown máximo",
 "c_hdd": "Drawdown segurar", "c_exp": "No mercado", "c_p": "p-valor", "c_beats": "Vence segurar",
 "c_win": "Conta como acerto", "yes": "sim", "no": "não",
 "equity_h": "Curvas de capital",
 "equity_note": "Crescimento de 1 unidade, escala logarítmica, com taxas. Só contam os dias em que a regra está "
                "totalmente definida.",
 "select_label": "Ativo e período", "strategy": "Estratégia (após taxas)", "hold": "Comprar e segurar",
 "why_h": "Por que poderia funcionar", "history_h": "Histórico de veredictos", "engine_src": "este motor, dados até {d}",
 "spec_h": "Especificação pré-registrada",
 "caution": "Esta hipótese passou no teste pré-registrado. Isso é motivo para confirmação independente e trading "
            "simulado, não para operar com dinheiro real.",
 "families": {"trend": "tendência", "flows": "fluxos", "sentiment": "sentimento", "carry": "carry",
              "intraday": "intradiário", "other": "outro", "risk": "risco", "calendar": "calendário"},
 "statuses": {"draft": "rascunho", "registered": "registrada", "passed": "aprovada", "weak": "fraca",
              "rejected": "rejeitada", "archived": "arquivada"},
 "glossary": [
  ("O que é comprar e segurar?", "Comprar uma moeda uma vez e mantê-la. Toda estratégia aqui é comparada com isso: se "
   "não vence ficar parado, não vale o esforço nem as taxas."),
  ("O que é uma hipótese?", "Uma ideia de trading escrita como regra precisa, por exemplo “manter Bitcoin só enquanto "
   "o preço estiver acima da média de 50 dias”. Ela é escrita e travada antes do teste."),
  ("O que é o índice de Sharpe?", "O retorno dividido pelo quanto o caminho balançou, por ano. Maior é melhor. Cerca "
   "de 0,5 é típico para segurar Bitcoin; 1,0 ou mais por muitos anos é raro."),
  ("O que são CAGR e drawdown máximo?", "CAGR é o crescimento anual médio. Drawdown máximo é a pior queda a partir "
   "de um pico: −50% significa que a conta chegou a valer metade do seu máximo."),
  ("O que é p-valor?", "A chance de ver um resultado tão bom se a ideia não tivesse vantagem real. Menor é melhor. "
   "Como muitas ideias são testadas, a meta é mais baixa que o 0,05 usual (correção de Bonferroni)."),
  ("O que significa fora da amostra?", "As regras são escolhidas com um período da história (2018–2021) e avaliadas "
   "em um período posterior que nunca viram (a partir de 2022). Ir bem só nos dados usados para escolher não prova "
   "nada."),
  ("O que é pré-registro?", "Escrever a regra, os dados e o critério de sucesso antes do teste e guardar a impressão "
   "SHA-256. Ninguém pode ajustar o teste em silêncio depois de ver o resultado."),
  ("O que é média móvel (SMA)?", "O preço médio de fechamento dos últimos N dias. “SMA200” é a média de 200 dias; "
   "preço acima dela costuma indicar tendência de alta de longo prazo."),
  ("O que é taxa de funding?", "Uma taxa que traders de futuros pagam entre si a cada oito horas para manter o preço "
   "do futuro perto do real. Quando a maioria aposta na alta, paga quem aposta na queda."),
  ("Posso operar com isso?", "Não. Isto é pesquisa, não recomendação nem serviço de sinais. Nada passou até agora, e "
   "mesmo uma aprovação precisaria de confirmação independente e trading simulado."),
 ],
 "monitors": {
  "h020_rule": ('Regra H-020 hoje: BTC dentro ou fora do mercado', 'A única regra que passou no teste. Ela fica fora do Bitcoin enquanto os depósitos líquidos em corretoras estão nos 20% mais altos do último ano. Não é sinal de operação: ainda está sendo verificada (H-022).'),
  "btc_exchange_flow": ('Fluxo líquido de BTC para corretoras (7 dias)', 'Bitcoin enviado às corretoras menos bitcoin retirado nos últimos 7 dias. Positivo = depósitos líquidos (costuma indicar vendas à frente); negativo = saques para carteiras próprias.'),
  "breadth": ('Amplitude do mercado: moedas acima da média de 200 dias', 'Parte das 13 moedas com preço acima da própria média de 200 dias. Alto = a maior parte do mercado está em alta; baixo = a maioria está caindo.'),
  "ever_trend": ('Everscale (EVER) versus sua média de 50 dias', 'Quanto o EVER na Gate.io está acima (+) ou abaixo (−) da média de 50 dias. É a regra H-018: acima = no mercado, abaixo = fora.'),
  "funding_carry": ("Carry de funding do BTC: rendimento anual após custos",
                    "Quanto você ganharia por ano segurando BTC e vendendo a mesma quantidade em futuros, de modo que "
                    "o preço não importa. Quando a maioria está comprada, os vendidos recebem."),
  "stablecoin_growth": ("Crescimento das stablecoins (30 dias)",
                        "Quão rápido cresce a oferta de moedas atreladas ao dólar (USDT, USDC). Novas stablecoins "
                        "costumam ser dinheiro esperando para comprar cripto; queda significa dinheiro saindo."),
  "fear_greed": ("Índice Fear & Greed cripto",
                 "Uma nota de humor de 0 a 100 baseada em preço, volatilidade e redes sociais. Baixo = medo, alto = "
                 "ganância."),
  "btc_trend": ("BTC versus sua média de 200 dias",
                "Quanto o preço está acima (+) ou abaixo (−) da média dos últimos 200 dias. Acima costuma indicar "
                "tendência de alta de longo prazo."),
  "btc_volatility": ("Volatilidade do BTC (30 dias, anualizada)",
                     "Quanto o preço oscila, em escala anual. 40% significa um movimento anual típico de cerca de 40% "
                     "para cima ou para baixo."),
 },
 "bands": {"rule_in": 'no mercado', "rule_out": 'fora do mercado', "deposits": 'depósitos', "withdrawals": 'saques', "weak": 'fraca', "mixed": 'mista', "strong": 'forte', "negative": "negativo", "low": "baixo", "moderate": "moderado", "attractive": "atraente",
           "contracting": "em queda", "flat": "estável", "expanding": "em alta", "extreme_fear": "medo extremo",
           "fear": "medo", "neutral": "neutro", "greed": "ganância", "extreme_greed": "ganância extrema",
           "below": "abaixo", "above": "acima", "calm": "calmo", "normal": "normal", "stressed": "tenso",
           "unavailable": "sem dados"},
 "notes": {
  ("h020_rule", "rule_out"): 'Depósitos fortes em corretoras: a regra está fora do mercado.',
  ("btc_exchange_flow", "deposits"): 'Depósitos fortes são testados na H-020 (BTC) e na H-021 (ETH).',
  ("ever_trend", "above"): 'A regra H-018 está no mercado. Melhor que segurar, mas não significativo; liquidez muito baixa.',
  ("ever_trend", "below"): 'A regra H-018 está fora do mercado.',
  ("funding_carry", "attractive"): "Rejeitado na H-011 com ~1,5% ao ano. Um carry tão alto merece nova análise.",
  ("funding_carry", "negative"): "Vendidos pagam comprados: posicionamento baixista lotado.",
  ("stablecoin_growth", "expanding"): "Dinheiro entrando em cripto. H-006/H-010 não acharam um sinal confiável nisso.",
  ("fear_greed", "extreme_greed"): "Sair em ≥ 75 (H-008) não venceu segurar.",
 },
 "titles": {
  "H-022": 'Replicação da H-020 com dados coletados após 15/10/2026',
  "H-023": 'Gram (GRAM, antigo Toncoin): a regra SMA50 vence segurar desde 2023',
  "H-024": 'Rotação por força relativa: as 3 moedas mais fortes (1 e 3 dias), sem saltos extremos, só com BTC acima da média de 200 dias',
  "H-025": 'Rotação de momentum simples: as 3 moedas mais fortes em 1 e 3 dias',
  "H-026": 'Reversão de curto prazo: as 3 moedas que mais caíram ontem',
  "H-020": 'BTC fora do mercado quando os depósitos líquidos de 7 dias em corretoras estão nos 20% mais altos',
  "H-021": 'ETH fora do mercado quando os depósitos líquidos de 7 dias em corretoras estão nos 20% mais altos',
  "H-012": 'Meta de volatilidade (30%/ano) vence segurar em BTC, ETH, SOL',
  "H-013": 'Meta de volatilidade (30%/ano) vence segurar em 8 moedas independentes',
  "H-014": 'Momentum semanal: segurar só após alta de 7 dias (BTC, ETH, SOL)',
  "H-015": 'Efeito segunda-feira: BTC só às segundas (UTC) vence segurar',
  "H-016": 'Virada do mês: BTC só nos últimos 2 e primeiros 3 dias do mês',
  "H-017": 'Filtro do Bitcoin: altcoins só enquanto o BTC estiver acima da média de 200 dias',
  "H-018": 'Everscale (EVER): a regra SMA50 vence segurar desde 2022',
  "H-019": 'Everscale (EVER): segurar só enquanto o BTC estiver acima da média de 200 dias',
  "H-001": "Conjunto de indicadores de minuto (RSI, MACD, EMA, momentum) prevê a direção em 1–4 h",
  "H-002": "Sinais de minuto invertidos são lucrativos após taxas",
  "H-003": "A melhor regra de tendência diária (escolhida em 2018–2021) vence segurar fora da amostra, spot",
  "H-004": "A melhor regra de tendência diária, comprado/vendido em futuros, vence segurar",
  "H-005": "SMA50 (comprado ou fora, spot) vence segurar em 8 moedas independentes",
  "H-006": "Comprado em BTC quando o crescimento de 7 dias de USDT+USDC está acima da mediana anual",
  "H-007": "BTC fora do mercado quando o funding de 7 dias está acima do percentil 80 anual",
  "H-008": "BTC fora do mercado quando Fear & Greed ≥ 75",
  "H-009": "Comprado em BTC só quando o fluxo líquido de 5 dias dos ETFs à vista é positivo",
  "H-010": "Timing por stablecoins (H-006) vence segurar em 8 moedas independentes",
  "H-011": "O carry de funding do BTC (spot comprado + perpétuo vendido) compensa o risco",
 },
},
# ---------------------------------------------------------------- Turkish
"tr": {
 'nav_coins': 'Coinler',
 'coins_title': 'Coinler',
 'coins_intro': 'Çalışmalarda kullanılan tüm coinler: bugünkü fiyat, trend ve volatilite. Grafiğini ve test edilen her kuralın bugün ne dediğini görmek için bir coin açın.',
 'th_coin': 'Coin',
 'th_price': 'Fiyat',
 'th_7d': '7 gün',
 'th_30d': '30 gün',
 'th_vs200': '200 günlük ortalamaya göre',
 'th_vol': 'Volatilite (30 g)',
 'coin_title': '{name} ({ticker}): fiyat, trend, volatilite ve test edilen kurallar',
 'coin_desc': '{name} ({ticker}) bugün: {price}, 30 günde {ch30}, 200 günlük ortalamaya göre {vs200}. Trend, volatilite ve test edilen her alım satım kuralının durumu, her gün güncellenir.',
 'coin_lead': '{exchange} günlük kapanışları (UTC). Son gün: {date}.',
 'back_coins': '← Tüm coinler',
 'chart12_h': 'Son 12 ay',
 'close_label': '{ticker} kapanış',
 'sma50': '50 günlük ortalama',
 'stats_h': 'Rakamlar',
 'st_price': 'Fiyat',
 'st_7d': 'Değişim, 7 gün',
 'st_30d': 'Değişim, 30 gün',
 'st_1y': 'Değişim, 1 yıl',
 'st_sma50': '50 günlük ortalamaya göre',
 'st_sma200': '200 günlük ortalamaya göre',
 'st_vol': 'Volatilite (30 gün, yıllık)',
 'signals_h': 'Test edilen kurallar bugün ne diyor',
 'signals_warn': 'Bunlar hipotezlerdeki kuralların bugünkü durumlarıdır. Hiçbiri testini geçmedi, bu yüzden al ya da sat sinyali değildir. Her kuralın ne yapacağını gösterir; böylece davranışını izleyebilirsiniz.',
 'sig_sma50': 'Trend: fiyat 50 günlük ortalamanın üzerinde',
 'sig_mom7': 'Haftalık momentum: fiyat 7 gün öncesinden yüksek',
 'sig_vol': 'Volatilite hedefi (yıllık %30): tam pozisyonun payı',
 'sig_btc': 'Piyasa rejimi: Bitcoin 200 günlük ortalamanın üzerinde',
 'state_in': 'piyasada',
 'state_out': 'piyasa dışında',
 'th_rule': 'Kural',
 'th_state': 'Bugün',
 'th_tested_in': 'Test edildiği yer',
 'coin_studies_h': 'Bu coini içeren çalışmalar',
 'no_studies': 'Bu coin yalnızca piyasa filtresi olarak kullanılıyor.',
 'thin_note': "Bu coin Binance'te değil {exchange} üzerinde işlem görüyor. Likidite düşük; küçük işlemlerle fiyat sıçrayabilir.",
 'th_peak': 'Zirveden',
 'th_100': '1 yıl önce 100$ →',
 'st_peak': '{since} tarihinden beri en yüksek kapanıştan ({date}, {peak})',
 'st_100': '1 yıl önce yatırılan 100$ şimdi',
 'st_corr': 'Bitcoin ile korelasyon (90 gün)',
 'corr_note': "Korelasyon: 1 = Bitcoin ile tam aynı hareket, 0 = ilişki yok, −1 = ters hareket. Çoğu coin 0,6'nın üzerinde; bu yüzden birkaç coin tutmak tek coin tutmaktan pek daha güvenli değil.",
 "plain_scheduled": 'Veri toplanıyor. Önceden kayıtlı test, bir yıllık veri biriktiğinde {date} tarihinde yapılacak.',
 "sig_rule": 'Kural {id}',
 "site_title": "Crypto Research Labs: açık, önceden kayıtlı kripto alım satım araştırması",
 "site_desc": "Açık ve önceden kayıtlı kripto alım satım araştırması: {verdict} Canlı piyasa rejimi (BTC funding "
              "carry, stablecoin arzı, Korku ve Açgözlülük, trend, volatilite) ve her hipotez otomatik olarak yeniden "
              "test edilir.",
 "hyp_desc": "{id} ({verdict}): {title}. {plain}",
 "nav_dashboard": "Panel", "nav_new": "Yeni misiniz?", "nav_regime": "Piyasa bugün", "nav_hyp": "Hipotezler",
 "nav_glossary": "Sözlük", "nav_method": "Yöntem", "lang_label": "Dil",
 "updated": "Güncellendi {t} · veriler: Binance, OKX, DefiLlama, alternative.me, BGeometrics",
 "h1": "Crypto Research Labs: açık, önceden kayıtlı kripto alım satım araştırması",
 "lead": "Her alım satım fikri önce yazılır, bir hash ile kilitlenir ve ancak sonra gerçek piyasa verisiyle, örneklem "
         "dışında ve istatistiksel bir sıfır hipotezine karşı test edilir. Zamanlanmış ajanlar verileri her gün "
         "günceller, piyasayı izler ve eski fikirleri yeni verilerle yeniden test eder. {verdict}",
 "verdict_none": "Şimdiye kadar test edilen {n} hipotezin hiçbiri önceden kayıtlı testini geçemedi.",
 "verdict_some": "{n} hipotezden {p} tanesi önceden kayıtlı testini geçiyor.",
 "how_title": "Yeni misiniz? Bu sayfa nasıl okunur",
 "how": [
  "<strong>Soru.</strong> Basit ve herkese açık bir kural, komisyonlardan sonra bir coini alıp tutmaktan daha iyi "
  "olabilir mi? Deneyenlerin çoğu olamayacağını görür. Bu proje bunu dürüstçe kontrol eder.",
  "<strong>Piyasa bugün</strong> kripto piyasasının bugünkü durumunu gösterir: Bitcoin trendde mi, ne kadar gergin, "
  "yeni para giriyor mu. Piyasayı tarif eder; al ya da sat sinyali değildir.",
  "<strong>Hipotezler</strong> test edilen tüm fikirleri listeler. {pass} önceden belirlenen çıtayı geçtiği, {weak} "
  "“biraz daha iyi ama şans olabilir”, {fail} ise tutmayı geçemediği anlamına gelir.",
  "Herhangi bir hipotezi açarak rakamlarını ve 1 doların kuralla ve sadece tutarak nasıl büyüyeceğini gösteren "
  "grafiği görebilirsiniz.",
  "Bilmediğiniz bir kelime mi var? Aşağıdaki <a href=\"#glossary\">sözlüğe</a> bakın.",
 ],
 "regime_title": "Piyasa bugün",
 "regime_intro": "Geçmiş kararları belirleyen koşullar her gün yeniden hesaplanır. Bir gösterge başka bir aralığa "
                 "geçtiğinde uyarı gönderilir.",
 "source_down": "Kaynağa ulaşılamıyor",
 "btc_title": "Bitcoin ve 200 günlük ortalaması",
 "btc_text": "BTC {date} tarihinde <strong>{price}</strong> seviyesinden kapandı; 200 günlük hareketli ortalamaya "
             "({sma}) göre {diff}. Logaritmik ölçek, 2020'den bu yana günlük kapanışlar.",
 "btc_close": "BTC/USDT kapanış", "sma200": "200 günlük ortalama",
 "hyp_title": "Test edilen hipotezler",
 "hyp_intro": "{pass} = önceden kayıtlı kriter sağlandı. {weak} = çoğu zaman al-tut stratejisini geçiyor ama anlamlı "
              "değil. {fail} = ikisi de değil. Tüm sonuçlar için bir hipotezi açın.",
 "th_id": "ID", "th_hyp": "Hipotez", "th_family": "Tür", "th_verdict": "Karar", "th_tested": "Test tarihi",
 "th_plain": "Ne anlama geliyor",
 "glossary_title": "Yeni başlayanlar için sözlük",
 "method_title": "Yöntem",
 "method": [
  "<strong>Ön kayıt.</strong> Çalışmanın tanımı çalıştırılmadan önce hash'lenir (SHA-256). Sonraki her değişiklik "
  "kontrolü bozar; sonuçları gördükten sonra parametre ayarlanamaz.",
  "<strong>Geleceğe bakmak yok.</strong> Tüm zamanlar UTC; günlük kapanıştaki karar ertesi gün uygulanır; dış veriler "
  "yayın gecikmesi kadar kaydırılır.",
  "<strong>Örneklem dışı.</strong> Kurallar 2018–2021 verisiyle seçilir, 2022'den itibaren komisyonlarla değerlendirilir.",
  "<strong>Sıfır hipotezine karşı.</strong> Bonferroni düzeltmeli bootstrap ve döngüsel kaydırma testleri, ardından "
  "kuralın tasarımında kullanılmayan sekiz coinde doğrulama.",
 ],
 "method_more": "Ayrıntılı açıklama (İngilizce)",
 "data_title": "Veri güncelliği", "th_series": "Seri", "th_from": "Başlangıç", "th_last": "Son gün",
 "th_behind": "Gecikme (gün)",
 "footer_disclaimer": "<strong>Yatırım tavsiyesi değildir.</strong> Crypto Research Labs açık bir araştırma "
                      "projesidir. İşlem yapmaz, para yönetmez ve sinyal satmaz. “Geçti”, sonucun daha yakından "
                      "incelenmeye değer olduğu anlamına gelir; para kazandıracağı anlamına gelmez.",
 "footer_source": "Kaynak kod, veri hattı ve tüm hipotezler", "footer_data": "makine tarafından okunabilir veri",
 "Pass": "Geçti", "Weak": "Zayıf", "Fail": "Kaldı",
 "plain_PASS": "Fikir, testten önce belirlenen çıtayı geçti. Bağımsız olarak yeniden incelenmeyi hak ediyor. Kâr "
               "vaadi değildir.",
 "plain_WEAK": "Fikir alıp tutmaktan biraz daha iyi sonuç verdi, ancak şansı dışlamaya yetmedi. Kanıtlanmamış kabul "
               "edin.",
 "plain_FAIL": "Fikir, coini alıp tutmaktan daha iyi olamadı. Reddedildi.",
 "plain_none": "Henüz test edilmedi.",
 "in_plain": "Kısaca",
 "back": "← Tüm hipotezler", "family": "Tür", "status": "Durum",
 "result_h": "Sonuç", "en_note": "Teknik ayrıntılar motor tarafından üretilir ve İngilizce gösterilir.",
 "metrics_note": "Sharpe: risk birimi başına getiri (yüksek daha iyi). CAGR: ortalama yıllık büyüme. Maksimum düşüş: "
                 "zirveden en kötü düşüş. p-değeri: sonucun şans olma olasılığı (düşük daha iyi). “Tut” sütunları "
                 "aynı varlık ve günler için al-tut sonucudur.",
 "no_results": "Henüz motor sonucu yok: bu çalışma kayıt için saklanıyor ve yeniden çalıştırılmıyor.",
 "c_asset": "Varlık", "c_period": "Dönem", "c_rule": "Kural (örneklem içinde seçildi)", "c_sharpe": "Sharpe",
 "c_hsharpe": "Tut Sharpe", "c_cagr": "CAGR", "c_hcagr": "Tut CAGR", "c_dd": "Maks. düşüş", "c_hdd": "Tut düşüş",
 "c_exp": "Piyasada", "c_p": "p-değeri", "c_beats": "Tutmayı geçti", "c_win": "Başarı sayıldı",
 "yes": "evet", "no": "hayır",
 "equity_h": "Sermaye eğrileri",
 "equity_note": "1 birimin büyümesi, logaritmik ölçek, komisyonlar dahil. Yalnızca kuralın tam tanımlı olduğu günler "
                "sayılır.",
 "select_label": "Varlık ve dönem", "strategy": "Strateji (komisyon sonrası)", "hold": "Al ve tut",
 "why_h": "Neden işe yarayabilir", "history_h": "Karar geçmişi", "engine_src": "bu motor, veri {d} tarihine kadar",
 "spec_h": "Önceden kayıtlı tanım",
 "caution": "Bu hipotez önceden kayıtlı testini geçti. Bu, bağımsız doğrulama ve kağıt üzerinde işlem için bir "
            "nedendir; gerçek parayla işlem için değil.",
 "families": {"trend": "trend", "flows": "akışlar", "sentiment": "duyarlılık", "carry": "carry",
              "intraday": "gün içi", "other": "diğer", "risk": "risk", "calendar": "takvim"},
 "statuses": {"draft": "taslak", "registered": "kayıtlı", "passed": "geçti", "weak": "zayıf",
              "rejected": "reddedildi", "archived": "arşivlendi"},
 "glossary": [
  ("Al ve tut nedir?", "Bir coini bir kez alıp elde tutmak. Buradaki her strateji bununla karşılaştırılır; hiçbir şey "
   "yapmamayı geçemeyen bir strateji emeğe ve komisyona değmez."),
  ("Hipotez nedir?", "Kesin bir kural olarak yazılmış alım satım fikri; örneğin “Bitcoin'i yalnızca fiyatı 50 günlük "
   "ortalamanın üzerindeyken tut”. Test edilmeden önce yazılır ve kilitlenir."),
  ("Sharpe oranı nedir?", "Getirinin, yolun ne kadar sarsıntılı olduğuna bölünmesi, yıllık. Yüksek daha iyi. "
   "Bitcoin'i tutmak için 0,5 civarı tipiktir; uzun yıllar boyunca 1,0 ve üzeri nadirdir."),
  ("CAGR ve maksimum düşüş nedir?", "CAGR ortalama yıllık büyümedir. Maksimum düşüş zirveden en kötü düşüştür: −%50, "
   "hesabın bir noktada en yüksek değerinin yarısına indiği anlamına gelir."),
  ("p-değeri nedir?", "Fikrin gerçek bir avantajı yokken bu kadar iyi bir sonuç görme olasılığı. Düşük daha iyi. Çok "
   "sayıda fikir test edildiği için çıta olağan 0,05'ten düşüktür (Bonferroni düzeltmesi)."),
  ("Örneklem dışı ne demek?", "Kurallar tarihin bir döneminde (2018–2021) seçilir ve hiç görmedikleri sonraki bir "
   "dönemde (2022'den itibaren) değerlendirilir. Yalnızca seçimde kullanılan veride iyi olmak hiçbir şey kanıtlamaz."),
  ("Ön kayıt nedir?", "Kuralı, veriyi ve başarı kriterini testten önce yazmak ve SHA-256 parmak izini saklamak. Kimse "
   "sonucu gördükten sonra testi sessizce değiştiremez."),
  ("Hareketli ortalama (SMA) nedir?", "Son N günün ortalama kapanış fiyatı. “SMA200” 200 günlük ortalamadır; fiyatın "
   "bunun üzerinde olması genellikle uzun vadeli yükseliş trendi demektir."),
  ("Funding oranı nedir?", "Vadeli işlem yapanların, vadeli fiyatı gerçek fiyata yakın tutmak için sekiz saatte bir "
   "birbirine ödediği ücret. Çoğunluk yükselişe oynadığında, düşüşe oynayanlara öder."),
  ("Bununla işlem yapabilir miyim?", "Hayır. Bu bir araştırmadır; tavsiye ya da sinyal hizmeti değildir. Şimdiye "
   "kadar hiçbir şey geçmedi; geçse bile bağımsız doğrulama ve kağıt üzerinde işlem gerekir."),
 ],
 "monitors": {
  "h020_rule": ('H-020 kuralı bugün: BTC piyasada mı dışında mı', "Testini geçen tek kural. Borsalara net yatırmalar son bir yılın en üst %20'sindeyken Bitcoin tutmaz. İşlem sinyali değildir: hâlâ doğrulanıyor (H-022)."),
  "btc_exchange_flow": ('Borsalara net BTC akışı (7 gün)', 'Son 7 günde borsalara gönderilen bitcoin eksi çekilen bitcoin. Artı = net yatırma (çoğunlukla yaklaşan satış olarak okunur), eksi = kişisel cüzdanlara net çekim.'),
  "breadth": ('Piyasa genişliği: 200 günlük ortalamanın üzerindeki coinler', '13 coinden fiyatı kendi 200 günlük ortalamasının üzerinde olanların payı. Yüksek = piyasanın çoğu yükselişte; düşük = coinlerin çoğu düşüyor.'),
  "ever_trend": ('Everscale (EVER) ve 50 günlük ortalaması', "EVER'in Gate.io'da 50 günlük ortalamasının ne kadar üstünde (+) ya da altında (−) olduğu. H-018 kuralı: üstünde = piyasada, altında = dışarıda."),
  "funding_carry": ("BTC funding carry: maliyet sonrası yıllık getiri",
                    "BTC tutup aynı miktarda BTC vadeli işlemi açığa satarak yılda ne kazanacağınız; fiyatın önemi "
                    "kalmaz. Vadelide çoğunluk long iken short'lara ödeme yapılır."),
  "stablecoin_growth": ("Stablecoin arz büyümesi (30 gün)",
                        "Dolara sabitlenmiş coinlerin (USDT, USDC) arzının ne kadar hızlı büyüdüğü. Yeni stablecoinler "
                        "genellikle kripto almayı bekleyen paradır; azalma paranın çıktığını gösterir."),
  "fear_greed": ("Kripto Korku ve Açgözlülük endeksi",
                 "Fiyat hareketleri, volatilite ve sosyal medyadan oluşturulan 0–100 arası duygu puanı. Düşük = korku, "
                 "yüksek = açgözlülük."),
  "btc_trend": ("BTC ve 200 günlük ortalaması",
                "Fiyatın son 200 günün ortalamasının ne kadar üstünde (+) ya da altında (−) olduğu. Üstünde olması "
                "genellikle uzun vadeli yükseliş demektir."),
  "btc_volatility": ("BTC volatilitesi (30 gün, yıllık)",
                     "Fiyatın yıllık ölçekte ne kadar dalgalandığı. %40, yaklaşık %40 yukarı veya aşağı tipik bir "
                     "yıllık hareket demektir."),
 },
 "bands": {"rule_in": 'piyasada', "rule_out": 'piyasa dışında', "deposits": 'yatırma', "withdrawals": 'çekim', "weak": 'zayıf', "mixed": 'karışık', "strong": 'güçlü', "negative": "negatif", "low": "düşük", "moderate": "orta", "attractive": "cazip",
           "contracting": "daralıyor", "flat": "yatay", "expanding": "genişliyor", "extreme_fear": "aşırı korku",
           "fear": "korku", "neutral": "nötr", "greed": "açgözlülük", "extreme_greed": "aşırı açgözlülük",
           "below": "altında", "above": "üstünde", "calm": "sakin", "normal": "normal", "stressed": "gergin",
           "unavailable": "veri yok"},
 "notes": {
  ("h020_rule", "rule_out"): 'Borsalara yoğun yatırma: kural piyasa dışında.',
  ("btc_exchange_flow", "deposits"): "Yoğun yatırmalar H-020 (BTC) ve H-021'de (ETH) test ediliyor.",
  ("ever_trend", "above"): 'H-018 kuralı piyasada. Tutmaktan iyi ama anlamlı değil; likidite çok düşük.',
  ("ever_trend", "below"): 'H-018 kuralı piyasa dışında.',
  ("funding_carry", "attractive"): "H-011'de yılda ~%1,5 ile reddedildi. Bu kadar yüksek carry yeniden incelenmeli.",
  ("funding_carry", "negative"): "Short'lar long'lara ödüyor: kalabalık düşüş pozisyonları.",
  ("stablecoin_growth", "expanding"): "Kriptoya para giriyor. H-006/H-010 bunda güvenilir bir sinyal bulamadı.",
  ("fear_greed", "extreme_greed"): "≥ 75'te çıkmak (H-008) tutmayı geçemedi.",
 },
 "titles": {
  "H-022": "H-020'nin 15.10.2026 sonrası toplanan verilerle tekrarı",
  "H-023": "Gram (GRAM, eski Toncoin): SMA50 kuralı 2023'ten beri al-tut'u geçer",
  "H-024": 'Göreli güç rotasyonu: en güçlü 3 coin (1 ve 3 gün), aşırı sıçramalar hariç, yalnızca BTC 200 günlük ortalamanın üzerindeyken',
  "H-025": 'Basit momentum rotasyonu: 1 ve 3 günde en güçlü 3 coin',
  "H-026": 'Kısa vadeli geri dönüş: dün en çok düşen 3 coin',
  "H-020": "7 günlük net borsa yatırmaları en üst %20'deyken BTC piyasa dışında",
  "H-021": "7 günlük net borsa yatırmaları en üst %20'deyken ETH piyasa dışında",
  "H-012": "Volatilite hedefi (yıllık %30) BTC, ETH, SOL'da al-tut'u geçer",
  "H-013": "Volatilite hedefi (yıllık %30) 8 bağımsız coinde al-tut'u geçer",
  "H-014": 'Haftalık momentum: yalnızca 7 günlük yükselişten sonra tut (BTC, ETH, SOL)',
  "H-015": "Pazartesi etkisi: BTC'yi yalnızca pazartesileri (UTC) tutmak al-tut'u geçer",
  "H-016": 'Ay dönümü: BTC yalnızca ayın son 2 ve ilk 3 gününde',
  "H-017": 'Bitcoin filtresi: altcoinler yalnızca BTC 200 günlük ortalamanın üzerindeyken',
  "H-018": "Everscale (EVER): SMA50 kuralı 2022'den beri al-tut'u geçer",
  "H-019": 'Everscale (EVER): yalnızca BTC 200 günlük ortalamanın üzerindeyken tut',
  "H-001": "Dakikalık gösterge topluluğu (RSI, MACD, EMA, momentum) 1–4 saatlik yönü tahmin eder",
  "H-002": "Ters çevrilmiş dakikalık sinyaller komisyon sonrası kârlıdır",
  "H-003": "En iyi günlük trend kuralı (2018–2021'de seçildi) örneklem dışında al-tut'u geçer, spot",
  "H-004": "En iyi günlük trend kuralı, vadelide long/short, al-tut'u geçer",
  "H-005": "SMA50 (long ya da dışarıda, spot) 8 bağımsız coinde al-tut'u geçer",
  "H-006": "USDT+USDC'nin 7 günlük büyümesi yıllık medyanın üzerindeyken BTC long",
  "H-007": "7 günlük funding yıllık 80. yüzdeliğin üzerindeyken BTC piyasa dışında",
  "H-008": "Korku ve Açgözlülük ≥ 75 iken BTC piyasa dışında",
  "H-009": "Spot ETF'lere 5 günlük net akış pozitifken yalnızca BTC long",
  "H-010": "Stablecoin zamanlaması (H-006) 8 bağımsız coinde al-tut'u geçer",
  "H-011": "BTC funding carry (spot long + sürekli vadeli short) riske değer",
 },
},
# ---------------------------------------------------------------- Vietnamese
"vi": {
 'nav_coins': 'Đồng coin',
 'coins_title': 'Các đồng coin',
 'coins_intro': 'Mọi đồng coin dùng trong nghiên cứu: giá, xu hướng và độ biến động hôm nay. Mở một đồng coin để xem biểu đồ và mỗi quy tắc đã kiểm tra đang nói gì hôm nay.',
 'th_coin': 'Coin',
 'th_price': 'Giá',
 'th_7d': '7 ngày',
 'th_30d': '30 ngày',
 'th_vs200': 'so với TB 200 ngày',
 'th_vol': 'Biến động (30 ngày)',
 'coin_title': '{name} ({ticker}): giá, xu hướng, biến động và các quy tắc đã kiểm tra',
 'coin_desc': '{name} ({ticker}) hôm nay: {price}, {ch30} trong 30 ngày, {vs200} so với trung bình 200 ngày. Xu hướng, biến động và trạng thái của mọi quy tắc giao dịch đã kiểm tra, cập nhật hằng ngày.',
 'coin_lead': 'Giá đóng cửa ngày từ {exchange} (UTC). Ngày cuối: {date}.',
 'back_coins': '← Tất cả coin',
 'chart12_h': '12 tháng gần nhất',
 'close_label': 'Giá đóng cửa {ticker}',
 'sma50': 'Trung bình 50 ngày',
 'stats_h': 'Số liệu',
 'st_price': 'Giá',
 'st_7d': 'Thay đổi 7 ngày',
 'st_30d': 'Thay đổi 30 ngày',
 'st_1y': 'Thay đổi 1 năm',
 'st_sma50': 'So với TB 50 ngày',
 'st_sma200': 'So với TB 200 ngày',
 'st_vol': 'Biến động (30 ngày, theo năm)',
 'signals_h': 'Các quy tắc đã kiểm tra nói gì hôm nay',
 'signals_warn': 'Đây là trạng thái hôm nay của các quy tắc trong giả thuyết. Chưa quy tắc nào vượt qua kiểm tra, nên đây không phải tín hiệu mua hay bán. Chúng cho thấy mỗi quy tắc sẽ làm gì để bạn theo dõi cách nó vận hành.',
 'sig_sma50': 'Xu hướng: giá trên trung bình 50 ngày',
 'sig_mom7': 'Động lượng 1 tuần: giá cao hơn 7 ngày trước',
 'sig_vol': 'Mục tiêu biến động (30%/năm): tỷ lệ của một vị thế đầy đủ',
 'sig_btc': 'Trạng thái thị trường: Bitcoin trên trung bình 200 ngày',
 'state_in': 'trong thị trường',
 'state_out': 'đứng ngoài',
 'th_rule': 'Quy tắc',
 'th_state': 'Hôm nay',
 'th_tested_in': 'Kiểm tra trong',
 'coin_studies_h': 'Các nghiên cứu có đồng coin này',
 'no_studies': 'Đồng coin này chỉ được dùng làm bộ lọc thị trường.',
 'thin_note': 'Đồng coin này giao dịch trên {exchange}, không phải Binance. Thanh khoản thấp nên giá có thể nhảy mạnh chỉ với giao dịch nhỏ.',
 'th_peak': 'Từ đỉnh',
 'th_100': '$100 một năm trước →',
 'st_peak': 'So với giá đóng cửa cao nhất từ {since} ({peak} ngày {date})',
 'st_100': '$100 đầu tư một năm trước giờ là',
 'st_corr': 'Tương quan với Bitcoin (90 ngày)',
 'corr_note': 'Tương quan: 1 = biến động y như Bitcoin, 0 = không liên quan, −1 = ngược chiều. Đa số coin trên 0,6, nên giữ nhiều coin cũng không an toàn hơn nhiều so với giữ một coin.',
 "plain_scheduled": 'Dữ liệu đang được thu thập. Bài kiểm tra đã đăng ký trước sẽ chạy vào {date}, khi đủ một năm dữ liệu.',
 "sig_rule": 'Quy tắc {id}',
 "site_title": "Crypto Research Labs: nghiên cứu giao dịch tiền mã hóa mở, đăng ký trước",
 "site_desc": "Nghiên cứu chiến lược giao dịch tiền mã hóa mở và đăng ký trước: {verdict} Trạng thái thị trường trực "
              "tiếp (lợi suất funding BTC, nguồn cung stablecoin, chỉ số Sợ hãi & Tham lam, xu hướng, biến động) và "
              "mọi giả thuyết được kiểm tra lại tự động.",
 "hyp_desc": "{id} ({verdict}): {title}. {plain}",
 "nav_dashboard": "Bảng điều khiển", "nav_new": "Người mới?", "nav_regime": "Thị trường hôm nay",
 "nav_hyp": "Giả thuyết", "nav_glossary": "Thuật ngữ", "nav_method": "Phương pháp", "lang_label": "Ngôn ngữ",
 "updated": "Cập nhật {t} · dữ liệu từ Binance, OKX, DefiLlama, alternative.me, BGeometrics",
 "h1": "Crypto Research Labs: nghiên cứu giao dịch tiền mã hóa mở, đăng ký trước",
 "lead": "Mỗi ý tưởng giao dịch được viết ra, khóa bằng mã băm rồi mới được kiểm tra trên dữ liệu thị trường thật, "
         "ngoài mẫu và so với giả thuyết không thống kê. Các tác tử chạy theo lịch cập nhật dữ liệu hằng ngày, theo dõi "
         "thị trường và kiểm tra lại ý tưởng cũ khi có dữ liệu mới. {verdict}",
 "verdict_none": "Chưa giả thuyết nào trong số {n} giả thuyết đã kiểm tra vượt qua bài kiểm tra đăng ký trước.",
 "verdict_some": "{p} trên {n} giả thuyết vượt qua bài kiểm tra đăng ký trước.",
 "how_title": "Người mới? Cách đọc trang này",
 "how": [
  "<strong>Câu hỏi.</strong> Một quy tắc đơn giản, công khai có thể thắng việc chỉ mua một đồng coin rồi giữ, sau phí "
  "giao dịch không? Đa số người thử đều thấy là không. Dự án này kiểm tra điều đó một cách trung thực.",
  "<strong>Thị trường hôm nay</strong> cho thấy tình hình thị trường crypto: Bitcoin có xu hướng không, căng thẳng "
  "đến đâu, có tiền mới đổ vào không. Đây là mô tả thị trường, không phải tín hiệu mua hay bán.",
  "<strong>Giả thuyết</strong> liệt kê mọi ý tưởng đã kiểm tra. {pass} nghĩa là đạt mức đặt ra từ trước, {weak} nghĩa "
  "là “tốt hơn một chút nhưng có thể do may mắn”, {fail} nghĩa là không thắng việc giữ.",
  "Mở bất kỳ giả thuyết nào để xem số liệu và biểu đồ 1 đô la sẽ tăng thế nào theo quy tắc so với chỉ giữ.",
  "Gặp từ lạ? Xem <a href=\"#glossary\">bảng thuật ngữ</a> bên dưới.",
 ],
 "regime_title": "Thị trường hôm nay",
 "regime_intro": "Các điều kiện quyết định những kết luận trước đây, được tính lại mỗi ngày. Chỉ gửi cảnh báo khi một "
                 "chỉ số chuyển sang vùng khác.",
 "source_down": "Nguồn không khả dụng",
 "btc_title": "Bitcoin so với đường trung bình 200 ngày",
 "btc_text": "BTC đóng cửa ở <strong>{price}</strong> ngày {date}, {diff} so với đường trung bình động 200 ngày "
             "({sma}). Thang logarit, giá đóng cửa hằng ngày từ năm 2020.",
 "btc_close": "Giá đóng cửa BTC/USDT", "sma200": "Trung bình 200 ngày",
 "hyp_title": "Các giả thuyết đã kiểm tra",
 "hyp_intro": "{pass} = đạt tiêu chí đăng ký trước. {weak} = thường thắng mua và giữ nhưng không có ý nghĩa thống kê. "
              "{fail} = không đạt cả hai. Mở một giả thuyết để xem toàn bộ kết quả.",
 "th_id": "ID", "th_hyp": "Giả thuyết", "th_family": "Loại", "th_verdict": "Kết luận", "th_tested": "Ngày kiểm tra",
 "th_plain": "Ý nghĩa",
 "glossary_title": "Thuật ngữ cho người mới",
 "method_title": "Phương pháp",
 "method": [
  "<strong>Đăng ký trước.</strong> Mô tả nghiên cứu được băm (SHA-256) trước khi chạy. Mọi thay đổi sau đó đều làm "
  "hỏng kiểm tra, nên không thể chỉnh tham số sau khi thấy kết quả.",
  "<strong>Không nhìn trước tương lai.</strong> Mọi thời gian theo UTC; quyết định lúc đóng cửa ngày được áp dụng cho "
  "ngày hôm sau; dữ liệu bên ngoài được lùi theo độ trễ công bố.",
  "<strong>Ngoài mẫu.</strong> Quy tắc được chọn trên 2018–2021 và đánh giá từ 2022 trở đi, có tính phí.",
  "<strong>So với giả thuyết không.</strong> Kiểm định bootstrap và dịch vòng với hiệu chỉnh Bonferroni, sau đó xác "
  "nhận trên tám đồng coin không dùng để thiết kế quy tắc.",
 ],
 "method_more": "Mô tả đầy đủ (tiếng Anh)",
 "data_title": "Độ mới của dữ liệu", "th_series": "Chuỗi", "th_from": "Từ", "th_last": "Ngày cuối",
 "th_behind": "Trễ (ngày)",
 "footer_disclaimer": "<strong>Không phải lời khuyên tài chính.</strong> Crypto Research Labs là một dự án nghiên cứu "
                      "mở. Dự án không giao dịch, không quản lý tiền và không bán tín hiệu. “Đạt” nghĩa là kết quả "
                      "đáng được xem xét kỹ hơn, không có nghĩa là sẽ kiếm được tiền.",
 "footer_source": "Mã nguồn, quy trình dữ liệu và mọi giả thuyết", "footer_data": "dữ liệu dạng máy đọc được",
 "Pass": "Đạt", "Weak": "Yếu", "Fail": "Không đạt",
 "plain_PASS": "Ý tưởng đã đạt mức đặt ra trước khi kiểm tra. Nó đáng được xem xét độc lập. Đây không phải lời hứa "
               "lợi nhuận.",
 "plain_WEAK": "Ý tưởng tốt hơn một chút so với mua và giữ, nhưng chưa đủ để loại trừ may mắn. Hãy coi là chưa được "
               "chứng minh.",
 "plain_FAIL": "Ý tưởng không thắng việc chỉ mua coin rồi giữ. Nó bị loại.",
 "plain_none": "Chưa được kiểm tra.",
 "in_plain": "Nói đơn giản",
 "back": "← Tất cả giả thuyết", "family": "Loại", "status": "Trạng thái",
 "result_h": "Kết quả", "en_note": "Chi tiết kỹ thuật do công cụ tạo ra và hiển thị bằng tiếng Anh.",
 "metrics_note": "Sharpe: lợi nhuận trên mỗi đơn vị rủi ro (càng cao càng tốt). CAGR: tăng trưởng trung bình năm. "
                 "Sụt giảm tối đa: mức giảm tệ nhất từ đỉnh. p-value: khả năng kết quả do may mắn (càng thấp càng tốt). "
                 "Các cột “Giữ” là mua và giữ cùng tài sản trong cùng các ngày.",
 "no_results": "Chưa có kết quả từ công cụ: nghiên cứu này được lưu để tham khảo và không chạy lại.",
 "c_asset": "Tài sản", "c_period": "Giai đoạn", "c_rule": "Quy tắc (chọn trong mẫu)", "c_sharpe": "Sharpe",
 "c_hsharpe": "Sharpe giữ", "c_cagr": "CAGR", "c_hcagr": "CAGR giữ", "c_dd": "Sụt giảm tối đa", "c_hdd": "Sụt giảm giữ",
 "c_exp": "Trong thị trường", "c_p": "p-value", "c_beats": "Thắng giữ", "c_win": "Tính là thắng",
 "yes": "có", "no": "không",
 "equity_h": "Đường vốn",
 "equity_note": "Tăng trưởng của 1 đơn vị, thang logarit, đã tính phí. Chỉ tính những ngày quy tắc được xác định đầy đủ.",
 "select_label": "Tài sản và giai đoạn", "strategy": "Chiến lược (sau phí)", "hold": "Mua và giữ",
 "why_h": "Vì sao có thể hiệu quả", "history_h": "Lịch sử kết luận", "engine_src": "công cụ này, dữ liệu đến {d}",
 "spec_h": "Đặc tả đã đăng ký trước",
 "caution": "Giả thuyết này đã vượt qua bài kiểm tra đăng ký trước. Đó là lý do để xác nhận độc lập và giao dịch thử, "
            "không phải để giao dịch bằng tiền thật.",
 "families": {"trend": "xu hướng", "flows": "dòng tiền", "sentiment": "tâm lý", "carry": "carry",
              "intraday": "trong ngày", "other": "khác", "risk": "rủi ro", "calendar": "lịch"},
 "statuses": {"draft": "bản nháp", "registered": "đã đăng ký", "passed": "đạt", "weak": "yếu",
              "rejected": "bị loại", "archived": "lưu trữ"},
 "glossary": [
  ("Mua và giữ là gì?", "Mua một đồng coin một lần và giữ nó. Mọi chiến lược ở đây đều được so với cách này: chiến lược "
   "không thắng được việc không làm gì thì không đáng công sức và phí."),
  ("Giả thuyết là gì?", "Một ý tưởng giao dịch được viết thành quy tắc chính xác, ví dụ “chỉ giữ Bitcoin khi giá trên "
   "đường trung bình 50 ngày”. Nó được viết ra và khóa lại trước khi kiểm tra."),
  ("Tỷ lệ Sharpe là gì?", "Lợi nhuận chia cho mức độ chao đảo trên đường đi, tính theo năm. Càng cao càng tốt. Khoảng "
   "0,5 là bình thường khi giữ Bitcoin; từ 1,0 trở lên trong nhiều năm là hiếm."),
  ("CAGR và sụt giảm tối đa là gì?", "CAGR là tăng trưởng trung bình mỗi năm. Sụt giảm tối đa là mức giảm tệ nhất từ "
   "đỉnh: −50% nghĩa là có lúc tài khoản chỉ còn một nửa giá trị cao nhất."),
  ("p-value là gì?", "Khả năng thấy kết quả tốt như vậy nếu ý tưởng không có lợi thế thật. Càng nhỏ càng tốt. Vì kiểm "
   "tra nhiều ý tưởng nên ngưỡng thấp hơn mức 0,05 thông thường (hiệu chỉnh Bonferroni)."),
  ("Ngoài mẫu nghĩa là gì?", "Quy tắc được chọn bằng một giai đoạn lịch sử (2018–2021) và đánh giá trên giai đoạn sau mà "
   "nó chưa từng thấy (từ 2022). Chỉ tốt trên dữ liệu dùng để chọn thì không chứng minh được gì."),
  ("Đăng ký trước là gì?", "Viết ra quy tắc, dữ liệu và tiêu chí thành công trước khi kiểm tra, rồi lưu dấu vân tay "
   "SHA-256. Không ai có thể âm thầm chỉnh bài kiểm tra sau khi thấy kết quả."),
  ("Đường trung bình động (SMA) là gì?", "Giá đóng cửa trung bình của N ngày gần nhất. “SMA200” là trung bình 200 ngày; "
   "giá nằm trên thường cho thấy xu hướng tăng dài hạn."),
  ("Funding rate là gì?", "Khoản phí mà người giao dịch hợp đồng tương lai trả cho nhau mỗi tám giờ để giữ giá hợp đồng "
   "gần giá thật. Khi đa số đặt cược giá tăng, họ trả cho những người đặt cược giá giảm."),
  ("Tôi có thể giao dịch theo đây không?", "Không. Đây là nghiên cứu, không phải lời khuyên hay dịch vụ tín hiệu. Đến "
   "nay chưa có gì đạt, và ngay cả khi đạt cũng cần xác nhận độc lập và giao dịch thử trước."),
 ],
 "monitors": {
  "h020_rule": ('Quy tắc H-020 hôm nay: BTC trong hay ngoài thị trường', 'Quy tắc duy nhất đã vượt qua kiểm tra. Nó không giữ Bitcoin khi lượng nạp ròng vào sàn thuộc nhóm 20% cao nhất của năm qua. Không phải tín hiệu giao dịch: vẫn đang được kiểm chứng (H-022).'),
  "btc_exchange_flow": ('Dòng BTC ròng vào sàn (7 ngày)', 'Lượng bitcoin nạp vào sàn trừ lượng rút ra trong 7 ngày qua. Dương = nạp ròng (thường được hiểu là sắp bán), âm = rút ròng về ví cá nhân.'),
  "breadth": ('Độ rộng thị trường: coin trên trung bình 200 ngày', 'Tỷ lệ trong 13 coin có giá trên trung bình 200 ngày của chính nó. Cao = phần lớn thị trường đang tăng; thấp = đa số coin đang giảm.'),
  "ever_trend": ('Everscale (EVER) so với trung bình 50 ngày', 'EVER trên Gate.io cao hơn (+) hay thấp hơn (−) bao nhiêu so với trung bình 50 ngày. Đây là quy tắc H-018: trên = trong thị trường, dưới = đứng ngoài.'),
  "funding_carry": ("Carry funding BTC: lợi suất năm sau chi phí",
                    "Số tiền bạn kiếm được mỗi năm khi giữ BTC và bán khống cùng lượng BTC trên hợp đồng tương lai, nên "
                    "giá không quan trọng. Khi đa số mua (long), bên bán khống được trả tiền."),
  "stablecoin_growth": ("Tăng trưởng stablecoin (30 ngày)",
                        "Tốc độ tăng nguồn cung các đồng neo theo đô la (USDT, USDC). Stablecoin mới thường là tiền chờ "
                        "mua crypto; nguồn cung giảm nghĩa là tiền đang rút ra."),
  "fear_greed": ("Chỉ số Sợ hãi & Tham lam",
                 "Điểm tâm lý từ 0 đến 100 dựa trên biến động giá, độ biến động và mạng xã hội. Thấp = sợ hãi, cao = "
                 "tham lam."),
  "btc_trend": ("BTC so với trung bình 200 ngày",
                "Giá cao hơn (+) hay thấp hơn (−) bao nhiêu so với trung bình 200 ngày qua. Cao hơn thường nghĩa là xu "
                "hướng tăng dài hạn."),
  "btc_volatility": ("Độ biến động BTC (30 ngày, theo năm)",
                     "Giá dao động mạnh đến mức nào, quy ra năm. 40% nghĩa là biến động năm điển hình khoảng 40% lên "
                     "hoặc xuống."),
 },
 "bands": {"rule_in": 'trong thị trường', "rule_out": 'đứng ngoài', "deposits": 'nạp vào sàn', "withdrawals": 'rút khỏi sàn', "weak": 'yếu', "mixed": 'trung tính', "strong": 'mạnh', "negative": "âm", "low": "thấp", "moderate": "vừa phải", "attractive": "hấp dẫn",
           "contracting": "thu hẹp", "flat": "đi ngang", "expanding": "mở rộng", "extreme_fear": "cực kỳ sợ hãi",
           "fear": "sợ hãi", "neutral": "trung lập", "greed": "tham lam", "extreme_greed": "cực kỳ tham lam",
           "below": "dưới", "above": "trên", "calm": "bình lặng", "normal": "bình thường", "stressed": "căng thẳng",
           "unavailable": "không có dữ liệu"},
 "notes": {
  ("h020_rule", "rule_out"): 'Nạp mạnh vào sàn: quy tắc đang đứng ngoài.',
  ("btc_exchange_flow", "deposits"): 'Lượng nạp lớn được kiểm tra trong H-020 (BTC) và H-021 (ETH).',
  ("ever_trend", "above"): 'Quy tắc H-018 đang trong thị trường. Tốt hơn giữ nhưng chưa có ý nghĩa thống kê; thanh khoản rất thấp.',
  ("ever_trend", "below"): 'Quy tắc H-018 đang đứng ngoài.',
  ("funding_carry", "attractive"): "Bị loại ở H-011 với ~1,5%/năm. Mức carry cao thế này đáng kiểm tra lại.",
  ("funding_carry", "negative"): "Bên bán khống trả cho bên mua: vị thế giảm giá quá đông.",
  ("stablecoin_growth", "expanding"): "Tiền đang vào crypto. H-006/H-010 không tìm thấy tín hiệu đáng tin ở đây.",
  ("fear_greed", "extreme_greed"): "Thoát ở ≥ 75 (H-008) không thắng việc giữ.",
 },
 "titles": {
  "H-022": 'Kiểm tra lặp lại H-020 trên dữ liệu thu thập sau 15/10/2026',
  "H-023": 'Gram (GRAM, trước là Toncoin): quy tắc SMA50 thắng mua và giữ từ 2023',
  "H-024": 'Xoay vòng theo sức mạnh tương đối: 3 coin mạnh nhất (1 và 3 ngày), bỏ qua cú tăng đột biến, chỉ khi BTC trên trung bình 200 ngày',
  "H-025": 'Xoay vòng động lượng đơn giản: 3 coin mạnh nhất trong 1 và 3 ngày',
  "H-026": 'Đảo chiều ngắn hạn: 3 coin giảm mạnh nhất hôm qua',
  "H-020": 'BTC đứng ngoài khi lượng nạp ròng vào sàn 7 ngày thuộc nhóm 20% cao nhất',
  "H-021": 'ETH đứng ngoài khi lượng nạp ròng vào sàn 7 ngày thuộc nhóm 20% cao nhất',
  "H-012": 'Mục tiêu biến động (30%/năm) thắng mua và giữ trên BTC, ETH, SOL',
  "H-013": 'Mục tiêu biến động (30%/năm) thắng mua và giữ trên 8 coin độc lập',
  "H-014": 'Động lượng 1 tuần: chỉ giữ sau khi tăng 7 ngày (BTC, ETH, SOL)',
  "H-015": 'Hiệu ứng thứ Hai: chỉ giữ BTC vào thứ Hai (UTC) thắng mua và giữ',
  "H-016": 'Chuyển tháng: chỉ giữ BTC 2 ngày cuối và 3 ngày đầu tháng',
  "H-017": 'Bộ lọc Bitcoin: chỉ giữ altcoin khi BTC trên trung bình 200 ngày',
  "H-018": 'Everscale (EVER): quy tắc SMA50 thắng mua và giữ từ 2022',
  "H-019": 'Everscale (EVER): chỉ giữ khi BTC trên trung bình 200 ngày',
  "H-001": "Tổ hợp chỉ báo theo phút (RSI, MACD, EMA, động lượng) dự đoán hướng trong 1–4 giờ",
  "H-002": "Tín hiệu theo phút đảo ngược có lãi sau phí",
  "H-003": "Quy tắc xu hướng ngày tốt nhất (chọn trên 2018–2021) thắng mua và giữ ngoài mẫu, giao ngay",
  "H-004": "Quy tắc xu hướng ngày tốt nhất, long/short hợp đồng tương lai, thắng mua và giữ",
  "H-005": "SMA50 (long hoặc đứng ngoài, giao ngay) thắng mua và giữ trên 8 coin độc lập",
  "H-006": "Long BTC khi tăng trưởng 7 ngày của USDT+USDC cao hơn trung vị 1 năm",
  "H-007": "BTC đứng ngoài khi funding 7 ngày cao hơn phân vị 80 của 1 năm",
  "H-008": "BTC đứng ngoài khi chỉ số Sợ hãi & Tham lam ≥ 75",
  "H-009": "Chỉ long BTC khi dòng tiền ròng 5 ngày vào ETF giao ngay dương",
  "H-010": "Định thời theo stablecoin (H-006) thắng mua và giữ trên 8 coin độc lập",
  "H-011": "Carry funding BTC (long giao ngay + short hợp đồng vĩnh cửu) đáng với rủi ro",
 },
},
# ---------------------------------------------------------------- Chinese (Simplified)
"zh": {
 'nav_coins': '币种',
 'coins_title': '币种',
 'coins_intro': '研究中使用的所有币种：今日价格、趋势和波动率。打开某个币种可查看其图表，以及每条已检验规则今天的状态。',
 'th_coin': '币种',
 'th_price': '价格',
 'th_7d': '7 天',
 'th_30d': '30 天',
 'th_vs200': '相对 200 日均线',
 'th_vol': '波动率（30 天）',
 'coin_title': '{name}（{ticker}）：价格、趋势、波动率与已检验规则',
 'coin_desc': '{name}（{ticker}）今日：{price}，30 天 {ch30}，相对 200 日均线 {vs200}。趋势、波动率以及每条已检验交易规则的状态，每日更新。',
 'coin_lead': '来自 {exchange} 的日收盘价（UTC）。最新日期：{date}。',
 'back_coins': '← 全部币种',
 'chart12_h': '最近 12 个月',
 'close_label': '{ticker} 收盘价',
 'sma50': '50 日均线',
 'stats_h': '数据',
 'st_price': '价格',
 'st_7d': '7 天涨跌',
 'st_30d': '30 天涨跌',
 'st_1y': '1 年涨跌',
 'st_sma50': '相对 50 日均线',
 'st_sma200': '相对 200 日均线',
 'st_vol': '波动率（30 天，年化）',
 'signals_h': '已检验规则今天的状态',
 'signals_warn': '这些是假设中各条规则今天的状态。它们都没有通过检验，因此不是买卖信号。它们展示每条规则会怎么做，便于观察其表现。',
 'sig_sma50': '趋势：价格高于 50 日均线',
 'sig_mom7': '一周动量：价格高于 7 天前',
 'sig_vol': '目标波动率（年化 30%）：占满仓的比例',
 'sig_btc': '市场状态：比特币高于 200 日均线',
 'state_in': '持仓',
 'state_out': '空仓',
 'th_rule': '规则',
 'th_state': '今天',
 'th_tested_in': '检验于',
 'coin_studies_h': '包含该币种的研究',
 'no_studies': '该币种仅用作市场过滤条件。',
 'thin_note': '该币种在 {exchange} 而非 Binance 交易。流动性较低，小额交易也可能导致价格大幅波动。',
 'th_peak': '距高点',
 'th_100': '一年前的 $100 →',
 'st_peak': '距 {since} 以来最高收盘价（{date}，{peak}）',
 'st_100': '一年前投入的 $100 现在值',
 'st_corr': '与比特币的相关性（90 天）',
 'corr_note': '相关性：1 = 与比特币完全同步，0 = 无关联，−1 = 反向。大多数币高于 0.6，所以持有多个币并不比持有一个安全多少。',
 "plain_scheduled": '数据正在积累中。预注册的检验将在积累一年数据后于 {date} 进行。',
 "sig_rule": '规则 {id}',
 "site_title": "Crypto Research Labs：公开、预注册的加密货币交易研究",
 "site_desc": "公开、预注册的加密货币交易策略研究：{verdict}实时市场状态（BTC 资金费率套利收益、稳定币供应、恐惧与贪婪指数、"
              "趋势、波动率），每个假设都会自动重新检验。",
 "hyp_desc": "{id}（{verdict}）：{title}。{plain}",
 "nav_dashboard": "仪表盘", "nav_new": "新手指南", "nav_regime": "今日市场", "nav_hyp": "假设",
 "nav_glossary": "术语", "nav_method": "方法", "lang_label": "语言",
 "updated": "更新于 {t} · 数据来源：Binance、OKX、DefiLlama、alternative.me、BGeometrics",
 "h1": "Crypto Research Labs：公开、预注册的加密货币交易研究",
 "lead": "每个交易想法都会先写下来并用哈希锁定，然后才在真实市场数据上检验：使用样本外数据，并与统计零假设比较。"
         "定时运行的代理每天更新数据、观察市场，并在新数据到来时重新检验旧想法。{verdict}",
 "verdict_none": "目前检验过的 {n} 个假设中，没有一个通过预注册的检验。",
 "verdict_some": "{n} 个假设中有 {p} 个通过了预注册的检验。",
 "how_title": "第一次来？如何阅读本页",
 "how": [
  "<strong>核心问题。</strong>扣除交易费用后，一个简单、公开的规则能否跑赢“买入并持有”？大多数尝试的人发现不能。"
  "本项目如实地检验这一点。",
  "<strong>今日市场</strong>展示加密市场当前的状况：比特币是否处于趋势中、市场有多紧张、是否有新资金流入。"
  "它描述市场，不是买卖信号。",
  "<strong>假设</strong>列出所有检验过的想法。{pass} 表示达到了事先设定的标准，{weak} 表示“略好一些，但可能是运气”，"
  "{fail} 表示没有跑赢持有。",
  "打开任意一个假设，可以看到数据，以及 1 美元按规则操作与单纯持有分别会如何增长的图表。",
  "遇到不懂的词？请看下方的<a href=\"#glossary\">术语表</a>。",
 ],
 "regime_title": "今日市场",
 "regime_intro": "决定过往结论的市场条件，每天重新计算。只有当某个指标进入另一个区间时才会发送提醒。",
 "source_down": "数据源不可用",
 "btc_title": "比特币与其 200 日均线",
 "btc_text": "BTC 于 {date} 收于 <strong>{price}</strong>，相对 200 日移动平均线（{sma}）{diff}。对数坐标，"
             "2020 年以来的日收盘价。",
 "btc_close": "BTC/USDT 收盘价", "sma200": "200 日均线",
 "hyp_title": "已检验的假设",
 "hyp_intro": "{pass} = 满足预注册标准。{weak} = 多数情况下跑赢买入持有，但不显著。{fail} = 两者都不满足。"
              "打开一个假设可查看完整结果。",
 "th_id": "编号", "th_hyp": "假设", "th_family": "类别", "th_verdict": "结论", "th_tested": "检验日期",
 "th_plain": "含义",
 "glossary_title": "新手术语表",
 "method_title": "研究方法",
 "method": [
  "<strong>预注册。</strong>研究规范在运行前计算 SHA-256 哈希。之后任何修改都会使校验失败，因此无法在看到结果后调整参数。",
  "<strong>不看未来。</strong>所有时间均为 UTC；日收盘时的决定在下一天执行；外部数据按其发布延迟进行滞后处理。",
  "<strong>样本外。</strong>规则在 2018–2021 年数据上选择，从 2022 年起评估，并计入手续费。",
  "<strong>与零假设比较。</strong>使用带 Bonferroni 校正的自助法和循环平移检验，然后在八个未参与规则设计的币种上验证。",
 ],
 "method_more": "完整说明（英文）",
 "data_title": "数据新鲜度", "th_series": "数据序列", "th_from": "起始", "th_last": "最新日期", "th_behind": "滞后天数",
 "footer_disclaimer": "<strong>不构成投资建议。</strong>Crypto Research Labs 是一个开放的研究项目。它不进行交易、不管理资金，"
                      "也不出售信号。“通过”意味着结果值得进一步研究，而不是一定能赚钱。",
 "footer_source": "源代码、数据管道与全部假设", "footer_data": "机器可读数据",
 "Pass": "通过", "Weak": "偏弱", "Fail": "未通过",
 "plain_PASS": "该想法达到了检验前设定的标准，值得独立复核。这不代表一定盈利。",
 "plain_WEAK": "该想法比买入持有略好，但不足以排除运气因素。请视为未被证实。",
 "plain_FAIL": "该想法没有跑赢简单地买入并持有，已被否定。",
 "plain_none": "尚未检验。",
 "in_plain": "通俗地说",
 "back": "← 全部假设", "family": "类别", "status": "状态",
 "result_h": "结果", "en_note": "技术细节由引擎生成，以英文显示。",
 "metrics_note": "Sharpe：单位风险的收益（越高越好）。CAGR：年均增长率。最大回撤：从峰值的最大跌幅。p 值：结果来自运气的概率"
                 "（越低越好）。“持有”列为同一资产、同一时间段的买入持有结果。",
 "no_results": "暂无引擎结果：该研究仅作记录保存，不会重新运行。",
 "c_asset": "资产", "c_period": "区间", "c_rule": "规则（样本内选择）", "c_sharpe": "Sharpe", "c_hsharpe": "持有 Sharpe",
 "c_cagr": "CAGR", "c_hcagr": "持有 CAGR", "c_dd": "最大回撤", "c_hdd": "持有回撤", "c_exp": "持仓时间",
 "c_p": "p 值", "c_beats": "跑赢持有", "c_win": "计为成功", "yes": "是", "no": "否",
 "equity_h": "资金曲线",
 "equity_note": "1 个单位的增长，对数坐标，已计入手续费。仅统计规则完全确定的交易日。",
 "select_label": "资产与区间", "strategy": "策略（扣费后）", "hold": "买入持有",
 "why_h": "为什么可能有效", "history_h": "结论历史", "engine_src": "本引擎，数据截至 {d}",
 "spec_h": "预注册规范",
 "caution": "该假设通过了预注册检验。这意味着应当进行独立验证和模拟交易，而不是用真金白银交易。",
 "families": {"trend": "趋势", "flows": "资金流", "sentiment": "情绪", "carry": "套利", "intraday": "日内", "other": "其他", "risk": "风险", "calendar": "日历"},
 "statuses": {"draft": "草稿", "registered": "已注册", "passed": "通过", "weak": "偏弱", "rejected": "已否定",
              "archived": "已归档"},
 "glossary": [
  ("什么是买入持有？", "买入一次币并一直持有。这里的每个策略都与之比较：连“什么都不做”都跑不赢的策略，不值得付出精力和手续费。"),
  ("什么是假设？", "写成精确规则的交易想法，例如“只在价格高于 50 日均线时持有比特币”。它在检验之前写下并锁定。"),
  ("什么是夏普比率？", "收益除以过程中的波动程度，按年计算。越高越好。持有比特币通常约为 0.5；多年保持 1.0 以上很少见。"),
  ("什么是 CAGR 和最大回撤？", "CAGR 是年均增长率。最大回撤是从峰值的最大跌幅：−50% 表示账户某一时刻只剩最高值的一半。"),
  ("什么是 p 值？", "如果这个想法没有真正优势，仍能看到这么好结果的概率。越小越好。由于检验了很多想法，门槛低于常用的 0.05"
   "（Bonferroni 校正）。"),
  ("什么是样本外？", "规则在一段历史（2018–2021）上选出，在它从未见过的后续时期（2022 年起）上评估。只在选择规则所用的数据上"
   "表现好，什么也证明不了。"),
  ("什么是预注册？", "在检验之前写下规则、数据和成功标准，并保存其 SHA-256 指纹。没有人能在看到结果后悄悄修改检验。"),
  ("什么是移动平均线（SMA）？", "最近 N 天的平均收盘价。“SMA200”是 200 日均线；价格在其上方通常意味着长期上升趋势。"),
  ("什么是资金费率？", "期货交易者之间每八小时互相支付的费用，用来让期货价格贴近现货价格。多数人押注上涨时，他们向押注下跌的人付费。"),
  ("我可以据此交易吗？", "不可以。这是研究，不是投资建议，也不是信号服务。到目前为止没有任何假设通过；即使通过，也需要先独立"
   "验证并进行模拟交易。"),
 ],
 "monitors": {
  "h020_rule": ('H-020 规则今日状态：BTC 持仓还是空仓', '唯一通过检验的规则。当交易所净存入处于过去一年最高 20% 时不持有比特币。这不是交易信号：仍在验证中（H-022）。'),
  "btc_exchange_flow": ('BTC 交易所净流入（7 天）', '过去 7 天转入交易所的比特币减去转出的比特币。正值 = 净存入（常被视为即将卖出），负值 = 净提取到个人钱包。'),
  "breadth": ('市场广度：高于 200 日均线的币种', '13 个币中价格高于自身 200 日均线的比例。高 = 大部分市场处于上升趋势；低 = 大多数币在下跌。'),
  "ever_trend": ('Everscale (EVER) 相对 50 日均线', 'EVER 在 Gate.io 上高于（+）或低于（−）其 50 日均价的幅度。这就是 H-018 规则：高于 = 持仓，低于 = 空仓。'),
  "funding_carry": ("BTC 资金费率套利：扣除成本后的年化收益",
                    "持有 BTC 同时做空等量 BTC 期货每年能赚多少，价格涨跌不影响结果。当期货市场多数人做多时，空头会收到费用。"),
  "stablecoin_growth": ("稳定币供应增长（30 天）",
                        "与美元挂钩的币（USDT、USDC）供应增长有多快。新增稳定币往往是等待买入加密资产的资金；供应减少意味着资金流出。"),
  "fear_greed": ("加密货币恐惧与贪婪指数", "根据价格走势、波动率和社交媒体计算的 0–100 情绪分数。低 = 恐惧，高 = 贪婪。"),
  "btc_trend": ("BTC 相对 200 日均线", "价格高于（+）或低于（−）过去 200 天均价的幅度。高于通常意味着长期上升趋势。"),
  "btc_volatility": ("BTC 波动率（30 天，年化）", "价格波动有多大，换算为一年。40% 表示一年内典型涨跌幅约为 40%。"),
 },
 "bands": {"rule_in": '持仓', "rule_out": '空仓', "deposits": '净存入', "withdrawals": '净提取', "weak": '弱', "mixed": '分化', "strong": '强', "negative": "负值", "low": "低", "moderate": "中等", "attractive": "有吸引力", "contracting": "收缩",
           "flat": "持平", "expanding": "扩张", "extreme_fear": "极度恐惧", "fear": "恐惧", "neutral": "中性",
           "greed": "贪婪", "extreme_greed": "极度贪婪", "below": "低于", "above": "高于", "calm": "平稳",
           "normal": "正常", "stressed": "紧张", "unavailable": "无数据"},
 "notes": {
  ("h020_rule", "rule_out"): '交易所大额存入：规则处于空仓。',
  ("btc_exchange_flow", "deposits"): '大额存入在 H-020（BTC）和 H-021（ETH）中检验。',
  ("ever_trend", "above"): 'H-018 规则处于持仓状态。目前优于持有，但不显著；流动性很低。',
  ("ever_trend", "below"): 'H-018 规则处于空仓状态。',
  ("funding_carry", "attractive"): "H-011 在约 1.5%/年时被否定。如此高的套利收益值得重新评估。",
  ("funding_carry", "negative"): "空头向多头付费：看空仓位过于拥挤。",
  ("stablecoin_growth", "expanding"): "资金正在流入加密市场。H-006/H-010 未发现可靠的择时信号。",
  ("fear_greed", "extreme_greed"): "在 ≥ 75 时离场（H-008）未能跑赢持有。",
 },
 "titles": {
  "H-022": '用 2026-10-15 之后收集的数据复现 H-020',
  "H-023": 'Gram（GRAM，原 Toncoin）：自 2023 年起 SMA50 规则跑赢持有',
  "H-024": '相对强度轮动：持有最强的 3 个币（1 日和 3 日），跳过单日暴涨，仅在 BTC 高于 200 日均线时',
  "H-025": '简单动量轮动：持有 1 日和 3 日最强的 3 个币',
  "H-026": '短期反转：持有昨天跌幅最大的 3 个币',
  "H-020": '当 7 日交易所净存入处于最高 20% 时 BTC 空仓',
  "H-021": '当 7 日交易所净存入处于最高 20% 时 ETH 空仓',
  "H-012": '目标波动率（年化 30%）在 BTC、ETH、SOL 上跑赢买入持有',
  "H-013": '目标波动率（年化 30%）在 8 个独立币种上跑赢买入持有',
  "H-014": '一周动量：仅在 7 日上涨后持有（BTC、ETH、SOL）',
  "H-015": '周一效应：仅在周一（UTC）持有 BTC 跑赢买入持有',
  "H-016": '月初月末效应：仅在每月最后 2 天和最初 3 天持有 BTC',
  "H-017": '比特币过滤：仅在 BTC 高于 200 日均线时持有山寨币',
  "H-018": 'Everscale (EVER)：SMA50 规则自 2022 年起跑赢买入持有',
  "H-019": 'Everscale (EVER)：仅在 BTC 高于 200 日均线时持有',
  "H-001": "分钟级指标组合（RSI、MACD、EMA、动量）可预测 1–4 小时方向",
  "H-002": "反向的分钟级信号在扣除手续费后盈利",
  "H-003": "最佳日线趋势规则（2018–2021 年选出）在样本外跑赢买入持有（现货）",
  "H-004": "最佳日线趋势规则（期货多空）跑赢买入持有",
  "H-005": "SMA50（现货做多或空仓）在 8 个独立币种上跑赢买入持有",
  "H-006": "当 USDT+USDC 7 日增长高于其 1 年中位数时做多 BTC",
  "H-007": "当 7 日资金费率高于其 1 年第 80 百分位时 BTC 空仓",
  "H-008": "当恐惧与贪婪指数 ≥ 75 时 BTC 空仓",
  "H-009": "仅在现货 ETF 5 日净流入为正时做多 BTC",
  "H-010": "稳定币择时（H-006）在 8 个独立币种上跑赢买入持有",
  "H-011": "BTC 资金费率套利（现货做多 + 永续合约做空）值得承担风险",
 },
},
}


from crl.i18n_diag import D as _DIAG  # noqa: E402  diagnosis + coverage-scan strings

from crl.i18n_layout import L as _LAYOUT  # noqa: E402  menu, home, Market, Research, About

for _code, _strings in _DIAG.items():
    T[_code].update(_strings)
for _code, _strings in _LAYOUT.items():
    T[_code].update(_strings)


def t(lang: str, key: str, **kw):
    """Translated string (or list) with English fallback."""
    v = T.get(lang, {}).get(key)
    if v is None:
        v = T[DEFAULT][key]
    return v.format(**kw) if kw and isinstance(v, str) else v


def sub(lang: str, group: str, key, default=None):
    """Lookup inside a nested dict (bands, monitors, titles, ...) with English fallback."""
    for code in (lang, DEFAULT):
        v = T.get(code, {}).get(group, {}).get(key)
        if v is not None:
            return v
    return default

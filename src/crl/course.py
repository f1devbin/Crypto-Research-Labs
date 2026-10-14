"""Beginner course, one page per language (`course.html`). Lessons are light markdown
(paragraphs, `1.` and `-` lists, pipe tables, **bold**, [links](url), `code`) with {placeholders}
filled from the live data at every build, so the numbers in the course are always current.
`[[flow]]` on its own line becomes the "how it works" diagram.

To edit a lesson, change the text here; `pytest` checks every language has the same lessons and
placeholders.
"""
import html
import re

# --------------------------------------------------------------------------------------------- en
EN = [
("Why this project exists", """
The project answers one question: **can a simple rule earn more than buying a coin and holding it?** An example rule: "hold SOL only while its price is above its 50-day average".

The internet is full of rules like this, all with beautiful charts. Usually it is self-deception: the rule was fitted to the past, fees were forgotten, or it was tested on one lucky period. This project protects itself in three ways:

1. **Write it down first, test second.** The rule and the bar for success are written down and sealed with a fingerprint (a hash). The test cannot be adjusted after seeing the result.
2. **Test on years the rule has not seen.** A rule is chosen on 2018–2021 and judged from 2022 onwards.
3. **Compare with luck.** A statistical test answers whether such a result could appear by chance.

**Today's result:** {verdict_line} That is a result too: it saves the money that would go into trading "beautiful" rules.
"""),
("How it works", """
Everything runs by itself on GitHub's servers. Nobody needs to keep a computer switched on.

[[flow]]

- **Every day at {update_utc} UTC** fresh prices are downloaded and checked, market conditions are recalculated and this website is rebuilt.
- **Every Monday** old hypotheses are re-tested on the new data. If a verdict changes, an alert is sent.
- **Once a month** an AI model may suggest new ideas. A person checks and locks each one before it is tested.
"""),
("A tour of the home page", """
Open the [home page]({site}). The menu at the top jumps to each section; the language links are below it.

| Section | What is there | Why look |
| --- | --- | --- |
| New here? | 5 steps to read the page | once, to get the logic |
| Market regime | cards: funding, stablecoins, fear & greed, BTC trend, BTC volatility, market breadth, EVER | today's "weather" in the market |
| Coins | {n_coins} coins: price, 7 and 30 days, trend, volatility | quick overview, entry to each coin |
| Bitcoin vs its 200-day average | BTC chart since 2020 | the long-term trend of the whole market |
| Hypotheses | all {n_hyps} ideas with verdicts | what has been tested and how it ended |
| Glossary | 10 terms in plain words | when a word is unclear |
| Data freshness | last day of each data source | if numbers look old |

**How to read a market card.** The big number is today's value. The framed word under it is the zone (for example "greed" or "above"). The line at the bottom shows the last 12 months. What matters is not the number itself but **a change of zone**: that is when an alert is sent (lesson 7).
"""),
("How to read a coin page — SOL as an example", """
Every coin has its own page. Home page → "Coins" → click **SOL Solana**, or open [Solana]({site}coins/SOLUSDT.html) directly. For other coins only the ticker in the address changes: `ETHUSDT`, `BTCUSDT`, `EVERUSDT`…

A coin page is read in four steps:

1. **12-month chart.** Blue line = price, yellow dashes = 50-day average, white dots = 200-day average. Price above both averages = uptrend, below both = downtrend. The scale is logarithmic: a rise from $10 to $20 looks the same as from $100 to $200.
2. **Numbers.** Change over 7 days, 30 days and a year; distance from the averages; volatility. Volatility of 70% means a typical yearly move of about 70% up or down. Today: BTC {btc_vol}, SOL {sol_vol}, EVER {ever_vol}. Three more lines put the price in context: how far it is below its highest close (SOL: {sol_dd_peak}), what $100 invested a year ago is worth now (SOL: {sol_100}), and how closely the coin moves with Bitcoin, from −1 to 1 (SOL: {sol_corr}).
3. **What the tested rules say today.** Four rules from the hypotheses and what each would do today: "in the market", "out of the market" or a share of a position. Next to each is the verdict of its test. None has passed, so this is **an observation, not a signal**.
4. **Studies that include this coin.** For SOL the most interesting is H-014 (1-week momentum): on SOL the rule reached a Sharpe of {sol_mom_sharpe} against {sol_mom_hold} for holding, but it failed on BTC, so the verdict is "weak".

**Three questions to ask about any coin:** is the price above or below its 200-day average? Is volatility higher or lower than usual? Is Bitcoin rising or falling (the last row of the rules table)?
"""),
("How to read a hypothesis", """
Open any hypothesis from the table on the home page, for example [H-003]({site}hypotheses/H-003.html). At the top is a coloured verdict and a sentence "in plain words".

| Verdict | Meaning |
| --- | --- |
| Pass (green) | met the bar set before the test; worth an independent check |
| Weak (amber) | a bit better than holding, but it could be luck |
| Fail (red) | did not beat holding |

Then a results table, one row per coin and period. The columns are always compared in pairs, rule against "hold":

- **Sharpe**: return per unit of risk. Higher is better. Holding Bitcoin gives about 0.5.
- **CAGR**: average yearly growth.
- **Max drawdown**: the worst fall from a peak. −50% means the money halved at some point.
- **p-value**: the chance the result is luck. The smaller the better; it must be below the bar written in the hypothesis.

Under the table is a chart of how 1 dollar would have grown with the rule (solid line) and with holding (dashed). The list below lets you switch coin and period.
"""),
("Watching Everscale (EVER)", """
EVER is not on Binance, so its prices come from Gate.io. You can follow it in three places:

1. **The EVER card** in "Market regime" on the home page: how far the price is from its 50-day average. Plus means the H-018 rule is "in the market", minus means "out".
2. **The EVER page**: [Everscale]({site}coins/EVERUSDT.html), with a chart, numbers and the state of each rule.
3. **Hypotheses H-018 and H-019**, tested on EVER. Since mid-2022 the SMA50 rule returned {ever_rule_cagr} a year against {ever_hold_cagr} for holding, with a worst drawdown of {ever_rule_dd} against {ever_hold_dd}.

**Important.** The rule "beats" holding mainly because holding lost almost everything. EVER's daily trading volume is small, so the price can jump even on small trades. This is information to watch, not a recommendation.
"""),
("Alerts in Telegram", """
On this website nothing has to be configured: just open the page once a day. Alerts are for people who run **their own copy** of the project (it is free):

1. Create a bot with [@BotFather](https://t.me/BotFather) and copy its token.
2. Send your bot any message, then find your chat id (for example with [@userinfobot](https://t.me/userinfobot)).
3. [Fork the repository](https://github.com/f1devbin/Crypto-Research-Labs/fork), then in the fork: *Settings → Secrets and variables → Actions* → add `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`.
4. *Settings → Pages → Source: GitHub Actions*, then *Actions → research-agents → Run workflow*.

An alert arrives only when something changes: a market card moves to another zone, or a hypothesis gets a new verdict. On quiet days there are no messages.
"""),
("How to test your own idea", """
The easiest way does not need any code:

1. Open [a new issue "Hypothesis idea"](https://github.com/f1devbin/Crypto-Research-Labs/issues/new?template=hypothesis.yml).
2. Describe the rule in plain words: when you are in the market, when you are out, which coins.
3. Explain **why** it should work, and **what counts as success**. Write this before looking at any charts.

The idea is turned into a hypothesis file, locked and tested. The result appears on this website in all languages, with a page of its own.

If you know a little Python, read [CONTRIBUTING.md](https://github.com/f1devbin/Crypto-Research-Labs/blob/main/CONTRIBUTING.md): a hypothesis is a short YAML file.
"""),
("What the project does not do", """
- **It does not give advice.** No verdict here tells you to buy or sell. Even a "pass" would only be a reason for further checks.
- **It does not trade** and does not manage anyone's money.
- **It does not promise the future.** All results describe the past; markets change.
- **Not everything is included.** Taxes, slippage on large orders and the risk of an exchange failing are not in the numbers. Fees are.
- **Small coins are risky in a special way.** With little trading volume, the price you see may not be the price you get.

If you want to act on something here, first ask: what happens to me if the rule stops working tomorrow?
"""),
("Practice: tasks for one week", """
- [ ] Open the home page and find today's Fear & Greed zone.
- [ ] Find the coin with the highest volatility in the "Coins" table.
- [ ] Open the SOL page: is the price above or below its 200-day average?
- [ ] Open H-005 and explain in one sentence why it failed.
- [ ] Open the EVER page and compare its volatility with Bitcoin's.
- [ ] Come back in a week: did any market card change zone?
- [ ] Write down one idea of your own: the rule, why it should work, what counts as success.
"""),
]

# --------------------------------------------------------------------------------------------- ru
RU = [
("Зачем этот проект", """
Проект отвечает на один вопрос: **может ли простое правило заработать больше, чем «купил и держи»?** Пример правила: «держать SOL, только пока цена выше средней за 50 дней».

В интернете таких правил тысячи, и почти все показывают красивые графики. Обычно это самообман: правило подогнали под прошлое, забыли про комиссии или проверили на одном удачном отрезке. Проект защищается от этого тремя приёмами:

1. **Сначала записать, потом проверять.** Правило и критерий успеха записываются заранее и «запечатываются» отпечатком (хешем). Подправить тест после того, как увидел результат, нельзя.
2. **Проверять на «чужих» годах.** Правило выбирают на 2018–2021, а оценивают с 2022 года — на данных, которых оно не видело.
3. **Сравнивать с везением.** Статистический тест отвечает, мог ли такой результат получиться случайно.

**Результат на сегодня:** {verdict_line} Это тоже результат: он экономит деньги, которые ушли бы на торговлю по «красивым» правилам.
"""),
("Как это устроено", """
Всё работает само на серверах GitHub. Держать включённым свой компьютер не нужно.

[[flow]]

- **Каждый день в {update_utc} UTC** скачиваются и проверяются свежие цены, пересчитывается состояние рынка и пересобирается этот сайт.
- **Каждый понедельник** старые гипотезы перепроверяются на новых данных. Если вердикт изменился, приходит уведомление.
- **Раз в месяц** ИИ-модель может предложить новые идеи. Человек проверяет и фиксирует каждую до того, как её начнут тестировать.
"""),
("Главная страница", """
Откройте [главную страницу]({site}). Меню вверху ведёт к разделам, ниже — переключатель языка.

| Раздел | Что там | Зачем смотреть |
| --- | --- | --- |
| Новичкам | 5 шагов «как читать страницу» | один раз, чтобы понять логику |
| Рынок сейчас | карточки: фандинг, стейблкоины, страх и жадность, тренд BTC, волатильность BTC, ширина рынка, EVER | какая «погода» на рынке сегодня |
| Монеты | {n_coins} монет: цена, 7 и 30 дней, тренд, волатильность | быстрый обзор и вход на страницу монеты |
| Биткоин и 200-дневная | график BTC с 2020 года | долгосрочный тренд всего рынка |
| Гипотезы | все {n_hyps} идей с вердиктами | что уже проверено и чем закончилось |
| Словарь | 10 терминов простыми словами | когда встретилось непонятное слово |
| Свежесть данных | последний день по каждому источнику | если цифры кажутся старыми |

**Как читать карточку рынка.** Большое число — значение сегодня. Рамка под ним — зона (например, «жадность» или «выше»). Линия внизу — как показатель менялся за 12 месяцев. Важна не сама цифра, а **смена зоны**: именно тогда приходит уведомление (урок 7).
"""),
("Как смотреть монету — на примере SOL", """
У каждой монеты своя страница. Главная → раздел «Монеты» → нажать **SOL Solana**, или сразу открыть [Solana]({site}coins/SOLUSDT.html). Для других монет меняется только тикер в адресе: `ETHUSDT`, `BTCUSDT`, `EVERUSDT`…

Страница монеты читается за 4 шага:

1. **График за 12 месяцев.** Синяя линия — цена, жёлтый пунктир — средняя за 50 дней, белые точки — средняя за 200 дней. Цена выше обеих средних — восходящий тренд, ниже обеих — нисходящий. Шкала логарифмическая: рост с $10 до $20 и с $100 до $200 выглядит одинаково.
2. **Цифры.** Изменение за 7 дней, 30 дней и год; насколько цена выше или ниже средних; волатильность. Волатильность 70% значит: типичное движение за год — около 70% вверх или вниз. Сегодня: BTC {btc_vol}, SOL {sol_vol}, EVER {ever_vol}. Ещё три строки дают контекст: насколько цена ниже своего максимума (SOL: {sol_dd_peak}), сколько сейчас стоят $100, вложенные год назад (SOL: {sol_100}), и насколько монета движется вместе с биткоином, от −1 до 1 (SOL: {sol_corr}).
3. **«Что сегодня говорят проверенные правила».** Четыре правила из гипотез и что каждое сделало бы сегодня: «в рынке», «вне рынка» или доля позиции. Рядом — вердикт проверки этого правила. Ни одно не прошло, поэтому это **наблюдение, а не сигнал**.
4. **«Исследования с этой монетой».** Для SOL самое интересное — H-014 (недельный моментум): на SOL правило дало Sharpe {sol_mom_sharpe} против {sol_mom_hold} у удержания, но на BTC не сработало, поэтому вердикт «слабо».

**Три вопроса по любой монете:** цена выше или ниже 200-дневной средней? Волатильность выше или ниже обычного? Биткоин сейчас растёт или падает (последняя строка таблицы правил)?
"""),
("Как читать гипотезу", """
Откройте любую гипотезу из таблицы на главной, например [H-003]({site}hypotheses/H-003.html). Вверху — цветной вердикт и фраза «простыми словами».

| Вердикт | Что значит |
| --- | --- |
| Прошла (зелёный) | взяла планку, заданную до проверки; стоит независимо перепроверить |
| Слабо (жёлтый) | чуть лучше удержания, но это может быть везением |
| Не прошла (красный) | не обыграла удержание |

Дальше таблица результатов — строка на каждую монету и период. Столбцы всегда сравниваются парами: правило против «удержания»:

- **Sharpe** — доходность на единицу риска. Больше — лучше. У удержания биткоина около 0,5.
- **CAGR** — средний рост за год.
- **Макс. просадка** — худшее падение от пика. −50% значит, что в какой-то момент деньги уменьшились вдвое.
- **p-value** — вероятность, что результат случаен. Чем меньше, тем лучше; должно быть ниже планки, записанной в гипотезе.

Под таблицей — график, как вырос бы 1 доллар по правилу (сплошная линия) и при удержании (пунктир). Список выше графика переключает монету и период.
"""),
("Следим за Everscale (EVER)", """
EVER нет на Binance, поэтому цены берутся с Gate.io. Следить за ним можно в трёх местах:

1. **Карточка EVER** в разделе «Рынок сейчас» на главной: насколько цена выше или ниже 50-дневной средней. Плюс — правило H-018 «в рынке», минус — «вне рынка».
2. **Страница EVER**: [Everscale]({site}coins/EVERUSDT.html) — график, цифры и состояние каждого правила.
3. **Гипотезы H-018 и H-019**, проверенные на EVER. С середины 2022 года правило SMA50 дало {ever_rule_cagr} в год против {ever_hold_cagr} при удержании, худшая просадка {ever_rule_dd} против {ever_hold_dd}.

**Важно.** Правило «обыгрывает» удержание в основном потому, что удержание потеряло почти всё. Объём торгов EVER маленький, поэтому цена может скакать даже от небольших сделок. Это информация для наблюдения, а не рекомендация.
"""),
("Уведомления в Telegram", """
На этом сайте ничего настраивать не нужно: достаточно открывать страницу раз в день. Уведомления — для тех, кто запускает **свою копию** проекта (это бесплатно):

1. Создайте бота у [@BotFather](https://t.me/BotFather) и скопируйте его токен.
2. Напишите своему боту любое сообщение и узнайте свой chat id (например, через [@userinfobot](https://t.me/userinfobot)).
3. [Сделайте форк репозитория](https://github.com/f1devbin/Crypto-Research-Labs/fork), затем в форке: *Settings → Secrets and variables → Actions* → добавьте `TELEGRAM_BOT_TOKEN` и `TELEGRAM_CHAT_ID`.
4. *Settings → Pages → Source: GitHub Actions*, затем *Actions → research-agents → Run workflow*.

Уведомление приходит только когда что-то изменилось: карточка рынка перешла в другую зону или у гипотезы новый вердикт. В спокойные дни сообщений нет.
"""),
("Как проверить свою идею", """
Самый простой путь не требует программирования:

1. Откройте [новую заявку «Hypothesis idea»](https://github.com/f1devbin/Crypto-Research-Labs/issues/new?template=hypothesis.yml).
2. Опишите правило простыми словами: когда вы в рынке, когда вне, какие монеты.
3. Объясните, **почему** оно должно работать и **что считать успехом**. Напишите это до того, как смотреть графики.

Идею превратят в файл гипотезы, зафиксируют и проверят. Результат появится на этом сайте на всех языках, со своей страницей.

Если немного знаете Python, прочитайте [CONTRIBUTING.md](https://github.com/f1devbin/Crypto-Research-Labs/blob/main/CONTRIBUTING.md): гипотеза — это короткий YAML-файл.
"""),
("Чего проект не делает", """
- **Не даёт советов.** Ни один вердикт здесь не говорит покупать или продавать. Даже «прошла» — только повод для дальнейших проверок.
- **Не торгует** и не управляет чужими деньгами.
- **Не обещает будущего.** Все результаты описывают прошлое; рынки меняются.
- **Учтено не всё.** Налоги, проскальзывание на крупных заявках и риск банкротства биржи в цифры не входят. Комиссии входят.
- **Маленькие монеты рискованны по-особому.** При малом объёме торгов цена, которую вы видите, может не совпасть с ценой, по которой вы купите или продадите.

Если хотите действовать по чему-то отсюда, сначала спросите себя: что будет со мной, если правило завтра перестанет работать?
"""),
("Практика: задания на неделю", """
- [ ] Откройте главную и найдите сегодняшнюю зону индекса страха и жадности.
- [ ] Найдите в таблице «Монеты» монету с самой высокой волатильностью.
- [ ] Откройте страницу SOL: цена выше или ниже 200-дневной средней?
- [ ] Откройте H-005 и объясните одной фразой, почему она не прошла.
- [ ] Откройте страницу EVER и сравните его волатильность с биткоином.
- [ ] Вернитесь через неделю: какая-нибудь карточка рынка сменила зону?
- [ ] Запишите одну свою идею: правило, почему должно работать, что считать успехом.
"""),
]

# --------------------------------------------------------------------------------------------- es
ES = [
("Por qué existe este proyecto", """
El proyecto responde a una pregunta: **¿puede una regla sencilla ganar más que comprar una moneda y mantenerla?** Un ejemplo de regla: "mantener SOL solo mientras su precio esté por encima de su media de 50 días".

Internet está lleno de reglas así, todas con gráficos bonitos. Normalmente es autoengaño: la regla se ajustó al pasado, se olvidaron las comisiones o se probó en un único periodo afortunado. Este proyecto se protege de tres maneras:

1. **Primero escribir, después probar.** La regla y el listón de éxito se escriben antes y se sellan con una huella (un hash). La prueba no se puede ajustar después de ver el resultado.
2. **Probar en años que la regla no ha visto.** La regla se elige con 2018–2021 y se juzga desde 2022.
3. **Comparar con la suerte.** Una prueba estadística responde si ese resultado pudo salir por casualidad.

**Resultado de hoy:** {verdict_line} También es un resultado: ahorra el dinero que se iría en operar con reglas "bonitas".
"""),
("Cómo funciona", """
Todo funciona solo en los servidores de GitHub. Nadie necesita tener un ordenador encendido.

[[flow]]

- **Cada día a las {update_utc} UTC** se descargan y comprueban los precios nuevos, se recalcula el estado del mercado y se reconstruye esta web.
- **Cada lunes** las hipótesis antiguas se vuelven a probar con los datos nuevos. Si cambia un veredicto, se envía una alerta.
- **Una vez al mes** un modelo de IA puede proponer ideas nuevas. Una persona revisa y bloquea cada una antes de probarla.
"""),
("Un recorrido por la página principal", """
Abre la [página principal]({site}). El menú de arriba lleva a cada sección; los idiomas están debajo.

| Sección | Qué hay | Para qué mirarla |
| --- | --- | --- |
| ¿Eres nuevo? | 5 pasos para leer la página | una vez, para entender la lógica |
| Mercado hoy | tarjetas: funding, stablecoins, miedo y codicia, tendencia BTC, volatilidad BTC, amplitud del mercado, EVER | el "clima" del mercado hoy |
| Monedas | {n_coins} monedas: precio, 7 y 30 días, tendencia, volatilidad | vista rápida y acceso a cada moneda |
| Bitcoin y su media de 200 días | gráfico de BTC desde 2020 | la tendencia de largo plazo del mercado |
| Hipótesis | las {n_hyps} ideas con veredicto | qué se ha probado y cómo terminó |
| Glosario | 10 términos en palabras sencillas | cuando una palabra no está clara |
| Actualidad de los datos | último día de cada fuente | si los números parecen viejos |

**Cómo leer una tarjeta del mercado.** El número grande es el valor de hoy. La palabra enmarcada debajo es la zona (por ejemplo "codicia" o "por encima"). La línea inferior muestra los últimos 12 meses. Lo importante no es el número sino **el cambio de zona**: entonces llega una alerta (lección 7).
"""),
("Cómo leer la página de una moneda — SOL como ejemplo", """
Cada moneda tiene su página. Página principal → "Monedas" → pulsa **SOL Solana**, o abre [Solana]({site}coins/SOLUSDT.html) directamente. Para otras monedas solo cambia el ticker en la dirección: `ETHUSDT`, `BTCUSDT`, `EVERUSDT`…

La página se lee en cuatro pasos:

1. **Gráfico de 12 meses.** Línea azul = precio, rayas amarillas = media de 50 días, puntos blancos = media de 200 días. Precio sobre ambas medias = tendencia alcista; bajo ambas = bajista. La escala es logarítmica: subir de $10 a $20 se ve igual que de $100 a $200.
2. **Cifras.** Cambio en 7 días, 30 días y un año; distancia a las medias; volatilidad. Una volatilidad del 70% significa un movimiento anual típico de un 70% arriba o abajo. Hoy: BTC {btc_vol}, SOL {sol_vol}, EVER {ever_vol}. Tres líneas más dan contexto: cuánto está por debajo de su cierre más alto (SOL: {sol_dd_peak}), cuánto valen hoy $100 invertidos hace un año (SOL: {sol_100}) y cuánto se mueve junto con Bitcoin, de −1 a 1 (SOL: {sol_corr}).
3. **Qué dicen hoy las reglas probadas.** Cuatro reglas de las hipótesis y qué haría cada una hoy: "dentro del mercado", "fuera del mercado" o una parte de la posición. Al lado, el veredicto de su prueba. Ninguna ha superado la prueba, así que es **una observación, no una señal**.
4. **Estudios que incluyen esta moneda.** Para SOL lo más interesante es H-014 (momentum semanal): en SOL la regla logró un Sharpe de {sol_mom_sharpe} frente a {sol_mom_hold} al mantener, pero falló en BTC, por eso el veredicto es "débil".

**Tres preguntas para cualquier moneda:** ¿el precio está por encima o por debajo de su media de 200 días? ¿La volatilidad es mayor o menor de lo habitual? ¿Bitcoin sube o baja (última fila de la tabla de reglas)?
"""),
("Cómo leer una hipótesis", """
Abre cualquier hipótesis de la tabla principal, por ejemplo [H-003]({site}hypotheses/H-003.html). Arriba hay un veredicto de color y una frase "en pocas palabras".

| Veredicto | Significado |
| --- | --- |
| Supera (verde) | alcanzó el listón fijado antes de la prueba; merece una revisión independiente |
| Débil (ámbar) | algo mejor que mantener, pero puede ser suerte |
| No supera (rojo) | no ganó a mantener |

Después viene una tabla de resultados, una fila por moneda y periodo. Las columnas se comparan siempre en parejas, regla frente a "mantener":

- **Sharpe**: rentabilidad por unidad de riesgo. Más es mejor. Mantener Bitcoin da alrededor de 0,5.
- **CAGR**: crecimiento anual medio.
- **Caída máxima**: la peor caída desde un pico. −50% significa que el dinero se redujo a la mitad en algún momento.
- **p-valor**: la probabilidad de que el resultado sea suerte. Cuanto más pequeño, mejor; debe estar por debajo del listón escrito en la hipótesis.

Bajo la tabla hay un gráfico de cómo habría crecido 1 dólar con la regla (línea continua) y manteniendo (discontinua). La lista permite cambiar de moneda y periodo.
"""),
("Seguir a Everscale (EVER)", """
EVER no está en Binance, así que sus precios vienen de Gate.io. Puedes seguirlo en tres lugares:

1. **La tarjeta de EVER** en "Mercado hoy": cuánto se aleja el precio de su media de 50 días. Positivo = la regla H-018 está "dentro", negativo = "fuera".
2. **La página de EVER**: [Everscale]({site}coins/EVERUSDT.html), con gráfico, cifras y el estado de cada regla.
3. **Las hipótesis H-018 y H-019**, probadas en EVER. Desde mediados de 2022 la regla SMA50 rindió {ever_rule_cagr} al año frente a {ever_hold_cagr} manteniendo, con una caída máxima de {ever_rule_dd} frente a {ever_hold_dd}.

**Importante.** La regla "gana" a mantener sobre todo porque mantener lo perdió casi todo. El volumen diario de EVER es pequeño y el precio puede saltar incluso con operaciones pequeñas. Es información para observar, no una recomendación.
"""),
("Alertas en Telegram", """
En esta web no hay que configurar nada: basta con abrir la página una vez al día. Las alertas son para quien ejecuta **su propia copia** del proyecto (es gratis):

1. Crea un bot con [@BotFather](https://t.me/BotFather) y copia su token.
2. Envía cualquier mensaje a tu bot y averigua tu chat id (por ejemplo con [@userinfobot](https://t.me/userinfobot)).
3. [Haz un fork del repositorio](https://github.com/f1devbin/Crypto-Research-Labs/fork) y en el fork: *Settings → Secrets and variables → Actions* → añade `TELEGRAM_BOT_TOKEN` y `TELEGRAM_CHAT_ID`.
4. *Settings → Pages → Source: GitHub Actions*, y luego *Actions → research-agents → Run workflow*.

La alerta llega solo cuando algo cambia: una tarjeta del mercado pasa a otra zona o una hipótesis tiene un veredicto nuevo. En los días tranquilos no hay mensajes.
"""),
("Cómo probar tu propia idea", """
La forma más sencilla no necesita programar:

1. Abre [una nueva issue "Hypothesis idea"](https://github.com/f1devbin/Crypto-Research-Labs/issues/new?template=hypothesis.yml).
2. Describe la regla con palabras sencillas: cuándo estás dentro del mercado, cuándo fuera, qué monedas.
3. Explica **por qué** debería funcionar y **qué cuenta como éxito**. Escríbelo antes de mirar ningún gráfico.

La idea se convierte en un archivo de hipótesis, se bloquea y se prueba. El resultado aparece en esta web en todos los idiomas, con su propia página.

Si sabes algo de Python, lee [CONTRIBUTING.md](https://github.com/f1devbin/Crypto-Research-Labs/blob/main/CONTRIBUTING.md): una hipótesis es un archivo YAML corto.
"""),
("Lo que el proyecto no hace", """
- **No da consejos.** Ningún veredicto dice comprar o vender. Incluso un "supera" sería solo motivo para más comprobaciones.
- **No opera** ni gestiona el dinero de nadie.
- **No promete el futuro.** Todos los resultados describen el pasado; los mercados cambian.
- **No todo está incluido.** Impuestos, deslizamiento en órdenes grandes y el riesgo de quiebra de un exchange no están en las cifras. Las comisiones sí.
- **Las monedas pequeñas tienen un riesgo especial.** Con poco volumen, el precio que ves puede no ser el precio al que compras o vendes.

Si quieres actuar según algo de aquí, pregúntate primero: ¿qué me pasa si la regla deja de funcionar mañana?
"""),
("Práctica: tareas para una semana", """
- [ ] Abre la página principal y encuentra la zona de hoy del índice de miedo y codicia.
- [ ] Encuentra en la tabla "Monedas" la moneda con mayor volatilidad.
- [ ] Abre la página de SOL: ¿el precio está por encima o por debajo de su media de 200 días?
- [ ] Abre H-005 y explica en una frase por qué no superó la prueba.
- [ ] Abre la página de EVER y compara su volatilidad con la de Bitcoin.
- [ ] Vuelve dentro de una semana: ¿alguna tarjeta del mercado cambió de zona?
- [ ] Escribe una idea propia: la regla, por qué debería funcionar, qué cuenta como éxito.
"""),
]

# --------------------------------------------------------------------------------------------- pt
PT = [
("Por que este projeto existe", """
O projeto responde a uma pergunta: **uma regra simples consegue ganhar mais do que comprar uma moeda e segurar?** Um exemplo de regra: "segurar SOL só enquanto o preço estiver acima da média de 50 dias".

A internet está cheia de regras assim, todas com gráficos bonitos. Normalmente é autoengano: a regra foi ajustada ao passado, as taxas foram esquecidas ou o teste foi feito num único período de sorte. Este projeto se protege de três formas:

1. **Primeiro escrever, depois testar.** A regra e a meta de sucesso são escritas antes e seladas com uma impressão digital (um hash). O teste não pode ser ajustado depois de ver o resultado.
2. **Testar em anos que a regra não viu.** A regra é escolhida em 2018–2021 e avaliada a partir de 2022.
3. **Comparar com a sorte.** Um teste estatístico responde se esse resultado poderia surgir por acaso.

**Resultado de hoje:** {verdict_line} Isso também é um resultado: economiza o dinheiro que iria para operar com regras "bonitas".
"""),
("Como funciona", """
Tudo roda sozinho nos servidores do GitHub. Ninguém precisa deixar um computador ligado.

[[flow]]

- **Todo dia às {update_utc} UTC** os preços novos são baixados e verificados, o estado do mercado é recalculado e este site é reconstruído.
- **Toda segunda-feira** as hipóteses antigas são testadas de novo com os dados novos. Se um veredicto muda, um alerta é enviado.
- **Uma vez por mês** um modelo de IA pode sugerir ideias novas. Uma pessoa revisa e trava cada uma antes do teste.
"""),
("Um passeio pela página principal", """
Abra a [página principal]({site}). O menu no topo leva a cada seção; os idiomas ficam logo abaixo.

| Seção | O que tem | Por que olhar |
| --- | --- | --- |
| Novo aqui? | 5 passos para ler a página | uma vez, para entender a lógica |
| Mercado hoje | cartões: funding, stablecoins, medo e ganância, tendência do BTC, volatilidade do BTC, amplitude do mercado, EVER | o "clima" do mercado hoje |
| Moedas | {n_coins} moedas: preço, 7 e 30 dias, tendência, volatilidade | visão rápida e acesso a cada moeda |
| Bitcoin e sua média de 200 dias | gráfico do BTC desde 2020 | a tendência de longo prazo do mercado |
| Hipóteses | todas as {n_hyps} ideias com veredicto | o que já foi testado e como terminou |
| Glossário | 10 termos em palavras simples | quando uma palavra não está clara |
| Atualização dos dados | último dia de cada fonte | se os números parecem antigos |

**Como ler um cartão do mercado.** O número grande é o valor de hoje. A palavra emoldurada abaixo é a faixa (por exemplo "ganância" ou "acima"). A linha de baixo mostra os últimos 12 meses. O que importa não é o número, e sim **a mudança de faixa**: é quando chega um alerta (lição 7).
"""),
("Como ler a página de uma moeda — SOL como exemplo", """
Cada moeda tem sua página. Página principal → "Moedas" → clique em **SOL Solana**, ou abra [Solana]({site}coins/SOLUSDT.html) direto. Para outras moedas só muda o ticker no endereço: `ETHUSDT`, `BTCUSDT`, `EVERUSDT`…

A página é lida em quatro passos:

1. **Gráfico de 12 meses.** Linha azul = preço, tracejado amarelo = média de 50 dias, pontos brancos = média de 200 dias. Preço acima das duas médias = tendência de alta; abaixo das duas = de baixa. A escala é logarítmica: subir de $10 para $20 parece igual a subir de $100 para $200.
2. **Números.** Variação em 7 dias, 30 dias e um ano; distância das médias; volatilidade. Volatilidade de 70% significa um movimento anual típico de cerca de 70% para cima ou para baixo. Hoje: BTC {btc_vol}, SOL {sol_vol}, EVER {ever_vol}. Mais três linhas dão contexto: quanto o preço está abaixo do maior fechamento (SOL: {sol_dd_peak}), quanto valem hoje $100 investidos há um ano (SOL: {sol_100}) e quanto a moeda se move junto com o Bitcoin, de −1 a 1 (SOL: {sol_corr}).
3. **O que as regras testadas dizem hoje.** Quatro regras das hipóteses e o que cada uma faria hoje: "no mercado", "fora do mercado" ou uma fração da posição. Ao lado, o veredicto do teste. Nenhuma passou, então isto é **uma observação, não um sinal**.
4. **Estudos com esta moeda.** Para SOL o mais interessante é a H-014 (momentum semanal): em SOL a regra chegou a Sharpe {sol_mom_sharpe} contra {sol_mom_hold} de segurar, mas falhou no BTC, por isso o veredicto é "fraca".

**Três perguntas para qualquer moeda:** o preço está acima ou abaixo da média de 200 dias? A volatilidade está maior ou menor que o normal? O Bitcoin está subindo ou caindo (última linha da tabela de regras)?
"""),
("Como ler uma hipótese", """
Abra qualquer hipótese da tabela principal, por exemplo a [H-003]({site}hypotheses/H-003.html). No topo há um veredicto colorido e uma frase "em poucas palavras".

| Veredicto | Significado |
| --- | --- |
| Passou (verde) | atingiu a meta definida antes do teste; merece verificação independente |
| Fraca (âmbar) | um pouco melhor que segurar, mas pode ser sorte |
| Reprovada (vermelho) | não venceu segurar |

Depois vem a tabela de resultados, uma linha por moeda e período. As colunas são sempre comparadas em pares, regra contra "segurar":

- **Sharpe**: retorno por unidade de risco. Maior é melhor. Segurar Bitcoin dá cerca de 0,5.
- **CAGR**: crescimento anual médio.
- **Drawdown máximo**: a pior queda a partir de um pico. −50% significa que o dinheiro caiu pela metade em algum momento.
- **p-valor**: a chance de o resultado ser sorte. Quanto menor, melhor; precisa ficar abaixo da meta escrita na hipótese.

Abaixo da tabela há um gráfico de como 1 dólar teria crescido com a regra (linha cheia) e segurando (tracejada). A lista troca a moeda e o período.
"""),
("Acompanhando a Everscale (EVER)", """
A EVER não está na Binance, então os preços vêm da Gate.io. Dá para acompanhar em três lugares:

1. **O cartão da EVER** em "Mercado hoje": quanto o preço está longe da média de 50 dias. Positivo = a regra H-018 está "no mercado", negativo = "fora".
2. **A página da EVER**: [Everscale]({site}coins/EVERUSDT.html), com gráfico, números e o estado de cada regra.
3. **As hipóteses H-018 e H-019**, testadas na EVER. Desde meados de 2022 a regra SMA50 rendeu {ever_rule_cagr} ao ano contra {ever_hold_cagr} segurando, com pior queda de {ever_rule_dd} contra {ever_hold_dd}.

**Importante.** A regra "vence" segurar principalmente porque segurar perdeu quase tudo. O volume diário da EVER é pequeno, e o preço pode saltar mesmo com negócios pequenos. É informação para acompanhar, não uma recomendação.
"""),
("Alertas no Telegram", """
Neste site não é preciso configurar nada: basta abrir a página uma vez por dia. Os alertas são para quem roda **a própria cópia** do projeto (é grátis):

1. Crie um bot com o [@BotFather](https://t.me/BotFather) e copie o token.
2. Mande qualquer mensagem para o seu bot e descubra o seu chat id (por exemplo com o [@userinfobot](https://t.me/userinfobot)).
3. [Faça um fork do repositório](https://github.com/f1devbin/Crypto-Research-Labs/fork) e no fork: *Settings → Secrets and variables → Actions* → adicione `TELEGRAM_BOT_TOKEN` e `TELEGRAM_CHAT_ID`.
4. *Settings → Pages → Source: GitHub Actions*, depois *Actions → research-agents → Run workflow*.

O alerta chega só quando algo muda: um cartão do mercado muda de faixa ou uma hipótese ganha um veredicto novo. Em dias calmos não há mensagens.
"""),
("Como testar sua própria ideia", """
O caminho mais simples não exige programação:

1. Abra [uma nova issue "Hypothesis idea"](https://github.com/f1devbin/Crypto-Research-Labs/issues/new?template=hypothesis.yml).
2. Descreva a regra com palavras simples: quando você está no mercado, quando está fora, quais moedas.
3. Explique **por que** ela deveria funcionar e **o que conta como sucesso**. Escreva isso antes de olhar qualquer gráfico.

A ideia vira um arquivo de hipótese, é travada e testada. O resultado aparece neste site em todos os idiomas, com página própria.

Se você sabe um pouco de Python, leia o [CONTRIBUTING.md](https://github.com/f1devbin/Crypto-Research-Labs/blob/main/CONTRIBUTING.md): uma hipótese é um arquivo YAML curto.
"""),
("O que o projeto não faz", """
- **Não dá conselhos.** Nenhum veredicto diz para comprar ou vender. Mesmo um "passou" seria só motivo para mais verificações.
- **Não opera** nem administra dinheiro de ninguém.
- **Não promete o futuro.** Todos os resultados descrevem o passado; os mercados mudam.
- **Nem tudo está incluído.** Impostos, slippage em ordens grandes e o risco de falência de uma corretora não estão nos números. As taxas estão.
- **Moedas pequenas têm um risco especial.** Com pouco volume, o preço que você vê pode não ser o preço em que você compra ou vende.

Se quiser agir com base em algo daqui, pergunte-se antes: o que acontece comigo se a regra parar de funcionar amanhã?
"""),
("Prática: tarefas para uma semana", """
- [ ] Abra a página principal e encontre a faixa de hoje do índice de medo e ganância.
- [ ] Encontre na tabela "Moedas" a moeda com maior volatilidade.
- [ ] Abra a página da SOL: o preço está acima ou abaixo da média de 200 dias?
- [ ] Abra a H-005 e explique em uma frase por que ela foi reprovada.
- [ ] Abra a página da EVER e compare a volatilidade dela com a do Bitcoin.
- [ ] Volte daqui a uma semana: algum cartão do mercado mudou de faixa?
- [ ] Escreva uma ideia sua: a regra, por que deveria funcionar, o que conta como sucesso.
"""),
]

# --------------------------------------------------------------------------------------------- tr
TR = [
("Bu proje neden var", """
Proje tek bir soruyu yanıtlar: **basit bir kural, bir coini alıp tutmaktan daha fazla kazandırabilir mi?** Örnek kural: "SOL'u yalnızca fiyatı 50 günlük ortalamanın üzerindeyken tut".

İnternet bu tür kurallarla dolu ve hepsinin grafikleri güzel. Genellikle bu bir kendini kandırmadır: kural geçmişe uydurulmuş, komisyonlar unutulmuş ya da tek bir şanslı dönemde test edilmiştir. Bu proje kendini üç yolla korur:

1. **Önce yaz, sonra test et.** Kural ve başarı çıtası önceden yazılır ve bir parmak iziyle (hash) mühürlenir. Sonucu gördükten sonra test değiştirilemez.
2. **Kuralın görmediği yıllarda test et.** Kural 2018–2021 verisiyle seçilir, 2022'den itibaren değerlendirilir.
3. **Şansla karşılaştır.** İstatistiksel bir test, böyle bir sonucun tesadüfen çıkıp çıkamayacağını yanıtlar.

**Bugünkü sonuç:** {verdict_line} Bu da bir sonuçtur: "güzel" kurallarla işlem yaparak kaybedilecek parayı korur.
"""),
("Nasıl çalışır", """
Her şey GitHub sunucularında kendiliğinden çalışır. Kimsenin bilgisayarını açık tutması gerekmez.

[[flow]]

- **Her gün {update_utc} UTC'de** yeni fiyatlar indirilir ve kontrol edilir, piyasa durumu yeniden hesaplanır ve bu site yeniden oluşturulur.
- **Her pazartesi** eski hipotezler yeni verilerle yeniden test edilir. Bir karar değişirse uyarı gönderilir.
- **Ayda bir** bir yapay zekâ modeli yeni fikirler önerebilir. Bir insan her birini test edilmeden önce kontrol eder ve kilitler.
"""),
("Ana sayfa turu", """
[Ana sayfayı]({site}) açın. Üstteki menü her bölüme götürür; dil bağlantıları hemen altındadır.

| Bölüm | Ne var | Neden bakılır |
| --- | --- | --- |
| Yeni misiniz? | sayfayı okumak için 5 adım | bir kez, mantığı anlamak için |
| Piyasa bugün | kartlar: funding, stablecoinler, korku ve açgözlülük, BTC trendi, BTC volatilitesi, piyasa genişliği, EVER | bugün piyasanın "havası" |
| Coinler | {n_coins} coin: fiyat, 7 ve 30 gün, trend, volatilite | hızlı bakış ve her coinin sayfası |
| Bitcoin ve 200 günlük ortalaması | 2020'den beri BTC grafiği | tüm piyasanın uzun vadeli trendi |
| Hipotezler | {n_hyps} fikrin tümü ve kararları | neler test edildi, nasıl sonuçlandı |
| Sözlük | basit dille 10 terim | bir kelime anlaşılmadığında |
| Veri güncelliği | her kaynağın son günü | rakamlar eski görünürse |

**Piyasa kartı nasıl okunur.** Büyük sayı bugünkü değerdir. Altındaki çerçeveli kelime aralıktır (örneğin "açgözlülük" ya da "üstünde"). Alttaki çizgi son 12 ayı gösterir. Önemli olan sayının kendisi değil, **aralığın değişmesidir**: uyarı o zaman gelir (ders 7).
"""),
("Bir coin sayfası nasıl okunur — SOL örneği", """
Her coinin kendi sayfası var. Ana sayfa → "Coinler" → **SOL Solana**'ya tıklayın ya da doğrudan [Solana]({site}coins/SOLUSDT.html) sayfasını açın. Diğer coinler için adreste yalnızca ticker değişir: `ETHUSDT`, `BTCUSDT`, `EVERUSDT`…

Sayfa dört adımda okunur:

1. **12 aylık grafik.** Mavi çizgi = fiyat, sarı kesikli = 50 günlük ortalama, beyaz noktalar = 200 günlük ortalama. Fiyat iki ortalamanın da üstünde = yükseliş trendi; ikisinin de altında = düşüş. Ölçek logaritmiktir: 10$'dan 20$'a çıkış, 100$'dan 200$'a çıkışla aynı görünür.
2. **Rakamlar.** 7 gün, 30 gün ve bir yıldaki değişim; ortalamalara uzaklık; volatilite. %70 volatilite, yıllık tipik hareketin yaklaşık %70 yukarı ya da aşağı olduğu anlamına gelir. Bugün: BTC {btc_vol}, SOL {sol_vol}, EVER {ever_vol}. Üç satır daha bağlam verir: fiyatın en yüksek kapanışın ne kadar altında olduğu (SOL: {sol_dd_peak}), 1 yıl önce yatırılan 100$'ın şimdi ne ettiği (SOL: {sol_100}) ve coinin Bitcoin ile ne kadar birlikte hareket ettiği, −1 ile 1 arası (SOL: {sol_corr}).
3. **Test edilen kurallar bugün ne diyor.** Hipotezlerden dört kural ve her birinin bugün ne yapacağı: "piyasada", "piyasa dışında" ya da pozisyonun bir payı. Yanında testinin kararı var. Hiçbiri testi geçmedi, bu yüzden bu **bir gözlemdir, sinyal değil**.
4. **Bu coini içeren çalışmalar.** SOL için en ilginci H-014 (haftalık momentum): kural SOL'da {sol_mom_sharpe} Sharpe'a ulaştı, tutmanınki {sol_mom_hold}; ama BTC'de işe yaramadı, bu yüzden karar "zayıf".

**Her coin için üç soru:** fiyat 200 günlük ortalamanın üstünde mi altında mı? Volatilite normalden yüksek mi düşük mü? Bitcoin yükseliyor mu düşüyor mu (kural tablosunun son satırı)?
"""),
("Bir hipotez nasıl okunur", """
Ana sayfadaki tablodan herhangi bir hipotezi açın, örneğin [H-003]({site}hypotheses/H-003.html). Üstte renkli bir karar ve "kısaca" cümlesi var.

| Karar | Anlamı |
| --- | --- |
| Geçti (yeşil) | testten önce belirlenen çıtayı geçti; bağımsız kontrolü hak ediyor |
| Zayıf (kehribar) | tutmaktan biraz iyi ama şans olabilir |
| Kaldı (kırmızı) | tutmayı geçemedi |

Ardından sonuç tablosu gelir: her coin ve dönem için bir satır. Sütunlar hep çift olarak karşılaştırılır, kural ve "tut":

- **Sharpe**: risk birimi başına getiri. Yüksek daha iyi. Bitcoin'i tutmak yaklaşık 0,5 verir.
- **CAGR**: ortalama yıllık büyüme.
- **Maks. düşüş**: zirveden en kötü düşüş. −%50, paranın bir noktada yarıya indiği anlamına gelir.
- **p-değeri**: sonucun şans olma olasılığı. Ne kadar küçükse o kadar iyi; hipotezde yazan çıtanın altında olmalı.

Tablonun altında 1 doların kuralla (düz çizgi) ve tutarak (kesikli) nasıl büyüyeceğini gösteren bir grafik var. Liste coin ve dönemi değiştirir.
"""),
("Everscale (EVER) takibi", """
EVER Binance'te yok, bu yüzden fiyatlar Gate.io'dan geliyor. Üç yerden takip edebilirsiniz:

1. Ana sayfada "Piyasa bugün" bölümündeki **EVER kartı**: fiyatın 50 günlük ortalamadan ne kadar uzak olduğu. Artı = H-018 kuralı "piyasada", eksi = "dışarıda".
2. **EVER sayfası**: [Everscale]({site}coins/EVERUSDT.html) — grafik, rakamlar ve her kuralın durumu.
3. EVER üzerinde test edilen **H-018 ve H-019 hipotezleri**. 2022 ortasından beri SMA50 kuralı yılda {ever_rule_cagr} getirdi, tutmak ise {ever_hold_cagr}; en kötü düşüş {ever_rule_dd}, tutmada {ever_hold_dd}.

**Önemli.** Kural tutmayı esas olarak tutmak neredeyse her şeyi kaybettiği için "geçiyor". EVER'in günlük işlem hacmi küçük; fiyat küçük işlemlerle bile sıçrayabilir. Bu izlemek için bir bilgidir, tavsiye değildir.
"""),
("Telegram uyarıları", """
Bu sitede hiçbir şeyi ayarlamanız gerekmez: sayfayı günde bir kez açmanız yeterli. Uyarılar, projenin **kendi kopyasını** çalıştıranlar içindir (ücretsiz):

1. [@BotFather](https://t.me/BotFather) ile bir bot oluşturun ve tokenını kopyalayın.
2. Botunuza herhangi bir mesaj gönderin ve chat id'nizi öğrenin (örneğin [@userinfobot](https://t.me/userinfobot) ile).
3. [Depoyu fork edin](https://github.com/f1devbin/Crypto-Research-Labs/fork), ardından fork'ta: *Settings → Secrets and variables → Actions* → `TELEGRAM_BOT_TOKEN` ve `TELEGRAM_CHAT_ID` ekleyin.
4. *Settings → Pages → Source: GitHub Actions*, sonra *Actions → research-agents → Run workflow*.

Uyarı yalnızca bir şey değiştiğinde gelir: bir piyasa kartı başka aralığa geçtiğinde ya da bir hipotez yeni karar aldığında. Sakin günlerde mesaj gelmez.
"""),
("Kendi fikrinizi nasıl test edersiniz", """
En kolay yol kod gerektirmez:

1. [Yeni bir "Hypothesis idea" issue'su](https://github.com/f1devbin/Crypto-Research-Labs/issues/new?template=hypothesis.yml) açın.
2. Kuralı basit kelimelerle anlatın: ne zaman piyasadasınız, ne zaman dışarıdasınız, hangi coinler.
3. **Neden** işe yaraması gerektiğini ve **neyin başarı sayılacağını** açıklayın. Bunu herhangi bir grafiğe bakmadan önce yazın.

Fikir bir hipotez dosyasına dönüştürülür, kilitlenir ve test edilir. Sonuç bu sitede tüm dillerde, kendi sayfasıyla görünür.

Biraz Python biliyorsanız [CONTRIBUTING.md](https://github.com/f1devbin/Crypto-Research-Labs/blob/main/CONTRIBUTING.md) dosyasını okuyun: bir hipotez kısa bir YAML dosyasıdır.
"""),
("Projenin yapmadıkları", """
- **Tavsiye vermez.** Buradaki hiçbir karar al ya da sat demez. "Geçti" bile yalnızca daha fazla kontrol için bir nedendir.
- **İşlem yapmaz** ve kimsenin parasını yönetmez.
- **Geleceği vaat etmez.** Tüm sonuçlar geçmişi anlatır; piyasalar değişir.
- **Her şey dahil değildir.** Vergiler, büyük emirlerde kayma ve bir borsanın batma riski rakamlarda yok. Komisyonlar var.
- **Küçük coinlerin özel bir riski vardır.** Hacim düşükken gördüğünüz fiyat, alıp satacağınız fiyat olmayabilir.

Buradaki bir şeye göre hareket etmek isterseniz önce kendinize sorun: kural yarın çalışmayı bırakırsa bana ne olur?
"""),
("Pratik: bir haftalık görevler", """
- [ ] Ana sayfayı açın ve korku ve açgözlülük endeksinin bugünkü aralığını bulun.
- [ ] "Coinler" tablosunda volatilitesi en yüksek coini bulun.
- [ ] SOL sayfasını açın: fiyat 200 günlük ortalamanın üstünde mi altında mı?
- [ ] H-005'i açın ve neden kaldığını bir cümleyle açıklayın.
- [ ] EVER sayfasını açın ve volatilitesini Bitcoin'inkiyle karşılaştırın.
- [ ] Bir hafta sonra geri gelin: herhangi bir piyasa kartı aralık değiştirdi mi?
- [ ] Kendi fikrinizi yazın: kural, neden işe yaramalı, ne başarı sayılır.
"""),
]

# --------------------------------------------------------------------------------------------- vi
VI = [
("Vì sao có dự án này", """
Dự án trả lời một câu hỏi: **một quy tắc đơn giản có kiếm được nhiều hơn việc mua một đồng coin rồi giữ không?** Ví dụ quy tắc: "chỉ giữ SOL khi giá trên đường trung bình 50 ngày".

Trên mạng có vô số quy tắc như vậy, kèm biểu đồ đẹp. Thường đó là tự lừa mình: quy tắc được khớp với quá khứ, quên phí, hoặc chỉ thử trên một giai đoạn may mắn. Dự án tự bảo vệ bằng ba cách:

1. **Viết trước, kiểm tra sau.** Quy tắc và mức thành công được viết ra trước và "niêm phong" bằng dấu vân tay (mã băm). Không thể chỉnh bài kiểm tra sau khi thấy kết quả.
2. **Kiểm tra trên những năm quy tắc chưa thấy.** Quy tắc được chọn trên 2018–2021 và đánh giá từ 2022.
3. **So với may mắn.** Một kiểm định thống kê cho biết kết quả đó có thể xuất hiện ngẫu nhiên hay không.

**Kết quả hôm nay:** {verdict_line} Đó cũng là một kết quả: nó giữ lại số tiền lẽ ra mất vào việc giao dịch theo các quy tắc "đẹp".
"""),
("Cách hoạt động", """
Mọi thứ tự chạy trên máy chủ của GitHub. Không ai cần để máy tính bật.

[[flow]]

- **Mỗi ngày lúc {update_utc} UTC** giá mới được tải về và kiểm tra, trạng thái thị trường được tính lại và trang web này được dựng lại.
- **Mỗi thứ Hai** các giả thuyết cũ được kiểm tra lại với dữ liệu mới. Nếu kết luận thay đổi, cảnh báo được gửi đi.
- **Mỗi tháng một lần** một mô hình AI có thể đề xuất ý tưởng mới. Con người xem xét và khóa từng ý tưởng trước khi kiểm tra.
"""),
("Tham quan trang chủ", """
Mở [trang chủ]({site}). Menu phía trên dẫn tới từng mục; liên kết ngôn ngữ nằm ngay bên dưới.

| Mục | Có gì | Xem để làm gì |
| --- | --- | --- |
| Người mới? | 5 bước để đọc trang | một lần, để hiểu logic |
| Thị trường hôm nay | các thẻ: funding, stablecoin, sợ hãi & tham lam, xu hướng BTC, biến động BTC, độ rộng thị trường, EVER | "thời tiết" thị trường hôm nay |
| Đồng coin | {n_coins} coin: giá, 7 và 30 ngày, xu hướng, biến động | xem nhanh và vào trang từng coin |
| Bitcoin và trung bình 200 ngày | biểu đồ BTC từ 2020 | xu hướng dài hạn của cả thị trường |
| Giả thuyết | toàn bộ {n_hyps} ý tưởng kèm kết luận | đã kiểm tra gì và kết quả ra sao |
| Thuật ngữ | 10 thuật ngữ bằng lời đơn giản | khi gặp từ khó hiểu |
| Độ mới của dữ liệu | ngày cuối của từng nguồn | nếu số liệu có vẻ cũ |

**Cách đọc thẻ thị trường.** Số lớn là giá trị hôm nay. Chữ đóng khung bên dưới là vùng (ví dụ "tham lam" hoặc "trên"). Đường ở dưới cùng là 12 tháng gần nhất. Điều quan trọng không phải con số mà là **việc đổi vùng**: lúc đó cảnh báo được gửi (bài 7).
"""),
("Cách đọc trang một đồng coin — ví dụ SOL", """
Mỗi đồng coin có trang riêng. Trang chủ → "Đồng coin" → nhấn **SOL Solana**, hoặc mở thẳng [Solana]({site}coins/SOLUSDT.html). Với coin khác chỉ đổi mã trong địa chỉ: `ETHUSDT`, `BTCUSDT`, `EVERUSDT`…

Trang được đọc trong bốn bước:

1. **Biểu đồ 12 tháng.** Đường xanh = giá, nét đứt vàng = trung bình 50 ngày, chấm trắng = trung bình 200 ngày. Giá trên cả hai đường trung bình = xu hướng tăng; dưới cả hai = giảm. Thang logarit: tăng từ $10 lên $20 trông giống từ $100 lên $200.
2. **Số liệu.** Thay đổi 7 ngày, 30 ngày và một năm; khoảng cách tới các đường trung bình; độ biến động. Biến động 70% nghĩa là dao động năm điển hình khoảng 70% lên hoặc xuống. Hôm nay: BTC {btc_vol}, SOL {sol_vol}, EVER {ever_vol}. Ba dòng nữa cho thêm bối cảnh: giá thấp hơn mức đóng cửa cao nhất bao nhiêu (SOL: {sol_dd_peak}), $100 đầu tư một năm trước giờ là bao nhiêu (SOL: {sol_100}), và coin biến động cùng Bitcoin đến mức nào, từ −1 đến 1 (SOL: {sol_corr}).
3. **Các quy tắc đã kiểm tra nói gì hôm nay.** Bốn quy tắc từ các giả thuyết và mỗi quy tắc sẽ làm gì hôm nay: "trong thị trường", "đứng ngoài" hoặc một phần vị thế. Bên cạnh là kết luận kiểm tra. Chưa quy tắc nào đạt, nên đây là **quan sát, không phải tín hiệu**.
4. **Nghiên cứu có đồng coin này.** Với SOL thú vị nhất là H-014 (động lượng 1 tuần): trên SOL quy tắc đạt Sharpe {sol_mom_sharpe} so với {sol_mom_hold} khi giữ, nhưng thất bại trên BTC, nên kết luận là "yếu".

**Ba câu hỏi cho mọi đồng coin:** giá trên hay dưới trung bình 200 ngày? Biến động cao hay thấp hơn thường lệ? Bitcoin đang tăng hay giảm (dòng cuối bảng quy tắc)?
"""),
("Cách đọc một giả thuyết", """
Mở bất kỳ giả thuyết nào trong bảng ở trang chủ, ví dụ [H-003]({site}hypotheses/H-003.html). Phía trên có kết luận màu và một câu "nói đơn giản".

| Kết luận | Ý nghĩa |
| --- | --- |
| Đạt (xanh lá) | đạt mức đặt ra trước khi kiểm tra; đáng được kiểm tra độc lập |
| Yếu (vàng) | tốt hơn giữ một chút nhưng có thể do may mắn |
| Không đạt (đỏ) | không thắng việc giữ |

Tiếp theo là bảng kết quả, mỗi dòng một coin và giai đoạn. Các cột luôn so theo cặp, quy tắc với "giữ":

- **Sharpe**: lợi nhuận trên mỗi đơn vị rủi ro. Càng cao càng tốt. Giữ Bitcoin cho khoảng 0,5.
- **CAGR**: tăng trưởng trung bình mỗi năm.
- **Sụt giảm tối đa**: mức giảm tệ nhất từ đỉnh. −50% nghĩa là có lúc tiền chỉ còn một nửa.
- **p-value**: khả năng kết quả do may mắn. Càng nhỏ càng tốt; phải thấp hơn ngưỡng ghi trong giả thuyết.

Dưới bảng là biểu đồ 1 đô la tăng thế nào theo quy tắc (nét liền) và khi giữ (nét đứt). Danh sách cho phép đổi coin và giai đoạn.
"""),
("Theo dõi Everscale (EVER)", """
EVER không có trên Binance, nên giá lấy từ Gate.io. Bạn có thể theo dõi ở ba nơi:

1. **Thẻ EVER** trong "Thị trường hôm nay" ở trang chủ: giá cách trung bình 50 ngày bao xa. Dương = quy tắc H-018 "trong thị trường", âm = "đứng ngoài".
2. **Trang EVER**: [Everscale]({site}coins/EVERUSDT.html), có biểu đồ, số liệu và trạng thái từng quy tắc.
3. **Giả thuyết H-018 và H-019**, kiểm tra trên EVER. Từ giữa 2022 quy tắc SMA50 đạt {ever_rule_cagr} mỗi năm so với {ever_hold_cagr} khi giữ, sụt giảm tệ nhất {ever_rule_dd} so với {ever_hold_dd}.

**Quan trọng.** Quy tắc "thắng" việc giữ chủ yếu vì giữ đã mất gần hết. Khối lượng giao dịch ngày của EVER nhỏ, giá có thể nhảy mạnh chỉ với giao dịch nhỏ. Đây là thông tin để theo dõi, không phải khuyến nghị.
"""),
("Cảnh báo qua Telegram", """
Trên trang này không cần cài đặt gì: chỉ cần mở trang mỗi ngày một lần. Cảnh báo dành cho người chạy **bản sao riêng** của dự án (miễn phí):

1. Tạo bot với [@BotFather](https://t.me/BotFather) và sao chép token.
2. Gửi bot của bạn một tin nhắn bất kỳ, rồi tìm chat id của bạn (ví dụ qua [@userinfobot](https://t.me/userinfobot)).
3. [Fork kho mã](https://github.com/f1devbin/Crypto-Research-Labs/fork), sau đó trong bản fork: *Settings → Secrets and variables → Actions* → thêm `TELEGRAM_BOT_TOKEN` và `TELEGRAM_CHAT_ID`.
4. *Settings → Pages → Source: GitHub Actions*, rồi *Actions → research-agents → Run workflow*.

Cảnh báo chỉ đến khi có thay đổi: một thẻ thị trường đổi vùng hoặc một giả thuyết có kết luận mới. Ngày yên ắng sẽ không có tin nhắn.
"""),
("Cách kiểm tra ý tưởng của bạn", """
Cách đơn giản nhất không cần lập trình:

1. Mở [một issue mới "Hypothesis idea"](https://github.com/f1devbin/Crypto-Research-Labs/issues/new?template=hypothesis.yml).
2. Mô tả quy tắc bằng lời đơn giản: khi nào bạn trong thị trường, khi nào đứng ngoài, những coin nào.
3. Giải thích **vì sao** nó nên hiệu quả và **thế nào là thành công**. Viết điều này trước khi xem bất kỳ biểu đồ nào.

Ý tưởng được chuyển thành tệp giả thuyết, được khóa và kiểm tra. Kết quả xuất hiện trên trang này bằng mọi ngôn ngữ, với trang riêng.

Nếu biết chút Python, hãy đọc [CONTRIBUTING.md](https://github.com/f1devbin/Crypto-Research-Labs/blob/main/CONTRIBUTING.md): một giả thuyết là một tệp YAML ngắn.
"""),
("Những gì dự án không làm", """
- **Không đưa lời khuyên.** Không kết luận nào ở đây bảo mua hay bán. Ngay cả "đạt" cũng chỉ là lý do để kiểm tra thêm.
- **Không giao dịch** và không quản lý tiền của ai.
- **Không hứa hẹn tương lai.** Mọi kết quả mô tả quá khứ; thị trường thay đổi.
- **Không phải mọi thứ đều được tính.** Thuế, trượt giá với lệnh lớn và rủi ro sàn phá sản không có trong số liệu. Phí thì có.
- **Coin nhỏ có rủi ro riêng.** Khi khối lượng thấp, giá bạn thấy có thể không phải giá bạn mua hay bán được.

Nếu muốn hành động theo điều gì đó ở đây, trước hết hãy tự hỏi: chuyện gì xảy ra với tôi nếu ngày mai quy tắc ngừng hiệu quả?
"""),
("Thực hành: bài tập trong một tuần", """
- [ ] Mở trang chủ và tìm vùng hôm nay của chỉ số sợ hãi & tham lam.
- [ ] Tìm trong bảng "Đồng coin" đồng có biến động cao nhất.
- [ ] Mở trang SOL: giá trên hay dưới trung bình 200 ngày?
- [ ] Mở H-005 và giải thích bằng một câu vì sao nó không đạt.
- [ ] Mở trang EVER và so sánh biến động của nó với Bitcoin.
- [ ] Quay lại sau một tuần: có thẻ thị trường nào đổi vùng không?
- [ ] Viết ra một ý tưởng của riêng bạn: quy tắc, vì sao nên hiệu quả, thế nào là thành công.
"""),
]

# --------------------------------------------------------------------------------------------- zh
ZH = [
("为什么有这个项目", """
本项目只回答一个问题：**一个简单的规则，能否比买入一个币并一直持有赚得更多？** 规则示例：“只在价格高于 50 日均线时持有 SOL”。

网上这样的规则成千上万，几乎都配着漂亮的图表。通常这是自欺欺人：规则被拟合到过去，忘了手续费，或者只在一段幸运的时期测试过。本项目用三种方法防止这一点：

1. **先写下来，再检验。** 规则和成功标准事先写好，并用指纹（哈希）“封存”。看到结果后无法再调整检验。
2. **在规则没见过的年份上检验。** 规则在 2018–2021 年选出，从 2022 年起评估。
3. **与运气比较。** 统计检验回答这样的结果是否可能偶然出现。

**今天的结论：**{verdict_line}这本身也是结果：它省下了按“漂亮”规则交易会亏掉的钱。
"""),
("工作原理", """
一切都在 GitHub 的服务器上自动运行，不需要任何人开着电脑。

[[flow]]

- **每天 UTC {update_utc}**：下载并检查最新价格，重新计算市场状态，并重新生成本网站。
- **每周一**：用新数据重新检验旧假设。结论发生变化时会发送提醒。
- **每月一次**：AI 模型可以提出新想法。每个想法在检验前都由人审核并锁定。
"""),
("首页导览", """
打开[首页]({site})。顶部菜单可跳转到各个部分，语言链接在其下方。

| 部分 | 内容 | 为什么看 |
| --- | --- | --- |
| 新手指南 | 阅读本页的 5 个步骤 | 看一次，理解逻辑 |
| 今日市场 | 卡片：资金费率、稳定币、恐惧与贪婪、BTC 趋势、BTC 波动率、市场广度、EVER | 今天市场的“天气” |
| 币种 | {n_coins} 个币：价格、7 天和 30 天、趋势、波动率 | 快速概览并进入各币页面 |
| 比特币与其 200 日均线 | 2020 年以来的 BTC 图表 | 整个市场的长期趋势 |
| 假设 | 全部 {n_hyps} 个想法及结论 | 检验过什么、结果如何 |
| 术语 | 10 个术语的通俗解释 | 遇到看不懂的词时 |
| 数据新鲜度 | 每个数据源的最新日期 | 数字看起来过时时 |

**如何阅读市场卡片。**大数字是今天的数值。下方带框的词是所处区间（例如“贪婪”或“高于”）。底部的线显示最近 12 个月。重要的不是数字本身，而是**区间的变化**：这时会发送提醒（第 7 课）。
"""),
("如何阅读币种页面——以 SOL 为例", """
每个币都有自己的页面。首页 →“币种”→ 点击 **SOL Solana**，或直接打开 [Solana]({site}coins/SOLUSDT.html)。其他币只需改地址里的代码：`ETHUSDT`、`BTCUSDT`、`EVERUSDT`……

页面分四步阅读：

1. **12 个月图表。**蓝线 = 价格，黄色虚线 = 50 日均线，白色点线 = 200 日均线。价格高于两条均线 = 上升趋势；低于两条 = 下降趋势。坐标是对数的：从 10 美元涨到 20 美元，与从 100 美元涨到 200 美元看起来一样。
2. **数据。**7 天、30 天和一年的涨跌；与均线的距离；波动率。波动率 70% 表示一年内典型涨跌幅约为 70%。今天：BTC {btc_vol}，SOL {sol_vol}，EVER {ever_vol}。另外三行提供背景：价格距最高收盘价有多远（SOL：{sol_dd_peak}），一年前投入的 $100 现在值多少（SOL：{sol_100}），以及该币与比特币同步程度，范围 −1 到 1（SOL：{sol_corr}）。
3. **已检验规则今天的状态。**来自假设的四条规则，以及每条今天会怎么做：“持仓”、“空仓”或仓位比例。旁边是该规则的检验结论。没有一条通过检验，所以这是**观察，不是信号**。
4. **包含该币种的研究。**对 SOL 最有意思的是 H-014（一周动量）：在 SOL 上规则的 Sharpe 为 {sol_mom_sharpe}，持有为 {sol_mom_hold}；但在 BTC 上失败，所以结论是“偏弱”。

**对任何币都可以问的三个问题：**价格高于还是低于 200 日均线？波动率高于还是低于平常？比特币在涨还是在跌（规则表最后一行）？
"""),
("如何阅读一个假设", """
从首页表格打开任意假设，例如 [H-003]({site}hypotheses/H-003.html)。顶部是带颜色的结论和一句“通俗地说”。

| 结论 | 含义 |
| --- | --- |
| 通过（绿色） | 达到了检验前设定的标准；值得独立复核 |
| 偏弱（琥珀色） | 比持有略好，但可能是运气 |
| 未通过（红色） | 没有跑赢持有 |

接着是结果表，每个币和区间一行。各列总是成对比较：规则对比“持有”：

- **Sharpe**：单位风险的收益。越高越好。持有比特币约为 0.5。
- **CAGR**：年均增长率。
- **最大回撤**：从峰值的最大跌幅。−50% 表示资金某一时刻减半。
- **p 值**：结果来自运气的概率。越小越好；必须低于假设中写明的门槛。

表格下方的图表显示 1 美元按规则（实线）和持有（虚线）会如何增长。列表可切换币种和区间。
"""),
("关注 Everscale (EVER)", """
EVER 不在 Binance 上市，所以价格来自 Gate.io。可以在三个地方关注它：

1. 首页“今日市场”中的 **EVER 卡片**：价格离 50 日均线有多远。正值 = H-018 规则“持仓”，负值 = “空仓”。
2. **EVER 页面**：[Everscale]({site}coins/EVERUSDT.html)，包含图表、数据和每条规则的状态。
3. 在 EVER 上检验的 **H-018 和 H-019 假设**。自 2022 年中以来，SMA50 规则的年化收益为 {ever_rule_cagr}，持有为 {ever_hold_cagr}；最大回撤 {ever_rule_dd}，持有为 {ever_hold_dd}。

**重要。**规则之所以“跑赢”持有，主要是因为持有几乎亏光了。EVER 的日交易量很小，即使小额交易也可能让价格大幅跳动。这是用于观察的信息，不是建议。
"""),
("Telegram 提醒", """
在本网站上无需任何设置：每天打开一次页面即可。提醒适用于运行**自己副本**的人（免费）：

1. 用 [@BotFather](https://t.me/BotFather) 创建机器人并复制其 token。
2. 给你的机器人发任意消息，然后查到你的 chat id（例如通过 [@userinfobot](https://t.me/userinfobot)）。
3. [Fork 本仓库](https://github.com/f1devbin/Crypto-Research-Labs/fork)，然后在 fork 中：*Settings → Secrets and variables → Actions* → 添加 `TELEGRAM_BOT_TOKEN` 和 `TELEGRAM_CHAT_ID`。
4. *Settings → Pages → Source: GitHub Actions*，然后 *Actions → research-agents → Run workflow*。

只有发生变化时才会收到提醒：某张市场卡片进入另一个区间，或某个假设得到新结论。平静的日子没有消息。
"""),
("如何检验你自己的想法", """
最简单的方法不需要编程：

1. 打开[新的 “Hypothesis idea” issue](https://github.com/f1devbin/Crypto-Research-Labs/issues/new?template=hypothesis.yml)。
2. 用简单的话描述规则：什么时候持仓，什么时候空仓，哪些币。
3. 说明它**为什么**应该有效，以及**什么算成功**。在看任何图表之前写下这些。

想法会被写成假设文件，锁定后进行检验。结果会以所有语言显示在本网站上，并有自己的页面。

如果你懂一点 Python，请阅读 [CONTRIBUTING.md](https://github.com/f1devbin/Crypto-Research-Labs/blob/main/CONTRIBUTING.md)：一个假设就是一个简短的 YAML 文件。
"""),
("本项目不做什么", """
- **不提供建议。**这里没有任何结论告诉你买或卖。即使“通过”，也只是进一步检查的理由。
- **不进行交易**，也不管理任何人的资金。
- **不承诺未来。**所有结果描述的都是过去；市场会变化。
- **并非一切都计入。**税费、大额订单的滑点以及交易所倒闭的风险不在数字中。手续费已计入。
- **小币种有特殊风险。**交易量小时，你看到的价格可能不是你实际买卖的价格。

如果你想根据这里的内容采取行动，请先问自己：如果规则明天失效，我会怎样？
"""),
("练习：一周任务", """
- [ ] 打开首页，找到恐惧与贪婪指数今天所处的区间。
- [ ] 在“币种”表中找到波动率最高的币。
- [ ] 打开 SOL 页面：价格高于还是低于 200 日均线？
- [ ] 打开 H-005，用一句话解释它为什么未通过。
- [ ] 打开 EVER 页面，把它的波动率与比特币比较。
- [ ] 一周后再回来：有没有哪张市场卡片换了区间？
- [ ] 写下一个你自己的想法：规则、为什么应该有效、什么算成功。
"""),
]

LESSONS = {"en": EN, "ru": RU, "es": ES, "pt": PT, "tr": TR, "vi": VI, "zh": ZH}

UI = {  # page chrome
 "en": {"nav": "Course for beginners", "title": "Crypto Research Labs course for beginners: how to read crypto data honestly",
        "h1": "Course for beginners", "badge": "For beginners · no finance or coding knowledge needed",
        "lead": "Ten short lessons, 5–10 minutes each: from \"what is this\" to testing your own idea. The numbers in the lessons are updated every day from live data.",
        "desc": "A free step-by-step course for beginners: how to read crypto market data, coin pages and trading-rule tests without fooling yourself. 10 short lessons, updated daily.",
        "toc": "Lessons", "lesson": "Lesson {n}", "flow": ["Market data", "Agents check and recalculate", "Results and verdicts", "Website and alerts"],
        "cta": "Start with lesson 1", "home_link": "New to crypto research? Take the free course for beginners"},
 "ru": {"nav": "Курс для новичков", "title": "Курс Crypto Research Labs для новичков: как честно читать данные о криптовалютах",
        "h1": "Курс для новичков", "badge": "Для новичков · знания финансов и программирования не нужны",
        "lead": "Десять коротких уроков по 5–10 минут: от «что это такое» до проверки своей идеи. Цифры в уроках каждый день обновляются из свежих данных.",
        "desc": "Бесплатный пошаговый курс для новичков: как читать данные крипторынка, страницы монет и проверки торговых правил, не обманывая себя. 10 коротких уроков, обновляется ежедневно.",
        "toc": "Уроки", "lesson": "Урок {n}", "flow": ["Рыночные данные", "Агенты проверяют и пересчитывают", "Результаты и вердикты", "Сайт и уведомления"],
        "cta": "Начать с урока 1", "home_link": "Впервые разбираетесь в крипте? Пройдите бесплатный курс для новичков"},
 "es": {"nav": "Curso para principiantes", "title": "Curso de Crypto Research Labs para principiantes: cómo leer datos cripto con honestidad",
        "h1": "Curso para principiantes", "badge": "Para principiantes · sin conocimientos de finanzas ni programación",
        "lead": "Diez lecciones cortas de 5–10 minutos: de \"qué es esto\" a probar tu propia idea. Las cifras de las lecciones se actualizan cada día con datos reales.",
        "desc": "Curso gratuito paso a paso para principiantes: cómo leer datos del mercado cripto, páginas de monedas y pruebas de reglas de trading sin engañarte. 10 lecciones cortas, actualizado a diario.",
        "toc": "Lecciones", "lesson": "Lección {n}", "flow": ["Datos de mercado", "Los agentes comprueban y recalculan", "Resultados y veredictos", "Web y alertas"],
        "cta": "Empieza por la lección 1", "home_link": "¿Nuevo en la investigación cripto? Haz el curso gratuito para principiantes"},
 "pt": {"nav": "Curso para iniciantes", "title": "Curso do Crypto Research Labs para iniciantes: como ler dados cripto com honestidade",
        "h1": "Curso para iniciantes", "badge": "Para iniciantes · sem precisar saber finanças ou programação",
        "lead": "Dez lições curtas de 5–10 minutos: de \"o que é isso\" até testar sua própria ideia. Os números das lições são atualizados todo dia com dados reais.",
        "desc": "Curso gratuito passo a passo para iniciantes: como ler dados do mercado cripto, páginas de moedas e testes de regras de trading sem se enganar. 10 lições curtas, atualizado diariamente.",
        "toc": "Lições", "lesson": "Lição {n}", "flow": ["Dados de mercado", "Agentes verificam e recalculam", "Resultados e veredictos", "Site e alertas"],
        "cta": "Comece pela lição 1", "home_link": "Novo em pesquisa cripto? Faça o curso gratuito para iniciantes"},
 "tr": {"nav": "Yeni başlayanlar kursu", "title": "Crypto Research Labs yeni başlayanlar kursu: kripto verilerini dürüstçe okumak",
        "h1": "Yeni başlayanlar için kurs", "badge": "Yeni başlayanlar için · finans ya da programlama bilgisi gerekmez",
        "lead": "5–10 dakikalık on kısa ders: \"bu nedir\"den kendi fikrinizi test etmeye kadar. Derslerdeki rakamlar her gün gerçek verilerle güncellenir.",
        "desc": "Yeni başlayanlar için ücretsiz adım adım kurs: kripto piyasa verilerini, coin sayfalarını ve alım satım kuralı testlerini kendinizi kandırmadan okumak. 10 kısa ders, her gün güncellenir.",
        "toc": "Dersler", "lesson": "Ders {n}", "flow": ["Piyasa verileri", "Ajanlar kontrol eder ve yeniden hesaplar", "Sonuçlar ve kararlar", "Site ve uyarılar"],
        "cta": "Ders 1 ile başlayın", "home_link": "Kripto araştırmasında yeni misiniz? Ücretsiz yeni başlayanlar kursunu alın"},
 "vi": {"nav": "Khóa học cho người mới", "title": "Khóa học Crypto Research Labs cho người mới: đọc dữ liệu crypto một cách trung thực",
        "h1": "Khóa học cho người mới", "badge": "Dành cho người mới · không cần kiến thức tài chính hay lập trình",
        "lead": "Mười bài ngắn, mỗi bài 5–10 phút: từ \"đây là gì\" đến kiểm tra ý tưởng của riêng bạn. Số liệu trong bài được cập nhật hằng ngày từ dữ liệu thật.",
        "desc": "Khóa học miễn phí từng bước cho người mới: cách đọc dữ liệu thị trường crypto, trang từng coin và kiểm tra quy tắc giao dịch mà không tự lừa mình. 10 bài ngắn, cập nhật hằng ngày.",
        "toc": "Các bài học", "lesson": "Bài {n}", "flow": ["Dữ liệu thị trường", "Tác tử kiểm tra và tính lại", "Kết quả và kết luận", "Trang web và cảnh báo"],
        "cta": "Bắt đầu với bài 1", "home_link": "Mới tìm hiểu nghiên cứu crypto? Học khóa miễn phí cho người mới"},
 "zh": {"nav": "新手课程", "title": "Crypto Research Labs 新手课程：如何诚实地解读加密货币数据",
        "h1": "新手课程", "badge": "面向新手 · 无需金融或编程知识",
        "lead": "十节短课，每节 5–10 分钟：从“这是什么”到检验你自己的想法。课程中的数字每天根据实时数据更新。",
        "desc": "免费的新手分步课程：如何读懂加密市场数据、币种页面和交易规则检验而不自欺。10 节短课，每日更新。",
        "toc": "课程目录", "lesson": "第 {n} 课", "flow": ["市场数据", "代理检查并重新计算", "结果与结论", "网站与提醒"],
        "cta": "从第 1 课开始", "home_link": "刚接触加密研究？参加免费新手课程"},
}

COMMA_DECIMAL = {"ru", "es", "pt", "tr", "vi"}
PLACEHOLDER = re.compile(r"\{([a-z_0-9]+)\}")


def placeholders(text: str) -> set:
    return set(PLACEHOLDER.findall(text))


def fill(text: str, values: dict) -> str:
    return PLACEHOLDER.sub(lambda m: str(values.get(m.group(1), "—")), text)


# ------------------------------------------------------------------ tiny markdown → HTML (trusted text)
_INLINE = [
    (re.compile(r"`([^`]+)`"), r"<code>\1</code>"),
    (re.compile(r"\*\*(.+?)\*\*"), r"<strong>\1</strong>"),
    (re.compile(r"(?<!\*)\*([^*]+)\*(?!\*)"), r"<em>\1</em>"),
    (re.compile(r"\[([^\]]+)\]\(([^)]+)\)"), r'<a href="\2">\1</a>'),
]


_NUM = re.compile(r"^\d+\. ")


def _inline(s: str) -> str:
    s = html.escape(s, quote=False)
    for rx, rep in _INLINE:
        s = rx.sub(rep, s)
    return s


def md_to_html(md: str, flow_html: str = "") -> str:
    out, blocks = [], [b.strip("\n") for b in re.split(r"\n\s*\n", md.strip()) if b.strip()]
    for b in blocks:
        lines = b.split("\n")
        if b.strip() == "[[flow]]":
            out.append(flow_html)
        elif all(re.match(r"^\d+\. ", ln) for ln in lines):
            out.append("<ol>" + "".join("<li>" + _inline(_NUM.sub("", ln)) + "</li>" for ln in lines) + "</ol>")
        elif all(ln.startswith("- [ ] ") for ln in lines):
            out.append('<ul class="tasks">' + "".join(
                f'<li><label><input type="checkbox"> {_inline(ln[6:])}</label></li>' for ln in lines) + "</ul>")
        elif all(ln.startswith("- ") for ln in lines):
            out.append("<ul>" + "".join(f"<li>{_inline(ln[2:])}</li>" for ln in lines) + "</ul>")
        elif all(ln.startswith("|") for ln in lines):
            rows = [[c.strip() for c in ln.strip("|").split("|")] for ln in lines if not re.match(r"^\|\s*-", ln)]
            head = "".join(f"<th>{_inline(c)}</th>" for c in rows[0])
            body = "".join("<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in r) + "</tr>" for r in rows[1:])
            out.append(f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>')
        else:
            out.append(f"<p>{_inline(' '.join(lines))}</p>")
    return "\n".join(out)


def flow_html(labels: list[str]) -> str:
    items = '<span class="flow-arrow" aria-hidden="true">→</span>'.join(
        f'<span class="flow-step">{html.escape(x)}</span>' for x in labels)
    return f'<div class="flow" role="img" aria-label="{html.escape(" → ".join(labels))}">{items}</div>'

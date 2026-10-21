"""Setup guide page (setup.html): your own copy, Telegram alerts, the optional AI model key.
Same tiny markdown as the course (crl.course.md_to_html). English is the fallback."""

REPO = "https://github.com/f1devbin/Crypto-Research-Labs"
SETTINGS = "Settings → Secrets and variables → Actions"

GUIDE = {
# ---------------------------------------------------------------- English
"en": {
 "nav": "Setup",
 "title": "Setup: Telegram alerts, AI model key, your own copy | Crypto Research Labs",
 "h1": "Setup: alerts, AI key and your own copy",
 "desc": "Step by step: get Telegram alerts in your language, connect an optional AI model key for a plain-language weekly digest, and run your own copy of Crypto Research Labs on GitHub for free.",
 "lead": "Everything here is optional. The dashboard works without any of it. All settings live in the GitHub repository, in " + SETTINGS + ".",
 "toc": "Contents",
 "sections": [
  ("Where the settings are", f"""Open the repository on GitHub → **{SETTINGS}**. There are two tabs:

- **Secrets**: hidden values (tokens, keys). Nobody can read them back, not even you, and they are masked in logs.
- **Variables**: ordinary values that are not secret (a language code, a model name).

A change applies from the next run. To run now: **Actions → research-agents → Run workflow**."""),
  ("Telegram alerts", f"""The agents can message you when something important happens: the market regime changes, the H-020 rule switches in or out, a hypothesis gets a new verdict, a data source breaks, and once a week a digest.

1. In Telegram open **@BotFather**. Use an existing bot (`/mybots` → your bot → **API Token**) or create one with `/newbot`.
2. Open your bot and press **Start**, otherwise it is not allowed to write to you.
3. Find your chat ID: write to **@userinfobot**, it replies with a number like `123456789`. For a group or a channel add the bot there; their IDs start with `-100`.
4. In **{SETTINGS} → Secrets → New repository secret** create `TELEGRAM_BOT_TOKEN` (the token) and `TELEGRAM_CHAT_ID` (the ID).
5. Language: in **Variables → New repository variable** create `TELEGRAM_LANG` with `en`, `ru`, `es`, `pt`, `tr`, `vi` or `zh`. Without it alerts are in English. Every alert ends with a link to the dashboard in the same language.
6. Test: **Actions → research-agents → Run workflow**, tick **test_alert**, run. You should get "Telegram alerts are connected" within a few minutes. If the step fails, the token or ID is wrong, or the bot was never started.

Alerts are sent only when something changes, so quiet days are silent."""),
  ("AI model key (optional)", f"""All tests are done by the engine with fixed rules; a model is never asked whether an idea works. A key from Anthropic adds two helpers:

- **Weekly digest in plain words.** Without a key you get the raw weekly reports in English. With a key a model rewrites them into a short briefing in the language of `TELEGRAM_LANG`, using only numbers from the reports and never suggesting trades.
- **New hypothesis drafts once a month** (the 1st). The model reads what has been tested and proposes new ideas as a pull request with status *draft*. You decide what to register; nothing is tested until you do.

How to connect:

1. Go to **console.anthropic.com**, sign up and add credit under Billing. The API is paid per use and separately from a Claude subscription. A weekly digest and a monthly proposal cost cents a month. Check first that your country is on Anthropic's list of supported regions.
2. **API Keys → Create Key**, copy the key (`sk-ant-…`). It is shown only once.
3. In **{SETTINGS} → Secrets** create `ANTHROPIC_API_KEY` with the key.
4. Optional: variable `CRL_LLM_MODEL` to choose another model (default `claude-sonnet-5-5`).
5. For the monthly drafts to arrive as pull requests: **Settings → Actions → General → Allow GitHub Actions to create and approve pull requests**.

To switch it off, delete the secret. Revoke a leaked key in the console at once."""),
  ("Run your own copy", f"""Everything runs on GitHub's free servers; nothing is needed on your computer.

1. Open [{REPO}]({REPO}) and press **Fork**.
2. In your fork: **Settings → Pages → Source: GitHub Actions**.
3. **Actions** → enable workflows if asked → **research-agents → Run workflow**. The first run takes about 20 minutes (it downloads the price history). Then it runs by itself every day.
4. Your dashboard appears at `https://<your-name>.github.io/Crypto-Research-Labs/`.
5. Add Telegram and the AI key as described above if you want them.

To add your own idea, see [CONTRIBUTING.md]({REPO}/blob/main/CONTRIBUTING.md) or post it in [Discussions → Ideas]({REPO}/discussions/categories/ideas)."""),
  ("All settings at a glance", """| Name | Where | What it does |
| --- | --- | --- |
| `TELEGRAM_BOT_TOKEN` | Secrets | bot token from @BotFather |
| `TELEGRAM_CHAT_ID` | Secrets | who receives alerts |
| `TELEGRAM_LANG` | Variables | alert language: en, ru, es, pt, tr, vi, zh |
| `ANTHROPIC_API_KEY` | Secrets | plain-language digest and monthly hypothesis drafts |
| `CRL_LLM_MODEL` | Variables | another model instead of claude-sonnet-5-5 |
| `GOOGLE_SITE_VERIFICATION` | Variables | Google Search Console code |
| `CRL_SITE_URL` | Variables | dashboard address if you use your own domain |"""),
 ],
},
# ---------------------------------------------------------------- Russian
"ru": {
 "nav": "Настройка",
 "title": "Настройка: уведомления в Telegram, ключ ИИ-модели, своя копия | Crypto Research Labs",
 "h1": "Настройка: уведомления, ключ ИИ и своя копия",
 "desc": "Пошагово: уведомления в Telegram на вашем языке, необязательный ключ ИИ-модели для понятной недельной сводки и бесплатный запуск своей копии Crypto Research Labs на GitHub.",
 "lead": "Всё здесь необязательно: дашборд работает и без этого. Все настройки хранятся в репозитории GitHub: Settings → Secrets and variables → Actions.",
 "toc": "Содержание",
 "sections": [
  ("Где находятся настройки", f"""Откройте репозиторий на GitHub → **{SETTINGS}**. Там две вкладки:

- **Secrets** — скрытые значения (токены, ключи). Прочитать их обратно нельзя даже владельцу, в логах они замаскированы.
- **Variables** — обычные несекретные значения (код языка, название модели).

Изменения действуют со следующего запуска. Запустить сразу: **Actions → research-agents → Run workflow**."""),
  ("Уведомления в Telegram", f"""Агенты пишут вам, когда происходит что-то важное: сменился режим рынка, правило H-020 вошло в рынок или вышло, у гипотезы новый вердикт, сломался источник данных, и раз в неделю — сводка.

1. В Telegram откройте **@BotFather**. Возьмите существующего бота (`/mybots` → бот → **API Token**) или создайте нового командой `/newbot`.
2. Откройте своего бота и нажмите **Start**, иначе ему нельзя писать вам.
3. Узнайте свой ID: напишите **@userinfobot**, он ответит числом вроде `123456789`. Для группы или канала добавьте туда бота, их ID начинаются с `-100`.
4. В **{SETTINGS} → Secrets → New repository secret** создайте `TELEGRAM_BOT_TOKEN` (токен) и `TELEGRAM_CHAT_ID` (ID).
5. Язык: во вкладке **Variables → New repository variable** создайте `TELEGRAM_LANG` со значением `ru` (или `en`, `es`, `pt`, `tr`, `vi`, `zh`). Без неё уведомления на английском. В конце каждого уведомления — ссылка на дашборд на том же языке.
6. Проверка: **Actions → research-agents → Run workflow**, отметьте **test_alert** и запустите. Через несколько минут придёт «уведомления в Telegram подключены». Если шаг упал — неверный токен или ID, либо бот не запущен.

Уведомления приходят только при изменениях, в спокойные дни их нет."""),
  ("Ключ ИИ-модели (необязательно)", f"""Все проверки делает движок по заранее зафиксированным правилам: модель никогда не решает, работает ли идея. Ключ Anthropic добавляет двух помощников:

- **Недельная сводка простыми словами.** Без ключа приходят сырые недельные отчёты на английском. С ключом модель пересказывает их коротко на языке из `TELEGRAM_LANG`, только по цифрам из отчётов и без торговых советов.
- **Черновики новых гипотез раз в месяц** (1-го числа). Модель смотрит, что уже проверено, и предлагает идеи пулл-реквестом в статусе *draft*. Регистрировать или нет — решаете вы; без регистрации ничего не проверяется.

Как подключить:

1. Зайдите на **console.anthropic.com**, зарегистрируйтесь и пополните баланс в разделе Billing. API оплачивается по факту использования и отдельно от подписки Claude. Недельная сводка и ежемесячные предложения стоят центы в месяц. Заранее проверьте, что ваша страна есть в списке поддерживаемых регионов Anthropic.
2. **API Keys → Create Key**, скопируйте ключ (`sk-ant-…`). Он показывается один раз.
3. В **{SETTINGS} → Secrets** создайте `ANTHROPIC_API_KEY` с этим ключом.
4. Необязательно: переменная `CRL_LLM_MODEL`, чтобы выбрать другую модель (по умолчанию `claude-sonnet-5-5`).
5. Чтобы черновики приходили пулл-реквестами: **Settings → Actions → General → Allow GitHub Actions to create and approve pull requests**.

Чтобы выключить — удалите секрет. Если ключ утёк, сразу отзовите его в консоли."""),
  ("Своя копия проекта", f"""Всё работает на бесплатных серверах GitHub, на вашем компьютере ничего не нужно.

1. Откройте [{REPO}]({REPO}) и нажмите **Fork**.
2. В своей копии: **Settings → Pages → Source: GitHub Actions**.
3. **Actions** → включите workflows, если попросит → **research-agents → Run workflow**. Первый запуск идёт около 20 минут (загружается история цен). Дальше всё работает само каждый день.
4. Ваш дашборд появится по адресу `https://<ваш-ник>.github.io/Crypto-Research-Labs/`.
5. По желанию подключите Telegram и ключ ИИ, как описано выше.

Свою идею можно предложить через [CONTRIBUTING.md]({REPO}/blob/main/CONTRIBUTING.md) или в [Discussions → Ideas]({REPO}/discussions/categories/ideas)."""),
  ("Все настройки одной таблицей", """| Имя | Где | Что делает |
| --- | --- | --- |
| `TELEGRAM_BOT_TOKEN` | Secrets | токен бота от @BotFather |
| `TELEGRAM_CHAT_ID` | Secrets | кому приходят уведомления |
| `TELEGRAM_LANG` | Variables | язык уведомлений: en, ru, es, pt, tr, vi, zh |
| `ANTHROPIC_API_KEY` | Secrets | сводка простыми словами и черновики гипотез |
| `CRL_LLM_MODEL` | Variables | другая модель вместо claude-sonnet-5-5 |
| `GOOGLE_SITE_VERIFICATION` | Variables | код Google Search Console |
| `CRL_SITE_URL` | Variables | адрес дашборда при своём домене |"""),
 ],
},
# ---------------------------------------------------------------- Spanish
"es": {
 "nav": "Configuración",
 "title": "Configuración: alertas de Telegram, clave de IA, tu propia copia | Crypto Research Labs",
 "h1": "Configuración: alertas, clave de IA y tu propia copia",
 "desc": "Paso a paso: alertas de Telegram en tu idioma, una clave opcional de modelo de IA para un resumen semanal en palabras sencillas, y tu propia copia gratuita de Crypto Research Labs en GitHub.",
 "lead": "Todo es opcional: el panel funciona sin nada de esto. Los ajustes viven en el repositorio de GitHub: Settings → Secrets and variables → Actions.",
 "toc": "Contenido",
 "sections": [
  ("Dónde están los ajustes", f"""Abre el repositorio en GitHub → **{SETTINGS}**. Hay dos pestañas:

- **Secrets**: valores ocultos (tokens, claves). Nadie puede volver a leerlos y se ocultan en los registros.
- **Variables**: valores normales no secretos (un código de idioma, un nombre de modelo).

Los cambios se aplican desde la siguiente ejecución. Para ejecutar ya: **Actions → research-agents → Run workflow**."""),
  ("Alertas de Telegram", f"""Los agentes te escriben cuando pasa algo importante: cambia el régimen del mercado, la regla H-020 entra o sale, una hipótesis recibe un nuevo veredicto, falla una fuente de datos, y una vez por semana, un resumen.

1. En Telegram abre **@BotFather**. Usa un bot existente (`/mybots` → tu bot → **API Token**) o crea uno con `/newbot`.
2. Abre tu bot y pulsa **Start**; si no, no puede escribirte.
3. Tu ID de chat: escribe a **@userinfobot**, responde con un número como `123456789`. Para un grupo o canal añade allí el bot; sus ID empiezan por `-100`.
4. En **{SETTINGS} → Secrets → New repository secret** crea `TELEGRAM_BOT_TOKEN` (el token) y `TELEGRAM_CHAT_ID` (el ID).
5. Idioma: en **Variables → New repository variable** crea `TELEGRAM_LANG` con `es` (o `en`, `ru`, `pt`, `tr`, `vi`, `zh`). Sin ella las alertas llegan en inglés. Cada alerta termina con un enlace al panel en el mismo idioma.
6. Prueba: **Actions → research-agents → Run workflow**, marca **test_alert** y ejecuta. En unos minutos llegará «las alertas de Telegram están conectadas». Si el paso falla, el token o el ID son incorrectos o el bot no se inició.

Las alertas solo llegan cuando algo cambia."""),
  ("Clave de modelo de IA (opcional)", f"""Todas las pruebas las hace el motor con reglas fijas; nunca se pregunta a un modelo si una idea funciona. Una clave de Anthropic añade dos ayudantes:

- **Resumen semanal en palabras sencillas.** Sin clave recibes los informes semanales en bruto, en inglés. Con clave, un modelo los resume en el idioma de `TELEGRAM_LANG`, solo con cifras de los informes y sin sugerir operaciones.
- **Borradores de nuevas hipótesis cada mes** (el día 1). El modelo propone ideas como pull request en estado *draft*. Tú decides qué registrar; nada se prueba hasta entonces.

Cómo conectarla:

1. Entra en **console.anthropic.com**, regístrate y añade saldo en Billing. La API se paga por uso y aparte de una suscripción de Claude; un resumen semanal y una propuesta mensual cuestan céntimos al mes. Comprueba antes que tu país está en la lista de regiones admitidas por Anthropic.
2. **API Keys → Create Key** y copia la clave (`sk-ant-…`). Solo se muestra una vez.
3. En **{SETTINGS} → Secrets** crea `ANTHROPIC_API_KEY` con la clave.
4. Opcional: variable `CRL_LLM_MODEL` para elegir otro modelo (por defecto `claude-sonnet-5-5`).
5. Para que los borradores lleguen como pull requests: **Settings → Actions → General → Allow GitHub Actions to create and approve pull requests**.

Para desactivarla, borra el secreto. Si la clave se filtra, revócala en la consola enseguida."""),
  ("Tu propia copia", f"""Todo funciona en los servidores gratuitos de GitHub; no necesitas nada en tu ordenador.

1. Abre [{REPO}]({REPO}) y pulsa **Fork**.
2. En tu copia: **Settings → Pages → Source: GitHub Actions**.
3. **Actions** → activa los workflows si lo pide → **research-agents → Run workflow**. La primera ejecución tarda unos 20 minutos (descarga el historial de precios). Después funciona sola cada día.
4. Tu panel estará en `https://<tu-usuario>.github.io/Crypto-Research-Labs/`.
5. Si quieres, añade Telegram y la clave de IA como se explica arriba.

Para proponer tu idea, mira [CONTRIBUTING.md]({REPO}/blob/main/CONTRIBUTING.md) o publícala en [Discussions → Ideas]({REPO}/discussions/categories/ideas)."""),
  ("Todos los ajustes", """| Nombre | Dónde | Qué hace |
| --- | --- | --- |
| `TELEGRAM_BOT_TOKEN` | Secrets | token del bot de @BotFather |
| `TELEGRAM_CHAT_ID` | Secrets | quién recibe las alertas |
| `TELEGRAM_LANG` | Variables | idioma: en, ru, es, pt, tr, vi, zh |
| `ANTHROPIC_API_KEY` | Secrets | resumen en palabras sencillas y borradores de hipótesis |
| `CRL_LLM_MODEL` | Variables | otro modelo en lugar de claude-sonnet-5-5 |
| `GOOGLE_SITE_VERIFICATION` | Variables | código de Google Search Console |
| `CRL_SITE_URL` | Variables | dirección del panel con dominio propio |"""),
 ],
},
# ---------------------------------------------------------------- Portuguese
"pt": {
 "nav": "Configuração",
 "title": "Configuração: alertas no Telegram, chave de IA, sua própria cópia | Crypto Research Labs",
 "h1": "Configuração: alertas, chave de IA e sua própria cópia",
 "desc": "Passo a passo: alertas no Telegram no seu idioma, uma chave opcional de modelo de IA para um resumo semanal em palavras simples e sua própria cópia gratuita do Crypto Research Labs no GitHub.",
 "lead": "Tudo aqui é opcional: o painel funciona sem isso. As configurações ficam no repositório do GitHub: Settings → Secrets and variables → Actions.",
 "toc": "Conteúdo",
 "sections": [
  ("Onde ficam as configurações", f"""Abra o repositório no GitHub → **{SETTINGS}**. Há duas abas:

- **Secrets**: valores ocultos (tokens, chaves). Ninguém consegue lê-los de volta e eles ficam mascarados nos logs.
- **Variables**: valores comuns, não secretos (um código de idioma, um nome de modelo).

As mudanças valem a partir da próxima execução. Para rodar agora: **Actions → research-agents → Run workflow**."""),
  ("Alertas no Telegram", f"""Os agentes avisam quando algo importante acontece: o regime do mercado muda, a regra H-020 entra ou sai, uma hipótese recebe novo veredicto, uma fonte de dados falha, e uma vez por semana, um resumo.

1. No Telegram abra **@BotFather**. Use um bot existente (`/mybots` → seu bot → **API Token**) ou crie um com `/newbot`.
2. Abra seu bot e toque em **Start**; sem isso ele não pode escrever para você.
3. Seu ID: escreva para **@userinfobot**, ele responde com um número como `123456789`. Para grupo ou canal, adicione o bot lá; os IDs começam com `-100`.
4. Em **{SETTINGS} → Secrets → New repository secret** crie `TELEGRAM_BOT_TOKEN` (o token) e `TELEGRAM_CHAT_ID` (o ID).
5. Idioma: em **Variables → New repository variable** crie `TELEGRAM_LANG` com `pt` (ou `en`, `ru`, `es`, `tr`, `vi`, `zh`). Sem ela os alertas vêm em inglês. Cada alerta termina com um link para o painel no mesmo idioma.
6. Teste: **Actions → research-agents → Run workflow**, marque **test_alert** e execute. Em poucos minutos chega "os alertas do Telegram estão conectados". Se o passo falhar, o token ou o ID estão errados ou o bot não foi iniciado.

Os alertas só chegam quando algo muda."""),
  ("Chave de modelo de IA (opcional)", f"""Todos os testes são feitos pelo motor com regras fixas; nunca se pergunta a um modelo se uma ideia funciona. Uma chave da Anthropic adiciona dois ajudantes:

- **Resumo semanal em palavras simples.** Sem chave você recebe os relatórios brutos em inglês. Com chave, um modelo os resume no idioma de `TELEGRAM_LANG`, só com números dos relatórios e sem sugerir operações.
- **Rascunhos de novas hipóteses todo mês** (dia 1). O modelo propõe ideias como pull request com status *draft*. Você decide o que registrar; nada é testado antes disso.

Como conectar:

1. Acesse **console.anthropic.com**, cadastre-se e adicione crédito em Billing. A API é paga por uso e separada de uma assinatura do Claude; um resumo semanal e uma proposta mensal custam centavos por mês. Verifique antes se o seu país está na lista de regiões suportadas pela Anthropic.
2. **API Keys → Create Key** e copie a chave (`sk-ant-…`). Ela aparece só uma vez.
3. Em **{SETTINGS} → Secrets** crie `ANTHROPIC_API_KEY` com a chave.
4. Opcional: variável `CRL_LLM_MODEL` para outro modelo (padrão `claude-sonnet-5-5`).
5. Para os rascunhos chegarem como pull requests: **Settings → Actions → General → Allow GitHub Actions to create and approve pull requests**.

Para desligar, apague o segredo. Se a chave vazar, revogue-a no console imediatamente."""),
  ("Sua própria cópia", f"""Tudo roda nos servidores gratuitos do GitHub; nada é necessário no seu computador.

1. Abra [{REPO}]({REPO}) e clique em **Fork**.
2. Na sua cópia: **Settings → Pages → Source: GitHub Actions**.
3. **Actions** → ative os workflows se pedir → **research-agents → Run workflow**. A primeira execução leva uns 20 minutos (baixa o histórico de preços). Depois roda sozinha todo dia.
4. Seu painel fica em `https://<seu-usuario>.github.io/Crypto-Research-Labs/`.
5. Se quiser, adicione Telegram e a chave de IA como descrito acima.

Para sugerir uma ideia, veja [CONTRIBUTING.md]({REPO}/blob/main/CONTRIBUTING.md) ou publique em [Discussions → Ideas]({REPO}/discussions/categories/ideas)."""),
  ("Todas as configurações", """| Nome | Onde | O que faz |
| --- | --- | --- |
| `TELEGRAM_BOT_TOKEN` | Secrets | token do bot do @BotFather |
| `TELEGRAM_CHAT_ID` | Secrets | quem recebe os alertas |
| `TELEGRAM_LANG` | Variables | idioma: en, ru, es, pt, tr, vi, zh |
| `ANTHROPIC_API_KEY` | Secrets | resumo em palavras simples e rascunhos de hipóteses |
| `CRL_LLM_MODEL` | Variables | outro modelo em vez de claude-sonnet-5-5 |
| `GOOGLE_SITE_VERIFICATION` | Variables | código do Google Search Console |
| `CRL_SITE_URL` | Variables | endereço do painel com domínio próprio |"""),
 ],
},
# ---------------------------------------------------------------- Turkish
"tr": {
 "nav": "Kurulum",
 "title": "Kurulum: Telegram bildirimleri, yapay zekâ anahtarı, kendi kopyanız | Crypto Research Labs",
 "h1": "Kurulum: bildirimler, yapay zekâ anahtarı ve kendi kopyanız",
 "desc": "Adım adım: kendi dilinizde Telegram bildirimleri, sade dilde haftalık özet için isteğe bağlı yapay zekâ anahtarı ve Crypto Research Labs'in GitHub'da ücretsiz kendi kopyası.",
 "lead": "Buradaki her şey isteğe bağlıdır: panel bunlar olmadan da çalışır. Ayarlar GitHub deposunda durur: Settings → Secrets and variables → Actions.",
 "toc": "İçindekiler",
 "sections": [
  ("Ayarlar nerede", f"""GitHub'da depoyu açın → **{SETTINGS}**. İki sekme vardır:

- **Secrets**: gizli değerler (token, anahtar). Kimse geri okuyamaz, kayıtlarda maskelenir.
- **Variables**: gizli olmayan sıradan değerler (dil kodu, model adı).

Değişiklik bir sonraki çalıştırmada geçerli olur. Hemen çalıştırmak için: **Actions → research-agents → Run workflow**."""),
  ("Telegram bildirimleri", f"""Ajanlar önemli bir şey olduğunda yazar: piyasa rejimi değişir, H-020 kuralı girer veya çıkar, bir hipotez yeni karar alır, bir veri kaynağı bozulur ve haftada bir özet.

1. Telegram'da **@BotFather**'ı açın. Mevcut bir botu kullanın (`/mybots` → bot → **API Token**) ya da `/newbot` ile yenisini oluşturun.
2. Botunuzu açıp **Start**'a basın, yoksa size yazamaz.
3. Sohbet kimliğiniz: **@userinfobot**'a yazın, `123456789` gibi bir sayı döner. Grup veya kanal için botu oraya ekleyin; kimlikleri `-100` ile başlar.
4. **{SETTINGS} → Secrets → New repository secret** içinde `TELEGRAM_BOT_TOKEN` (token) ve `TELEGRAM_CHAT_ID` (kimlik) oluşturun.
5. Dil: **Variables → New repository variable** içinde `TELEGRAM_LANG` değişkenini `tr` (veya `en`, `ru`, `es`, `pt`, `vi`, `zh`) ile oluşturun. Yoksa bildirimler İngilizce gelir. Her bildirim aynı dilde panele bağlantıyla biter.
6. Test: **Actions → research-agents → Run workflow**, **test_alert** kutusunu işaretleyip çalıştırın. Birkaç dakikada "Telegram bildirimleri bağlandı" gelir. Adım başarısız olursa token veya kimlik yanlıştır ya da bot başlatılmamıştır.

Bildirimler yalnızca bir şey değiştiğinde gelir."""),
  ("Yapay zekâ anahtarı (isteğe bağlı)", f"""Tüm testleri motor sabit kurallarla yapar; bir fikrin işe yarayıp yaramadığı asla bir modele sorulmaz. Anthropic anahtarı iki yardımcı ekler:

- **Sade dilde haftalık özet.** Anahtarsız ham haftalık raporlar İngilizce gelir. Anahtarla bir model bunları `TELEGRAM_LANG` dilinde kısaca özetler; yalnızca raporlardaki sayıları kullanır ve işlem önermez.
- **Her ay yeni hipotez taslakları** (ayın 1'i). Model fikirleri *draft* durumunda pull request olarak önerir. Neyin kaydedileceğine siz karar verirsiniz; o zamana kadar hiçbir şey test edilmez.

Nasıl bağlanır:

1. **console.anthropic.com**'a girin, kaydolun ve Billing bölümünden bakiye ekleyin. API kullanım başına ve Claude aboneliğinden ayrı ücretlendirilir; haftalık özet ve aylık öneri ayda birkaç sente mal olur. Önce ülkenizin Anthropic'in desteklenen bölgeler listesinde olduğunu kontrol edin.
2. **API Keys → Create Key**, anahtarı (`sk-ant-…`) kopyalayın. Yalnızca bir kez gösterilir.
3. **{SETTINGS} → Secrets** içinde anahtarla `ANTHROPIC_API_KEY` oluşturun.
4. İsteğe bağlı: başka bir model için `CRL_LLM_MODEL` değişkeni (varsayılan `claude-sonnet-5-5`).
5. Taslakların pull request olarak gelmesi için: **Settings → Actions → General → Allow GitHub Actions to create and approve pull requests**.

Kapatmak için gizli değeri silin. Anahtar sızarsa konsoldan hemen iptal edin."""),
  ("Kendi kopyanız", f"""Her şey GitHub'ın ücretsiz sunucularında çalışır; bilgisayarınızda hiçbir şey gerekmez.

1. [{REPO}]({REPO}) adresini açıp **Fork**'a basın.
2. Kopyanızda: **Settings → Pages → Source: GitHub Actions**.
3. **Actions** → istenirse workflow'ları etkinleştirin → **research-agents → Run workflow**. İlk çalıştırma yaklaşık 20 dakika sürer (fiyat geçmişini indirir). Sonra her gün kendiliğinden çalışır.
4. Paneliniz `https://<kullanıcı-adınız>.github.io/Crypto-Research-Labs/` adresinde olur.
5. İsterseniz Telegram'ı ve yapay zekâ anahtarını yukarıdaki gibi ekleyin.

Fikir önermek için [CONTRIBUTING.md]({REPO}/blob/main/CONTRIBUTING.md) dosyasına bakın ya da [Discussions → Ideas]({REPO}/discussions/categories/ideas) bölümüne yazın."""),
  ("Tüm ayarlar", """| Ad | Nerede | Ne yapar |
| --- | --- | --- |
| `TELEGRAM_BOT_TOKEN` | Secrets | @BotFather'dan bot token'ı |
| `TELEGRAM_CHAT_ID` | Secrets | bildirimleri kim alır |
| `TELEGRAM_LANG` | Variables | bildirim dili: en, ru, es, pt, tr, vi, zh |
| `ANTHROPIC_API_KEY` | Secrets | sade dilde özet ve hipotez taslakları |
| `CRL_LLM_MODEL` | Variables | claude-sonnet-5-5 yerine başka model |
| `GOOGLE_SITE_VERIFICATION` | Variables | Google Search Console kodu |
| `CRL_SITE_URL` | Variables | kendi alan adınızla panel adresi |"""),
 ],
},
# ---------------------------------------------------------------- Vietnamese
"vi": {
 "nav": "Cài đặt",
 "title": "Cài đặt: thông báo Telegram, khóa mô hình AI, bản sao riêng | Crypto Research Labs",
 "h1": "Cài đặt: thông báo, khóa AI và bản sao riêng",
 "desc": "Từng bước: nhận thông báo Telegram bằng ngôn ngữ của bạn, kết nối khóa mô hình AI (tùy chọn) để có bản tóm tắt tuần dễ hiểu, và chạy bản sao Crypto Research Labs miễn phí trên GitHub.",
 "lead": "Mọi thứ ở đây đều tùy chọn: bảng điều khiển vẫn hoạt động khi không có chúng. Các cài đặt nằm trong kho GitHub: Settings → Secrets and variables → Actions.",
 "toc": "Nội dung",
 "sections": [
  ("Cài đặt nằm ở đâu", f"""Mở kho trên GitHub → **{SETTINGS}**. Có hai thẻ:

- **Secrets**: giá trị ẩn (token, khóa). Không ai đọc lại được và chúng bị che trong nhật ký.
- **Variables**: giá trị thông thường, không bí mật (mã ngôn ngữ, tên mô hình).

Thay đổi có hiệu lực từ lần chạy tiếp theo. Chạy ngay: **Actions → research-agents → Run workflow**."""),
  ("Thông báo Telegram", f"""Các tác tử nhắn cho bạn khi có điều quan trọng: trạng thái thị trường thay đổi, quy tắc H-020 vào hoặc ra, giả thuyết có kết luận mới, nguồn dữ liệu bị lỗi, và mỗi tuần một bản tóm tắt.

1. Trong Telegram mở **@BotFather**. Dùng bot có sẵn (`/mybots` → bot → **API Token**) hoặc tạo mới bằng `/newbot`.
2. Mở bot của bạn và nhấn **Start**, nếu không bot không được phép nhắn cho bạn.
3. ID trò chuyện: nhắn cho **@userinfobot**, nó trả về một số như `123456789`. Với nhóm hoặc kênh, thêm bot vào đó; ID bắt đầu bằng `-100`.
4. Trong **{SETTINGS} → Secrets → New repository secret** tạo `TELEGRAM_BOT_TOKEN` (token) và `TELEGRAM_CHAT_ID` (ID).
5. Ngôn ngữ: trong **Variables → New repository variable** tạo `TELEGRAM_LANG` với `vi` (hoặc `en`, `ru`, `es`, `pt`, `tr`, `zh`). Nếu không có, thông báo bằng tiếng Anh. Mỗi thông báo kết thúc bằng liên kết tới bảng điều khiển cùng ngôn ngữ.
6. Kiểm tra: **Actions → research-agents → Run workflow**, chọn **test_alert** rồi chạy. Sau vài phút sẽ nhận "đã kết nối thông báo Telegram". Nếu bước này lỗi, token hoặc ID sai, hoặc bot chưa được bắt đầu.

Thông báo chỉ gửi khi có thay đổi."""),
  ("Khóa mô hình AI (tùy chọn)", f"""Mọi kiểm tra đều do bộ máy thực hiện theo quy tắc cố định; không bao giờ hỏi mô hình xem ý tưởng có hiệu quả không. Khóa Anthropic thêm hai trợ thủ:

- **Tóm tắt tuần bằng lời đơn giản.** Không có khóa, bạn nhận báo cáo thô bằng tiếng Anh. Có khóa, mô hình tóm tắt bằng ngôn ngữ của `TELEGRAM_LANG`, chỉ dùng số liệu trong báo cáo và không gợi ý giao dịch.
- **Bản nháp giả thuyết mới mỗi tháng** (ngày 1). Mô hình đề xuất ý tưởng dưới dạng pull request ở trạng thái *draft*. Bạn quyết định đăng ký cái nào; chưa đăng ký thì chưa kiểm tra.

Cách kết nối:

1. Vào **console.anthropic.com**, đăng ký và nạp tiền trong Billing. API tính phí theo mức dùng, tách biệt với gói Claude; tóm tắt tuần và đề xuất tháng chỉ tốn vài xu mỗi tháng. Hãy kiểm tra trước rằng quốc gia của bạn có trong danh sách khu vực được Anthropic hỗ trợ.
2. **API Keys → Create Key**, sao chép khóa (`sk-ant-…`). Khóa chỉ hiện một lần.
3. Trong **{SETTINGS} → Secrets** tạo `ANTHROPIC_API_KEY` với khóa đó.
4. Tùy chọn: biến `CRL_LLM_MODEL` để chọn mô hình khác (mặc định `claude-sonnet-5-5`).
5. Để bản nháp đến dưới dạng pull request: **Settings → Actions → General → Allow GitHub Actions to create and approve pull requests**.

Muốn tắt, hãy xóa secret. Nếu khóa bị lộ, thu hồi ngay trong console."""),
  ("Bản sao riêng", f"""Mọi thứ chạy trên máy chủ miễn phí của GitHub; máy tính của bạn không cần gì.

1. Mở [{REPO}]({REPO}) và nhấn **Fork**.
2. Trong bản sao: **Settings → Pages → Source: GitHub Actions**.
3. **Actions** → bật workflows nếu được hỏi → **research-agents → Run workflow**. Lần chạy đầu mất khoảng 20 phút (tải lịch sử giá). Sau đó tự chạy mỗi ngày.
4. Bảng điều khiển của bạn ở `https://<tên-của-bạn>.github.io/Crypto-Research-Labs/`.
5. Nếu muốn, thêm Telegram và khóa AI như mô tả ở trên.

Muốn đề xuất ý tưởng, xem [CONTRIBUTING.md]({REPO}/blob/main/CONTRIBUTING.md) hoặc đăng trong [Discussions → Ideas]({REPO}/discussions/categories/ideas)."""),
  ("Tất cả cài đặt", """| Tên | Ở đâu | Tác dụng |
| --- | --- | --- |
| `TELEGRAM_BOT_TOKEN` | Secrets | token bot từ @BotFather |
| `TELEGRAM_CHAT_ID` | Secrets | ai nhận thông báo |
| `TELEGRAM_LANG` | Variables | ngôn ngữ: en, ru, es, pt, tr, vi, zh |
| `ANTHROPIC_API_KEY` | Secrets | tóm tắt dễ hiểu và bản nháp giả thuyết |
| `CRL_LLM_MODEL` | Variables | mô hình khác thay cho claude-sonnet-5-5 |
| `GOOGLE_SITE_VERIFICATION` | Variables | mã Google Search Console |
| `CRL_SITE_URL` | Variables | địa chỉ bảng điều khiển khi dùng tên miền riêng |"""),
 ],
},
# ---------------------------------------------------------------- Chinese
"zh": {
 "nav": "设置",
 "title": "设置：Telegram 通知、AI 模型密钥、自己的副本 | Crypto Research Labs",
 "h1": "设置：通知、AI 密钥和自己的副本",
 "desc": "分步说明：用你的语言接收 Telegram 通知，可选接入 AI 模型密钥以获得通俗的每周摘要，并在 GitHub 上免费运行自己的 Crypto Research Labs 副本。",
 "lead": "这里的一切都是可选的：没有它们仪表盘也能正常运行。所有设置都在 GitHub 仓库中：Settings → Secrets and variables → Actions。",
 "toc": "目录",
 "sections": [
  ("设置在哪里", f"""在 GitHub 打开仓库 → **{SETTINGS}**。有两个标签：

- **Secrets**：隐藏的值（令牌、密钥）。任何人都无法再读取，日志中也会被遮蔽。
- **Variables**：普通的非机密值（语言代码、模型名称）。

修改从下一次运行开始生效。立即运行：**Actions → research-agents → Run workflow**。"""),
  ("Telegram 通知", f"""发生重要事情时智能体会通知你：市场状态变化、H-020 规则入场或离场、假设得到新结论、数据源出错，以及每周一次摘要。

1. 在 Telegram 打开 **@BotFather**。使用已有机器人（`/mybots` → 机器人 → **API Token**）或用 `/newbot` 新建。
2. 打开你的机器人并点击 **Start**，否则它无法给你发消息。
3. 获取聊天 ID：给 **@userinfobot** 发消息，它会回复类似 `123456789` 的数字。群组或频道需先把机器人加进去，其 ID 以 `-100` 开头。
4. 在 **{SETTINGS} → Secrets → New repository secret** 中创建 `TELEGRAM_BOT_TOKEN`（令牌）和 `TELEGRAM_CHAT_ID`（ID）。
5. 语言：在 **Variables → New repository variable** 中创建 `TELEGRAM_LANG`，值为 `zh`（或 `en`、`ru`、`es`、`pt`、`tr`、`vi`）。不设置则为英文。每条通知末尾附有同语言的仪表盘链接。
6. 测试：**Actions → research-agents → Run workflow**，勾选 **test_alert** 后运行。几分钟内会收到"Telegram 通知已连接"。如果该步骤失败，说明令牌或 ID 有误，或尚未启动机器人。

只有出现变化时才会发送通知。"""),
  ("AI 模型密钥（可选）", f"""所有检验都由引擎按固定规则完成，从不让模型判断一个想法是否有效。Anthropic 密钥会增加两个助手：

- **通俗的每周摘要。** 没有密钥时你收到的是英文原始周报。有密钥时，模型会用 `TELEGRAM_LANG` 的语言简要复述，只使用报告中的数字，也不给出交易建议。
- **每月的新假设草稿**（每月 1 日）。模型以 *draft* 状态的 pull request 提出想法。是否登记由你决定，登记前不会检验任何内容。

如何接入：

1. 访问 **console.anthropic.com**，注册并在 Billing 中充值。API 按用量计费，与 Claude 订阅分开；每周摘要和每月提案每月只需几美分。请先确认你所在国家在 Anthropic 支持的地区列表中。
2. **API Keys → Create Key**，复制密钥（`sk-ant-…`）。它只显示一次。
3. 在 **{SETTINGS} → Secrets** 中用该密钥创建 `ANTHROPIC_API_KEY`。
4. 可选：变量 `CRL_LLM_MODEL` 用于选择其他模型（默认 `claude-sonnet-5-5`）。
5. 若要草稿以 pull request 形式到达：**Settings → Actions → General → Allow GitHub Actions to create and approve pull requests**。

要关闭，删除该 secret 即可。如果密钥泄露，请立即在控制台撤销。"""),
  ("运行自己的副本", f"""一切都在 GitHub 的免费服务器上运行，你的电脑上不需要任何东西。

1. 打开 [{REPO}]({REPO}) 并点击 **Fork**。
2. 在你的副本中：**Settings → Pages → Source: GitHub Actions**。
3. **Actions** → 如有提示请启用 workflows → **research-agents → Run workflow**。首次运行约需 20 分钟（下载价格历史），之后每天自动运行。
4. 你的仪表盘地址为 `https://<你的用户名>.github.io/Crypto-Research-Labs/`。
5. 如需要，按上文接入 Telegram 和 AI 密钥。

想提出自己的想法，请看 [CONTRIBUTING.md]({REPO}/blob/main/CONTRIBUTING.md) 或发到 [Discussions → Ideas]({REPO}/discussions/categories/ideas)。"""),
  ("全部设置一览", """| 名称 | 位置 | 作用 |
| --- | --- | --- |
| `TELEGRAM_BOT_TOKEN` | Secrets | 来自 @BotFather 的机器人令牌 |
| `TELEGRAM_CHAT_ID` | Secrets | 通知接收者 |
| `TELEGRAM_LANG` | Variables | 通知语言：en、ru、es、pt、tr、vi、zh |
| `ANTHROPIC_API_KEY` | Secrets | 通俗摘要和假设草稿 |
| `CRL_LLM_MODEL` | Variables | 替代 claude-sonnet-5-5 的其他模型 |
| `GOOGLE_SITE_VERIFICATION` | Variables | Google Search Console 代码 |
| `CRL_SITE_URL` | Variables | 使用自有域名时的仪表盘地址 |"""),
 ],
},
}

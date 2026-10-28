"""Strings for the site layout: menu, home page, Market, Research and About pages, in 7 languages.
Merged into i18n.T; English is the fallback."""

L = {
"en": {
 "diag_dir_down": "down", "diag_dir_up": "up",
 "nav_market": "Market", "nav_research": "Research", "nav_beginners": "New here?", "nav_about": "About",
 "menu": "Menu",
 "hero_eyebrow": "Open research · updated {t}",
 "hero_q": "Can a simple rule beat “buy and hold”?",
 "hero_a": "We tested <strong>{n} trading ideas</strong> on real data, with fees and on years that were not used to "
           "pick them. {result}",
 "hero_one": "<strong>One passed.</strong>", "hero_some": "<strong>{p} passed.</strong>",
 "hero_none": "<strong>None has passed yet.</strong>",
 "tally_pass": "passed", "tally_weak": "weak", "tally_fail": "failed", "tally_wait": "waiting for data",
 "btn_market": "Market today →", "btn_new": "New here? Start here →",
 "scene_cap": "each block is one hypothesis; its height shows the verdict",
 "today_eyebrow": "Market today", "all_market": "All market indicators →",
 "passed_eyebrow": "What passed the test",
 "now_in": "now: in the market", "now_out": "now: out of the market",
 "pass_text": "Met the bar set before testing ({k} of {n} ideas have). It is not a promise of profit: it is being re-checked "
              "on new data.",
 "pass_risk_note": "This forecasts how big the next day's move will be, not its direction: on its own it does not beat holding, it helps judge risk.", "recheck_of": 'Re-check {id}',
 "open_hyp": "Open the hypothesis →", "recheck": "Re-check",
 "recheck_days": "{done} of {total} days", "recheck_date": "test on {date}",
 "digest_line": "Weekly digest: {start} – {end}", "read": "Read →",
 "market_eyebrow": "Market · {date}",
 "market_h1": "What the crypto market looks like today",
 "market_lead": "The readings that decided past verdicts, recomputed every day. This describes the market; it is "
                "not a signal to buy or sell.",
 "g_trend": "Where is the market going", "g_mood": "How nervous is it", "g_money": "Is money coming in",
 "g_coins": "Coins", "what_is": "What is this?", "watch_badge": "Watched",
 "fresh_ok": "✓ All sources up to date ({date})", "fresh_late": "{series}: {n} days behind",
 "fresh_link": "Data sources and freshness →",
 "research_h1": "What we tested and how it ended",
 "research_lead": "Every idea is written down and locked before it is tested. Click a verdict to filter the table.",
 "filter_all": "All", "all_h": "All hypotheses",
 "method_short_h": "How we test",
 "flow_steps": ["Idea written down", "Locked with a hash", "Tested out of sample", "Verdict", "Re-tested on new data"],
 "propose": "Propose your own idea →",
 "about_h1": "About the project",
 "about_how_h": "How it runs",
 "about_how": "Every morning, as soon as all sources have published yesterday's data (usually 03:00–07:00 UTC), "
              "the agents download and check the data, recompute the market readings and rebuild this site. Once a "
              "week they also re-test the hypotheses that are due, check every rule on every coin and write the "
              "weekly digest.",
 "about_links_h": "Code, data and settings",
 "read_h": "How to read this site in 2 minutes",
 "how2": [
  "<strong>The question.</strong> Can a simple, published rule beat just buying a coin and holding it, after "
  "trading fees? Usually it cannot. This project checks that honestly.",
  "<strong>Market</strong> shows what the crypto market looks like today. It describes the market; it is not a buy "
  "or sell signal.",
  "<strong>Research</strong> lists every idea tested so far. {pass} means it met the bar set in advance, {weak} "
  "means “a bit better, but could be luck”, {fail} means it did not beat holding.",
  "Open any hypothesis to see its numbers and a chart of how 1 dollar would have grown with the rule versus simply "
  "holding.",
  "Unfamiliar word? See the <a href=\"#glossary\">glossary</a> at the end of this page.",
 ],
},
"ru": {
 "diag_dir_down": "вниз", "diag_dir_up": "вверх",
 "nav_market": "Рынок", "nav_research": "Исследования", "nav_beginners": "Новичкам", "nav_about": "О проекте",
 "menu": "Меню",
 "hero_eyebrow": "Открытое исследование · обновлено {t}",
 "hero_q": "Можно ли обыграть «купил и держи» простым правилом?",
 "hero_a": "Мы проверили <strong>{n} торговых идей</strong> на реальных данных, с комиссиями и на годах, которые не "
           "использовались для их подбора. {result}",
 "hero_one": "<strong>Прошла одна.</strong>", "hero_some": "<strong>Прошли: {p}.</strong>",
 "hero_none": "<strong>Пока не прошла ни одна.</strong>",
 "tally_pass": "прошла", "tally_weak": "слабо", "tally_fail": "не прошли", "tally_wait": "ждёт данных",
 "btn_market": "Рынок сегодня →", "btn_new": "Новичок? Начните здесь →",
 "scene_cap": "каждый блок — одна гипотеза; высота — вердикт",
 "today_eyebrow": "Рынок сегодня", "all_market": "Все показатели рынка →",
 "passed_eyebrow": "Что прошло проверку",
 "now_in": "сейчас: в рынке", "now_out": "сейчас: вне рынка",
 "pass_text": "Выполнила планку, заданную до проверки (таких {k} из {n} идей). Это не обещание прибыли: её "
              "перепроверяют на новых данных.",
 "pass_risk_note": 'Это прогноз силы завтрашнего движения, а не его направления: сам по себе он не обгоняет удержание, а помогает оценивать риск.', "recheck_of": 'Перепроверка {id}',
 "open_hyp": "Открыть гипотезу →", "recheck": "Перепроверка",
 "recheck_days": "{done} из {total} дней", "recheck_date": "проверка {date}",
 "digest_line": "Недельная сводка: {start} – {end}", "read": "Читать →",
 "market_eyebrow": "Рынок · {date}",
 "market_h1": "Какая погода на крипторынке сегодня",
 "market_lead": "Показатели, от которых зависели прошлые вердикты. Пересчитываются каждый день. Это описание рынка, "
                "а не сигнал купить или продать.",
 "g_trend": "Куда идёт рынок", "g_mood": "Насколько нервно", "g_money": "Приходят ли деньги",
 "g_coins": "Монеты", "what_is": "Что это?", "watch_badge": "Под наблюдением",
 "fresh_ok": "✓ Все источники обновлены ({date})", "fresh_late": "{series}: отставание {n} дн.",
 "fresh_link": "Источники и свежесть данных →",
 "research_h1": "Что мы проверили и чем закончилось",
 "research_lead": "Каждая идея записывается и фиксируется до проверки. Нажмите на вердикт, чтобы отфильтровать "
                  "таблицу.",
 "filter_all": "Все", "all_h": "Все гипотезы",
 "method_short_h": "Как мы проверяем",
 "flow_steps": ["Идея записана", "Зафиксирована хешем", "Проверка вне выборки", "Вердикт",
                "Перепроверка на новых данных"],
 "propose": "Предложить свою идею →",
 "about_h1": "О проекте",
 "about_how_h": "Как это работает",
 "about_how": "Каждое утро, как только все источники опубликуют данные за вчера (обычно в 03:00–07:00 UTC), агенты "
              "скачивают и проверяют данные, пересчитывают показатели рынка и пересобирают этот сайт. Раз в неделю "
              "они ещё перепроверяют гипотезы, у которых подошёл срок, проверяют каждое правило на каждой монете и "
              "пишут недельную сводку.",
 "about_links_h": "Код, данные и настройка",
 "read_h": "Как читать этот сайт за 2 минуты",
 "how2": [
  "<strong>Главный вопрос.</strong> Может ли простое публичное правило обыграть обычную покупку монеты «купил и "
  "держи» с учётом комиссий? Чаще всего — нет. Этот проект проверяет это честно.",
  "<strong>Рынок</strong> показывает состояние крипторынка сегодня. Это описание рынка, а не сигнал купить или "
  "продать.",
  "<strong>Исследования</strong> — все проверенные идеи. {pass} — идея прошла планку, заданную заранее; {weak} — "
  "«чуть лучше, но это может быть везением»; {fail} — не обыграла простое удержание.",
  "Откройте любую гипотезу: там цифры и график — как вырос бы 1 доллар по правилу и при простом удержании.",
  "Непонятное слово? Загляните в <a href=\"#glossary\">словарь</a> в конце этой страницы.",
 ],
},
"es": {
 "diag_dir_down": "baja", "diag_dir_up": "sube",
 "nav_market": "Mercado", "nav_research": "Investigación", "nav_beginners": "¿Eres nuevo?", "nav_about": "Acerca de",
 "menu": "Menú",
 "hero_eyebrow": "Investigación abierta · actualizado {t}",
 "hero_q": "¿Puede una regla simple ganar a «comprar y mantener»?",
 "hero_a": "Probamos <strong>{n} ideas de trading</strong> con datos reales, con comisiones y en años que no se usaron "
           "para elegirlas. {result}",
 "hero_one": "<strong>Pasó una.</strong>", "hero_some": "<strong>Pasaron {p}.</strong>",
 "hero_none": "<strong>Ninguna ha pasado todavía.</strong>",
 "tally_pass": "pasó", "tally_weak": "débil", "tally_fail": "no pasaron", "tally_wait": "esperando datos",
 "btn_market": "Mercado hoy →", "btn_new": "¿Eres nuevo? Empieza aquí →",
 "scene_cap": "cada bloque es una hipótesis; su altura muestra el veredicto",
 "today_eyebrow": "Mercado hoy", "all_market": "Todos los indicadores del mercado →",
 "passed_eyebrow": "Lo que pasó la prueba",
 "now_in": "ahora: en el mercado", "now_out": "ahora: fuera del mercado",
 "pass_text": "Superó el listón fijado antes de la prueba ({k} de {n} ideas lo han hecho). No es una promesa de ganancias: "
              "se vuelve a comprobar con datos nuevos.",
 "pass_risk_note": 'Prevé el tamaño del movimiento de mañana, no su dirección: por sí sola no gana a mantener; ayuda a valorar el riesgo.', "recheck_of": 'Nueva comprobación {id}',
 "open_hyp": "Abrir la hipótesis →", "recheck": "Nueva comprobación",
 "recheck_days": "{done} de {total} días", "recheck_date": "prueba el {date}",
 "digest_line": "Resumen semanal: {start} – {end}", "read": "Leer →",
 "market_eyebrow": "Mercado · {date}",
 "market_h1": "Cómo está hoy el mercado cripto",
 "market_lead": "Las lecturas que decidieron veredictos anteriores, recalculadas cada día. Describen el mercado; no "
                "son una señal para comprar o vender.",
 "g_trend": "Hacia dónde va el mercado", "g_mood": "Qué tan nervioso está", "g_money": "¿Entra dinero?",
 "g_coins": "Monedas", "what_is": "¿Qué es esto?", "watch_badge": "En observación",
 "fresh_ok": "✓ Todas las fuentes al día ({date})", "fresh_late": "{series}: {n} días de retraso",
 "fresh_link": "Fuentes de datos y actualización →",
 "research_h1": "Qué probamos y cómo terminó",
 "research_lead": "Cada idea se escribe y se bloquea antes de probarla. Pulsa un veredicto para filtrar la tabla.",
 "filter_all": "Todas", "all_h": "Todas las hipótesis",
 "method_short_h": "Cómo probamos",
 "flow_steps": ["Idea escrita", "Bloqueada con un hash", "Prueba fuera de muestra", "Veredicto",
                "Nueva prueba con datos nuevos"],
 "propose": "Propón tu propia idea →",
 "about_h1": "Acerca del proyecto",
 "about_how_h": "Cómo funciona",
 "about_how": "Cada mañana, en cuanto todas las fuentes publican los datos de ayer (normalmente entre las 03:00 y las "
              "07:00 UTC), los agentes descargan y comprueban los datos, recalculan las lecturas del mercado y "
              "reconstruyen esta web. Una vez por semana también vuelven a probar las hipótesis que tocan, revisan "
              "cada regla en cada moneda y escriben el resumen semanal.",
 "about_links_h": "Código, datos y configuración",
 "read_h": "Cómo leer esta web en 2 minutos",
 "how2": [
  "<strong>La pregunta.</strong> ¿Puede una regla simple y publicada ganar a comprar una moneda y mantenerla, "
  "después de comisiones? Casi nunca. Este proyecto lo comprueba con honestidad.",
  "<strong>Mercado</strong> muestra cómo está hoy el mercado cripto. Describe el mercado; no es una señal de compra "
  "o venta.",
  "<strong>Investigación</strong> lista cada idea probada. {pass} significa que superó el listón fijado de antemano, "
  "{weak} significa «algo mejor, pero puede ser suerte», {fail} significa que no ganó a mantener.",
  "Abre cualquier hipótesis para ver sus números y un gráfico de cómo habría crecido 1 dólar con la regla frente a "
  "simplemente mantener.",
  "¿Una palabra desconocida? Consulta el <a href=\"#glossary\">glosario</a> al final de esta página.",
 ],
},
"pt": {
 "diag_dir_down": "queda", "diag_dir_up": "alta",
 "nav_market": "Mercado", "nav_research": "Pesquisa", "nav_beginners": "Novo aqui?", "nav_about": "Sobre",
 "menu": "Menu",
 "hero_eyebrow": "Pesquisa aberta · atualizado {t}",
 "hero_q": "Uma regra simples consegue vencer o “comprar e segurar”?",
 "hero_a": "Testamos <strong>{n} ideias de trading</strong> com dados reais, com taxas e em anos que não foram usados "
           "para escolhê-las. {result}",
 "hero_one": "<strong>Uma passou.</strong>", "hero_some": "<strong>{p} passaram.</strong>",
 "hero_none": "<strong>Nenhuma passou ainda.</strong>",
 "tally_pass": "passou", "tally_weak": "fraca", "tally_fail": "não passaram", "tally_wait": "aguardando dados",
 "btn_market": "Mercado hoje →", "btn_new": "Novo aqui? Comece aqui →",
 "scene_cap": "cada bloco é uma hipótese; a altura mostra o veredito",
 "today_eyebrow": "Mercado hoje", "all_market": "Todos os indicadores do mercado →",
 "passed_eyebrow": "O que passou no teste",
 "now_in": "agora: no mercado", "now_out": "agora: fora do mercado",
 "pass_text": "Atingiu a meta definida antes do teste ({k} de {n} ideias conseguiram). Não é promessa de lucro: ela é "
              "verificada de novo com dados novos.",
 "pass_risk_note": 'Prevê o tamanho do movimento de amanhã, não a direção: sozinha não vence segurar; ajuda a avaliar o risco.', "recheck_of": 'Nova verificação {id}',
 "open_hyp": "Abrir a hipótese →", "recheck": "Nova verificação",
 "recheck_days": "{done} de {total} dias", "recheck_date": "teste em {date}",
 "digest_line": "Resumo semanal: {start} – {end}", "read": "Ler →",
 "market_eyebrow": "Mercado · {date}",
 "market_h1": "Como está o mercado cripto hoje",
 "market_lead": "As leituras que decidiram veredictos anteriores, recalculadas todo dia. Elas descrevem o mercado; "
                "não são um sinal de compra ou venda.",
 "g_trend": "Para onde vai o mercado", "g_mood": "Quão nervoso ele está", "g_money": "Está entrando dinheiro?",
 "g_coins": "Moedas", "what_is": "O que é isto?", "watch_badge": "Em observação",
 "fresh_ok": "✓ Todas as fontes em dia ({date})", "fresh_late": "{series}: {n} dias de atraso",
 "fresh_link": "Fontes de dados e atualização →",
 "research_h1": "O que testamos e como terminou",
 "research_lead": "Cada ideia é escrita e travada antes do teste. Clique num veredito para filtrar a tabela.",
 "filter_all": "Todas", "all_h": "Todas as hipóteses",
 "method_short_h": "Como testamos",
 "flow_steps": ["Ideia escrita", "Travada com um hash", "Teste fora da amostra", "Veredito",
                "Novo teste com dados novos"],
 "propose": "Proponha sua própria ideia →",
 "about_h1": "Sobre o projeto",
 "about_how_h": "Como funciona",
 "about_how": "Toda manhã, assim que todas as fontes publicam os dados de ontem (normalmente entre 03:00 e 07:00 UTC), "
              "os agentes baixam e verificam os dados, recalculam as leituras do mercado e reconstroem este site. Uma "
              "vez por semana eles também testam de novo as hipóteses que estão no prazo, verificam cada regra em cada "
              "moeda e escrevem o resumo semanal.",
 "about_links_h": "Código, dados e configuração",
 "read_h": "Como ler este site em 2 minutos",
 "how2": [
  "<strong>A pergunta.</strong> Uma regra simples e publicada consegue vencer comprar uma moeda e segurá-la, depois "
  "das taxas? Quase nunca. Este projeto verifica isso com honestidade.",
  "<strong>Mercado</strong> mostra como está o mercado cripto hoje. Descreve o mercado; não é sinal de compra ou "
  "venda.",
  "<strong>Pesquisa</strong> lista cada ideia testada. {pass} significa que atingiu a meta definida antes, {weak} "
  "significa “um pouco melhor, mas pode ser sorte”, {fail} significa que não venceu segurar.",
  "Abra qualquer hipótese para ver os números e um gráfico de como 1 dólar teria crescido com a regra contra "
  "simplesmente segurar.",
  "Palavra desconhecida? Veja o <a href=\"#glossary\">glossário</a> no fim desta página.",
 ],
},
"tr": {
 "diag_dir_down": "aşağı", "diag_dir_up": "yukarı",
 "nav_market": "Piyasa", "nav_research": "Araştırma", "nav_beginners": "Yeni misiniz?", "nav_about": "Hakkında",
 "menu": "Menü",
 "hero_eyebrow": "Açık araştırma · güncellendi {t}",
 "hero_q": "Basit bir kural “al ve tut”u yenebilir mi?",
 "hero_a": "<strong>{n} alım satım fikrini</strong> gerçek verilerle, komisyonlar dahil ve seçimlerinde kullanılmayan "
           "yıllarda test ettik. {result}",
 "hero_one": "<strong>Biri geçti.</strong>", "hero_some": "<strong>{p} tanesi geçti.</strong>",
 "hero_none": "<strong>Henüz hiçbiri geçmedi.</strong>",
 "tally_pass": "geçti", "tally_weak": "zayıf", "tally_fail": "geçemedi", "tally_wait": "veri bekliyor",
 "btn_market": "Bugün piyasa →", "btn_new": "Yeni misiniz? Buradan başlayın →",
 "scene_cap": "her blok bir hipotez; yüksekliği kararı gösterir",
 "today_eyebrow": "Bugün piyasa", "all_market": "Tüm piyasa göstergeleri →",
 "passed_eyebrow": "Testi geçen",
 "now_in": "şu an: piyasada", "now_out": "şu an: piyasa dışında",
 "pass_text": "Testten önce belirlenen çıtayı geçti ({n} fikirden {k} tanesi geçti). Bu bir kâr vaadi değildir: yeni "
              "verilerle yeniden kontrol ediliyor.",
 "pass_risk_note": 'Yarınki hareketin yönünü değil büyüklüğünü tahmin eder: tek başına tutmayı yenmez, riski değerlendirmeye yardım eder.', "recheck_of": 'Yeniden kontrol {id}',
 "open_hyp": "Hipotezi aç →", "recheck": "Yeniden kontrol",
 "recheck_days": "{total} günün {done} günü", "recheck_date": "test tarihi {date}",
 "digest_line": "Haftalık özet: {start} – {end}", "read": "Oku →",
 "market_eyebrow": "Piyasa · {date}",
 "market_h1": "Kripto piyasası bugün nasıl görünüyor",
 "market_lead": "Geçmiş kararları belirleyen göstergeler, her gün yeniden hesaplanır. Piyasayı tarif eder; alım ya da "
                "satım sinyali değildir.",
 "g_trend": "Piyasa nereye gidiyor", "g_mood": "Ne kadar gergin", "g_money": "Para giriyor mu",
 "g_coins": "Coinler", "what_is": "Bu nedir?", "watch_badge": "Takipte",
 "fresh_ok": "✓ Tüm kaynaklar güncel ({date})", "fresh_late": "{series}: {n} gün geride",
 "fresh_link": "Veri kaynakları ve güncellik →",
 "research_h1": "Neleri test ettik ve sonuç ne oldu",
 "research_lead": "Her fikir test edilmeden önce yazılır ve kilitlenir. Tabloyu filtrelemek için bir karara tıklayın.",
 "filter_all": "Tümü", "all_h": "Tüm hipotezler",
 "method_short_h": "Nasıl test ediyoruz",
 "flow_steps": ["Fikir yazıldı", "Hash ile kilitlendi", "Örneklem dışı test", "Karar", "Yeni verilerle yeniden test"],
 "propose": "Kendi fikrinizi önerin →",
 "about_h1": "Proje hakkında",
 "about_how_h": "Nasıl çalışır",
 "about_how": "Her sabah, tüm kaynaklar dünün verisini yayımlar yayımlamaz (genellikle 03:00–07:00 UTC), ajanlar "
              "verileri indirip kontrol eder, piyasa göstergelerini yeniden hesaplar ve bu siteyi yeniden oluşturur. "
              "Haftada bir ayrıca zamanı gelen hipotezleri yeniden test eder, her kuralı her coinde kontrol eder ve "
              "haftalık özeti yazar.",
 "about_links_h": "Kod, veri ve ayarlar",
 "read_h": "Bu siteyi 2 dakikada okumak",
 "how2": [
  "<strong>Soru.</strong> Basit ve yayımlanmış bir kural, komisyonlardan sonra bir coini alıp tutmayı yenebilir mi? "
  "Çoğu zaman yenemez. Bu proje bunu dürüstçe kontrol eder.",
  "<strong>Piyasa</strong> kripto piyasasının bugün nasıl göründüğünü gösterir. Piyasayı tarif eder; alım ya da satım "
  "sinyali değildir.",
  "<strong>Araştırma</strong> test edilen her fikri listeler. {pass} önceden belirlenen çıtayı geçtiği, {weak} "
  "“biraz daha iyi ama şans olabilir”, {fail} tutmayı yenemediği anlamına gelir.",
  "Rakamlarını ve 1 doların kuralla, sadece tutmaya kıyasla nasıl büyüyeceğini gösteren grafiği görmek için herhangi "
  "bir hipotezi açın.",
  "Bilmediğiniz bir kelime mi var? Bu sayfanın sonundaki <a href=\"#glossary\">sözlüğe</a> bakın.",
 ],
},
"vi": {
 "diag_dir_down": "giảm", "diag_dir_up": "tăng",
 "nav_market": "Thị trường", "nav_research": "Nghiên cứu", "nav_beginners": "Người mới", "nav_about": "Giới thiệu",
 "menu": "Menu",
 "hero_eyebrow": "Nghiên cứu mở · cập nhật {t}",
 "hero_q": "Một quy tắc đơn giản có thắng được “mua và giữ” không?",
 "hero_a": "Chúng tôi đã kiểm tra <strong>{n} ý tưởng giao dịch</strong> trên dữ liệu thật, có tính phí và trên những "
           "năm không dùng để chọn chúng. {result}",
 "hero_one": "<strong>Một ý tưởng đạt.</strong>", "hero_some": "<strong>{p} ý tưởng đạt.</strong>",
 "hero_none": "<strong>Chưa có ý tưởng nào đạt.</strong>",
 "tally_pass": "đạt", "tally_weak": "yếu", "tally_fail": "không đạt", "tally_wait": "đang chờ dữ liệu",
 "btn_market": "Thị trường hôm nay →", "btn_new": "Người mới? Bắt đầu ở đây →",
 "scene_cap": "mỗi khối là một giả thuyết; chiều cao thể hiện kết luận",
 "today_eyebrow": "Thị trường hôm nay", "all_market": "Tất cả chỉ số thị trường →",
 "passed_eyebrow": "Điều đã vượt qua kiểm tra",
 "now_in": "hiện tại: trong thị trường", "now_out": "hiện tại: ngoài thị trường",
 "pass_text": "Đã đạt ngưỡng đặt ra trước khi kiểm tra ({k}/{n} ý tưởng làm được). Đây không phải lời hứa lợi nhuận: "
              "nó đang được kiểm tra lại trên dữ liệu mới.",
 "pass_risk_note": 'Đây là dự báo độ lớn của biến động ngày mai, không phải hướng: tự nó không thắng việc giữ, mà giúp đánh giá rủi ro.', "recheck_of": 'Kiểm tra lại {id}',
 "open_hyp": "Mở giả thuyết →", "recheck": "Kiểm tra lại",
 "recheck_days": "{done}/{total} ngày", "recheck_date": "kiểm tra ngày {date}",
 "digest_line": "Tóm tắt tuần: {start} – {end}", "read": "Đọc →",
 "market_eyebrow": "Thị trường · {date}",
 "market_h1": "Thị trường crypto hôm nay thế nào",
 "market_lead": "Các chỉ số đã quyết định những kết luận trước đây, được tính lại mỗi ngày. Chúng mô tả thị trường; "
                "không phải tín hiệu mua hay bán.",
 "g_trend": "Thị trường đang đi về đâu", "g_mood": "Thị trường căng thẳng đến mức nào", "g_money": "Tiền có đang vào không",
 "g_coins": "Các đồng coin", "what_is": "Đây là gì?", "watch_badge": "Đang theo dõi",
 "fresh_ok": "✓ Mọi nguồn đều đã cập nhật ({date})", "fresh_late": "{series}: chậm {n} ngày",
 "fresh_link": "Nguồn dữ liệu và độ mới →",
 "research_h1": "Chúng tôi đã kiểm tra gì và kết quả ra sao",
 "research_lead": "Mỗi ý tưởng được viết ra và khóa lại trước khi kiểm tra. Nhấn vào một kết luận để lọc bảng.",
 "filter_all": "Tất cả", "all_h": "Tất cả giả thuyết",
 "method_short_h": "Cách chúng tôi kiểm tra",
 "flow_steps": ["Viết ra ý tưởng", "Khóa bằng mã băm", "Kiểm tra ngoài mẫu", "Kết luận", "Kiểm tra lại trên dữ liệu mới"],
 "propose": "Đề xuất ý tưởng của bạn →",
 "about_h1": "Giới thiệu dự án",
 "about_how_h": "Cách vận hành",
 "about_how": "Mỗi sáng, ngay khi mọi nguồn đã công bố dữ liệu của hôm qua (thường lúc 03:00–07:00 UTC), các tác tử "
              "tải và kiểm tra dữ liệu, tính lại các chỉ số thị trường và dựng lại trang này. Mỗi tuần một lần, chúng "
              "còn kiểm tra lại các giả thuyết đến hạn, kiểm tra mọi quy tắc trên mọi đồng coin và viết bản tóm tắt tuần.",
 "about_links_h": "Mã nguồn, dữ liệu và cài đặt",
 "read_h": "Đọc trang này trong 2 phút",
 "how2": [
  "<strong>Câu hỏi.</strong> Một quy tắc đơn giản, công khai có thắng được việc mua một đồng coin rồi giữ, sau phí "
  "giao dịch không? Thường là không. Dự án này kiểm tra điều đó một cách trung thực.",
  "<strong>Thị trường</strong> cho thấy thị trường crypto hôm nay ra sao. Nó mô tả thị trường; không phải tín hiệu mua "
  "hay bán.",
  "<strong>Nghiên cứu</strong> liệt kê mọi ý tưởng đã kiểm tra. {pass} nghĩa là đạt ngưỡng đặt trước, {weak} nghĩa là "
  "“tốt hơn một chút nhưng có thể do may mắn”, {fail} nghĩa là không thắng việc giữ.",
  "Mở bất kỳ giả thuyết nào để xem số liệu và biểu đồ 1 đô la tăng thế nào theo quy tắc so với chỉ giữ.",
  "Gặp từ lạ? Xem <a href=\"#glossary\">thuật ngữ</a> ở cuối trang này.",
 ],
},
"zh": {
 "diag_dir_down": "下行", "diag_dir_up": "上行",
 "nav_market": "市场", "nav_research": "研究", "nav_beginners": "新手入门", "nav_about": "关于",
 "menu": "菜单",
 "hero_eyebrow": "公开研究 · 更新于 {t}",
 "hero_q": "简单的规则能跑赢“买入持有”吗？",
 "hero_a": "我们用真实数据检验了 <strong>{n} 个交易想法</strong>，计入手续费，并且只在未用于挑选规则的年份上评估。{result}",
 "hero_one": "<strong>只有一个通过。</strong>", "hero_some": "<strong>{p} 个通过。</strong>",
 "hero_none": "<strong>目前还没有通过的。</strong>",
 "tally_pass": "通过", "tally_weak": "偏弱", "tally_fail": "未通过", "tally_wait": "等待数据",
 "btn_market": "今日市场 →", "btn_new": "新手？从这里开始 →",
 "scene_cap": "每个方块代表一个假设；高度表示结论",
 "today_eyebrow": "今日市场", "all_market": "全部市场指标 →",
 "passed_eyebrow": "通过检验的",
 "now_in": "当前：在场", "now_out": "当前：离场",
 "pass_text": "达到了检验前设定的标准（{n} 个想法中有 {k} 个做到）。这不是盈利承诺：它正在用新数据重新检验。",
 "pass_risk_note": '这是对明天波动大小的预测，而不是方向：单靠它跑不赢持有，但有助于判断风险。', "recheck_of": '重新检验 {id}',
 "open_hyp": "打开该假设 →", "recheck": "重新检验",
 "recheck_days": "{done}/{total} 天", "recheck_date": "检验日期 {date}",
 "digest_line": "每周摘要：{start} – {end}", "read": "阅读 →",
 "market_eyebrow": "市场 · {date}",
 "market_h1": "今天的加密市场是什么样子",
 "market_lead": "这些指标决定了过去的结论，每天重新计算。它们描述市场，不是买入或卖出信号。",
 "g_trend": "市场往哪里走", "g_mood": "市场有多紧张", "g_money": "有资金流入吗",
 "g_coins": "币种", "what_is": "这是什么？", "watch_badge": "关注中",
 "fresh_ok": "✓ 所有数据源均已更新（{date}）", "fresh_late": "{series}：落后 {n} 天",
 "fresh_link": "数据来源与新鲜度 →",
 "research_h1": "我们检验了什么，结果如何",
 "research_lead": "每个想法都在检验前写下并锁定。点击一个结论即可筛选表格。",
 "filter_all": "全部", "all_h": "全部假设",
 "method_short_h": "我们如何检验",
 "flow_steps": ["写下想法", "用哈希锁定", "样本外检验", "结论", "用新数据重新检验"],
 "propose": "提出你自己的想法 →",
 "about_h1": "关于项目",
 "about_how_h": "运行方式",
 "about_how": "每天早上，一旦所有数据源发布了昨天的数据（通常在 UTC 03:00–07:00），代理就会下载并检查数据、重新计算市场"
              "指标并重建本网站。每周一次，它们还会重新检验到期的假设、在每个币种上检查每条规则，并撰写每周摘要。",
 "about_links_h": "代码、数据与设置",
 "read_h": "两分钟看懂本网站",
 "how2": [
  "<strong>核心问题。</strong>扣除交易手续费后，一条简单、公开的规则能否跑赢直接买入并持有？通常不能。本项目诚实地检验这一点。",
  "<strong>市场</strong>展示今天加密市场的状态。它描述市场，不是买卖信号。",
  "<strong>研究</strong>列出所有检验过的想法。{pass} 表示达到事先设定的标准，{weak} 表示“略好，但可能是运气”，{fail} "
  "表示没有跑赢持有。",
  "打开任意一个假设，可以看到数字，以及按规则与单纯持有相比 1 美元会如何增长的图表。",
  "遇到不懂的词？请看本页末尾的<a href=\"#glossary\">术语表</a>。",
 ],
},
}

# daily model forecast page (H-027 … H-030)
FC = {
"en": {
 "fc_h1": "Today's model forecast",
 "fc_lead": "Every morning, before 12:00 UTC, one model gives two probabilities for each of our {n} coins. It is a "
            "research experiment scored in public: not advice, and nobody trades on it.",
 "fc_published": "Published {t} · based on data up to {d}",
 "fc_late": "This forecast was published after 12:00 UTC, so it does not count in the score.",
 "fc_none": "No forecast yet: the first one appears after the next morning run.",
 "fc_th_up": "Chance of rising above fees", "fc_th_move": "Chance of a bigger move than usual",
 "fc_th_share": "Paper portfolio: share in the coin", "fc_th_change": "Change", "fc_pp": "{v} pp",
 "fc_gate": "† Gate.io: thin trading; the Gate fee and slippage are counted.",
 "fc_live_h": "How the model is doing live",
 "fc_live_text": "Scored on forecasts published before 12:00 UTC, from noon to noon, since {start}. A fair verdict "
                 "needs about a year of data: the first official test is on {date}.",
 "fc_live_wait": "Live scoring starts once the first forecasts have their next-day prices.",
 "fc_days": "Days scored", "fc_hits": "Direction right", "fc_skill_dir": "Direction: Brier skill vs base rate",
 "fc_skill_risk": "Bigger moves: Brier skill vs base rate",
 "fc_skill_note": "Above zero means the probabilities were better than the coin's usual frequency.",
 "fc_month_h": "$100 at the start of {m}",
 "fc_th_model": "Model's paper portfolio", "fc_th_hold": "Hold the coin", "fc_th_const": "Constant share",
 "fc_month_note": "A single month is mostly luck. The constant share holds the model's average share without any "
                  "timing: beating it is what would show skill.",
 "fc_back_h": "Tested on history (2022 onward)",
 "fc_back_text": "Walk-forward: every month the model is refitted only on what was already known, fees included.",
 "fc_back_wait": "The history test runs right after registration; its result will appear here.",
 "fc_back_dir": "Direction", "fc_back_risk": "Bigger moves", "fc_back_line": "Brier skill {bss}, p = {p}",
 "fc_how_h": "How it works",
 "fc_how": [
  "<strong>Two questions per coin.</strong> Will the next day's return beat the cost of buying and selling? Will "
  "the next day's move be bigger than the coin's usual daily move?",
  "<strong>One model for all coins.</strong> Inputs: recent returns, distance from the 50- and 200-day averages, "
  "volatility, Bitcoin's moves, funding, Fear & Greed, stablecoin supply and exchange flows, each compared with "
  "its own past year.",
  "<strong>No hindsight.</strong> The model is refitted on the first day of each month and then frozen; every "
  "forecast is committed to GitHub before 12:00 UTC, so it cannot be changed after the fact.",
  "<strong>Paper portfolio.</strong> The share of $100 held in the coin equals the chance of a rise; it changes "
  "only when the share moves by 10 points or more. Fees: 0.1 % per trade on Binance, 0.4 % on Gate.io coins.",
  "Pre-registered as <a href=\"hypotheses/H-027.html\">H-027</a>, <a href=\"hypotheses/H-028.html\">H-028</a> "
  "(history) and <a href=\"hypotheses/H-029.html\">H-029</a>, <a href=\"hypotheses/H-030.html\">H-030</a> (live).",
 ],
 "fc_home": "Today's model forecast for {n} coins ({d})", "fc_research": "Daily model forecast for every coin →",
 "fc_open": "Open →",
 "cal_h": "Calibration: forecast vs what happened", "cal_said": "Forecast", "cal_happened": "Happened",
 "cal_n": "Days", "c_bss": "Brier skill", "c_hits": "Guessed right", "c_q": "q (FDR)",
 "c_csharpe": "Constant share Sharpe", "c_days": "Days",
},
"ru": {
 "fc_h1": "Прогноз модели на сегодня",
 "fc_lead": "Каждое утро, до 12:00 UTC, одна модель даёт две вероятности для каждой из наших {n} монет. Это "
            "исследование с открытым счётом: не совет, и никто по нему не торгует.",
 "fc_published": "Опубликовано {t} · по данным до {d}",
 "fc_late": "Этот прогноз вышел после 12:00 UTC, поэтому в счёт не идёт.",
 "fc_none": "Прогноза пока нет: первый появится после ближайшего утреннего запуска.",
 "fc_th_up": "Шанс роста больше комиссии", "fc_th_move": "Шанс движения сильнее обычного",
 "fc_th_share": "Бумажный портфель: доля в монете", "fc_th_change": "Изменение", "fc_pp": "{v} п.п.",
 "fc_gate": "† Gate.io: мало торгов; учтены комиссия Gate и проскальзывание.",
 "fc_live_h": "Как модель справляется вживую",
 "fc_live_text": "Считаются прогнозы, опубликованные до 12:00 UTC, от полудня до полудня, начиная с {start}. Для "
                 "честного вердикта нужен примерно год данных: первая официальная проверка {date}.",
 "fc_live_wait": "Живой счёт начнётся, когда у первых прогнозов появятся цены следующего дня.",
 "fc_days": "Дней в счёте", "fc_hits": "Направление угадано", "fc_skill_dir": "Направление: Brier skill против базовой частоты",
 "fc_skill_risk": "Сильные движения: Brier skill против базовой частоты",
 "fc_skill_note": "Больше нуля — вероятности модели оказались точнее обычной частоты для монеты.",
 "fc_month_h": "$100 в начале месяца {m}",
 "fc_th_model": "Бумажный портфель модели", "fc_th_hold": "Просто держать", "fc_th_const": "Постоянная доля",
 "fc_month_note": "Результат одного месяца — в основном удача. Постоянная доля держит среднюю долю модели без "
                  "всякого выбора момента: обогнать её — вот что показало бы умение.",
 "fc_back_h": "Проверка на истории (с 2022 года)",
 "fc_back_text": "Скользящая проверка: каждый месяц модель переобучается только на том, что уже было известно, с комиссиями.",
 "fc_back_wait": "Проверка на истории запускается сразу после регистрации; результат появится здесь.",
 "fc_back_dir": "Направление", "fc_back_risk": "Сильные движения", "fc_back_line": "Brier skill {bss}, p = {p}",
 "fc_how_h": "Как это устроено",
 "fc_how": [
  "<strong>Два вопроса по каждой монете.</strong> Обгонит ли завтрашняя доходность затраты на покупку и продажу? "
  "Будет ли завтрашнее движение сильнее обычного дневного хода монеты?",
  "<strong>Одна модель на все монеты.</strong> Входные данные: недавние доходности, расстояние до 50- и 200-дневной "
  "средней, волатильность, движения биткоина, фандинг, индекс страха и жадности, объём стейблкоинов и притоки на "
  "биржи — каждый показатель сравнивается со своим прошлым годом.",
  "<strong>Без заглядывания в будущее.</strong> Модель переобучается 1-го числа каждого месяца и дальше не "
  "меняется; каждый прогноз коммитится на GitHub до 12:00 UTC, поэтому задним числом его не поправить.",
  "<strong>Бумажный портфель.</strong> Доля из $100 в монете равна шансу роста; она меняется, только если сдвиг "
  "10 пунктов или больше. Комиссии: 0,1 % за сделку на Binance, 0,4 % на монетах Gate.io.",
  "Предрегистрация: <a href=\"hypotheses/H-027.html\">H-027</a>, <a href=\"hypotheses/H-028.html\">H-028</a> "
  "(история) и <a href=\"hypotheses/H-029.html\">H-029</a>, <a href=\"hypotheses/H-030.html\">H-030</a> (вживую).",
 ],
 "fc_home": "Прогноз модели на сегодня для {n} монет ({d})", "fc_research": "Ежедневный прогноз модели для каждой монеты →",
 "fc_open": "Открыть →",
 "cal_h": "Калибровка: прогноз и что сбылось", "cal_said": "Прогноз", "cal_happened": "Сбылось",
 "cal_n": "Дней", "c_bss": "Brier skill", "c_hits": "Угадано", "c_q": "q (FDR)",
 "c_csharpe": "Sharpe постоянной доли", "c_days": "Дней",
},
"es": {
 "fc_h1": "Previsión del modelo para hoy",
 "fc_lead": "Cada mañana, antes de las 12:00 UTC, un modelo da dos probabilidades para cada una de nuestras {n} "
            "monedas. Es un experimento de investigación con marcador público: no es un consejo y nadie opera con él.",
 "fc_published": "Publicado {t} · con datos hasta {d}",
 "fc_late": "Esta previsión salió después de las 12:00 UTC, así que no cuenta en el marcador.",
 "fc_none": "Aún no hay previsión: la primera aparecerá tras la próxima ejecución de la mañana.",
 "fc_th_up": "Probabilidad de subir más que las comisiones", "fc_th_move": "Probabilidad de un movimiento mayor de lo habitual",
 "fc_th_share": "Cartera en papel: parte en la moneda", "fc_th_change": "Cambio", "fc_pp": "{v} pp",
 "fc_gate": "† Gate.io: poca negociación; se cuentan la comisión de Gate y el deslizamiento.",
 "fc_live_h": "Cómo le va al modelo en vivo",
 "fc_live_text": "Se puntúan las previsiones publicadas antes de las 12:00 UTC, de mediodía a mediodía, desde el "
                 "{start}. Un veredicto justo necesita cerca de un año de datos: la primera prueba oficial es el {date}.",
 "fc_live_wait": "La puntuación en vivo empieza cuando las primeras previsiones tienen el precio del día siguiente.",
 "fc_days": "Días puntuados", "fc_hits": "Dirección acertada", "fc_skill_dir": "Dirección: Brier skill frente a la frecuencia base",
 "fc_skill_risk": "Movimientos grandes: Brier skill frente a la frecuencia base",
 "fc_skill_note": "Por encima de cero significa que las probabilidades fueron mejores que la frecuencia habitual de la moneda.",
 "fc_month_h": "$100 al inicio de {m}",
 "fc_th_model": "Cartera en papel del modelo", "fc_th_hold": "Mantener la moneda", "fc_th_const": "Parte constante",
 "fc_month_note": "Un solo mes es sobre todo suerte. La parte constante mantiene la parte media del modelo sin elegir "
                  "momentos: superarla es lo que mostraría habilidad.",
 "fc_back_h": "Probado con el histórico (desde 2022)",
 "fc_back_text": "Prueba móvil: cada mes el modelo se reajusta solo con lo que ya se sabía, con comisiones.",
 "fc_back_wait": "La prueba con el histórico se ejecuta justo después del registro; su resultado aparecerá aquí.",
 "fc_back_dir": "Dirección", "fc_back_risk": "Movimientos grandes", "fc_back_line": "Brier skill {bss}, p = {p}",
 "fc_how_h": "Cómo funciona",
 "fc_how": [
  "<strong>Dos preguntas por moneda.</strong> ¿Superará el rendimiento de mañana el coste de comprar y vender? ¿Será "
  "el movimiento de mañana mayor que el movimiento diario habitual de la moneda?",
  "<strong>Un modelo para todas las monedas.</strong> Datos: rendimientos recientes, distancia a las medias de 50 y "
  "200 días, volatilidad, movimientos de Bitcoin, funding, miedo y codicia, oferta de stablecoins y flujos a "
  "exchanges, cada uno comparado con su propio último año.",
  "<strong>Sin mirar al futuro.</strong> El modelo se reajusta el primer día de cada mes y luego se congela; cada "
  "previsión se sube a GitHub antes de las 12:00 UTC, así que no se puede cambiar después.",
  "<strong>Cartera en papel.</strong> La parte de $100 en la moneda es igual a la probabilidad de subida; solo "
  "cambia si se mueve 10 puntos o más. Comisiones: 0,1 % por operación en Binance, 0,4 % en monedas de Gate.io.",
  "Prerregistrado como <a href=\"hypotheses/H-027.html\">H-027</a>, <a href=\"hypotheses/H-028.html\">H-028</a> "
  "(histórico) y <a href=\"hypotheses/H-029.html\">H-029</a>, <a href=\"hypotheses/H-030.html\">H-030</a> (en vivo).",
 ],
 "fc_home": "Previsión del modelo para hoy en {n} monedas ({d})", "fc_research": "Previsión diaria del modelo para cada moneda →",
 "fc_open": "Abrir →",
 "cal_h": "Calibración: previsión frente a lo ocurrido", "cal_said": "Previsión", "cal_happened": "Ocurrió",
 "cal_n": "Días", "c_bss": "Brier skill", "c_hits": "Aciertos", "c_q": "q (FDR)",
 "c_csharpe": "Sharpe de la parte constante", "c_days": "Días",
},
"pt": {
 "fc_h1": "Previsão do modelo para hoje",
 "fc_lead": "Toda manhã, antes das 12:00 UTC, um modelo dá duas probabilidades para cada uma das nossas {n} moedas. "
            "É um experimento de pesquisa com placar público: não é conselho, e ninguém opera com ele.",
 "fc_published": "Publicado {t} · com dados até {d}",
 "fc_late": "Esta previsão saiu depois das 12:00 UTC, então não conta no placar.",
 "fc_none": "Ainda não há previsão: a primeira aparece depois da próxima execução da manhã.",
 "fc_th_up": "Chance de subir acima das taxas", "fc_th_move": "Chance de um movimento maior que o normal",
 "fc_th_share": "Carteira de papel: fração na moeda", "fc_th_change": "Mudança", "fc_pp": "{v} p.p.",
 "fc_gate": "† Gate.io: pouco volume; a taxa da Gate e o slippage são contados.",
 "fc_live_h": "Como o modelo está indo ao vivo",
 "fc_live_text": "São pontuadas as previsões publicadas antes das 12:00 UTC, de meio-dia a meio-dia, desde {start}. "
                 "Um veredito justo precisa de cerca de um ano de dados: o primeiro teste oficial é em {date}.",
 "fc_live_wait": "A pontuação ao vivo começa quando as primeiras previsões tiverem o preço do dia seguinte.",
 "fc_days": "Dias pontuados", "fc_hits": "Direção certa", "fc_skill_dir": "Direção: Brier skill contra a frequência base",
 "fc_skill_risk": "Movimentos grandes: Brier skill contra a frequência base",
 "fc_skill_note": "Acima de zero significa que as probabilidades foram melhores que a frequência habitual da moeda.",
 "fc_month_h": "$100 no início de {m}",
 "fc_th_model": "Carteira de papel do modelo", "fc_th_hold": "Segurar a moeda", "fc_th_const": "Fração constante",
 "fc_month_note": "Um único mês é sobretudo sorte. A fração constante mantém a fração média do modelo sem escolher "
                  "momentos: vencê-la é o que mostraria habilidade.",
 "fc_back_h": "Testado no histórico (desde 2022)",
 "fc_back_text": "Teste móvel: todo mês o modelo é reajustado só com o que já se sabia, com taxas.",
 "fc_back_wait": "O teste no histórico roda logo após o registro; o resultado aparecerá aqui.",
 "fc_back_dir": "Direção", "fc_back_risk": "Movimentos grandes", "fc_back_line": "Brier skill {bss}, p = {p}",
 "fc_how_h": "Como funciona",
 "fc_how": [
  "<strong>Duas perguntas por moeda.</strong> O retorno de amanhã vai superar o custo de comprar e vender? O "
  "movimento de amanhã vai ser maior que o movimento diário habitual da moeda?",
  "<strong>Um modelo para todas as moedas.</strong> Dados: retornos recentes, distância das médias de 50 e 200 dias, "
  "volatilidade, movimentos do Bitcoin, funding, medo e ganância, oferta de stablecoins e fluxos para corretoras, "
  "cada um comparado com o seu próprio último ano.",
  "<strong>Sem olhar o futuro.</strong> O modelo é reajustado no primeiro dia de cada mês e depois congelado; cada "
  "previsão vai para o GitHub antes das 12:00 UTC, então não pode ser mudada depois.",
  "<strong>Carteira de papel.</strong> A fração de $100 na moeda é igual à chance de alta; só muda se mexer 10 "
  "pontos ou mais. Taxas: 0,1 % por operação na Binance, 0,4 % nas moedas da Gate.io.",
  "Pré-registrado como <a href=\"hypotheses/H-027.html\">H-027</a>, <a href=\"hypotheses/H-028.html\">H-028</a> "
  "(histórico) e <a href=\"hypotheses/H-029.html\">H-029</a>, <a href=\"hypotheses/H-030.html\">H-030</a> (ao vivo).",
 ],
 "fc_home": "Previsão do modelo para hoje em {n} moedas ({d})", "fc_research": "Previsão diária do modelo para cada moeda →",
 "fc_open": "Abrir →",
 "cal_h": "Calibração: previsão contra o que aconteceu", "cal_said": "Previsão", "cal_happened": "Aconteceu",
 "cal_n": "Dias", "c_bss": "Brier skill", "c_hits": "Acertos", "c_q": "q (FDR)",
 "c_csharpe": "Sharpe da fração constante", "c_days": "Dias",
},
"tr": {
 "fc_h1": "Modelin bugünkü tahmini",
 "fc_lead": "Her sabah 12:00 UTC'den önce tek bir model, {n} coinimizin her biri için iki olasılık verir. Bu, skoru "
            "herkese açık bir araştırma deneyidir: tavsiye değildir ve kimse buna göre işlem yapmaz.",
 "fc_published": "Yayımlandı {t} · {d} tarihine kadarki verilerle",
 "fc_late": "Bu tahmin 12:00 UTC'den sonra yayımlandı, bu yüzden skora sayılmaz.",
 "fc_none": "Henüz tahmin yok: ilki bir sonraki sabah çalışmasından sonra görünecek.",
 "fc_th_up": "Komisyonların üzerinde yükselme olasılığı", "fc_th_move": "Olağandan büyük hareket olasılığı",
 "fc_th_share": "Kâğıt portföy: coindeki pay", "fc_th_change": "Değişim", "fc_pp": "{v} puan",
 "fc_gate": "† Gate.io: işlem hacmi düşük; Gate komisyonu ve kayma hesaba katılır.",
 "fc_live_h": "Model canlıda nasıl gidiyor",
 "fc_live_text": "{start} tarihinden itibaren 12:00 UTC'den önce yayımlanan tahminler, öğleden öğleye puanlanır. Adil "
                 "bir karar için yaklaşık bir yıllık veri gerekir: ilk resmi test {date}.",
 "fc_live_wait": "Canlı puanlama, ilk tahminlerin ertesi gün fiyatları oluşunca başlar.",
 "fc_days": "Puanlanan gün", "fc_hits": "Doğru yön", "fc_skill_dir": "Yön: taban orana karşı Brier skill",
 "fc_skill_risk": "Büyük hareketler: taban orana karşı Brier skill",
 "fc_skill_note": "Sıfırın üstü, olasılıkların coinin olağan sıklığından daha iyi olduğu anlamına gelir.",
 "fc_month_h": "{m} başında $100",
 "fc_th_model": "Modelin kâğıt portföyü", "fc_th_hold": "Coini tutmak", "fc_th_const": "Sabit pay",
 "fc_month_note": "Tek bir ay çoğunlukla şanstır. Sabit pay, modelin ortalama payını zamanlama yapmadan tutar: onu "
                  "geçmek beceriyi gösterirdi.",
 "fc_back_h": "Geçmişte test (2022'den itibaren)",
 "fc_back_text": "Kayan test: model her ay yalnızca o ana kadar bilinenlerle yeniden kurulur, komisyonlar dahil.",
 "fc_back_wait": "Geçmiş testi kayıttan hemen sonra çalışır; sonucu burada görünecek.",
 "fc_back_dir": "Yön", "fc_back_risk": "Büyük hareketler", "fc_back_line": "Brier skill {bss}, p = {p}",
 "fc_how_h": "Nasıl çalışır",
 "fc_how": [
  "<strong>Her coin için iki soru.</strong> Yarınki getiri alım satım maliyetini geçecek mi? Yarınki hareket coinin "
  "olağan günlük hareketinden büyük olacak mı?",
  "<strong>Tüm coinler için tek model.</strong> Girdiler: son getiriler, 50 ve 200 günlük ortalamalara uzaklık, "
  "volatilite, Bitcoin'in hareketleri, funding, korku ve açgözlülük, stablecoin arzı ve borsalara akışlar; her biri "
  "kendi geçen yılıyla karşılaştırılır.",
  "<strong>Geleceğe bakmadan.</strong> Model her ayın ilk günü yeniden kurulur ve sonra dondurulur; her tahmin "
  "12:00 UTC'den önce GitHub'a işlenir, bu yüzden sonradan değiştirilemez.",
  "<strong>Kâğıt portföy.</strong> 100 doların coindeki payı yükselme olasılığına eşittir; yalnızca pay 10 puan ya "
  "da daha fazla değişince değişir. Komisyonlar: Binance'te işlem başına %0,1, Gate.io coinlerinde %0,4.",
  "Ön kayıt: <a href=\"hypotheses/H-027.html\">H-027</a>, <a href=\"hypotheses/H-028.html\">H-028</a> (geçmiş) ve "
  "<a href=\"hypotheses/H-029.html\">H-029</a>, <a href=\"hypotheses/H-030.html\">H-030</a> (canlı).",
 ],
 "fc_home": "{n} coin için modelin bugünkü tahmini ({d})", "fc_research": "Her coin için modelin günlük tahmini →",
 "fc_open": "Aç →",
 "cal_h": "Kalibrasyon: tahmin ve gerçekleşen", "cal_said": "Tahmin", "cal_happened": "Gerçekleşen",
 "cal_n": "Gün", "c_bss": "Brier skill", "c_hits": "Doğru tahmin", "c_q": "q (FDR)",
 "c_csharpe": "Sabit pay Sharpe", "c_days": "Gün",
},
"vi": {
 "fc_h1": "Dự báo của mô hình hôm nay",
 "fc_lead": "Mỗi sáng, trước 12:00 UTC, một mô hình đưa ra hai xác suất cho từng đồng trong {n} đồng coin của chúng tôi. "
            "Đây là thí nghiệm nghiên cứu được chấm điểm công khai: không phải lời khuyên và không ai giao dịch theo nó.",
 "fc_published": "Công bố {t} · theo dữ liệu đến {d}",
 "fc_late": "Dự báo này ra sau 12:00 UTC nên không được tính điểm.",
 "fc_none": "Chưa có dự báo: dự báo đầu tiên sẽ xuất hiện sau lần chạy buổi sáng tới.",
 "fc_th_up": "Xác suất tăng vượt phí", "fc_th_move": "Xác suất biến động lớn hơn bình thường",
 "fc_th_share": "Danh mục giấy: tỷ trọng coin", "fc_th_change": "Thay đổi", "fc_pp": "{v} điểm %",
 "fc_gate": "† Gate.io: thanh khoản thấp; đã tính phí Gate và trượt giá.",
 "fc_live_h": "Mô hình đang làm thế nào trên dữ liệu thật",
 "fc_live_text": "Chấm điểm các dự báo công bố trước 12:00 UTC, từ trưa đến trưa, kể từ {start}. Một kết luận công bằng "
                 "cần khoảng một năm dữ liệu: kiểm tra chính thức đầu tiên vào {date}.",
 "fc_live_wait": "Việc chấm điểm trực tiếp bắt đầu khi các dự báo đầu tiên có giá của ngày hôm sau.",
 "fc_days": "Số ngày được chấm", "fc_hits": "Đoán đúng hướng", "fc_skill_dir": "Hướng: Brier skill so với tần suất cơ sở",
 "fc_skill_risk": "Biến động lớn: Brier skill so với tần suất cơ sở",
 "fc_skill_note": "Trên 0 nghĩa là xác suất của mô hình tốt hơn tần suất thông thường của đồng coin.",
 "fc_month_h": "$100 vào đầu {m}",
 "fc_th_model": "Danh mục giấy của mô hình", "fc_th_hold": "Giữ coin", "fc_th_const": "Tỷ trọng cố định",
 "fc_month_note": "Một tháng chủ yếu là may rủi. Tỷ trọng cố định giữ mức tỷ trọng trung bình của mô hình mà không "
                  "chọn thời điểm: vượt được nó mới cho thấy năng lực.",
 "fc_back_h": "Kiểm tra trên lịch sử (từ 2022)",
 "fc_back_text": "Kiểm tra trượt: mỗi tháng mô hình chỉ được huấn luyện lại trên những gì đã biết, có tính phí.",
 "fc_back_wait": "Kiểm tra trên lịch sử chạy ngay sau khi đăng ký; kết quả sẽ hiện ở đây.",
 "fc_back_dir": "Hướng", "fc_back_risk": "Biến động lớn", "fc_back_line": "Brier skill {bss}, p = {p}",
 "fc_how_h": "Cách hoạt động",
 "fc_how": [
  "<strong>Hai câu hỏi cho mỗi coin.</strong> Lợi nhuận ngày mai có vượt chi phí mua và bán không? Biến động ngày mai "
  "có lớn hơn mức biến động hằng ngày thông thường của coin không?",
  "<strong>Một mô hình cho mọi coin.</strong> Đầu vào: lợi nhuận gần đây, khoảng cách tới trung bình 50 và 200 ngày, "
  "biến động, diễn biến của Bitcoin, funding, sợ hãi & tham lam, nguồn cung stablecoin và dòng tiền vào sàn — mỗi "
  "chỉ số được so với năm vừa qua của chính nó.",
  "<strong>Không nhìn trước tương lai.</strong> Mô hình được huấn luyện lại vào ngày đầu mỗi tháng rồi giữ nguyên; "
  "mỗi dự báo được commit lên GitHub trước 12:00 UTC nên không thể sửa lại về sau.",
  "<strong>Danh mục giấy.</strong> Tỷ trọng của $100 nằm trong coin bằng xác suất tăng; chỉ thay đổi khi lệch từ 10 "
  "điểm trở lên. Phí: 0,1 % mỗi giao dịch trên Binance, 0,4 % với coin trên Gate.io.",
  "Đăng ký trước là <a href=\"hypotheses/H-027.html\">H-027</a>, <a href=\"hypotheses/H-028.html\">H-028</a> (lịch sử) "
  "và <a href=\"hypotheses/H-029.html\">H-029</a>, <a href=\"hypotheses/H-030.html\">H-030</a> (trực tiếp).",
 ],
 "fc_home": "Dự báo của mô hình hôm nay cho {n} coin ({d})", "fc_research": "Dự báo hằng ngày của mô hình cho từng coin →",
 "fc_open": "Mở →",
 "cal_h": "Hiệu chuẩn: dự báo và thực tế", "cal_said": "Dự báo", "cal_happened": "Thực tế",
 "cal_n": "Ngày", "c_bss": "Brier skill", "c_hits": "Đoán đúng", "c_q": "q (FDR)",
 "c_csharpe": "Sharpe tỷ trọng cố định", "c_days": "Ngày",
},
"zh": {
 "fc_h1": "模型今日预测",
 "fc_lead": "每天早上 12:00 UTC 之前，同一个模型为我们的 {n} 个币各给出两个概率。这是公开计分的研究实验：不是建议，也没有人据此交易。",
 "fc_published": "发布于 {t} · 基于截至 {d} 的数据",
 "fc_late": "这份预测在 12:00 UTC 之后发布，因此不计入成绩。",
 "fc_none": "暂无预测：第一份将在下一次早间运行后出现。",
 "fc_th_up": "上涨超过手续费的概率", "fc_th_move": "波动大于平常的概率",
 "fc_th_share": "模拟组合：该币仓位", "fc_th_change": "变化", "fc_pp": "{v} 个百分点",
 "fc_gate": "† Gate.io：成交清淡；已计入 Gate 手续费和滑点。",
 "fc_live_h": "模型的实盘表现",
 "fc_live_text": "自 {start} 起，对 12:00 UTC 前发布的预测按中午到中午计分。公正的结论需要约一年的数据：第一次正式检验在 {date}。",
 "fc_live_wait": "首批预测有了次日价格后，实盘计分即开始。",
 "fc_days": "计分天数", "fc_hits": "方向猜中", "fc_skill_dir": "方向：相对基础频率的 Brier skill",
 "fc_skill_risk": "大幅波动：相对基础频率的 Brier skill",
 "fc_skill_note": "大于零表示模型的概率比该币的通常频率更准确。",
 "fc_month_h": "{m} 月初的 $100",
 "fc_th_model": "模型的模拟组合", "fc_th_hold": "持有该币", "fc_th_const": "固定仓位",
 "fc_month_note": "单个月份主要取决于运气。固定仓位以模型的平均仓位持有、不择时：跑赢它才说明有能力。",
 "fc_back_h": "历史检验（2022 年起）",
 "fc_back_text": "滚动检验：每个月模型只用当时已知的数据重新训练，计入手续费。",
 "fc_back_wait": "历史检验在登记后立即运行；结果将显示在这里。",
 "fc_back_dir": "方向", "fc_back_risk": "大幅波动", "fc_back_line": "Brier skill {bss}，p = {p}",
 "fc_how_h": "运作方式",
 "fc_how": [
  "<strong>每个币两个问题。</strong>明天的收益会超过买卖成本吗？明天的波动会大于该币平常的日波动吗？",
  "<strong>所有币共用一个模型。</strong>输入：近期收益、与 50 日和 200 日均线的距离、波动率、比特币走势、资金费率、恐惧与贪婪、"
  "稳定币供应和交易所资金流，每项都与其自身过去一年比较。",
  "<strong>不偷看未来。</strong>模型在每月第一天重新训练后冻结；每份预测在 12:00 UTC 前提交到 GitHub，事后无法修改。",
  "<strong>模拟组合。</strong>$100 中持有该币的比例等于上涨概率；只有变动达到 10 个百分点或以上才调整。手续费：Binance 每笔 "
  "0.1%，Gate.io 币种 0.4%。",
  "预先登记为 <a href=\"hypotheses/H-027.html\">H-027</a>、<a href=\"hypotheses/H-028.html\">H-028</a>（历史）和 "
  "<a href=\"hypotheses/H-029.html\">H-029</a>、<a href=\"hypotheses/H-030.html\">H-030</a>（实盘）。",
 ],
 "fc_home": "模型今日对 {n} 个币的预测（{d}）", "fc_research": "模型对每个币的每日预测 →",
 "fc_open": "打开 →",
 "cal_h": "校准：预测与实际", "cal_said": "预测", "cal_happened": "实际",
 "cal_n": "天数", "c_bss": "Brier skill", "c_hits": "猜中", "c_q": "q (FDR)",
 "c_csharpe": "固定仓位 Sharpe", "c_days": "天数",
},
}

TITLES = {
 "ru": {"H-027": "Ежедневная модель оценивает шанс роста каждой монеты выше комиссии точнее базовой частоты",
        "H-028": "Ежедневная модель оценивает шанс движения сильнее обычного точнее базовой частоты",
        "H-029": "Живая перепроверка H-027: ежедневные прогнозы направления, опубликованные до 12:00 UTC",
        "H-030": "Живая перепроверка H-028: ежедневные прогнозы сильных движений, опубликованные до 12:00 UTC"},
 "es": {"H-027": "Un modelo diario da la probabilidad de que cada moneda suba más que las comisiones mejor que su frecuencia base",
        "H-028": "Un modelo diario da la probabilidad de un movimiento mayor de lo habitual mejor que su frecuencia base",
        "H-029": "Réplica en vivo de H-027: previsiones diarias de dirección publicadas antes de las 12:00 UTC",
        "H-030": "Réplica en vivo de H-028: previsiones diarias de movimientos grandes publicadas antes de las 12:00 UTC"},
 "pt": {"H-027": "Um modelo diário estima a chance de cada moeda subir acima das taxas melhor que a frequência base",
        "H-028": "Um modelo diário estima a chance de um movimento maior que o normal melhor que a frequência base",
        "H-029": "Replicação ao vivo da H-027: previsões diárias de direção publicadas antes das 12:00 UTC",
        "H-030": "Replicação ao vivo da H-028: previsões diárias de movimentos grandes publicadas antes das 12:00 UTC"},
 "tr": {"H-027": "Günlük bir model, her coinin komisyonların üzerinde yükselme olasılığını taban orandan daha iyi veriyor",
        "H-028": "Günlük bir model, her coinin olağandan büyük hareket olasılığını taban orandan daha iyi veriyor",
        "H-029": "H-027'nin canlı tekrarı: 12:00 UTC'den önce yayımlanan günlük yön tahminleri",
        "H-030": "H-028'in canlı tekrarı: 12:00 UTC'den önce yayımlanan günlük büyük hareket tahminleri"},
 "vi": {"H-027": "Mô hình hằng ngày ước lượng xác suất mỗi coin tăng vượt phí tốt hơn tần suất cơ sở",
        "H-028": "Mô hình hằng ngày ước lượng xác suất biến động lớn hơn bình thường tốt hơn tần suất cơ sở",
        "H-029": "Kiểm tra lại trực tiếp H-027: dự báo hướng hằng ngày công bố trước 12:00 UTC",
        "H-030": "Kiểm tra lại trực tiếp H-028: dự báo biến động lớn hằng ngày công bố trước 12:00 UTC"},
 "zh": {"H-027": "每日模型对各币涨幅超过手续费的概率估计优于基础频率",
        "H-028": "每日模型对各币出现大于平常波动的概率估计优于基础频率",
        "H-029": "H-027 的实盘复现：12:00 UTC 前发布的每日方向预测",
        "H-030": "H-028 的实盘复现：12:00 UTC 前发布的每日大幅波动预测"},
}
FAMILIES = {"en": "forecast", "ru": "прогноз", "es": "previsión", "pt": "previsão", "tr": "tahmin", "vi": "dự báo",
            "zh": "预测"}

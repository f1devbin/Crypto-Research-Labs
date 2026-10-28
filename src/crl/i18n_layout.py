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
 "pass_text": "The only one of {n} ideas that met the bar set before testing. It is not a promise of profit: it is "
              "being re-checked on new data.",
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
 "pass_text": "Единственная из {n} идей, которая выполнила планку, заданную до проверки. Это не обещание прибыли: "
              "её перепроверяют на новых данных.",
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
 "pass_text": "La única de {n} ideas que superó el listón fijado antes de la prueba. No es una promesa de ganancias: "
              "se está volviendo a comprobar con datos nuevos.",
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
 "pass_text": "A única de {n} ideias que atingiu a meta definida antes do teste. Não é promessa de lucro: ela está "
              "sendo verificada de novo com dados novos.",
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
 "pass_text": "{n} fikir arasında testten önce belirlenen çıtayı geçen tek fikir. Bu bir kâr vaadi değildir: yeni "
              "verilerle yeniden kontrol ediliyor.",
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
 "pass_text": "Ý tưởng duy nhất trong {n} ý tưởng đạt ngưỡng đặt ra trước khi kiểm tra. Đây không phải lời hứa lợi "
              "nhuận: nó đang được kiểm tra lại trên dữ liệu mới.",
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
 "pass_text": "{n} 个想法中唯一达到检验前设定标准的一个。这不是盈利承诺：它正在用新数据重新检验。",
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

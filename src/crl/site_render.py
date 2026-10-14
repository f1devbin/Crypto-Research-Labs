"""HTML for the static dashboard, one prerendered copy per language.

Every number and every word is rendered server-side so search engines and readers without
JavaScript see the full content; JavaScript only draws the charts. English lives at the site
root (x-default), other languages under /<lang>/, linked with hreflang.
"""
import html
import json

from crl.i18n import DEFAULT, LANGS, sub, t

CHART_JS = "https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"
VERDICT_CLASS = {"PASS": "pass", "WEAK": "weak", "FAIL": "fail"}
VERDICT_KEY = {"PASS": "Pass", "WEAK": "Weak", "FAIL": "Fail"}
REPO = "https://github.com/f1devbin/Crypto-Research-Labs"

CSS = """
:root{--bg:#0d1117;--panel:#161b22;--line:#3d444d;--text:#ffffff;--text2:#e6edf3;--link:#79c0ff;
--pass:#2ea043;--weak:#d29922;--fail:#f85149;--accent:#58a6ff;--hold:#e6edf3}
@media (prefers-color-scheme:light){:root{--bg:#ffffff;--panel:#f6f8fa;--line:#c8d1da;--text:#000000;
--text2:#1f2328;--link:#0550ae;--pass:#116329;--weak:#7d4e00;--fail:#a40e26;--accent:#0550ae;--hold:#1f2328}}
*{box-sizing:border-box}
html{font-size:18px}
body{margin:0;background:var(--bg);color:var(--text);font:1rem/1.6 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
a{color:var(--link)}
header,main,footer{max-width:1100px;margin:0 auto;padding:0 16px}
header{padding-top:28px}
nav{display:flex;flex-wrap:wrap;gap:6px 18px;font-weight:600;margin:6px 0 4px}
nav.langs{gap:4px 14px;font-weight:500;font-size:.95rem}
nav.langs a[aria-current]{color:var(--text);font-weight:700;text-decoration:none}
h1{font-size:2rem;line-height:1.25;margin:.2em 0 .3em}
h2{font-size:1.45rem;margin:1.8em 0 .6em;border-bottom:2px solid var(--line);padding-bottom:.25em}
h3{font-size:1.1rem;margin:0 0 .3em}
p,li{color:var(--text2)}
.lead{font-size:1.12rem;max-width:62ch}
.meta{color:var(--text2);font-size:.95rem}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px}
.card{overflow-wrap:anywhere;background:var(--panel);border:2px solid var(--line);border-radius:10px;padding:14px 16px}
.value{font-size:1.9rem;font-weight:700;line-height:1.2;margin:.15em 0}
.band{display:inline-block;border:2px solid var(--text);border-radius:6px;padding:0 8px;font-weight:700;font-size:.9rem}
.note{font-size:.92rem;margin:.5em 0 0}
.explain{font-size:.92rem;margin:.2em 0 .4em}
.plain{font-size:1.05rem;border-left:6px solid var(--accent);background:var(--panel);padding:10px 14px;border-radius:6px}
.steps{counter-reset:s;list-style:none;padding:0}
.steps li{counter-increment:s;margin:.4em 0;padding-left:2.2em;position:relative}
.steps li::before{content:counter(s);position:absolute;left:0;top:0;width:1.6em;height:1.6em;border-radius:50%;
background:var(--accent);color:var(--bg);font-weight:700;text-align:center;line-height:1.6em}
details{background:var(--panel);border:2px solid var(--line);border-radius:10px;padding:8px 14px;margin:8px 0}
summary{cursor:pointer;font-weight:700;color:var(--text)}
.chart{position:relative;width:100%;height:300px;margin:8px 0}
.spark{position:relative;width:100%;height:80px;margin-top:8px}
.table-wrap{overflow-x:auto;border:2px solid var(--line);border-radius:10px}
table{border-collapse:collapse;width:100%;font-size:.95rem}
td:first-child{white-space:nowrap}
th,td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top}
th{background:var(--panel);color:var(--text);white-space:nowrap}
td{color:var(--text2)}
td.num{text-align:right;white-space:nowrap;font-variant-numeric:tabular-nums}
.badge{display:inline-block;min-width:4.2em;text-align:center;border-radius:6px;padding:1px 8px;font-weight:700;color:#fff}
.badge.pass{background:var(--pass)}.badge.weak{background:var(--weak)}.badge.fail{background:var(--fail)}
.badge.none{background:transparent;color:var(--text);border:2px solid var(--line)}
.yes{color:var(--pass);font-weight:700}.no{color:var(--text2)}
pre{background:var(--panel);border:2px solid var(--line);border-radius:10px;padding:12px;overflow-x:auto;font-size:.88rem;color:var(--text)}
.callout{border-left:6px solid var(--weak);background:var(--panel);padding:10px 14px;border-radius:6px}
select{font:inherit;padding:4px 8px;background:var(--panel);color:var(--text);border:2px solid var(--line);border-radius:6px}
footer{margin-top:48px;padding-bottom:40px;border-top:2px solid var(--line)}
:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
"""

# draws every <canvas data-chart="key"> from the JSON in #chart-data
CHART_SCRIPT = """
(function(){
var el=document.getElementById('chart-data');if(!el||!window.Chart)return;
var D=JSON.parse(el.textContent),css=getComputedStyle(document.documentElement);
function c(n){return css.getPropertyValue(n).trim()}
Chart.defaults.color=c('--text');Chart.defaults.borderColor=c('--line');
Chart.defaults.font.size=14;Chart.defaults.animation=false;
function draw(cv,spec){
 var ds=spec.series.map(function(s,i){return{label:s.label,data:s.v,borderColor:c(s.color||(i?'--hold':'--accent')),
  borderWidth:s.width||2,pointRadius:0,tension:0,borderDash:s.dash||[],spanGaps:true}});
 return new Chart(cv,{type:'line',data:{labels:spec.d,datasets:ds},options:{responsive:true,maintainAspectRatio:false,
  interaction:{mode:'index',intersect:false},plugins:{legend:{display:!spec.spark,labels:{boxWidth:18}},
  tooltip:{enabled:!spec.spark}},scales:{x:{display:!spec.spark,ticks:{maxTicksLimit:8,maxRotation:0}},
  y:{display:!spec.spark,type:spec.log?'logarithmic':'linear'}}}});
}
document.querySelectorAll('canvas[data-chart]').forEach(function(cv){var s=D[cv.dataset.chart];if(s)draw(cv,s)});
var sel=document.getElementById('curve-select');
if(sel){var cv=document.getElementById('curve'),ch=draw(cv,D[sel.value]);
 sel.addEventListener('change',function(){ch.destroy();ch=draw(cv,D[sel.value])})}
})();
"""


def _safe_json(obj) -> str:
    """JSON that can sit inside <script> without closing it."""
    return json.dumps(obj, separators=(",", ":"), ensure_ascii=False).replace("</", "<\\/")


def e(x) -> str:
    return html.escape("" if x is None else str(x), quote=True)


def pct(v, signed=False, nd=1) -> str:
    if v is None:
        return "—"
    return f"{v:+.{nd}%}" if signed else f"{v:.{nd}%}"


def num(v, nd=2) -> str:
    return "—" if v is None else f"{v:.{nd}f}"


def page_url(base: str, lang: str, hid: str | None = None) -> str:
    root = base if lang == DEFAULT else f"{base}{lang}/"
    return f"{root}hypotheses/{hid}.html" if hid else root


def page_path(lang: str, hid: str | None = None) -> str:
    """Path of a page relative to the site root."""
    root = "" if lang == DEFAULT else f"{lang}/"
    return f"{root}hypotheses/{hid}.html" if hid else f"{root}index.html"


def asset_root(lang: str, hid: str | None = None) -> str:
    depth = (lang != DEFAULT) + (hid is not None)
    return "../" * depth


def verdict_word(lang: str, verdict) -> str:
    return t(lang, VERDICT_KEY[verdict]) if verdict in VERDICT_KEY else "—"


def badge(lang: str, verdict) -> str:
    if not verdict:
        return '<span class="badge none">—</span>'
    return f'<span class="badge {VERDICT_CLASS.get(verdict, "none")}">{e(verdict_word(lang, verdict))}</span>'


def plain(lang: str, verdict) -> str:
    return t(lang, f"plain_{verdict}") if verdict in VERDICT_KEY else t(lang, "plain_none")


def title_of(lang: str, h: dict) -> str:
    return sub(lang, "titles", h["id"], h["title"])


def fmt_monitor(m: dict) -> str:
    if m["value"] is None:
        return "—"
    try:
        return m["format"].format(m["value"])
    except (ValueError, KeyError):
        return f"{m['value']:.4g}"


def page(*, lang: str, hid: str | None, base: str, title: str, description: str, body: str, charts: dict,
         jsonld: list, verification: str = "") -> str:
    root = asset_root(lang, hid)
    canonical = page_url(base, lang, hid)
    hl, locale = LANGS[lang][1], LANGS[lang][2]
    alternates = "".join(f'<link rel="alternate" hreflang="{LANGS[c][1]}" href="{e(page_url(base, c, hid))}">'
                         for c in LANGS)
    alternates += f'<link rel="alternate" hreflang="x-default" href="{e(page_url(base, DEFAULT, hid))}">'
    og_alt = "".join(f'<meta property="og:locale:alternate" content="{LANGS[c][2]}">' for c in LANGS if c != lang)
    meta_verify = f'<meta name="google-site-verification" content="{e(verification)}">' if verification else ""
    og_image = base + "og.png"
    scripts = ""
    if charts:
        scripts = (f'<script type="application/json" id="chart-data">{_safe_json(charts)}</script>'
                   f'<script src="{CHART_JS}" defer></script><script defer src="{root}charts.js"></script>')
    ld = "".join('<script type="application/ld+json">' + _safe_json(j) + "</script>" for j in jsonld)
    return f"""<!doctype html>
<html lang="{hl}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{e(canonical)}">
{alternates}
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#0d1117" media="(prefers-color-scheme: dark)">
<meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)">
<meta name="color-scheme" content="dark light">
{meta_verify}
<meta property="og:type" content="{'article' if hid else 'website'}">
<meta property="og:site_name" content="Crypto Research Labs">
<meta property="og:locale" content="{locale}">{og_alt}
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{e(canonical)}">
<meta property="og:image" content="{e(og_image)}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(description)}">
<meta name="twitter:image" content="{e(og_image)}">
<link rel="icon" href="{root}favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://cdnjs.cloudflare.com" crossorigin>
<style>{CSS}</style>
{ld}
</head>
<body>
{body}
{scripts}
</body>
</html>
"""


def header(lang: str, hid: str | None, generated: str) -> str:
    home = asset_root(lang, hid) + ("" if lang == DEFAULT else f"{lang}/") if hid else ""
    home = home or "./"
    # links to the same page in every language, relative to the current page
    up = asset_root(lang, hid)
    langs = []
    for c, (name, hl, _) in LANGS.items():
        target = up + page_path(c, hid).replace("index.html", "")
        target = target or "./"
        cur = ' aria-current="page"' if c == lang else ""
        langs.append(f'<a href="{e(target)}" hreflang="{hl}" lang="{hl}"{cur}>{e(name)}</a>')
    return f"""<header>
<nav aria-label="{e(t(lang, 'nav_dashboard'))}"><a href="{home}">{e(t(lang, 'nav_dashboard'))}</a>
<a href="{home}#how-to-read">{e(t(lang, 'nav_new'))}</a><a href="{home}#regime">{e(t(lang, 'nav_regime'))}</a>
<a href="{home}#hypotheses">{e(t(lang, 'nav_hyp'))}</a><a href="{home}#glossary">{e(t(lang, 'nav_glossary'))}</a>
<a href="{home}#methodology">{e(t(lang, 'nav_method'))}</a><a href="{REPO}">GitHub</a></nav>
<nav class="langs" aria-label="{e(t(lang, 'lang_label'))}">{''.join(langs)}</nav>
<p class="meta">{e(t(lang, 'updated', t=generated))}</p>
</header>"""


def footer(lang: str, hid: str | None) -> str:
    return f"""<footer>
<p>{t(lang, 'footer_disclaimer')}</p>
<p>{e(t(lang, 'footer_source'))}: <a href="{REPO}">{REPO}</a> · MIT License ·
<a href="{asset_root(lang, hid)}data.json">{e(t(lang, 'footer_data'))}</a></p>
</footer>"""


def results_table(lang: str, rows: list[dict], kind: str) -> str:
    if not rows:
        return f"<p>{e(t(lang, 'no_results'))}</p>"
    rule_col = kind == "rule_search"
    cols = ["c_asset", "c_period"] + (["c_rule"] if rule_col else []) + [
        "c_sharpe", "c_hsharpe", "c_cagr", "c_hcagr", "c_dd", "c_hdd", "c_exp", "c_p", "c_beats", "c_win"]
    head = "<tr>" + "".join(f"<th>{e(t(lang, c))}</th>" for c in cols) + "</tr>"
    yes, no = f"<span class=yes>{e(t(lang, 'yes'))}</span>", f"<span class=no>{e(t(lang, 'no'))}</span>"
    body = []
    for r in rows:
        p = "—" if r.get("p") is None else f"{r['p']:.3f}"
        body.append(
            f"<tr><td>{e(r.get('symbol'))}</td><td>{e(r.get('period'))} ({e(r.get('start'))} → {e(r.get('end'))})</td>"
            + (f"<td>{e(r.get('selected'))}</td>" if rule_col else "")
            + f"<td class=num>{num(r.get('sharpe'))}</td><td class=num>{num(r.get('hold_sharpe'))}</td>"
            f"<td class=num>{pct(r.get('cagr'), True)}</td><td class=num>{pct(r.get('hold_cagr'), True)}</td>"
            f"<td class=num>{pct(r.get('max_dd'))}</td><td class=num>{pct(r.get('hold_max_dd'))}</td>"
            f"<td class=num>{pct(r.get('exposure'), nd=0)}</td><td class=num>{p}</td>"
            f"<td>{yes if r.get('beats_hold') else no}</td><td>{yes if r.get('win') else no}</td></tr>")
    return f'<div class="table-wrap"><table><thead>{head}</thead><tbody>{"".join(body)}</tbody></table></div>'


def _badges(lang: str) -> dict:
    return {"pass": badge(lang, "PASS"), "weak": badge(lang, "WEAK"), "fail": badge(lang, "FAIL")}


def index_page(lang: str, data: dict, base: str, verification: str = "") -> str:
    hyps, reg = data["hypotheses"], data["regime"]
    n, n_pass = len(hyps), sum(h["verdict"] == "PASS" for h in hyps)
    verdict_line = t(lang, "verdict_some", p=n_pass, n=n) if n_pass else t(lang, "verdict_none", n=n)
    b = _badges(lang)
    charts, cards = {}, []
    for m in reg:
        label, explain = sub(lang, "monitors", m["id"], (m["label"], m.get("explain", "")))
        band = sub(lang, "bands", m["band"], m["band"])
        note = sub(lang, "notes", (m["id"], m["band"]), m.get("note", ""))
        key = f"spark-{m['id']}"
        if m.get("history") and m["history"]["v"]:
            charts[key] = {"d": m["history"]["d"], "series": [{"label": label, "v": m["history"]["v"]}], "spark": True}
        spark = (f'<div class="spark"><canvas data-chart="{key}" role="img" aria-label="{e(label)}"></canvas></div>'
                 if key in charts else "")
        note_html = f'<p class="note">{e(note)}</p>' if note else ""
        err = f'<p class="note">{e(t(lang, "source_down"))}</p>' if m.get("error") else ""
        cards.append(f'<article class="card"><h3>{e(label)}</h3><p class="explain">{e(explain)}</p>'
                     f'<div class="value">{e(fmt_monitor(m))}</div><span class="band">{e(band)}</span>'
                     f'{note_html}{err}{spark}</article>')

    btc = ""
    if data.get("btc"):
        bt = data["btc"]
        charts["btc"] = {"d": bt["close"]["d"], "log": True,
                         "series": [{"label": t(lang, "btc_close"), "v": bt["close"]["v"]},
                                    {"label": t(lang, "sma200"), "v": bt["sma200"]["v"], "dash": [6, 4]}]}
        last, sma = bt["close"]["v"][-1], bt["sma200"]["v"][-1]
        text = t(lang, "btc_text", price=f"${last:,.0f}", date=bt["close"]["d"][-1], diff=pct(last / sma - 1, True),
                 sma=f"${sma:,.0f}")
        btc = (f'<section aria-labelledby="btc"><h2 id="btc">{e(t(lang, "btc_title"))}</h2><p>{text}</p>'
               f'<div class="chart"><canvas data-chart="btc" role="img" aria-label="{e(t(lang, "btc_title"))}">'
               f'</canvas></div></section>')

    rows = []
    for h in hyps:
        when = (h.get("run_at") or "")[:10] or (h["history"][-1]["date"] if h["history"] else "")
        href = f'hypotheses/{e(h["id"])}.html'
        rows.append(f'<tr><td><a href="{href}">{e(h["id"])}</a></td><td><a href="{href}">{e(title_of(lang, h))}</a></td>'
                    f'<td>{e(sub(lang, "families", h["family"], h["family"]))}</td><td>{badge(lang, h["verdict"])}</td>'
                    f'<td>{e(plain(lang, h["verdict"]))}</td><td class=num>{e(when)}</td></tr>')

    fresh = "".join(f'<tr><td>{e(d["series"])}</td><td class=num>{e(d.get("first") or "—")}</td>'
                    f'<td class=num>{e(d.get("last") or "—")}</td>'
                    f'<td class=num>{"—" if d.get("lag_days") is None else d["lag_days"]}</td></tr>'
                    for d in data["data"])
    how = "".join(f"<li>{s.format(**b)}</li>" for s in t(lang, "how"))
    method = "".join(f"<li>{s}</li>" for s in t(lang, "method"))
    glossary = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in t(lang, "glossary"))

    body = f"""{header(lang, None, data['generated_at'])}
<main>
<h1>{e(t(lang, 'h1'))}</h1>
<p class="lead">{e(t(lang, 'lead', verdict=verdict_line))}</p>

<section aria-labelledby="how-to-read"><h2 id="how-to-read">{e(t(lang, 'how_title'))}</h2>
<ol class="steps">{how}</ol></section>

<section aria-labelledby="regime"><h2 id="regime">{e(t(lang, 'regime_title'))}</h2>
<p>{e(t(lang, 'regime_intro'))}</p>
<div class="cards">{''.join(cards)}</div></section>

{btc}

<section aria-labelledby="hypotheses"><h2 id="hypotheses">{e(t(lang, 'hyp_title'))}</h2>
<p>{t(lang, 'hyp_intro', **b)}</p>
<div class="table-wrap"><table><thead><tr><th>{e(t(lang, 'th_id'))}</th><th>{e(t(lang, 'th_hyp'))}</th>
<th>{e(t(lang, 'th_family'))}</th><th>{e(t(lang, 'th_verdict'))}</th><th>{e(t(lang, 'th_plain'))}</th>
<th>{e(t(lang, 'th_tested'))}</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div></section>

<section aria-labelledby="glossary"><h2 id="glossary">{e(t(lang, 'glossary_title'))}</h2>{glossary}</section>

<section aria-labelledby="methodology"><h2 id="methodology">{e(t(lang, 'method_title'))}</h2>
<ul>{method}</ul>
<p>{e(t(lang, 'method_more'))}: <a href="{REPO}/blob/main/docs/METHODOLOGY.md">METHODOLOGY.md</a>
· <a href="{REPO}/blob/main/docs/FINDINGS.md">FINDINGS.md</a></p></section>

<section aria-labelledby="data"><h2 id="data">{e(t(lang, 'data_title'))}</h2>
<div class="table-wrap"><table><thead><tr><th>{e(t(lang, 'th_series'))}</th><th>{e(t(lang, 'th_from'))}</th>
<th>{e(t(lang, 'th_last'))}</th><th>{e(t(lang, 'th_behind'))}</th></tr></thead><tbody>{fresh}</tbody></table></div>
</section>
</main>
{footer(lang, None)}"""

    url = page_url(base, lang)
    description = t(lang, "site_desc", verdict=verdict_line)
    jsonld = [
        {"@context": "https://schema.org", "@type": "WebSite", "name": "Crypto Research Labs", "url": url,
         "description": description, "inLanguage": LANGS[lang][1]},
        {"@context": "https://schema.org", "@type": "Dataset", "name": "Crypto Research Labs hypothesis results",
         "description": "Pre-registered backtests of crypto trading hypotheses on Binance daily data, with "
                        "out-of-sample statistics, significance tests and verdicts, updated automatically.",
         "url": url, "license": "https://opensource.org/licenses/MIT", "isAccessibleForFree": True,
         "creator": {"@type": "Person", "name": "F1DevBin", "url": "https://github.com/f1devbin"},
         "dateModified": data["generated_at"][:10],
         "keywords": ["cryptocurrency", "bitcoin", "backtesting", "trend following", "funding rate",
                      "pre-registration", "quantitative research"],
         "distribution": [{"@type": "DataDownload", "encodingFormat": "application/json",
                           "contentUrl": base + "data.json"}]},
        {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": LANGS[lang][1], "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in t(lang, "glossary")]},
    ]
    return page(lang=lang, hid=None, base=base, title=t(lang, "site_title"), description=description[:320],
                body=body, charts=charts, jsonld=jsonld, verification=verification)


def spec_text(spec: dict) -> str:
    import yaml
    return yaml.safe_dump(spec, sort_keys=False, allow_unicode=True)


def hypothesis_page(lang: str, h: dict, data: dict, base: str, verification: str = "") -> str:
    hid = h["id"]
    title = title_of(lang, h)
    charts, curve_block = {}, ""
    if h["curves"]:
        opts = []
        for i, c in enumerate(h["curves"]):
            key = f"c{i}"
            label = f"{c['symbol']} · {c['period']}" + (f" · {c['rule']}" if c.get("rule") else "")
            charts[key] = {"d": c["d"], "log": True,
                           "series": [{"label": t(lang, "strategy"), "v": c["strategy"], "width": 2.5},
                                      {"label": t(lang, "hold"), "v": c["hold"], "dash": [6, 4]}]}
            opts.append(f'<option value="{key}">{e(label)}</option>')
        curve_block = (f'<h2 id="equity">{e(t(lang, "equity_h"))}</h2><p>{e(t(lang, "equity_note"))}</p>'
                       f'<label>{e(t(lang, "select_label"))}: <select id="curve-select">{"".join(opts)}</select></label>'
                       f'<div class="chart"><canvas id="curve" role="img" aria-label="{e(t(lang, "equity_h"))}">'
                       f'</canvas></div>')
    history = "".join(f"<li>{e(x['date'])}: {badge(lang, x['verdict'])} ({e(x.get('source') or '')})</li>"
                      for x in h["history"])
    engine = (f"<li>{e((h.get('run_at') or '')[:10])}: {badge(lang, h['verdict'])} "
              f"({e(t(lang, 'engine_src', d=h.get('data_end') or ''))})</li>" if h.get("run_at") else "")
    spec = f"<h2>{e(t(lang, 'spec_h'))}</h2><pre lang=\"en\">{e(spec_text(h['spec']))}</pre>" if h.get("spec") else ""
    caution = f'<p class="callout">{e(t(lang, "caution"))}</p>' if h["verdict"] == "PASS" else ""
    en_note = "" if lang == DEFAULT else f'<p class="meta">{e(t(lang, "en_note"))}</p>'
    body = f"""{header(lang, hid, data['generated_at'])}
<main>
<p class="meta"><a href="../#hypotheses">{e(t(lang, 'back'))}</a></p>
<h1>{e(hid)}: {e(title)}</h1>
<p>{badge(lang, h['verdict'])} &nbsp;{e(t(lang, 'family'))}: <strong>{e(sub(lang, 'families', h['family'], h['family']))}</strong>
· {e(t(lang, 'status'))}: <strong>{e(sub(lang, 'statuses', h['status'], h['status']))}</strong></p>
{caution}
<p class="plain"><strong>{e(t(lang, 'in_plain'))}:</strong> {e(plain(lang, h['verdict']))}</p>
<h2>{e(t(lang, 'result_h'))}</h2>
{en_note}
<p lang="en">{e(h['summary'])}</p>
<p class="meta">{e(t(lang, 'metrics_note'))} <a href="../#glossary">{e(t(lang, 'nav_glossary'))}</a></p>
{results_table(lang, h['rows'], (h.get('spec') or {}).get('kind', ''))}
{curve_block}
<h2>{e(t(lang, 'why_h'))}</h2><p lang="en">{e(h['rationale'])}</p>
<h2>{e(t(lang, 'history_h'))}</h2><ul>{history}{engine}</ul>
{spec}
</main>
{footer(lang, hid)}"""
    url = page_url(base, lang, hid)
    description = t(lang, "hyp_desc", id=hid, verdict=verdict_word(lang, h["verdict"]), title=title,
                    plain=plain(lang, h["verdict"]))
    jsonld = [{"@context": "https://schema.org", "@type": "TechArticle", "headline": f"{hid}: {title}"[:110],
               "description": description[:300], "url": url, "inLanguage": LANGS[lang][1],
               "dateModified": (h.get("run_at") or data["generated_at"])[:10],
               "author": {"@type": "Person", "name": "F1DevBin", "url": "https://github.com/f1devbin"},
               "image": base + "og.png",
               "isPartOf": {"@type": "WebSite", "name": "Crypto Research Labs", "url": page_url(base, lang)}},
              {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                  {"@type": "ListItem", "position": 1, "name": "Crypto Research Labs", "item": page_url(base, lang)},
                  {"@type": "ListItem", "position": 2, "name": hid, "item": url}]}]
    return page(lang=lang, hid=hid, base=base, title=f"{hid}: {title} | Crypto Research Labs",
                description=description[:320], body=body, charts=charts, jsonld=jsonld, verification=verification)


def sitemap(base: str, entries: list[tuple[str | None, str]]) -> str:
    """entries: (hypothesis id or None for the home page, lastmod). Each URL lists all its language versions."""
    out = []
    for hid, lastmod in entries:
        alts = "".join(f'<xhtml:link rel="alternate" hreflang="{LANGS[c][1]}" href="{e(page_url(base, c, hid))}"/>'
                       for c in LANGS)
        alts += f'<xhtml:link rel="alternate" hreflang="x-default" href="{e(page_url(base, DEFAULT, hid))}"/>'
        for c in LANGS:
            out.append(f"<url><loc>{e(page_url(base, c, hid))}</loc><lastmod>{e(lastmod)}</lastmod>{alts}</url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            'xmlns:xhtml="http://www.w3.org/1999/xhtml">' + "".join(out) + "</urlset>\n")


FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" '
           'fill="#0d1117"/><path d="M10 46 L24 30 L34 38 L54 16" fill="none" stroke="#58a6ff" stroke-width="6" '
           'stroke-linecap="round" stroke-linejoin="round"/><circle cx="54" cy="16" r="5" fill="#2ea043"/></svg>')

NOT_FOUND = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport"
content="width=device-width, initial-scale=1"><meta name="robots" content="noindex"><title>Page not found |
Crypto Research Labs</title><style>body{background:#0d1117;color:#fff;font:18px/1.6 system-ui,sans-serif;
max-width:700px;margin:60px auto;padding:0 16px}a{color:#79c0ff}</style></head><body><h1>Page not found</h1>
<p><a href="/Crypto-Research-Labs/">Go to the Crypto Research Labs dashboard</a></p></body></html>
"""

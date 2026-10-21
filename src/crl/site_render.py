"""HTML for the static dashboard, one prerendered copy per language.

Every number and every word is rendered server-side so search engines and readers without
JavaScript see the full content; JavaScript only draws the charts. English lives at the site
root (x-default), other languages under /<lang>/, linked with hreflang.
"""
import html
import json
import re

from crl import course as C
from crl import setup_guide as SG
from crl.i18n import DEFAULT, LANGS, sub, t

CHART_JS = "https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"
VERDICT_CLASS = {"PASS": "pass", "WEAK": "weak", "FAIL": "fail"}
VERDICT_KEY = {"PASS": "Pass", "WEAK": "Weak", "FAIL": "Fail"}
REPO = "https://github.com/f1devbin/Crypto-Research-Labs"
# coin-page rule -> hypotheses that tested it
SIGNAL_STUDIES_R = {"sma50": ["H-005", "H-018"], "mom7": ["H-014"], "vol": ["H-012", "H-013"], "btc": ["H-017", "H-019"]}

CSS = """
:root{--bg:#0f1b2d;--panel:#15243b;--raised:#1b2e4a;--line:#2f4568;--text:#ffffff;--text2:#e3eaf5;
--link:#8ccbff;--accent:#7cc4ff;--pass:#46c281;--weak:#f0b44c;--fail:#ff6b73;--hold:#e3eaf5;--ink:#0f1b2d}
@media (prefers-color-scheme:light){:root{--bg:#f5f8fc;--panel:#ffffff;--raised:#eaf0f8;--line:#c3cfdf;
--text:#08111f;--text2:#1c293b;--link:#0a58a8;--accent:#0a58a8;--pass:#127a43;--weak:#8a5a00;--fail:#b4232f;
--hold:#1c293b;--ink:#ffffff}}
*{box-sizing:border-box}
html{font-size:18px;-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--text);
font:1rem/1.6 "IBM Plex Sans",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;font-variant-numeric:tabular-nums}
a{color:var(--link);text-underline-offset:.18em;text-decoration-thickness:1px}
a:hover{text-decoration-thickness:2px}
main,footer,.bar{max-width:1120px;margin:0 auto;padding:0 20px}
/* header: brand row + section nav + languages */
.site-head{background:var(--panel);border-bottom:1px solid var(--line);margin-bottom:28px}
.bar{display:flex;flex-wrap:wrap;align-items:center;gap:8px 24px;padding-top:14px;padding-bottom:14px}
.brand{display:flex;align-items:center;gap:10px;color:var(--text);text-decoration:none;font-weight:700;font-size:1.08rem;letter-spacing:-.01em}
.brand svg{width:30px;height:30px;flex:none}
.updated{margin-left:auto;color:var(--text2);font-size:.85rem}
nav.sections{display:flex;flex-wrap:wrap;gap:4px;padding-top:0;padding-bottom:10px;margin-left:auto;margin-right:auto}
nav.sections a:first-child{margin-left:-12px}
nav.sections a{color:var(--text);text-decoration:none;font-weight:500;font-size:.92rem;padding:5px 12px;border-radius:999px;border:1px solid transparent}
nav.sections a:hover{border-color:var(--line);background:var(--raised)}
nav.langs{display:flex;flex-wrap:wrap;gap:2px 14px;font-size:.85rem;padding-top:0;padding-bottom:14px}
nav.langs a{color:var(--text2);text-decoration:none}
nav.langs a[aria-current]{color:var(--text);font-weight:700;text-decoration:underline;text-underline-offset:.3em}
h1{font-size:2.3rem;line-height:1.15;letter-spacing:-.02em;font-weight:700;margin:.1em 0 .35em;max-width:26ch}
h2{font-size:1.5rem;line-height:1.25;letter-spacing:-.01em;font-weight:600;margin:2.4em 0 .7em;padding-bottom:.35em;border-bottom:1px solid var(--line)}
h3{font-size:1.08rem;font-weight:600;margin:0 0 .3em}
p,li{color:var(--text2)}
main p{max-width:78ch}
.lead{font-size:1.15rem;max-width:64ch}
.meta{color:var(--text2);font-size:.9rem}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px}
.card{overflow-wrap:anywhere;background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px 18px}
.card h3{font-size:1rem}
.value{font-size:2rem;font-weight:600;letter-spacing:-.02em;line-height:1.15;margin:.2em 0}
.band{display:inline-block;border:1px solid var(--text2);border-radius:999px;padding:0 10px;font-weight:600;font-size:.82rem}
.note{font-size:.9rem;margin:.5em 0 0}
.explain{font-size:.9rem;margin:.2em 0 .4em}
.plain{font-size:1.05rem;border-left:4px solid var(--accent);background:var(--panel);padding:12px 16px;border-radius:0 10px 10px 0}
.steps{counter-reset:s;list-style:none;padding:0}
.steps li{counter-increment:s;margin:.5em 0;padding-left:2.4em;position:relative}
.steps li::before{content:counter(s);position:absolute;left:0;top:.1em;width:1.6em;height:1.6em;border-radius:50%;
background:var(--accent);color:var(--ink);font-weight:700;text-align:center;line-height:1.6em;font-size:.9rem}
.flow{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:12px 0}
.flow-step{border:1px solid var(--accent);border-radius:10px;padding:10px 14px;font-weight:600;background:var(--panel)}
.flow-arrow{font-size:1.5rem;font-weight:700;color:var(--accent)}
.beginner{display:inline-block;background:var(--pass);color:var(--ink);font-weight:700;border-radius:999px;padding:2px 12px}
.course-cta{display:flex;align-items:center;gap:10px;border:1px solid var(--pass);border-radius:12px;padding:14px 18px;margin:16px 0;
font-weight:600;background:var(--panel);text-decoration:none;color:var(--text)}
.course-cta:hover{background:var(--raised)}
ul.tasks{list-style:none;padding-left:0}ul.tasks li{margin:.35em 0}ul.tasks input{width:1.1em;height:1.1em;vertical-align:-2px}
.toc{columns:2;column-gap:32px}@media (max-width:640px){.toc{columns:1}}
details{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:10px 16px;margin:8px 0}
summary{cursor:pointer;font-weight:600;color:var(--text)}
canvas{max-width:100%}
.chart{position:relative;width:100%;height:320px;margin:8px 0;background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:12px}
.spark{position:relative;width:100%;height:80px;margin-top:10px}
/* tables */
.table-wrap{overflow-x:auto;border:1px solid var(--line);border-radius:14px;background:var(--panel)}
table{border-collapse:collapse;width:100%;font-size:.94rem}
th,td{text-align:left;padding:10px 12px;border-bottom:1px solid var(--line);vertical-align:top}
tbody tr:last-child td{border-bottom:0}
th{background:var(--raised);color:var(--text);vertical-align:bottom;line-height:1.25;font-size:.84rem;font-weight:600;hyphens:auto}
tbody tr:hover td{background:color-mix(in srgb,var(--raised) 60%,transparent)}
td{color:var(--text2)}
th.num,td.num{text-align:right;white-space:nowrap}
.sub{display:block;font-size:.84rem;color:var(--text2);font-weight:400;margin-top:1px}
a .sub{text-decoration:none}
.badge{display:inline-block;min-width:4.4em;text-align:center;border-radius:999px;padding:1px 10px;font-weight:700;font-size:.85rem;color:var(--ink)}
.badge.pass{background:var(--pass)}.badge.weak{background:var(--weak)}.badge.fail{background:var(--fail)}
.badge.none{background:transparent;color:var(--text);border:1px solid var(--line)}
.yes{color:var(--pass);font-weight:700}.no{color:var(--text2)}
pre{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:14px;overflow-x:auto;font-size:.86rem;color:var(--text)}
.callout{border-left:4px solid var(--weak);background:var(--panel);padding:12px 16px;border-radius:0 10px 10px 0}
select{font:inherit;padding:6px 10px;background:var(--panel);color:var(--text);border:1px solid var(--line);border-radius:8px}
footer{margin-top:64px;padding-top:20px;padding-bottom:48px;border-top:1px solid var(--line);font-size:.9rem}
code{background:var(--raised);border:1px solid var(--line);border-radius:5px;padding:0 5px;font-size:.9em;overflow-wrap:anywhere}
:focus-visible{outline:3px solid var(--accent);outline-offset:2px;border-radius:4px}
/* diagnosis: the one loud element on the page */
.diag{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:20px 24px;margin:20px 0 8px;position:relative;overflow:hidden}
.diag::before{content:"";position:absolute;inset:0 auto 0 0;width:6px;background:var(--weak)}
.diag.up::before{background:var(--pass)}.diag.down::before{background:var(--fail)}
.diag h2{border:0;margin:0 0 .2em;padding:0;font-size:1rem;font-weight:600;color:var(--text2)}
.diag-head{font-size:1.6rem;line-height:1.25;font-weight:600;letter-spacing:-.015em;color:var(--text);margin:.1em 0 .5em;max-width:32ch}
.meter{display:flex;height:10px;border-radius:999px;overflow:hidden;background:var(--raised);max-width:420px;margin:.2em 0 .4em}
.meter i{display:block}.meter .m-up{background:var(--pass)}.meter .m-0{background:var(--line)}.meter .m-down{background:var(--fail)}
ul.diag-list{list-style:none;padding-left:0;margin:.8em 0;display:grid;gap:8px}
ul.diag-list li{margin:0;padding-left:1.9em;position:relative;max-width:80ch}
ul.diag-list li::before{position:absolute;left:0;top:.05em;font-weight:700;width:1.3em;text-align:center}
li.t-up::before{content:"▲";color:var(--pass)}li.t-down::before{content:"▼";color:var(--fail)}li.t-0::before{content:"●";color:var(--text2);font-size:.8em;top:.25em}
.diag h3{margin-top:1em}
/* rule x coin matrix: chips */
td.sc{text-align:center;vertical-align:middle;padding:6px 3px}
.chip{display:inline-flex;align-items:center;justify-content:center;width:2.1em;height:1.75em;border-radius:7px;font-weight:700;font-size:.9rem;position:relative}
.works .chip{background:var(--pass);color:var(--ink)}
.better .chip{background:color-mix(in srgb,var(--weak) 22%,transparent);color:var(--weak);border:1px solid var(--weak)}
.worse .chip{color:var(--text2);border:1px solid var(--line)}
.nodata .chip{color:var(--text2);border:1px dashed var(--line)}
.legend .official .chip{border:1px solid var(--line)}
.official .chip::after{content:"";position:absolute;bottom:-6px;left:50%;width:6px;height:6px;margin-left:-3px;border-radius:50%;background:var(--accent)}
.legend{display:flex;flex-wrap:wrap;gap:6px 20px;font-size:.9rem;margin:.6em 0;align-items:center;padding:0}
.legend li{list-style:none;display:flex;align-items:center;gap:8px}
.legend .sc{display:inline-flex;padding:0}
table.matrix th{font-size:.8rem;text-align:center;padding:10px 3px}
table.matrix th:first-child,table.matrix td:first-child{text-align:left;min-width:10em;max-width:15em;position:sticky;left:0;z-index:1;background:var(--panel)}
table.matrix th:first-child{background:var(--raised)}
table.matrix td{padding-bottom:12px}
table.sortable th{cursor:pointer;user-select:none}table.sortable th:hover{color:var(--accent)}
table.sortable th[aria-sort=ascending]::after{content:" ▲"}table.sortable th[aria-sort=descending]::after{content:" ▼"}
.progress{height:10px;background:var(--raised);border-radius:999px;overflow:hidden;max-width:420px;margin:.4em 0}
.progress span{display:block;height:100%;background:var(--accent);border-radius:999px}
td .progress{min-width:110px;margin:.5em 0 .2em}
/* phones: data tables become labelled cards, the matrix becomes one chip grid per rule */
@media (max-width:760px){
html{font-size:16px}
main,footer,.bar{padding:0 14px}
.bar{padding-top:12px;padding-bottom:10px}.updated{margin-left:0;width:100%}
nav.sections{overflow-x:auto;flex-wrap:nowrap;scrollbar-width:none;padding:0 14px 10px}nav.sections a:first-child{margin-left:0}
nav.sections a{white-space:nowrap;border-color:var(--line)}
nav.langs{padding:0 14px 12px}
h1{font-size:1.75rem}
h2{font-size:1.3rem}
.diag{padding:16px 16px 16px 20px}.diag-head{font-size:1.3rem}
.table-wrap:has(table.rt),.table-wrap:has(table.matrix){border:0;overflow:visible;background:none}
table.rt thead,table.matrix thead,.sort-hint{display:none}
table.rt,table.rt tbody,table.rt tr,table.matrix,table.matrix tbody{display:block;width:100%}
table.rt tr{background:var(--panel);border:1px solid var(--line);border-radius:12px;margin:0 0 10px;padding:6px 0}
table.rt td{display:flex;justify-content:space-between;align-items:baseline;gap:14px;border:0;padding:4px 14px;text-align:right;white-space:normal}
table.rt td::before{content:attr(data-label);font-weight:600;color:var(--text);text-align:left;flex:0 1 auto;font-size:.9rem}
table.rt td:first-child{display:block;text-align:left;font-size:1.05rem;padding-bottom:8px;border-bottom:1px solid var(--line);margin-bottom:4px}
table.rt td:first-child::before{content:none}
tbody tr:hover td{background:none}
table.matrix tr{display:grid;grid-template-columns:repeat(auto-fill,minmax(54px,1fr));gap:10px 4px;background:var(--panel);
border:1px solid var(--line);border-radius:12px;margin:0 0 10px;padding:12px}
table.matrix td{border:0;padding:0}
table.matrix td:first-child{grid-column:1/-1;position:static;max-width:none;background:none;padding-bottom:4px}
table.matrix td.sc{display:flex;flex-direction:column;align-items:center;gap:3px}
table.matrix td.sc::before{content:attr(data-label);font-size:.75rem;font-weight:600;color:var(--text2)}
}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
"""

# sorts any <table class="sortable"> by the clicked column; cells may carry data-v with the raw value
SORT_SCRIPT = """
(function(){
function val(td){var v=td.getAttribute('data-v');if(v===null)v=td.textContent.trim();
 if(v===''||v==='—')return null;var n=parseFloat(v.replace(/[$,%+\\s]/g,'').replace('−','-'));return isNaN(n)?v.toLowerCase():n}
document.querySelectorAll('table.sortable').forEach(function(t){
 var ths=t.tHead?t.tHead.rows[0].cells:[];
 Array.prototype.forEach.call(ths,function(th,i){th.tabIndex=0;th.title=t.dataset.hint||'';
  function go(){var asc=th.getAttribute('aria-sort')!=='ascending';
   Array.prototype.forEach.call(ths,function(o){o.removeAttribute('aria-sort')});
   th.setAttribute('aria-sort',asc?'ascending':'descending');
   var b=t.tBodies[0],rows=Array.prototype.slice.call(b.rows);
   rows.sort(function(x,y){var a=val(x.cells[i]),c=val(y.cells[i]);
    if(a===null)return 1;if(c===null)return -1;
    var r=(typeof a==='number'&&typeof c==='number')?a-c:String(a).localeCompare(String(c));return asc?r:-r});
   rows.forEach(function(r){b.appendChild(r)})}
  th.addEventListener('click',go);th.addEventListener('keydown',function(ev){if(ev.key==='Enter'||ev.key===' '){ev.preventDefault();go()}});
 })})
})();
"""

# draws every <canvas data-chart="key"> from the JSON in #chart-data
CHART_SCRIPT = """
(function(){
var el=document.getElementById('chart-data');if(!el||!window.Chart)return;
var D=JSON.parse(el.textContent),css=getComputedStyle(document.documentElement);
function c(n){return css.getPropertyValue(n).trim()}
Chart.defaults.color=c('--text');Chart.defaults.borderColor=c('--line');
Chart.defaults.font.size=14;Chart.defaults.font.family='"IBM Plex Sans",system-ui,sans-serif';Chart.defaults.animation=false;
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


def price(v) -> str:
    if v is None:
        return "—"
    if v >= 1000:
        return f"${v:,.0f}"
    if v >= 1:
        return f"${v:,.2f}"
    return f"${v:.4g}"


def usd(v) -> str:
    return "—" if v is None else f"${v:,.0f}"


def pct(v, signed=False, nd=1) -> str:
    if v is None:
        return "—"
    return f"{v:+.{nd}%}" if signed else f"{v:.{nd}%}"


def num(v, nd=2) -> str:
    return "—" if v is None else f"{v:.{nd}f}"


def _rel(key: str | None) -> str:
    """Page key -> path inside a language root: None = home, "coin:SOLUSDT", or a hypothesis id."""
    if key is None:
        return ""
    if key in ("course", "setup"):
        return f"{key}.html"
    if key.startswith("coin:"):
        return f"coins/{key[5:]}.html"
    return f"hypotheses/{key}.html"


def page_url(base: str, lang: str, hid: str | None = None) -> str:
    root = base if lang == DEFAULT else f"{base}{lang}/"
    return root + _rel(hid)


def page_path(lang: str, hid: str | None = None) -> str:
    """Path of a page relative to the site root."""
    root = "" if lang == DEFAULT else f"{lang}/"
    return root + (_rel(hid) or "index.html")


def asset_root(lang: str, hid: str | None = None) -> str:
    depth = (lang != DEFAULT) + (hid is not None and hid not in ("course", "setup"))
    return "../" * depth


def verdict_word(lang: str, verdict) -> str:
    return t(lang, VERDICT_KEY[verdict]) if verdict in VERDICT_KEY else "—"


def badge(lang: str, verdict) -> str:
    if not verdict:
        return '<span class="badge none">—</span>'
    return f'<span class="badge {VERDICT_CLASS.get(verdict, "none")}">{e(verdict_word(lang, verdict))}</span>'


def plain(lang: str, verdict, test_after=None) -> str:
    if verdict in VERDICT_KEY:
        return t(lang, f"plain_{verdict}")
    return t(lang, "plain_scheduled", date=test_after) if test_after else t(lang, "plain_none")


def title_of(lang: str, h: dict) -> str:
    return sub(lang, "titles", h["id"], h["title"])


def fmt_monitor(m: dict) -> str:
    if m["value"] is None:
        return "—"
    try:
        return m["format"].format(m["value"])
    except (ValueError, KeyError):
        return f"{m['value']:.4g}"


_TABLE = re.compile(r"<table([^>]*)>(.*?)</table>", re.S)
_TAG = re.compile(r"<[^>]+>")


def responsive_tables(body: str) -> str:
    """Give every data table (one with a header row) the class `rt` and copy each column header
    into its cells as data-label, so on a phone the CSS shows each row as a labelled card."""
    def fix(m):
        attrs, inner = m.group(1), m.group(2)
        if "matrix" in attrs or "<thead" not in inner:
            return m.group(0)
        head = inner.split("</thead>", 1)[0]
        labels = [html.unescape(_TAG.sub("", x)).strip() for x in re.findall(r"<th[^>]*>(.*?)</th>", head, re.S)]
        rest = inner.split("</thead>", 1)[1]

        def row(rm):
            i = iter(labels)
            return re.sub(r"<td(?=[\s>])", lambda _: f'<td data-label="{e(next(i, ""))}"', rm.group(0))
        rest = re.sub(r"<tr[^>]*>.*?</tr>", row, rest, flags=re.S)
        if "class=" in attrs:
            attrs = re.sub(r'class="([^"]*)"', r'class="\1 rt"', attrs, count=1)
        else:
            attrs += ' class="rt"'
        return f"<table{attrs}>{head}</thead>{rest}</table>"
    return _TABLE.sub(fix, body)


def page(*, lang: str, hid: str | None, base: str, title: str, description: str, body: str, charts: dict,
         jsonld: list, verification: str = "") -> str:
    body = responsive_tables(body)
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
    scripts += f'<script defer src="{root}sort.js"></script>'
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
<meta name="theme-color" content="#15243b" media="(prefers-color-scheme: dark)">
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
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&display=swap">
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
    return f"""<header class="site-head">
<div class="bar"><a class="brand" href="{home}">{LOGO}<span>Crypto Research Labs</span></a>
<span class="updated">{e(t(lang, 'updated', t=generated))}</span></div>
<nav class="sections bar" aria-label="{e(t(lang, 'nav_dashboard'))}"><a href="{home}">{e(t(lang, 'nav_dashboard'))}</a>
<a href="{home}course.html">{e(C.UI.get(lang, C.UI['en'])['nav'])}</a>
<a href="{home}#how-to-read">{e(t(lang, 'nav_new'))}</a><a href="{home}#regime">{e(t(lang, 'nav_regime'))}</a>
<a href="{home}#coins">{e(t(lang, 'nav_coins'))}</a><a href="{home}#hypotheses">{e(t(lang, 'nav_hyp'))}</a><a href="{home}#glossary">{e(t(lang, 'nav_glossary'))}</a>
<a href="{home}#methodology">{e(t(lang, 'nav_method'))}</a><a href="{home}setup.html">{e(SG.GUIDE.get(lang, SG.GUIDE['en'])['nav'])}</a><a href="{REPO}">GitHub</a></nav>
<nav class="langs bar" aria-label="{e(t(lang, 'lang_label'))}">{''.join(langs)}</nav>
</header>"""


def footer(lang: str, hid: str | None) -> str:
    return f"""<footer>
<p>{t(lang, 'footer_disclaimer')}</p>
<p>{e(t(lang, 'footer_source'))}: <a href="{REPO}">{REPO}</a> · MIT License ·
<a href="{asset_root(lang, hid)}data.json">{e(t(lang, 'footer_data'))}</a> ·
<a href="{asset_root(lang, hid)}{'' if lang == DEFAULT else lang + '/'}setup.html">{e(SG.GUIDE.get(lang, SG.GUIDE['en'])['nav'])}</a></p>
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


TONE_CLASS = {1: "t-up", -1: "t-down", 0: "t-0"}
SCAN_MARK = {"works": "✓", "better": "↑", "worse": "✗", "nodata": "·"}


def _diag_item(lang: str, it: dict) -> str:
    kw = {}
    if it["key"].startswith("d_trend") or it["key"].startswith("d_money"):
        kw["v"] = pct(it.get("v"), nd=1)
    elif it["key"].startswith("d_vol"):
        kw["v"] = pct(it.get("v"), nd=0)
    elif it["key"] == "d_mood":
        kw["v"] = f"{it['v']:.0f}"
        kw["band"] = sub(lang, "bands", it["band"], it["band"])
    elif it["key"].startswith("d_breadth"):
        kw = {"k": it["k"], "n": it["n"]}
    text = t(lang, it["key"], **kw)
    if it["key"] == "d_mood" and it["band"] in ("extreme_fear", "fear"):
        text += " " + t(lang, "d_mood_fear")
    elif it["key"] == "d_mood" and it["band"] in ("extreme_greed", "greed"):
        text += " " + t(lang, "d_mood_greed")
    return f'<li class="{TONE_CLASS[it["tone"]]}">{e(text)}</li>'


def diag_section(lang: str, data: dict) -> str:
    d = data.get("diagnosis")
    if not d:
        return ""
    items = "".join(_diag_item(lang, it) for it in d["items"])
    return (f'<section aria-labelledby="diagnosis" class="diag {d["level"]}"><h2 id="diagnosis">'
            f'{e(t(lang, "diag_title"))}</h2><p class="diag-head">{e(t(lang, "diag_level_" + d["level"]))}</p>'
            f'<div class="meter" role="img" aria-label="{e(t(lang, "diag_count", up=d["up"], down=d["down"], neutral=d["neutral"]))}">'
            f'<i class="m-up" style="width:{100 * d["up"] / max(d["up"] + d["neutral"] + d["down"], 1):.1f}%"></i>'
            f'<i class="m-0" style="width:{100 * d["neutral"] / max(d["up"] + d["neutral"] + d["down"], 1):.1f}%"></i>'
            f'<i class="m-down" style="width:{100 * d["down"] / max(d["up"] + d["neutral"] + d["down"], 1):.1f}%"></i></div>'
            f'<p class="meta">{e(t(lang, "diag_count", up=d["up"], down=d["down"], neutral=d["neutral"]))}</p>'
            f'<ul class="diag-list">{items}</ul>'
            f'<h3>{e(t(lang, "diag_means_h"))}</h3><p>{e(t(lang, "diag_means_" + d["level"]))}</p>'
            f'<p class="meta">{e(t(lang, "diag_intro"))} {e(t(lang, "diag_disclaimer"))}</p></section>')


def _scan_cells(data: dict) -> dict:
    sc = data.get("scan") or {}
    return {(c["rule"], c["symbol"]): c for c in sc.get("cells", [])}


def rule_label(lang: str, rid: str, hyps: dict) -> str:
    return sub(lang, "rule_short", rid) or (title_of(lang, hyps[rid]) if rid in hyps else rid)


def coin_diag(lang: str, c: dict, data: dict) -> str:
    out = []
    v50, v200 = c.get("vs50"), c.get("vs200")
    if v50 is not None and v200 is not None:
        key = ("cd_trend_up" if v50 > 0 else "cd_trend_pullback") if v200 > 0 else \
              ("cd_trend_turn" if v50 > 0 else "cd_trend_down")
        tone = {"cd_trend_up": 1, "cd_trend_down": -1}.get(key, 0)
        out.append((tone, t(lang, key)))
    elif v50 is not None:
        out.append((1 if v50 > 0 else -1, t(lang, "cd_trend_short_up" if v50 > 0 else "cd_trend_short_down")))
    dd = c.get("dd_peak")
    if dd is not None:
        if dd > -0.02:
            out.append((1, t(lang, "cd_atpeak", date=c.get("peak_date", ""))))
        else:
            need = 1 / (1 + dd) - 1
            out.append((-1 if dd < -0.5 else 0, t(lang, "cd_peak", dd=pct(dd, True, 0), date=c.get("peak_date", ""),
                                                  need=pct(need, False, 0) if need < 10 else f"{need + 1:,.0f}×")))
    btc = next((x for x in data.get("coins", []) if x["symbol"] == "BTCUSDT"), None)
    if c.get("vol"):
        if c["symbol"] == "BTCUSDT" or not btc or not btc.get("vol"):
            out.append((0, t(lang, "cd_vol_btc", v=pct(c["vol"], nd=0))))
        else:
            x = c["vol"] / btc["vol"]
            out.append((-1 if x >= 2 else 0, t(lang, "cd_vol", x=f"{x:.1f}")))
    if c.get("corr_btc") is not None:
        r = c["corr_btc"]
        key = "cd_corr_high" if r >= 0.7 else ("cd_corr_mid" if r >= 0.4 else "cd_corr_low")
        out.append((0, t(lang, key, c=f"{r:.2f}")))
    sc = data.get("scan")
    if sc:
        hyps = {h["id"]: h for h in data["hypotheses"]}
        mine = [x for x in sc["cells"] if x["symbol"] == c["symbol"] and x["status"] != "nodata"]
        works = [x["rule"] for x in mine if x["status"] == "works"]
        better = sum(x["status"] == "better" for x in mine)
        start = max(sc.get("start") or "", c.get("since") or "")
        if works:
            txt = t(lang, "cd_rules_works", start=start, rules="; ".join(rule_label(lang, r, hyps) for r in works))
            out.append((1, txt + (" " + t(lang, "cd_rules_better", k=better) if better else "")))
        elif mine:
            txt = t(lang, "cd_rules_none", n=len(mine), start=start)
            out.append((0, txt + (" " + t(lang, "cd_rules_better", k=better) if better else "")))
    if not out:
        return ""
    items = "".join(f'<li class="{TONE_CLASS[tone]}">{e(txt)}</li>' for tone, txt in out)
    lvl = {1: "up", -1: "down"}.get(out[0][0], "") if out else ""
    return (f'<section aria-labelledby="cdiag" class="diag {lvl}"><h2 id="cdiag">'
            f'{e(t(lang, "cdiag_title"))}</h2><ul class="diag-list">{items}</ul>'
            f'<p class="meta">{e(t(lang, "diag_disclaimer"))}</p></section>')


def _legend(lang: str) -> str:
    items = []
    for st in ("works", "better", "worse", "nodata"):
        word = t(lang, f"scan_{st}").split(" ", 1)[-1]
        items.append(f'<li><span class="sc {st}"><span class="chip">{SCAN_MARK[st]}</span></span>{e(word)}</li>')
    items.append(f'<li><span class="sc official"><span class="chip"></span></span>{e(t(lang, "scan_official"))}</li>')
    return '<ul class="legend">' + "".join(items) + "</ul>"


def scan_matrix(lang: str, data: dict) -> str:
    sc = data.get("scan")
    if not sc or not sc.get("cells"):
        return ""
    hyps = {h["id"]: h for h in data["hypotheses"]}
    cells = _scan_cells(data)
    coins = sc["coins"]
    head = "".join(f'<th><a href="coins/{e(s)}.html">{e(s.removesuffix("USDT"))}</a></th>' for s in coins)
    rows = []
    for r in sc["rules"]:
        tds = []
        for s in coins:
            c = cells.get((r["id"], s), {"status": "nodata"})
            tip = (f'{s.removesuffix("USDT")}: Sharpe {num(c.get("sharpe"))} / {num(c.get("hold_sharpe"))}'
                   if c.get("sharpe") is not None else s.removesuffix("USDT"))
            cls = f'sc {c["status"]}' + (" official" if c.get("official") else "")
            tds.append(f'<td class="{cls}" title="{e(tip)}" data-label="{e(s.removesuffix("USDT"))}">'
                       f'<span class="chip">{SCAN_MARK[c["status"]]}</span></td>')
        rows.append(f'<tr><td><a href="hypotheses/{e(r["id"])}.html">{e(r["id"])}</a><span class="sub">{e(rule_label(lang, r["id"], hyps))}</span></td>'
                    + "".join(tds) + "</tr>")
    n = sum(sc["counts"].get(k, 0) for k in ("works", "better", "worse"))
    counts = t(lang, "scan_counts", works=sc["counts"].get("works", 0), better=sc["counts"].get("better", 0),
               worse=sc["counts"].get("worse", 0), total=n)
    return (f'<section aria-labelledby="scan"><h2 id="scan">{e(t(lang, "scan_title"))}</h2>'
            f'<p>{e(t(lang, "scan_intro", start=sc["start"]))}</p>{_legend(lang)}<p class="meta">{e(counts)} · '
            f'{e((sc.get("generated_at") or "")[:10])}</p>'
            f'<div class="table-wrap"><table class="matrix"><thead><tr><th>{e(t(lang, "th_rule_short"))}</th>{head}</tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></div></section>')


def _scan_row(lang: str, c: dict, first: str) -> str:
    cls = f'sc {c["status"]}' + (" official" if c.get("official") else "")
    word = t(lang, f'scan_{c["status"]}').split(" ", 1)[-1]
    sh = c.get("sharpe")
    return (f"<tr><td>{first}</td><td class=\"{cls}\"><span class=\"chip\">{SCAN_MARK[c['status']]}</span></td><td>{e(word)}</td>"
            f'<td class=num data-v="{"" if sh is None else sh}">{num(sh)} / {num(c.get("hold_sharpe"))}</td>'
            f'<td class=num data-v="{"" if c.get("cagr") is None else c["cagr"]}">{pct(c.get("cagr"), True, 0)} / {pct(c.get("hold_cagr"), True, 0)}</td>'
            f'<td class=num>{e(c.get("start") or "—")}</td></tr>')


def _scan_table(lang: str, rows: list[str], first_head: str) -> str:
    return (f'<div class="table-wrap"><table class="sortable" data-hint="{e(t(lang, "sort_hint"))}"><thead><tr>'
            f'<th>{e(first_head)}</th><th>✓</th><th>{e(t(lang, "th_result"))}</th><th>{e(t(lang, "th_sharpe_pair"))}</th>'
            f'<th>CAGR</th><th>{e(t(lang, "th_from"))}</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>')


def scan_for_rule(lang: str, hid: str, data: dict) -> str:
    sc = data.get("scan")
    if not sc:
        return ""
    r = next((x for x in sc["rules"] if x["id"] == hid or hid in x.get("also", [])), None)
    if not r:
        return ""
    cells = _scan_cells(data)
    rows = [_scan_row(lang, cells[(r["id"], s)],
                      f'<a href="../coins/{e(s)}.html">{e(s.removesuffix("USDT"))}</a>')
            for s in sc["coins"] if (r["id"], s) in cells]
    return (f'<h2 id="scan">{e(t(lang, "scan_rule_h"))}</h2><p>{e(t(lang, "scan_rule_intro", start=sc["start"]))}</p>'
            f'{_legend(lang)}{_scan_table(lang, rows, t(lang, "th_coin"))}')


def scan_for_coin(lang: str, sym: str, data: dict) -> str:
    sc = data.get("scan")
    if not sc:
        return ""
    hyps = {h["id"]: h for h in data["hypotheses"]}
    cells = _scan_cells(data)
    rows = [_scan_row(lang, cells[(r["id"], sym)],
                      f'<a href="../hypotheses/{e(r["id"])}.html">{e(r["id"])}</a><span class="sub">{e(rule_label(lang, r["id"], hyps))}</span>')
            for r in sc["rules"] if (r["id"], sym) in cells]
    if not rows:
        return ""
    return (f'<h2 id="scan">{e(t(lang, "scan_coin_h"))}</h2><p>{e(t(lang, "scan_coin_intro", start=sc["start"]))}</p>'
            f'{_legend(lang)}{_scan_table(lang, rows, t(lang, "th_rule_short"))}')


def progress_bar(lang: str, pr: dict | None, inline: bool = False) -> str:
    if not pr:
        return ""
    bar = f'<div class="progress" role="img" aria-label="{pr["share"]:.0%}"><span style="width:{pr["share"] * 100:.1f}%"></span></div>'
    if inline:
        return f'{bar}<span class="meta">{pr["done"]}/{pr["total"]}</span>'
    return f'<p>{e(t(lang, "progress", done=pr["done"], total=pr["total"], share=pct(pr["share"], nd=1), date=pr["date"]))}</p>{bar}'


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
                     f'<div class="value">{e(band if m.get("metric") == "rule_state" else fmt_monitor(m))}</div><span class="band">{e(band)}</span>'
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

    coin_rows = "".join(
        f'<tr><td><a href="coins/{e(c["symbol"])}.html"><strong>{e(c["ticker"])}</strong><span class="sub">{e(c["name"])}</span></a></td>'
        f'<td class=num>{price(c["price"])}</td><td class=num>{pct(c["ch7"], True)}</td>'
        f'<td class=num>{pct(c["ch30"], True)}</td><td class=num>{pct(c["vs200"], True)}</td>'
        f'<td class=num>{pct(c["vol"], nd=0)}</td><td class=num>{pct(c.get("dd_peak"), True, 1 if abs(c.get("dd_peak") or 0) >= 0.995 else 0)}</td>'
        f'<td class=num>{usd(c.get("usd100"))}</td></tr>' for c in data.get("coins", []))
    coins_section = (f'<section aria-labelledby="coins"><h2 id="coins">{e(t(lang, "coins_title"))}</h2>'
                     f'<p>{e(t(lang, "coins_intro"))}</p><p class="meta sort-hint">{e(t(lang, "sort_hint"))}</p>'
                     f'<div class="table-wrap"><table class="sortable" data-hint="{e(t(lang, "sort_hint"))}"><thead><tr>'
                     f'<th>{e(t(lang, "th_coin"))}</th><th class=num>{e(t(lang, "th_price"))}</th><th class=num>{e(t(lang, "th_7d"))}</th>'
                     f'<th class=num>{e(t(lang, "th_30d"))}</th><th class=num>{e(t(lang, "th_vs200"))}</th><th class=num>{e(t(lang, "th_vol"))}</th>'
                     f'<th class=num>{e(t(lang, "th_peak"))}</th><th class=num>{e(t(lang, "th_100"))}</th></tr></thead><tbody>{coin_rows}</tbody></table></div></section>') if coin_rows else ""

    rows = []
    for h in hyps:
        when = (h.get("run_at") or "")[:10] or (h["history"][-1]["date"] if h["history"] else "")
        href = f'hypotheses/{e(h["id"])}.html'
        rows.append(f'<tr><td><a href="{href}">{e(h["id"])}</a></td><td><a href="{href}">{e(title_of(lang, h))}</a></td>'
                    f'<td>{e(sub(lang, "families", h["family"], h["family"]))}</td><td>{badge(lang, h["verdict"])}</td>'
                    f'<td>{e(plain(lang, h["verdict"], h.get("test_after")))}{progress_bar(lang, h.get("progress"), True)}</td>'
                    f'<td class=num>{e(when)}</td></tr>')

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
{diag_section(lang, data)}
<a class="course-cta" href="course.html">{e(C.UI.get(lang, C.UI['en'])['home_link'])} →</a>

<section aria-labelledby="how-to-read"><h2 id="how-to-read">{e(t(lang, 'how_title'))}</h2>
<ol class="steps">{how}</ol></section>

<section aria-labelledby="regime"><h2 id="regime">{e(t(lang, 'regime_title'))}</h2>
<p>{e(t(lang, 'regime_intro'))}</p>
<div class="cards">{''.join(cards)}</div></section>

{coins_section}

{btc}

<section aria-labelledby="hypotheses"><h2 id="hypotheses">{e(t(lang, 'hyp_title'))}</h2>
<p>{t(lang, 'hyp_intro', **b)}</p>
<p class="meta sort-hint">{e(t(lang, 'sort_hint'))}</p>
<div class="table-wrap"><table class="sortable" data-hint="{e(t(lang, 'sort_hint'))}"><thead><tr><th>{e(t(lang, 'th_id'))}</th><th>{e(t(lang, 'th_hyp'))}</th>
<th>{e(t(lang, 'th_family'))}</th><th>{e(t(lang, 'th_verdict'))}</th><th>{e(t(lang, 'th_plain'))}</th>
<th>{e(t(lang, 'th_tested'))}</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div></section>

{scan_matrix(lang, data)}

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
<p class="plain"><strong>{e(t(lang, 'in_plain'))}:</strong> {e(plain(lang, h['verdict'], h.get('test_after')))}</p>
{progress_bar(lang, h.get('progress'))}
<h2>{e(t(lang, 'result_h'))}</h2>
{en_note}
<p lang="en">{e(h['summary'])}</p>
<p class="meta">{e(t(lang, 'metrics_note'))} <a href="../#glossary">{e(t(lang, 'nav_glossary'))}</a></p>
{results_table(lang, h['rows'], (h.get('spec') or {}).get('kind', ''))}
{curve_block}
{scan_for_rule(lang, hid, data)}
<h2>{e(t(lang, 'why_h'))}</h2><p lang="en">{e(h['rationale'])}</p>
<h2>{e(t(lang, 'history_h'))}</h2><ul>{history}{engine}</ul>
{spec}
</main>
{footer(lang, hid)}"""
    url = page_url(base, lang, hid)
    description = t(lang, "hyp_desc", id=hid, verdict=verdict_word(lang, h["verdict"]), title=title,
                    plain=plain(lang, h["verdict"], h.get("test_after")))
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


def coin_page(lang: str, c: dict, data: dict, base: str, verification: str = "") -> str:
    key = f"coin:{c['symbol']}"
    hyps = {h["id"]: h for h in data["hypotheses"]}
    ch = c["chart"]
    charts = {"coin": {"d": ch["close"]["d"], "log": True, "series": [
        {"label": t(lang, "close_label", ticker=c["ticker"]), "v": ch["close"]["v"]},
        {"label": t(lang, "sma50"), "v": ch["sma50"]["v"], "dash": [6, 4], "color": "--weak"},
        {"label": t(lang, "sma200"), "v": ch["sma200"]["v"], "dash": [2, 3]}]}}
    stats = [("st_price", price(c["price"])), ("st_7d", pct(c["ch7"], True)), ("st_30d", pct(c["ch30"], True)),
             ("st_1y", pct(c["ch365"], True)), ("st_sma50", pct(c["vs50"], True)),
             ("st_sma200", pct(c["vs200"], True)), ("st_vol", pct(c["vol"], nd=0)),
             (t(lang, "st_peak", since=(c.get("since") or "")[:4], peak=price(c.get("peak")), date=c.get("peak_date", "")),
              pct(c.get("dd_peak"), True)),
             ("st_100", usd(c.get("usd100"))),
             ("st_corr", "—" if c.get("corr_btc") is None else f"{c['corr_btc']:.2f}")]
    stat_rows = "".join(f"<tr><th scope=row>{e(t(lang, k) if k.startswith('st_') else k)}</th><td class=num>{e(v)}</td></tr>"
                        for k, v in stats)

    def state(sig, val):
        if val is None:
            return "—"
        if sig == "vol":
            return f"<strong>{pct(val, nd=0)}</strong>"
        cls, word = ("yes", t(lang, "state_in")) if val else ("no", t(lang, "state_out"))
        return f'<span class="{cls}">{e(word)}</span>'

    sig_rows = []
    for sig, label in (("sma50", "sig_sma50"), ("mom7", "sig_mom7"), ("vol", "sig_vol"), ("btc", "sig_btc")):
        links = " ".join(f'<a href="../hypotheses/{i}.html">{i}</a> {badge(lang, hyps[i]["verdict"])}'
                         for i in SIGNAL_STUDIES_R[sig] if i in hyps)
        sig_rows.append(f"<tr><td>{e(t(lang, label))}</td><td>{state(sig, c['signals'][sig])}</td><td>{links}</td></tr>")
    for rs in c.get("rule_states", []):
        h = hyps.get(rs["id"])
        if not h:
            continue
        val = None if rs["state"] is None else rs["state"] >= 0.5
        sig_rows.append(f'<tr><td>{e(t(lang, "sig_rule", id=rs["id"]))}: {e(title_of(lang, h))}</td>'
                        f'<td>{state("rule", val)}</td><td><a href="../hypotheses/{e(rs["id"])}.html">{e(rs["id"])}</a> '
                        f'{badge(lang, rs["verdict"])}</td></tr>')
    studies = "".join(f'<li><a href="../hypotheses/{e(s["id"])}.html">{e(s["id"])}: {e(title_of(lang, hyps[s["id"]]))}'
                      f'</a> {badge(lang, s["verdict"])}</li>' for s in c["studies"] if s["id"] in hyps)
    thin = (f'<p class="callout">{e(t(lang, "thin_note", exchange=c["exchange"]))}</p>'
            if c["exchange"] != "Binance" else "")
    title = t(lang, "coin_title", name=c["name"], ticker=c["ticker"])
    body = f"""{header(lang, key, data['generated_at'])}
<main>
<p class="meta"><a href="../#coins">{e(t(lang, 'back_coins'))}</a></p>
<h1>{e(title)}</h1>
<p>{e(t(lang, 'coin_lead', exchange=c['exchange'], date=c['date']))}</p>
{thin}
{coin_diag(lang, c, data)}
<h2>{e(t(lang, 'chart12_h'))}</h2>
<div class="chart"><canvas data-chart="coin" role="img" aria-label="{e(title)}"></canvas></div>
<h2>{e(t(lang, 'stats_h'))}</h2>
<div class="table-wrap"><table><tbody>{stat_rows}</tbody></table></div>
<p class="meta">{e(t(lang, 'corr_note'))}</p>
<h2>{e(t(lang, 'signals_h'))}</h2>
<p class="callout">{e(t(lang, 'signals_warn'))}</p>
<div class="table-wrap"><table><thead><tr><th>{e(t(lang, 'th_rule'))}</th><th>{e(t(lang, 'th_state'))}</th>
<th>{e(t(lang, 'th_tested_in'))}</th></tr></thead><tbody>{''.join(sig_rows)}</tbody></table></div>
{scan_for_coin(lang, c['symbol'], data)}
<h2>{e(t(lang, 'coin_studies_h'))}</h2>
{f'<ul>{studies}</ul>' if studies else f'<p>{e(t(lang, "no_studies"))}</p>'}
<p class="meta"><a href="../#glossary">{e(t(lang, 'nav_glossary'))}</a></p>
</main>
{footer(lang, key)}"""
    url = page_url(base, lang, key)
    description = t(lang, "coin_desc", name=c["name"], ticker=c["ticker"], price=price(c["price"]),
                    ch30=pct(c["ch30"], True), vs200=pct(c["vs200"], True))
    jsonld = [{"@context": "https://schema.org", "@type": "WebPage", "name": title, "description": description[:300],
               "url": url, "inLanguage": LANGS[lang][1], "dateModified": c["date"],
               "about": {"@type": "Thing", "name": f"{c['name']} ({c['ticker']})"},
               "isPartOf": {"@type": "WebSite", "name": "Crypto Research Labs", "url": page_url(base, lang)}},
              {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                  {"@type": "ListItem", "position": 1, "name": "Crypto Research Labs", "item": page_url(base, lang)},
                  {"@type": "ListItem", "position": 2, "name": f"{c['name']} ({c['ticker']})", "item": url}]}]
    return page(lang=lang, hid=key, base=base, title=f"{title} | Crypto Research Labs", description=description[:320],
                body=body, charts=charts, jsonld=jsonld, verification=verification)


def course_page(lang: str, values: dict, data: dict, base: str, verification: str = "") -> str:
    ui = C.UI.get(lang, C.UI["en"])
    lessons = C.LESSONS.get(lang, C.LESSONS["en"])
    flow = C.flow_html(ui["flow"])
    toc = "".join(f'<li><a href="#lesson-{i}">{e(ui["lesson"].format(n=i))}. {e(title)}</a></li>'
                  for i, (title, _) in enumerate(lessons, 1))
    parts = []
    for i, (title, md) in enumerate(lessons, 1):
        parts.append(f'<section aria-labelledby="lesson-{i}"><h2 id="lesson-{i}">{e(ui["lesson"].format(n=i))}. '
                     f'{e(title)}</h2>{C.md_to_html(C.fill(md, values), flow)}</section>')
    body = f"""{header(lang, "course", data['generated_at'])}
<main>
<h1>{e(ui['h1'])}</h1>
<p><span class="beginner">{e(ui['badge'])}</span></p>
<p class="lead">{e(ui['lead'])}</p>
<h2>{e(ui['toc'])}</h2>
<ol class="toc">{toc}</ol>
{''.join(parts)}
</main>
{footer(lang, "course")}"""
    url = page_url(base, lang, "course")
    jsonld = [{"@context": "https://schema.org", "@type": "Course", "name": ui["title"], "description": ui["desc"],
               "url": url, "inLanguage": LANGS[lang][1], "isAccessibleForFree": True, "educationalLevel": "Beginner",
               "provider": {"@type": "Organization", "name": "Crypto Research Labs", "sameAs": REPO},
               "hasCourseInstance": {"@type": "CourseInstance", "courseMode": "online",
                                     "courseWorkload": "PT1H30M"},
               "offers": {"@type": "Offer", "price": 0, "priceCurrency": "USD", "category": "Free"},
               "dateModified": data["generated_at"][:10]},
              {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                  {"@type": "ListItem", "position": 1, "name": "Crypto Research Labs", "item": page_url(base, lang)},
                  {"@type": "ListItem", "position": 2, "name": ui["h1"], "item": url}]}]
    return page(lang=lang, hid="course", base=base, title=ui["title"], description=ui["desc"][:320], body=body,
                charts={}, jsonld=jsonld, verification=verification)


def setup_page(lang: str, data: dict, base: str, verification: str = "") -> str:
    g = SG.GUIDE.get(lang, SG.GUIDE["en"])
    toc = "".join(f'<li><a href="#s{i}">{e(title)}</a></li>' for i, (title, _) in enumerate(g["sections"], 1))
    parts = "".join(f'<section aria-labelledby="s{i}"><h2 id="s{i}">{e(title)}</h2>{C.md_to_html(md)}</section>'
                    for i, (title, md) in enumerate(g["sections"], 1))
    body = f"""{header(lang, "setup", data['generated_at'])}
<main>
<h1>{e(g['h1'])}</h1>
<p class="lead">{e(g['lead'])}</p>
<h2>{e(g['toc'])}</h2>
<ol>{toc}</ol>
{parts}
</main>
{footer(lang, "setup")}"""
    url = page_url(base, lang, "setup")
    jsonld = [{"@context": "https://schema.org", "@type": "HowTo", "name": g["h1"], "description": g["desc"],
               "url": url, "inLanguage": LANGS[lang][1],
               "step": [{"@type": "HowToSection", "name": title, "position": i}
                        for i, (title, _) in enumerate(g["sections"], 1)],
               "dateModified": data["generated_at"][:10]},
              {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                  {"@type": "ListItem", "position": 1, "name": "Crypto Research Labs", "item": page_url(base, lang)},
                  {"@type": "ListItem", "position": 2, "name": g["h1"], "item": url}]}]
    return page(lang=lang, hid="setup", base=base, title=g["title"], description=g["desc"][:320], body=body,
                charts={}, jsonld=jsonld, verification=verification)


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


LOGO = ('<svg viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="14" fill="#15243b"/>'
        '<path d="M10 46 L24 30 L34 38 L54 16" fill="none" stroke="#7cc4ff" stroke-width="6" stroke-linecap="round" '
        'stroke-linejoin="round"/><circle cx="54" cy="16" r="5.5" fill="#46c281"/></svg>')

FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" '
           'fill="#0f1b2d"/><path d="M10 46 L24 30 L34 38 L54 16" fill="none" stroke="#7cc4ff" stroke-width="6" '
           'stroke-linecap="round" stroke-linejoin="round"/><circle cx="54" cy="16" r="5" fill="#46c281"/></svg>')

NOT_FOUND = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport"
content="width=device-width, initial-scale=1"><meta name="robots" content="noindex"><title>Page not found |
Crypto Research Labs</title><style>body{background:#0d1117;color:#fff;font:18px/1.6 system-ui,sans-serif;
max-width:700px;margin:60px auto;padding:0 16px}a{color:#79c0ff}</style></head><body><h1>Page not found</h1>
<p><a href="/Crypto-Research-Labs/">Go to the Crypto Research Labs dashboard</a></p></body></html>
"""

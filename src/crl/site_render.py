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
TOP_PAGES = ("market", "research", "forecast", "digest", "course", "about", "setup")
SIGNAL_STUDIES_R = {"sma50": ["H-005", "H-018"], "mom7": ["H-014"], "vol": ["H-012", "H-013"], "btc": ["H-017", "H-019"]}

CSS = """
:root{--bg:#0f1b2d;--panel:#15243b;--raised:#1b2e4a;--line:#3a5479;--text:#ffffff;--text2:#e3eaf5;
--link:#8ccbff;--accent:#7cc4ff;--pass:#46c281;--weak:#f0b44c;--fail:#ff6b73;--hold:#e3eaf5;--ink:#0f1b2d;
--pend:#9fb6d6;--edge:#0a1424;--shade:rgba(0,0,0,.5);--glow:rgba(70,194,129,.55);
--mono:"IBM Plex Mono",ui-monospace,Menlo,monospace}
@media (prefers-color-scheme:light){:root{--bg:#eef3fa;--panel:#ffffff;--raised:#e3ebf6;--line:#9fb2cc;
--text:#06101d;--text2:#18263a;--link:#08458a;--accent:#0a58a8;--pass:#127a43;--weak:#8a5a00;--fail:#b4232f;
--hold:#18263a;--ink:#ffffff;--pend:#4d6585;--edge:#b9c8dc;--shade:rgba(20,40,70,.22);--glow:rgba(18,122,67,.35)}}
*{box-sizing:border-box}
html{font-size:18px;-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--text);
background-image:radial-gradient(1200px 600px at 85% -10%,color-mix(in srgb,var(--accent) 12%,transparent),transparent 70%);
font:1rem/1.6 "IBM Plex Sans",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;font-variant-numeric:tabular-nums}
a{color:var(--link);text-underline-offset:.18em;text-decoration-thickness:1px}
a:hover{text-decoration-thickness:2px}
main,footer,.bar{max-width:1120px;margin:0 auto;padding:0 20px}
footer p{max-width:90ch}
/* header: brand, five pages, language list, GitHub */
.site-head{position:sticky;top:0;z-index:5;background:var(--panel);border-bottom:1px solid var(--line);
box-shadow:0 6px 18px var(--shade);margin-bottom:32px}
.bar{display:flex;align-items:center;gap:10px 16px;padding-top:10px;padding-bottom:10px;position:relative}
.brand{display:flex;align-items:center;gap:10px;color:var(--text);text-decoration:none;font-weight:700;font-size:1.05rem;letter-spacing:-.01em;margin-right:auto}
.brand svg{width:32px;height:32px;flex:none;filter:drop-shadow(0 3px 0 var(--edge))}
nav.menu{display:flex;flex:none;gap:4px}
.brand span{white-space:nowrap}
.pill.menu-btn{display:none}
nav.menu a{color:var(--text);text-decoration:none;font-weight:600;font-size:.95rem;padding:7px 14px;border-radius:10px;border:1px solid transparent}
nav.menu a:hover{background:var(--raised);border-color:var(--line)}
nav.menu a[aria-current]{background:var(--raised);border-color:var(--line);box-shadow:0 3px 0 var(--edge)}
.pill{display:inline-flex;align-items:center;gap:6px;font:600 .9rem "IBM Plex Sans",system-ui,sans-serif;color:var(--text);
background:var(--raised);border:1px solid var(--line);border-radius:10px;padding:6px 12px;box-shadow:0 3px 0 var(--edge);
cursor:pointer;text-decoration:none;white-space:nowrap}
details.langs{position:relative;background:none;border:0;padding:0;margin:0}
details.langs summary{list-style:none}details.langs summary::-webkit-details-marker{display:none}
.lang-list{position:absolute;right:0;top:calc(100% + 8px);display:grid;gap:2px;background:var(--panel);border:1px solid var(--line);
border-radius:12px;padding:8px;min-width:170px;box-shadow:0 14px 28px var(--shade);z-index:6}
.lang-list a{color:var(--text);text-decoration:none;padding:6px 10px;border-radius:8px;font-weight:500}
.lang-list a:hover{background:var(--raised)}.lang-list a[aria-current]{font-weight:700;text-decoration:underline}
/* depth: the 3D language of the site lives on containers; text stays flat and high-contrast */
.slab{background:linear-gradient(180deg,color-mix(in srgb,var(--raised) 70%,var(--panel)),var(--panel));border:1px solid var(--line);
border-radius:18px;box-shadow:inset 0 1px 0 color-mix(in srgb,#fff 10%,transparent),0 6px 0 var(--edge),0 22px 40px var(--shade);
transition:transform .25s ease}
.eyebrow{font:600 .8rem var(--mono);letter-spacing:.06em;text-transform:uppercase;color:var(--accent);margin:0 0 .4em}
.more{display:inline-flex;font-weight:600;margin-top:14px}
main section{margin-top:52px}
.hero{display:grid;grid-template-columns:1.05fr .95fr;gap:24px;align-items:center}
.hero h1{font-size:2.6rem;max-width:20ch}
.answer{font-size:1.2rem;max-width:36ch}.answer strong{color:var(--text)}
.tally{display:flex;flex-wrap:wrap;gap:10px;margin:22px 0 26px;padding:0;list-style:none}
.tally li{display:flex;align-items:center;gap:8px;font-weight:600;color:var(--text);background:var(--panel);border:1px solid var(--line);
border-radius:10px;padding:6px 12px;box-shadow:0 3px 0 var(--edge);margin:0}
.tally b{font:600 1.1rem var(--mono)}
.sq{width:14px;height:14px;border-radius:4px;display:inline-block}
.sq.p{background:var(--pass)}.sq.w{background:var(--weak)}.sq.f{background:var(--fail)}.sq.n{border:2px dashed var(--pend)}
.cta{display:flex;flex-wrap:wrap;gap:12px}
.btn{display:inline-flex;align-items:center;font:700 1.02rem "IBM Plex Sans",system-ui,sans-serif;text-decoration:none;border-radius:14px;
padding:14px 22px;transition:transform .15s ease}
.btn.primary{background:var(--accent);color:var(--ink);box-shadow:0 5px 0 color-mix(in srgb,var(--accent) 45%,#000),0 14px 26px var(--shade)}
.btn.ghost{background:var(--raised);color:var(--text);border:2px solid var(--pass);box-shadow:0 5px 0 var(--edge),0 14px 26px var(--shade)}
.btn:active{transform:translateY(4px)}
.scene{perspective:1000px;height:400px;display:grid;place-items:center}
.field{display:grid;grid-template-columns:repeat(6,var(--s));gap:12px;--s:46px;transform-style:preserve-3d;
transform:rotateX(58deg) rotateZ(38deg);animation:sway 16s ease-in-out infinite alternate}
@keyframes sway{from{transform:rotateX(58deg) rotateZ(32deg)}to{transform:rotateX(56deg) rotateZ(46deg)}}
.blk{position:relative;width:var(--s);height:var(--s);transform-style:preserve-3d;--h:16px;--c:var(--fail)}
.blk i{position:absolute;display:block}
.blk .t{inset:0;transform:translateZ(var(--h));background:linear-gradient(135deg,color-mix(in srgb,var(--c) 75%,#fff),var(--c));border-radius:3px}
.blk .f{left:0;top:100%;width:100%;height:var(--h);transform-origin:top;transform:rotateX(90deg);background:color-mix(in srgb,var(--c) 62%,#000)}
.blk .r{top:0;left:100%;width:var(--h);height:100%;transform-origin:left;transform:rotateY(-90deg);background:color-mix(in srgb,var(--c) 45%,#000)}
.blk.w{--c:var(--weak);--h:42px}.blk.p{--c:var(--pass);--h:118px}.blk.p .t{box-shadow:0 0 40px 12px var(--glow)}
.blk.n{--h:4px;--c:var(--raised)}.blk.n .t{border:2px dashed var(--pend);background:transparent}
.scene-cap{text-align:center;font:500 .85rem var(--mono);margin-top:-18px}
.gauge{width:100%;max-width:300px;filter:drop-shadow(0 6px 0 var(--edge)) drop-shadow(0 16px 22px var(--shade))}
.gauge text{font:600 12px var(--mono);fill:var(--text2)}
.count{font:600 .9rem var(--mono)}
.meaning{margin-top:16px;padding:14px 16px;border-radius:12px;background:var(--bg);border:1px solid var(--line)}
.meaning strong{color:var(--text)}
.found{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:20px}
.card{padding:22px 24px;min-width:0}
.card h3 a{color:var(--text);text-decoration:none}.card h3 a:hover{text-decoration:underline}
.card h3{font-size:1.15rem;line-height:1.3;margin:.6em 0 .4em}
.badge.in{background:var(--accent)}.badge.wait{background:var(--pend)}
.progress3d{height:22px;border-radius:999px;background:var(--bg);border:1px solid var(--line);box-shadow:inset 0 3px 6px var(--shade);overflow:hidden;margin:14px 0 8px}
.progress3d span{display:block;height:100%;min-width:22px;border-radius:999px;background:linear-gradient(180deg,color-mix(in srgb,var(--accent) 70%,#fff),var(--accent))}
.kv{display:flex;flex-wrap:wrap;gap:8px 18px;font-weight:600;color:var(--text)}
.digest-line{display:flex;flex-wrap:wrap;align-items:center;gap:10px 16px;margin-top:24px;padding:16px 20px}
.digest-line strong{color:var(--text)}
.group h2{display:flex;align-items:center;gap:12px;border:0}
.cube{width:28px;height:28px;flex:none}
.m h3{font-size:1rem;line-height:1.35}
.wide{grid-column:1/-1}
details.what{background:none;border:0;padding:0;margin:10px 0 0}
details.what summary{color:var(--link)}details.what p{font-size:.95rem;margin:.4em 0 0}
.watchnote{margin-top:16px;padding:16px 20px;display:flex;gap:14px;align-items:flex-start}
.watchnote p{margin:.2em 0}
tr.watch td{background:color-mix(in srgb,var(--weak) 12%,transparent)}
.fresh{margin-top:32px;display:flex;flex-wrap:wrap;gap:8px 20px;align-items:center;font-weight:600}
.ok{color:var(--pass)}
.vblocks{display:flex;flex-wrap:wrap;gap:14px;margin:20px 0 12px}
.vblock{display:flex;flex-direction:column;align-items:flex-start;gap:2px;min-width:140px;padding:14px 18px;border-radius:14px;
border:2px solid var(--line);background:var(--panel);color:var(--text);font:600 1rem "IBM Plex Sans",system-ui,sans-serif;cursor:pointer;
box-shadow:0 5px 0 var(--edge),0 12px 22px var(--shade);transition:transform .15s ease}
.vblock b{font:600 2rem/1.1 var(--mono)}
.vblock.pass b{color:var(--pass)}.vblock.weak b{color:var(--weak)}.vblock.fail b{color:var(--fail)}.vblock.wait b{color:var(--pend)}
.vblock[aria-pressed="true"]{border-color:var(--accent);transform:translateY(3px);box-shadow:0 2px 0 var(--edge)}
ol.flow3d{list-style:none;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:14px;counter-reset:f}
ol.flow3d li{counter-increment:f;padding:16px 18px;font-weight:600;color:var(--text);margin:0}
ol.flow3d li::before{content:counter(f);display:block;font:600 1.5rem var(--mono);color:var(--accent)}
.howto{padding:6px 24px 14px}
.crumbs{margin-top:0}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px;margin:14px 0}
.stat{padding:14px 18px;display:flex;flex-direction:column;gap:4px}.stat span{font-weight:600;color:var(--text2)}
.stat b{font:600 1.6rem var(--mono);color:var(--text)}
#hyp-table td:first-child{white-space:nowrap}
h1{font-size:2.3rem;line-height:1.15;letter-spacing:-.02em;font-weight:700;margin:.1em 0 .35em;max-width:26ch;text-wrap:balance}
h2{font-size:1.5rem;line-height:1.25;letter-spacing:-.01em;font-weight:600;margin:2.4em 0 .7em;padding-bottom:.35em;border-bottom:1px solid var(--line)}
h3{font-size:1.08rem;font-weight:600;margin:0 0 .3em}
p,li{color:var(--text2)}
main p{max-width:78ch}
.lead{font-size:1.15rem;max-width:64ch}
.meta{color:var(--text2);font-size:.9rem}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:18px}
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
/* diagnosis: gauge + headline + reasons */
.diag{display:grid;grid-template-columns:300px 1fr;gap:28px;align-items:center;padding:24px 28px;margin:12px 0 8px}
section.diag{display:block;background:var(--panel);border:1px solid var(--line);border-radius:16px}
.diag h2{border:0;margin:0 0 .2em;padding:0}
.diag-head{font-size:1.5rem;line-height:1.25;font-weight:600;letter-spacing:-.015em;color:var(--text);margin:.1em 0 .4em;max-width:32ch}
.meter{display:flex;height:10px;border-radius:999px;overflow:hidden;background:var(--raised);max-width:420px;margin:.2em 0 .4em}
.meter i{display:block}.meter .m-up{background:var(--pass)}.meter .m-0{background:var(--line)}.meter .m-down{background:var(--fail)}
ul.diag-list{list-style:none;padding-left:0;margin:.8em 0;display:grid;gap:8px}
ul.diag-list li{margin:0;padding-left:1.9em;position:relative;max-width:80ch}
ul.diag-list li::before{position:absolute;left:0;top:.05em;font-weight:700;width:1.3em;text-align:center}
li.t-up::before{content:"▲";color:var(--pass)}li.t-down::before{content:"▼";color:var(--fail)}li.t-0::before{content:"●";color:var(--text2);font-size:.8em;top:.25em}
.diag h3{margin-top:1em}
.digest{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px 20px;margin:14px 0}
.digest h2,.digest h3{border:0;margin:0 0 .5em;padding:0}
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
.bar{padding-top:10px;padding-bottom:10px;gap:8px;flex-wrap:wrap}.js-menu .bar{flex-wrap:nowrap}
.brand{font-size:.95rem;line-height:1.15}.brand span{white-space:normal}.pill.gh{display:none}
nav.menu{flex-wrap:wrap}.js-menu .pill.menu-btn{display:inline-flex}
.js-menu nav.menu{display:none;position:absolute;left:0;right:0;top:100%;flex-direction:column;background:var(--panel);
border-bottom:1px solid var(--line);padding:8px 14px 14px;box-shadow:0 14px 24px var(--shade)}
.js-menu nav.menu.open{display:flex}
nav.menu a{font-size:1.05rem;padding:10px 12px}
.hero,.diag{grid-template-columns:1fr}.hero h1{font-size:2rem}
.scene{height:300px}.field{--s:34px;gap:9px}.blk.p{--h:88px}.blk.w{--h:32px}.blk{--h:12px}
.gauge{max-width:260px;justify-self:center}.diag{padding:20px}
.vblock{min-width:calc(50% - 7px);flex:1}
#hyp-table td:nth-child(3),#hyp-table td:nth-child(5){display:none}
h1{font-size:1.75rem}
h2{font-size:1.3rem}
.diag-head{font-size:1.3rem}
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
@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
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

# menu button on phones, verdict filter on Research, gentle 3D tilt, and redirects from the old one-page anchors
UI_SCRIPT = """
(function(){
var d=document,h=d.documentElement,page=d.body.getAttribute('data-page');
if(page==='home'){var old={'#how-to-read':'course.html#read','#regime':'market.html','#coins':'market.html#coins',
 '#btc':'market.html#btc','#hypotheses':'research.html#all','#scan':'research.html#scan','#glossary':'course.html#glossary',
 '#methodology':'about.html#methodology','#data':'about.html#data','#digest':'digest.html'};
 if(old[location.hash]){location.replace(old[location.hash]);return}}
var btn=d.querySelector('.menu-btn'),menu=d.getElementById('site-menu');
if(btn&&menu){h.classList.add('js-menu');btn.hidden=false;
 btn.addEventListener('click',function(){var o=menu.classList.toggle('open');btn.setAttribute('aria-expanded',o)})}
var tb=d.getElementById('hyp-table');
if(tb){d.querySelectorAll('.vblock').forEach(function(b){b.addEventListener('click',function(){
 var f=b.getAttribute('data-filter');d.querySelectorAll('.vblock').forEach(function(x){x.setAttribute('aria-pressed',x===b)});
 Array.prototype.forEach.call(tb.tBodies[0].rows,function(r){r.hidden=f!=='ALL'&&r.getAttribute('data-verdict')!==f})})})}
if(matchMedia('(hover:hover) and (pointer:fine)').matches&&!matchMedia('(prefers-reduced-motion:reduce)').matches){
 d.querySelectorAll('.tilt').forEach(function(el){
  el.addEventListener('pointermove',function(ev){var r=el.getBoundingClientRect(),x=(ev.clientX-r.left)/r.width-.5,
   y=(ev.clientY-r.top)/r.height-.5,k=r.width>600?2:4;
   el.style.transform='perspective(1000px) rotateX('+(-y*k).toFixed(2)+'deg) rotateY('+(x*k).toFixed(2)+'deg) translateY(-3px)'});
  el.addEventListener('pointerleave',function(){el.style.transform=''})})}
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
    if key in TOP_PAGES:
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
    depth = (lang != DEFAULT) + (hid is not None and hid not in TOP_PAGES)
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
    scripts += f'<script defer src="{root}sort.js"></script><script defer src="{root}ui.js"></script>'
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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500;600&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap">
<style>{CSS}</style>
{ld}
</head>
<body data-page="{'home' if hid is None else _section_of(hid)}">
{body}
{scripts}
</body>
</html>
"""


NAV = (("market", "nav_market"), ("research", "nav_research"), ("digest", "nav_digest"), ("course", "nav_beginners"),
       ("about", "nav_about"))


def _section_of(hid: str | None) -> str | None:
    """Which menu item a page belongs to."""
    if hid is None:
        return None
    if hid.startswith("coin:"):
        return "market"
    if hid == "setup":
        return "about"
    if hid == "forecast":
        return "research"
    return hid if hid in TOP_PAGES else "research"


def header(lang: str, hid: str | None, generated: str) -> str:
    home = (asset_root(lang, hid) + ("" if lang == DEFAULT else f"{lang}/")) or "./"
    up = asset_root(lang, hid)
    langs = []
    for c, (name, hl, _) in LANGS.items():
        target = up + page_path(c, hid).replace("index.html", "")
        target = target or "./"
        cur = ' aria-current="page"' if c == lang else ""
        langs.append(f'<a href="{e(target)}" hreflang="{hl}" lang="{hl}"{cur}>{e(name)}</a>')
    here = _section_of(hid)
    items = "".join(f'<a href="{home}{key}.html"{" aria-current=page" if key == here else ""}>{e(t(lang, label))}</a>'
                    for key, label in NAV)
    return f"""<header class="site-head"><div class="bar">
<a class="brand" href="{home}">{LOGO}<span>Crypto Research Labs</span></a>
<button type="button" class="pill menu-btn" aria-controls="site-menu" aria-expanded="false" hidden>☰ {e(t(lang, 'menu'))}</button>
<nav class="menu" id="site-menu" aria-label="{e(t(lang, 'menu'))}">{items}</nav>
<details class="langs"><summary class="pill" aria-label="{e(t(lang, 'lang_label'))}">{e(lang.upper())} ▾</summary>
<div class="lang-list">{''.join(langs)}</div></details>
<a class="pill gh" href="{REPO}">GitHub</a>
</div></header>"""


def footer(lang: str, hid: str | None) -> str:
    root = asset_root(lang, hid)
    pre = root + ("" if lang == DEFAULT else lang + "/")
    return f"""<footer>
<p>{t(lang, 'footer_disclaimer')}</p>
<p><a href="{pre}about.html">{e(t(lang, 'nav_about'))}</a> ·
<a href="{pre}setup.html">{e(SG.GUIDE.get(lang, SG.GUIDE['en'])['nav'])}</a> ·
<a href="{root}data.json">{e(t(lang, 'footer_data'))}</a> · <a href="{REPO}">GitHub</a> · MIT License</p>
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


def diag_item_text(lang: str, it: dict) -> str:
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
    return text


def _diag_item(lang: str, it: dict) -> str:
    return f'<li class="{TONE_CLASS[it["tone"]]}">{e(diag_item_text(lang, it))}</li>'


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


MONITOR_GROUP = {"btc_trend": "g_trend", "breadth": "g_trend", "btc_volatility": "g_mood", "fear_greed": "g_mood",
                 "stablecoin_growth": "g_money", "btc_exchange_flow": "g_money", "h020_rule": "g_money",
                 "funding_carry": "g_money", "ever_trend": "watch"}
GROUP_ORDER = ("g_trend", "g_mood", "g_money")
GROUP_COLOR = {"g_trend": "--accent", "g_mood": "--weak", "g_money": "--pass", "g_coins": "--text2"}
BLOCK_CLASS = {"PASS": "p", "WEAK": "w", "FAIL": "f"}


def cube(var: str) -> str:
    """Small isometric cube used as a section marker."""
    return (f'<svg class="cube" viewBox="0 0 28 28" aria-hidden="true"><path d="M14 2 L26 8 L14 14 L2 8Z" fill="var({var})"/>'
            f'<path d="M2 8 L14 14 L14 26 L2 20Z" fill="color-mix(in srgb,var({var}) 55%,#000)"/>'
            f'<path d="M26 8 L14 14 L14 26 L26 20Z" fill="color-mix(in srgb,var({var}) 75%,#000)"/></svg>')


def gauge(lang: str, d: dict) -> str:
    """Semicircular 3D gauge for the market diagnosis: needle angle = (up − down) / all signals."""
    total = max(d["up"] + d["down"] + d["neutral"], 1)
    angle = 90 * (d["up"] - d["down"]) / total
    label = t(lang, "diag_count", up=d["up"], down=d["down"], neutral=d["neutral"])
    return (f'<svg class="gauge" viewBox="0 0 300 180" role="img" aria-label="{e(label)}">'
            '<defs><linearGradient id="bevel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" '
            'stop-opacity=".22"/><stop offset="1" stop-color="#000" stop-opacity=".25"/></linearGradient></defs>'
            '<path d="M30 150 A120 120 0 0 1 90 46.1" stroke="var(--fail)" stroke-width="30" fill="none"/>'
            '<path d="M90 46.1 A120 120 0 0 1 210 46.1" stroke="var(--line)" stroke-width="30" fill="none"/>'
            '<path d="M210 46.1 A120 120 0 0 1 270 150" stroke="var(--pass)" stroke-width="30" fill="none"/>'
            '<path d="M30 150 A120 120 0 0 1 270 150" stroke="url(#bevel)" stroke-width="30" fill="none"/>'
            f'<g transform="rotate({angle:.1f} 150 150)"><path d="M150 150 L145 150 L150 48 L155 150 Z" fill="var(--text)"/></g>'
            '<circle cx="150" cy="150" r="13" fill="var(--text)"/><circle cx="150" cy="150" r="6" fill="var(--panel)"/>'
            f'<text x="20" y="176">{e(t(lang, "diag_dir_down"))}</text>'
            f'<text x="280" y="176" text-anchor="end">{e(t(lang, "diag_dir_up"))}</text></svg>')


def diag_card(lang: str, data: dict, short: bool) -> str:
    """Market diagnosis. Short (home): the signals that point somewhere; full (Market): every signal and what it means."""
    d = data.get("diagnosis")
    if not d:
        return ""
    items = d["items"]
    if short:
        items = [it for it in items if it["tone"]] or items[:3]
    lis = "".join(_diag_item(lang, it) for it in items)
    tail = (f'<a class="more" href="market.html">{e(t(lang, "all_market"))}</a>' if short else
            f'<p class="meaning"><strong>{e(t(lang, "diag_means_h"))}.</strong> {e(t(lang, "diag_means_" + d["level"]))}</p>'
            f'<p class="meta">{e(t(lang, "diag_intro"))} {e(t(lang, "diag_disclaimer"))}</p>')
    return (f'<div class="slab tilt diag {d["level"]}">{gauge(lang, d)}<div class="diag-body">'
            f'<h2 class="diag-head" id="diagnosis">{e(t(lang, "diag_level_" + d["level"]))}</h2>'
            f'<p class="count">{e(t(lang, "diag_count", up=d["up"], down=d["down"], neutral=d["neutral"]))}</p>'
            f'<ul class="diag-list">{lis}</ul>{tail}</div></div>')


def verdict_field(hyps: list[dict]) -> str:
    blocks = "".join(f'<div class="blk {BLOCK_CLASS.get(h["verdict"], "n")}"><i class="t"></i><i class="f"></i>'
                     f'<i class="r"></i></div>' for h in hyps)
    return f'<div class="scene" aria-hidden="true"><div class="field">{blocks}</div></div>'


def _counts(hyps: list[dict]) -> dict:
    return {k: sum(h["verdict"] == k for h in hyps) for k in ("PASS", "WEAK", "FAIL")} | {
        None: sum(h["verdict"] not in VERDICT_KEY for h in hyps)}


def _digest_range(d: dict) -> tuple[str, str, str]:
    """The digest written on day D covers D−7 … D−1: (ISO week of that span, start, end)."""
    import datetime as _dt
    day = _dt.date.fromisoformat(d["date"])
    start, end = day - _dt.timedelta(days=7), day - _dt.timedelta(days=1)
    y, w, _ = start.isocalendar()
    return f"{y}-W{w:02d}", str(start), str(end)


def index_page(lang: str, data: dict, base: str, verification: str = "") -> str:
    hyps = data["hypotheses"]
    n, cnt = len(hyps), _counts(hyps)
    result = (t(lang, "hero_one") if cnt["PASS"] == 1 else t(lang, "hero_some", p=cnt["PASS"]) if cnt["PASS"]
              else t(lang, "hero_none"))
    verdict_line = t(lang, "verdict_some", p=cnt["PASS"], n=n) if cnt["PASS"] else t(lang, "verdict_none", n=n)
    tally = "".join(f'<li><span class="sq {c}"></span><b>{k}</b> {e(t(lang, key))}</li>' for c, k, key in (
        ("p", cnt["PASS"], "tally_pass"), ("w", cnt["WEAK"], "tally_weak"), ("f", cnt["FAIL"], "tally_fail"),
        ("n", cnt[None], "tally_wait")) if k)
    hero = (f'<div class="hero"><div><p class="eyebrow">{e(t(lang, "hero_eyebrow", t=data["generated_at"]))}</p>'
            f'<h1>{e(t(lang, "hero_q"))}</h1><p class="answer">{t(lang, "hero_a", n=n, result=result)}</p>'
            f'<ul class="tally">{tally}</ul><div class="cta">'
            f'<a class="btn primary" href="market.html">{e(t(lang, "btn_market"))}</a>'
            f'<a class="btn ghost" href="course.html">{e(t(lang, "btn_new"))}</a></div></div>'
            f'<div>{verdict_field(hyps)}<p class="scene-cap">{e(t(lang, "scene_cap"))}</p></div></div>')
    today = (f'<section aria-labelledby="diagnosis"><p class="eyebrow">{e(t(lang, "today_eyebrow"))}</p>'
             f'{diag_card(lang, data, short=True)}</section>') if data.get("diagnosis") else ""

    cards = []
    states = {m["id"]: m for m in data["regime"] if m.get("metric") == "rule_state"}
    for h in hyps:
        if h["verdict"] != "PASS":
            continue
        m = states.get(h["id"].lower().replace("-", "") + "_rule")
        now = ""
        if m and m.get("value") is not None:
            now = f' <span class="badge in">{e(t(lang, "now_in" if m["value"] >= 0.5 else "now_out"))}</span>'
        note = (f'<p>{e(t(lang, "pass_risk_note"))}</p>'
                if (h.get("spec") or {}).get("target") == "risk" else "")
        rep = next((r for r in hyps if r.get("replicates") == h["id"] and r.get("progress")), None)
        recheck = ""
        if rep:
            pr = rep["progress"]
            days = t(lang, "recheck_days", done=pr["done"], total=pr["total"])
            recheck = (f'<p class="kv"><a href="hypotheses/{e(rep["id"])}.html">{e(t(lang, "recheck_of", id=rep["id"]))}</a></p>'
                       f'<div class="progress3d" role="img" aria-label="{e(days)}"><span style="width:{pr["share"] * 100:.1f}%"></span></div>'
                       f'<p class="kv"><span>{e(days)}</span><span>{e(t(lang, "recheck_date", date=pr["date"]))}</span></p>')
        cards.append(f'<article class="slab tilt card">{badge(lang, "PASS")}{now}'
                     f'<h3><a href="hypotheses/{e(h["id"])}.html">{e(h["id"])}. {e(title_of(lang, h))}</a></h3>'
                     f'<p>{e(t(lang, "pass_text", n=n, k=cnt["PASS"]))}</p>{note}{recheck}'
                     f'<a class="more" href="hypotheses/{e(h["id"])}.html">{e(t(lang, "open_hyp"))}</a></article>')
    found = (f'<section aria-labelledby="found"><p class="eyebrow" id="found">{e(t(lang, "passed_eyebrow"))}</p>'
             f'<div class="found">{"".join(cards)}</div></section>') if cards else ""
    ds = data.get("digests") or []
    digest = ""
    if ds:
        _, start, end = _digest_range(ds[0])
        digest = (f'<p class="slab digest-line"><strong>{e(t(lang, "digest_line", start=start, end=end))}</strong>'
                  f'<a href="digest.html">{e(t(lang, "read"))}</a></p>')
    td = (data.get("forecast") or {}).get("today")
    if td:
        digest = (f'<p class="slab digest-line"><strong>{e(t(lang, "fc_home", n=len(td["rows"]), d=td["date"]))}</strong>'
                  f'<a href="forecast.html">{e(t(lang, "fc_open"))}</a></p>') + digest

    body = f"""{header(lang, None, data['generated_at'])}
<main>
{hero}
{today}
{found}
{digest}
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
    ]
    return page(lang=lang, hid=None, base=base, title=t(lang, "site_title"), description=description[:320],
                body=body, charts={}, jsonld=jsonld, verification=verification)


def _crumbs(lang: str, base: str, key: str, name: str) -> dict:
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Crypto Research Labs", "item": page_url(base, lang)},
        {"@type": "ListItem", "position": 2, "name": name, "item": page_url(base, lang, key)}]}


def _monitor_card(lang: str, m: dict, charts: dict) -> str:
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
    value = band if m.get("metric") == "rule_state" else fmt_monitor(m)
    what = f'<details class="what"><summary>{e(t(lang, "what_is"))}</summary><p>{e(explain)}</p></details>' if explain else ""
    return (f'<article class="slab tilt card m"><h3>{e(label)}</h3><div class="value">{e(value)}</div>'
            f'<span class="band">{e(band)}</span>{note_html}{err}{spark}{what}</article>')


def _coins_table(lang: str, data: dict) -> str:
    rows = "".join(
        f'<tr{" class=watch" if c["symbol"] == "EVERUSDT" else ""}><td><a href="coins/{e(c["symbol"])}.html"><strong>{e(c["ticker"])}</strong>'
        f'<span class="sub">{e(c["name"])}</span></a></td>'
        f'<td class=num>{price(c["price"])}</td><td class=num>{pct(c["ch7"], True)}</td>'
        f'<td class=num>{pct(c["ch30"], True)}</td><td class=num>{pct(c["vs200"], True)}</td>'
        f'<td class=num>{pct(c["vol"], nd=0)}</td><td class=num>{pct(c.get("dd_peak"), True, 1 if abs(c.get("dd_peak") or 0) >= 0.995 else 0)}</td>'
        f'<td class=num>{usd(c.get("usd100"))}</td></tr>' for c in data.get("coins", []))
    if not rows:
        return ""
    return (f'<p>{e(t(lang, "coins_intro"))}</p><p class="meta sort-hint">{e(t(lang, "sort_hint"))}</p>'
            f'<div class="table-wrap"><table class="sortable" data-hint="{e(t(lang, "sort_hint"))}"><thead><tr>'
            f'<th>{e(t(lang, "th_coin"))}</th><th class=num>{e(t(lang, "th_price"))}</th><th class=num>{e(t(lang, "th_7d"))}</th>'
            f'<th class=num>{e(t(lang, "th_30d"))}</th><th class=num>{e(t(lang, "th_vs200"))}</th><th class=num>{e(t(lang, "th_vol"))}</th>'
            f'<th class=num>{e(t(lang, "th_peak"))}</th><th class=num>{e(t(lang, "th_100"))}</th></tr></thead><tbody>{rows}</tbody></table></div>')


def market_page(lang: str, data: dict, base: str, verification: str = "") -> str:
    charts: dict = {}
    groups: dict[str, list[str]] = {g: [] for g in GROUP_ORDER}
    watch = []
    for m in data["regime"]:
        g = MONITOR_GROUP.get(m["id"], "g_money")
        if g == "watch":
            watch.append(m)
            continue
        groups[g].append(_monitor_card(lang, m, charts))
    if data.get("btc"):
        bt = data["btc"]
        charts["btc"] = {"d": bt["close"]["d"], "log": True,
                         "series": [{"label": t(lang, "btc_close"), "v": bt["close"]["v"]},
                                    {"label": t(lang, "sma200"), "v": bt["sma200"]["v"], "dash": [6, 4]}]}
        last, sma = bt["close"]["v"][-1], bt["sma200"]["v"][-1]
        text = t(lang, "btc_text", price=f"${last:,.0f}", date=bt["close"]["d"][-1], diff=pct(last / sma - 1, True),
                 sma=f"${sma:,.0f}")
        groups["g_trend"].insert(0, f'<article class="slab tilt card m wide" id="btc"><h3>{e(t(lang, "btc_title"))}</h3>'
                                    f'<p>{text}</p><div class="chart"><canvas data-chart="btc" role="img" '
                                    f'aria-label="{e(t(lang, "btc_title"))}"></canvas></div></article>')
    sections = "".join(f'<section class="group" aria-labelledby="{g}"><h2 id="{g}">{cube(GROUP_COLOR[g])}{e(t(lang, g))}</h2>'
                       f'<div class="cards">{"".join(cs)}</div></section>' for g, cs in groups.items() if cs)
    notes = ""
    for m in watch:
        label, explain = sub(lang, "monitors", m["id"], (m["label"], m.get("explain", "")))
        note = sub(lang, "notes", (m["id"], m["band"]), m.get("note", ""))
        notes += (f'<div class="slab watchnote"><span class="badge wait">{e(t(lang, "watch_badge"))}</span><div>'
                  f'<p><strong>{e(label)}: {e(fmt_monitor(m))}</strong> · {e(sub(lang, "bands", m["band"], m["band"]))}</p>'
                  f'{f"<p>{e(note)}</p>" if note else ""}<p class="meta">{e(explain)}</p></div></div>')
    coins = _coins_table(lang, data)
    coins_section = (f'<section class="group" aria-labelledby="coins"><h2 id="coins">{cube(GROUP_COLOR["g_coins"])}'
                     f'{e(t(lang, "g_coins"))}</h2>{coins}{notes}</section>') if coins or notes else ""
    late = [d for d in data["data"] if (d.get("lag_days") or 0) > 1]
    fresh = (f'<span class="ok">{e(t(lang, "fresh_ok", date=data["generated_at"][:10]))}</span>' if not late else
             "".join(f'<span>{e(t(lang, "fresh_late", series=d["series"], n=d["lag_days"]))}</span>' for d in late))
    date = (data.get("btc") or {}).get("close", {}).get("d", [data["generated_at"][:10]])[-1]
    body = f"""{header(lang, "market", data['generated_at'])}
<main>
<p class="eyebrow">{e(t(lang, 'market_eyebrow', date=date))}</p>
<h1>{e(t(lang, 'market_h1'))}</h1>
<p class="lead">{e(t(lang, 'market_lead'))}</p>
<section aria-labelledby="diagnosis">{diag_card(lang, data, short=False)}</section>
{sections}
{coins_section}
<p class="fresh">{fresh}<a href="about.html#data">{e(t(lang, 'fresh_link'))}</a></p>
</main>
{footer(lang, "market")}"""
    url = page_url(base, lang, "market")
    jsonld = [{"@context": "https://schema.org", "@type": "WebPage", "name": t(lang, "market_h1"),
               "description": t(lang, "market_lead"), "url": url, "inLanguage": LANGS[lang][1],
               "dateModified": data["generated_at"][:10]}, _crumbs(lang, base, "market", t(lang, "nav_market"))]
    return page(lang=lang, hid="market", base=base, title=f"{t(lang, 'market_h1')} | Crypto Research Labs",
                description=t(lang, "market_lead")[:320], body=body, charts=charts, jsonld=jsonld,
                verification=verification)


def research_page(lang: str, data: dict, base: str, verification: str = "") -> str:
    hyps = data["hypotheses"]
    cnt, b = _counts(hyps), _badges(lang)
    blocks = "".join(f'<button type="button" class="vblock {cls}" data-filter="{f}" aria-pressed="false">'
                     f'<b>{k}</b><span>{e(word)}</span></button>' for cls, f, k, word in (
        ("pass", "PASS", cnt["PASS"], t(lang, "tally_pass")), ("weak", "WEAK", cnt["WEAK"], t(lang, "tally_weak")),
        ("fail", "FAIL", cnt["FAIL"], t(lang, "tally_fail")), ("wait", "NONE", cnt[None], t(lang, "tally_wait"))) if k)
    rows = []
    for h in hyps:
        when = (h.get("run_at") or "")[:10] or (h["history"][-1]["date"] if h["history"] else "")
        href = f'hypotheses/{e(h["id"])}.html'
        rows.append(f'<tr data-verdict="{e(h["verdict"] or "NONE")}"><td><a href="{href}">{e(h["id"])}</a></td>'
                    f'<td><a href="{href}">{e(title_of(lang, h))}</a></td>'
                    f'<td>{e(sub(lang, "families", h["family"], h["family"]))}</td>'
                    f'<td>{badge(lang, h["verdict"])}{progress_bar(lang, h.get("progress"), True)}</td>'
                    f'<td class=num>{e(when)}</td></tr>')
    steps = t(lang, "flow_steps")
    flow = "".join(f'<li class="slab">{e(s)}</li>' for s in steps)
    body = f"""{header(lang, "research", data['generated_at'])}
<main>
<h1>{e(t(lang, 'research_h1'))}</h1>
<p class="lead">{e(t(lang, 'research_lead'))}</p>
<p class="slab digest-line"><a href="forecast.html"><strong>{e(t(lang, 'fc_research'))}</strong></a></p>
<div class="vblocks" role="group" aria-label="{e(t(lang, 'th_verdict'))}">
<button type="button" class="vblock all" data-filter="ALL" aria-pressed="true"><b>{len(hyps)}</b><span>{e(t(lang, 'filter_all'))}</span></button>
{blocks}</div>
<p class="meta">{t(lang, 'hyp_intro', **b)}</p>
<section aria-labelledby="all"><h2 id="all">{e(t(lang, 'all_h'))}</h2>
<p class="meta sort-hint">{e(t(lang, 'sort_hint'))}</p>
<div class="table-wrap"><table class="sortable" id="hyp-table" data-hint="{e(t(lang, 'sort_hint'))}"><thead><tr>
<th>{e(t(lang, 'th_id'))}</th><th>{e(t(lang, 'th_hyp'))}</th><th>{e(t(lang, 'th_family'))}</th>
<th>{e(t(lang, 'th_verdict'))}</th><th>{e(t(lang, 'th_tested'))}</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>
</section>
{scan_matrix(lang, data)}
<section aria-labelledby="how-we-test"><h2 id="how-we-test">{e(t(lang, 'method_short_h'))}</h2>
<ol class="flow3d">{flow}</ol>
<p><a href="about.html#methodology">{e(t(lang, 'method_title'))} →</a> · <a href="{REPO}/blob/main/CONTRIBUTING.md">{e(t(lang, 'propose'))}</a></p>
</section>
</main>
{footer(lang, "research")}"""
    url = page_url(base, lang, "research")
    jsonld = [{"@context": "https://schema.org", "@type": "CollectionPage", "name": t(lang, "research_h1"),
               "description": t(lang, "research_lead"), "url": url, "inLanguage": LANGS[lang][1],
               "dateModified": data["generated_at"][:10],
               "hasPart": [{"@type": "TechArticle", "headline": f'{h["id"]}: {title_of(lang, h)}'[:110],
                            "url": page_url(base, lang, h["id"])} for h in hyps]},
              _crumbs(lang, base, "research", t(lang, "nav_research"))]
    return page(lang=lang, hid="research", base=base, title=f"{t(lang, 'research_h1')} | Crypto Research Labs",
                description=t(lang, "research_lead")[:320], body=body, charts={}, jsonld=jsonld,
                verification=verification)


def about_page(lang: str, data: dict, base: str, verification: str = "") -> str:
    hyps = data["hypotheses"]
    n, n_pass = len(hyps), sum(h["verdict"] == "PASS" for h in hyps)
    verdict_line = t(lang, "verdict_some", p=n_pass, n=n) if n_pass else t(lang, "verdict_none", n=n)
    method = "".join(f"<li>{s}</li>" for s in t(lang, "method"))
    fresh = "".join(f'<tr><td>{e(d["series"])}</td><td class=num>{e(d.get("first") or "—")}</td>'
                    f'<td class=num>{e(d.get("last") or "—")}</td>'
                    f'<td class=num>{"—" if d.get("lag_days") is None else d["lag_days"]}</td></tr>'
                    for d in data["data"])
    setup = SG.GUIDE.get(lang, SG.GUIDE["en"])["nav"]
    body = f"""{header(lang, "about", data['generated_at'])}
<main>
<h1>{e(t(lang, 'about_h1'))}</h1>
<p class="lead">{e(t(lang, 'lead', verdict=verdict_line))}</p>
<section aria-labelledby="how-it-runs"><h2 id="how-it-runs">{e(t(lang, 'about_how_h'))}</h2><p>{e(t(lang, 'about_how'))}</p></section>
<section aria-labelledby="methodology"><h2 id="methodology">{e(t(lang, 'method_title'))}</h2>
<ul>{method}</ul>
<p>{e(t(lang, 'method_more'))}: <a href="{REPO}/blob/main/docs/METHODOLOGY.md">METHODOLOGY.md</a>
· <a href="{REPO}/blob/main/docs/FINDINGS.md">FINDINGS.md</a></p></section>
<section aria-labelledby="data"><h2 id="data">{e(t(lang, 'data_title'))}</h2>
<div class="table-wrap"><table><thead><tr><th>{e(t(lang, 'th_series'))}</th><th>{e(t(lang, 'th_from'))}</th>
<th>{e(t(lang, 'th_last'))}</th><th>{e(t(lang, 'th_behind'))}</th></tr></thead><tbody>{fresh}</tbody></table></div>
<p class="meta">{e(t(lang, 'updated', t=data['generated_at']))}</p></section>
<section aria-labelledby="links"><h2 id="links">{e(t(lang, 'about_links_h'))}</h2>
<ul><li><a href="setup.html">{e(setup)}</a></li><li><a href="{asset_root(lang, 'about')}data.json">{e(t(lang, 'footer_data'))}</a> (data.json)</li>
<li><a href="{REPO}">GitHub</a> · MIT License</li></ul></section>
</main>
{footer(lang, "about")}"""
    url = page_url(base, lang, "about")
    jsonld = [{"@context": "https://schema.org", "@type": "AboutPage", "name": t(lang, "about_h1"),
               "description": t(lang, "lead", verdict=verdict_line)[:300], "url": url, "inLanguage": LANGS[lang][1],
               "dateModified": data["generated_at"][:10]}, _crumbs(lang, base, "about", t(lang, "nav_about"))]
    return page(lang=lang, hid="about", base=base, title=f"{t(lang, 'about_h1')} | Crypto Research Labs",
                description=t(lang, "lead", verdict=verdict_line)[:320], body=body, charts={}, jsonld=jsonld,
                verification=verification)


GATE_SYMBOLS = ("EVERUSDT", "GRAMUSDT")


def _f(v, fmt) -> str:
    return "—" if v is None else format(v, fmt)


def forecast_results_table(lang: str, rows: list[dict]) -> str:
    """Per-coin (and pooled) scores of a forecast hypothesis."""
    if not rows:
        return f"<p>{e(t(lang, 'no_results'))}</p>"
    port = any("sharpe" in r for r in rows)
    cols = ["c_asset", "c_days", "c_bss", "c_p", "c_q", "c_hits"] + (["c_sharpe", "c_hsharpe", "c_csharpe", "c_exp"] if port else [])
    head = "<tr>" + "".join(f"<th>{e(t(lang, c))}</th>" for c in cols) + "</tr>"
    body = []
    for r in rows:
        name = "∑" if r["symbol"] == "ALL" else e(r["symbol"].removesuffix("USDT"))
        cells = [f"<td><strong>{name}</strong></td>", f"<td class=num>{r.get('days', '—')}</td>",
                 f"<td class=num>{_f(r.get('bss'), '+.4f')}</td>", f"<td class=num>{_f(r.get('p'), '.3f')}</td>",
                 f"<td class=num>{_f(r.get('q'), '.3f')}</td>", f"<td class=num>{pct(r.get('hits'), nd=1)}</td>"]
        if port:
            cells += [f"<td class=num>{num(r.get('sharpe'))}</td>", f"<td class=num>{num(r.get('hold_sharpe'))}</td>",
                      f"<td class=num>{num(r.get('const_sharpe'))}</td>", f"<td class=num>{pct(r.get('exposure'), nd=0)}</td>"]
        body.append("<tr>" + "".join(cells) + "</tr>")
    return f'<div class="table-wrap"><table><thead>{head}</thead><tbody>{"".join(body)}</tbody></table></div>'


def calibration_table(lang: str, bins: list[dict]) -> str:
    if not bins:
        return ""
    rows = "".join(f'<tr><td>{b["lo"]:.0%}–{b["hi"]:.0%}</td><td class=num>{pct(b["p"], nd=1)}</td>'
                   f'<td class=num>{pct(b["y"], nd=1)}</td><td class=num>{b["n"]}</td></tr>' for b in bins)
    return (f'<h2 id="calibration">{e(t(lang, "cal_h"))}</h2><div class="table-wrap"><table><thead><tr>'
            f'<th>{e(t(lang, "cal_said"))}</th><th class=num>{e(t(lang, "cal_said"))} ⌀</th>'
            f'<th class=num>{e(t(lang, "cal_happened"))}</th><th class=num>{e(t(lang, "cal_n"))}</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div>')


def _coin_label(c: dict | None, sym: str, prefix: str = "") -> str:
    tick = (c or {}).get("ticker") or sym.removesuffix("USDT")
    name = (c or {}).get("name") or ""
    gate = " †" if sym in GATE_SYMBOLS else ""
    return f'<a href="{prefix}coins/{e(sym)}.html"><strong>{e(tick)}</strong>{gate}<span class="sub">{e(name)}</span></a>'


def forecast_page(lang: str, data: dict, base: str, verification: str = "") -> str:
    fc = data.get("forecast") or {}
    coins = {c["symbol"]: c for c in data.get("coins", [])}
    n = len((next((h for h in data["hypotheses"] if h["id"] == "H-029"), {}).get("spec") or {}).get("universe", [])) or 13
    td = fc.get("today")
    if td:
        var_ids = sorted({k for r in td["rows"] for k in (r.get("variants") or {})})
        rows = []
        for r in td["rows"]:
            ch = "—"
            if r.get("w_exec") is not None and r.get("w_prev") is not None:
                ch = t(lang, "fc_pp", v=f"{(r['w_exec'] - r['w_prev']) * 100:+.0f}")
            var_cells = "".join(f'<td class=num>{pct((r.get("variants") or {}).get(v), nd=0)}</td>' for v in var_ids)
            rows.append(f'<tr><td>{_coin_label(coins.get(r["symbol"]), r["symbol"])}</td>'
                        f'<td class=num>{pct(r.get("p_direction"), nd=0)}</td>{var_cells}<td class=num>{pct(r.get("p_risk"), nd=0)}</td>'
                        f'<td class=num>{pct(r.get("w_exec"), nd=0)}</td><td class=num>{e(ch)}</td></tr>')
        late = "" if td["on_time"] else f'<p class="callout">{e(t(lang, "fc_late"))}</p>'
        stamp = td["published"].replace("T", " ").replace("Z", " UTC")
        today = (f'<p class="meta">{e(t(lang, "fc_published", t=stamp, d=td["decision_date"]))}</p>{late}'
                 f'<p class="meta sort-hint">{e(t(lang, "sort_hint"))}</p>'
                 f'<div class="table-wrap"><table class="sortable" data-hint="{e(t(lang, "sort_hint"))}"><thead><tr>'
                 f'<th>{e(t(lang, "th_coin"))}</th><th class=num>{e(t(lang, "fc_th_up"))}</th>'
                 + "".join(f'<th class=num>{e(t(lang, "fc_th_up_v2", id=v))}</th>' for v in var_ids) +
                 f'<th class=num>{e(t(lang, "fc_th_move"))}</th><th class=num>{e(t(lang, "fc_th_share"))}</th>'
                 f'<th class=num>{e(t(lang, "fc_th_change"))}</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
                 f'<p class="meta">{e(t(lang, "fc_gate"))}</p>')
    else:
        today = f'<p class="callout">{e(t(lang, "fc_none"))}</p>'

    live = fc.get("live") or {}
    start, test_after = fc.get("start") or "—", fc.get("test_after") or "—"
    role = lambda target, variant: next((v for v in live.values() if v["target"] == target and v["variant"] == variant), None)
    base_d, base_r = role("direction", False), role("risk", False)
    variants = {hid: v for hid, v in live.items() if v["variant"]}
    if base_d:
        pd_, pr_ = base_d["pooled"], (base_r or {}).get("pooled") or {}
        kv = [(t(lang, "fc_days"), str(pd_.get("days", "—"))), (t(lang, "fc_hits"), pct(pd_.get("hits"), nd=1)),
              (t(lang, "fc_skill_dir"), _f(pd_.get("bss"), "+.4f")), (t(lang, "fc_skill_risk"), _f(pr_.get("bss"), "+.4f"))]
        kv += [(t(lang, "fc_skill_v2", id=hid), _f(v["pooled"].get("bss"), "+.4f")) for hid, v in sorted(variants.items())]
        tiles = "".join(f'<div class="slab stat"><span>{e(k)}</span><b>{e(v)}</b></div>' for k, v in kv)
        monthly = base_d.get("monthly") or []
        month_html = ""
        if monthly:
            last = max(m["month"] for m in monthly)
            vmon = {hid: {m["symbol"]: m for m in (v.get("monthly") or []) if m["month"] == last}
                    for hid, v in sorted(variants.items())}
            vmon = {hid: x for hid, x in vmon.items() if x}
            mrows = "".join(f'<tr><td>{_coin_label(coins.get(m["symbol"]), m["symbol"])}</td><td class=num>{usd(m["model"])}</td>'
                            + "".join(f'<td class=num>{usd((x.get(m["symbol"]) or {}).get("model"))}</td>' for x in vmon.values())
                            + f'<td class=num>{usd(m["hold"])}</td><td class=num>{usd(m["const"])}</td></tr>'
                            for m in monthly if m["month"] == last)
            month_html = (f'<h3>{e(t(lang, "fc_month_h", m=last))}</h3><div class="table-wrap"><table><thead><tr>'
                          f'<th>{e(t(lang, "th_coin"))}</th><th class=num>{e(t(lang, "fc_th_model"))}</th>'
                          + "".join(f'<th class=num>{e(t(lang, "fc_th_model_v2", id=hid))}</th>' for hid in vmon)
                          + f'<th class=num>{e(t(lang, "fc_th_hold"))}</th><th class=num>{e(t(lang, "fc_th_const"))}</th>'
                          f'</tr></thead><tbody>{mrows}</tbody></table></div><p class="meta">{e(t(lang, "fc_month_note"))}</p>')
        live_html = (f'<p>{e(t(lang, "fc_live_text", start=start, date=test_after))}</p><div class="stats">{tiles}</div>'
                     f'<p class="meta">{e(t(lang, "fc_skill_note"))}</p>{month_html}')
    else:
        live_html = (f'<p>{e(t(lang, "fc_live_text", start=start, date=test_after))}</p>'
                     f'<p class="callout">{e(t(lang, "fc_live_wait"))}</p>')

    hist = fc.get("history") or {}
    items = []
    for target, label in (("direction", "fc_back_dir"), ("risk", "fc_back_risk")):
        h = hist.get(target)
        if not h:
            continue
        pooled = h.get("pooled") or {}
        line = (e(t(lang, "fc_back_line", bss=_f(pooled.get("bss"), "+.4f"), p=_f(pooled.get("p"), ".3f")))
                if h.get("verdict") else e(t(lang, "fc_back_wait")))
        items.append(f'<li><a href="hypotheses/{e(h["id"])}.html">{e(h["id"])}</a> · {e(t(lang, label))}: '
                     f'{badge(lang, h.get("verdict"))} {line}</li>')
    how = "".join(f"<li>{x}</li>" for x in t(lang, "fc_how"))
    body = f"""{header(lang, "forecast", data['generated_at'])}
<main>
<p class="meta crumbs"><a href="research.html">← {e(t(lang, 'nav_research'))}</a></p>
<h1>{e(t(lang, 'fc_h1'))}</h1>
<p class="lead">{e(t(lang, 'fc_lead', n=n))}</p>
<section aria-labelledby="today">{today}</section>
<section aria-labelledby="live"><h2 id="live">{e(t(lang, 'fc_live_h'))}</h2>{live_html}</section>
<section aria-labelledby="history"><h2 id="history">{e(t(lang, 'fc_back_h'))}</h2>
<p>{e(t(lang, 'fc_back_text'))}</p><ul>{''.join(items)}</ul></section>
<section aria-labelledby="how"><h2 id="how">{e(t(lang, 'fc_how_h'))}</h2><ul>{how}</ul></section>
</main>
{footer(lang, "forecast")}"""
    url = page_url(base, lang, "forecast")
    jsonld = [{"@context": "https://schema.org", "@type": "Dataset", "name": t(lang, "fc_h1"),
               "description": t(lang, "fc_lead", n=n), "url": url, "inLanguage": LANGS[lang][1],
               "license": "https://opensource.org/licenses/MIT", "isAccessibleForFree": True,
               "creator": {"@type": "Person", "name": "F1DevBin", "url": "https://github.com/f1devbin"},
               "dateModified": (td or {}).get("date") or data["generated_at"][:10],
               "distribution": [{"@type": "DataDownload", "encodingFormat": "text/csv",
                                 "contentUrl": f"{REPO}/blob/main/datasets/forecast_log.csv"}]},
              _crumbs(lang, base, "forecast", t(lang, "fc_h1"))]
    return page(lang=lang, hid="forecast", base=base, title=f"{t(lang, 'fc_h1')} | Crypto Research Labs",
                description=t(lang, "fc_lead", n=n)[:320], body=body, charts={}, jsonld=jsonld,
                verification=verification)


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
<p class="meta crumbs"><a href="../research.html#all">{e(t(lang, 'back'))}</a></p>
<h1>{e(hid)}: {e(title)}</h1>
<p>{badge(lang, h['verdict'])} &nbsp;{e(t(lang, 'family'))}: <strong>{e(sub(lang, 'families', h['family'], h['family']))}</strong>
· {e(t(lang, 'status'))}: <strong>{e(sub(lang, 'statuses', h['status'], h['status']))}</strong></p>
{caution}
<p class="plain"><strong>{e(t(lang, 'in_plain'))}:</strong> {e(plain(lang, h['verdict'], h.get('test_after')))}</p>
{progress_bar(lang, h.get('progress'))}
<h2>{e(t(lang, 'result_h'))}</h2>
{en_note}
<p lang="en">{e(h['summary'])}</p>
<p class="meta">{e(t(lang, 'metrics_note'))} <a href="../course.html#glossary">{e(t(lang, 'nav_glossary'))}</a></p>
{forecast_results_table(lang, h['rows']) if (h.get('spec') or {}).get('kind') in ('forecast', 'forecast_live') else results_table(lang, h['rows'], (h.get('spec') or {}).get('kind', ''))}
{calibration_table(lang, h.get('calibration') or [])}
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
<p class="meta crumbs"><a href="../market.html#coins">{e(t(lang, 'back_coins'))}</a></p>
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
<p class="meta"><a href="../course.html#glossary">{e(t(lang, 'nav_glossary'))}</a></p>
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
    how = "".join(f"<li>{x.format(**_badges(lang))}</li>" for x in t(lang, "how2"))
    glossary = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in t(lang, "glossary"))
    parts = []
    for i, (title, md) in enumerate(lessons, 1):
        parts.append(f'<section aria-labelledby="lesson-{i}"><h2 id="lesson-{i}">{e(ui["lesson"].format(n=i))}. '
                     f'{e(title)}</h2>{C.md_to_html(C.fill(md, values), flow)}</section>')
    body = f"""{header(lang, "course", data['generated_at'])}
<main>
<h1>{e(ui['h1'])}</h1>
<p><span class="beginner">{e(ui['badge'])}</span></p>
<p class="lead">{e(ui['lead'])}</p>
<section aria-labelledby="read" class="slab howto"><h2 id="read">{e(t(lang, 'read_h'))}</h2>
<ol class="steps">{how}</ol></section>
<h2>{e(ui['toc'])}</h2>
<ol class="toc">{toc}</ol>
{''.join(parts)}
<section aria-labelledby="glossary"><h2 id="glossary">{e(t(lang, 'glossary_title'))}</h2>{glossary}</section>
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
              {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": LANGS[lang][1], "mainEntity": [
                  {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                  for q, a in t(lang, "glossary")]},
              {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                  {"@type": "ListItem", "position": 1, "name": "Crypto Research Labs", "item": page_url(base, lang)},
                  {"@type": "ListItem", "position": 2, "name": ui["h1"], "item": url}]}]
    return page(lang=lang, hid="course", base=base, title=ui["title"], description=ui["desc"][:320], body=body,
                charts={}, jsonld=jsonld, verification=verification)


def _digest_block(lang: str, d: dict, level: str = "h2") -> str:
    text = d["texts"].get(lang)
    note = ""
    if text is None:
        text = d["texts"].get("en") or next(iter(d["texts"].values()))
        note = f'<p class="meta">{e(t(lang, "digest_fallback"))}</p>'
    week, start, end = _digest_range(d)
    head = e(t(lang, "digest_week", week=week, start=start, end=end))
    return (f'<article class="digest"><{level} id="{e(d["week"])}">{head}</{level}>{note}{C.md_to_html(text)}'
            f'<p class="meta">{e(t(lang, "digest_model", model=d.get("model") or "—"))}</p></article>')


def digest_page(lang: str, data: dict, base: str, verification: str = "") -> str:
    ds = data.get("digests") or []
    items = "".join(_digest_block(lang, d) for d in ds) or f'<p class="callout">{e(t(lang, "digest_empty"))}</p>'
    body = f"""{header(lang, "digest", data['generated_at'])}
<main>
<h1>{e(t(lang, 'digest_h1'))}</h1>
<p class="lead">{e(t(lang, 'digest_lead'))}</p>
{items}
<p class="meta"><a href="{REPO}/tree/main/reports/digest">GitHub: reports/digest</a></p>
</main>
{footer(lang, "digest")}"""
    url = page_url(base, lang, "digest")
    jsonld = [{"@context": "https://schema.org", "@type": "CollectionPage", "name": t(lang, "digest_title"),
               "description": t(lang, "digest_desc"), "url": url, "inLanguage": LANGS[lang][1],
               "dateModified": (ds[0]["date"] if ds else data["generated_at"][:10]),
               "hasPart": [{"@type": "Article", "headline": t(lang, "digest_week", week=_digest_range(d)[0],
                                                              start=_digest_range(d)[1], end=_digest_range(d)[2]),
                            "datePublished": d["date"], "url": f"{url}#{d['week']}"} for d in ds]},
              {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                  {"@type": "ListItem", "position": 1, "name": "Crypto Research Labs", "item": page_url(base, lang)},
                  {"@type": "ListItem", "position": 2, "name": t(lang, "digest_title"), "item": url}]}]
    return page(lang=lang, hid="digest", base=base, title=f"{t(lang, 'digest_title')} | Crypto Research Labs",
                description=t(lang, "digest_desc")[:320], body=body, charts={}, jsonld=jsonld, verification=verification)


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

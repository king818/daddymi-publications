#!/usr/bin/env python3
"""Generate index.html (GitHub Pages front-end) and PUBLICATIONS.md (no-JS fallback)
from publications.yaml — the single source of truth.

Usage:  python3 generate.py
Rule:   NEVER hand-edit index.html or PUBLICATIONS.md. Edit publications.yaml, re-run this.
Requires: Python 3 + PyYAML. The generated HTML itself has zero dependencies.
"""
import json, html, datetime
import yaml

BASE = "https://king818.github.io/daddymi-publications/"

with open("publications.yaml", encoding="utf-8") as f:
    DATA = yaml.safe_load(f)

PUBS = DATA.get("publications", [])
PRIV = DATA.get("replaced_or_private", [])
UNV = DATA.get("unverified", [])

LANG_LABEL = {"zh": "中文", "en": "English", "": "—"}

def sort_key(r):
    return (r.get("published") or "", r.get("series") or "", r.get("topic") or "")

PUBS = sorted(PUBS, key=sort_key, reverse=True)
PRIV = sorted(PRIV, key=sort_key, reverse=True)

from collections import Counter
plat_counts = Counter(r["platform"] for r in PUBS)
series_counts = Counter(r["series"] for r in PUBS)
series_list = sorted(series_counts)
platforms = sorted(plat_counts)
langs = sorted({r["language"] for r in PUBS if r["language"]})
types = sorted({r["type"] for r in PUBS})
today = datetime.date.today().isoformat()

# ---------------- PUBLICATIONS.md ----------------
def md_table(rows):
    out = ["| Published | Series | Topic | Lang | Type | Title | Video ID | Playlist | Archive | Status |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        title_link = f"[{r['title']}]({r['url']})" if r.get("url") else r["title"]
        out.append("| {published} | {series} | {topic} | {lang} | {type} | {title} | `{nid}` | {playlist} | {arch} | {status} |".format(
            published=r["published"], series=r["series"], topic=r["topic"],
            lang=LANG_LABEL.get(r["language"], r["language"]), type=r["type"], title=title_link,
            nid=r["native_id"], playlist=r["playlist"] or "—",
            arch=r["archive_note"] or "—", status=r["status"]))
    return "\n".join(out)

md = []
md.append("# Publications — full tables (no-JS fallback)\n")
md.append("Generated from `publications.yaml` by `generate.py` — do not hand-edit. "
          f"Live, filterable version: {BASE}\n")
md.append(f"**{len(PUBS)} public videos** · {len(PRIV)} replaced/private versions · "
          + " · ".join(f"{s}: {series_counts[s]}" for s in series_list) + "\n")
for s in series_list:
    rows = [r for r in PUBS if r["series"] == s]
    md.append(f"\n## {s} ({len(rows)})\n")
    md.append(md_table(rows))
if PRIV:
    md.append(f"\n## Replaced / Private versions ({len(PRIV)})\n")
    md.append("Same productions, kept for the record — not public.\n")
    md.append(md_table(PRIV))
if UNV:
    md.append("\n## Unverified / pending\n")
    for u in UNV:
        md.append(f"- **{u['item']}** — {u['reason']} Next: {u['action']}")
md.append("")
open("PUBLICATIONS.md", "w", encoding="utf-8").write("\n".join(md))

# ---------------- index.html ----------------
def embed(rows):
    return json.dumps(rows, ensure_ascii=False).replace("</", "<\\/")

html_doc = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Daddy Mi — Publications Index</title>
<style>
  :root { --ink:#1c2430; --mut:#5b6675; --line:#dfe3ea; --gold:#C9A764; --bg:#f7f4ec; }
  * { box-sizing: border-box; }
  body { margin:0; font-family:-apple-system, "Helvetica Neue", Arial, "PingFang TC", "Microsoft JhengHei", sans-serif; color:var(--ink); background:#fff; }
  header { background:#0B1220; color:#F7F4EC; padding:20px 16px 16px; }
  header h1 { margin:0 0 4px; font-size:22px; }
  header p { margin:0; color:#cdbf9f; font-size:13px; }
  .counts { display:flex; flex-wrap:wrap; gap:8px; margin-top:12px; }
  .chip { background:#16213a; border:1px solid #2c3c5f; border-radius:999px; padding:4px 10px; font-size:12.5px; }
  .chip b { color:var(--gold); }
  .controls { position:sticky; top:0; background:#fff; border-bottom:1px solid var(--line); padding:10px 12px; display:flex; flex-wrap:wrap; gap:8px; z-index:5; }
  .controls select, .controls input { font-size:14px; padding:7px 8px; border:1px solid var(--line); border-radius:8px; }
  .controls input { flex:1 1 160px; }
  main { padding:6px 12px 30px; }
  h2 { font-size:16px; margin:20px 0 6px; border-left:4px solid var(--gold); padding-left:8px; }
  table { width:100%; border-collapse:collapse; font-size:13.5px; }
  th, td { text-align:left; padding:7px 8px; border-bottom:1px solid var(--line); vertical-align:top; }
  th { color:var(--mut); font-weight:600; font-size:12px; }
  td a { color:#1757a8; text-decoration:none; }
  td a:hover { text-decoration:underline; }
  .meta { color:var(--mut); font-size:12px; }
  .status { font-size:12px; }
  .priv { background:var(--bg); }
  .unv { background:#fdf6e3; border:1px solid #eadfc0; border-radius:10px; padding:10px 14px; margin-top:10px; font-size:13.5px; }
  @media (max-width:760px) {
    table, thead, tbody, th, td, tr { display:block; }
    thead { display:none; }
    tr { border:1px solid var(--line); border-radius:10px; margin:10px 0; padding:6px 4px; }
    td { border:none; padding:3px 8px; }
    td.t { font-weight:600; font-size:14.5px; }
  }
</style>
</head>
<body>
<header>
  <h1>米老爸 Daddy Mi — Publications Index</h1>
  <p>Every video our production has published, in one place. Data: publications.yaml · Updated __TODAY__</p>
  <div class="counts">__CHIPS__</div>
</header>
<div class="controls">
  <input id="q" type="search" placeholder="Search title / topic / video ID…">
  <select id="fPlatform"><option value="">All platforms</option>__PLAT_OPTS__</select>
  <select id="fSeries"><option value="">All series</option>__SERIES_OPTS__</select>
  <select id="fLang"><option value="">All languages</option>__LANG_OPTS__</select>
  <select id="fType"><option value="">All types</option>__TYPE_OPTS__</select>
</div>
<main>
  <div id="list"></div>
  __UNV_HTML__
</main>
<script>
const PUBS = __PUBS_JSON__;
const PRIV = __PRIV_JSON__;
const LANG = {"zh":"中文","en":"English","":"—"};
const $ = id => document.getElementById(id);
function row(r, priv) {
  const link = r.url ? '<a href="'+r.url+'" target="_blank" rel="noopener">'+escapeHtml(r.title)+'</a>' : escapeHtml(r.title);
  return '<tr'+(priv?' class="priv"':'')+'>'
    + '<td class="t">'+link+'</td>'
    + '<td>'+r.published+'</td>'
    + '<td>'+escapeHtml(r.topic)+'</td>'
    + '<td>'+(LANG[r.language]||r.language)+'</td>'
    + '<td>'+escapeHtml(r.type)+'</td>'
    + '<td class="meta">'+escapeHtml(r.native_id)+'</td>'
    + '<td class="meta">'+escapeHtml(r.playlist||'—')+'</td>'
    + '<td class="meta">'+(r.archive_note?escapeHtml(r.archive_note):'—')+'</td>'
    + '<td class="status">'+escapeHtml(r.status)+'</td></tr>';
}
function escapeHtml(s){return String(s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));}
function render() {
  const q = $('q').value.trim().toLowerCase(), fp=$('fPlatform').value, fs=$('fSeries').value, fl=$('fLang').value, ft=$('fType').value;
  const match = r => (!fp||r.platform===fp)&&(!fs||r.series===fs)&&(!fl||r.language===fl)&&(!ft||r.type===ft)
    &&(!q||(r.title+' '+r.topic+' '+r.native_id+' '+r.series).toLowerCase().includes(q));
  let h = '';
  const groups = {};
  PUBS.filter(match).forEach(r=>{(groups[r.series]=groups[r.series]||[]).push(r);});
  Object.keys(groups).sort().forEach(s=>{
    h += '<h2>'+escapeHtml(s)+' ('+groups[s].length+')</h2><table><thead><tr><th>Title</th><th>Published</th><th>Topic</th><th>Lang</th><th>Type</th><th>Video ID</th><th>Playlist</th><th>Archive</th><th>Status / next check</th></tr></thead><tbody>'
      + groups[s].map(r=>row(r,false)).join('') + '</tbody></table>';
  });
  const priv = PRIV.filter(match);
  if (priv.length) {
    h += '<h2>Replaced / Private versions ('+priv.length+')</h2><table><thead><tr><th>Title</th><th>Published</th><th>Topic</th><th>Lang</th><th>Type</th><th>Video ID</th><th>Playlist</th><th>Archive</th><th>Status / next check</th></tr></thead><tbody>'
      + priv.map(r=>row(r,true)).join('') + '</tbody></table>';
  }
  if (!h) h = '<p class="meta">No matches.</p>';
  $('list').innerHTML = h;
}
['q','fPlatform','fSeries','fLang','fType'].forEach(id=>{ $(id).addEventListener('input', render); $(id).addEventListener('change', render); });
render();
</script>
</body>
</html>
"""

chips = [f"<span class='chip'><b>{len(PUBS)}</b> public videos</span>"]
chips += [f"<span class='chip'>{html.escape(p)}: <b>{plat_counts[p]}</b></span>" for p in platforms]
chips += [f"<span class='chip'>{html.escape(s)}: <b>{series_counts[s]}</b></span>" for s in series_list]
chips.append(f"<span class='chip'><b>{len(PRIV)}</b> replaced/private</span>")

unv_html = ""
if UNV:
    items = "".join(f"<p><b>{html.escape(u['item'])}</b> — {html.escape(u['reason'])} Next: {html.escape(u['action'])}</p>" for u in UNV)
    unv_html = f"<h2>Unverified / pending</h2><div class='unv'>{items}</div>"

html_doc = (html_doc
    .replace("__TODAY__", today)
    .replace("__CHIPS__", "".join(chips))
    .replace("__PLAT_OPTS__", "".join(f"<option>{html.escape(p)}</option>" for p in platforms))
    .replace("__SERIES_OPTS__", "".join(f"<option>{html.escape(s)}</option>" for s in series_list))
    .replace("__LANG_OPTS__", "".join(f"<option value='{l}'>{LANG_LABEL.get(l,l)}</option>" for l in langs))
    .replace("__TYPE_OPTS__", "".join(f"<option>{html.escape(t)}</option>" for t in types))
    .replace("__UNV_HTML__", unv_html)
    .replace("__PUBS_JSON__", embed(PUBS))
    .replace("__PRIV_JSON__", embed(PRIV)))
open("index.html", "w", encoding="utf-8").write(html_doc)
print(f"generated index.html + PUBLICATIONS.md — {len(PUBS)} public, {len(PRIV)} private, {len(UNV)} unverified")

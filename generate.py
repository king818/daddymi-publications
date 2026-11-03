#!/usr/bin/env python3
"""Generate index.html (GitHub Pages front-end) and PUBLICATIONS.md (no-JS fallback)
from publications.yaml — the single source of truth.

Usage:  python3 generate.py
Rule:   NEVER hand-edit index.html or PUBLICATIONS.md. Edit publications.yaml, re-run this.
Requires: Python 3 + PyYAML. The generated HTML itself has zero dependencies.

Presentation standard (boss, 2026-11-03): every row's main label must be human
positioning — what it is, which number, what it covers — readable without any ID.
Video IDs and archive GUIDs appear only as small secondary text (GUIDs as short
codes). Blocks are split by series x language, headings carry counts.
"""
import json, html, datetime, re
import yaml

BASE = "https://king818.github.io/daddymi-publications/"

# ---------------- display derivation (no yaml structure change) ----------------

SERIES_DISP = {
    "Come, Follow Me 2026": {"zh": "來跟隨我 2026", "en": "Come, Follow Me 2026"},
    "Daily Verse · Neville Readings": {"zh": "每日經文 · Neville 解讀", "en": "Daily Verse · Neville Readings"},
    "General Conference Talks (Elders Quorum)": {"zh": "總會大會 · 長老定額組討論", "en": "General Conference Talks (Elders Quorum)"},
    "Neville Inner Reading Podcast": {"zh": "Neville 內在解讀播客", "en": "Neville Inner Reading Podcast"},
    "Finance Basics": {"zh": "財經基礎 · 錢的知識", "en": "Finance Basics"},
}

def lang_group(lang):
    return "zh" if (lang or "").startswith("zh") else "en"

def _clean_title(t):
    """Unwrap YAML-artifact quoting stored literally in a few title values
    (e.g. \"'Selling ... Beginner''s Guide ...'\") without touching titles
    whose quotes are real (leading quote but no closing quote)."""
    t = (t or "").strip()
    if len(t) >= 2 and t.startswith("'") and t.endswith("'"):
        t = t[1:-1].replace("''", "'")
    return t

def _strip_shorts(t):
    return re.sub(r"\s*#Shorts\s*$", "", _clean_title(t)).strip()

def _cfm_zh_theme(title):
    t = _strip_shorts(title)
    if "｜" in t:
        tail = t.split("｜", 1)[1]
        if " | " in tail:
            tail = tail.split(" | ")[0]
        if " · " in tail:
            tail = tail.split(" · ")[0]
        return tail.strip()
    if " | " in t:
        parts = [p.strip() for p in t.split("|")]
        if len(parts) >= 2:
            return parts[1]
    return t

ZH_BOOK = r"(?:詩篇|诗篇|以賽亞書|以赛亚书|約翰福音|约翰福音|希伯來書|希伯来书|歌羅西書|歌罗西书|提摩太[後后][書书]|雅各書|雅各书|箴言|腓立比書|腓立比书|羅馬書|罗马书|創世記|创世记|出埃及記|出埃及记|馬太福音|马太福音|馬可福音|马可福音|路加福音|使徒行傳|使徒行传|哥林多[前後后][書书]|加拉太書|加拉太书|以弗所書|以弗所书|帖撒羅尼迦[前後后][書书]|彼得[前後后][書书]|約翰一書|约翰一书|啟示錄|启示录|傳道書|传道书|雅歌|耶利米書|耶利米书|以西結書|以西结书|但以理書|但以理书|約伯記|约伯记|路得記|路得记|撒母耳記[上下]|列王紀[上下]|列王纪[上下]|歷代志[上下]|历代志[上下]|以斯拉記|以斯拉记|尼希米記|尼希米记|以斯帖記|以斯帖记|何西阿書|何西阿书|約珥書|约珥书|阿摩司書|阿摩司书|俄巴底亞書|俄巴底亚书|約拿書|约拿书|彌迦書|弥迦书|那鴻書|那鸿书|哈巴谷書|哈巴谷书|西番雅書|西番雅书|哈該書|哈该书|撒迦利亞書|撒迦利亚书|瑪拉基書|玛拉基书)"

def _dv_zh_ref(title, topic):
    m = re.search(ZH_BOOK + r"\s*\d+:\d+(?:[-–]\d+)?", title or "")
    return m.group(0) if m else topic

def _ep_date(r):
    m = re.search(r"\d{4}-\d{2}-\d{2}", r.get("title") or "")
    return m.group(0) if m else (r.get("published") or "")

def human_label(r):
    series = r.get("series") or ""
    lang = lang_group(r.get("language"))
    title = _clean_title(r.get("title") or "")
    topic = r.get("topic") or ""
    if series == "Come, Follow Me 2026":
        m = re.match(r"Lesson\s+(\d+)\s*[—-]\s*(.+)", topic)
        if m:
            n, theme = m.group(1), m.group(2).strip()
            if lang == "zh":
                return f"第 {n} 週 · {_cfm_zh_theme(title)}"
            return f"Week {n} · {theme}"
        return _strip_shorts(title)
    if series == "Daily Verse · Neville Readings":
        d = _ep_date(r)
        if lang == "zh":
            return f"{d} · {_dv_zh_ref(title, topic)}"
        return f"{d} · {topic}"
    if series == "General Conference Talks (Elders Quorum)":
        if lang == "zh":
            t = _strip_shorts(title)
            if "｜" in t:
                t = t.split("｜")[0]
            return t.strip()
        return topic
    if series == "Neville Inner Reading Podcast":
        return _strip_shorts(title)
    if series == "Finance Basics":
        t = _strip_shorts(title)
        if lang == "zh":
            return t.split("｜")[0].strip()
        return t.split(" — ")[0].strip()
    return _strip_shorts(title)

TYPE_DISP = {
    "zh": {"Long": "長集", "Short (hook)": "Short · 鉤子", "Short (funnel)": "Short · 導入", "Short (sister cut)": "Short · 姐妹版", "Short": "Short"},
    "en": {"Long": "Long", "Short (hook)": "Short (hook)", "Short (funnel)": "Short (funnel)", "Short (sister cut)": "Short (sister cut)", "Short": "Short"},
}

def type_label(r):
    return TYPE_DISP[lang_group(r.get("language"))].get(r.get("type") or "", r.get("type") or "")

GUID_RE = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")

def archive_disp(r):
    """-> (main, sub) human archive label; never a full GUID."""
    lang = lang_group(r.get("language"))
    v = (r.get("archive_note") or "").strip()
    if not v:
        return ("待存档", "") if lang == "zh" else ("Not archived yet", "")
    m = GUID_RE.search(v)
    short = m.group(0)[:8] if m else None
    if short is None:
        m2 = re.search(r"\b[0-9a-f]{8}\b", v)
        short = m2.group(0) if m2 else None
    nb = None
    if "Gospel" in v:
        nb = "Gospel"
    elif "Video Artifacts" in v:
        nb = "Video Artifacts"
    main = "已存档" if lang == "zh" else "Archived"
    sub = " · ".join(x for x in [nb, short] if x)
    return (main, sub)

def status_label(r):
    lang = lang_group(r.get("language"))
    s = (r.get("status") or "").strip()
    zh = lang == "zh"
    if s.startswith("Live") or s == "Public":
        out = "已發布" if zh else "Live"
        m = re.search(r"spot-check due ~?(\d{4})-(\d{2})-(\d{2})", s)
        if m:
            out += f" · {'抽查' if zh else 'check'} {m.group(2)}-{m.group(3)}"
        return out
    if s.startswith("Private"):
        if "duplicate" in s:
            return "Private · 重複上傳" if zh else "Private · duplicate"
        if "original version" in s:
            return "Private · 舊版" if zh else "Private · original"
        if "replaced by redo" in s:
            return "Private · 已被重製版取代" if zh else "Private · replaced by redo"
        if "replaced" in s:
            return "Private · 已被取代" if zh else "Private · replaced"
        return "Private"
    return s.split("—")[0].strip()[:30]

def disp(r):
    am, asub = archive_disp(r)
    return {
        "label": human_label(r),
        "sub": _strip_shorts(r.get("title") or ""),
        "type_label": type_label(r),
        "archive_main": am,
        "archive_sub": asub,
        "status_label": status_label(r),
    }

# ---------------- load ----------------

def load():
    with open("publications.yaml", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("publications", []), data.get("replaced_or_private", []), data.get("unverified", [])

TYPE_RANK = {"Long": 0, "Short (hook)": 1, "Short (funnel)": 2}

def sort_rows(rows):
    return sorted(rows, key=lambda r: (r.get("published") or "", TYPE_RANK.get(r.get("type") or "", 3), r.get("title") or ""), reverse=False) \
        if False else sorted(rows, key=lambda r: (r.get("published") or ""), reverse=True)

def group_blocks(rows):
    """[(series, lang_group, [rows])] in stable series order, zh before en."""
    series_order = []
    for r in rows:
        if r["series"] not in series_order:
            series_order.append(r["series"])
    blocks = []
    for s in series_order:
        for lg in ("zh", "en"):
            sub = [r for r in rows if r["series"] == s and lang_group(r.get("language")) == lg]
            if sub:
                blocks.append((s, lg, sort_rows(sub)))
    return blocks

def block_title(series, lg, n, private=False):
    name = SERIES_DISP.get(series, {}).get(lg, series)
    if private:
        return f"已取代 / Private · {name} — {'中文' if lg == 'zh' else 'English'}{'（' if lg == 'zh' else ' ('}{n}{'）' if lg == 'zh' else ')'}"
    return f"{name} — {'中文' if lg == 'zh' else 'English'}{'（' if lg == 'zh' else ' ('}{n}{'）' if lg == 'zh' else ')'}"

# ---------------- main ----------------

def main():
    PUBS, PRIV, UNV = load()
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
        out = ["| 發布 | 標題 | 類型 | 播放清單 | 存檔 | 狀態 | ID |",
               "|---|---|---|---|---|---|---|"]
        for r in rows:
            d = disp(r)
            title_cell = f"[{d['label']}]({r['url']})" if r.get("url") else d["label"]
            if d["sub"] and d["sub"] != d["label"]:
                title_cell += f"<br><sub>{d['sub']}</sub>"
            arch = d["archive_main"] + (f" · {d['archive_sub']}" if d["archive_sub"] else "")
            out.append("| {published} | {title} | {typ} | {playlist} | {arch} | {status} | `{nid}` |".format(
                published=r["published"], title=title_cell, typ=d["type_label"],
                playlist=r["playlist"] or "—", arch=arch, status=d["status_label"], nid=r["native_id"]))
        return "\n".join(out)

    md = []
    md.append("# Publications — full tables (no-JS fallback)\n")
    md.append("Generated from `publications.yaml` by `generate.py` — do not hand-edit. "
              f"Live, filterable version: {BASE}\n")
    md.append(f"**{len(PUBS)} public videos** · {len(PRIV)} replaced/private versions · "
              + " · ".join(f"{s}: {series_counts[s]}" for s in series_list) + "\n")
    for s, lg, rows in group_blocks(PUBS):
        md.append(f"\n## {block_title(s, lg, len(rows))}\n")
        md.append(md_table(rows))
    if PRIV:
        md.append(f"\n## Replaced / Private versions ({len(PRIV)})\n")
        md.append("Same productions, kept for the record — not public.\n")
        for s, lg, rows in group_blocks(PRIV):
            md.append(f"\n### {block_title(s, lg, len(rows), private=True)}\n")
            md.append(md_table(rows))
    if UNV:
        md.append("\n## Unverified / pending\n")
        for u in UNV:
            md.append(f"- **{u['item']}** — {u['reason']} Next: {u['action']}")
    md.append("")
    open("PUBLICATIONS.md", "w", encoding="utf-8").write("\n".join(md))

    # ---------------- index.html ----------------
    def embed(rows):
        slim = []
        for r in rows:
            slim.append({
                "platform": r["platform"], "series": r["series"], "language": r["language"],
                "type": r["type"], "published": r["published"], "url": r.get("url"),
                "native_id": r["native_id"], "playlist": r.get("playlist") or "",
                "disp": disp(r),
            })
        return json.dumps(slim, ensure_ascii=False).replace("</", "<\\/")

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
  h2 { font-size:16.5px; margin:24px 0 6px; border-left:4px solid var(--gold); padding-left:8px; }
  table { width:100%; border-collapse:collapse; font-size:13.5px; table-layout:fixed; }
  th, td { text-align:left; padding:7px 8px; border-bottom:1px solid var(--line); vertical-align:top; overflow-wrap:break-word; }
  th { color:var(--mut); font-weight:600; font-size:12px; }
  td a { color:#1757a8; text-decoration:none; }
  td a:hover { text-decoration:underline; }
  .lbl { font-size:14.5px; font-weight:600; line-height:1.35; }
  .sub { color:var(--mut); font-size:12px; margin-top:2px; line-height:1.4; }
  .vid { color:#9aa3b2; font-size:11px; font-family:ui-monospace, Menlo, monospace; margin-top:2px; }
  .meta { color:var(--mut); font-size:12px; }
  .arch-sub { color:var(--mut); font-size:11.5px; }
  .pend { color:#b07d2b; }
  .status { font-size:12.5px; }
  .priv { background:var(--bg); }
  .unv { background:#fdf6e3; border:1px solid #eadfc0; border-radius:10px; padding:10px 14px; margin-top:10px; font-size:13.5px; }
  col.c-title { width:auto; } col.c-date { width:96px; } col.c-type { width:104px; }
  col.c-pl { width:168px; } col.c-arch { width:150px; } col.c-status { width:170px; }
  @media (max-width:760px) {
    table, thead, tbody, th, td, tr { display:block; }
    thead { display:none; }
    tr { border:1px solid var(--line); border-radius:10px; margin:10px 0; padding:6px 4px; }
    td { border:none; padding:3px 8px; }
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
const SERIES_DISP = __SERIES_DISP__;
const $ = id => document.getElementById(id);
function escapeHtml(s){return String(s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));}
function langGroup(l){ return (l||"").startsWith("zh") ? "zh" : "en"; }
function blockTitle(series, lg, n, priv) {
  const name = (SERIES_DISP[series]||{})[lg] || series;
  const lang = lg === "zh" ? "中文" : "English";
  const cnt = lg === "zh" ? "（"+n+"）" : " ("+n+")";
  return priv ? ("已取代 / Private · "+name+" — "+lang+cnt) : (name+" — "+lang+cnt);
}
function row(r, priv) {
  const d = r.disp;
  const labelHtml = r.url ? '<a href="'+r.url+'" target="_blank" rel="noopener">'+escapeHtml(d.label)+'</a>' : escapeHtml(d.label);
  const subHtml = (d.sub && d.sub !== d.label) ? '<div class="sub">'+escapeHtml(d.sub)+'</div>' : '';
  const pendCls = (/待存档|Not archived/.test(d.archive_main)) ? ' class="pend"' : '';
  return '<tr'+(priv?' class="priv"':'')+'>'
    + '<td><div class="lbl">'+labelHtml+'</div>'+subHtml+'<div class="vid">ID '+escapeHtml(r.native_id)+'</div></td>'
    + '<td>'+r.published+'</td>'
    + '<td>'+escapeHtml(d.type_label)+'</td>'
    + '<td class="meta">'+escapeHtml(r.playlist||'—')+'</td>'
    + '<td><span'+pendCls+'>'+escapeHtml(d.archive_main)+'</span>'+(d.archive_sub?'<div class="arch-sub">'+escapeHtml(d.archive_sub)+'</div>':'')+'</td>'
    + '<td class="status">'+escapeHtml(d.status_label)+'</td></tr>';
}
function tableHtml(rows, priv) {
  return '<table><colgroup><col class="c-title"><col class="c-date"><col class="c-type"><col class="c-pl"><col class="c-arch"><col class="c-status"></colgroup>'
    + '<thead><tr><th>標題 Title</th><th>發布 Published</th><th>類型 Type</th><th>播放清單 Playlist</th><th>存檔 Archive</th><th>狀態 Status</th></tr></thead><tbody>'
    + rows.map(r=>row(r,priv)).join('') + '</tbody></table>';
}
function groupsOf(rows) {
  const order = []; const map = {};
  rows.forEach(r=>{ const k = r.series; if(!(k in map)){ map[k]={zh:[],en:[]}; order.push(k);} map[k][langGroup(r.language)].push(r); });
  return order.map(s=>({series:s, zh:map[s].zh, en:map[s].en}));
}
function render() {
  const q = $('q').value.trim().toLowerCase(), fp=$('fPlatform').value, fs=$('fSeries').value, fl=$('fLang').value, ft=$('fType').value;
  const match = r => (!fp||r.platform===fp)&&(!fs||r.series===fs)&&(!fl||r.language===fl)&&(!ft||r.type===ft)
    &&(!q||(r.disp.label+' '+r.disp.sub+' '+r.native_id+' '+r.series).toLowerCase().includes(q));
  let h = '';
  groupsOf(PUBS.filter(match)).forEach(g=>{
    ["zh","en"].forEach(lg=>{ const rows = g[lg]; if(rows.length){ h += '<h2>'+escapeHtml(blockTitle(g.series, lg, rows.length, false))+'</h2>' + tableHtml(rows, false); } });
  });
  const priv = PRIV.filter(match);
  if (priv.length) {
    h += '<h2>Replaced / Private versions ('+priv.length+')</h2>';
    groupsOf(priv).forEach(g=>{
      ["zh","en"].forEach(lg=>{ const rows = g[lg]; if(rows.length){ h += '<h2>'+escapeHtml(blockTitle(g.series, lg, rows.length, true))+'</h2>' + tableHtml(rows, true); } });
    });
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

    LANG_LABEL = {"zh": "中文", "en": "English", "": "—"}
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
        .replace("__LANG_OPTS__", "".join(f"<option value='{l}'>{LANG_LABEL.get(l, l)}</option>" for l in langs))
        .replace("__TYPE_OPTS__", "".join(f"<option>{html.escape(t)}</option>" for t in types))
        .replace("__UNV_HTML__", unv_html)
        .replace("__SERIES_DISP__", json.dumps(SERIES_DISP, ensure_ascii=False))
        .replace("__PUBS_JSON__", embed(PUBS))
        .replace("__PRIV_JSON__", embed(PRIV)))
    open("index.html", "w", encoding="utf-8").write(html_doc)
    print(f"generated index.html + PUBLICATIONS.md — {len(PUBS)} public, {len(PRIV)} private, {len(UNV)} unverified")

if __name__ == "__main__":
    main()

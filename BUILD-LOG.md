# Portal MVP — BUILD LOG

- Branch: `portal-mvp` (off origin/main `246cdbc6300f937214aebd7804ef8b022318936e`)
- Scope: joint recommendation §8 step 1 (Protect) + step 2 (Portal MVP) ONLY.
- **The root switch (§8 step 3) is NOT done and is separately gated.** Nothing on
  this branch is live: GitHub Pages serves `main`, and the root `index.html`
  on this branch is byte-identical to origin/main.
- Built: 2026-11-08 (America/Los_Angeles).

---

## 1. Protection — current index snapshot & verification

Source of truth: `publications.yaml` → `generate.py` → `index.html` + `PUBLICATIONS.md`.
All counts below were recomputed from the files on this branch, not copied from prose.

| Item | Value | How verified |
|---|---|---|
| `publications.yaml` entries | **324** | PyYAML load; 324 unique `native_id`s |
| Entry statuses | 139 `Public`, 115 `Live`, 70 `Live — …` variants (all public-facing; 0 private/unlisted in the YAML) | status counter over all 324 |
| Series totals | Come, Follow Me 2026: 138 · Daily Verse · Neville Readings: 144 · General Conference Talks (Elders Quorum): 28 · Neville Inner Reading Podcast: 7 · Finance Basics: 6 · Music Videos: 1 → **324** | series counter; matches the header line of `PUBLICATIONS.md` exactly |
| Playlists (11 distinct names) | 每日經文 · Neville 解讀 2026（中文）75 · 來跟隨我 2026（中文）69 · Come, Follow Me 2026 (English) 69 · Daily Verse · Neville Readings 2026 (English) 69 · 總會大會演講 2026（中文）14 · General Conference Talks 2026 (English) 14 · Neville 內在解讀播客 2026（中文）4 · Neville Inner Reading Podcast 2026 (English) 3 · 財經基礎 · 錢的知識 2026（中文）3 · Finance Basics 2026 (English) 3 · 音樂錄影帶 MV 1 | playlist counter over all 324 |
| Generated `index.html` data | **398** unique `native_id`s embedded (`const PUBS`) = 324 public + **74 replaced/private** versions | regex extraction; ID sets of `index.html` and `PUBLICATIONS.md` are identical |
| YAML → index completeness | all 324 YAML ids present in the generated index; **0 missing** | set difference |
| `index.html` | 439,150 bytes · MD5 `508aed79e3706d7753e5c81b54878ad3` | md5sum at snapshot time |
| `publications.yaml` | MD5 `0c79b6f6981b400734fe9b107b8ecaa5` | md5sum |
| `PUBLICATIONS.md` | MD5 `aa760f8f08377967f4f54e5c8c94d3db` | md5sum |

No dead or non-public entries were found among the 324 (per the YAML's own status
fields); nothing was fudged or dropped.

### /publications/ copy (`publications/index.html`)

A byte-copy of the current generated `index.html` (439,333 bytes, MD5
`8b54d0b6eca2bfedd866c5ee4416774c`) with exactly two surgical changes, proven by a
round-trip test (removing the changes reproduces the source byte-for-byte):

1. A back-link bar injected immediately after `<body>`:
   「← 返回米老爸首页」 → `../`
2. The three relative content links (`gospel-wisdom/theme-zh/`, `theme-en/`,
   `mixi/`) prefixed with `../` so they still resolve to the same targets when
   the page is served one directory deeper.

Note for the switch step: `generate.py` still owns the root `index.html`; this
copy was made by hand for the migration. At the switch, teach `generate.py`
(or a post-step) to emit the /publications/ copy so the two never drift.

One structural fact for the migration: the current index renders its series
blocks with JavaScript and defines **no stable playlist fragment ids** (the
only element ids are UI controls). The portal's legacy-anchor script (§3) is
therefore a catch-all: any unrecognized `#fragment` is forwarded to
`/publications/#fragment`.

## 2. What was built

| File | What |
|---|---|
| `publications/index.html` | The /publications/ copy (above) |
| `portal-src/content.json` | **Single content source** — every trilingual string for the portal |
| `portal-src/build.py` | Renders the three portal pages from the template + content.json (`python3 portal-src/build.py`) |
| `portal/index.html` | Portal, zh-Hans (the future root page) — 9,874 bytes |
| `portal/zh-hant/index.html` | Portal, zh-Hant — 9,915 bytes |
| `portal/en/index.html` | Portal, English — 10,004 bytes |
| `sitemap.xml` | Draft sitemap for the post-switch URL layout (portal trio with hreflang + /publications/ + existing key pages) |
| `robots.txt` | Draft (points at the sitemap) |
| `404.html` | Draft custom 404, trilingual, root-absolute links |

Portal structure (per joint recommendation §§1–3, 5): top bar (brand, always-visible
简/繁/EN text switcher, nav) → hero (brand line + listen block: native
`<audio controls preload="none">` playing ④《換我們為妳點燈》 from the existing
`gospel-wisdom/dian-deng/song.mp3` — referenced, not duplicated — with the small
Mi Xi cover `gospel-wisdom/dian-deng/mixi-cover-diandeng.jpg`, the AI disclosure
line beside the player, the song-page link, and the "next song first" prompt
anchoring to the form) → 「探索作品」 as a text link only → email block (the page's
only conversion block) → three featured cards (Gospel Wisdom / 米曦 Mi Xi /
视频库·影片庫·Video Library → /publications/) → About 米老爸 (honest AI-use
statement; no legal name, no family information) → footer (support@daddymi777.com,
privacy line, YouTube channel + MV playlist links labelled 需境外网络， © 2026
米老爸 Daddy Mi).

Design/constraints honoured: abstract morning-light CSS ground (no stock photos;
Mi Xi's face appears only as the small song cover in the listen block); system
font stack only; zero external resources; no autoplay; no prices, membership
buttons, testimonials, popups, or embedded YouTube players; separate language
URLs with full hreflang and per-page canonicals; subpage links carry `?lang=`
(zh-hans / zh-hant / en) so the visitor's language choice carries over; the hero
brand line is the **working line** 「以智慧启发人生，以科技传递温暖。/ Wisdom for
Life. Technology with Heart.」 (GPT finalizes wording per the recommendation).
Each page is ~10 KB — inside the ≤30 KB first-screen HTML+CSS target.

## 3. Local verification (2026-11-08)

Method: the repo worktree served by the durable Range-capable harness pattern
(`sangu-tribute-2026-11-08/qc/harness/range_server.py`, port 8941) and driven in
headless Chromium (Playwright). Full JSON report:
`~/workspace/portal-build-2026-11-08/qc/results/verify-portal.json`
(script: `~/workspace/portal-build-2026-11-08/qc/verify_portal.py`).

| Check | Result |
|---|---|
| Portal pages load | 3/3 → HTTP 200 (zh-Hans / zh-Hant / en, correct `lang` attributes) |
| Network requests per page | 2 (the page + the cover image). The audio file is **not** fetched — `preload="none"` works |
| External (non-origin) requests | **0 on all three pages** |
| Audio element | present, `controls`, `preload="none"` on all three pages |
| Audio Range request | HTTP **206**, `Content-Range: bytes 0-1023/4260669` (the MP3 is 4,260,669 bytes) |
| Email form | **0 `<form>` elements** on every portal page (inert by design, see §4) |
| Language cross-links | all 6 switcher targets resolve 200; switching preserves context |
| Same-origin link crawl (new files) | 19 unique targets, **all 200, zero dead** |
| Legacy-anchor redirect | `/portal/#legacy-playlist-x` → lands on `/publications/#legacy-playlist-x`; the portal's own `#works` does **not** redirect |
| Mobile geometry (390×844) | hero bottom 250 px; email block top **826 px** (inside the first viewport, before Works at 1,090 px); DOM order hero → listen → subscribe → works confirmed |
| /publications/ copy in-browser | loads 200; `PUBS.length` = **324** public entries renderable; back link 「← 返回米老爸首页」 present; title kept as "Daddy Mi — Publications Index" |

## 4. What remains gated (honest list)

1. **Email form is INERT — deliberately.** The subscribe block carries the copy
   and an HTML-comment placeholder marking exactly where the provider's
   pure-HTML `<form action>` goes, plus a working interim contact line
   (mailto: support@daddymi777.com). There is **no form element** — nothing
   pretends to subscribe anyone. Unblocks when: the mainland form test
   (recommendation §6; order Buttondown → Kit → MailerLite) picks a provider.
2. **Analytics not installed.** Same gate as the form: the beacon
   (Cloudflare Web Analytics / GoatCounter) must first be verified loadable
   from the mainland (§6). No third-party script was added.
3. **Mainland measurement (§6 gate) not yet run.** Pages/R2 dual-source
   multi-node test is still owed before the switch; the interim default
   (host on Pages) is what this build assumes. R2 card-binding requirement
   remains UNVERIFIED.
4. **Root switch not done.** The portal currently sits under `portal/` on this
   branch; the live root still serves the index. Switch steps still owed
   (§8.3): move portal pages to `/`, `/zh-hant/`, `/en/`; retire the root index
   to /publications/ only; make `generate.py` emit the publications copy;
   update YouTube description links that point at the root; resubmit sitemap;
   verify share cards by posting to 微信/Line/X.
5. **The 视频库 card link (`../publications/`)** resolves on this branch and
   locally, but on the **live** site /publications/ does not exist until the
   switch — expected, recorded here so nobody "fixes" it pre-switch.
6. **Brand line is the working line.** GPT's final wording may still replace
   「以智慧启发人生，以科技传递温暖。/ Wisdom for Life. Technology with Heart.」
   — a one-line change in `portal-src/content.json` + re-run build.py.

---

## 5. Root switch — DONE 2026-11-09 (boss directive 02:42 PST)

Boss: "Previously I asked for a landing page. Currently, it is pointing to
our publication list. We should [have] a simple stylist landing page."
Executed the same day; the gated §8 step 3 is complete.

What changed (on top of merged origin/main `0235a3a`):

| Piece | Change |
|---|---|
| `index.html` (root) | NOW the portal (zh-Hans), generated by `portal-src/build.py` from `portal-src/content.json` |
| `zh-hant/index.html`, `en/index.html` | The other two portal views, same source |
| `portal/` directory | REMOVED — the preview layout is retired; the portal lives at the root |
| Hero | Golden-ring 米 brand mark (`brand/mark-transparent.png`, asset DMI-BG-0651) above the brand line; favicon suite in `<head>`; small mark in the footer |
| Email form | Full Buttondown embed markup wired (pure-HTML POST, no JS): `<form action="https://buttondown.com/api/emails/embed-subscribe/REPLACE_WITH_BUTTONDOWN_USERNAME" method="post">` with an email input + submit button. **The username is a marked placeholder** — activation is exactly one step: create the Buttondown account, put its username into `portal-src/content.json` (`site.buttondown_username`), re-run `portal-src/build.py`. The page copy itself says subscribing opens soon and offers the support mailbox meanwhile — nothing pretends to work. Mainland three-test still owed before the placeholder is swapped (joint rec. §6) |
| Legacy-anchor rescue | Now relative (`publications/#…` from the root page, `../publications/#…` from language pages) so it also resolves on the github.io mirror |
| `publications/index.html` | The complete index, regenerated as a byte-transform of origin/main's live index (back-link bar + `../` on brand/ and gospel-wisdom/ references). Round-trip proven: stripping the transform reproduces origin/main `index.html` exactly. Embedded data unchanged: 398 unique native_ids; 324 public entries |
| `generate.py` | Now owns /publications/: emits `publications/index.html` (with the brand favicon links + footer brand mark in its template — they were hand-edits from the logo rollout) and no longer writes the root. Verified locally: its output matches the hand-made branch copy except the intended brand additions and the date stamp |
| `sitemap.xml`, `robots.txt`, `404.html` | The branch drafts, now live |

Verification (live, post-push): /, /zh-hant/, /en/ → 200 portal;
`/publications/` → 200 with the same 398 embedded ids / 324 public
entries as the pre-switch root; /gospel-wisdom/ and song pages
unaffected; brand assets 200; mobile 390×844 geometry checked
(no autoplay — audio stays `preload="none"`; AI disclosure beside
the player on all three views).

Still owed (not part of the switch): Buttondown account + mainland
three-test → one-word form activation; YouTube description links that
point at the root now land on the portal (legacy-anchor script forwards
old #fragments to /publications/); analytics beacon mainland check.

**Addendum — same day (2026-11-09): the email form is wired to the REAL
Buttondown account.** Username `daddymi`, newsletter "Daddy Mi"; the form
action on all three portal views is
`https://buttondown.com/api/emails/embed-subscribe/daddymi`
(POST, field `email`), styled to the page design with the page's own
per-language labels. The interim "subscribing opens soon" note was
replaced by a plain "or write to us directly" line to the support
mailbox. One caveat, recorded not hidden: the Buttondown account's email
verification (amani.dd.chen@gmail.com) was still being completed when
this shipped — until it lands, Buttondown's public newsletter page 404s
and subscriber confirmations may not flow. The mainland three-test
(§6) also remains owed. The wiring itself is final; nothing about the
form needs to change when verification lands.

---

**Addendum — 2026-11-09: stylesheet C 「水墨之光」 (Ink & Light) + Track A
calligraphy artwork deployed (boss ruling 2026-11-09 04:40 PST: Track A).**
`portal-src/portal.css` is candidate C's final sheet (rice paper `#F8F4EA`,
indigo ink `#1E2A38`, gold as light `#C9A227`/`#E9D48A`) plus a clearly-marked
production-integration block at the end (sr-only, fallback, strip rules);
single `portal.css` visual layer retained. Hero structure is unchanged
except the brand line: on the zh-Hans and zh-Hant views it is now the
QC-passed AI-generated calligraphy artwork —
`brand/calligraphy/brand-line1.png` + `brand-line2.png` (indigo `#1E2A38`).
Semantics/fallback per team review: the images carry `alt=""`, the real
sentence sits in an sr-only span in each view's own script
（以智慧启发人生，以科技传递温暖。 / 以智慧啟發人生，以科技傳遞溫暖。), and a hidden
serif layer (Noto Serif 600, indigo) replaces the images if one fails to
load (`onerror` → `.callig-failed`). The song card carries the vertical
inscription strip `brand/calligraphy/inscr-0..3.png` (`role="img"`, per-view
aria-label 点灯的人 / 點燈的人， glyph images `alt=""`; opacity .34, right
edge; CSS hides it on small screens). Images are served from 2736×714 /
2714×667 masters at ≤430 CSS px (≈6.4× — retina-safe); alpha edges checked
against `#F8F4EA` at 200%: zero bright semi-transparent fringe pixels
(16,704 semi-transparent px, all dark ink texture, mean luminance 42.7).
The stylesheet has no dark-mode rules — the design is light-locked, so the
indigo ink cannot land on a dark background. The English view keeps its
brand line as elegant serif text (`h1.brand-en`, EB Garamond italic) under
the same C palette — no Chinese calligraphy there. `build.py` renders both
blocks from two placeholders (`%%BRANDLINE_BLOCK%%`, `%%INSCR_STRIP%%`);
content and function are untouched: Buttondown form
(`embed-subscribe/daddymi`) on all three views, audio player, cards, About
faith line, footer support@ + © 2026 米老爸 Daddy Mi. Calligraphy provenance
+ per-glyph QC: `~/workspace/portal-stylesheet-2026-11-09/candidate-c-fix2/README.md`
(candidate a; QC count 18 字次 / 16 个不同字， all verified; 啟's left
component is a gyōsho-simplified form, disclosed to and accepted by the boss).

## 2026-11-09 — Portal UX pass (boss order 12:14 PST)

- Subscribe form rebuilt: label on its own line + ONE joined pill shell (subfield, 56px fixed, never stacks) — fixes the iOS giant-oval bug (missing appearance reset + old mobile column rule turned the input flex-basis into its height); global guard: form controls capped at 56px by construction.
- Type rhythm: hero title clamp(34px,6vw,52px); section spacing 72px desktop / 56px mobile; band title 32px.
- Hero glow softened (.5→.38 peak, 560px cap); listen card mobile stack with centered 168px cover; media corners 10px; work cards left-aligned on mobile with press feedback; nav + language switch 44px tap targets; footer spacing loosened.
- Reveal-on-scroll: inline IntersectionObserver script; the hiding class is added by JS only — no-JS and prefers-reduced-motion visitors see everything.
- Palette, fonts, Track A calligraphy, brand mark, copy, link targets and the Buttondown form (action + field names) unchanged.
- Verified by Amani (parent): build outputs keep the form action/name/subfield in all three views; headless render at 390px measures input 54px / shell 56px / button 46px — the giant oval is gone.

## 2026-11-11 — Album picture gallery 上线 (boss 17:23/17:25 PST 定）

- 新增公开画册页 /album/gallery/（五语：SC 根、/tc/、/en/、/ja/、/ko/）：米曦首张专辑《光，慢慢成为路》的视觉画册——《A Little More Like Light》全部 18 帧分镜图（S2-A 用定版 v2-a），JPG 1600px q85、共 3.8MB；boss 联络表上的 8 帧带 ★ 推荐标记 (S1-A/S2-A/S3-A/S4-A/S5-A/S6-A/S7-B/S8-A)。
- 设计 = natural page（boss 原话 "the natural page")：纯黑底、图片满幅 edge-to-edge、无卡片/边框/装饰，图注极简（帧号 + 一句短诗）。页眉明示「首张专辑」归属与本歌视觉世界。
- 分享卡：五语各自 og:title/description + twitter card，og:image 统一用专辑微笑分享卡 assets/share-album.jpg。
- 入口与回链：五语主页 nav + 五语 /music/ 索引卡片 + gospel-wisdom/theme-en 五语视图按钮 → 画册；画册页脚回 /music/ 与主页；右上角语言切换齐全。

## 2026-11-11 — 全站歌曲互链修复 (boss 17:38–17:42 PST 亲测发现)

- 缺陷: 歌曲页之间缺第 5 首《灯下擂茶》的链接 — 歌曲 1–4 页、认识米曦页的专辑之旅只有 4 首; /order/ 样品卡里第 5 首链向试听页 v5 且播 v5 音频 (非定版); 画册页脚只有总索引链接、没有逐首链接。
- 专辑曲序统一为 /music/ 总索引的定版顺序: 01《換我們為妳點燈》02《愿你心里有光》03 A Little More Like Light 04《在你话语里，天亮了》05《灯下擂茶》(此前 gw 页内部编号以主题歌为 01/02, 与总索引不一致, 本次一并校正; 卡片图随歌走, 新增 album-thumbs/song5.jpg = 米曦白衣正面 S7-B 480x480)。
- 歌曲页 1–4 + 认识米曦页 (各 5 语视图): 专辑之旅补齐 5 首 (当前页标注、其余互链)、下一首按新曲序、进度改「第 1–5 首, 共 12 首」、工具行补「全部歌曲 / 专辑画册 / 回首页」按钮 (语种对应链接); 米曦页曲目引言「四首歌」改「五首歌」(五语同步)。
- mx005 正式版页 (五语): 页脚前新增专辑曲目块 — 5 首按序 (05 标此页)、全部歌曲 / 专辑画册 / 首页链接; 只链正式版页, 无 Take 字样。
- 画册页 (五语): 页脚导航补 5 首逐首链接 (语种标题 + 对应链接)。
- /order/ (五语): 《灯下擂茶》样品卡改链正式版页 (本语种)、音频改播定版 Take 4 (/music/mx005/v4/song.mp3)。
- 主页 #works 为分类卡 (灵修/米曦/视频库/定制)、不逐首列歌, 无需改; 顶栏已有画册与试听存档入口。

## 2026-11-11 — 专辑曲序更正 + 第 5 首正式版页改版 (boss 17:51–17:57 PST 亲裁)

- 更正: 上一条 (commit 3320dc1) 把全站曲序统一到 /music/ 总索引的自排顺序 — 那是错的。boss 亲裁恢复原始定版曲序: 01《在你话语里，天亮了》(theme-zh)、02 A Little More Like Light (theme-en)、03《换我们为你点灯》(dian-deng)、04《愿你心里有光》(birthday-light)、05《灯下擂茶》(mx005)。注: gw 四页正文的「系列第 N 首」本来就是这个顺序, 只有专辑之旅块与总索引被上一工改反。
- 全站按定版序校正: /music/ 总索引 (五语, 卡片重排 + trackno 重号)、歌曲 1–4 页与认识米曦页的专辑之旅 (五语视图: 卡片重排重号、「下一首」按新序)、画册页脚逐首链接 (五语)、/order/ 样品卡顺序 (五语: 点灯在擂茶之前)。
- 第 5 首正式版页 (五语) 改版为 Gospel Wisdom 家族风格 (暖纸底色、衬线、卡片分节, 与 1–4 首同款): 播放器换成与 1–4 首同款的整幅原生播放器 (去掉原来的大圆按钮); 页底专辑导航改为与 1–4 首同款的图文卡片 (定版曲序, 05 标此页); 故事、康乃馨擂茶图、歌词 (54 句同步高亮)、制作手记、署名、语言切换全部保留, 仍无 Take 字样, og 分享卡未动。
- theme-en 页自身的独特风格按 boss 裁示保留不动 (只改其编号与顺序文字)。

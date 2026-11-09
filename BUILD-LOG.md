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

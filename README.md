# Daddy Mi — Publications Index

One authoritative, owner-friendly index of everything our production has published — so the channel owner can track all published work, on every platform, from a single page.

## 🌐 Live index (start here)

**https://king818.github.io/daddymi-publications/**

Filterable by platform / series / language / type, with a search box; newest first; mobile-friendly.

## Contents

| File | What it is |
|---|---|
| `publications.yaml` | **Single source of truth.** One record per publication. Edit this file only. |
| `index.html` | The live page above — generated from `publications.yaml` by `generate.py`. Never hand-edit. |
| `PUBLICATIONS.md` | The same tables in Markdown (no-JS fallback) — also generated. Never hand-edit. |
| `generate.py` | Regenerates `index.html` + `PUBLICATIONS.md` from `publications.yaml`. |

## Scope

- **Included:** every video produced by our podcast pipeline (2026-10-28 onward) and published on the 米老爸 channel — Come, Follow Me 2026, Daily Verse · Neville Readings, General Conference Talks (Elders Quorum), Neville Inner Reading Podcast (EP1), and Finance Basics.
- **Excluded:** legacy channel stock uploaded before this project (including livestreams) — it is not our production and stays hands-off.
- **Backup channel 米公子：** no productions have been published there as of 2026-11-02 (verified against production records).
- Replaced/Private versions of our own videos are kept in a separate section so nothing our pipeline uploaded is ever lost from view.
- The data model already carries a `platform` field, so Xiaohongshu / Instagram / TikTok posts from the soft pilots (and anything else) can be added as rows the same way.

## Fields — and why each extra field exists

| Field | Purpose |
|---|---|
| `platform` | Which platform the item lives on (YouTube today; pilots next). |
| `native_id` | The platform's own ID for the item (YouTube video ID). Titles repeat across languages — the native ID is the unambiguous cross-reference. |
| `archive_note` | Link/identifier of the item's Evernote archive note (the downloadable episode package). From the tracking page, the owner can jump straight to the package. Blank where no archive note is recorded — never invented. |
| `status` | Not just "done": what is pending — e.g. `Live`, `Live — 48h spot-check due 2026-11-03`, `Private — replaced by redo <id>`. |
| `playlist` | The canonical playlist/collection the item belongs to. |

## How this stays current

1. **In the same session as every publish**, append the new row(s) to `publications.yaml` (platform, series, topic, language, type, title, date, URL, native ID, playlist, archive note, status).
2. Run `python3 generate.py` — it rebuilds `index.html` and `PUBLICATIONS.md`.
3. Commit and push all three files together. The live page updates itself from the push.

Never hand-edit the HTML or the Markdown tables; they are regenerated from the data file every time.

## Verification

Initial build (2026-11-02): every Public row was cross-checked from the production runsheets and daily logs, and each video's existence and exact current title were verified live via YouTube oEmbed (93/93 confirmed on the 米老爸 channel). Items that could not be verified are listed under **Unverified / pending** in the data file and on the page — never silently dropped, never guessed.

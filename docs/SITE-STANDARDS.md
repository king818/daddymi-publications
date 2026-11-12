# Daddy Mi Site Standards

The standing engineering rules for daddymi777.com (this repository). Every page, generator and deploy follows them — a page that breaks a rule does not ship.

## Contents

- [1. Paths: root-absolute, always](#1-paths-root-absolute-always)
- [2. Canonical URLs](#2-canonical-urls)
- [3. Cache-busting by filename](#3-cache-busting-by-filename)
- [4. Share cards](#4-share-cards)
- [5. The link audit is the deploy gate](#5-the-link-audit-is-the-deploy-gate)
- [6. Performance budgets](#6-performance-budgets)
- [7. Generators are the source of truth](#7-generators-are-the-source-of-truth)

## 1. Paths: root-absolute, always

Every internal link and asset reference — `href`, `src`, form `action`, poster, CSS `url()`, and asset paths inside page JavaScript — uses a **root-absolute path**:

| ✅ Root-absolute | ❌ Never |
| --- | --- |
| `/music/mx005/v4/` | `../v4/`, `music/mx005/v4/` |
| `/brand/mark-transparent.png` | `../../brand/mark-transparent.png` |
| `/assets/teasers/mx005-teaser.mp3` | `song.mp3` (bare same-directory name) |

Why: relative paths silently break when a page is generated at one depth and served at another — two 404 incidents on 2026-11-11 (album gallery images, preview archive players) traced to exactly this. Root-absolute paths say what they mean from any page.

## 2. Canonical URLs

- Directory URLs end with a **trailing slash** and are the canonical form: `/music/mx005/`, never `/music/mx005`.
- One canonical URL per locale, declared with `<link rel="canonical">`, with `hreflang` alternates across all five locales (zh-Hans, zh-Hant, en, ja, ko) plus `x-default`.
- A page's own assets are referenced root-absolute too (§1) — no same-directory exceptions.

## 3. Cache-busting by filename

- A **changed** static asset (image, audio, stylesheet content that must refresh) ships under a **new filename** — never overwrite a cached asset in place. This is how share-card images are already handled (`share-v2.jpg`, renamed crops for WeChat).
- Unchanged assets keep their names; content that is not cache-sensitive (HTML) is replaced in place as usual.

## 4. Share cards

Every page carries a complete share card:

| Element | Rule |
| --- | --- |
| `og:title` / `og:description` | Written for that page, in the page's own language |
| `og:image` | A page-appropriate image, **1200×630** |
| `twitter:card` | `summary_large_image`, with title/description/image mirroring og |
| One song / page, one image | Each song has its **own** dedicated share image, identical across its five locales |
| Non-song pages | Company imagery (logo / lamp photo), never a singer's album or single photo |

## 5. The link audit is the deploy gate

- The audit script lives at [`tools/link_audit.py`](../tools/link_audit.py) and runs **on every deploy**, after the Pages build is live:

  ```bash
  python3 tools/link_audit.py            # audits https://daddymi777.com
  python3 tools/link_audit.py --base http://127.0.0.1:8000   # local preview
  ```

- It crawls from the home pages (all five locales) through `/music/`, every song page, the preview archives and version pages, `/album/`, `/order/`, the `/gospel-wisdom/` tree, `/publications/` and `/concordance/`, collecting every internal `href`/`src` and verifying each returns **HTTP 200**.
- **All-green is the completion gate**: the script exits non-zero on any failure, and a deploy with a failing audit is not done. Audit reports are filed under `docs/link-audit-YYYY-MM-DD.md`.

## 6. Performance budgets

Budgets already in force stay in force:

| Budget | Limit |
| --- | --- |
| Mobile first screen | ≤ 500 KB total |
| Hero image | ≤ 280 KB |
| Audio teasers / previews | `preload="none"`, MP3 128k, well under 1 MB each |
| Autoplay | Never — audio and video start only on a visitor's tap |

## 7. Generators are the source of truth

- Pages built by a generator (`portal-src/build.py` → the five home pages; `generate.py` → `/publications/`) are fixed **in the generator and its data**, never by hand-editing the output — a hand edit is silently reverted by the next run.
- After fixing a generator, re-run it and commit its output together with the source change.
- One known environment caveat: `generate.py` needs **OpenCC** in its Python environment for the Simplified/Traditional label variants. Without it the generator warns and emits single-script labels — do not commit that degraded output; regenerate in an environment with OpenCC, or align only the intended lines of the artifact by hand and say so in the commit message.

---

*Established 2026-11-11 (boss: "Need to implement in the best practice"). Companion rules: boss's Markdown style standard — clear title, TOC on long docs, tables for structured data.*

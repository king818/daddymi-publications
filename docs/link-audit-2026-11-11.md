# Link Audit — 2026-11-11

Site-wide internal-link audit run after the root-absolute path standardization and the homepage Music Preview deploy (commit `d3878c3`). Method and gate: [`docs/SITE-STANDARDS.md`](SITE-STANDARDS.md) §5, script [`tools/link_audit.py`](../tools/link_audit.py) against the live site.

## Result

| Metric | Count |
| --- | --- |
| Pages crawled | 114 |
| Unique internal URLs checked | 214 |
| HTTP 200 | 214 |
| Failures | **0** |

Crawl coverage: home pages ×5 locales, `/music/` tree (index ×5, mx005 release ×5, preview archive ×5, version pages v1–v9 and their locales), the five song pages and hub in `/gospel-wisdom/`, `/album/gallery/`, `/order/` ×5, `/publications/`, `/concordance/`, `/404.html` — every internal `href`/`src`/CSS `url()`/JS asset reference collected and verified.

## Spot checks beyond the crawl

Deep assets verified individually (all 200): `/music/mx005/v6/s606.mp3`, `/music/mx005/v9/s1101.mp3`, `/music/mx005/v7/prelude-s606.mp3`, `/gospel-wisdom/dian-deng/mtv.mp4`, `/album/gallery/img/s8-b.jpg`, `/music/mx005/v4/song.mp3`, `/gospel-wisdom/album-thumbs/song3.webp`, `/brand/calligraphy/brand-line1.png`, `/assets/share-home.jpg`, and the five homepage teasers under `/assets/teasers/` (200, exact byte sizes as registered).

## Notes

- The sweep converted **878 internal references** to root-absolute form across 84 files; a repo-wide grep confirms no `../` reference remains in any HTML file.
- `/for-mother/` (private token pages) is intentionally not linked from public pages, so it is outside the crawl; its references were converted by the same sweep and its stylesheet was spot-checked at 200.
- Out of scope (other repositories, follow-ups): the `sangu.` and `light.` subdomains.
- Pre-existing unrelated breakage found: **none**.

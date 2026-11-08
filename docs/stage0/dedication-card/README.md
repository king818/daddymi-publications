# Dedication Card — 敬献卡（claim-a-day 回礼）

Generator + sample cards for the Stage-0 dedication card (approval packet §10, approved 2026-11-08).

## What this is

When a reader submits the claim-a-day form, the team produces a personalized
thank-you card (name **exactly as submitted — never "correct" it**), one card
per submission, sent by email as a PNG attachment within 24 h (packet §10 /
§12 holiday coverage: during 2026-12-20 → 2027-01-04, sent the same day they
are checked, with a note that the team is on holiday schedule).

## Files

- `make_dedication_card.py` — the generator (PIL + Noto Serif CJK, no cost, no network).
- `sample-card-zh.png` / `sample-card-en.png` — TEMPLATE SAMPLES ONLY.
  Placeholders are bracketed. **There are no real claimants yet (0 submissions
  as of 2026-11-08), so no real personalized cards exist. Never fabricate one.**

## Card copy (packet §10, verbatim fields)

- Title: 為你獻上一天 / A Day Dedicated to You
- Recipient: the name as submitted
- Date: the M月D日 as chosen (an effort signal, not a calendar lock)
- One daily verse (scripture text + reference)
- Signature: 米老爸 Daddy Mi 团队 / Team Daddy Mi — 《福音智慧》每日灵修 365 篇，正在汇编
- **Fine print, REQUIRED on every card, both languages:**
  - "This card does not reserve a day or promise inclusion in the book."
  - 「本卡不保留任何一天，也不承诺刊入书中。」

## Usage

```bash
python3 make_dedication_card.py \
  --name "[name exactly as submitted]" \
  --date-line "[M月D日 as chosen]" \
  --verse "[chosen verse text]" \
  --ref "[Book chapter:verse]" \
  --lang zh \
  --out card-<date>-<seq>.png
```

Output is 1600×1000 PNG. Attach to the reply email (do not link to an external host).

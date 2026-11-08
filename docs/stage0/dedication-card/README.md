# Dedication Card — 献词卡 (claim-a-day)

Generator + sample for the Stage-0 dedication card. The card face follows the
approval packet **§10 final copy exactly** (approved 2026-11-08).

## Discipline (packet §10)

- Made **only on request** — for claim-a-day registrants, one card per request.
- The recipient name is used **exactly as submitted — never "corrected"**.
- Total card-production time budget for the whole campaign: **30 minutes**.
- A claim counts as engagement only — never toward E1–E3.
- There are **no claimants yet (0 submissions as of 2026-11-08)**, so no real
  personalized cards exist. The sample below is a bracketed-placeholder
  template render — never fabricate a "real" card.

## Card face (§10 verbatim layout)

```
Day [N] · [scripture reference]
「[one line of that entry's scripture]」
Dedicated to [name] — [dedication line]
献给 [name] —— [dedication line]

A personal reading dedication for [name], inspired by Gospel Wisdom.
This card does not reserve a day or promise inclusion in the book.
这是一张因《福音智慧》而作的个人阅读献词卡。本卡不保留任何一天，也不承诺刊入书中。

Footer: Gospel Wisdom · 福音智慧每日灵修 — https://king818.github.io/daddymi-publications/gospel-wisdom/
```

## Files

- `make_dedication_card.py` — generator (PIL + Noto Serif CJK; no cost, no network; 1600×1000 PNG).
- `sample-card-bilingual.png` — template sample with bracketed placeholders.

## Usage

```bash
python3 make_dedication_card.py \
  --day 128 --ref "Joshua 1:9" \
  --verse-line "[one line of that entry's scripture]" \
  --name "[name exactly as submitted]" \
  --dedication "[dedication line exactly as submitted]" \
  --out card-day128.png
```

Deliver the PNG as an email attachment to the claimant (the packet's §10
thank-you flow rides with the claim-a-day reply; §12 holiday coverage applies
2026-12-20 → 2027-01-04).

#!/usr/bin/env python3
"""Dedication card generator — Gospel Wisdom claim-a-day cards (Stage 0, packet §10 FINAL copy).

Card face follows the approved §10 layout exactly:
    Day [N] · [scripture reference]
    「[one line of that entry's scripture]」
    Dedicated to [name] — [dedication line]
    献给 [name] —— [dedication line]
    Fine print (verbatim, both languages, REQUIRED):
      "A personal reading dedication for [name], inspired by Gospel Wisdom.
       This card does not reserve a day or promise inclusion in the book."
      「这是一张因《福音智慧》而作的个人阅读献词卡。本卡不保留任何一天，也不承诺刊入书中。」
    Footer: Gospel Wisdom · 福音智慧每日灵修 — https://king818.github.io/daddymi-publications/gospel-wisdom/

Discipline (packet §10): made only on request (claim-a-day registrants);
names are used exactly as submitted — never "corrected". Total production
time budget for the whole campaign: 30 minutes.

Usage:
  python3 make_dedication_card.py \
      --day 128 --ref "Joshua 1:9" \
      --verse-line "Be strong and of a good courage; be not afraid." \
      --name "[Name as submitted]" \
      --dedication "[dedication line]" \
      --out card.png
"""
import argparse
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1600, 1000
BG = (250, 247, 240)
INK = (42, 38, 34)
MUTED = (110, 102, 92)
ACCENT = (146, 64, 14)
BORDER = (198, 188, 168)

FONT_REG = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc"
FONT_BOLD = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"

FOOTER = "Gospel Wisdom · 福音智慧每日灵修 — https://king818.github.io/daddymi-publications/gospel-wisdom/"
FINE_EN = ("A personal reading dedication for {name}, inspired by Gospel Wisdom. "
           "This card does not reserve a day or promise inclusion in the book.")
FINE_ZH = "这是一张因《福音智慧》而作的个人阅读献词卡。本卡不保留任何一天，也不承诺刊入书中。"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def wrap(draw, s, f, max_w):
    """Latin wraps on word boundaries; CJK wraps per character."""
    if " " in s:
        lines, cur = [], ""
        for word in s.split(" "):
            trial = (cur + " " + word).strip()
            if cur and text_w(draw, trial, f) > max_w:
                lines.append(cur)
                cur = word
            else:
                cur = trial
        if cur:
            lines.append(cur)
        return lines
    lines, cur = [], ""
    for ch in s:
        trial = cur + ch
        if cur and text_w(draw, trial, f) > max_w:
            lines.append(cur)
            cur = ch
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def center(draw, y, s, f, fill=INK):
    draw.text(((W - text_w(draw, s, f)) / 2, y), s, font=f, fill=fill)
    return y + f.size + 16


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--day", required=True, help="Day number, e.g. 128")
    ap.add_argument("--ref", required=True, help="Scripture reference of that entry")
    ap.add_argument("--verse-line", required=True, help="One line of the entry's scripture")
    ap.add_argument("--name", required=True, help="Name exactly as submitted")
    ap.add_argument("--dedication", required=True, help="Dedication short line as submitted")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([36, 36, W - 36, H - 36], radius=28, outline=BORDER, width=3)
    d.rounded_rectangle([52, 52, W - 52, H - 52], radius=20, outline=BORDER, width=1)

    y = 120
    y = center(d, y, f"Day {args.day} · {args.ref}", font(FONT_BOLD, 58), ACCENT)
    y += 22
    f_verse = font(FONT_REG, 44)
    for ln in wrap(d, f"「{args.verse_line}」", f_verse, W - 300):
        y = center(d, y, ln, f_verse)
    y += 36
    y = center(d, y, f"Dedicated to {args.name} — {args.dedication}", font(FONT_BOLD, 42))
    y = center(d, y, f"献给 {args.name} ——{args.dedication}", font(FONT_BOLD, 42))

    f_fine = font(FONT_REG, 25)
    fine_en = wrap(d, FINE_EN.format(name=args.name), f_fine, W - 260)
    fy = H - 96 - (len(fine_en) + 1) * 41 - 34
    for ln in fine_en:
        fy = center(d, fy, ln, f_fine, MUTED)
    fy = center(d, fy, FINE_ZH, f_fine, MUTED)
    center(d, H - 96, FOOTER, font(FONT_REG, 24), MUTED)

    img.save(args.out, "PNG")
    print(f"wrote {args.out} ({W}x{H})")


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Dedication card generator — Gospel Wisdom claim-a-day thank-you cards (Stage 0, packet §10).

Renders a 1600x1000 PNG dedication card from the approved copy:
  - Title: 為你獻上一天 / A Day Dedicated to You
  - Recipient line (name is read as submitted; NEVER corrected — packet §10)
  - Date line: 「◯月◯日」as chosen (effort signal, not a calendar lock)
  - Daily verse (scripture text + reference)
  - Signature block
  - Fine print (REQUIRED, verbatim): "This card does not reserve a day or promise
    inclusion in the book." + 中文等值「本卡不保留任何一天，也不承诺刊入书中。」
  Fonts: Noto Serif CJK (local system fonts). No external assets, no cost.

Usage:
  python3 make_dedication_card.py \
      --name "[Name as submitted]" \
      --date-line "[M月D日 as chosen]" \
      --verse "[verse text]" \
      --ref "[Book chapter:verse]" \
      --lang zh|en \
      --out card.png
"""
import argparse
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1600, 1000
BG = (250, 247, 240)          # warm paper
INK = (42, 38, 34)            # near-black warm
MUTED = (110, 102, 92)
ACCENT = (146, 64, 14)        # deep amber, same family as the public pages
BORDER = (198, 188, 168)
WHITE = (255, 255, 255)

FONT_REG = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc"
FONT_BOLD = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"

FINE_ZH = "本卡不保留任何一天，也不承诺刊入书中。"
FINE_EN = "This card does not reserve a day or promise inclusion in the book."
SIGN_ZH = ["署名：", "米老爸 Daddy Mi 团队", "《福音智慧》每日灵修 365 篇，正在汇编"]
SIGN_EN = ["Signed,", "Team Daddy Mi", "Gospel Wisdom — a daily devotional of 365 entries, now being compiled"]


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def wrap(draw, s, f, max_w):
    """Greedy wrap: Latin text wraps on word boundaries; CJK wraps per character."""
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
    return y + f.size + 14


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--date-line", required=True)
    ap.add_argument("--verse", required=True)
    ap.add_argument("--ref", required=True)
    ap.add_argument("--lang", choices=["zh", "en"], default="zh")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    zh = args.lang == "zh"
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([36, 36, W - 36, H - 36], radius=28, outline=BORDER, width=3)
    d.rounded_rectangle([52, 52, W - 52, H - 52], radius=20, outline=BORDER, width=1)

    y = 96
    f_title = font(FONT_BOLD, 64)
    y = center(d, y, "為你獻上一天" if zh else "A Day Dedicated to You", f_title, ACCENT)
    y += 6
    f_sub = font(FONT_REG, 30)
    y = center(d, y, "《福音智慧》每日灵修 · 认领一天" if zh else "Gospel Wisdom Daily Devotional · Claim a Day", f_sub, MUTED)
    y += 26

    f_name = font(FONT_BOLD, 46)
    y = center(d, y, (f"獻給 {args.name}" if zh else f"Dedicated to {args.name}"), f_name)
    f_date = font(FONT_REG, 38)
    y = center(d, y, (f"你選的日子：{args.date_line}" if zh else f"The day you chose: {args.date_line}"), f_date)
    y += 30

    f_verse = font(FONT_REG, 40)
    lines = wrap(d, args.verse, f_verse, W - 320)
    for ln in lines:
        y = center(d, y, ln, f_verse)
    f_ref = font(FONT_REG, 30)
    y = center(d, y, f"—— {args.ref}", f_ref, MUTED)
    y += 34

    f_sign = font(FONT_REG, 30)
    for ln in (SIGN_ZH if zh else SIGN_EN):
        y = center(d, y, ln, f_sign, MUTED)

    f_fine = font(FONT_REG, 24)
    fine_lines = [FINE_ZH, FINE_EN] if zh else [FINE_EN, FINE_ZH]
    fy = H - 150
    for ln in fine_lines:
        fy = center(d, fy, ln, f_fine, MUTED)

    img.save(args.out, "PNG")
    print(f"wrote {args.out} ({W}x{H})")


if __name__ == "__main__":
    sys.exit(main())

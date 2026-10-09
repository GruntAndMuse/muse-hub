#!/usr/bin/env python3
"""stamp-shot.py — burn a timestamp banner into a screenshot.

Replaces the inline python3 -c one-liner in the deed-watch cron definition.
Same output, reviewable code, reusable everywhere.

Usage:
    stamp-shot.py IMAGE [--label TEXT] [--font-size N]

Default label: "Screenshot captured YYYY-MM-DD HH:MM PDT | <basename>"
"""
import argparse
import datetime
import os
import sys

from PIL import Image, ImageDraw, ImageFont

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("image", help="PNG/JPG to stamp (modified in place)")
    ap.add_argument("--label", default=None)
    ap.add_argument("--font-size", type=int, default=28)
    args = ap.parse_args()

    if not os.path.isfile(args.image):
        print(f"no such file: {args.image}", file=sys.stderr)
        return 1

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    label = args.label or f"Screenshot captured {now} | {os.path.basename(args.image)}"

    img = Image.open(args.image).convert("RGB")
    w, h = img.size
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype(FONT, args.font_size)
    except OSError:
        font = ImageFont.load_default()

    bb = d.textbbox((0, 0), label, font=font)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    bh = th + 24
    d.rectangle([0, h - bh, w, h], fill=(0, 0, 0))
    d.text(((w - tw) // 2, h - bh + 12), label, fill=(255, 255, 0), font=font)
    img.save(args.image)
    print(f"stamped: {args.image}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

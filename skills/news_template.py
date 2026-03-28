#!/usr/bin/env python3
"""
News Template V8 - Clean. Full image. Text at bottom only.
No badges, no clutter. Just image + headline + description at bottom.
"""

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Error: pip3 install Pillow", file=sys.stderr)
    sys.exit(1)

W = 1080
H = 1350
MARGIN = 50


def font(size, bold=False):
    paths_bold = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/ArialHB.ttc",
        "/System/Library/Fonts/HelveticaNeue.ttc",
    ]
    paths_reg = [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/HelveticaNeue.ttc",
    ]
    for p in (paths_bold if bold else paths_reg):
        try:
            idx = 1 if (bold and p.endswith(".ttc")) else 0
            return ImageFont.truetype(p, size, index=idx)
        except (OSError, IndexError):
            try:
                return ImageFont.truetype(p, size, index=0)
            except (OSError, IndexError):
                continue
    return ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = f"{cur} {w}".strip()
        if draw.textbbox((0, 0), test, font=fnt)[2] <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def create_news_post(headline, summary, category, brand, filename,
                     bg_image_path=None, breaking=False):

    img = Image.new("RGB", (W, H), (10, 10, 18))

    # =========================================
    # IMAGE: fills entire canvas
    # =========================================
    if bg_image_path and Path(bg_image_path).exists():
        try:
            bg = Image.open(bg_image_path).convert("RGB")
            scale = max(W / bg.width, H / bg.height)
            new_w = int(bg.width * scale)
            new_h = int(bg.height * scale)
            bg = bg.resize((new_w, new_h), Image.LANCZOS)
            left = (new_w - W) // 2
            top = (new_h - H) // 2
            bg = bg.crop((left, top, left + W, top + H))
            img.paste(bg, (0, 0))
        except Exception:
            pass

    # =========================================
    # GRADIENT: only bottom 40%, subtle
    # Image shows through
    # =========================================
    grad_start = int(H * 0.60)
    for y in range(grad_start, H):
        ratio = (y - grad_start) / (H - grad_start)
        opacity = (ratio ** 1.2) * 0.8
        overlay = Image.new("RGBA", (W, 1), (0, 0, 0, int(opacity * 255)))
        img.paste(
            Image.alpha_composite(
                img.crop((0, y, W, y + 1)).convert("RGBA"), overlay
            ).convert("RGB"),
            (0, y)
        )

    draw = ImageDraw.Draw(img)

    # =========================================
    # HEADLINE - bottom, left aligned, multi-color
    # =========================================
    f_head = font(52, bold=True)
    head_lines = wrap(draw, headline.upper(), f_head, W - MARGIN * 2)

    # Bigger description
    f_desc = font(32)
    desc_lines = wrap(draw, summary, f_desc, W - MARGIN * 2)
    # Ensure min 2 lines, max 3
    desc_lines = desc_lines[:3]

    # Bottom margin
    bottom_pad = 60
    desc_total = len(desc_lines) * 44
    head_total = len(head_lines[:3]) * 64
    red_line = 25

    # Start positions (from bottom)
    desc_start = H - bottom_pad - desc_total
    head_start = desc_start - red_line - head_total - 10

    # Headline colors - alternate between yellow and white
    head_colors = [
        (255, 210, 45),    # Yellow
        (255, 255, 255),   # White
        (100, 200, 255),   # Light blue
    ]

    for i, line in enumerate(head_lines[:3]):
        lx = MARGIN
        color = head_colors[i % len(head_colors)]

        # Strong shadow
        for ox, oy in [(3, 3), (2, 2), (1, 1), (-1, -1), (0, 2), (2, 0)]:
            draw.text((lx + ox, head_start + oy), line, fill=(0, 0, 0), font=f_head)
        draw.text((lx, head_start), line, fill=color, font=f_head)
        head_start += 64

    # Red accent line
    draw.rectangle((MARGIN, head_start + 5, MARGIN + 70, head_start + 9), fill=(220, 35, 35))

    # =========================================
    # DESCRIPTION - bigger, 2-3 lines
    # =========================================
    for line in desc_lines:
        for ox, oy in [(2, 2), (1, 1), (-1, 1)]:
            draw.text((MARGIN + ox, desc_start + oy), line, fill=(0, 0, 0), font=f_desc)
        draw.text((MARGIN, desc_start), line, fill=(220, 220, 225), font=f_desc)
        desc_start += 44

    # =========================================
    # SAVE
    # =========================================
    out = Path(filename)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(out), "PNG", quality=95)
    print(f"Image saved: {out.resolve()}")
    print(f"MEDIA:{out.resolve()}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--headline", "-hl", required=True)
    p.add_argument("--summary", "-s", required=True)
    p.add_argument("--category", "-c", default="NEWS")
    p.add_argument("--brand", "-b", default="VK NEWS")
    p.add_argument("--filename", "-f", required=True)
    p.add_argument("--bg-image", "-bg", default=None)
    p.add_argument("--breaking", action="store_true")
    args = p.parse_args()
    create_news_post(args.headline, args.summary, args.category,
                     args.brand, args.filename, args.bg_image, args.breaking)


if __name__ == "__main__":
    main()

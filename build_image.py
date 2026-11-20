#!/usr/bin/env python3
"""Build the news-image entry: draw a one-day world-news front page (1024x1024 PNG).

Reads the day's top stories (hard-coded from reporting of 20 Nov 2026) and renders
a clean newspaper-style summary. Run: python3 build_image.py  ->  writes news.png
in this directory. The entry program (main.py) then copies news.png to /output/entry.png.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36

NAVY = (20, 33, 61)
GOLD = (252, 163, 17)
PAPER = (250, 247, 242)
INK = (24, 24, 24)
GREY = (90, 90, 90)
CARD = (255, 255, 255)
LINE = (210, 205, 195)
RED = (178, 34, 34)
BLUE = (30, 80, 160)
GREEN = (28, 110, 70)
ORANGE = (200, 90, 20)
SLATE = (90, 80, 140)
TEAL = (14, 110, 110)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_chip(draw, x, y, label, color):
    f = font(FONT_BOLD, 15)
    tw = draw.textlength(label, font=f)
    pad_x, pad_y = 10, 5
    draw.rounded_rectangle([x, y, x + tw + pad_x * 2, y + 26], radius=4, fill=color)
    draw.text((x + pad_x, y + pad_y), label, font=f, fill=(255, 255, 255))
    return tw + pad_x * 2


def draw_story(draw, x, y, w, h, chip_label, chip_color, headline, summary,
               head_size, sum_size):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=CARD,
                           outline=LINE, width=1)
    cx, cy = x + 16, y + 14
    draw_chip(draw, cx, cy, chip_label, chip_color)
    ty = cy + 34
    hf = font(FONT_BOLD, head_size)
    for line in wrap(draw, headline, hf, w - 32):
        draw.text((x + 16, ty), line, font=hf, fill=INK)
        ty += head_size + 6
    ty += 2
    sf = font(FONT_REG, sum_size)
    for line in wrap(draw, summary, sf, w - 32):
        draw.text((x + 16, ty), line, font=sf, fill=GREY)
        ty += sum_size + 6


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.rectangle([0, 0, W, 148], fill=NAVY)
    title_f = font(FONT_SERIF_BOLD, 58)
    d.text((MARGIN, 22), "THE WORLD IN ONE DAY", font=title_f, fill=(255, 255, 255))
    date_f = font(FONT_BOLD, 32)
    d.text((MARGIN, 96), "Friday, 20 November 2026", font=date_f, fill=GOLD)
    # small globe motif, top right
    gx, gy, gr = W - 92, 74, 34
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], outline=GOLD, width=3)
    d.ellipse([gx - gr // 2, gy - gr, gx + gr // 2, gy + gr], outline=GOLD, width=2)
    d.line([gx - gr, gy, gx + gr, gy], fill=GOLD, width=2)
    d.rectangle([0, 148, W, 154], fill=GOLD)

    # Lead story (full width)
    draw_story(d, MARGIN, 170, W - 2 * MARGIN, 180,
               "JUSTICE", RED,
               "World Court: Myanmar committed genocide against the Rohingya",
               "The International Court of Justice rules 9-6 that Myanmar's forces "
               "committed genocide - the court's first such finding against a state.",
               30, 21)

    # Grid 2x2
    col_w = (W - 2 * MARGIN - 16) // 2
    draw_story(d, MARGIN, 366, col_w, 200,
               "DIPLOMACY", BLUE,
               "Trump, Xi and Putin meet in Shenzhen",
               "First three-way summit ends with a joint peace declaration after "
               "~70 minutes; no breakthrough on Ukraine, Iran or arms limits.",
               25, 19)
    draw_story(d, MARGIN + col_w + 16, 366, col_w, 200,
               "MARKETS", GREEN,
               "Anthropic soars on Nasdaq debut; stocks slide",
               "Shares close near $97, 17% above the $83 IPO price. S&P 500 falls "
               "~2% for a fifth day; Nikkei drops 4.8%.",
               25, 19)
    draw_story(d, MARGIN, 582, col_w, 200,
               "MIDDLE EAST", ORANGE,
               "Houthi missile hits Riyadh's tallest tower",
               "A missile strikes the Saudi sovereign wealth fund tower in the "
               "financial district, blowing out windows across eight floors.",
               25, 19)
    draw_story(d, MARGIN + col_w + 16, 582, col_w, 200,
               "EUROPE", SLATE,
               "Russian strikes hit Kyiv bridges; 8 killed",
               "Overnight attacks kill eight and injure 28 across nine regions. "
               "Ukraine's allies meet in Berlin.",
               25, 19)

    # Bottom story (full width)
    draw_story(d, MARGIN, 798, W - 2 * MARGIN, 140,
               "USA", TEAL,
               "Trump: no Iran decision until 2027",
               "President says he won't decide the next step until the new year. "
               "Senate blocks a measure to end the war, 51-48.",
               27, 20)

    # Footer
    ff = font(FONT_REG, 15)
    d.text((MARGIN, 954),
           "Sources: International Court of Justice  |  Reuters  |  AP  |  SCMP  |  Just Security",
           font=ff, fill=GREY)
    d.text((MARGIN, 978), "20 November 2026  |  All events reported on this day.",
           font=ff, fill=GREY)

    img.save("news.png", optimize=True)
    print("wrote news.png", img.size)


if __name__ == "__main__":
    main()

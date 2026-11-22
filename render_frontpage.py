#!/usr/bin/env python3
"""Render the front page for Sunday 22 November 2026.

Draws a newspaper front page ("THE WORLD") with Pillow and writes it to
entry.png (or to the path given as the first argument). Pure stdlib + Pillow,
no network, fully deterministic: the same code always paints the same bytes.
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
INK = (18, 18, 18)
PAPER = (255, 255, 255)
ACCENT = (176, 32, 32)
MUTE = (105, 105, 105)
WASH = (238, 238, 238)
SEA = (46, 92, 128)
SKY = (224, 232, 238)
FIRE = (216, 108, 28)
LEAF = (96, 128, 84)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def load(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def serif_b(size):
    return load("DejaVuSerif-Bold.ttf", size)


def serif(size):
    return load("DejaVuSerif.ttf", size)


def sans_b(size):
    return load("DejaVuSans-Bold.ttf", size)


def sans(size):
    return load("DejaVuSans.ttf", size)


def wrap(pen, text, font, width):
    """Split text into lines that fit inside width (measured, not guessed)."""
    lines = []
    current = ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if pen.textlength(trial, font=font) <= width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def put_lines(pen, x, y, lines, font, fill, gap):
    for line in lines:
        pen.text((x, y), line, font=font, fill=fill)
        y += gap
    return y


def kicker(pen, x, y, text):
    pen.text((x, y), text, font=sans_b(16), fill=ACCENT)


def headline(pen, x, y, text, size, width):
    font = serif_b(size)
    lines = wrap(pen, text, font, width)
    return put_lines(pen, x, y, lines, font, INK, int(size * 1.18))


def subhead(pen, x, y, text, size, width):
    font = serif(size)
    lines = wrap(pen, text, font, width)
    return put_lines(pen, x, y, lines, font, (52, 52, 52), int(size * 1.32))


def rule(pen, x0, y, x1, weight=2):
    pen.line([(x0, y), (x1, y)], fill=INK, width=weight)


def frame_box(pen, x0, y0, x1, y1, fill=WASH):
    pen.rectangle([x0, y0, x1, y1], fill=fill, outline=MUTE, width=1)


def star(pen, cx, cy, r, fill):
    import math

    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    pen.polygon(pts, fill=fill)


# ---------------------------------------------------------------- sketches

def sketch_ship(pen, x0, y0, x1, y1):
    """Cargo ship on fire, two drones above, a lifeboat on the waves."""
    w, h = x1 - x0, y1 - y0
    sea_y = y0 + int(h * 0.68)
    pen.rectangle([x0, y0, x1, sea_y], fill=SKY)
    pen.rectangle([x0, sea_y, x1, y1], fill=SEA)
    for i in range(4):
        wx = x0 + 20 + i * 85
        pen.arc([wx, sea_y + 12, wx + 60, sea_y + 34], 180, 360,
                fill=(255, 255, 255), width=3)
    hull_y = sea_y - 34
    pen.polygon([(x0 + 18, hull_y), (x1 - 18, hull_y),
                 (x1 - 52, hull_y + 34), (x0 + 44, hull_y + 34)],
                fill=(38, 38, 44))
    pen.rectangle([x0 + 52, hull_y - 34, x0 + 122, hull_y], fill=(150, 52, 44))
    pen.rectangle([x0 + 130, hull_y - 34, x0 + 196, hull_y], fill=(96, 96, 96))
    pen.rectangle([x0 + 204, hull_y - 22, x0 + 258, hull_y], fill=(150, 52, 44))
    for sx, sy in ((x0 + 90, hull_y - 62), (x0 + 150, hull_y - 78),
                   (x0 + 210, hull_y - 58)):
        pen.ellipse([sx, sy, sx + 34, sy + 26], fill=(120, 120, 120))
        pen.ellipse([sx + 10, sy - 14, sx + 36, sy + 6], fill=(150, 150, 150))
    pen.polygon([(x0 + 150, hull_y - 34), (x0 + 168, hull_y - 66),
                 (x0 + 186, hull_y - 34)], fill=FIRE)
    pen.polygon([(x0 + 196, hull_y - 34), (x0 + 210, hull_y - 58),
                 (x0 + 224, hull_y - 34)], fill=(232, 160, 40))
    for dx, dy in ((x0 + 60, y0 + 26), (x1 - 110, y0 + 44)):
        pen.rectangle([dx, dy, dx + 26, dy + 10], fill=INK)
        pen.line([(dx - 8, dy - 2), (dx + 34, dy - 2)], fill=INK, width=2)
        pen.line([(dx - 8, dy + 12), (dx + 34, dy + 12)], fill=INK, width=2)
        pen.line([(dx + 13, dy + 10), (dx + 13, dy + 26)], fill=INK, width=2)
    pen.ellipse([x1 - 96, sea_y + 16, x1 - 30, sea_y + 34], fill=(232, 120, 30))
    pen.rectangle([x1 - 88, sea_y + 10, x1 - 38, sea_y + 18], fill=(232, 120, 30))


def sketch_quake(pen, x0, y0, x1, y1):
    """Cracked ground, mountains, and a seismograph trace."""
    w, h = x1 - x0, y1 - y0
    mid = y0 + int(h * 0.55)
    pen.polygon([(x0, y1), (x0 + int(w * 0.30), y0 + 14),
                 (x0 + int(w * 0.55), y1)], fill=(120, 120, 118))
    pen.polygon([(x0 + int(w * 0.38), y1), (x0 + int(w * 0.68), y0 + 30),
                 (x0 + w, y1)], fill=(150, 150, 148))
    pen.line([(x0 + int(w * 0.5), y0 + 8), (x0 + int(w * 0.46), mid),
              (x0 + int(w * 0.58), mid + 18), (x0 + int(w * 0.52), y1 - 8)],
             fill=INK, width=3)
    trace = [(x0 + 8, mid), (x0 + 26, mid), (x0 + 34, mid - 22),
             (x0 + 42, mid + 20), (x0 + 50, mid - 8), (x0 + 58, mid + 8),
             (x0 + 66, mid - 26), (x0 + 74, mid + 24), (x0 + 82, mid - 6),
             (x0 + 92, mid), (x0 + 110, mid), (x0 + 122, mid - 14),
             (x0 + 130, mid)]
    pen.line(trace, fill=ACCENT, width=3)


def sketch_flag(pen, x0, y0, x1, y1):
    """Danish flag on a pole above a ministry building."""
    w, h = x1 - x0, y1 - y0
    pole_x = x0 + int(w * 0.5)
    pen.line([(pole_x, y0 + 12), (pole_x, y1 - 34)], fill=INK, width=3)
    fx0, fy0 = pole_x + 4, y0 + 12
    fw, fh = int(w * 0.52), 34
    pen.rectangle([fx0, fy0, fx0 + fw, fy0 + fh], fill=(178, 32, 32))
    pen.rectangle([fx0 + 12, fy0, fx0 + 20, fy0 + fh], fill=PAPER)
    pen.rectangle([fx0, fy0 + 13, fx0 + fw, fy0 + 21], fill=PAPER)
    by0 = y1 - 34
    pen.rectangle([x0 + 6, by0, x1 - 6, y1], fill=(120, 120, 118))
    for i in range(4):
        wx = x0 + 16 + i * 28
        pen.rectangle([wx, by0 + 8, wx + 14, by0 + 22], fill=PAPER)


def sketch_trade(pen, x0, y0, x1, y1):
    """EU and Indonesian flags above a signed document."""
    w, h = x1 - x0, y1 - y0
    pen.rectangle([x0 + 8, y0 + 10, x0 + 58, y0 + 40], fill=(28, 52, 112))
    for i in range(12):
        import math
        ang = i * math.pi / 6
        pen.ellipse([x0 + 31 + 15 * math.cos(ang) - 2,
                     y0 + 25 + 10 * math.sin(ang) - 2,
                     x0 + 31 + 15 * math.cos(ang) + 2,
                     y0 + 25 + 10 * math.sin(ang) + 2], fill=(232, 200, 40))
    pen.rectangle([x0 + 66, y0 + 10, x0 + 116, y0 + 25], fill=(178, 32, 32))
    pen.rectangle([x0 + 66, y0 + 25, x0 + 116, y0 + 40], fill=PAPER)
    pen.rectangle([x0 + 14, y0 + 52, x1 - 14, y1 - 8], fill=PAPER,
                  outline=MUTE, width=1)
    for i in range(4):
        ly = y0 + 62 + i * 12
        pen.line([(x0 + 22, ly), (x1 - 34, ly)], fill=MUTE, width=2)
    pen.ellipse([x1 - 44, y1 - 30, x1 - 20, y1 - 8], fill=ACCENT)


def sketch_cuffs(pen, x0, y0, x1, y1):
    """Handcuffs and a police star."""
    w, h = x1 - x0, y1 - y0
    cy = y0 + int(h * 0.62)
    pen.ellipse([x0 + 10, cy - 26, x0 + 58, cy + 22], outline=INK, width=5)
    pen.ellipse([x0 + 72, cy - 26, x0 + 120, cy + 22], outline=INK, width=5)
    pen.line([(x0 + 56, cy - 2), (x0 + 74, cy - 2)], fill=INK, width=4)
    star(pen, x0 + int(w * 0.5), y0 + 26, 22, (212, 160, 32))
    star(pen, x0 + int(w * 0.5), y0 + 26, 10, PAPER)


def sketch_climate(pen, x0, y0, x1, y1):
    """A warming globe beside a thermometer."""
    w, h = x1 - x0, y1 - y0
    cx, cy = x0 + int(w * 0.32), y0 + int(h * 0.5)
    r = min(w, h) // 2 - 10
    pen.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 120, 170))
    pen.ellipse([cx - r + 10, cy - r + 8, cx - 4, cy - 2], fill=LEAF)
    pen.ellipse([cx - 2, cy + 2, cx + r - 8, cy + r - 10], fill=LEAF)
    tx = x0 + int(w * 0.72)
    pen.rectangle([tx - 7, y0 + 10, tx + 7, y1 - 22], outline=INK, width=2)
    pen.rectangle([tx - 4, y0 + 22, tx + 4, y1 - 26], fill=ACCENT)
    pen.ellipse([tx - 12, y1 - 30, tx + 12, y1 - 6], fill=ACCENT)
    pen.line([(tx + 16, y0 + 20), (tx + 16, y1 - 20)], fill=MUTE, width=2)
    for i in range(3):
        pen.line([(tx + 16, y0 + 24 + i * 18), (tx + 22, y0 + 24 + i * 18)],
                 fill=MUTE, width=2)


# ---------------------------------------------------------------- page

STORIES = [
    dict(tag="GULF OF FINLAND",
         head="Drones Strike Russian Cargo Ship in the Baltic",
         body="Sparta II ablaze after two drone strikes; 16 crew take to "
              "lifeboats as the ship drifts into Finnish waters. Finland "
              "points to Ukraine and tightens air and sea curbs.",
         art=sketch_ship),
    dict(tag="INDONESIA",
         head="M7.2 Quake Strikes Off Maluku",
         body="BMKG puts the tremor 43 km off Southwest Maluku at 125 km "
              "deep; felt as far as Timor-Leste and Kupang. No tsunami "
              "warning.",
         art=sketch_quake),
    dict(tag="DENMARK",
         head="Denmark Expels Russian Attaché",
         body="Copenhagen says Russian intelligence plotted to kill rapper "
              "Kyivstoner at a September concert; two charged after the "
              "plot was foiled.",
         art=sketch_flag),
    dict(tag="TRADE",
         head="EU and Indonesia Sign Trade Pact",
         body="After a decade of talks, IEU-CEPA scraps duties on over 90% "
              "of tariff lines; EU exporters save about €600m a year.",
         art=sketch_trade),
    dict(tag="MEXICO",
         head="Mexico Captures Most-Wanted Cartel Boss",
         body="Fausto Isidro Meza Flores, known as 'El Chapo Isidro', "
              "seized in a Sinaloa raid on Saturday.",
         art=sketch_cuffs),
    dict(tag="CLIMATE",
         head="COP31 Deadlocked on Fossil Fuels",
         body="Climate talks in Antalya stall over the future of fossil "
              "fuels and climate finance as the summit nears its close.",
         art=sketch_climate),
]

TICKER = [
    "M6.7 quake rattles Peru's Andes; Lima residents rush into the streets",
    "UN talks on killer robots end with no binding rules  •  "
    "Japan–India deepen military ties",
]


def masthead(pen):
    title = "THE WORLD"
    font = serif_b(62)
    tw = pen.textlength(title, font=font)
    pen.text(((PAGE - tw) / 2, 30), title, font=font, fill=INK)
    rule(pen, 30, 102, 994, 2)
    date = "SUNDAY, 22 NOVEMBER 2026"
    dfont = sans_b(21)
    dw = pen.textlength(date, font=dfont)
    pen.text(((PAGE - dw) / 2, 110), date, font=dfont, fill=ACCENT)
    rule(pen, 30, 140, 994, 2)


def lead_story(pen, story):
    kicker(pen, 30, 152, story["tag"])
    y = headline(pen, 30, 180, story["head"], 37, 560)
    subhead(pen, 30, y + 8, story["body"], 17, 560)
    frame_box(pen, 625, 156, 994, 380)
    story["art"](pen, 627, 158, 992, 378)


def half_column(pen, story, x0, y0, x1):
    """One of the two-column stories: text left, sketch right."""
    kicker(pen, x0, y0 + 4, story["tag"])
    y = headline(pen, x0, y0 + 28, story["head"], 25, 300)
    subhead(pen, x0, y + 6, story["body"], 15, 300)
    frame_box(pen, x0 + 318, y0 + 28, x1 - 6, y0 + 168)
    story["art"](pen, x0 + 320, y0 + 30, x1 - 8, y0 + 166)


def closing_story(pen, story, y0):
    kicker(pen, 30, y0 + 4, story["tag"])
    headline(pen, 30, y0 + 28, story["head"], 28, 720)
    subhead(pen, 30, y0 + 62, story["body"], 16, 720)
    frame_box(pen, 780, y0 + 8, 994, y0 + 92)
    story["art"](pen, 782, y0 + 10, 992, y0 + 90)


def ticker_band(pen):
    pen.rectangle([17, 896, 1007, 1007], fill=ACCENT)
    font = sans(18)
    for i, line in enumerate(TICKER):
        tw = pen.textlength(line, font=font)
        pen.text(((PAGE - tw) / 2, 918 + i * 34), line, font=font,
                 fill=PAPER)


def build(path):
    sheet = Image.new("RGB", (PAGE, PAGE), PAPER)
    pen = ImageDraw.Draw(sheet)
    masthead(pen)
    lead_story(pen, STORIES[0])
    rule(pen, 30, 392, 994, 2)
    half_column(pen, STORIES[1], 30, 400, 500)
    half_column(pen, STORIES[2], 524, 400, 994)
    pen.line([(512, 404), (512, 576)], fill=MUTE, width=1)
    rule(pen, 30, 588, 994, 2)
    half_column(pen, STORIES[3], 30, 596, 500)
    half_column(pen, STORIES[4], 524, 596, 994)
    pen.line([(512, 600), (512, 772)], fill=MUTE, width=1)
    rule(pen, 30, 784, 994, 2)
    closing_story(pen, STORIES[5], 792)
    ticker_band(pen)
    pen.rectangle([16, 16, 1007, 1007], outline=INK, width=3)
    sheet.save(path, "PNG")


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else "entry.png")

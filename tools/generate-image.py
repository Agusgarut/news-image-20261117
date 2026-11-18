#!/usr/bin/env python3
"""Draw the 17 November 2026 front page (1024x1024) with Pillow only.

Newspaper front-page template, in my own words and drawings:
masthead, giant serif date, 13 story panels in 3 rows, a world map
with numbered pins, and an "also on Tuesday" list. No photos, no
downloaded art, no copied text. Run: python3 tools/generate-image.py
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1024, 1024
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "entry.png")

SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SERIFB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"

NAVY = (19, 33, 61)
PAPER = (246, 240, 221)
INK = (20, 20, 20)
RED = (178, 34, 34)
GREY = (100, 100, 100)
BLUE = (43, 94, 167)
CRIMSON = (179, 64, 46)
GREEN = (46, 125, 79)
PURPLE = (106, 74, 158)
TEAL = (29, 122, 140)
SLATE = (52, 58, 64)

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
d.rectangle([5, 5, W - 6, H - 6], outline=NAVY, width=2)

# ---------- header ----------
d.text((16, 14), "THE WORLD'S NEWS IN ONE PICTURE", font=font(SANSB, 15), fill=RED)
right = "13 STORIES  ·  4 CONTINENTS  ·  ALL FROM TUESDAY"
d.text((W - 16 - d.textlength(right, font=font(SANSB, 15)), 14), right,
       font=font(SANSB, 15), fill=GREY)
# ---------- giant date ----------
title = "Tuesday 17 November 2026"
tw = d.textlength(title, font=font(SERIFB, 56))
d.text(((W - tw) / 2, 40), title, font=font(SERIFB, 56), fill=INK)
d.line([16, 112, W - 16, 112], fill=INK, width=3)
d.line([16, 117, W - 16, 117], fill=INK, width=1)

# ---------- pictograms ----------
def pic(kind, x, y, w, h):
    if kind == "bridge":
        d.rectangle([x, y, x + w, y + h], fill=(207, 232, 245))
        d.rectangle([x, y + h - 22, x + w, y + h], fill=TEAL)
        d.rectangle([x, y + h - 48, x + w // 3, y + h - 40], fill=(60, 60, 60))
        d.rectangle([x + 2 * w // 3, y + h - 48, x + w, y + h - 40], fill=(60, 60, 60))
        d.polygon([(x + w // 3 + 6, y + h - 46), (x + 2 * w // 3 - 4, y + h - 30),
                   (x + 2 * w // 3 - 16, y + h - 18), (x + w // 3 + 14, y + h - 30)], fill=(90, 90, 90))
        d.ellipse([x + w // 2 - 14, y + 6, x + w // 2 + 14, y + 28], fill=(200, 200, 200))
    elif kind == "radar":
        d.rectangle([x, y, x + w, y + h], fill=(232, 213, 163))
        d.pieslice([x + w // 2 - 34, y + 4, x + w // 2 + 34, y + 72], 180, 360,
                   fill=(255, 255, 255), outline=NAVY, width=2)
        d.line([x + w // 2, y + 38, x + w // 2 + 28, y + 14], fill=RED, width=3)
        d.rectangle([x + 10, y + h - 18, x + 76, y + h - 8], fill=(120, 60, 40))
        d.polygon([(x + 22, y + h - 18), (x + 64, y + h - 18), (x + 54, y + h - 32), (x + 32, y + h - 32)],
                  fill=(90, 90, 90))
        d.polygon([(x + 40, y + h - 34), (x + 46, y + h - 44), (x + 52, y + h - 34)], fill=(220, 60, 30))
    elif kind == "summit":
        d.rectangle([x, y, x + w, y + h], fill=(198, 222, 240))
        for bx, bw, bh in [(x + 10, 46, 30), (x + 66, 60, 44), (x + 136, 40, 26)]:
            d.rectangle([bx, y + h - bh, bx + bw, y + h], fill=NAVY)
        d.line([x + w - 52, y + 6, x + w - 52, y + h - 6], fill=(60, 60, 60), width=3)
        d.rectangle([x + w - 52, y + 6, x + w - 22, y + 22], fill=RED)
        d.line([x + w - 84, y + 6, x + w - 84, y + h - 6], fill=(60, 60, 60), width=3)
        d.rectangle([x + w - 84, y + 6, x + w - 58, y + 22], fill=(255, 255, 255), outline=RED, width=2)
    elif kind == "truck":
        d.rectangle([x, y, x + w, y + h], fill=(240, 228, 200))
        d.rectangle([x + 56, y + 16, x + w - 66, y + h - 16], fill=(255, 255, 255), outline=NAVY, width=2)
        d.rectangle([x + w - 56, y + 24, x + w - 12, y + h - 16], fill=RED)
        d.ellipse([x + 72, y + h - 18, x + 94, y + h - 2], fill=(30, 30, 30))
        d.ellipse([x + w - 52, y + h - 18, x + w - 30, y + h - 2], fill=(30, 30, 30))
        d.text((x + 10, y + 8), "AID", font=font(SANSB, 18), fill=RED)
    elif kind == "jet":
        d.rectangle([x, y, x + w, y + h], fill=(207, 232, 245))
        d.ellipse([x + w - 52, y + 6, x + w - 8, y + 50], fill=(220, 60, 50))
        d.polygon([(x + 14, y + h // 2 - 4), (x + w - 70, y + h // 2 - 10), (x + w - 56, y + h // 2),
                   (x + w - 70, y + h // 2 + 10), (x + 14, y + h // 2 + 4)], fill=NAVY)
        d.polygon([(x + 60, y + h // 2 - 8), (x + 92, y + 4), (x + 102, y + h // 2 - 8)], fill=NAVY)
    elif kind == "map":
        d.rectangle([x, y, x + w, y + h], fill=(210, 235, 205))
        d.polygon([(x + w // 2 - 18, y + 6), (x + w // 2 + 34, y + 6), (x + w // 2 + 52, y + 24),
                   (x + w // 2 + 40, y + h - 8), (x + w // 2 - 6, y + h - 12), (x + w // 2 - 24, y + 22)],
                  fill=(90, 160, 90), outline=(40, 100, 40))
        d.ellipse([x + w // 2 - 6, y + 12, x + w // 2 + 10, y + 28], fill=RED)
        d.polygon([(x + w // 2 + 2, y + 28), (x + w // 2 - 3, y + 38), (x + w // 2 + 7, y + 38)], fill=RED)
        d.text((x + 8, y + 6), "RWANDA", font=font(SANSB, 13), fill=NAVY)
    elif kind == "yurt":
        d.rectangle([x, y, x + w, y + h], fill=(214, 228, 240))
        d.polygon([(x, y + h), (x + 40, y + 12), (x + w - 40, y + 12), (x + w, y + h)], fill=(150, 170, 190))
        d.pieslice([x + w // 2 - 52, y + 10, x + w // 2 + 52, y + h - 6], 180, 360, fill=(240, 230, 200), outline=NAVY, width=2)
        d.rectangle([x + w // 2 - 12, y + h - 26, x + w // 2 + 12, y + h - 6], fill=RED)
    elif kind == "chart":
        d.rectangle([x, y, x + w, y + h], fill=(232, 238, 245))
        bars = [18, 26, 22, 34, 44]
        for i, bh in enumerate(bars):
            bx = x + 12 + i * ((w - 24) // 5)
            d.rectangle([bx, y + h - 8 - bh, bx + 22, y + h - 8], fill=GREEN if i < 4 else RED)
        d.line([x + 10, y + h - 30, x + w - 10, y + 10], fill=NAVY, width=2)
    elif kind == "virus":
        d.rectangle([x, y, x + w, y + h], fill=(245, 220, 220))
        cx, cy, r = x + w // 2, y + h // 2, 16
        for ang in range(0, 360, 45):
            import math
            dx, dy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
            d.line([cx + dx * r, cy + dy * r, cx + dx * (r + 9), cy + dy * (r + 9)], fill=RED, width=3)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(255, 255, 255))
    elif kind == "globe":
        d.rectangle([x, y, x + w, y + h], fill=(205, 230, 225))
        d.ellipse([x + w // 2 - 24, y + 4, x + w // 2 + 24, y + h - 4], fill=(120, 190, 220), outline=NAVY, width=2)
        d.arc([x + w // 2 - 24, y + 4, x + w // 2 + 24, y + h - 4], 200, 340, fill=GREEN, width=6)
        d.polygon([(x + w // 2 + 6, y + 12), (x + w // 2 + 20, y + 4), (x + w // 2 + 16, y + 22)], fill=GREEN)
    elif kind == "parliament":
        d.rectangle([x, y, x + w, y + h], fill=(228, 228, 232))
        d.polygon([(x + 20, y + 10), (x + w // 2, y - 2), (x + w - 20, y + 10)], fill=NAVY)
        for i in range(4):
            cx = x + 26 + i * ((w - 52) // 3)
            d.rectangle([cx, y + 14, cx + 8, y + h - 8], fill=NAVY)
        d.rectangle([x + 14, y + h - 10, x + w - 14, y + h - 4], fill=NAVY)
    elif kind == "crash":
        d.rectangle([x, y, x + w, y + h], fill=(220, 224, 232))
        d.polygon([(x + 16, y + h // 2), (x + w - 60, y + h // 2 - 12), (x + w - 40, y + h // 2 + 2),
                   (x + w - 60, y + h // 2 + 14)], fill=SLATE)
        d.polygon([(x + w - 66, y + h // 2 - 8), (x + w - 40, y + h - 14), (x + w - 52, y + h // 2 + 6)], fill=SLATE)
        for cx, cy, r in [(x + w - 34, y + 10, 10), (x + w - 22, y + 18, 13)]:
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(160, 160, 160))
        d.polygon([(x + w - 30, y + h - 16), (x + w - 24, y + h - 28), (x + w - 18, y + h - 16)], fill=(220, 90, 30))
    elif kind == "scales":
        d.rectangle([x, y, x + w, y + h], fill=(236, 230, 214))
        d.line([x + w // 2, y + 8, x + w // 2, y + h - 10], fill=NAVY, width=3)
        d.line([x + w // 2 - 34, y + 14, x + w // 2 + 34, y + 14], fill=NAVY, width=3)
        d.polygon([(x + w // 2 - 44, y + 16), (x + w // 2 - 24, y + 16), (x + w // 2 - 34, y + 34)], fill=NAVY)
        d.polygon([(x + w // 2 + 24, y + 16), (x + w // 2 + 44, y + 16), (x + w // 2 + 34, y + 34)], fill=NAVY)
        d.rectangle([x + w // 2 - 16, y + h - 12, x + w // 2 + 16, y + h - 6], fill=NAVY)

# ---------- panels ----------
# (num, category, colour, headline, dek, caption, pic, region)
PANELS = [
    (1, "EUROPE · UKRAINE WAR", BLUE, "Kerch Bridge Falls Into the Sea",
     "Ukrainian drones drop a road span; 2 killed. Kyiv's bridges hit in reply.",
     "KERCH STRAIT • CRIMEA", "bridge"),
    (2, "MIDDLE EAST", CRIMSON, "Drone Strikes US Radar Base",
     "Bahrain attack intercepted; US answers; 4th tanker burns.",
     "SHEIKH ISA • BAHRAIN", "radar"),
    (3, "ASIA · DIPLOMACY", CRIMSON, "Trump Takes the Quad to Manila",
     "Summit turns to critical minerals; Xi, Putin talks next.",
     "MANILA • PHILIPPINES", "summit"),
    (4, "MIDDLE EAST · GAZA", CRIMSON, "Four Nations Demand Gaza Aid Open",
     "Britain, Australia, Canada, Italy urge crossings open.",
     "GAZA CROSSINGS", "truck"),
    (5, "ASIA · JAPAN", CRIMSON, "Japan Protests Airspace Breach",
     "Russian plane near Fukuoka; Tokyo scrambles fighters.",
     "FUKUOKA • JAPAN", "jet"),
    (6, "EUROPE · MIGRATION", BLUE, "EU Plans Rwanda Return Hubs",
     "Five EU states plan a 2027 pilot of about 100 people.",
     "KIGALI • RWANDA", "map"),
    (7, "ASIA · MONGOLIA", CRIMSON, "Mongolia's President Steps Aside",
     "Khurelsukh quits over graft claims; parliament decides.",
     "ULAANBAATAR", "yurt"),
    (8, "MARKETS · USA", PURPLE, "Nvidia Beats; Dow Drops 849",
     "Revenue $115.8bn beats forecasts; Dow falls a 4th day.",
     "WALL STREET", "chart"),
    (9, "AFRICA · HEALTH", GREEN, "Ebola Cases Pass 11,000",
     "WHO: cases doubled in 3 months; 5,500 dead in Congo.",
     "ITURI • DR CONGO", "virus"),
    (10, "CLIMATE · COP31", TEAL, "COP31 Splits on Fossil Phase-Out",
     "Antalya divides over ending fossil fuels.",
     "ANTALYA • TÜRKIYE", "globe"),
    (11, "EUROPE · SERBIA", BLUE, "Students Lead Serbia's New House",
     "Student-backed bloc takes charge after protests.",
     "BELGRADE", "parliament"),
    (12, "ASIA · RUSSIA", CRIMSON, "Military Plane Crashes in Siberia",
     "An-12 crashes near Kemerovo; all 19 aboard killed.",
     "KEMEROVO • SIBERIA", "crash"),
    (13, "AFRICA · MOZAMBIQUE", GREEN, "Mozambique Tries Mondlane",
     "Opposition leader on trial after disputed vote.",
     "MAPUTO", "scales"),
]

def light(col):
    return tuple(235 + (c - 235) // 4 for c in col)

def draw_panel(x, y, w, h, p, large):
    num, cat, col, head, dek, cap, kind = p
    pic_h = 56 if large else 48
    strip_h = 16 if large else 14
    d.rounded_rectangle([x, y, x + w, y + h], radius=6, fill=(255, 255, 255), outline=NAVY, width=2)
    pic(kind, x + 6, y + 6, w - 12, pic_h)
    sy = y + 6 + pic_h
    d.rectangle([x + 6, sy, x + w - 6, sy + strip_h], fill=light(col))
    d.text((x + 10, sy + 2), cap, font=font(SANSB, 10 if large else 9), fill=NAVY)
    cy = sy + strip_h + 6
    r = 10 if large else 8
    d.ellipse([x + 10, cy, x + 10 + 2 * r, cy + 2 * r], fill=col)
    d.text((x + 10 + r - 3, cy + 2), str(num), font=font(SANSB, 11 if large else 10), fill=(255, 255, 255))
    d.text((x + 14 + 2 * r, cy + 2), cat, font=font(SANSB, 11 if large else 10), fill=col)
    hy = cy + 2 * r + 4
    hf = font(SERIFB, 19 if large else 15)
    hlines = wrap(d, head, hf, w - 20)
    for i, ln in enumerate(hlines[:2]):
        d.text((x + 10, hy + i * (22 if large else 17)), ln, font=hf, fill=INK)
    dy = hy + len(hlines[:2]) * (22 if large else 17) + 2
    df = font(SANS, 12 if large else 10)
    for i, ln in enumerate(wrap(d, dek, df, w - 20)[:2]):
        d.text((x + 10, dy + i * (14 if large else 12)), ln, font=df, fill=(60, 60, 60))

# row 1: 3 large panels
for i, p in enumerate(PANELS[:3]):
    draw_panel(14 + i * 336, 128, 324, 192, p, True)
# rows 2 and 3: 5 small panels each
for row, group in enumerate((PANELS[3:8], PANELS[8:13])):
    for i, p in enumerate(group):
        draw_panel(14 + i * 201, 328 + row * 176, 191, 168, p, False)

# ---------- bottom: map + also list ----------
by = 680
# map panel (left, ~1/3)
mx, mw, mh = 14, 320, 282
d.rounded_rectangle([mx, by, mx + mw, by + mh], radius=6, fill=(255, 255, 255), outline=NAVY, width=2)
d.text((mx + 12, by + 10), "WHERE IT HAPPENED", font=font(SANSB, 16), fill=NAVY)
d.line([mx + 12, by + 34, mx + mw - 12, by + 34], fill=NAVY, width=2)
mapx, mapy, mapw, maph = mx + 10, by + 44, mw - 20, 168
d.rectangle([mapx, mapy, mapx + mapw, mapy + maph], fill=(207, 227, 238))
# simplified continents (cream land on pale sea)
d.polygon([(mapx + 8, mapy + 30), (mapx + 70, mapy + 18), (mapx + 88, mapy + 48), (mapx + 60, mapy + 78),
           (mapx + 30, mapy + 96), (mapx + 12, mapy + 60)], fill=(232, 220, 192))          # N America
d.polygon([(mapx + 52, mapy + 112), (mapx + 78, mapy + 108), (mapx + 86, mapy + 138), (mapx + 70, mapy + 162),
           (mapx + 56, mapy + 146)], fill=(232, 220, 192))                                 # S America
d.polygon([(mapx + 138, mapy + 42), (mapx + 168, mapy + 34), (mapx + 180, mapy + 52), (mapx + 162, mapy + 66),
           (mapx + 142, mapy + 60)], fill=(232, 220, 192))                                 # Europe
d.polygon([(mapx + 142, mapy + 74), (mapx + 178, mapy + 70), (mapx + 192, mapy + 100), (mapx + 182, mapy + 138),
           (mapx + 160, mapy + 150), (mapx + 146, mapy + 112)], fill=(232, 220, 192))      # Africa
d.polygon([(mapx + 184, mapy + 30), (mapx + 280, mapy + 22), (mapx + 292, mapy + 60), (mapx + 268, mapy + 96),
           (mapx + 228, mapy + 92), (mapx + 196, mapy + 64)], fill=(232, 220, 192))        # Asia
d.polygon([(mapx + 252, mapy + 150), (mapx + 282, mapy + 146), (mapx + 288, mapy + 162), (mapx + 262, mapy + 166)],
          fill=(232, 220, 192))                                                           # Australia
PINS = {1: (176, 42), 2: (206, 88), 3: (272, 96), 4: (194, 78), 5: (284, 62), 6: (168, 116),
        7: (246, 40), 8: (48, 44), 9: (164, 128), 10: (186, 64), 11: (148, 60), 12: (236, 32), 13: (176, 146)}
PINCOL = {1: BLUE, 2: CRIMSON, 3: CRIMSON, 4: CRIMSON, 5: CRIMSON, 6: BLUE, 7: CRIMSON, 8: PURPLE,
          9: GREEN, 10: TEAL, 11: BLUE, 12: CRIMSON, 13: GREEN}
for n, (px, py) in PINS.items():
    d.ellipse([mapx + px - 7, mapy + py - 7, mapx + px + 7, mapy + py + 7], fill=PINCOL[n], outline=(255, 255, 255), width=1)
    d.text((mapx + px - 3, mapy + py - 5), str(n), font=font(SANSB, 8), fill=(255, 255, 255))
ly = by + 222
lx_leg = mx + 12
for col, label in [(BLUE, "Europe"), (CRIMSON, "Asia"), (GREEN, "Africa"), (PURPLE, "N. America"), (TEAL, "Climate")]:
    d.ellipse([lx_leg, ly + 2, lx_leg + 10, ly + 12], fill=col)
    lx_leg += 14
    d.text((lx_leg, ly), label, font=font(SANSB, 11), fill=GREY)
    lx_leg += d.textlength(label, font=font(SANSB, 11)) + 12
    if label == "Africa":
        ly += 18
        lx_leg = mx + 12
d.text((mx + 12, by + 258), "Numbers match the panels above.",
       font=font(SANS, 11), fill=GREY)

# also list (right, ~2/3)
lx, lw = 346, 664
d.rounded_rectangle([lx, by, lx + lw, by + mh], radius=6, fill=(255, 255, 255), outline=NAVY, width=2)
d.text((lx + 12, by + 10), "ALSO ON TUESDAY 17 NOVEMBER", font=font(SANSB, 16), fill=NAVY)
d.line([lx + 12, by + 34, lx + lw - 12, by + 34], fill=NAVY, width=2)
ALSO = [
    ("Kyiv:", " Dnipro bridges hit by Russian ballistic missiles."),
    ("Moscow:", " Russia claims it downed 1,441 Ukrainian drones."),
    ("London:", " Britain sanctions 8 firms tied to settlements."),
    ("Prague:", " Train crash injures 46 people."),
    ("Paris:", " France hit by nationwide strikes."),
    ("Warsaw:", " Tusk survives a confidence vote."),
    ("Moldova:", " Airspace shut amid security fears."),
    ("Darwin:", " M6.6 quake strikes off northern Australia."),
    ("Hollywood:", " Robert Pattinson named the next James Bond."),
    ("Paris:", " Gérard Depardieu pleads guilty in court."),
    ("Aden:", " Houthi forces advance on the port city."),
]
col_w = 316
for ci in range(2):
    items = ALSO[ci * 6:(ci + 1) * 6]
    cx = lx + 12 + ci * (col_w + 8)
    yy = by + 48
    for j, (bold, rest) in enumerate(items):
        num = 14 + ci * 6 + j
        d.text((cx, yy), f"{num}.", font=font(SANSB, 12), fill=RED)
        bx = cx + 26
        full = bold + rest
        flines = wrap(d, full, font(SANS, 12), col_w - 26)
        # first line: bold prefix + the rest of that line in regular
        d.text((bx, yy), bold, font=font(SANSB, 12), fill=INK)
        bw = d.textlength(bold, font=font(SANSB, 12))
        d.text((bx + bw + 2, yy), flines[0][len(bold):], font=font(SANS, 12), fill=INK)
        if len(flines) > 1:
            d.text((bx, yy + 15), flines[1], font=font(SANS, 12), fill=INK)
            yy += 32
        else:
            yy += 20
        yy += 6

# ---------- footer ----------
d.text((16, 976), "Every story here happened or was first reported on Tuesday 17 November 2026.",
       font=font(SANS, 13), fill=GREY)
foot_r = "Sources: Reuters, AP, AFP, BBC, Al Jazeera. Original drawings."
d.text((W - 16 - d.textlength(foot_r, font=font(SANS, 13)), 976), foot_r,
       font=font(SANS, 13), fill=GREY)

img.save(OUT, "PNG", optimize=True)
print("wrote", OUT, os.path.getsize(OUT), "bytes")

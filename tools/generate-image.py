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

# ---------- flags (simple, recognisable patterns, drawn from scratch) ----------
def stripes(x, y, w, h, cols):
    n = len(cols)
    for i, c in enumerate(cols):
        d.rectangle([x, y + i * h // n, x + w, y + (i + 1) * h // n], fill=c)

def flag(kind, x, y, w, h):
    """Draw a small but recognisable flag; always with a thin outline."""
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=NAVY, width=1)
    if kind == "us":
        stripes(x + 1, y + 1, w - 2, h - 2, [(178, 34, 34), (255, 255, 255)] * 4)
        d.rectangle([x + 1, y + 1, x + w // 2, y + h // 2], fill=NAVY)
        for r in range(3):
            for c in range(4):
                d.ellipse([x + 5 + c * 9, y + 4 + r * 7, x + 8 + c * 9, y + 7 + r * 7], fill=(255, 255, 255))
    elif kind == "jp":
        d.ellipse([x + w // 2 - h // 4, y + h // 4, x + w // 2 + h // 4, y + 3 * h // 4], fill=(188, 0, 45))
    elif kind == "ukraine":
        stripes(x + 1, y + 1, w - 2, h - 2, [(0, 91, 187), (255, 213, 0)])
    elif kind == "mongolia":
        d.rectangle([x + 1, y + 1, x + w // 3, y + h - 1], fill=(206, 17, 38))
        d.rectangle([x + w // 3, y + 1, x + 2 * w // 3, y + h - 1], fill=(0, 70, 173))
        d.rectangle([x + 2 * w // 3, y + 1, x + w - 1, y + h - 1], fill=(206, 17, 38))
        d.ellipse([x + 5, y + h // 4, x + 13, y + h // 4 + 8], fill=(255, 215, 0))
        d.rectangle([x + 5, y + h // 2, x + 13, y + h - 4], fill=(255, 215, 0))
    elif kind == "serbia":
        stripes(x + 1, y + 1, w - 2, h - 2, [(198, 12, 48), (12, 64, 118), (255, 255, 255)])
    elif kind == "mozambique":
        stripes(x + 1, y + 1, w - 2, h - 2, [(0, 122, 61), (0, 0, 0), (255, 210, 0)])
        d.polygon([(x + 1, y + 1), (x + w // 3, y + h // 2), (x + 1, y + h - 1)], fill=(206, 17, 38))
    elif kind == "philippines":
        d.rectangle([x + 1, y + 1, x + w - 1, y + h // 2], fill=(0, 56, 168))
        d.rectangle([x + 1, y + h // 2, x + w - 1, y + h - 1], fill=(206, 17, 38))
        d.polygon([(x + 1, y + 1), (x + w // 2, y + h // 2), (x + 1, y + h - 1)], fill=(255, 255, 255))
        d.ellipse([x + 6, y + h // 2 - 4, x + 14, y + h // 2 + 4], fill=(255, 215, 0))
    elif kind == "rwanda":
        stripes(x + 1, y + 1, w - 2, h - 2, [(0, 122, 184), (255, 210, 0), (0, 140, 70)])
        d.ellipse([x + w - 16, y + 3, x + w - 6, y + 13], fill=(255, 215, 0))
    elif kind == "congo":
        d.rectangle([x + 1, y + 1, x + w - 1, y + h - 1], fill=(0, 127, 214))
        d.polygon([(x + 1, y + h - 1), (x + w - 1, y + 1), (x + w - 1, y + h // 3), (x + w // 3, y + h - 1)], fill=(206, 17, 38))
        d.ellipse([x + 6, y + 4, x + 14, y + 12], fill=(255, 215, 0))
    elif kind == "turkiye":
        d.rectangle([x + 1, y + 1, x + w - 1, y + h - 1], fill=(227, 10, 23))
        d.ellipse([x + w // 4, y + h // 4, x + w // 4 + h // 2, y + 3 * h // 4], fill=(255, 255, 255))
        d.ellipse([x + w // 4 + 5, y + h // 4 + 2, x + w // 4 + h // 2, y + 3 * h // 4 - 2], fill=(227, 10, 23))
        d.ellipse([x + w // 2 + 2, y + h // 2 - 3, x + w // 2 + 8, y + h // 2 + 3], fill=(255, 255, 255))
    elif kind == "india":
        stripes(x + 1, y + 1, w - 2, h - 2, [(255, 153, 51), (255, 255, 255), (19, 136, 8)])
        d.ellipse([x + w // 2 - 6, y + h // 2 - 6, x + w // 2 + 6, y + h // 2 + 6], outline=NAVY, width=2)
    elif kind == "australia":
        d.rectangle([x + 1, y + 1, x + w - 1, y + h - 1], fill=(0, 0, 139))
        d.rectangle([x + 1, y + 1, x + w // 2, y + h // 2], fill=(255, 255, 255))
        d.line([x + 1, y + 1, x + w // 2, y + h // 2], fill=(200, 0, 0), width=2)
        d.line([x + w // 2, y + 1, x + 1, y + h // 2], fill=(200, 0, 0), width=2)
        d.ellipse([x + w - 12, y + h - 12, x + w - 6, y + h - 6], fill=(255, 255, 255))
    elif kind == "uk":
        d.rectangle([x + 1, y + 1, x + w - 1, y + h - 1], fill=(0, 36, 125))
        d.rectangle([x + w // 2 - 3, y + 1, x + w // 2 + 3, y + h - 1], fill=(255, 255, 255))
        d.rectangle([x + 1, y + h // 2 - 3, x + w - 1, y + h // 2 + 3], fill=(255, 255, 255))
        d.rectangle([x + w // 2 - 1, y + 1, x + w // 2 + 1, y + h - 1], fill=(200, 16, 46))
        d.rectangle([x + 1, y + h // 2 - 1, x + w - 1, y + h // 2 + 1], fill=(200, 16, 46))
    elif kind == "canada":
        d.rectangle([x + 1, y + 1, x + w // 4, y + h - 1], fill=(255, 0, 0))
        d.rectangle([x + 3 * w // 4, y + 1, x + w - 1, y + h - 1], fill=(255, 0, 0))
        d.polygon([(x + w // 2, y + 4), (x + w // 2 + 6, y + h // 2), (x + w // 2 + 3, y + h - 4),
                   (x + w // 2 - 3, y + h - 4), (x + w // 2 - 6, y + h // 2)], fill=(255, 0, 0))
    elif kind == "italy":
        d.rectangle([x + 1, y + 1, x + w // 3, y + h - 1], fill=(0, 140, 70))
        d.rectangle([x + 2 * w // 3, y + 1, x + w - 1, y + h - 1], fill=(206, 17, 38))
    elif kind == "bahrain":
        d.rectangle([x + w // 3, y + 1, x + w - 1, y + h - 1], fill=(206, 17, 38))
        for i in range(5):
            yy = y + 1 + i * (h - 2) // 5
            d.polygon([(x + w // 3, yy), (x + w // 3 - 6, yy + (h - 2) // 10), (x + w // 3, yy + (h - 2) // 5)], fill=(206, 17, 38))
    elif kind == "russia":
        stripes(x + 1, y + 1, w - 2, h - 2, [(255, 255, 255), (0, 57, 166), (213, 0, 50)])

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
d.rectangle([5, 5, W - 6, H - 6], outline=NAVY, width=2)

# ---------- header ----------
d.text((16, 14), "THE WORLD'S NEWS IN ONE PICTURE", font=font(SANSB, 15), fill=RED)
right = "13 STORIES  ·  6 CONTINENTS  ·  ALL FROM TUESDAY"
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
        flag("ukraine", x + 8, y + 6, 54, 30)
    elif kind == "radar":
        d.rectangle([x, y, x + w, y + h], fill=(232, 213, 163))
        d.pieslice([x + w // 2 - 34, y + 4, x + w // 2 + 34, y + 72], 180, 360,
                   fill=(255, 255, 255), outline=NAVY, width=2)
        d.line([x + w // 2, y + 38, x + w // 2 + 28, y + 14], fill=RED, width=3)
        d.rectangle([x + 10, y + h - 18, x + 76, y + h - 8], fill=(120, 60, 40))
        d.polygon([(x + 22, y + h - 18), (x + 64, y + h - 18), (x + 54, y + h - 32), (x + 32, y + h - 32)],
                  fill=(90, 90, 90))
        d.polygon([(x + 40, y + h - 34), (x + 46, y + h - 44), (x + 52, y + h - 34)], fill=(220, 60, 30))
        flag("bahrain", x + 8, y + 6, 46, 26)
        flag("us", x + w - 56, y + 6, 48, 28)
    elif kind == "summit":
        d.rectangle([x, y, x + w, y + h], fill=(198, 222, 240))
        fw = (w - 32) // 4
        for i, (fk, lab) in enumerate([("us", "USA"), ("india", "INDIA"), ("jp", "JAPAN"), ("australia", "AUSTRALIA")]):
            fx = x + 8 + i * (fw + 4)
            flag(fk, fx, y + 6, fw, 36)
            d.text((fx, y + 44), lab, font=font(SANSB, 8), fill=NAVY)
    elif kind == "truck":
        d.rectangle([x, y, x + w, y + h], fill=(240, 228, 200))
        fw = (w - 20) // 4
        for i, fk in enumerate(["uk", "australia", "canada", "italy"]):
            flag(fk, x + 6 + i * (fw + 3), y + 4, fw, 20)
        d.rectangle([x + 56, y + 28, x + w - 66, y + h - 12], fill=(255, 255, 255), outline=NAVY, width=2)
        d.rectangle([x + w - 56, y + 32, x + w - 12, y + h - 12], fill=RED)
        d.ellipse([x + 72, y + h - 18, x + 94, y + h - 2], fill=(30, 30, 30))
        d.ellipse([x + w - 52, y + h - 18, x + w - 30, y + h - 2], fill=(30, 30, 30))
        d.text((x + 10, y + 28), "AID", font=font(SANSB, 16), fill=RED)
    elif kind == "jet":
        d.rectangle([x, y, x + w, y + h], fill=(207, 232, 245))
        flag("jp", x + w - 66, y + 4, 58, 34)
        d.polygon([(x + 14, y + h // 2 - 4), (x + w - 70, y + h // 2 - 10), (x + w - 56, y + h // 2),
                   (x + w - 70, y + h // 2 + 10), (x + 14, y + h // 2 + 4)], fill=NAVY)
        d.polygon([(x + 60, y + h // 2 - 8), (x + 92, y + 4), (x + 102, y + h // 2 - 8)], fill=NAVY)
    elif kind == "map":
        d.rectangle([x, y, x + w, y + h], fill=(210, 235, 205))
        flag("rwanda", x + 8, y + 6, 56, 32)
        d.polygon([(x + w // 2 - 18, y + 6), (x + w // 2 + 34, y + 6), (x + w // 2 + 52, y + 24),
                   (x + w // 2 + 40, y + h - 8), (x + w // 2 - 6, y + h - 12), (x + w // 2 - 24, y + 22)],
                  fill=(90, 160, 90), outline=(40, 100, 40))
        d.ellipse([x + w // 2 - 6, y + 12, x + w // 2 + 10, y + 28], fill=RED)
        d.polygon([(x + w // 2 + 2, y + 28), (x + w // 2 - 3, y + 38), (x + w // 2 + 7, y + 38)], fill=RED)
    elif kind == "yurt":
        d.rectangle([x, y, x + w, y + h], fill=(214, 228, 240))
        flag("mongolia", x + 8, y + 6, 56, 32)
        d.pieslice([x + w // 2 - 52, y + 10, x + w // 2 + 52, y + h - 6], 180, 360, fill=(240, 230, 200), outline=NAVY, width=2)
        d.rectangle([x + w // 2 - 12, y + h - 26, x + w // 2 + 12, y + h - 6], fill=RED)
    elif kind == "chart":
        d.rectangle([x, y, x + w, y + h], fill=(232, 238, 245))
        flag("us", x + w - 58, y + 4, 50, 28)
        bars = [18, 26, 22, 34, 44]
        for i, bh in enumerate(bars):
            bx = x + 12 + i * ((w - 24) // 5)
            d.rectangle([bx, y + h - 8 - bh, bx + 22, y + h - 8], fill=GREEN if i < 4 else RED)
        d.line([x + 10, y + h - 30, x + w - 10, y + 10], fill=NAVY, width=2)
    elif kind == "virus":
        d.rectangle([x, y, x + w, y + h], fill=(245, 220, 220))
        flag("congo", x + 8, y + 6, 56, 32)
        cx, cy, r = x + w - 34, y + h // 2, 14
        for ang in range(0, 360, 45):
            import math
            dx, dy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
            d.line([cx + dx * r, cy + dy * r, cx + dx * (r + 8), cy + dy * (r + 8)], fill=RED, width=3)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 255, 255))
    elif kind == "globe":
        d.rectangle([x, y, x + w, y + h], fill=(205, 230, 225))
        flag("turkiye", x + 8, y + 6, 56, 32)
        d.ellipse([x + w - 48, y + 4, x + w - 4, y + h - 4], fill=(120, 190, 220), outline=NAVY, width=2)
        d.arc([x + w - 48, y + 4, x + w - 4, y + h - 4], 200, 340, fill=GREEN, width=6)
    elif kind == "parliament":
        d.rectangle([x, y, x + w, y + h], fill=(228, 228, 232))
        flag("serbia", x + 8, y + 6, 56, 32)
        d.polygon([(x + 70, y + 10), (x + w // 2 + 20, y - 2), (x + w - 14, y + 10)], fill=NAVY)
        for i in range(3):
            cx = x + 76 + i * 28
            d.rectangle([cx, y + 14, cx + 8, y + h - 8], fill=NAVY)
        d.rectangle([x + 70, y + h - 10, x + w - 14, y + h - 4], fill=NAVY)
    elif kind == "crash":
        d.rectangle([x, y, x + w, y + h], fill=(220, 224, 232))
        flag("russia", x + 8, y + 6, 56, 32)
        d.polygon([(x + 16, y + h // 2), (x + w - 60, y + h // 2 - 12), (x + w - 40, y + h // 2 + 2),
                   (x + w - 60, y + h // 2 + 14)], fill=SLATE)
        d.polygon([(x + w - 66, y + h // 2 - 8), (x + w - 40, y + h - 14), (x + w - 52, y + h // 2 + 6)], fill=SLATE)
        for cx, cy, r in [(x + w - 34, y + 10, 10), (x + w - 22, y + 18, 13)]:
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(160, 160, 160))
        d.polygon([(x + w - 30, y + h - 16), (x + w - 24, y + h - 28), (x + w - 18, y + h - 16)], fill=(220, 90, 30))
    elif kind == "scales":
        d.rectangle([x, y, x + w, y + h], fill=(236, 230, 214))
        flag("mozambique", x + 8, y + 6, 56, 32)
        d.line([x + w - 44, y + 8, x + w - 44, y + h - 10], fill=NAVY, width=3)
        d.line([x + w - 72, y + 14, x + w - 16, y + 14], fill=NAVY, width=3)
        d.polygon([(x + w - 80, y + 16), (x + w - 62, y + 16), (x + w - 71, y + 32)], fill=NAVY)
        d.polygon([(x + w - 26, y + 16), (x + w - 8, y + 16), (x + w - 17, y + 32)], fill=NAVY)
        d.rectangle([x + w - 58, y + h - 12, x + w - 30, y + h - 6], fill=NAVY)

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
# map panel (left, wider now so the world map can actually be read)
mx, mw, mh = 14, 380, 282
d.rounded_rectangle([mx, by, mx + mw, by + mh], radius=6, fill=(255, 255, 255), outline=NAVY, width=2)
d.text((mx + 12, by + 10), "WHERE IT HAPPENED", font=font(SANSB, 16), fill=NAVY)
d.line([mx + 12, by + 34, mx + mw - 12, by + 34], fill=NAVY, width=2)
mapx, mapy, mapw, maph = mx + 10, by + 44, mw - 20, 190
d.rectangle([mapx, mapy, mapx + mapw, mapy + maph], fill=(198, 222, 235))
# equirectangular projection: lon -170..190, lat 75..-55
def ll(lon, lat):
    return (mapx + (lon + 170) / 360 * mapw, mapy + (75 - lat) / 130 * maph)
def land(poly, label=None, lab_lon=None, lab_lat=None):
    pts = [ll(lo, la) for lo, la in poly]
    d.polygon(pts, fill=(233, 214, 168), outline=(110, 88, 55), width=1)
    if label:
        lx_, ly_ = ll(lab_lon, lab_lat)
        f = font(SANSB, 9)
        d.text((lx_ - d.textlength(label, font=f) / 2, ly_ - 5), label, font=f, fill=(90, 78, 55))
# light graticule
for lo in range(-150, 181, 30):
    x0, _ = ll(lo, 0)
    d.line([x0, mapy, x0, mapy + maph], fill=(180, 205, 220), width=1)
for la in (60, 30, 0, -30):
    _, y0 = ll(0, la)
    d.line([mapx, y0, mapx + mapw, y0], fill=(180, 205, 220), width=1)
LAND = [
    ([(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-65, 60), (-55, 47), (-70, 42), (-75, 35), (-80, 26), (-90, 21), (-97, 16), (-92, 14), (-83, 9), (-79, 9), (-83, 15), (-90, 14), (-97, 26), (-105, 20), (-110, 24), (-120, 34), (-125, 40), (-125, 49), (-130, 55), (-140, 60), (-155, 58), (-165, 60)], "N. AMERICA", -100, 58),
    ([(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18), (-70, -23), (-70, -30), (-72, -37), (-73, -44), (-70, -50), (-68, -55), (-65, -55), (-62, -48), (-58, -38), (-52, -32), (-48, -28), (-41, -23), (-35, -9), (-35, -6), (-44, -3), (-50, 0), (-53, 4), (-58, 6), (-62, 9), (-70, 11), (-75, 10)], "S. AMERICA", -60, -14),
    ([(-10, 36), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (-1, 50), (2, 51), (5, 53), (8, 57), (10, 59), (5, 60), (5, 62), (12, 65), (18, 69), (25, 71), (30, 70), (35, 68), (40, 68), (45, 65), (48, 60), (45, 55), (40, 50), (38, 46), (32, 46), (28, 45), (23, 40), (26, 38), (23, 36), (19, 40), (15, 44), (12, 44), (8, 44), (3, 42), (-9, 37)], "EUROPE", -15, 45),
    ([(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53)], None, None, None),
    ([(-17, 15), (-16, 20), (-13, 27), (-10, 31), (-6, 35), (0, 36), (10, 37), (11, 34), (20, 32), (25, 32), (30, 31), (32, 31), (35, 28), (37, 22), (39, 18), (43, 12), (48, 11), (51, 10), (46, 5), (41, 0), (40, -5), (40, -10), (36, -18), (33, -26), (28, -33), (20, -35), (17, -32), (15, -27), (12, -18), (13, -12), (9, -1), (9, 4), (-8, 4), (-13, 8), (-17, 12)], "AFRICA", -25, 0),
    ([(44, -16), (47, -15), (50, -16), (49, -20), (45, -25), (43, -22)], None, None, None),
    ([(30, 70), (40, 68), (50, 69), (60, 69), (70, 72), (80, 73), (90, 75), (100, 77), (110, 74), (120, 73), (130, 72), (140, 72), (150, 70), (160, 69), (170, 67), (178, 65), (170, 60), (162, 56), (158, 52), (150, 59), (142, 54), (140, 48), (135, 43), (130, 42), (127, 40), (122, 38), (120, 32), (122, 28), (118, 25), (110, 21), (108, 18), (105, 10), (103, 8), (100, 7), (98, 12), (95, 16), (92, 21), (88, 22), (85, 19), (80, 15), (77, 8), (75, 12), (72, 20), (68, 23), (66, 25), (62, 25), (58, 26), (56, 27), (52, 26), (50, 29), (48, 30), (44, 29), (42, 27), (40, 24), (38, 22), (35, 28), (34, 31), (36, 36), (30, 36), (27, 38), (28, 41), (30, 45), (28, 46), (30, 48), (30, 60)], "ASIA", 95, 70),
    ([(130, 31), (133, 33), (136, 34), (139, 35), (141, 38), (142, 41), (144, 44), (142, 44), (140, 40), (137, 35), (133, 32)], None, None, None),
    ([(114, -22), (114, -30), (115, -35), (120, -34), (124, -33), (129, -32), (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27), (150, -23), (146, -19), (142, -15), (142, -11), (137, -12), (135, -15), (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)], "AUSTRALIA", 134, -28),
]
for poly, lab, llo, lla in LAND:
    land(poly, lab, llo, lla)
# numbered pins: (lon, lat, label dx, label dy) — clustered pins get a
# leader line from their true spot to a spread-out numbered circle
PINS = {1: (37, 45, 0, -34), 2: (50.5, 26, 40, -6), 3: (121, 14.5, 0, 0),
        4: (34.5, 31.5, 38, 22), 5: (130.5, 33.6, 0, 0), 6: (30, -2, -28, 20),
        7: (107, 48, 26, -20), 8: (-74, 41, 0, 0), 9: (29.5, 1.5, -30, -14),
        10: (30.7, 36.9, -40, 8), 11: (20.5, 44.8, -38, -22),
        12: (86, 55.3, -30, 18), 13: (32.6, -26, 0, 0)}
PINCOL = {1: BLUE, 2: CRIMSON, 3: CRIMSON, 4: CRIMSON, 5: CRIMSON, 6: BLUE, 7: CRIMSON, 8: PURPLE,
          9: GREEN, 10: TEAL, 11: BLUE, 12: CRIMSON, 13: GREEN}
for n, (lo, la, dx, dy) in PINS.items():
    px, py = ll(lo, la)
    cx, cy = px + dx, py + dy
    if dx or dy:
        d.line([px, py, cx, cy], fill=NAVY, width=1)
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=PINCOL[n], outline=(255, 255, 255), width=1)
    d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=PINCOL[n], outline=(255, 255, 255), width=2)
    nf = font(SANSB, 11)
    d.text((cx - d.textlength(str(n), font=nf) / 2, cy - 8), str(n), font=nf, fill=(255, 255, 255))
ly = by + 238
lx_leg = mx + 12
for col, label in [(BLUE, "Europe"), (CRIMSON, "Asia"), (GREEN, "Africa"), (PURPLE, "N. America"), (TEAL, "Climate")]:
    d.ellipse([lx_leg, ly + 2, lx_leg + 10, ly + 12], fill=col)
    lx_leg += 14
    d.text((lx_leg, ly), label, font=font(SANSB, 11), fill=GREY)
    lx_leg += d.textlength(label, font=font(SANSB, 11)) + 12
    if label == "Africa":
        ly += 16
        lx_leg = mx + 12

# also list (right)
lx, lw = 406, 604
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
col_w = 286
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

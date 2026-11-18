#!/usr/bin/env python3
"""Draw the 17 November 2026 front page (1024x1024) with Pillow only.

Newspaper front-page template, in my own words and drawings:
masthead, giant serif date, 13 story panels in 3 rows, a world map
with numbered pins, and an "also on Tuesday" list. No photos, no
downloaded art, no copied text. Run: python3 tools/generate-image.py
"""
from PIL import Image, ImageDraw, ImageFont
import math
import os
import random

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

# ---------- realism helpers (all deterministic, no photos) ----------
def _lerp(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

def _blend(c, bg, t):
    """Blend colour c toward bg by t (0 = c, 1 = bg)."""
    return tuple(int(c[i] + (bg[i] - c[i]) * t) for i in range(3))

def vgrad(x, y, w, h, c1, c2):
    """Vertical gradient, top c1 -> bottom c2, drawn as 1px lines."""
    if h <= 1:
        d.rectangle([x, y, x + w, y + h], fill=c1)
        return
    for i in range(h):
        d.line([(x, y + i), (x + w, y + i)], fill=_lerp(c1, c2, i / (h - 1)))

def hgrad(x, y, w, h, c1, c2):
    if w <= 1:
        d.rectangle([x, y, x + w, y + h], fill=c1)
        return
    for i in range(w):
        d.line([(x + i, y), (x + i, y + h)], fill=_lerp(c1, c2, i / (w - 1)))

def soft_disc(cx, cy, rx, ry, colour, bg, steps=6):
    """A soft-edged disc: concentric ellipses fading into bg (smoke, glow)."""
    for i in range(steps, 0, -1):
        t = i / steps
        col = _blend(colour, bg, 1 - t * 0.85)
        d.ellipse([cx - rx * t, cy - ry * t, cx + rx * t, cy + ry * t], fill=col)

def sun_glow(cx, cy, r, sky):
    """Pale halo rings around a sun disc."""
    for i in range(4, 0, -1):
        col = _blend((255, 214, 130), sky, 1 - i / 4 * 0.75)
        d.ellipse([cx - r * i, cy - r * i, cx + r * i, cy + r * i], fill=col)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 226, 150))

def cloud(cx, cy, s, sky):
    """A small soft cloud: overlapping pale discs."""
    for dx, dy, r in [(-s, 2, s // 2), (0, -2, s // 2 + 2), (s, 2, s // 2)]:
        soft_disc(cx + dx, cy + dy, r, r // 2 + 2, (255, 255, 255), sky, steps=4)

def fold_shade(x, y, w, h, period=9, amp=0.16):
    """Cloth folds on a flag: darken/lighten vertical bands with a sine wave.

    Works on the pixels already drawn, so it shades any flag pattern.
    """
    px = img.load()
    for xx in range(max(0, x), min(W, x + w)):
        f = 1.0 + amp * math.sin(2 * math.pi * (xx - x) / period)
        for yy in range(max(0, y), min(H, y + h)):
            r, g, b = px[xx, yy]
            px[xx, yy] = (max(0, min(255, int(r * f))),
                          max(0, min(255, int(g * f))),
                          max(0, min(255, int(b * f))))

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
    # cloth folds: shade the finished flag so it reads as fabric, not a sticker
    fold_shade(x + 1, y + 1, w - 2, h - 2)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
# paper with a faint warm gradient, top lighter than the bottom edge
vgrad(0, 0, W, H, (248, 243, 226), (236, 227, 203))
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
        # dusk sky, sea below, low sun glow on the horizon
        sky = (250, 214, 170)
        vgrad(x, y, w, h - 22, (244, 190, 140), (214, 228, 238))
        sun_glow(x + w - 52, y + 12, 6, sky)
        cloud(x + 58, y + 10, 12, sky)
        cloud(x + w // 2 + 10, y + 6, 9, sky)
        # sea with a gradient, a sunlit path, and layered wave lines
        vgrad(x, y + h - 22, w, 22, (46, 140, 150), (16, 84, 104))
        d.rectangle([x + w - 72, y + h - 22, x + w - 32, y + h], fill=(120, 180, 180))
        for wy in (y + h - 16, y + h - 9, y + h - 4):
            for wx in range(x + 6, x + w - 12, 26):
                d.arc([wx, wy - 3, wx + 14, wy + 3], 180, 360, fill=(190, 225, 230), width=1)
        # bridge spans: steel with a top highlight, shadowed underside, pillars
        for bx0, bx1 in [(x, x + w // 3), (x + 2 * w // 3, x + w)]:
            d.rectangle([bx0, y + h - 48, bx1, y + h - 40], fill=(58, 58, 62))
            d.line([(bx0, y + h - 48), (bx1, y + h - 48)], fill=(150, 150, 155), width=2)
            d.line([(bx0, y + h - 41), (bx1, y + h - 41)], fill=(30, 30, 34), width=2)
            for px0 in (bx0 + 18, bx0 + (bx1 - bx0) // 2, bx1 - 24):
                d.rectangle([px0, y + h - 40, px0 + 6, y + h - 22], fill=(44, 44, 48))
                d.rectangle([px0, y + h - 26, px0 + 10, y + h - 22], fill=(30, 30, 34))
        # two small jets in the sky
        for jx, jy in [(x + w // 2 - 66, y + 12), (x + w // 2 + 52, y + 6)]:
            d.polygon([(jx, jy), (jx + 12, jy + 2), (jx, jy + 4)], fill=(30, 30, 36))
            d.polygon([(jx + 4, jy), (jx + 8, jy - 4), (jx + 10, jy + 1)], fill=(30, 30, 36))
        # fallen span, tilted into the water, with foam and a dark shadow
        d.polygon([(x + w // 3 + 6, y + h - 46), (x + 2 * w // 3 - 4, y + h - 30),
                   (x + 2 * w // 3 - 16, y + h - 18), (x + w // 3 + 14, y + h - 30)], fill=(74, 74, 80))
        d.line([(x + w // 3 + 8, y + h - 45), (x + 2 * w // 3 - 6, y + h - 30)], fill=(140, 140, 146), width=2)
        d.ellipse([x + w // 2 - 26, y + h - 20, x + w // 2 + 26, y + h - 8], fill=(16, 84, 104))
        for fx, fy, fr in [(x + w // 2 - 18, y + h - 12, 5), (x + w // 2 + 4, y + h - 9, 6),
                            (x + w // 2 + 18, y + h - 13, 4)]:
            d.arc([fx - fr, fy - fr, fx + fr, fy + fr], 180, 360, fill=(230, 245, 245), width=2)
        # layered smoke plumes over the break
        soft_disc(x + w // 2 - 8, y + 14, 16, 10, (90, 90, 95), sky, steps=5)
        soft_disc(x + w // 2 + 12, y + 8, 12, 8, (120, 120, 125), sky, steps=5)
        soft_disc(x + w // 2 + 2, y + 20, 9, 6, (60, 60, 65), sky, steps=4)
        flag("ukraine", x + 8, y + 6, 54, 30)
    elif kind == "radar":
        # a real map of the Gulf, like the reference: cream land, blue sea,
        # coastline, place names, and boxed callouts at the right spots
        vgrad(x, y, w, h, (168, 208, 232), (140, 188, 220))
        # Iran: big landmass across the top; Arabia: landmass bottom-left
        d.polygon([(x, y), (x + w, y), (x + w, y + 20), (x + w - 40, y + 26),
                   (x + w - 90, y + 18), (x + w - 150, y + 26), (x + w - 210, y + 16),
                   (x + w - 260, y + 24), (x, y + 22)],
                  fill=(238, 226, 190), outline=(150, 128, 88))
        d.polygon([(x, y + h), (x, y + 34), (x + 70, y + 40), (x + 110, y + 34),
                   (x + 130, y + 44), (x + 100, y + h)],
                  fill=(238, 226, 190), outline=(150, 128, 88))
        # Qeshm island in the strait, and a small tanker in the sea
        d.ellipse([x + w - 96, y + 30, x + w - 62, y + 38], fill=(238, 226, 190),
                  outline=(150, 128, 88))
        d.rectangle([x + w - 52, y + h - 18, x + w - 22, y + h - 10], fill=(120, 60, 40))
        d.rectangle([x + w - 52, y + h - 24, x + w - 38, y + h - 18], fill=(90, 90, 95))
        d.line([(x + w - 52, y + h - 18), (x + w - 22, y + h - 18)], fill=(255, 255, 255), width=1)
        # gentle wave lines on the sea
        for wy in (y + 34, y + 44, y + h - 8):
            for wx in range(x + 120, x + w - 30, 24):
                d.arc([wx, wy - 2, wx + 12, wy + 2], 180, 360, fill=(200, 228, 240), width=1)
        # place names on the map
        d.text((x + 108, y + 6), "IRAN", font=font(SANSB, 10), fill=(90, 70, 40))
        d.text((x + 16, y + 38), "BAHRAIN", font=font(SANSB, 8), fill=(90, 70, 40))
        d.text((x + w - 92, y + 40), "QESHM", font=font(SANSB, 8), fill=(90, 70, 40))
        # boxed callouts: red where drones were downed, blue where the US struck
        d.rectangle([x + 88, y + 24, x + 184, y + 36], fill=(200, 30, 30))
        d.text((x + 93, y + 26), "DRONES DOWNED", font=font(SANSB, 8), fill=(255, 255, 255))
        d.rectangle([x + w - 128, y + 8, x + w - 58, y + 20], fill=(30, 80, 170))
        d.text((x + w - 123, y + 10), "US STRIKES", font=font(SANSB, 8), fill=(255, 255, 255))
        # small drone silhouettes over the strait
        for jx, jy in [(x + 150, y + 42), (x + 168, y + 46)]:
            d.polygon([(jx, jy), (jx + 10, jy + 2), (jx, jy + 3)], fill=(40, 40, 44))
            d.ellipse([jx - 2, jy - 2, jx + 2, jy + 2], fill=(40, 40, 44))
    elif kind == "summit":
        # a meeting room, like the reference: pale wall, a purple banner
        # on top, four flags standing on a brown conference table
        vgrad(x, y, w, h, (232, 226, 240), (214, 206, 226))
        banner = "QUAD LEADERS' SUMMIT · MANILA"
        bf = font(SANSB, 10)
        d.rectangle([x, y, x + w, y + 15], fill=(106, 74, 158))
        d.text(((x + x + w - d.textlength(banner, font=bf)) / 2, y + 2), banner, font=bf,
               fill=(255, 255, 255))
        # brown table along the very bottom, with a polished top edge
        d.rectangle([x, y + h - 6, x + w, y + h], fill=(122, 82, 52))
        d.rectangle([x, y + h - 6, x + w, y + h - 3], fill=(168, 122, 84))
        fw = (w - 32) // 4
        for i, (fk, lab) in enumerate([("us", "USA"), ("india", "INDIA"), ("jp", "JAPAN"), ("australia", "AUSTRALIA")]):
            fx = x + 8 + i * (fw + 4)
            # a thin pole and a soft shadow where the flag meets the table
            d.line([(fx + fw // 2, y + 17), (fx + fw // 2, y + h - 6)], fill=(90, 70, 50), width=1)
            flag(fk, fx, y + 18, fw, 22)
            d.text((fx, y + 41), lab, font=font(SANSB, 8), fill=NAVY)
    elif kind == "truck":
        # dusty road at golden hour: warm sky, hazy hills, shaded asphalt
        vgrad(x, y, w, h, (242, 226, 188), (224, 200, 150))
        d.polygon([(x, y + 26), (x + w // 3, y + 18), (x + 2 * w // 3, y + 24), (x + w, y + 20),
                   (x + w, y + 28), (x, y + 28)], fill=(206, 178, 128))
        # distant tents and a damaged building on the horizon
        for tx in (x + 12, x + 132):
            d.polygon([(tx, y + 28), (tx + 10, y + 18), (tx + 20, y + 28)], fill=(236, 228, 208))
            d.line([(tx + 10, y + 18), (tx + 10, y + 28)], fill=(180, 170, 150), width=1)
        d.rectangle([x + w - 34, y + 14, x + w - 8, y + 28], fill=(170, 150, 120))
        d.rectangle([x + w - 30, y + 18, x + w - 24, y + 23], fill=(60, 55, 50))
        d.rectangle([x, y + 28, x + w, y + h], fill=(120, 108, 92))
        d.rectangle([x, y + 28, x + w, y + 31], fill=(150, 138, 118))
        for wx in range(x + 8, x + w, 22):
            d.line([(wx, y + h - 5), (wx + 10, y + h - 5)], fill=(230, 220, 190), width=2)
        fw = (w - 20) // 4
        for i, fk in enumerate(["uk", "australia", "canada", "italy"]):
            flag(fk, x + 6 + i * (fw + 3), y + 4, fw, 20)
        # truck: white cargo box with a top highlight, red cab, cast shadow
        d.ellipse([x + 50, y + h - 10, x + w - 8, y + h - 4], fill=(92, 82, 68))
        d.rectangle([x + 56, y + 28, x + w - 66, y + h - 12], fill=(252, 252, 248), outline=NAVY, width=2)
        d.rectangle([x + 56, y + 28, x + w - 66, y + 32], fill=(210, 210, 200))
        d.rectangle([x + w - 56, y + 32, x + w - 12, y + h - 12], fill=(178, 44, 40))
        d.rectangle([x + w - 56, y + 32, x + w - 12, y + 36], fill=(220, 90, 80))
        d.rectangle([x + w - 52, y + 34, x + w - 34, y + 42], fill=(198, 222, 240), outline=NAVY, width=1)
        for wxx, wyy in [(x + 72, y + h - 18), (x + w - 52, y + h - 18)]:
            d.ellipse([wxx, wyy, wxx + 22, wyy + 16], fill=(28, 28, 30))
            d.ellipse([wxx + 7, wyy + 5, wxx + 15, wyy + 11], fill=(160, 160, 165))
        d.text((x + 10, y + 28), "AID", font=font(SANSB, 16), fill=RED)
    elif kind == "jet":
        # morning sky gradient, soft clouds, a sun disc behind the flag
        sky3 = (205, 230, 244)
        vgrad(x, y, w, h, (196, 224, 242), (228, 240, 248))
        cloud(x + 30, y + 10, 10, sky3)
        cloud(x + 78, y + 34, 8, sky3)
        cloud(x + w - 30, y + h - 10, 9, sky3)
        # sea far below, with a coastline and wave lines
        vgrad(x, y + h - 12, w, 12, (90, 160, 190), (60, 130, 170))
        d.line([(x, y + h - 12), (x + w, y + h - 12)], fill=(240, 240, 230), width=1)
        for wx in range(x + 8, x + w - 8, 20):
            d.arc([wx, y + h - 9, wx + 10, y + h - 5], 180, 360, fill=(210, 235, 245), width=1)
        sun_glow(x + w - 38, y + 21, 7, sky3)
        flag("jp", x + w - 66, y + 4, 58, 34)
        # jet with a pale top highlight, darker belly, and a fading contrail
        d.line([(x + 6, y + h // 2 + 2), (x + 34, y + h // 2 + 2)], fill=(230, 235, 240), width=2)
        d.polygon([(x + 14, y + h // 2 - 4), (x + w - 70, y + h // 2 - 10), (x + w - 56, y + h // 2),
                   (x + w - 70, y + h // 2 + 10), (x + 14, y + h // 2 + 4)], fill=NAVY)
        d.polygon([(x + 16, y + h // 2 - 4), (x + w - 72, y + h // 2 - 9), (x + w - 62, y + h // 2 - 6)],
                  fill=(70, 90, 120))
        d.polygon([(x + w - 70, y + h // 2 + 4), (x + w - 58, y + h // 2 + 9), (x + w - 70, y + h // 2 + 10)],
                  fill=(12, 22, 42))
        d.polygon([(x + 60, y + h // 2 - 8), (x + 92, y + 4), (x + 102, y + h // 2 - 8)], fill=NAVY)
        d.ellipse([x + w - 62, y + h // 2 - 4, x + w - 54, y + h // 2 + 4], fill=(255, 214, 130))
    elif kind == "map":
        # green hill country: layered hills, a lake, and the map pin on top
        vgrad(x, y, w, h, (206, 232, 200), (168, 205, 160))
        d.polygon([(x, y + 30), (x + w // 3, y + 18), (x + 2 * w // 3, y + 26), (x + w, y + 20),
                   (x + w, y + h), (x, y + h)], fill=(140, 190, 130))
        d.polygon([(x, y + 38), (x + w // 2, y + 28), (x + w, y + 36), (x + w, y + h), (x, y + h)],
                  fill=(110, 170, 105))
        d.ellipse([x + 14, y + h - 14, x + 62, y + h - 4], fill=(120, 185, 215))
        d.arc([x + 14, y + h - 14, x + 62, y + h - 4], 180, 360, fill=(220, 240, 250), width=1)
        for tx, ty in [(x + 76, y + 30), (x + 150, y + 34)]:
            d.polygon([(tx, ty), (tx + 4, ty - 8), (tx + 8, ty)], fill=(40, 110, 60))
        flag("rwanda", x + 8, y + 6, 56, 32)
        d.polygon([(x + w // 2 - 18, y + 6), (x + w // 2 + 34, y + 6), (x + w // 2 + 52, y + 24),
                   (x + w // 2 + 40, y + h - 8), (x + w // 2 - 6, y + h - 12), (x + w // 2 - 24, y + 22)],
                  fill=(90, 160, 90), outline=(40, 100, 40))
        d.ellipse([x + w // 2 - 2, y + h - 10, x + w // 2 + 30, y + h - 4], fill=(70, 130, 70))
        d.ellipse([x + w // 2 - 6, y + 12, x + w // 2 + 10, y + 28], fill=RED)
        d.polygon([(x + w // 2 + 2, y + 28), (x + w // 2 - 3, y + 38), (x + w // 2 + 7, y + 38)], fill=RED)
    elif kind == "yurt":
        # open steppe: pale sky, distant snow-capped mountains, grass
        sky4 = (212, 226, 240)
        vgrad(x, y, w, h, (206, 222, 238), (232, 228, 200))
        cloud(x + 130, y + 8, 9, sky4)
        d.polygon([(x, y + 26), (x + 40, y + 14), (x + 80, y + 24), (x + 120, y + 12),
                   (x + 160, y + 22), (x + w, y + 16), (x + w, y + 28), (x, y + 28)],
                  fill=(150, 170, 200))
        for mx0 in (40, 120):
            d.polygon([(x + mx0, y + 16), (x + mx0 + 8, y + 10), (x + mx0 + 16, y + 16)],
                      fill=(245, 245, 248))
        vgrad(x, y + 28, w, h - 28, (190, 200, 130), (150, 170, 95))
        for gx in range(x + 6, x + w - 6, 14):
            d.line([(gx, y + h - 6), (gx + 3, y + h - 12)], fill=(110, 140, 70), width=1)
        flag("mongolia", x + 8, y + 6, 56, 32)
        # the ger (yurt): domed roof with a shaded side, red door, cast shadow
        d.ellipse([x + w // 2 - 52, y + h - 10, x + w // 2 + 52, y + h - 4], fill=(120, 140, 75))
        d.pieslice([x + w // 2 - 52, y + 10, x + w // 2 + 52, y + h - 6], 180, 360, fill=(240, 230, 200), outline=NAVY, width=2)
        d.pieslice([x + w // 2 + 10, y + 14, x + w // 2 + 52, y + h - 6], 270, 360, fill=(214, 200, 168))
        d.arc([x + w // 2 - 52, y + 10, x + w // 2 + 52, y + h - 6], 180, 260, fill=(255, 255, 255), width=2)
        d.rectangle([x + w // 2 - 12, y + h - 26, x + w // 2 + 12, y + h - 6], fill=(178, 44, 40))
        d.rectangle([x + w // 2 - 12, y + h - 26, x + w // 2 + 12, y + h - 22], fill=(220, 90, 80))
    elif kind == "chart":
        # a trading screen: dark blue board, glowing bars, a falling line
        vgrad(x, y, w, h, (38, 52, 78), (22, 32, 56))
        d.rectangle([x + 8, y + 4, x + w - 8, y + 12], fill=(16, 24, 44))
        for tx in range(x + 12, x + w - 12, 14):
            d.rectangle([tx, y + 6, tx + 6, y + 10], fill=(255, 180, 60) if (tx // 14) % 3 else (90, 200, 120))
        flag("us", x + w - 58, y + 14, 50, 22)
        bars = [18, 26, 22, 34, 44]
        for i, bh in enumerate(bars):
            bx = x + 12 + i * ((w - 24) // 5)
            col = (60, 190, 110) if i < 4 else (230, 70, 60)
            d.rectangle([bx + 2, y + h - 6 - bh, bx + 24, y + h - 8], fill=(10, 18, 34))
            d.rectangle([bx, y + h - 8 - bh, bx + 22, y + h - 8], fill=col)
            d.rectangle([bx, y + h - 8 - bh, bx + 22, y + h - 5 - bh], fill=(255, 255, 255))
            d.line([(bx + 11, y + h - 10 - bh), (bx + 11, y + h - 16 - bh)], fill=col, width=2)
        d.line([x + 10, y + h - 30, x + w - 10, y + 10], fill=(255, 214, 130), width=2)
        d.ellipse([x + w - 16, y + 12, x + w - 8, y + 20], fill=(230, 70, 60))
    elif kind == "virus":
        # a clinic yard: pale sky, a white clinic with a red cross, shaded ground
        vgrad(x, y, w, h, (244, 224, 220), (232, 200, 196))
        d.rectangle([x, y + h - 12, x + w, y + h], fill=(190, 160, 140))
        d.rectangle([x + w // 2 - 34, y + 12, x + w // 2 + 34, y + h - 12], fill=(252, 252, 248),
                    outline=(180, 170, 160), width=1)
        d.polygon([(x + w // 2 - 40, y + 12), (x + w // 2, y + 2), (x + w // 2 + 40, y + 12)],
                  fill=(178, 44, 40))
        d.rectangle([x + w // 2 - 6, y + 18, x + w // 2 + 6, y + 30], fill=(200, 40, 40))
        d.rectangle([x + w // 2 - 12, y + 22, x + w // 2 + 12, y + 26], fill=(200, 40, 40))
        d.rectangle([x + w // 2 - 20, y + 32, x + w // 2 + 20, y + h - 12], fill=(120, 70, 60))
        d.rectangle([x + w // 2 - 20, y + 32, x + w // 2 + 20, y + 35], fill=(150, 95, 80))
        for wy in (y + 16, y + 24):
            d.rectangle([x + w // 2 - 28, wy, x + w // 2 - 22, wy + 4], fill=(150, 190, 220))
            d.rectangle([x + w // 2 + 22, wy, x + w // 2 + 28, wy + 4], fill=(150, 190, 220))
        flag("congo", x + 8, y + 6, 56, 32)
        # the virus, shaded with a darker rim and a pale centre
        cx, cy, r = x + w - 30, y + h // 2 + 8, 11
        for ang in range(0, 360, 45):
            dx, dy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
            d.line([cx + dx * r, cy + dy * r, cx + dx * (r + 7), cy + dy * (r + 7)], fill=RED, width=3)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(190, 30, 30))
        d.ellipse([cx - r + 3, cy - r + 2, cx - 2, cy - 2], fill=(230, 90, 80))
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 255, 255))
    elif kind == "globe":
        # a summit hall in Antalya: warm wall, a podium, and a shaded globe
        vgrad(x, y, w, h, (214, 232, 226), (180, 208, 196))
        d.rectangle([x, y + h - 10, x + w, y + h], fill=(140, 110, 80))
        d.rectangle([x + w // 2 - 22, y + h - 22, x + w // 2 + 22, y + h - 10], fill=(96, 70, 50))
        d.rectangle([x + w // 2 - 22, y + h - 22, x + w // 2 + 22, y + h - 19], fill=(150, 115, 82))
        d.ellipse([x + w // 2 - 8, y + h - 30, x + w // 2 + 8, y + h - 22], fill=(240, 220, 190))
        flag("turkiye", x + 8, y + 6, 56, 32)
        # globe: ocean gradient, green land arcs, a bright highlight
        gx0, gy0 = x + w - 50, y + 2
        d.ellipse([gx0, gy0, gx0 + 44, gy0 + 44], fill=(110, 185, 218), outline=NAVY, width=2)
        d.pieslice([gx0 + 22, gy0, gx0 + 44, gy0 + 44], 270, 360, fill=(80, 160, 195))
        d.arc([gx0, gy0, gx0 + 44, gy0 + 44], 200, 340, fill=(70, 160, 90), width=6)
        d.arc([gx0, gy0, gx0 + 44, gy0 + 44], 20, 120, fill=(70, 160, 90), width=5)
        d.arc([gx0 + 6, gy0 + 4, gx0 + 22, gy0 + 20], 200, 320, fill=(255, 255, 255), width=2)
        # a small thermometer beside the globe, mercury rising
        d.rectangle([x + w - 62, y + 10, x + w - 56, y + h - 14], fill=(255, 255, 255), outline=NAVY, width=1)
        d.rectangle([x + w - 61, y + 22, x + w - 57, y + h - 15], fill=(220, 60, 40))
        d.ellipse([x + w - 64, y + h - 16, x + w - 54, y + h - 6], fill=(220, 60, 40))
    elif kind == "parliament":
        # the parliament house at dusk: warm sky, lit columns, steps, a crowd
        vgrad(x, y, w, h, (232, 222, 208), (206, 196, 178))
        d.ellipse([x + w - 34, y + 6, x + w - 18, y + 22], fill=(255, 224, 150))
        flag("serbia", x + 8, y + 6, 56, 32)
        # pediment with a shaded edge, columns with light and shadow sides
        d.polygon([(x + 70, y + 10), (x + w // 2 + 20, y - 2), (x + w - 14, y + 10)], fill=NAVY)
        d.polygon([(x + 70, y + 10), (x + w // 2 + 20, y - 2), (x + w // 2 + 20, y + 10)], fill=(60, 75, 100))
        for i in range(3):
            cx = x + 76 + i * 28
            d.rectangle([cx, y + 14, cx + 8, y + h - 8], fill=(240, 238, 230), outline=(150, 145, 130), width=1)
            d.rectangle([cx + 5, y + 14, cx + 8, y + h - 8], fill=(200, 195, 180))
            d.rectangle([cx - 2, y + 12, cx + 10, y + 15], fill=(240, 238, 230))
        d.rectangle([x + 70, y + h - 10, x + w - 14, y + h - 4], fill=(180, 170, 155))
        d.rectangle([x + 70, y + h - 7, x + w - 14, y + h - 4], fill=(150, 140, 125))
        # a small crowd in front of the steps
        for cx, cy, c in [(x + 84, y + h - 4, RED), (x + 96, y + h - 5, BLUE),
                          (x + 108, y + h - 4, (60, 60, 60)), (x + 120, y + h - 5, RED)]:
            d.ellipse([cx - 3, cy - 6, cx + 3, cy], fill=c)
    elif kind == "crash":
        # a snowy Siberian forest at dusk: grey-blue sky, pines, snow, smoke
        vgrad(x, y, w, h, (196, 206, 220), (228, 232, 238))
        cloud(x + 40, y + 8, 9, (200, 210, 222))
        # pine trees along the back, snow-capped
        for tx, th in [(x + 6, 22), (x + 26, 28), (x + 48, 20), (x + w - 58, 24), (x + w - 38, 28)]:
            d.polygon([(tx, y + h - 14), (tx + 8, y + h - 14 - th), (tx + 16, y + h - 14)],
                      fill=(36, 80, 52))
            d.polygon([(tx + 4, y + h - 14 - th + 6), (tx + 8, y + h - 14 - th), (tx + 12, y + h - 14 - th + 6)],
                      fill=(235, 238, 242))
        # snow ground with a soft shadow under the wreck
        vgrad(x, y + h - 14, w, 14, (238, 240, 244), (214, 220, 228))
        d.ellipse([x + 30, y + h - 12, x + w - 30, y + h - 4], fill=(190, 196, 206))
        flag("russia", x + 8, y + 6, 56, 32)
        # the plane, tilted down, fuselage highlight on top, dark belly
        d.polygon([(x + 16, y + h // 2), (x + w - 60, y + h // 2 - 12), (x + w - 40, y + h // 2 + 2),
                   (x + w - 60, y + h // 2 + 14)], fill=SLATE)
        d.polygon([(x + 20, y + h // 2 - 1), (x + w - 62, y + h // 2 - 11), (x + w - 48, y + h // 2 - 5)],
                  fill=(120, 128, 140))
        d.polygon([(x + w - 66, y + h // 2 - 8), (x + w - 40, y + h - 14), (x + w - 52, y + h // 2 + 6)], fill=SLATE)
        # layered smoke and a small fire glow at the impact point
        soft_disc(x + w - 34, y + 12, 12, 8, (130, 130, 135), (200, 210, 222), steps=5)
        soft_disc(x + w - 22, y + 18, 10, 7, (160, 160, 165), (200, 210, 222), steps=4)
        soft_disc(x + w - 26, y + h - 18, 10, 7, (255, 170, 60), (220, 224, 232), steps=4)
        d.polygon([(x + w - 30, y + h - 16), (x + w - 24, y + h - 28), (x + w - 18, y + h - 16)], fill=(220, 90, 30))
    elif kind == "scales":
        # a courthouse in Maputo: warm sky, a columned facade, shaded steps
        vgrad(x, y, w, h, (236, 228, 208), (214, 200, 172))
        d.rectangle([x + 10, y + 14, x + w - 10, y + h - 12], fill=(240, 236, 222), outline=(180, 170, 150), width=1)
        d.polygon([(x + 10, y + 14), (x + w // 2, y + 2), (x + w - 10, y + 14)], fill=(120, 90, 60))
        for cx in (x + 34, x + w // 2 - 4, x + w - 42):
            d.rectangle([cx, y + 16, cx + 8, y + h - 12], fill=(225, 218, 200), outline=(170, 160, 140), width=1)
            d.rectangle([cx + 5, y + 16, cx + 8, y + h - 12], fill=(195, 186, 165))
        d.rectangle([x + 10, y + h - 12, x + w - 10, y + h - 4], fill=(170, 155, 130))
        flag("mozambique", x + 8, y + 6, 56, 32)
        # the scales in front, brass with a bright rim and a soft shadow
        d.ellipse([x + w - 58, y + h - 10, x + w - 30, y + h - 5], fill=(150, 135, 110))
        d.line([x + w - 44, y + 8, x + w - 44, y + h - 10], fill=(90, 70, 40), width=3)
        d.line([x + w - 44, y + 8, x + w - 44, y + h - 10], fill=(200, 170, 100), width=1)
        d.line([x + w - 72, y + 14, x + w - 16, y + 14], fill=(90, 70, 40), width=3)
        d.polygon([(x + w - 80, y + 16), (x + w - 62, y + 16), (x + w - 71, y + 32)], fill=(200, 170, 100))
        d.polygon([(x + w - 26, y + 16), (x + w - 8, y + 16), (x + w - 17, y + 32)], fill=(200, 170, 100))
        d.rectangle([x + w - 58, y + h - 12, x + w - 30, y + h - 6], fill=(90, 70, 40))

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
    # soft drop shadow so the card lifts off the paper
    d.rounded_rectangle([x + 3, y + 3, x + w + 3, y + h + 3], radius=6, fill=(208, 198, 178))
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
d.rounded_rectangle([mx + 3, by + 3, mx + mw + 3, by + mh + 3], radius=6, fill=(208, 198, 178))
d.rounded_rectangle([mx, by, mx + mw, by + mh], radius=6, fill=(255, 255, 255), outline=NAVY, width=2)
d.text((mx + 12, by + 10), "WHERE IT HAPPENED", font=font(SANSB, 16), fill=NAVY)
d.line([mx + 12, by + 34, mx + mw - 12, by + 34], fill=NAVY, width=2)
mapx, mapy, mapw, maph = mx + 10, by + 44, mw - 20, 190
# sea with a depth gradient, lighter near the top
vgrad(mapx, mapy, mapw, maph, (202, 226, 238), (164, 196, 222))
# equirectangular projection: lon -170..190, lat 75..-55
def ll(lon, lat):
    return (mapx + (lon + 170) / 360 * mapw, mapy + (75 - lat) / 130 * maph)
def land(poly, label=None, lab_lon=None, lab_lat=None):
    pts = [ll(lo, la) for lo, la in poly]
    # relief shadow: the same shape offset down-right in a darker tan
    d.polygon([(px + 2, py + 2) for px, py in pts], fill=(206, 184, 138))
    d.polygon(pts, fill=(233, 214, 168), outline=(110, 88, 55), width=1)
    # a faint coastal highlight along the top edge of the land
    d.line(pts[:3], fill=(248, 236, 200), width=1)
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
d.rounded_rectangle([lx + 3, by + 3, lx + lw + 3, by + mh + 3], radius=6, fill=(208, 198, 178))
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

# a whisper of film grain over the whole page (seeded, so it is identical
# every run): it takes the flat digital edge off the paper and the drawings
rng = random.Random(20261117)
noise = Image.new("L", (W, H))
noise.putdata([128 + rng.randint(-16, 16) for _ in range(W * H)])
img = Image.blend(img, Image.merge("RGB", (noise, noise, noise)), 0.045)

img.save(OUT, "PNG", optimize=True)
print("wrote", OUT, os.path.getsize(OUT), "bytes")

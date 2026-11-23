#!/usr/bin/env python3
"""Render the ni23 front page: 'THE WORLD IN ONE DAY — Monday 23 November 2026'.

Deterministic, offline. Writes entry.png (1024x1024, <= 1 MiB).
All news verified by web search on 2026-11-23 for the 23 Nov news cycle.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

# ---- palette: warm newsprint ----
PAPER = (250, 246, 236)
INK = (26, 24, 20)
RED = (178, 34, 28)
BLUE = (28, 64, 120)
TEAL = (14, 96, 92)
GOLD = (176, 124, 22)
GREEN = (34, 110, 52)
AMBER = (176, 116, 10)
GREY = (110, 104, 92)
LIGHT = (238, 232, 218)
RULE = (26, 24, 20)
MAPDOT = (52, 58, 66)

FONT_DIR = "/usr/share/fonts/truetype"
def font(name, size):
    for p in (
        os.path.join(FONT_DIR, "dejavu", name),
        os.path.join(FONT_DIR, "noto", name),
    ):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SERIF_I = lambda s: font("DejaVuSerif-Italic.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_BO = lambda s: font("DejaVuSans-BoldOblique.ttf", s)

# ---- verified story set: 36 stories, 7 regions ----
# status: REPORTED / CLAIM / ONGOING
LEADS = [
    dict(num=1, region="WORLD", kicker="CLIMATE", status="REPORTED",
         scene="cop31",
         head="COP31 collapses: no deal in Antalya",
         summ="After two weeks and two days of overtime — the longest COP on record — the EU rejects a final text with no mention of fossil fuels. Kurum: 'There is nothing to do.' Talks suspended.",
         src="Reuters · UN News · edie"),
    dict(num=2, region="MIDDLE EAST", kicker="HORMUZ WAR", status="ONGOING",
         scene="hormuz",
         head="Iran strikes Bahrain, tankers burn",
         summ="Bahrain says two wounded as an Iranian strike hits a civilian industrial site at Sitra. The IRGC claims Patriot radars hit at Al-Riffa and Awali; two tankers catch fire on mines in the strait.",
         src="AFP · Al Jazeera · Reuters"),
    dict(num=3, region="EUROPE", kicker="UKRAINE", status="REPORTED",
         scene="kyiv",
         head="Zelenskyy pleads for US Patriots",
         summ="Russia kills seven across Ukraine on Sunday — three in Dymer, where a drone brought down a five-storey block. Zelenskyy says Moscow fired 2,700 drones in a week and urges the US to release Patriots.",
         src="Al Jazeera · Reuters · Kyiv Independent"),
]

SMALL = [
    dict(num=4, region="AMERICAS", kicker="MARKETS", status="REPORTED", scene="ipo",
         head="Anthropic's record $81.3bn IPO",
         summ="Claude maker up 17% on debut, briefly worth $2tn; Nasdaq −10%."),
    dict(num=5, region="AMERICAS", kicker="US POLITICS", status="REPORTED", scene="house",
         head="Democrats win 258 House seats",
         summ="Historic House majority, the largest since 1992, takes shape."),
    dict(num=6, region="ASIA-PACIFIC", kicker="DISASTER", status="REPORTED", scene="fire",
         head="24 body bags from Indonesia factory fire",
         summ="Rescuers scour the burned Milkita plant; dozens still missing."),
    dict(num=7, region="OCEANIA", kicker="CRICKET", status="REPORTED", scene="cricket",
         head="India post record 720/9d in Wellington",
         summ="India rewrite the record books on day four in Wellington."),
    dict(num=8, region="AMERICAS", kicker="F1", status="REPORTED", scene="f1",
         head="Verstappen wins chaotic Las Vegas GP",
         summ="A wild night race in Nevada as the Ferraris clash again."),
    dict(num=9, region="EUROPE", kicker="FOOTBALL", status="REPORTED", scene="football",
         head="Liverpool thrash 10-man Man Utd",
         summ="A statement win in Pochettino's first match in charge."),
    dict(num=10, region="ASIA-PACIFIC", kicker="AI IN SCHOOLS", status="REPORTED", scene="exam",
         head="S. Korea minister quits over AI cheating",
         summ="Education minister resigns over an AI exam-cheating scandal."),
    dict(num=11, region="ASIA-PACIFIC", kicker="DIPLOMACY", status="REPORTED", scene="delhi",
         head="Nepal PM holds talks with Modi",
         summ="Shah's Delhi visit reviews the full range of India–Nepal ties."),
    dict(num=12, region="WORLD", kicker="UNITED NATIONS", status="REPORTED", scene="un",
         head="UN to keep talking on lethal AI weapons",
         summ="UN talks on lethal autonomous weapons will continue."),
    dict(num=13, region="AMERICAS", kicker="CARTELS", status="REPORTED", scene="sinaloa",
         head="Mexico captures 'El Chapo Isidro'",
         summ="FBI's most-wanted cartel boss seized; 11 die in Sinaloa."),
]

WIRE = [
    (14, "EUROPE", "Russian cargo ship Sparta II still burning off Finland after drone strike"),
    (15, "AFRICA", "Russian warship hit in Libya by suspected Ukrainian drone at Benghazi"),
    (16, "EUROPE", "Lavrov calls Kyiv 'ancestral Russian lands' as sides trade strikes"),
    (17, "AMERICAS", "Trump doubles down calling Putin 'my friend' after China summit"),
    (18, "AMERICAS", "US intelligence chief: Putin is 'not America's friend in Ukraine'"),
    (19, "AMERICAS", "FBI investigates apparent breach of its criminal database"),
    (20, "AMERICAS", "Miley Cyrus marries Maxx Morando in California ceremony"),
    (21, "AMERICAS", "'Sunrise on the Reaping' opens at No. 1 with $120m in North America"),
    (22, "EUROPE", "Thousands march in Lisbon as living costs fuel anger"),
    (23, "EUROPE", "Thousands protest opposition-linked media closures in Istanbul"),
    (24, "AFRICA", "SPLA-IO attack leaves 24 civilians dead in South Sudan"),
    (25, "AFRICA", "WHO: fighting near Congo Ebola outbreak disrupts response efforts"),
    (26, "ASIA-PACIFIC", "Myanmar's army-backed government calls ASEAN decision 'unfair'"),
    (27, "AMERICAS", "Automation fault causes Delta flight delays in Atlanta"),
    (28, "AMERICAS", "Washington governor calls ICE 'out of control' after airport arrests"),
    (29, "AMERICAS", "3 killed and 1 wounded in shooting at Ohio baby shower"),
    (30, "AMERICAS", "Tom Jackson, Broncos star and ESPN broadcaster, dies at 75"),
    (31, "EUROPE", "Poland says Russia twice tried to kill a Ukrainian-American rapper"),
    (32, "EUROPE", "UK to produce Ukrainian drones under new deal signed in London"),
    (33, "EUROPE", "EU Council chief unveils reduced budget, keeps €100bn for Ukraine"),
    (34, "MIDDLE EAST", "Briton swims the Strait of Hormuz to highlight war's toll on sea life"),
    (35, "ASIA-PACIFIC", "Anupama defends IBSF World Women's Snooker Championship"),
    (36, "ASIA-PACIFIC", "Philippines to lead Asia-Pacific farm modernisation talks, 23–26 Nov"),
]

KEYS = [
    ("0", "COP31 deal agreed\nin Antalya"),
    ("2,700", "Russian drones fired\nat Ukraine in a week"),
    ("$81.3bn", "Anthropic's record\nIPO — largest ever"),
    ("258", "Democrat House seats\n— most since 1992"),
    ("24", "body bags recovered\nin Indonesia factory fire"),
    ("$120m", "'Sunrise on the Reaping'\nopening weekend"),
]

REGIONS = [
    ("EUROPE", 9, (28, 64, 120)),
    ("MIDDLE EAST", 2, (178, 34, 28)),
    ("ASIA-PACIFIC", 6, (14, 96, 92)),
    ("AMERICAS", 13, (34, 110, 52)),
    ("AFRICA", 3, (176, 124, 22)),
    ("OCEANIA", 1, (110, 70, 140)),
    ("WORLD", 2, (90, 88, 80)),
]

UTC_BEATS = [
    ("00:02", "UN agrees to keep\ntalking on lethal AI"),
    ("04:00", "Verstappen wins\nchaotic Las Vegas GP"),
    ("12:00", "COP31 collapses:\nno deal in Antalya"),
    ("14:00", "Bahrain: 2 wounded\nin Iran strike"),
    ("15:00", "Indonesia: 24 body\nbags from factory fire"),
    ("17:30", "Liverpool thrash\n10-man Man Utd"),
]

DATE_CHECK = [
    "Anthropic's debut was Thu 19 Nov — the market fallout, not the debut, is Monday's news.",
    "COP31 collapsed Sun 22 Nov afternoon; the reactions and suspension are Monday's story.",
    "The Indonesia fire broke out Sat 21 Nov evening; the search and toll are Monday's news.",
    "The Sparta II was struck Sat 22 Nov; it was still burning off Finland on Monday.",
    "The Bahrain strike was Sat 21 Nov; the wounded toll and Saudi reply came Sunday–Monday.",
    "'El Chapo Isidro' was captured Sun 22 Nov; the operation's fallout is Monday's news.",
]

# pins: (story num, fx, fy) fractions of the map area (lon/lat mapped)
PINS = [
    (1, 0.583, 0.30), (2, 0.655, 0.36), (3, 0.583, 0.22),
    (4, 0.294, 0.28), (5, 0.27, 0.33), (6, 0.72, 0.62),
    (7, 0.86, 0.90), (8, 0.18, 0.30), (9, 0.53, 0.22),
    (10, 0.853, 0.29), (11, 0.714, 0.34), (12, 0.55, 0.28),
    (13, 0.203, 0.36),
]

STATUS_COLOR = {"REPORTED": GREEN, "CLAIM": RED, "ONGOING": AMBER}


# ---- text helpers ----
def wrap(draw, text, fnt, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_lines(draw, lines, x, y, fnt, fill, lh=None, max_lines=None):
    if max_lines is not None:
        lines = lines[:max_lines]
    if lh is None:
        lh = fnt.size + 3
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y

def chip(draw, x, y, text, fnt, bg, fg=(255, 255, 255)):
    tw = draw.textlength(text, font=fnt)
    pad = 6
    draw.rounded_rectangle([x, y, x + tw + pad * 2, y + fnt.size + 7], radius=3, fill=bg)
    draw.text((x + pad, y + 3), text, font=fnt, fill=fg)
    return x + tw + pad * 2

# ---- drawn scenes (all original vector art, no images) ----
def scene_cop31(d, x, y, w, h):
    # conference hall: warm wall, long table, flags, delegates
    d.rectangle([x, y, x + w, y + h], fill=(188, 152, 108))
    d.rectangle([x, y, x + w, y + int(h * 0.42)], fill=(96, 56, 40))
    # windows
    for i in range(5):
        wx = x + 14 + i * (w - 28) // 5
        d.rectangle([wx, y + 8, wx + (w - 28) // 5 - 8, y + int(h * 0.34)], fill=(246, 232, 198), outline=(60, 36, 24), width=2)
    # flags row
    for i, c in enumerate([(178, 34, 28), (28, 64, 120), (34, 110, 52), (176, 124, 22), (14, 96, 92)]):
        fx = x + w // 2 - 52 + i * 22
        d.rectangle([fx, y + int(h * 0.46), fx + 14, y + int(h * 0.60)], fill=c)
        d.line([fx + 7, y + int(h * 0.46), fx + 7, y + int(h * 0.62)], fill=INK, width=2)
    # long table
    d.rectangle([x + 8, y + int(h * 0.66), x + w - 8, y + int(h * 0.80)], fill=(96, 52, 34))
    d.rectangle([x + 8, y + int(h * 0.66), x + w - 8, y + int(h * 0.70)], fill=(140, 82, 52))
    # delegates: heads + shoulders
    for i in range(6):
        cx = x + 26 + i * (w - 52) // 5
        d.ellipse([cx - 9, y + int(h * 0.74), cx + 9, y + int(h * 0.74) + 18], fill=(232, 196, 160))
        d.pieslice([cx - 16, y + int(h * 0.86), cx + 16, y + h + 6], 180, 360,
                   fill=[(28, 64, 120), (178, 34, 28), (34, 110, 52), (90, 88, 80), (14, 96, 92), (176, 124, 22)][i])
    # papers on table
    for i in range(4):
        px = x + 30 + i * (w - 60) // 3
        d.rectangle([px, y + int(h * 0.68), px + 22, y + int(h * 0.68) + 8], fill=(250, 246, 236))

def scene_hormuz(d, x, y, w, h):
    # night strait: dark sea, burning tanker, missile arcs, skyline
    d.rectangle([x, y, x + w, y + h], fill=(16, 22, 38))
    # stars
    for sx, sy in [(0.08, 0.12), (0.22, 0.06), (0.38, 0.14), (0.55, 0.08), (0.72, 0.12), (0.88, 0.07), (0.95, 0.2), (0.3, 0.2)]:
        d.ellipse([x + sx * w - 2, y + sy * h - 2, x + sx * w + 2, y + sy * h + 2], fill=(240, 230, 200))
    # moon
    d.ellipse([x + w * 0.82, y + 10, x + w * 0.82 + 26, y + 36], fill=(240, 232, 200))
    # skyline (Bahrain towers)
    for i, bh in enumerate([0.42, 0.55, 0.36, 0.62, 0.44]):
        bx = x + 12 + i * (w - 24) // 5
        bw = (w - 24) // 5 - 8
        d.rectangle([bx, y + h * 0.62 - bh * h * 0.5, bx + bw, y + h * 0.62], fill=(38, 48, 74))
        for wy in range(3):
            d.rectangle([bx + 4, y + h * 0.62 - bh * h * 0.5 + 6 + wy * 10, bx + bw - 4, y + h * 0.62 - bh * h * 0.5 + 12 + wy * 10], fill=(240, 200, 90))
    # sea
    d.rectangle([x, y + int(h * 0.62), x + w, y + h], fill=(24, 52, 88))
    for i in range(6):
        d.line([x + 8 + i * 8, y + int(h * 0.68) + i * 9, x + w - 8 - i * 6, y + int(h * 0.68) + i * 9], fill=(60, 110, 160), width=2)
    # tanker with fire
    tx, ty, tw = x + w * 0.30, y + int(h * 0.70), w * 0.42
    d.rectangle([tx, ty, tx + tw, ty + 18], fill=(120, 40, 30))
    d.rectangle([tx + tw * 0.55, ty - 16, tx + tw * 0.75, ty], fill=(200, 200, 200))
    for j, (fx, fy, fr) in enumerate([(0.15, -6, 14), (0.35, -14, 18), (0.55, -8, 15), (0.75, -12, 12)]):
        d.ellipse([tx + tw * fx - fr, ty + fy - fr, tx + tw * fx + fr, ty + fy + fr],
                  fill=[(240, 120, 20), (250, 180, 40), (230, 90, 20), (255, 200, 60)][j])
    # missile arcs
    d.arc([x + w * 0.05, y + 6, x + w * 0.55, y + int(h * 0.55)], 200, 340, fill=(255, 200, 80), width=3)
    d.arc([x + w * 0.45, y + 2, x + w * 0.98, y + int(h * 0.5)], 200, 340, fill=(255, 160, 60), width=3)

def scene_kyiv(d, x, y, w, h):
    # night Kyiv skyline: lit windows, drones, searchlights, burning block
    d.rectangle([x, y, x + w, y + h], fill=(18, 20, 36))
    for sx, sy in [(0.06, 0.1), (0.18, 0.05), (0.34, 0.12), (0.5, 0.07), (0.66, 0.13), (0.82, 0.06), (0.94, 0.15)]:
        d.ellipse([x + sx * w - 2, y + sy * h - 2, x + sx * w + 2, y + sy * h + 2], fill=(240, 230, 200))
    # searchlight beams
    d.polygon([(x + w * 0.2, y + h), (x + w * 0.05, y + 12), (x + w * 0.12, y + 12)], fill=(200, 210, 235))
    d.polygon([(x + w * 0.8, y + h), (x + w * 0.68, y + 8), (x + w * 0.76, y + 8)], fill=(200, 210, 235))
    # buildings
    for i, bh in enumerate([0.5, 0.68, 0.44, 0.74, 0.58, 0.4]):
        bx = x + 6 + i * (w - 12) // 6
        bw = (w - 12) // 6 - 6
        top = y + h - int(bh * h * 0.62)
        d.rectangle([bx, top, bx + bw, y + h], fill=(30, 34, 52))
        for r in range(4):
            for c in range(2):
                if (i + r + c) % 3 == 0:
                    d.rectangle([bx + 5 + c * (bw // 2), top + 8 + r * 14, bx + 5 + c * (bw // 2) + 8, top + 16 + r * 14], fill=(240, 200, 90))
    # burning block (right)
    bx = x + w * 0.78
    d.rectangle([bx, y + h - 52, bx + w * 0.18, y + h], fill=(60, 30, 26))
    for j, (fx, fr) in enumerate([(0.3, 12), (0.55, 16), (0.8, 11)]):
        d.ellipse([bx + w * 0.18 * fx - fr, y + h - 66 - fr, bx + w * 0.18 * fx + fr, y + h - 66 + fr],
                  fill=[(240, 120, 20), (250, 180, 40), (230, 90, 20)][j])
    # drones: small crosses with red dots
    for dx, dy in [(0.3, 0.2), (0.55, 0.12), (0.72, 0.24)]:
        cx, cy = x + dx * w, y + dy * h
        d.line([cx - 7, cy, cx + 7, cy], fill=(220, 220, 220), width=2)
        d.line([cx, cy - 7, cx, cy + 7], fill=(220, 220, 220), width=2)
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(255, 60, 40))

def scene_generic(d, x, y, w, h, sky, ground, kind):
    d.rectangle([x, y, x + w, y + h], fill=sky)
    d.rectangle([x, y + int(h * 0.62), x + w, y + h], fill=ground)
    if kind == "ipo":
        # rising chart + Nasdaq board
        d.rectangle([x + 8, y + 8, x + w - 8, y + int(h * 0.5)], fill=(16, 28, 52))
        pts = [(x + 12, y + int(h * 0.42)), (x + w * 0.3, y + int(h * 0.36)), (x + w * 0.5, y + int(h * 0.4)),
               (x + w * 0.68, y + int(h * 0.24)), (x + w - 12, y + int(h * 0.14))]
        d.line(pts, fill=(60, 220, 120), width=4, joint="curve")
        d.polygon([(x + w - 26, y + int(h * 0.14)), (x + w - 12, y + int(h * 0.14)), (x + w - 19, y + int(h * 0.06))], fill=(60, 220, 120))
        for i in range(5):
            d.rectangle([x + 14 + i * (w - 28) // 5, y + int(h * 0.72), x + 14 + (i + 1) * (w - 28) // 5 - 6, y + int(h * 0.72) + 16 - i * 2], fill=(240, 200, 90))
    elif kind == "house":
        d.rectangle([x + w * 0.2, y + int(h * 0.18), x + w * 0.8, y + int(h * 0.62)], fill=(240, 240, 235))
        d.polygon([(x + w * 0.14, y + int(h * 0.2)), (x + w * 0.5, y + 4), (x + w * 0.86, y + int(h * 0.2))], fill=(178, 34, 28))
        for i in range(6):
            d.rectangle([x + w * 0.26 + i * w * 0.09, y + int(h * 0.3), x + w * 0.26 + i * w * 0.09 + w * 0.05, y + int(h * 0.48)], fill=(28, 64, 120))
        d.rectangle([x + w * 0.44, y + int(h * 0.48), x + w * 0.56, y + int(h * 0.62)], fill=(90, 58, 40))
    elif kind == "fire":
        d.rectangle([x + 10, y + int(h * 0.3), x + w - 10, y + int(h * 0.62)], fill=(70, 60, 55))
        for j, (fx, fr) in enumerate([(0.25, 12), (0.5, 18), (0.75, 13)]):
            d.ellipse([x + w * fx - fr, y + int(h * 0.3) - fr, x + w * fx + fr, y + int(h * 0.3) + fr],
                      fill=[(240, 120, 20), (250, 180, 40), (230, 90, 20)][j])
        d.rectangle([x + w * 0.1, y + int(h * 0.62), x + w * 0.9, y + h - 4], fill=(120, 40, 30))
    elif kind == "cricket":
        d.ellipse([x + w * 0.15, y + int(h * 0.3), x + w * 0.85, y + int(h * 0.85)], fill=(34, 110, 52))
        d.rectangle([x + w * 0.42, y + int(h * 0.18), x + w * 0.58, y + int(h * 0.85)], fill=(214, 186, 148))
        d.line([x + w * 0.5, y + int(h * 0.18), x + w * 0.5, y + int(h * 0.85)], fill=(255, 255, 255), width=2)
        d.ellipse([x + w * 0.46, y + int(h * 0.3), x + w * 0.54, y + int(h * 0.38)], fill=(178, 34, 28))
    elif kind == "f1":
        d.rectangle([x + 8, y + int(h * 0.42), x + w - 8, y + int(h * 0.55)], fill=(40, 40, 44))
        d.rectangle([x + w * 0.2, y + int(h * 0.3), x + w * 0.8, y + int(h * 0.46)], fill=(178, 34, 28))
        d.rectangle([x + w * 0.3, y + int(h * 0.2), x + w * 0.62, y + int(h * 0.32)], fill=(28, 64, 120))
        for wx in (0.3, 0.68):
            d.ellipse([x + w * wx - 9, y + int(h * 0.5) - 9, x + w * wx + 9, y + int(h * 0.5) + 9], fill=(20, 20, 20), outline=(200, 200, 200))
    elif kind == "football":
        d.rectangle([x, y + int(h * 0.55), x + w, y + h], fill=(34, 110, 52))
        d.line([x + w * 0.5, y + int(h * 0.55), x + w * 0.5, y + h], fill=(255, 255, 255), width=2)
        d.ellipse([x + w * 0.1, y + int(h * 0.1), x + w * 0.9, y + int(h * 0.55)], fill=(240, 240, 235), outline=(200, 200, 200))
        d.ellipse([x + w * 0.44, y + int(h * 0.62), x + w * 0.56, y + int(h * 0.74)], fill=(255, 255, 255), outline=INK)
    elif kind == "exam":
        d.rectangle([x + w * 0.2, y + int(h * 0.18), x + w * 0.8, y + int(h * 0.62)], fill=(250, 246, 236), outline=INK)
        for i in range(3):
            d.line([x + w * 0.28, y + int(h * 0.3) + i * 10, x + w * 0.72, y + int(h * 0.3) + i * 10], fill=(120, 116, 104), width=2)
        d.rectangle([x + w * 0.62, y + int(h * 0.44), x + w * 0.74, y + int(h * 0.58)], fill=(178, 34, 28))
        d.line([x + w * 0.64, y + int(h * 0.51), x + w * 0.72, y + int(h * 0.51)], fill=(255, 255, 255), width=3)
    elif kind == "delhi":
        d.rectangle([x + w * 0.35, y + int(h * 0.2), x + w * 0.65, y + int(h * 0.62)], fill=(200, 90, 60))
        d.polygon([(x + w * 0.3, y + int(h * 0.22)), (x + w * 0.5, y + 4), (x + w * 0.7, y + int(h * 0.22))], fill=(176, 124, 22))
        d.ellipse([x + w * 0.46, y + int(h * 0.32), x + w * 0.54, y + int(h * 0.4)], fill=(90, 58, 40))
        for i in range(3):
            d.rectangle([x + 12 + i * (w - 24) // 3, y + int(h * 0.4), x + 12 + (i + 1) * (w - 24) // 3 - 6, y + int(h * 0.62)], fill=(240, 220, 190))
    elif kind == "un":
        d.ellipse([x + w * 0.3, y + int(h * 0.1), x + w * 0.7, y + int(h * 0.55)], fill=(28, 64, 120))
        for i in range(5):
            d.arc([x + w * 0.32 + i * 2, y + int(h * 0.14), x + w * 0.68 - i * 2, y + int(h * 0.5)], 200, 340, fill=(255, 255, 255), width=2)
        d.rectangle([x + w * 0.2, y + int(h * 0.58), x + w * 0.8, y + int(h * 0.62)], fill=(120, 116, 104))
    elif kind == "sinaloa":
        d.rectangle([x + w * 0.15, y + int(h * 0.25), x + w * 0.85, y + int(h * 0.62)], fill=(90, 58, 40))
        for i in range(4):
            d.rectangle([x + w * 0.2 + i * w * 0.15, y + int(h * 0.32), x + w * 0.2 + i * w * 0.15 + w * 0.08, y + int(h * 0.5)], fill=(240, 200, 90))
        d.line([x + w * 0.5, y + int(h * 0.25), x + w * 0.5, y + 4], fill=(178, 34, 28), width=3)

SCENES = {
    "cop31": scene_cop31, "hormuz": scene_hormuz, "kyiv": scene_kyiv,
    "ipo": lambda d, x, y, w, h: scene_generic(d, x, y, w, h, (16, 28, 52), (24, 40, 60), "ipo"),
    "house": lambda d, x, y, w, h: scene_generic(d, x, y, w, h, (180, 210, 230), (120, 150, 120), "house"),
    "fire": lambda d, x, y, w, h: scene_generic(d, x, y, w, h, (40, 36, 34), (60, 52, 48), "fire"),
    "cricket": lambda d, x, y, w, h: scene_generic(d, x, y, w, h, (150, 190, 220), (34, 110, 52), "cricket"),
    "f1": lambda d, x, y, w, h: scene_generic(d, x, y, w, h, (18, 20, 40), (40, 40, 44), "f1"),
    "football": lambda d, x, y, w, h: scene_generic(d, x, y, w, h, (150, 190, 220), (34, 110, 52), "football"),
    "exam": lambda d, x, y, w, h: scene_generic(d, x, y, w, h, (220, 214, 200), (180, 170, 150), "exam"),
    "delhi": lambda d, x, y, w, h: scene_generic(d, x, y, w, h, (200, 220, 235), (140, 120, 90), "delhi"),
    "un": lambda d, x, y, w, h: scene_generic(d, x, y, w, h, (190, 205, 225), (120, 130, 140), "un"),
    "sinaloa": lambda d, x, y, w, h: scene_generic(d, x, y, w, h, (220, 200, 170), (120, 100, 70), "sinaloa"),
}

# ---- dotted world map: coarse land grid (rows top->bottom, 72 cols) ----
# lon -180..180 across cols 0..71; lat 75..-60 down rows 0..15.
MAP_ROWS = [
    "........XXXXXXXXXXX.................XXX.....XXXXXXXXXXXXXXXXXXXXX.......",
    "......XXXXXXXXXXXXXXXX..............XXXXX...XXXXXXXXXXXXXXXXXXXXXXXX....",
    ".....XXXXXXXXXXXXXXXXX..............XXXXXX..XXXXXXXXXXXXXXXXXXXXXXXXX...",
    "......XXXXXXXXXXXXXXXX..............XXXXXXXX.XXXXXXXXXXXXXXXXXXXXXX.....",
    "........XXXXXXXXXXXXXX................XXXXXXXXXXXXXXXXXXXXXXXXXXXX......",
    "..........XXXXXXXXXXXX................XXXXXXXXXXXXXXXXXXXXXXXXX.........",
    "............XXXXXXXXXX..................XXXXXXXXXXXXXXXXXXXXX............",
    "..............XXXXXXXX....................XXXXXXXXXXXXXXXXX..............",
    "...............XXXXXXX....XXXXXXXXX.......XXXXXXXXXXXXXXX................",
    "................XXXXXX....XXXXXXXX.........XXXXXXXXXXXX..................",
    ".................XXXXX....XXXXXXXX..........XXXXXXXXXX...................",
    "..................XXXX....XXXXXXX............XXXXXXXX....................",
    "...................XXX.....XXXXX..............XXXXXX.....................",
    "....................XX......XXX................XXXX.....................",
    "....................X.......XX..................XX......................",
    "..........................................................XXXXXX........",
    ".........................................................XXXXXXXX.......",
    "..........................................................XXXXXX........",
]


# ---- page layout ----
def render(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 24
    CW = W - 2 * MX

    # masthead
    f_mast = SANS_B(13)
    mast = "THE WORLD IN ONE DAY"
    d.text(((W - d.textlength(mast, font=f_mast)) / 2, 5), mast, font=f_mast, fill=INK)
    d.text((MX, 5), "No. 327", font=SANS(10), fill=GREY)
    d.text((W - MX - d.textlength("PRICE: ONE DAY", font=SANS(10)), 5), "PRICE: ONE DAY", font=SANS(10), fill=GREY)
    d.line([MX, 24, W - MX, 24], fill=RULE, width=2)

    # headline: date as the huge serif headline
    f_head = SERIF_B(52)
    head = "Monday 23 November 2026"
    assert d.textlength(head, font=f_head) <= CW, "headline too wide"
    d.text((MX, 28), head, font=f_head, fill=INK)
    # red italic deck
    f_deck = SERIF_I(16)
    deck = "COP31 collapses with no deal  ·  Iran strikes Bahrain  ·  Zelenskyy begs for Patriots"
    assert d.textlength(deck, font=f_deck) <= CW, "deck too wide"
    d.text((MX, 84), deck, font=f_deck, fill=RED)

    # 6 boxed key numbers
    y0, y1 = 106, 152
    cellw = CW / 6
    for i, (num, lab) in enumerate(KEYS):
        x0 = MX + i * cellw
        d.rectangle([x0 + 1, y0, x0 + cellw - 1, y1], outline=INK, width=1, fill=(255, 255, 255))
        f_num = SANS_B(22)
        d.text((x0 + cellw / 2 - d.textlength(num, font=f_num) / 2, y0 + 2), num, font=f_num, fill=RED)
        for j, ll in enumerate(lab.split("\n")):
            f_lab = SANS(9)
            d.text((x0 + cellw / 2 - d.textlength(ll, font=f_lab) / 2, y0 + 25 + j * 10), ll, font=f_lab, fill=INK)

    # region strip
    y0, y1 = 158, 180
    x = MX
    d.rectangle([MX, y0, W - MX, y1], fill=INK)
    for name, cnt, col in REGIONS:
        lab = f"{name} {cnt}"
        f_r = SANS_B(11)
        tw = d.textlength(lab, font=f_r)
        d.rectangle([x + 2, y0 + 3, x + 2 + tw + 12, y1 - 3], fill=col)
        d.text((x + 8, y0 + 5), lab, font=f_r, fill=(255, 255, 255))
        x += tw + 18
    assert x <= W - MX, "region strip overflow"

    # UTC timeline strip
    y0, y1 = 184, 214
    d.rectangle([MX, y0, W - MX, y1], outline=INK, width=1, fill=LIGHT)
    f_utc = SANS_B(11)
    d.text((MX + 8, y0 + 3), "THE DAY IN UTC", font=f_utc, fill=RED)
    bx = MX + 118
    bw = (W - MX - bx) / 6
    for t, lab in UTC_BEATS:
        d.text((bx + 4, y0 + 3), t, font=SANS_B(11), fill=BLUE)
        # two-line label under time
        ll1, ll2 = lab.split("\n")
        d.text((bx + 44, y0 + 3), ll1, font=SANS(8), fill=INK)
        d.text((bx + 44, y0 + 13), ll2, font=SANS(8), fill=INK)
        bx += bw
    d.line([MX, y1, W - MX, y1], fill=RULE, width=1)

    # 3 lead cards
    lead_w = (CW - 20) / 3
    ly = 220
    scene_h = 176
    for i, st in enumerate(LEADS):
        x0 = MX + i * (lead_w + 10)
        x1 = x0 + lead_w
        d.rectangle([x0, ly, x1, ly + 266], outline=INK, width=1, fill=(255, 255, 255))
        SCENES[st["scene"]](d, x0 + 1, ly + 1, lead_w - 2, scene_h)
        chip(d, x0 + 7, ly + 7, st["kicker"], SANS_B(10), RED)
        chip(d, x1 - 7 - d.textlength(st["status"], font=SANS_B(9)) - 12, ly + 7,
             st["status"], SANS_B(9), STATUS_COLOR[st["status"]])
        hy = ly + scene_h + 8
        hl = wrap(d, f"{st['num']}. {st['head']}", SANS_B(14), lead_w - 14)
        assert len(hl) <= 2, f"lead {st['num']} headline {len(hl)} lines"
        draw_lines(d, hl, x0 + 7, hy, SANS_B(14), INK, lh=16, max_lines=2)
        sy = hy + len(hl) * 16 + 3
        sl = wrap(d, st["summ"], SANS(11), lead_w - 14)
        assert len(sl) <= 4, f"lead {st['num']} summary {len(sl)} lines"
        draw_lines(d, sl, x0 + 7, sy, SANS(11), INK, lh=13, max_lines=4)
        d.text((x0 + 7, ly + 266 - 13), st["src"], font=SANS(8), fill=GREY)

    # 10 small cards, 2 rows of 5
    small_w = (CW - 4 * 8) / 5
    for row in range(2):
        for col in range(5):
            st = SMALL[row * 5 + col]
            x0 = MX + col * (small_w + 8)
            y0 = 492 + row * 96
            y1 = y0 + 90
            d.rectangle([x0, y0, x0 + small_w, y1], outline=INK, width=1, fill=(255, 255, 255))
            SCENES[st["scene"]](d, x0 + 1, y0 + 1, small_w - 2, 40)
            chip(d, x0 + 5, y0 + 5, st["kicker"], SANS_B(8), RED)
            chip(d, x0 + small_w - 5 - d.textlength(st["status"], font=SANS_B(7)) - 10, y0 + 5,
                 st["status"], SANS_B(7), STATUS_COLOR[st["status"]])
            hl = wrap(d, f"{st['num']}. {st['head']}", SANS_B(11), small_w - 10)
            assert len(hl) <= 2, f"small {st['num']} headline {len(hl)} lines"
            draw_lines(d, hl, x0 + 5, y0 + 43, SANS_B(11), INK, lh=11, max_lines=2)
            sl = wrap(d, st["summ"], SANS(9), small_w - 10)
            assert len(sl) <= 2, f"small {st['num']} summary {len(sl)} lines"
            draw_lines(d, sl, x0 + 5, y0 + 43 + len(hl) * 11 + 2, SANS(9), INK, lh=10, max_lines=2)

    # dotted world map with numbered pins
    map_y0, map_y1 = 692, 788
    d.text((MX, map_y0), "THE WORLD, PINNED  —  numbered to the stories above", font=SANS_B(11), fill=INK)
    d.line([MX, map_y0 + 15, W - MX, map_y0 + 15], fill=RULE, width=1)
    my0, my1 = map_y0 + 18, map_y1
    rows = len(MAP_ROWS)
    cols = len(MAP_ROWS[0])
    cw = CW / cols
    ch = (my1 - my0) / rows
    for r, line in enumerate(MAP_ROWS):
        for c, ch2 in enumerate(line):
            if ch2 == "X":
                cx = MX + (c + 0.5) * cw
                cy = my0 + (r + 0.5) * ch
                d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=MAPDOT)
    for num, fx, fy in PINS:
        px = MX + fx * CW
        py = my0 + fy * (my1 - my0)
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255), width=1)
        t = str(num)
        d.text((px - d.textlength(t, font=SANS_B(9)) / 2, py - 5), t, font=SANS_B(9), fill=(255, 255, 255))

    # wire list: 23 more stories, 2 columns
    wy = 796
    d.text((MX, wy), "ALSO ON MONDAY 23 NOVEMBER — 23 MORE STORIES", font=SANS_B(12), fill=RED)
    d.line([MX, wy + 15, W - MX, wy + 15], fill=RULE, width=1)
    colw = (CW - 16) / 2
    for i, (num, region, text) in enumerate(WIRE):
        col = i % 2
        rowi = i // 2
        x0 = MX + col * (colw + 16)
        yy = wy + 20 + rowi * 10
        line = f"{num}. {text}"
        assert d.textlength(line, font=SANS(9)) <= colw, f"wire {num} too wide"
        d.text((x0, yy), line, font=SANS(9), fill=INK)

    # DATE CHECK box + certainty legend
    dy = 934
    d.rectangle([MX, dy, W - MX, 990], outline=RED, width=2, fill=(255, 250, 248))
    d.text((MX + 8, dy + 4), "DATE CHECK — what was deliberately left out, and why", font=SANS_B(10), fill=RED)
    dc_items = [
        "Anthropic's debut was Thu 19 Nov — only the market fallout is Monday's news.",
        "COP31 collapsed Sun 22 Nov; the reactions and suspension are Monday's story.",
        "The Indonesia fire broke out Sat 21 Nov; the search and toll are Monday's news.",
        "The Sparta II was struck Sat 22 Nov; it was still burning off Finland on Monday.",
        "The Bahrain strike was Sat 21 Nov; the wounded toll came Sunday–Monday.",
        "'El Chapo Isidro' was captured Sun 22 Nov; the fallout is Monday's news.",
    ]
    for i, item in enumerate(dc_items):
        col = i % 2
        rowi = i // 2
        x0 = MX + 8 + col * ((CW - 16) / 2)
        yy = dy + 19 + rowi * 11
        assert d.textlength(item, font=SANS(9)) <= (CW - 16) / 2 - 8, f"datecheck {i} too wide"
        d.text((x0, yy), "· " + item, font=SANS(9), fill=INK)
    d.text((MX, 993), "REPORTED = confirmed by wire agencies   ·   CLAIM = one side's claim, unverified   ·   ONGOING = still developing",
           font=SANS_B(9), fill=GREY)

    # footer
    d.line([MX, 1006, W - MX, 1006], fill=RULE, width=1)
    d.text((MX, 1010), "THE WORLD IN ONE DAY — Monday 23 November 2026  ·  36 stories  ·  7 regions  ·  Sources: Reuters, AFP, Al Jazeera, AP, BBC",
           font=SANS(9), fill=GREY)

    # layout assertions
    assert len(LEADS) + len(SMALL) + len(WIRE) == 36
    assert sum(c for _, c, _ in REGIONS) == 36
    assert len(KEYS) == 6 and len(UTC_BEATS) == 6
    img.save(path, "PNG", optimize=True)
    return path

def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    render(out)
    print("wrote", out, os.path.getsize(out), "bytes")

if __name__ == "__main__":
    main()

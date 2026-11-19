#!/usr/bin/env python3
"""THE WORLD IN ONE PAGE — Thursday, November 19, 2026.

Deterministic, offline front-page generator for the make.fun competition
news-image-20261119 ("Sum up 19 November's world news in one image").

Running `python3 main.py` writes `frontpage.png` (1024x1024) into the
working directory. No network, no randomness, no wall-clock reads: the
same code always produces the same image.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 36
CONTENT_W = W - 2 * MARGIN  # 952

PAPER = (247, 242, 231)
INK = (22, 20, 18)
FAINT = (120, 112, 98)
RULE = (40, 36, 30)

# ---------------------------------------------------------------------------
# Fonts ( Liberation -> DejaVu -> PIL default fallback chain )
# ---------------------------------------------------------------------------

FONT_DIRS = [
    "/usr/share/fonts/truetype/liberation",
    "/usr/share/fonts/truetype/dejavu",
]


def load_font(names, size):
    for name in names:
        for d in FONT_DIRS:
            path = os.path.join(d, name)
            if os.path.exists(path):
                return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def serif_bold(size):
    return load_font(["LiberationSerif-Bold.ttf", "DejaVuSerif-Bold.ttf"], size)


def serif_reg(size):
    return load_font(["LiberationSerif-Regular.ttf", "DejaVuSerif.ttf"], size)


def serif_italic(size):
    return load_font(["LiberationSerif-Italic.ttf", "DejaVuSerif-Italic.ttf"], size)


def sans(size):
    return load_font(["LiberationSans-Regular.ttf", "DejaVuSans.ttf"], size)


def sans_bold(size):
    return load_font(["LiberationSans-Bold.ttf", "DejaVuSans-Bold.ttf"], size)


# ---------------------------------------------------------------------------
# Text helpers
# ---------------------------------------------------------------------------


def wrap(draw, text, font, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, font, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------------------
# Hero artwork: a Vice-style sunset drawn entirely with PIL primitives
# ---------------------------------------------------------------------------


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


SKY_STOPS = [
    (0.00, (26, 5, 51)),      # deep indigo
    (0.35, (91, 29, 116)),    # purple
    (0.62, (200, 60, 130)),   # magenta pink
    (0.82, (255, 110, 90)),   # coral
    (1.00, (254, 180, 123)),  # horizon glow
]


def sky_color(t):
    for i in range(len(SKY_STOPS) - 1):
        t0, c0 = SKY_STOPS[i]
        t1, c1 = SKY_STOPS[i + 1]
        if t0 <= t <= t1:
            return lerp(c0, c1, (t - t0) / (t1 - t0))
    return SKY_STOPS[-1][1]


def draw_palm(draw, base_x, base_y, height, lean, scale=1.0):
    """Silhouette palm: curved trunk + drooping fronds."""
    col = (18, 6, 34)
    top_x = base_x + lean
    top_y = base_y - height
    # trunk as a tapering series of segments
    steps = 14
    for i in range(steps):
        t0, t1 = i / steps, (i + 1) / steps
        x0 = base_x + lean * (t0 * t0) + 6 * t0
        x1 = base_x + lean * (t1 * t1) + 6 * t1
        y0 = base_y - height * t0
        y1 = base_y - height * t1
        wdt = max(2, int((11 - 6 * t0) * scale))
        draw.line([x0, y0, x1, y1], fill=col, width=wdt)
    cx, cy = top_x + 6, top_y
    # coconuts
    draw.ellipse([cx - 7, cy - 2, cx + 3, cy + 8], fill=col)
    draw.ellipse([cx + 1, cy + 1, cx + 11, cy + 11], fill=col)
    # fronds: arcs drooping from the crown
    import math

    for ang_deg, length in [(-165, 86), (-130, 96), (-95, 88), (-60, 96),
                            (-25, 86), (5, 66), (-180, 62)]:
        ang = math.radians(ang_deg)
        pts = []
        segs = 12
        for i in range(segs + 1):
            t = i / segs
            x = cx + math.cos(ang) * length * t * scale
            y = cy + math.sin(ang) * length * t * scale + 34 * t * t * scale
            pts.append((x, y))
        draw.line(pts, fill=col, width=max(2, int(6 * scale)))


def draw_car(draw, cx, ground_y):
    """Low wedge sports-car silhouette with neon rims and underglow."""
    body = (14, 4, 26)
    pts = [
        (cx - 178, ground_y - 6),
        (cx - 168, ground_y - 26),
        (cx - 118, ground_y - 34),
        (cx - 74, ground_y - 56),
        (cx - 8, ground_y - 62),
        (cx + 62, ground_y - 58),
        (cx + 104, ground_y - 40),
        (cx + 158, ground_y - 30),
        (cx + 178, ground_y - 18),
        (cx + 178, ground_y - 6),
    ]
    draw.polygon(pts, fill=body)
    # canopy glass
    glass = [
        (cx - 62, ground_y - 55),
        (cx - 6, ground_y - 59),
        (cx + 48, ground_y - 55),
        (cx + 78, ground_y - 41),
        (cx - 84, ground_y - 41),
    ]
    draw.polygon(glass, fill=(52, 16, 74))
    # neon side stripe + underglow
    draw.line([cx - 170, ground_y - 14, cx + 170, ground_y - 14],
              fill=(255, 62, 150), width=3)
    draw.line([cx - 150, ground_y + 3, cx + 150, ground_y + 3],
              fill=(255, 62, 150), width=2)
    # wheels with teal rims
    for wx in (cx - 108, cx + 108):
        draw.ellipse([wx - 21, ground_y - 24, wx + 21, ground_y + 4], fill=(6, 2, 12))
        draw.ellipse([wx - 12, ground_y - 18, wx + 12, ground_y - 2],
                     outline=(45, 226, 230), width=3)


def draw_hero(img, x0, y0, x1, y1):
    draw = ImageDraw.Draw(img, "RGBA")
    horizon = y0 + int((y1 - y0) * 0.78)
    # sky gradient
    for yy in range(y0, horizon):
        t = (yy - y0) / max(1, (horizon - y0))
        draw.line([x0, yy, x1, yy], fill=sky_color(t))
    # retro sun with slice gaps, low over the horizon, right of centre
    sun_cx, sun_cy, sun_r = x1 - 235, horizon - 52, 104
    sun_top = sun_cy - sun_r
    for yy in range(sun_top, horizon):
        t = (yy - sun_top) / (2 * sun_r)
        col = lerp((255, 214, 120), (255, 84, 148), t)
        half = int((sun_r ** 2 - (yy - sun_cy) ** 2) ** 0.5)
        draw.line([sun_cx - half, yy, sun_cx + half, yy], fill=col)
    for i, gy in enumerate(range(horizon - 46, horizon, 11)):
        th = 2 + i
        t = (gy - y0) / max(1, (horizon - y0))
        draw.rectangle([sun_cx - sun_r, gy, sun_cx + sun_r, gy + th],
                       fill=sky_color(t))
    # distant skyline silhouette along the horizon
    sky = (22, 7, 40)
    towers = [(0, 26, 34), (34, 16, 52), (56, 30, 26), (92, 18, 44),
              (116, 24, 30), (640, 20, 40), (668, 30, 24), (706, 16, 48),
              (730, 26, 30), (762, 20, 36), (790, 28, 22), (824, 18, 42),
              (850, 24, 28), (882, 16, 38)]
    for off, wdt, hgt in towers:
        draw.rectangle([x0 + off, horizon - hgt, x0 + off + wdt, horizon], fill=sky)
    # sea / road band
    draw.rectangle([x0, horizon, x1, y1], fill=(13, 4, 26))
    # neon reflections on the wet ground
    for i, (off, ln, col) in enumerate([
            (60, 150, (255, 62, 150)), (250, 90, (45, 226, 230)),
            (430, 170, (255, 62, 150)), (660, 110, (45, 226, 230)),
            (810, 140, (255, 120, 90))]):
        yy = horizon + 12 + i * 11
        draw.line([x0 + off, yy, x0 + off + ln, yy], fill=col, width=2)
    # palms framing the scene
    draw_palm(draw, x0 + 54, y1, 200, 24, 1.0)
    draw_palm(draw, x1 - 48, y1, 176, -28, 0.9)
    # the car
    draw_car(draw, (x0 + x1) // 2 + 30, y1 - 14)
    # soft shade behind the headline for legibility (runs to the horizon line)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rectangle([x0, y0, x0 + 742, horizon], fill=(16, 2, 30, 96))
    img.paste(Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB"),
              (0, 0))
    draw = ImageDraw.Draw(img)
    # kicker + headline
    draw.text((x0 + 38, y0 + 28), "THE LAUNCH THE WORLD WAITED FOR",
              font=sans_bold(17), fill=(94, 234, 212))
    draw.text((x0 + 41, y0 + 55), "GTA VI IS HERE",
              font=serif_bold(88), fill=(30, 4, 40))
    draw.text((x0 + 38, y0 + 52), "GTA VI IS HERE",
              font=serif_bold(88), fill=(255, 255, 255))
    draw.text((x0 + 40, y0 + 148),
              "Rockstar's return to Leonida — Lucia Caminos & Jason Duval",
              font=serif_italic(19), fill=(255, 214, 235))


# ---------------------------------------------------------------------------
# Story blocks
# ---------------------------------------------------------------------------

LABEL_COLORS = {
    "WORLD": (157, 44, 44),
    "POLITICS": (31, 78, 121),
    "TECH": (108, 52, 131),
    "SPACE": (176, 124, 16),
    "MARKETS": (30, 107, 82),
}

F_LABEL = None
F_HEAD = None
F_SUM = None


def story(draw, x, y, col_w, label, headline, summary):
    """Draw one story block; returns the y just below it."""
    draw.text((x, y), label, font=F_LABEL, fill=LABEL_COLORS[label])
    y += 14
    lines = wrap(draw, headline, F_HEAD, col_w)
    y = draw_lines(draw, x, y, lines, F_HEAD, INK, 20)
    y += 1
    lines = wrap(draw, summary, F_SUM, col_w)
    y = draw_lines(draw, x, y, lines, F_SUM, (52, 48, 42), 15)
    return y


# ---------------------------------------------------------------------------
# Page assembly
# ---------------------------------------------------------------------------


def main():
    global F_LABEL, F_HEAD, F_SUM
    F_LABEL = sans_bold(11)
    F_HEAD = serif_bold(18)
    F_SUM = sans(12)

    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # ---- masthead ------------------------------------------------------
    draw.line([MARGIN, 30, W - MARGIN, 30], fill=RULE, width=3)
    draw.line([MARGIN, 37, W - MARGIN, 37], fill=RULE, width=1)
    title = "THE WORLD IN ONE PAGE"
    tf = serif_bold(57)
    tw = draw.textlength(title, font=tf)
    draw.text(((W - tw) / 2, 46), title, font=tf, fill=INK)
    draw.text((MARGIN, 118), "Vol. I — No. 19", font=sans_bold(13), fill=FAINT)
    date = "THURSDAY, NOVEMBER 19, 2026"
    df = sans_bold(15)
    dw = draw.textlength(date, font=df)
    draw.text(((W - dw) / 2, 116), date, font=df, fill=INK)
    tag = "One page · The whole planet"
    gw = draw.textlength(tag, font=sans_bold(13))
    draw.text((W - MARGIN - gw, 118), tag, font=sans_bold(13), fill=FAINT)
    draw.line([MARGIN, 140, W - MARGIN, 140], fill=RULE, width=1)
    draw.rectangle([MARGIN, 144, W - MARGIN, 148], fill=RULE)

    # ---- hero ----------------------------------------------------------
    hero_y0, hero_y1 = 158, 430
    draw_hero(img, MARGIN, hero_y0, W - MARGIN, hero_y1)
    draw = ImageDraw.Draw(img)
    draw.rectangle([MARGIN, hero_y0, W - MARGIN, hero_y1], outline=(24, 10, 36), width=2)

    deck = ("Rolling out at midnight local time — New Zealand first — as fans book days off work "
            "to play. On PS5 and Xbox Series X|S at $79.99, with 147 reviews averaging a Metacritic 99.")
    lines = wrap(draw, deck, serif_italic(17), CONTENT_W)
    draw_lines(draw, MARGIN, 439, lines, serif_italic(17), (52, 48, 42), 20)

    # ---- Voyager strip --------------------------------------------------
    strip_y0, strip_y1 = 486, 550
    draw.rectangle([MARGIN, strip_y0, W - MARGIN, strip_y1], fill=(18, 22, 58))
    draw.rectangle([MARGIN + 18, strip_y0 + 8, MARGIN + 26, strip_y0 + 16], fill=(240, 192, 64))
    draw.text((MARGIN + 33, strip_y0 + 5), "SPACE", font=sans_bold(11), fill=(240, 192, 64))
    draw.text((MARGIN + 18, strip_y0 + 20),
              "VOYAGER 1 REACHES ONE LIGHT-DAY FROM EARTH",
              font=serif_bold(20), fill=(255, 255, 255))
    draw.text((MARGIN + 18, strip_y0 + 44),
              "Humanity's first object that far out — its radio signal now takes ~24 hours to reach home. NASA confirmation expected today.",
              font=sans(12), fill=(205, 212, 240))

    # ---- columns ---------------------------------------------------------
    col_top = 564
    col_bot = 948
    col_w = 302
    col_x = [MARGIN, MARGIN + 325, MARGIN + 650]
    headers = ["THE WORLD", "CONFLICT & POLITICS", "TECH & MONEY"]
    for x, htxt in zip(col_x, headers):
        draw.text((x, col_top), htxt, font=sans_bold(13), fill=INK)
        draw.line([x, col_top + 19, x + col_w, col_top + 19], fill=RULE, width=2)
    for gx in (MARGIN + 313, MARGIN + 638):
        draw.line([gx, col_top, gx, col_bot], fill=(196, 188, 168), width=1)

    columns = [
        [
            ("WORLD", "TRUMP, XI, PUTIN IN FIRST TRILATERAL",
             "First US–China–Russia talks, at APEC in Shenzhen; a Trump–Putin one-on-one follows today."),
            ("WORLD", "US–IRAN FIRE FIGHT WIDENS",
             "US hits a Qeshm Island missile site; Iran strikes bases in Kuwait and Bahrain; three US carriers in region."),
            ("WORLD", "WORLD COURT RULES ON MYANMAR CASE",
             "The ICJ delivers its judgment today in The Gambia's genocide case over the Rohingya."),
            ("WORLD", "MOSCOW: FRANCE CROSSES RED LINE",
             "Lavrov accuses France of crossing a red line by deploying troops to Ukraine."),
        ],
        [
            ("POLITICS", "PELTOLA WINS ALASKA — SENATE 56–44",
             "Democrats seal their biggest Senate gain in nearly 70 years."),
            ("WORLD", "ISRAELI FORCES ENTER CENTRAL GAZA",
             "Ground troops advance after evacuation orders to residents."),
            ("WORLD", "CYCLONE AKVAN NEARS INDIA LANDFALL",
             "Landfall expected between Machilipatnam and Puri."),
            ("TECH", "AI CYBER THREATS OUTPACE DEFENCES",
             "AI-enabled attacks race ahead of defences; the NSA's classified network suffers an outage."),
        ],
        [
            ("TECH", "NVIDIA IN TURMOIL AS HUANG RESIGNS",
             "Founder Jensen Huang steps down; acting CEO Colette Kress vows earlier raises and more stock; H-series shipments to mainland China halted."),
            ("MARKETS", "EU PROPOSES €45BN LOAN FOR UKRAINE",
             "Brussels' plan would be repaid only once Russia pays reparations for the war."),
            ("MARKETS", "FED MINUTES POINT TO MORE HIKES",
             "Most officials expect further rate increases to bring inflation back to 2%."),
        ],
    ]

    for x, stories in zip(col_x, columns):
        y = col_top + 28
        for i, (label, head, summ) in enumerate(stories):
            if i > 0:
                draw.line([x, y - 6, x + col_w, y - 6], fill=(206, 198, 178), width=1)
            y = story(draw, x, y, col_w, label, head, summ)
            y += 13

    # ---- footer ticker ----------------------------------------------------
    foot_y0 = 956
    draw.rectangle([MARGIN, foot_y0, W - MARGIN, 1002], fill=INK)
    draw.text((MARGIN + 16, foot_y0 + 9), "ALSO TODAY", font=sans_bold(12), fill=(240, 192, 64))
    ticker = ("Australia sanctions Israeli settlers and West Bank groups; Albanese pictured with Putin at APEC as Trump "
              "hails his “friend” at the Quad  ·  Ted Lieu elected House Democratic Caucus chair, a first for a Taiwanese "
              "American  ·  Iraq jails six French ISIL members for life")
    lines = wrap(draw, ticker, sans(11), CONTENT_W - 130)
    draw_lines(draw, MARGIN + 118, foot_y0 + 8, lines, sans(11), (238, 234, 222), 15)

    img.save("frontpage.png", optimize=True)
    print("wrote frontpage.png", os.path.getsize("frontpage.png"), "bytes")


if __name__ == "__main__":
    main()

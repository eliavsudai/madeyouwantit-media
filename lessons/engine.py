"""MADE YOU WANT IT — lesson Reel engine (new campaign, Oct 27, 2026).

python3 engine.py <scenarios.json> <scenario_id> [test t1 t2 ...]
Cream / ink / red studio identity, animated diagrams, AI voice (Kokoro af_heart), karaoke captions.
"""
import os, sys, json, math, re, subprocess, numpy as np
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude/myw")
from design import font, text_w, draw_text, logo_bug

W, H, FPS = 1080, 1920, 30
CREAM = (243, 237, 226)
CREAM2 = (234, 226, 211)
INK = (20, 18, 16)
RED = (214, 38, 30)
GREY = (150, 142, 130)
VOICE, SPEED = "af_heart", 0.92
KOKORO = ("/home/claude/tts/kokoro-v1.0.onnx", "/home/claude/tts/voices-v1.0.bin")
WORK_DIR = "/home/claude/lessons/work"          # stills of our own published Reels


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def eout(x):
    x = clamp(x); return 1 - (1 - x) ** 3


def einout(x):
    x = clamp(x); return 3 * x * x - 2 * x * x * x


def lerp(a, b, k):
    return a + (b - a) * k


def rgba(c, a=1.0):
    return tuple(c) + (int(255 * clamp(a)),)


# ---------------- text helpers ----------------
def parse_marked(s):
    """'Shares *decide* reach' -> [('Shares',False),('decide',True),('reach',False)]"""
    out = []
    for tok in s.split():
        hl = tok.startswith("*") or tok.rstrip(".,!?:;'\"").endswith("*")
        out.append((tok.replace("*", ""), hl))
    return out


def rich_line(d, x, y, words, f, col=INK, hl=RED, alpha=1.0, anchor="m", tracking=0):
    total = sum(text_w(w, f, tracking) for w, _ in words) + f.getlength(" ") * (len(words) - 1)
    if anchor == "m":
        x = x - total / 2
    for w, h in words:
        draw_text(d, (x, y), w, f, rgba(hl if h else col, alpha), tracking=tracking)
        x += text_w(w, f, tracking) + f.getlength(" ")
    return total


def wrap_marked(s, f, maxw):
    words = parse_marked(s)
    lines, cur = [], []
    for w in words:
        test = cur + [w]
        if cur and sum(f.getlength(x) for x, _ in test) + f.getlength(" ") * (len(test) - 1) > maxw:
            lines.append(cur); cur = [w]
        else:
            cur = test
    if cur:
        lines.append(cur)
    return lines


# ---------------- background ----------------
def make_bg():
    rng = np.random.default_rng(2)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    g = 1 + 0.035 * np.exp(-(((xx - 540) / 800) ** 2 + ((yy - 700) / 1100) ** 2)) - 0.04 * (yy / H)
    a = np.array(CREAM, np.float32)[None, None] * g[..., None] + rng.normal(0, 2.2, (H, W, 1))
    return Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert("RGBA")


BG = None


def shadow_paste(base, im, x, y, blur=22, alpha=70, dy=18):
    a = im.getchannel("A").point(lambda v: v * alpha // 255)
    sh = Image.new("RGBA", im.size, (40, 30, 20, 0)); sh.putalpha(a)
    pad = blur * 3
    big = Image.new("RGBA", (im.width + pad * 2, im.height + pad * 2), (0, 0, 0, 0))
    big.alpha_composite(sh, (pad, pad))
    big = big.filter(ImageFilter.GaussianBlur(blur))
    base.alpha_composite(big, (int(x - pad), int(y - pad + dy)))
    base.alpha_composite(im, (int(x), int(y)))


# ---------------- icons ----------------
def icon(kind, s, col=INK, width=None):
    S = s * 4
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    w = width or max(4, int(S * 0.075))
    c = rgba(col)
    if kind == "heart":
        r = S * 0.2
        pts = []
        for i in range(181):
            t = i / 180 * 2 * math.pi
            x = 16 * math.sin(t) ** 3
            y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
            pts.append((S / 2 + x * S / 38, S / 2 + y * S / 38))
        d.line(pts + [pts[0]], fill=c, width=w, joint="curve")
    elif kind == "comment":
        d.ellipse((S * 0.12, S * 0.14, S * 0.88, S * 0.82), outline=c, width=w)
        d.polygon([(S * 0.2, S * 0.68), (S * 0.12, S * 0.9), (S * 0.36, S * 0.79)], fill=c)
    elif kind == "send":
        p = [(S * 0.1, S * 0.45), (S * 0.9, S * 0.12), (S * 0.6, S * 0.9), (S * 0.45, S * 0.56)]
        d.line(p + [p[0]], fill=c, width=w, joint="curve")
        d.line([(S * 0.45, S * 0.56), (S * 0.9, S * 0.12)], fill=c, width=w)
    elif kind == "save":
        p = [(S * 0.24, S * 0.1), (S * 0.76, S * 0.1), (S * 0.76, S * 0.9), (S * 0.5, S * 0.68), (S * 0.24, S * 0.9)]
        d.line(p + [p[0]], fill=c, width=w, joint="curve")
    elif kind == "eye":
        d.ellipse((S * 0.08, S * 0.28, S * 0.92, S * 0.72), outline=c, width=w)
        d.ellipse((S * 0.38, S * 0.38, S * 0.62, S * 0.62), fill=c)
    elif kind == "play":
        d.polygon([(S * 0.28, S * 0.18), (S * 0.82, S * 0.5), (S * 0.28, S * 0.82)], outline=c, width=w)
    elif kind == "check":
        d.line([(S * 0.18, S * 0.52), (S * 0.42, S * 0.76), (S * 0.84, S * 0.24)], fill=c, width=int(w * 1.4), joint="curve")
    elif kind == "x":
        d.line([(S * 0.22, S * 0.22), (S * 0.78, S * 0.78)], fill=c, width=int(w * 1.4))
        d.line([(S * 0.78, S * 0.22), (S * 0.22, S * 0.78)], fill=c, width=int(w * 1.4))
    elif kind == "user":
        d.ellipse((S * 0.34, S * 0.12, S * 0.66, S * 0.44), outline=c, width=w)
        d.arc((S * 0.16, S * 0.5, S * 0.84, S * 1.15), 180, 360, fill=c, width=w)
    elif kind == "clock":
        d.ellipse((S * 0.1, S * 0.1, S * 0.9, S * 0.9), outline=c, width=w)
        d.line([(S * 0.5, S * 0.5), (S * 0.5, S * 0.24)], fill=c, width=w)
        d.line([(S * 0.5, S * 0.5), (S * 0.68, S * 0.6)], fill=c, width=w)
    return im.resize((s, s), Image.LANCZOS)


# ---------------- phone + feed ----------------
PHONE_W, PHONE_H = 540, 1104
FEED_COLORS = [(214, 196, 170), (190, 205, 200), (226, 205, 190), (200, 196, 214), (220, 214, 180), (196, 186, 176)]


def phone_frame(w=PHONE_W, h=PHONE_H):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), int(w * 0.13), fill=(18, 17, 16, 255))
    return im


def phone_with(screen, w=PHONE_W, h=PHONE_H):
    im = phone_frame(w, h)
    m = int(w * 0.035)
    sw, shh = w - 2 * m, h - 2 * m
    scr = screen.resize((sw, shh), Image.LANCZOS) if screen.size != (sw, shh) else screen
    mask = Image.new("L", (sw, shh), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, sw - 1, shh - 1), int(w * 0.105), fill=255)
    im.paste(scr, (m, m), mask)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((w / 2 - 55, m + 14, w / 2 + 55, m + 44), 15, fill=(18, 17, 16, 255))
    return im


def screen_size(w=PHONE_W, h=PHONE_H):
    m = int(w * 0.035)
    return w - 2 * m, h - 2 * m


def feed_screen(offset, highlight=None, labels=None, stop_card=None, seed=0):
    sw, sh = screen_size()
    im = Image.new("RGBA", (sw, sh), (250, 248, 244, 255))
    d = ImageDraw.Draw(im)
    card_h = 560
    rng = np.random.default_rng(seed)
    k0 = int(offset // card_h) - 1
    for k in range(k0, k0 + 4):
        y = k * card_h - offset + 90
        col = FEED_COLORS[k % len(FEED_COLORS)]
        d.ellipse((24, y + 10, 64, y + 50), fill=(205, 198, 188, 255))
        d.rounded_rectangle((76, y + 20, 76 + 120 + (k * 37) % 90, y + 40), 10, fill=(215, 208, 198, 255))
        d.rectangle((0, y + 62, sw, y + 62 + 400), fill=col + (255,))
        # abstract shapes inside the post (no brands)
        cx = 80 + (k * 113) % (sw - 160)
        d.ellipse((cx, y + 150, cx + 130, y + 280), fill=tuple(int(c * 0.88) for c in col) + (255,))
        d.rounded_rectangle((40, y + 330, sw - 160, y + 345), 7, fill=tuple(int(c * 0.82) for c in col) + (255,))
        if labels and k in labels:
            f = font("anton", 64)
            txt = labels[k]
            draw_text(d, (sw / 2, y + 250), txt, f, rgba(INK), anchor="ms")
        if stop_card is not None and k == stop_card:
            d.rectangle((0, y + 62, sw, y + 462), outline=rgba(RED), width=8)
        for j, ic in enumerate(["heart", "comment", "send"]):
            im.alpha_composite(icon(ic, 34, (60, 56, 52)), (22 + j * 56, int(y + 478)))
        im.alpha_composite(icon("save", 34, (60, 56, 52)), (sw - 58, int(y + 478)))
    d.rectangle((0, 0, sw, 84), fill=(250, 248, 244, 255))
    d.line((0, 84, sw, 84), fill=(225, 220, 212, 255), width=2)
    return im


# ---------------- scenes ----------------
def headline_block(d, cx, y, text, size, maxw, color=INK, alpha=1.0, fname="anton", lead=1.02):
    f = font(fname, size)
    while True:
        lines = wrap_marked(text.upper() if fname == "anton" else text, f, maxw)
        if len(lines) <= 4 or size < 60:
            break
        size -= 6; f = font(fname, size)
    for i, ln in enumerate(lines):
        rich_line(d, cx, y + i * size * lead, ln, f, col=color, alpha=alpha)
    return y + (len(lines) - 1) * size * lead


def label(d, x, y, text, col=RED, alpha=1.0, size=34, anchor="ms"):
    draw_text(d, (x, y), text.upper(), font("inter_sb", size), rgba(col, alpha), tracking=7, anchor=anchor)


def sc_hook(img, p, lt, step, dur):
    d = ImageDraw.Draw(img)
    label(d, 540, 520, p["label"], RED)
    d.line((470, 556, 610, 556), fill=rgba(RED), width=4)
    size = p.get("size", 150)
    headline_block(d, 540, 700, p["headline"], size, 940)
    if p.get("sub"):
        f = font("inter_m", 46)
        draw_text(d, (540, 1270), p["sub"], f, rgba(GREY), anchor="ms")


def sc_statement(img, p, lt, step, dur):
    d = ImageDraw.Draw(img)
    a = eout(lt / 0.35)
    if p.get("label"):
        label(d, 540, 520, p["label"], RED, a)
    fname = p.get("font", "serif")
    size = p.get("size", 120 if fname == "serif" else 140)
    headline_block(d, 540, 700 + (1 - a) * 30, p["text"], size, 940, alpha=a, fname=fname, lead=1.08)
    if p.get("sub"):
        draw_text(d, (540, 1290), p["sub"], font("inter_m", 44), rgba(GREY, a), anchor="ms")


def sc_icons(img, p, lt, step, dur):
    """Engagement row. p: highlight (icon name), names (optional caption under each), note."""
    d = ImageDraw.Draw(img)
    kinds = p.get("kinds", ["heart", "comment", "send", "save"])
    names = p.get("names", {"heart": "likes", "comment": "comments", "send": "sends", "save": "saves"})
    hl = p.get("highlight")
    n = len(kinds)
    gap = 230 if n >= 4 else (300 if n == 3 else 420)
    x0 = 540 - gap * (n - 1) / 2
    for i, k in enumerate(kinds):
        a = eout((lt - i * 0.08) / 0.35)
        on = (k == hl) and lt > p.get("hl_at", 0.6)
        kk = eout((lt - p.get("hl_at", 0.6)) / 0.35) if on else 0
        s = int(160 * (1 + 0.3 * kk))
        col = RED if on else (INK if not hl or not lt > p.get("hl_at", 0.6) else (190, 182, 170))
        ic = icon(k, s, col)
        ic.putalpha(ic.getchannel("A").point(lambda v: int(v * a)))
        img.alpha_composite(ic, (int(x0 + i * gap - s / 2), int(820 - s / 2)))
        for li, part in enumerate(names.get(k, k).upper().split(" / ")):
            draw_text(d, (x0 + i * gap, 1010 + li * 44), part if li == 0 else "/ " + part, font("inter_sb", 34), rgba(col, a), tracking=3, anchor="ms")
    if p.get("title"):
        headline_block(d, 540, 560, p["title"], p.get("title_size", 96), 960, alpha=eout(lt / 0.35))
    if p.get("note"):
        draw_text(d, (540, 1180), p["note"], font("inter_m", 40), rgba(GREY, eout((lt - 0.8) / 0.4)), anchor="ms")


def sc_feed(img, p, lt, step, dur):
    """Phone feed scrolling; optionally stops on a card. p: stop_at (s), stop_card, labels{k:txt}, side_text."""
    stop_at = p.get("stop_at", None)
    speed = p.get("speed", 900)
    if stop_at is None or lt < stop_at:
        off = lt * speed
    else:
        target = p.get("stop_card", 3) * 560 - 90 + 0
        o0 = stop_at * speed
        off = lerp(o0, max(o0, target), eout((lt - stop_at) / 0.5))
    labels = {int(k): v for k, v in p.get("labels", {}).items()}
    scr = feed_screen(off, labels=labels, stop_card=p.get("stop_card") if stop_at is not None and lt > stop_at + 0.3 else None)
    ph = phone_with(scr)
    x = 540 - PHONE_W / 2 + p.get("dx", 0)
    shadow_paste(img, ph, x, 330)
    if p.get("side_text"):
        d = ImageDraw.Draw(img)
        a = eout((lt - p.get("side_at", 0.3)) / 0.35)
        headline_block(d, 540, 330, p["side_text"], 70, 980, alpha=a)


def sc_curve(img, p, lt, step, dur):
    """Retention curve. p: pts [[x,y],...] x in seconds, y in %, xmax, marks [{x, label}], title, note."""
    d = ImageDraw.Draw(img)
    X0, Y0, X1, Y1 = 150, 520, 980, 1260
    a = eout(lt / 0.3)
    d.line((X0, Y1, X1, Y1), fill=rgba(INK, a), width=4)
    d.line((X0, Y0, X0, Y1), fill=rgba(INK, a), width=4)
    fl = font("inter_m", 38)
    draw_text(d, (X0 - 20, Y0 + 12), "100%", fl, rgba(GREY, a), anchor="rs")
    draw_text(d, (X0 - 20, Y1), "0", fl, rgba(GREY, a), anchor="rs")
    xmax = p.get("xmax", 30)
    for s in p.get("ticks", [0, 3, 10, 20, 30]):
        x = X0 + (X1 - X0) * s / xmax
        d.line((x, Y1, x, Y1 + 14), fill=rgba(INK, a), width=3)
        draw_text(d, (x, Y1 + 56), f"{s}s", fl, rgba(GREY, a), anchor="ms")
    curves = p.get("curves") or [{"pts": p["pts"], "color": "red"}]
    k = clamp((lt - 0.3) / p.get("draw", 1.6))
    for cv in curves:
        pts = cv["pts"]
        xs = np.linspace(0, pts[-1][0], 200)
        ys = np.interp(xs, [q[0] for q in pts], [q[1] for q in pts])
        n = max(2, int(200 * k))
        line = [(X0 + (X1 - X0) * xs[i] / xmax, Y1 - (Y1 - Y0) * ys[i] / 100) for i in range(n)]
        col = RED if cv.get("color") == "red" else INK
        d.line(line, fill=rgba(col), width=9, joint="curve")
        if cv.get("label") and k > 0.95:
            lx, ly = line[-1]
            draw_text(d, (lx + 14, ly - 10), cv["label"], font("inter_sb", 34), rgba(col), anchor="ls")
    for m in p.get("marks", []):
        ma = eout((lt - m.get("at", 1.0)) / 0.3)
        if ma <= 0:
            continue
        x = X0 + (X1 - X0) * m["x"] / xmax
        for yy in range(Y0, Y1, 26):
            d.line((x, yy, x, yy + 13), fill=rgba(RED, ma), width=3)
        draw_text(d, (x, Y0 - 24), m["label"], font("inter_sb", 36), rgba(RED, ma), anchor="ms")
    if p.get("title"):
        headline_block(d, 540, 420, p["title"], 76, 960, alpha=a)
    draw_text(d, (X1, Y1 + 110), p.get("note", "Illustration"), font("inter_m", 30), rgba(GREY, a), anchor="rs")


def sc_counter(img, p, lt, step, dur):
    """Big number. p: from, to, prefix, suffix, decimals, label, icon, over (s)."""
    d = ImageDraw.Draw(img)
    k = eout(lt / p.get("over", 1.2))
    v = lerp(p.get("from", 0), p["to"], k)
    dec = p.get("decimals", 0)
    txt = f"{p.get('prefix', '')}{v:,.{dec}f}{p.get('suffix', '')}"
    f = font("anton", p.get("size", 330))
    draw_text(d, (540, 1000), txt, f, rgba(RED), anchor="ms")
    if p.get("icon"):
        ic = icon(p["icon"], 120, INK)
        img.alpha_composite(ic, (480, 540))
    if p.get("label"):
        headline_block(d, 540, 1140, p["label"], 64, 940, fname="inter_xb", lead=1.15)


def hook_card_screen(text, weak):
    sw, sh = screen_size()
    im = Image.new("RGBA", (sw, sh), (250, 248, 244, 255) if not weak else (236, 233, 228, 255))
    d = ImageDraw.Draw(im)
    if weak:
        f = font("inter_m", 46)
        lines = wrap_marked(text, f, sw - 70)
        for i, ln in enumerate(lines):
            rich_line(d, sw / 2, sh * 0.44 + i * 58, [(w, False) for w, _ in ln], f, col=(120, 114, 106))
    else:
        f = font("anton", 74)
        lines = wrap_marked(text.upper(), f, sw - 60)
        y0 = sh * 0.36
        for i, ln in enumerate(lines):
            rich_line(d, sw / 2, y0 + i * 78, ln, f, col=INK)
    return im


def sc_compare(img, p, lt, step, dur):
    """Two phones: weak vs strong. p: weak, strong, weak_label, strong_label, verdict_at."""
    d = ImageDraw.Draw(img)
    pw, phh = 400, 818
    for j, (key, lab, weak) in enumerate([("weak", p.get("weak_label", "WEAK"), True), ("strong", p.get("strong_label", "STRONG"), False)]):
        if not p.get(key):
            continue
        a = eout((lt - j * 0.25) / 0.4)
        if a <= 0:
            continue
        ph = phone_with(hook_card_screen(p[key], weak), pw, phh)
        if a < 1:
            ph.putalpha(ph.getchannel("A").point(lambda v: int(v * a)))
        x = 70 + j * 540 - (1 - a) * 0
        shadow_paste(img, ph, x, 470 + (1 - a) * 40, blur=18, alpha=60)
        draw_text(d, (x + pw / 2, 420), lab, font("inter_sb", 36), rgba(GREY if weak else RED, a), tracking=6, anchor="ms")
        va = eout((lt - p.get("verdict_at", 1.2) - j * 0.2) / 0.3)
        if va > 0:
            ic = icon("x" if weak else "check", 110, GREY if weak else RED)
            ic.putalpha(ic.getchannel("A").point(lambda v: int(v * va)))
            img.alpha_composite(ic, (int(x + pw / 2 - 55), int(470 + phh + 30)))


def sc_timeline(img, p, lt, step, dur):
    """A ruler 0..max seconds with a playhead; p: max, mark, mark_label, title."""
    d = ImageDraw.Draw(img)
    X0, X1, Y = 120, 960, 900
    mx = p.get("max", 10)
    a = eout(lt / 0.3)
    d.line((X0, Y, X1, Y), fill=rgba(INK, a), width=5)
    for s in range(0, int(mx) + 1):
        x = X0 + (X1 - X0) * s / mx
        hh = 26 if s % 5 == 0 else 14
        d.line((x, Y - hh, x, Y + hh), fill=rgba(INK, a), width=3)
        if s % p.get("label_every", 1) == 0:
            draw_text(d, (x, Y + 74), f"{s}s", font("inter_m", 38), rgba(GREY, a), anchor="ms")
    m = p.get("mark", 3)
    xm = X0 + (X1 - X0) * m / mx
    zone = eout((lt - 0.3) / 0.6)
    d.rectangle((X0, Y - 60, X0 + (xm - X0) * zone, Y - 34), fill=rgba(RED, 0.85))
    ph = X0 + (X1 - X0) * min(mx, (lt * p.get("play_speed", 1.0))) / mx
    d.line((ph, Y - 90, ph, Y + 40), fill=rgba(INK), width=4)
    if zone > 0.95 and p.get("mark_label"):
        draw_text(d, ((X0 + xm) / 2, Y - 92), p["mark_label"], font("inter_xb", 44), rgba(RED), anchor="ms")
    if p.get("title"):
        headline_block(d, 540, 560, p["title"], 96, 960, alpha=a)


def sc_list(img, p, lt, step, dur):
    """Numbered items revealed by step (one per spoken line) or by time. p: items, title, reveal: 'step'|'time'."""
    d = ImageDraw.Draw(img)
    a = eout(lt / 0.3)
    if p.get("title"):
        headline_block(d, 540, 470, p["title"], 84, 960, alpha=a)
    items = p["items"]
    for i, it in enumerate(items):
        shown = (i <= step) if p.get("reveal", "step") == "step" else (lt > 0.4 + i * p.get("every", 0.8))
        if not shown:
            continue
        ia = 1.0 if p.get("reveal", "step") == "step" and i < step else eout((lt - (0 if p.get("reveal", "step") == "step" else 0.4 + i * p.get("every", 0.8))) / 0.35)
        y = 660 + i * 200
        cur = (i == step) and p.get("reveal", "step") == "step"
        d.ellipse((90, y - 70, 186, y + 26), fill=rgba(RED if cur or p.get("reveal") == "time" else INK, ia))
        draw_text(d, (138, y + 4), str(i + 1), font("anton", 64), rgba((255, 255, 255), ia), anchor="ms")
        f = font("inter_xb", 62)
        lines = wrap_marked(it, f, 780)
        for j, ln in enumerate(lines[:2]):
            rich_line(d, 220, y - 4 + j * 72, ln, f, col=INK if cur or p.get("reveal") == "time" else (120, 112, 102), alpha=ia, anchor="l")


def sc_bars(img, p, lt, step, dur):
    """Horizontal bars. p: bars [{label, value, color}], unit, title, note, maxv."""
    d = ImageDraw.Draw(img)
    a = eout(lt / 0.3)
    if p.get("title"):
        headline_block(d, 540, 500, p["title"], 84, 960, alpha=a)
    bars = p["bars"]
    mx = p.get("maxv") or max(b["value"] for b in bars)
    for i, b in enumerate(bars):
        k = eout((lt - 0.3 - i * 0.25) / 0.8)
        y = 700 + i * 190
        draw_text(d, (120, y), b["label"], font("inter_sb", 40), rgba(INK, a), anchor="ls")
        L = 840 * b["value"] / mx * k
        col = RED if b.get("color") == "red" else INK
        d.rounded_rectangle((120, y + 24, 120 + max(20, L), y + 94), 14, fill=rgba(col, a))
        if k > 0.1:
            draw_text(d, (120 + max(20, L) + 18, y + 80), b.get("text", f"{b['value']:g}{p.get('unit', '')}"), font("anton", 64), rgba(col, k), anchor="ls")
    if p.get("note"):
        draw_text(d, (540, 700 + len(bars) * 190 + 40), p["note"], font("inter_m", 34), rgba(GREY, a), anchor="ms")


def sc_quote(img, p, lt, step, dur):
    """Source card: p: quote, who, role."""
    d = ImageDraw.Draw(img)
    a = eout(lt / 0.4)
    qs = p.get("size", 76)
    f = font("serif", qs)
    lines = wrap_marked(p["quote"], f, 800)
    ch = int(250 + len(lines) * qs * 1.18 + 150)
    card = Image.new("RGBA", (920, ch), (0, 0, 0, 0))
    cd = ImageDraw.Draw(card)
    cd.rounded_rectangle((0, 0, 919, ch - 1), 36, fill=(255, 253, 249, 255))
    cd.text((60, 150), "“", font=font("serif", 220), fill=rgba(RED), anchor="ls")
    for i, ln in enumerate(lines):
        rich_line(cd, 60, 250 + i * qs * 1.18, ln, f, col=INK, anchor="l")
    draw_text(cd, (60, ch - 90), p["who"].upper(), font("inter_sb", 34), rgba(RED), tracking=5, anchor="ls")
    if p.get("role"):
        draw_text(cd, (60, ch - 44), p["role"], font("inter_m", 32), rgba(GREY), anchor="ls")
    card.putalpha(card.getchannel("A").point(lambda v: int(v * a)))
    shadow_paste(img, card, 80, max(400, 860 - ch / 2) + (1 - a) * 30, alpha=int(60 * a))


@lru_cache(None)
def work_still(name):
    return Image.open(os.path.join(WORK_DIR, name)).convert("RGBA")


def sc_work(img, p, lt, step, dur):
    """Payoff: our own published Reels in phones. p: stills [file,...], title."""
    d = ImageDraw.Draw(img)
    stills = p.get("stills", sorted(os.listdir(WORK_DIR)))
    n = min(3, len(stills))
    pw, phh = 380, 776
    for i in range(n):
        a = eout((lt - i * 0.15) / 0.45)
        if a <= 0:
            continue
        ph = phone_with(work_still(stills[i]).resize(screen_size(pw, phh)), pw, phh)
        rot = (-6, 0, 6)[i] if n == 3 else 0
        ph = ph.rotate(rot, expand=True, resample=Image.BICUBIC)
        x = 540 - ph.width / 2 + (i - (n - 1) / 2) * 320
        y = 520 + (abs(i - (n - 1) / 2)) * 40 + (1 - a) * 60
        shadow_paste(img, ph, x, y, blur=18, alpha=int(60 * a))
    a = eout(lt / 0.35)
    label(d, 540, 440, p.get("title", "OUR WORK"), RED, a)


def sc_end(img, p, lt, step, dur):
    img.paste(Image.new("RGBA", (W, H), rgba(RED)), (0, 0))
    d = ImageDraw.Draw(img)
    k1 = eout(lt / 0.3)
    bug = logo_bug(170, bg=(255, 255, 255), fg=RED)
    img.alpha_composite(bug, (455, 420))
    draw_text(d, (540, 720), "MADE YOU WANT IT", font("anton", 104), rgba((255, 255, 255), k1), anchor="ms", tracking=4)
    draw_text(d, (540, 830), "Your product.", font("serif", 74), rgba((255, 255, 255), k1), anchor="ms")
    draw_text(d, (540, 915), "An account worth following.", font("serif", 74), rgba((255, 255, 255), k1), anchor="ms")
    k2 = eout((lt - 0.4) / 0.3)
    d.rounded_rectangle((150, 1030, 930, 1190), 80, fill=rgba((255, 255, 255), k2))
    draw_text(d, (540, 1135), "First ad free · DM “DAILY”", font("inter_xb", 52), rgba(RED, k2), anchor="ms")
    draw_text(d, (540, 1300), "@madeyouwantit.studio", font("inter_b", 44), rgba((255, 255, 255), eout((lt - 0.7) / 0.3)), anchor="ms")


SCENES = dict(hook=sc_hook, statement=sc_statement, icons=sc_icons, feed=sc_feed, curve=sc_curve, counter=sc_counter,
              compare=sc_compare, timeline=sc_timeline, list=sc_list, bars=sc_bars, quote=sc_quote, work=sc_work, end=sc_end)


# ---------------- build ----------------
class Reel:
    def __init__(self, sc, root):
        self.sc, self.root = sc, root
        os.makedirs(f"{root}/vo", exist_ok=True)
        self.lines = sc["lines"]

    def tts(self):
        meta_p = f"{self.root}/vo/meta.json"
        texts = [re.sub(r"\*", "", ln["say"]) for ln in self.lines]
        if os.path.exists(meta_p):
            m = json.load(open(meta_p))
            if [x["text"] for x in m] == texts:
                self.meta = m; return
        import soundfile as sf
        from kokoro_onnx import Kokoro
        k = Kokoro(*KOKORO)
        meta = []
        for i, t in enumerate(texts):
            s, sr = k.create(t, voice=VOICE, speed=SPEED, lang="en-us")
            a = np.abs(s); nz = np.where(a > 0.008)[0]; s = s[max(0, nz[0] - 200):nz[-1] + 600]
            f = f"{self.root}/vo/l{i:02d}.wav"; sf.write(f, s, sr)
            meta.append({"text": t, "dur": round(len(s) / sr, 3), "file": f})
        json.dump(meta, open(meta_p, "w"), indent=1)
        self.meta = meta

    def timeline(self):
        t = 0.25
        self.starts = []
        for i, ln in enumerate(self.lines):
            self.starts.append(t)
            gap = ln.get("pause", 0.32)
            if re.search(r"\d", ln["say"]):
                gap += 0.18                     # let numbers land
            t += self.meta[i]["dur"] + gap
        self.t_end = t + 0.1
        self.total = self.t_end + 2.6
        # scene groups: a line with "scene" starts a group; lines without continue it
        self.groups = []
        for i, ln in enumerate(self.lines):
            if "scene" in ln or i == 0:
                self.groups.append({"scene": ln.get("scene", {"kind": "hook"}), "start": self.starts[i] if i else 0.0, "first": i})
        for gi, g in enumerate(self.groups):
            g["end"] = self.groups[gi + 1]["start"] if gi + 1 < len(self.groups) else self.t_end
        # karaoke words
        self.words = []
        for i, ln in enumerate(self.lines):
            toks = parse_marked(ln["say"])
            wl = np.array([len(w) + 2 for w, _ in toks], float)
            cs = np.concatenate([[0], np.cumsum(wl)]) / wl.sum() * self.meta[i]["dur"]
            self.words.append([(self.starts[i] + cs[j], self.starts[i] + cs[j + 1], toks[j][0], toks[j][1]) for j in range(len(toks))])
        json.dump({"starts": self.starts, "end": self.t_end, "total": self.total,
                   "files": [m["file"] for m in self.meta]}, open(f"{self.root}/timeline.json", "w"), indent=1)

    def chunks(self, i):
        out, cur = [], []
        for w in self.words[i]:
            cur.append(w)
            if len(cur) >= 7 or (w[2].endswith((".", "?", "!", ":")) and len(cur) >= 2) or (w[2].endswith(",") and len(cur) >= 4):
                out.append(cur); cur = []
        if cur:
            if out and len(cur) <= 2 and len(out[-1]) + len(cur) <= 8:
                out[-1] += cur
            else:
                out.append(cur)
        return out

    def captions(self, img, t):
        for i in range(len(self.lines)):
            ws = self.words[i]
            nxt = self.starts[i + 1] if i + 1 < len(self.lines) else self.t_end
            if not (ws[0][0] - 0.05 <= t < min(nxt, ws[-1][1] + 0.6)):
                continue
            cl = self.chunks(i)
            for ci, ch in enumerate(cl):
                end = min(nxt, ch[-1][1] + 0.6) if ci == len(cl) - 1 else cl[ci + 1][0][0] - 0.03
                if ch[0][0] - 0.05 <= t < end:
                    self._draw_chunk(img, ch, t)
                    return

    def _draw_chunk(self, img, ch, t):
        size = 66
        f = font("inter_xb", size)
        text = " ".join(w[2] for w in ch)
        while text_w(text, f) > 930 and size > 44:
            size -= 2; f = font("inter_xb", size)
        lines = [ch]
        if text_w(text, f) > 930:
            mid = len(ch) // 2
            lines = [ch[:mid], ch[mid:]]
        d = ImageDraw.Draw(img)
        y0 = 1520 - (len(lines) - 1) * size * 0.6
        # soft cream plate for legibility over diagrams
        wmax = max(text_w(" ".join(w[2] for w in ln), f) for ln in lines)
        plate = Image.new("RGBA", (int(wmax + 80), int(len(lines) * size * 1.2 + 50)), rgba(CREAM, 0.0))
        pd = ImageDraw.Draw(plate)
        pd.rounded_rectangle((0, 0, plate.width - 1, plate.height - 1), 26, fill=rgba((255, 252, 246), 0.92))
        img.alpha_composite(plate, (int(540 - plate.width / 2), int(y0 - size * 0.95 - 10)))
        for li, ln in enumerate(lines):
            tw = text_w(" ".join(w[2] for w in ln), f)
            x = 540 - tw / 2
            y = y0 + li * size * 1.2
            for w in ln:
                said = t >= w[0]
                col = RED if (w[3] and said) else INK
                al = 1.0 if said or t < w[0] - 10 else 1.0
                d.text((x, y), w[2], font=f, fill=rgba(col, al), anchor="ls")
                if w[3] and said:
                    k = eout((t - w[0]) / 0.25)
                    d.line((x, y + 12, x + f.getlength(w[2]) * k, y + 12), fill=rgba(RED), width=6)
                x += f.getlength(w[2] + " ")

    def render(self, fi):
        global BG
        if BG is None:
            BG = make_bg()
        t = fi / FPS
        img = BG.copy()
        if t >= self.t_end:
            sc_end(img, {}, t - self.t_end, 0, 2.6)
            return img.convert("RGB")
        for g in self.groups:
            if g["start"] <= t < g["end"]:
                step = sum(1 for i, s in enumerate(self.starts) if s <= t and i >= g["first"]) - 1
                kind = g["scene"]["kind"]
                lt = t - g["start"]
                SCENES[kind](img, g["scene"], lt, max(0, step), g["end"] - g["start"])
                # quick cross-fade from previous scene for the first 0.18 s
                break
        # header: audience label + progress line (not on the hook)
        d = ImageDraw.Draw(img)
        on_end = any(g["scene"]["kind"] == "end" and g["start"] <= t for g in self.groups)
        if t >= self.groups[0]["end"] and not on_end:
            label(d, 540, 250, self.sc["audience"], GREY, 1.0, size=28)
        if not on_end:
            d.rectangle((0, 0, int(W * t / self.t_end), 10), fill=rgba(RED))
        self.captions(img, t)
        return img.convert("RGB")


def job(args):
    reel, fi = args
    p = f"{reel.root}/frames/{fi:05d}.jpg"
    if not os.path.exists(p):
        reel.render(fi).save(p, quality=92)


if __name__ == "__main__":
    scs = json.load(open(sys.argv[1]))
    sc = next(s for s in scs["scenarios"] if s["id"] == sys.argv[2])
    root = f"/home/claude/lessons/build/{sc['id']}"
    os.makedirs(f"{root}/frames", exist_ok=True)
    r = Reel(sc, root)
    r.tts(); r.timeline()
    P = "/tmp/claude-0/-home-claude/2371c677-845b-5e5d-a138-cf5eda76036b/scratchpad/"
    if len(sys.argv) > 3 and sys.argv[3] == "test":
        for tt in sys.argv[4:]:
            r.render(int(float(tt) * FPS)).save(f"{P}{sc['id']}_{tt}.jpg", quality=85)
        print(json.dumps({"starts": [round(s, 2) for s in r.starts], "end": round(r.t_end, 2), "total": round(r.total, 2)}))
    else:
        from multiprocessing import Pool
        N = int(r.total * FPS)
        with Pool(2) as pool:
            pool.map(job, [(r, i) for i in range(N)], chunksize=8)
        print("frames", N, "total", round(r.total, 2))

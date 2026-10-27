"""Retention Reel #1 — 'The Pin'. Silent tension, then the pitch, then the pop."""
import os, sys, json, math, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude/myw")
from design import font, text_w, draw_text, logo_bug, RED

W, H, FPS = 1080, 1920, 30
OUT = "/home/claude/r1/frames2"
os.makedirs(OUT, exist_ok=True)

# ---------------- timeline ----------------
_raw = json.load(open("/home/claude/r1/vo2/am_michael.json"))
_keep = [0, 2, 3, 4, 5, 6, 7, 8]
VO = [dict(_raw[k], file=f"/home/claude/r1/vo2/am_michael_{k:02d}.wav") for k in _keep]
D = [v["dur"] for v in VO]
STARTS = [4.0]
STARTS.append(STARTS[0] + D[0] + 0.3)
T_FAKE = STARTS[1] + D[1] + 0.15
STARTS.append(T_FAKE + 1.35)
STARTS.append(STARTS[2] + D[2] + 0.35)
STARTS.append(STARTS[3] + D[3] + 0.4)
STARTS.append(STARTS[4] + D[4] + 0.25)
STARTS.append(STARTS[5] + D[5] + 0.45)
T_TOUCH = STARTS[6] + D[6] + 0.3
T_POP = T_TOUCH + 0.45
STARTS.append(T_POP + 0.85)
T_END = STARTS[7] + D[7] + 0.35
TOTAL = T_END + 2.5
json.dump({"starts": STARTS, "fake": T_FAKE, "touch": T_TOUCH, "pop": T_POP, "end": T_END, "total": TOTAL,
           "files": [v["file"] for v in VO]}, open("/home/claude/r1/timeline2.json", "w"), indent=1)


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def eout(x):
    x = clamp(x); return 1 - (1 - x) ** 3


def einout(x):
    x = clamp(x); return 3 * x * x - 2 * x * x * x


# ---------------- world ----------------
BCX, BCY, RX, RY = 420.0, 860.0, 300.0, 350.0
YC = BCY - 0.2 * RY                                   # contact height
def surf_x(y):
    v = (y - BCY) / RY
    w = 1 - 0.15 * v
    return BCX + RX * w * math.sqrt(max(0, 1 - v * v))
XS = surf_x(YC)
PCONT = np.array([XS, YC])
G0 = 150.0                                            # gap after the entry (world px)
PX_PER_MM = 2.6
ANG = math.radians(6)
PIN_L = 280.0


def gap(t):
    if t >= T_TOUCH:
        return 0.0
    p = t / T_TOUCH
    return G0 * (1 - p) ** 1.35 + 200 * math.exp(-t / 0.42)


def lunge(t):
    tf = T_FAKE
    if t < tf or t > tf + 2.3:
        return 0.0
    A = gap(tf + 0.55) - 3.6
    if t < tf + 0.55:
        return A * eout((t - tf) / 0.55)
    if t < tf + 0.95:
        return A + 0.8 * math.sin((t - tf) * 40) * (t - tf - 0.55) / 0.4
    return A * (1 - einout((t - tf - 0.95) / 1.3))


def gap_eff(t):
    return gap(t) - lunge(t)


def dent(t):
    if t < T_TOUCH:
        return 0.0
    return 34.0 * clamp((t - T_TOUCH) / (T_POP - T_TOUCH)) ** 1.6


def camera(t):
    # push-in towards the contact point, then pull back after the pop
    p = clamp(t / T_TOUCH)
    k = p ** 1.7
    c = 0.94 + 1.4 * k
    cx = 650 + (XS + 10 - 650) * einout(p ** 0.9)
    cy = 930 + (YC - 930) * einout(p ** 0.9)
    if t >= T_POP:
        q = eout((t - T_POP - 0.05) / 0.9)
        c = c + (1.12 - c) * q
        cx = cx + (640 - cx) * q
        cy = cy + (960 - cy) * q
        sh = 16 * math.exp(-(t - T_POP) / 0.12) if t - T_POP < 0.6 else 0
        cx += sh * math.sin((t - T_POP) * 90)
        cy += sh * math.cos((t - T_POP) * 77)
    # handheld drift
    cx += 2.2 * math.sin(t * 0.9) + 1.3 * math.sin(t * 2.3 + 1)
    cy += 1.8 * math.sin(t * 0.7 + 2) + 1.1 * math.sin(t * 1.9)
    return c, cx, cy


def w2s(p, cam):
    c, cx, cy = cam
    return ((p[0] - cx) * c + W / 2, (p[1] - cy) * c + H / 2)


def cam_layer(img, S, ox, oy, cam, resample=Image.BICUBIC):
    c, cx, cy = cam
    a = S / c
    return img.transform((W, H), Image.AFFINE,
                         (a, 0, (-W / 2 / c + cx - ox) * S, 0, a, (-H / 2 / c + cy - oy) * S),
                         resample=resample)


# ---------------- sprites ----------------
def make_bg():
    S, ox, oy = 0.5, -400, -400
    w, h = int(1900 * S), int(2800 * S)
    ys, xs = np.mgrid[0:h, 0:w].astype(np.float32)
    X, Y = xs / S + ox, ys / S + oy
    d = np.sqrt(((X - 520) / 900) ** 2 + ((Y - 820) / 1100) ** 2)
    glow = np.exp(-d ** 2 * 1.6)
    base = np.array([10, 14, 17], np.float32)
    lit = np.array([46, 60, 66], np.float32)
    col = base[None, None] + (lit - base)[None, None] * glow[..., None]
    img = Image.fromarray(col.clip(0, 255).astype(np.uint8)).convert("RGBA")
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    dd = ImageDraw.Draw(lay)
    rng = np.random.default_rng(3)
    for _ in range(9):
        x, y = rng.uniform(-200, 1300), rng.uniform(-100, 2100)
        r = rng.uniform(40, 130)
        warm = rng.random() < 0.5
        colr = (255, 170, 110) if warm else (120, 200, 210)
        a = int(rng.uniform(10, 26))
        dd.ellipse(((x - ox - r) * S, (y - oy - r) * S, (x - ox + r) * S, (y - oy + r) * S), fill=colr + (a,))
    lay = lay.filter(ImageFilter.GaussianBlur(6))
    img.alpha_composite(lay)
    return img, S, ox, oy


def make_balloon():
    S, ox, oy = 2.5, BCX - 330.0, 490.0
    w, h = int(660 * S), int(1180 * S)
    ys, xs = np.mgrid[0:h, 0:w].astype(np.float32)
    X, Y = xs / S + ox, ys / S + oy
    u, v = (X - BCX) / RX, (Y - BCY) / RY
    wv = 1 - 0.15 * v
    uu = u / wv
    g = np.sqrt(uu ** 2 + v ** 2)
    alpha = np.clip((1 - g) * min(RX, RY) * S + 0.5, 0, 1)
    nz = np.sqrt(np.clip(1 - uu ** 2 - v ** 2, 0, 1))
    N = np.stack([uu, v, nz], -1)
    N /= np.linalg.norm(N, axis=-1, keepdims=True) + 1e-6
    L = np.array([-0.55, -0.6, 0.58]); L /= np.linalg.norm(L)
    V = np.array([0, 0, 1.0])
    Hh = L + V; Hh /= np.linalg.norm(Hh)
    diff = np.clip(N @ L, 0, 1)
    spec = np.clip(N @ Hh, 0, 1)
    base = np.array([196, 18, 26], np.float32)
    col = base[None, None] * (0.22 + 0.9 * diff[..., None])
    # subsurface glow (rubber is translucent): warm light through the rim on the lit side + back rim
    rim = (1 - nz) ** 2.5
    back = np.clip(N @ np.array([0.8, 0.1, -0.2]), 0, 1)
    col += np.array([255, 70, 50])[None, None] * (0.35 * rim * back)[..., None]
    col += np.array([255, 120, 90])[None, None] * (0.18 * np.exp(-((uu + 0.05) ** 2 + (v - 0.15) ** 2) / 0.25))[..., None]
    col += 255 * (0.8 * spec ** 400)[..., None] + np.array([255, 190, 180])[None, None] * (0.10 * spec ** 25)[..., None]
    # secondary soft window reflection
    win = np.exp(-(((uu + 0.45) / 0.07) ** 2 + ((v + 0.48) / 0.16) ** 2) ** 2)
    col += 255 * (0.55 * win)[..., None]
    # darker towards the knot
    col *= (1 - 0.35 * np.clip((v - 0.55) / 0.45, 0, 1) ** 2)[..., None]
    rgba = np.zeros((h, w, 4), np.uint8)
    rgba[..., :3] = col.clip(0, 255)
    rgba[..., 3] = (alpha * 255).astype(np.uint8)
    img = Image.fromarray(rgba)
    d = ImageDraw.Draw(img)
    def P(x, y):
        return ((x - ox) * S, (y - oy) * S)
    ky = BCY + RY
    # string
    pts = [P(BCX + 16 * math.sin((yy - ky) / 70) + (yy - ky) * 0.05, yy) for yy in np.arange(ky + 10, 1650, 4)]
    d.line(pts, fill=(222, 214, 200, 230), width=int(2.4 * S), joint="curve")
    # knot
    d.polygon([P(BCX - 6, ky - 6), P(BCX + 6, ky - 6), P(BCX + 15, ky + 16), P(BCX - 15, ky + 16)], fill=(120, 8, 14, 255))
    d.ellipse([*P(BCX - 9, ky + 8), *P(BCX + 9, ky + 22)], fill=(150, 14, 20, 255))
    return img, S, ox, oy


def make_pin():
    S = 2.5
    ox, oy = -8.0, -PIN_L * math.sin(ANG) - 40
    w, h = int((PIN_L * math.cos(ANG) + 50) * S), int((PIN_L * math.sin(ANG) + 80) * S)
    ys, xs = np.mgrid[0:h, 0:w].astype(np.float32)
    X, Y = xs / S + ox, ys / S + oy           # world offset from the tip
    dx, dy = math.cos(ANG), -math.sin(ANG)
    s = X * dx + Y * dy
    q = X * (-dy) + Y * dx
    shaft_len = PIN_L - 22
    rad = 4.4 * np.clip(s / 55, 0.04, 1)
    a_sh = np.clip((rad - np.abs(q)) * S + 0.5, 0, 1) * np.clip(s * S + 0.5, 0, 1) * (s <= shaft_len)
    qn = np.clip(q / np.maximum(rad, 1e-3), -1, 1)
    b = 0.28 + 0.75 * np.exp(-((qn + 0.35) / 0.22) ** 2) + 0.25 * np.exp(-((qn - 0.55) / 0.2) ** 2)
    sh_col = np.stack([b * 225, b * 230, b * 238], -1)
    # head
    hr = 21.0
    hx, hy = s - PIN_L, q
    hd = np.sqrt(hx ** 2 + hy ** 2) / hr
    a_hd = np.clip((1 - hd) * hr * S + 0.5, 0, 1)
    hz = np.sqrt(np.clip(1 - hd ** 2, 0, 1))
    # light from upper-left in screen terms -> express in (s,q) frame
    Lw = np.array([-0.55, -0.6, 0.58]); Lw /= np.linalg.norm(Lw)
    nxw = (hx * dx + hy * (-dy)) / hr       # back to world x
    nyw = (hx * dy + hy * dx) / hr
    dif = np.clip(nxw * Lw[0] + nyw * Lw[1] + hz * Lw[2], 0, 1)
    sp = np.clip(nxw * 0.3 * -1 + nyw * -0.35 + hz * 0.89, 0, 1) ** 70
    hcol = np.array([238, 178, 30], np.float32)[None, None] * (0.25 + 0.85 * dif[..., None]) + 255 * sp[..., None]
    col = sh_col * a_sh[..., None] * (1 - a_hd[..., None]) + hcol * a_hd[..., None]
    alpha = np.maximum(a_sh, a_hd)
    col = np.where(alpha[..., None] > 0, col / np.maximum(np.maximum(a_sh * (1 - a_hd) + a_hd, 1e-3), 1e-3)[..., None], 0)
    rgba = np.zeros((h, w, 4), np.uint8)
    rgba[..., :3] = col.clip(0, 255)
    rgba[..., 3] = (alpha * 255).astype(np.uint8)
    return Image.fromarray(rgba), S, ox, oy


BG = make_bg()
BAL = make_balloon()
BAL_LO = (BAL[0].resize((BAL[0].width // 2, BAL[0].height // 2), Image.LANCZOS), BAL[1] / 2, BAL[2], BAL[3])
PIN = make_pin()
PIN_LO = (PIN[0].resize((PIN[0].width // 2, PIN[0].height // 2), Image.LANCZOS), PIN[1] / 2, PIN[2], PIN[3])

# vignette + grain
_yy, _xx = np.mgrid[0:H, 0:W].astype(np.float32)
VIG = (1 - 0.55 * np.clip(np.sqrt(((_xx - W / 2) / (W * 0.75)) ** 2 + ((_yy - H / 2) / (H * 0.7)) ** 2) - 0.35, 0, 1) ** 1.4)[..., None]
_rng = np.random.default_rng(7)
GRAIN = [_rng.normal(0, 4.0, (H, W, 1)).astype(np.float32) for _ in range(6)]

# fragments (world, spawn relative to pop)
FRAGS = []
_r = np.random.default_rng(11)
while len(FRAGS) < 46:
    x, y = _r.uniform(BCX - RX * 1.15, BCX + RX * 1.15), _r.uniform(BCY - RY, BCY + RY)
    u, v = (x - BCX) / RX, (y - BCY) / RY
    g = math.sqrt((u / (1 - 0.15 * v)) ** 2 + v ** 2)
    if not (0.5 < g < 0.98):
        continue
    p = np.array([x, y])
    dist = np.linalg.norm(p - PCONT)
    dirv = (p - PCONT) / (dist + 1e-3)
    dirv = dirv * 0.6 + np.array([-(y - BCY), x - BCX]) / (np.hypot(x - BCX, y - BCY) + 1e-3) * _r.uniform(-0.4, 0.4)
    L = _r.uniform(36, 95); wd = _r.uniform(6, 15); kk = _r.uniform(-0.012, 0.012)
    ss = np.linspace(-L / 2, L / 2, 9)
    cy_ = kk * ss ** 2
    taper = 0.35 + 0.65 * np.sin(np.linspace(0.15, math.pi - 0.15, 9))
    top = [(a, b - wd / 2 * tp) for a, b, tp in zip(ss, cy_, taper)]
    bot = [(a, b + wd / 2 * tp) for a, b, tp in zip(ss, cy_, taper)][::-1]
    FRAGS.append(dict(p0=p, ts=dist / 1500.0, v0=dirv * _r.uniform(260, 720), rot0=_r.uniform(0, 6.28),
                      w=_r.uniform(-7, 7), shape=top + bot, edge=top, shade=_r.uniform(0.6, 1.1), inner=_r.random() < 0.3))


def frag_pos(f, tl):
    k = 2.0
    dt = tl - f["ts"]
    if dt < 0:
        return None
    disp = f["v0"] * (1 - math.exp(-k * dt)) / k + np.array([0, 0.5 * 520 * dt * dt])
    return f["p0"] + disp, f["rot0"] + f["w"] * (1 - math.exp(-1.2 * dt)) / 1.2


# ---------------- subtitles ----------------
def words_timing(i):
    words = VO[i]["text"].split()
    dur = VO[i]["dur"]
    wl = np.array([len(x) + 2 for x in words], float)
    cs = np.concatenate([[0], np.cumsum(wl)]) / wl.sum() * dur
    return [(STARTS[i] + cs[j], STARTS[i] + cs[j + 1], words[j]) for j in range(len(words))]


WORDS = [words_timing(i) for i in range(len(VO))]


def chunks(i):
    out, cur = [], []
    for w in WORDS[i]:
        cur.append(w)
        if len(cur) >= 4 or w[2].endswith((".", ",", "?")):
            out.append(cur); cur = []
    if cur:
        out.append(cur)
    return out


def draw_subs(img, t, y=1560):
    for i in range(len(VO)):
        ws = WORDS[i]
        if not (ws[0][0] - 0.05 <= t < ws[-1][1] + 0.25):
            continue
        cl = chunks(i)
        for ci, ch in enumerate(cl):
            end = ch[-1][1] + 0.25 if ci == len(cl) - 1 else cl[ci + 1][0][0] - 0.05
            if ch[0][0] - 0.05 <= t < end:
                text = " ".join(w[2] for w in ch)
                size = 80
                while text_w(text, font("inter_xb", size)) > 960:
                    size -= 4
                f = font("inter_xb", size)
                x = 540 - text_w(text, f) / 2
                d = ImageDraw.Draw(img)
                for w in ch:
                    col = (255, 214, 64, 255) if w[0] <= t < w[1] else (255, 255, 255, 255)
                    d.text((x, y), w[2], font=f, fill=col, anchor="ls", stroke_width=8, stroke_fill=(0, 0, 0, 255))
                    x += f.getlength(w[2] + " ")
                return


# ---------------- scenes ----------------
def scene_main(t):
    cam = camera(t)
    c = cam[0]
    bgcam = (1 + (c - 1) * 0.4, cam[1], cam[2])
    img = cam_layer(BG[0], BG[1], BG[2], BG[3], bgcam)

    # balloon (with slow bob)
    bob = 5 * math.sin(t * 0.8)
    bx = lunge(t)
    if t < T_POP + 0.8:
        spr = BAL if c > 1.55 else BAL_LO
        bl = cam_layer(spr[0], spr[1], spr[2] + bx, spr[3] + bob, cam)
        arr = np.asarray(bl).astype(np.float32)
        cxs, cys = w2s((XS + bx, YC + bob), cam)
        if dent(t) > 0:
            from scipy.ndimage import map_coordinates
            R = 95 * c
            x0, x1 = int(max(0, cxs - 3 * R)), int(min(W, cxs + 1.5 * R))
            y0, y1 = int(max(0, cys - 2.5 * R)), int(min(H, cys + 2.5 * R))
            yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
            rr = np.sqrt(((xx - cxs) / 1.6) ** 2 + (yy - cys) ** 2)
            disp = dent(t) * c * np.exp(-(rr / R) ** 2)
            for ch in range(4):
                arr[y0:y1, x0:x1, ch] = map_coordinates(arr[..., ch], [yy, xx + disp], order=1, mode="nearest")
            # tension shading in the dimple
            arr[y0:y1, x0:x1, :3] *= (1 - 0.35 * (disp / (24 * c + 1e-3)) ** 1.5)[..., None]
        # pin reflection + shadow on the rubber when close
        gp = gap_eff(t)
        if gp < 70 and t < T_POP:
            k = (1 - gp / 70) ** 2
            yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
            ddx = (xx - (cxs - 18 * c)) / (60 * c)
            ddy = (yy - (cys + 22 * c)) / (16 * c)
            shade = np.exp(-(ddx ** 2 + ddy ** 2))
            arr[..., :3] *= (1 - 0.45 * k * shade)[..., None]
            ddx = (xx - (cxs - 26 * c)) / (40 * c)
            ddy = (yy - (cys - 3 * c)) / (4 * c)
            arr[..., :3] += (np.array([255, 230, 170]) * 0.55 * k)[None, None] * np.exp(-(ddx ** 2 + ddy ** 2))[..., None]
        if t >= T_POP:
            tl = (t - T_POP)
            rf = 1500 * tl * c
            ang = np.arctan2(_yy - cys, _xx - cxs)
            jag = 1 + 0.10 * np.sin(ang * 7 + 1.3) + 0.06 * np.sin(ang * 17 + 0.2) + 0.04 * np.sin(ang * 31)
            dist = np.sqrt((_xx - cxs) ** 2 + (_yy - cys) ** 2) / jag
            gone = dist < rf
            band = (dist >= rf) & (dist < rf + 16 * c)
            arr[..., 3] = np.where(gone, 0, arr[..., 3])
            arr[..., :3] = np.where(band[..., None], arr[..., :3] * 0.45 + np.array([40, 0, 0]), arr[..., :3])
        bl = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
        img.alpha_composite(bl)
    else:
        # string falls after the pop: skip the balloon entirely
        pass

    # fragments
    if t >= T_POP:
        tl = (t - T_POP)
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        for f in FRAGS:
            for lag, al in ((0.035, 70), (0.017, 120), (0.0, 255)):
                r = frag_pos(f, tl - lag)
                if r is None:
                    continue
                p, rot = r
                cr, sr = math.cos(rot), math.sin(rot)
                tr = lambda x, y: w2s((p[0] + x * cr - y * sr, p[1] + bob + x * sr + y * cr), cam)
                base = (232, 112, 112) if f["inner"] else (186, 18, 26)
                col = tuple(int(clamp(b * f["shade"], 0, 255)) for b in base)
                d.polygon([tr(x, y) for x, y in f["shape"]], fill=col + (al,))
                if al == 255:
                    hl = tuple(int(clamp(b * 1.35 + 30, 0, 255)) for b in col)
                    d.line([tr(x, y) for x, y in f["edge"]], fill=hl + (200,), width=2)
        lay = lay.filter(ImageFilter.GaussianBlur(1.2))
        img.alpha_composite(lay)

    # pin
    tipx = XS + gap(t) - dent(t)
    spr = PIN if c > 1.55 else PIN_LO
    pin = cam_layer(spr[0], spr[1], spr[2] + tipx, spr[3] + YC + bob * 0.0, cam)
    # soft contact shadow of pin on the far wall is omitted (wall is far away)
    img.alpha_composite(pin)

    # readout
    if t < T_POP + 0.5:
        a = eout((t - 0.8) / 0.6) * (1 - clamp((t - T_POP) / 0.4))
        if a > 0:
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            d = ImageDraw.Draw(lay)
            sx, sy = w2s((XS + bx - dent(t), YC), cam)
            tx, _ = w2s((tipx, YC), cam)
            yl = sy - 64
            touch = t >= T_TOUCH or gap_eff(t) < 8
            col = (255, 80, 70) if touch else (255, 255, 255)
            al = int(225 * a)
            d.line([(sx, yl), (tx, yl)], fill=col + (al,), width=3)
            for xx in (sx, tx):
                d.line([(xx, yl - 13), (xx, yl + 13)], fill=col + (al,), width=3)
            mm = max(0.0, gap_eff(t)) / PX_PER_MM
            txt = f"{mm:4.1f} mm"
            fz = font("mono_sb", 52)
            xm = max((sx + tx) / 2, sx + 10)
            draw_text(d, (xm, yl - 26), txt, fz, col + (al,), anchor="ms")
            img.alpha_composite(lay)

    # grade: vignette + grain
    arr = np.asarray(img.convert("RGB")).astype(np.float32)
    arr = arr * VIG + GRAIN[int(t * FPS) % len(GRAIN)]
    # flash at pop
    if 0 <= t - T_POP < 0.14:
        arr += 255 * 0.42 * (1 - (t - T_POP) / 0.14)
    out = Image.fromarray(arr.clip(0, 255).astype(np.uint8)).convert("RGBA")
    # darken under subtitles
    if t >= STARTS[0] - 0.1:
        prof = np.clip((np.linspace(0, 1, H) - 0.70) / 0.08, 0, 1) * np.clip((0.92 - np.linspace(0, 1, H)) / 0.06, 0, 1)
        g = np.zeros((H, W, 4), np.uint8)
        g[..., 3] = (prof * 120)[:, None].astype(np.uint8)
        out.alpha_composite(Image.fromarray(g))
    return out


def scene_end(lt):
    img = Image.new("RGBA", (W, H), RED + (255,))
    d = ImageDraw.Draw(img)
    k1 = eout(lt / 0.3)
    draw_text(d, (540, 600 + (1 - k1) * 30), "Your first ad", font("anton", 140), (255, 255, 255, int(255 * k1)), anchor="ms")
    draw_text(d, (540, 760 + (1 - k1) * 30), "is on us.", font("anton", 140), (255, 255, 255, int(255 * k1)), anchor="ms")
    k2 = eout((lt - 0.45) / 0.3)
    d.rounded_rectangle((170, 880, 910, 1050), 85, fill=(255, 255, 255, int(255 * k2)))
    draw_text(d, (540, 995), "DM “DAILY”", font("anton", 100), RED + (int(255 * k2),), anchor="ms", tracking=4)
    k3 = eout((lt - 0.9) / 0.3)
    if k3 > 0:
        bug = logo_bug(120, bg=(255, 255, 255), fg=RED)
        bug.putalpha(bug.getchannel("A").point(lambda v: int(v * k3)))
        img.alpha_composite(bug, (480, 1150))
        draw_text(d, (540, 1340), "@madeyouwantit.studio", font("inter_b", 46), (255, 255, 255, int(255 * k3)), anchor="ms")
        draw_text(d, (540, 1400), "Reels people can't stop watching.", font("inter_m", 34), (255, 225, 220, int(255 * k3)), anchor="ms")
    return img


def render(fi):
    t = fi / FPS
    if t >= T_END:
        img = scene_end(t - T_END)
    else:
        img = scene_main(t)
        draw_subs(img, t)
    return img.convert("RGB")


def job(fi):
    p = f"{OUT}/{fi:05d}.jpg"
    if not os.path.exists(p):
        render(fi).save(p, quality=92)


if __name__ == "__main__":
    P = "/tmp/claude-0/-home-claude/2371c677-845b-5e5d-a138-cf5eda76036b/scratchpad/"
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        for tt in sys.argv[2:]:
            render(int(float(tt) * FPS)).save(f"{P}r2_{tt}.jpg", quality=85)
    else:
        from multiprocessing import Pool
        N = int(TOTAL * FPS)
        with Pool(2) as pool:
            pool.map(job, range(N), chunksize=8)
        print("frames", N)

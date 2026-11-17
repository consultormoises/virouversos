"""Biblioteca visual v2 – Virou Versos.
Fundos gerativos por campanha (numpy + PIL), texto com brilho, partículas.
"""
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

GF = "/usr/share/fonts/truetype/google-fonts/"
LORA = GF + "Lora-Variable.ttf"
LORA_I = GF + "Lora-Italic-Variable.ttf"
INTER = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
INTER_M = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"


def font(path, size, var=None):
    f = ImageFont.truetype(path, size)
    if var:
        try:
            f.set_variation_by_name(var)
        except Exception:
            pass
    return f


# ---------------------------------------------------------------- temas
THEMES = {
    "1. Ruídos do Agora": dict(
        key="waves", top=(5, 9, 30), bot=(16, 40, 96),
        glows=[(0.18, 0.22, 700, (40, 150, 255), 0.55), (0.85, 0.62, 800, (170, 70, 220), 0.40)],
        fg=(247, 243, 235), accent=(120, 200, 255), label="RUÍDOS DO AGORA"),
    "2. Cidade em Verso": dict(
        key="city", top=(22, 26, 70), bot=(250, 150, 96),
        mid=(128, 66, 118),
        glows=[(0.5, 0.80, 900, (255, 170, 100), 0.65)],
        fg=(255, 248, 236), accent=(255, 200, 130), label="CIDADE EM VERSO", scrim=0.42),
    "3. O que a gente não diz": dict(
        key="moon", top=(8, 6, 26), bot=(56, 32, 98),
        glows=[(0.80, 0.14, 650, (176, 140, 255), 0.55), (0.25, 0.85, 800, (110, 60, 190), 0.35)],
        fg=(242, 236, 252), accent=(200, 168, 248), label="O QUE A GENTE NÃO DIZ"),
    "4. Fecha o Ano em Verso": dict(
        key="sunrise", top=(14, 28, 56), bot=(255, 176, 104),
        mid=(120, 72, 110),
        glows=[(0.5, 0.80, 900, (255, 170, 100), 0.50)],
        fg=(255, 249, 238), accent=(255, 210, 150), label="FECHA O ANO EM VERSO", scrim=0.50),
}


# ---------------------------------------------------------------- helpers de imagem
def vgrad(H, W, stops):
    """stops: [(pos,(r,g,b)),...] -> float32 HxWx3"""
    ys = np.linspace(0, 1, H)
    pos = [s[0] for s in stops]
    out = np.zeros((H, 1, 3), np.float32)
    for c in range(3):
        out[:, 0, c] = np.interp(ys, pos, [s[1][c] for s in stops])
    return np.repeat(out, W, axis=1)


def add_glow(img, cx, cy, r, color, strength):
    H, W = img.shape[:2]
    x0, x1 = max(0, int(cx - r * 1.9)), min(W, int(cx + r * 1.9))
    y0, y1 = max(0, int(cy - r * 1.9)), min(H, int(cy + r * 1.9))
    if x1 <= x0 or y1 <= y0:
        return
    yy, xx = np.ogrid[y0:y1, x0:x1]
    d2 = ((xx - cx) ** 2 + (yy - cy) ** 2) / float(r * r)
    a = np.exp(-d2 * 2.4) * strength
    img[y0:y1, x0:x1] += a[..., None] * np.array(color, np.float32)


def sprite_glow(r, color=(255, 255, 255)):
    """disco suave RGBA-float (alpha 0-1) de raio r"""
    s = int(r * 2 + 1)
    yy, xx = np.ogrid[:s, :s]
    d2 = ((xx - r) ** 2 + (yy - r) ** 2) / float(r * r)
    a = np.clip(np.exp(-d2 * 3.0), 0, 1).astype(np.float32)
    return a, np.array(color, np.float32)


def blit_add(img, sprite, cx, cy, gain=1.0):
    a, col = sprite
    s = a.shape[0]
    r = s // 2
    x0, y0 = int(cx - r), int(cy - r)
    H, W = img.shape[:2]
    sx0, sy0 = max(0, -x0), max(0, -y0)
    x0c, y0c = max(0, x0), max(0, y0)
    x1c, y1c = min(W, x0 + s), min(H, y0 + s)
    if x1c <= x0c or y1c <= y0c:
        return
    sub = a[sy0:sy0 + (y1c - y0c), sx0:sx0 + (x1c - x0c)]
    img[y0c:y1c, x0c:x1c] += sub[..., None] * col * gain


def rgba_over(img, layer_rgba, ox=0, oy=0):
    """layer_rgba: HxWx4 uint8; compõe sobre img float32 (alpha normal)."""
    h, w = layer_rgba.shape[:2]
    H, W = img.shape[:2]
    x0, y0 = int(ox), int(oy)
    sx0, sy0 = max(0, -x0), max(0, -y0)
    x0c, y0c = max(0, x0), max(0, y0)
    x1c, y1c = min(W, x0 + w), min(H, y0 + h)
    if x1c <= x0c or y1c <= y0c:
        return
    sub = layer_rgba[sy0:sy0 + (y1c - y0c), sx0:sx0 + (x1c - x0c)].astype(np.float32)
    a = sub[..., 3:4] / 255.0
    img[y0c:y1c, x0c:x1c] = img[y0c:y1c, x0c:x1c] * (1 - a) + sub[..., :3] * a


def grain_pool(H, W, n=6, amp=7.0, seed=1):
    rng = np.random.default_rng(seed)
    return [(rng.standard_normal((H, W, 1)) * amp).astype(np.float32) for _ in range(n)]


def vignette(H, W, strength=0.42):
    yy, xx = np.ogrid[:H, :W]
    d = np.sqrt(((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H / 2) / (H * 0.62)) ** 2)
    v = 1 - strength * np.clip(d - 0.35, 0, 1) ** 1.6
    return v[..., None].astype(np.float32)


# ---------------------------------------------------------------- camadas de cena
def stars_layer(W, H, n, seed, ymax=0.7, color=(255, 255, 255)):
    rng = random.Random(seed)
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    pts = []
    for _ in range(n):
        x, y = rng.uniform(0, W), rng.uniform(0, H * ymax)
        r = rng.choice([1, 1, 1, 2, 2, 3])
        a = rng.randint(90, 230)
        d.ellipse([x - r, y - r, x + r, y + r], fill=color + (a,))
        pts.append((x, y, r))
    return L, pts


def skyline_layer(W, H, base_y, hmin, hmax, color, seed, windows=0.0, win_color=(255, 205, 120), haze=None):
    rng = random.Random(seed)
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    x = -rng.randint(0, 80)
    while x < W:
        bw = rng.randint(70, 170)
        bh = rng.randint(hmin, hmax)
        top = base_y - bh
        d.rectangle([x, top, x + bw, H], fill=color + (255,))
        kind = rng.random()
        if kind < 0.25:  # degrau
            d.rectangle([x + bw * 0.2, top - 40, x + bw * 0.75, top], fill=color + (255,))
        elif kind < 0.4:  # antena
            ax = x + bw * 0.5
            d.rectangle([ax - 2, top - 90, ax + 2, top], fill=color + (255,))
        if windows > 0:
            wx = 16
            wy = 22
            gx, gy = 14, 20
            yy_ = top + 26
            while yy_ + wy < base_y + 40:
                xx_ = x + 14
                while xx_ + wx < x + bw - 10:
                    if rng.random() < windows:
                        k = rng.uniform(0.55, 1.0)
                        c = tuple(int(v * k) for v in win_color) + (255,)
                        d.rectangle([xx_, yy_, xx_ + wx, yy_ + wy], fill=c)
                    xx_ += wx + gx
                yy_ += wy + gy
        x += bw + rng.randint(-6, 10)
    if haze:
        arr = np.array(L, np.float32)
        a = arr[..., 3:4] / 255.0
        grad = np.linspace(0, 1, H)[:, None, None]
        arr[..., :3] = arr[..., :3] * (1 - 0.0) + 0
        return Image.fromarray(arr.astype(np.uint8), "RGBA")
    return L


def ridge_layer(W, H, base_y, amp, color, seed, scale=1.0):
    rng = random.Random(seed)
    ph = [rng.uniform(0, 6.28) for _ in range(4)]
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    pts = []
    for x in range(0, W + 8, 8):
        y = base_y - amp * (0.55 * math.sin(x * 0.0021 * scale + ph[0]) + 0.30 * math.sin(x * 0.0057 * scale + ph[1])
                            + 0.15 * math.sin(x * 0.0123 * scale + ph[2]))
        pts.append((x, y))
    pts += [(W, H), (0, H)]
    d.polygon(pts, fill=color + (255,))
    return L


def fog_layer(W, H, cy, thick, color, seed, alpha=0.45):
    rng = np.random.default_rng(seed)
    n = rng.standard_normal((max(2, H // 24), max(2, W // 24)))
    im = Image.fromarray(((n - n.min()) / (n.max() - n.min()) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)
    im = im.filter(ImageFilter.GaussianBlur(40))
    a = np.array(im, np.float32) / 255.0
    yy = np.arange(H)[:, None]
    env = np.exp(-((yy - cy) / float(thick)) ** 2)
    a = np.clip((a - 0.35) * 1.8, 0, 1) * env * alpha
    out = np.zeros((H, W, 4), np.uint8)
    out[..., :3] = np.array(color, np.uint8)
    out[..., 3] = (a * 255).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


def bokeh_layer(W, H, n, seed, colors, rmin=18, rmax=70, ymin=0.0, ymax=0.8):
    rng = random.Random(seed)
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for _ in range(n):
        r = rng.randint(rmin, rmax)
        x, y = rng.uniform(0, W), rng.uniform(H * ymin, H * ymax)
        c = rng.choice(colors)
        a = rng.randint(28, 70)
        t = Image.new("RGBA", (r * 2 + 4, r * 2 + 4), (0, 0, 0, 0))
        td = ImageDraw.Draw(t)
        td.ellipse([2, 2, r * 2 + 2, r * 2 + 2], fill=c + (a,), outline=c + (min(255, a + 60),), width=2)
        t = t.filter(ImageFilter.GaussianBlur(1.4))
        L.alpha_composite(t, (int(x - r), int(y - r)) if x - r >= 0 and y - r >= 0 else (max(0, int(x - r)), max(0, int(y - r))))
    return L


def waves_draw(img_rgba, W, H, t, theme, cy, amp, nlines=26, phase0=0.0, Wt=None):
    """desenha linhas de onda (luz) num RGBA PIL. t em segundos."""
    d = ImageDraw.Draw(img_rgba)
    c1 = (90, 210, 255)
    c2 = (200, 110, 255)
    Wt = Wt or W
    xs = np.linspace(0, W, max(220, int(220 * W / Wt)))
    for k in range(nlines):
        u = k / (nlines - 1)
        off = (u - 0.5) * 2
        y0 = cy + off * H * 0.17
        mix = u
        col = tuple(int(c1[i] * (1 - mix) + c2[i] * mix) for i in range(3))
        ntile = max(1, int(round(W / Wt)))
        env = np.max([np.exp(-((xs - Wt * (i + 0.5 + 0.18 * math.sin(phase0 + t * 0.25 + i))) / (Wt * 0.38)) ** 2) for i in range(ntile)], axis=0)
        ys = y0 + amp * env * np.sin(xs / Wt * 2 * math.pi * (1.4 + 0.5 * off) + phase0 + t * 0.9 + k * 0.33) \
            + amp * 0.35 * env * np.sin(xs / Wt * 2 * math.pi * 3.1 - t * 0.6 + k * 0.5)
        a = int(60 + 150 * (1 - abs(off)) ** 1.5)
        d.line(list(zip(xs.tolist(), ys.tolist())), fill=col + (a,), width=2)


# ---------------------------------------------------------------- estágio de fundo estático
def build_scene(theme_name, W, H, seed=7, pan_margin=0, t_waves=0.0, tiles=1):
    """Retorna (base float32 HxWx3, layers dict) – base já tem gradiente, brilhos, astros."""
    th = THEMES[theme_name]
    key = th["key"]
    if "mid" in th:
        stops = [(0, th["top"]), (0.55, th["mid"]), (1, th["bot"])]
    else:
        stops = [(0, th["top"]), (1, th["bot"])]
    base = vgrad(H, W, stops)
    Wt = W // tiles
    for i in range(tiles):
        for gx, gy, gr, gc, gs in th["glows"]:
            add_glow(base, (i + gx) * Wt, gy * H, gr, gc, gs)
    layers = {}
    rngp = random.Random(seed)
    if key == "waves":
        # poeira de luz
        L, pts = stars_layer(W, H, 120, seed, ymax=1.0, color=(170, 215, 255))
        layers["stars"] = (L, pts)
    elif key == "city":
        st, pts = stars_layer(W, H, 70, seed, ymax=0.4, color=(255, 236, 214))
        layers["stars"] = (st, pts)
        # sol baixo
        for i in range(tiles):
            add_glow(base, (i + 0.72) * Wt, H * 0.73, 200, (255, 220, 160), 0.45)
        sw = W + pan_margin
        layers["far"] = skyline_layer(sw, H, int(H * 0.88), int(H * 0.05), int(H * 0.15), (92, 52, 104), seed + 1, windows=0.0)
        layers["mid"] = skyline_layer(sw, H, int(H * 0.94), int(H * 0.06), int(H * 0.17), (40, 30, 78), seed + 2, windows=0.20)
        layers["near"] = skyline_layer(sw, H, int(H * 1.00), int(H * 0.06), int(H * 0.19), (14, 14, 38), seed + 3, windows=0.30)
    elif key == "moon":
        st, pts = stars_layer(W, H, 160, seed, ymax=0.75, color=(235, 225, 255))
        layers["stars"] = (st, pts)
        mx, my, mr = int(Wt * 0.80), int(H * 0.15), int(min(Wt, H) * 0.075)
        add_glow(base, mx, my, mr * 4.5, (190, 160, 255), 0.35)
        # lua (renderizada com crateras suaves, supersampling)
        ss = 3
        R = mr * ss
        S = R * 2 + 8
        col = Image.new("RGB", (S, S), (250, 245, 232))
        cd = ImageDraw.Draw(col)
        crng = random.Random(seed + 99)
        for _ in range(9):
            cr = crng.randint(int(R * 0.08), int(R * 0.22))
            ang = crng.uniform(0, 6.28)
            dist = crng.uniform(0, R * 0.7)
            ccx, ccy = R + 4 + dist * math.cos(ang), R + 4 + dist * math.sin(ang)
            cd.ellipse([ccx - cr, ccy - cr, ccx + cr, ccy + cr], fill=(232, 224, 214))
        col = col.filter(ImageFilter.GaussianBlur(5))
        msk = Image.new("L", (S, S), 0)
        ImageDraw.Draw(msk).ellipse([4, 4, R * 2 + 4, R * 2 + 4], fill=255)
        msk = msk.filter(ImageFilter.GaussianBlur(1.2))
        size = (S // ss, S // ss)
        col = col.resize(size, Image.LANCZOS)
        msk = msk.resize(size, Image.LANCZOS)
        carr = np.array(col, np.float32)
        a_ = np.array(msk, np.float32)[..., None] / 255.0
        mh, mw = carr.shape[:2]
        x0, y0 = int(mx - mw / 2), int(my - mh / 2)
        base[y0:y0 + mh, x0:x0 + mw] = base[y0:y0 + mh, x0:x0 + mw] * (1 - a_) + carr * a_
        sw = W + pan_margin
        layers["ridge_far"] = ridge_layer(sw, H, int(H * 0.90), int(H * 0.07), (44, 26, 84), seed + 4)
        layers["ridge_near"] = ridge_layer(sw, H, int(H * 1.01), int(H * 0.06), (14, 9, 36), seed + 5, scale=1.7)
        layers["fog1"] = fog_layer(sw, H, int(H * 0.82), int(H * 0.10), (190, 170, 235), seed + 6, 0.40)
        layers["fog2"] = fog_layer(sw, H, int(H * 0.62), int(H * 0.12), (150, 120, 215), seed + 7, 0.30)
    elif key == "sunrise":
        st, pts = stars_layer(W, H, 50, seed, ymax=0.3, color=(255, 240, 220))
        layers["stars"] = (st, pts)
        for i in range(tiles):
            add_glow(base, (i + 0.5) * Wt, H * 0.80, 240, (255, 225, 160), 0.30)
        layers["bokeh"] = bokeh_layer(W + pan_margin, H, 34, seed + 8, [(255, 214, 140), (255, 185, 120), (255, 240, 200)],
                                      rmin=18, rmax=64, ymin=0.05, ymax=0.78)
        sw = W + pan_margin
        layers["hill_far"] = ridge_layer(sw, H, int(H * 0.90), int(H * 0.06), (66, 54, 96), seed + 9)
        layers["hill_near"] = ridge_layer(sw, H, int(H * 1.01), int(H * 0.06), (18, 22, 44), seed + 10, scale=1.4)
    return base, layers, th


def composite_static(base, layers, th, W, H, ox=0, panorama=False, t_waves=0.0, seed=7, Wt=None):
    img = base.copy()
    key = th["key"]
    # camadas desenhadas dentro do mesmo W
    def pil_over(L, x=0):
        arr = np.array(L)
        rgba_over(img, arr, -x, 0)
    if "stars" in layers:
        pil_over(layers["stars"][0])
    if key == "waves":
        L = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        waves_draw(L, W, H, t_waves, th, cy=H * 0.58, amp=H * 0.075, Wt=Wt)
        glow = L.filter(ImageFilter.GaussianBlur(7))
        a = np.array(glow, np.float32)
        img += a[..., :3] * (a[..., 3:4] / 255.0) * 1.4
        rgba_over(img, np.array(L), 0, 0)
    for name in ("far", "mid", "near", "ridge_far", "fog2", "ridge_near", "fog1", "bokeh", "hill_far", "hill_near"):
        if name in layers:
            pil_over(layers[name], ox)
    return img


def finish(img, grain=None, vig=None):
    if vig is not None:
        img = img * vig
    if grain is not None:
        img = img + grain
    return np.clip(img, 0, 255).astype(np.uint8)


# ---------------------------------------------------------------- texto
def wrap_text(d, text, fnt, maxw):
    out = []
    for para in text.split("\n"):
        words = para.split()
        line = ""
        for w in words:
            t = (line + " " + w).strip()
            if d.textlength(t, font=fnt) <= maxw:
                line = t
            else:
                out.append(line)
                line = w
        out.append(line)
    return out


def text_layer(lines, fnt, W, color, glow_color, line_h, pad=60, align="center", shadow=0.55, glow=0.35, tracking=0):
    """Gera um RGBA uint8 (altura = len(lines)*line_h + 2*pad) com sombra e brilho."""
    h = int(len(lines) * line_h + pad * 2)
    base = Image.new("RGBA", (W, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(base)
    y = pad
    for ln in lines:
        d.text((W / 2, y + line_h / 2), ln, font=fnt, fill=color + (255,), anchor="mm")
        y += line_h
    alpha = base.split()[3]
    sh = Image.new("RGBA", (W, h), (0, 0, 0, 0))
    sh.putalpha(alpha.filter(ImageFilter.GaussianBlur(16)).point(lambda v: int(v * shadow)))
    gl = Image.new("RGBA", (W, h), glow_color + (0,))
    gl.putalpha(alpha.filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(min(255, v * glow))))
    out = Image.new("RGBA", (W, h), (0, 0, 0, 0))
    out = Image.alpha_composite(out, sh)
    out = Image.alpha_composite(out, gl)
    out = Image.alpha_composite(out, base)
    return np.array(out)


def spaced(text, n=1):
    return (" " * n).join(list(text)).replace("   ", "  ")


def draw_emblem(d, cx, cy, r, color, fnt=None):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color + (230,), width=2)
    d.ellipse([cx - r + 7, cy - r + 7, cx + r - 7, cy + r - 7], outline=color + (110,), width=1)
    if fnt is None:
        fnt = font(LORA, int(r * 1.15), "Bold")
    d.text((cx, cy - 2), "V", font=fnt, fill=color + (255,), anchor="mm")


def draw_ornament(d, cx, cy, w, color):
    d.line([cx - w, cy, cx - 16, cy], fill=color + (200,), width=2)
    d.line([cx + 16, cy, cx + w, cy], fill=color + (200,), width=2)
    d.polygon([(cx, cy - 8), (cx + 8, cy), (cx, cy + 8), (cx - 8, cy)], outline=color + (240,), fill=color + (60,))


def icon_heart(d, cx, cy, s, color):
    pts = []
    for i in range(0, 361, 6):
        t = math.radians(i)
        x = 16 * math.sin(t) ** 3
        y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        pts.append((cx + x * s / 17, cy + y * s / 17))
    d.polygon(pts, outline=color + (255,), fill=color + (40,))
    d.line(pts + [pts[0]], fill=color + (255,), width=4)


def icon_comment(d, cx, cy, s, color):
    w, h = s * 1.15, s * 0.85
    x0, y0, x1, y1 = cx - w / 2, cy - h / 2 - s * 0.08, cx + w / 2, cy + h / 2 - s * 0.08
    d.rounded_rectangle([x0, y0, x1, y1], radius=s * 0.22, fill=color + (40,), outline=color + (255,), width=4)
    tail = [(cx - s * 0.28, y1 - 1), (cx - s * 0.42, y1 + s * 0.3), (cx - s * 0.02, y1 - 1)]
    d.polygon(tail, fill=color + (40,))
    d.line([tail[0], tail[1], tail[2]], fill=color + (255,), width=4)
    for k in (-1, 0, 1):
        d.ellipse([cx + k * s * 0.26 - 4, cy - s * 0.08 - 4, cx + k * s * 0.26 + 4, cy - s * 0.08 + 4], fill=color + (255,))


def icon_bookmark(d, cx, cy, s, color):
    w, h = s * 0.8, s * 1.1
    pts = [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx, cy + h / 2 - s * 0.32), (cx - w / 2, cy + h / 2)]
    d.polygon(pts, fill=color + (40,))
    d.line(pts + [pts[0]], fill=color + (255,), width=4)


def icon_send(d, cx, cy, s, color):
    pts = [(cx - s * 0.55, cy - s * 0.1), (cx + s * 0.6, cy - s * 0.55), (cx + s * 0.2, cy + s * 0.55), (cx - s * 0.05, cy + s * 0.12)]
    d.polygon(pts, fill=color + (40,))
    d.line(pts + [pts[0]], fill=color + (255,), width=4)
    d.line([(cx - s * 0.05, cy + s * 0.12), (cx + s * 0.6, cy - s * 0.55)], fill=color + (255,), width=3)


def scrim(img, cx, cy, rx, ry, k=0.35):
    H, W = img.shape[:2]
    x0, x1 = max(0, int(cx - rx * 1.7)), min(W, int(cx + rx * 1.7))
    y0, y1 = max(0, int(cy - ry * 1.7)), min(H, int(cy + ry * 1.7))
    if x1 <= x0 or y1 <= y0:
        return
    yy, xx = np.ogrid[y0:y1, x0:x1]
    d2 = ((xx - cx) / float(rx)) ** 2 + ((yy - cy) / float(ry)) ** 2
    m = np.exp(-d2 * 1.4) * k
    img[y0:y1, x0:x1] *= (1 - m)[..., None]

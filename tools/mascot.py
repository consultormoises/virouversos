"""Lume, o vagalume do Virou Versos (personagem original). draw_lume(t, size, mood) -> RGBA."""
import math, numpy as np
from PIL import Image, ImageDraw, ImageFilter

S = 1200  # canvas de desenho (supersample 2x sobre 600)
PLUM = (58, 36, 82)
CREAM = (255, 238, 214)
GOLD = (255, 205, 96)
GLOW = (255, 224, 140)


def _radial(size, cx, cy, r, color, power=2.0, alpha=1.0):
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / r
    a = np.clip(1 - d, 0, 1) ** power * alpha
    out = np.zeros((size, size, 4), np.float32)
    out[..., 0], out[..., 1], out[..., 2] = color
    out[..., 3] = a * 255
    return Image.fromarray(out.astype(np.uint8), "RGBA")


def _star(d, x, y, r, color):
    pts = []
    for i in range(8):
        a = math.pi / 4 * i - math.pi / 2
        rr = r if i % 2 == 0 else r * 0.28
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    d.polygon(pts, fill=color)


def draw_lume(t=0.0, size=600, mood="happy", glow=1.0):
    """t em segundos (loop de 6 s). mood: happy | wow | sleepy."""
    k = 2 * math.pi / 6.0
    bob = math.sin(t * k * 1.0) * 26
    sway = math.sin(t * k * 2.0) * 0.5
    pulse = 0.82 + 0.18 * math.sin(t * k * 3.0)
    cx, cy = S / 2, S / 2 + 40 + bob
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))

    # halo
    img.alpha_composite(_radial(S, cx, cy + 120, 520, GLOW, 1.6, 0.55 * pulse * glow))

    # asas (batem rápido)
    flap = math.sin(t * 2 * math.pi * 5.0)
    wl = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    wd = ImageDraw.Draw(wl)
    for side in (-1, 1):
        ang = side * (28 + 20 * flap)
        wing = Image.new("RGBA", (420, 420), (0, 0, 0, 0))
        ImageDraw.Draw(wing).ellipse([30, 150, 330, 270], fill=(225, 238, 255, 150), outline=(255, 255, 255, 210), width=5)
        wing = wing.rotate(ang * -side if side == 1 else ang * -side, resample=Image.BICUBIC, center=(30, 210))
        if side == -1:
            wing = wing.transpose(Image.FLIP_LEFT_RIGHT)
        px = int(cx + (60 if side == 1 else -60 - 420))
        wl.alpha_composite(wing, (px, int(cy - 20 - 210 + 40)))
    img.alpha_composite(wl)

    d = ImageDraw.Draw(img)
    # pernas
    for sx in (-60, 60):
        d.rounded_rectangle([cx + sx - 14, cy + 250, cx + sx + 14, cy + 310], radius=14, fill=PLUM)
    # abdômen brilhante
    bx, by = cx, cy + 135
    belly = _radial(S, bx, by, 190, GLOW, 1.0, 1.0 * glow)
    d.ellipse([bx - 125, by - 145, bx + 125, by + 145], fill=GOLD)
    img.alpha_composite(Image.composite(belly, Image.new("RGBA", (S, S), (0, 0, 0, 0)), Image.new("L", (S, S), 0)))
    inner = _radial(S, bx, by - 20, 150, (255, 247, 200), 0.9, 0.95 * pulse)
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).ellipse([bx - 125, by - 145, bx + 125, by + 145], fill=255)
    layer = Image.new("RGBA", (S, S), (0, 0, 0, 0)); layer.paste(inner, (0, 0), mask)
    img.alpha_composite(layer)
    d = ImageDraw.Draw(img)
    # V da marca na barriga
    vp = [(bx - 52, by - 62), (bx - 24, by - 62), (bx, by + 18), (bx + 24, by - 62), (bx + 52, by - 62), (bx + 12, by + 58), (bx - 12, by + 58)]
    d.polygon(vp, fill=PLUM)
    # bracinhos
    arm = 14 * math.sin(t * k * 2 + 1)
    d.ellipse([cx - 175, cy + 95 + arm, cx - 125, cy + 165 + arm], fill=CREAM, outline=PLUM, width=5)
    d.ellipse([cx + 125, cy + 95 - arm, cx + 175, cy + 165 - arm], fill=CREAM, outline=PLUM, width=5)

    # antenas
    for s in (-1, 1):
        ax = cx + s * 70
        tipx = cx + s * (150 + 26 * sway)
        tipy = cy - 330 + 10 * math.sin(t * k * 2 + s)
        pts = [(ax, cy - 190), (ax + s * 30 + 8 * sway, cy - 270), (tipx, tipy)]
        d.line(pts, fill=PLUM, width=9, joint="curve")
        img.alpha_composite(_radial(S, tipx, tipy, 70, GLOW, 1.2, 0.9 * pulse))
        d = ImageDraw.Draw(img)
        d.ellipse([tipx - 17, tipy - 17, tipx + 17, tipy + 17], fill=(255, 240, 170))

    # cabeça
    hx, hy = cx, cy - 70
    d.ellipse([hx - 185, hy - 175, hx + 185, hy + 175], fill=CREAM, outline=PLUM, width=7)
    # bochechas
    cheek = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    cd = ImageDraw.Draw(cheek)
    for s in (-1, 1):
        cd.ellipse([hx + s * 105 - 38, hy + 42 - 22, hx + s * 105 + 38, hy + 42 + 22], fill=(255, 150, 160, 170))
    img.alpha_composite(cheek.filter(ImageFilter.GaussianBlur(6)))
    d = ImageDraw.Draw(img)

    # olhos
    blink_phase = (t % 3.0)
    blink = 1.0
    if blink_phase > 2.85:
        blink = max(0.08, abs(blink_phase - 2.925) / 0.075)
    if mood == "sleepy":
        blink = 0.25
    ry = 44 * blink
    rx = 30 * (1.12 if mood == "wow" else 1.0)
    for s in (-1, 1):
        ex, ey = hx + s * 68, hy - 8
        d.ellipse([ex - rx, ey - ry, ex + rx, ey + ry], fill=PLUM)
        if blink > 0.5:
            d.ellipse([ex - 12 + 5 * math.sin(t * k), ey - 26, ex + 4 + 5 * math.sin(t * k), ey - 10], fill=(255, 255, 255))
            d.ellipse([ex + 6, ey + 8, ex + 16, ey + 18], fill=(255, 255, 255, 220))
    # boca
    if mood == "wow":
        d.ellipse([hx - 16, hy + 58, hx + 16, hy + 96], fill=PLUM)
    else:
        d.arc([hx - 38, hy + 38, hx + 38, hy + 92], start=15, end=165, fill=PLUM, width=8)

    # brilhos
    for i in range(7):
        ph = (t / 6.0 + i / 7.0) % 1.0
        ang = i * 2.4 + ph * 2 * math.pi
        rad = 360 + 70 * math.sin(i * 1.7)
        sx = cx + rad * math.cos(ang) * 0.95
        sy = cy + 40 + rad * math.sin(ang) * 0.75
        al = int(255 * math.sin(ph * math.pi) ** 1.5)
        _star(d, sx, sy, 16 + 6 * (i % 3), (255, 236, 160, al))

    return img.resize((size, size), Image.LANCZOS)


if __name__ == "__main__":
    draw_lume(0.0).save("/tmp/lume_test.png")


# ------------------------------------------------------------------
# Verso, o cachorrinho caramelo do Virou Versos (personagem original)
# ------------------------------------------------------------------
CARAMEL = (222, 156, 92)
CARAMEL_D = (178, 112, 58)
MUZZLE = (250, 228, 190)


def draw_verso(t=0.0, size=600, mood="happy"):
    """Retorna RGBA. Loop de 6 s (rabo 3 balanços/s, respirar, piscar)."""
    k = 2 * math.pi / 6.0
    breathe = math.sin(t * k * 2) * 6
    cx, cy = S / 2, S / 2 + 20
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # rabo (atrás)
    wag = math.sin(t * 2 * math.pi * 3)
    tip = (cx + 270 + 40 * wag, cy + 110 - 20 * abs(wag))
    pts = [(cx + 140, cy + 380), (cx + 260, cy + 340), (cx + 300 + 20 * wag, cy + 230), tip]
    d.line(pts, fill=PLUM, width=70, joint="curve")
    d.line(pts, fill=CARAMEL, width=52, joint="curve")
    d.ellipse([tip[0] - 26, tip[1] - 26, tip[0] + 26, tip[1] + 26], fill=CARAMEL)

    # corpo
    d.ellipse([cx - 195, cy + 70 + breathe * 0.3, cx + 195, cy + 440], fill=CARAMEL, outline=PLUM, width=7)
    d.ellipse([cx - 92, cy + 150, cx + 92, cy + 410], fill=MUZZLE)
    # patinhas
    for s in (-1, 1):
        d.ellipse([cx + s * 95 - 58, cy + 370, cx + s * 95 + 58, cy + 462], fill=MUZZLE, outline=PLUM, width=6)
        for q in (-1, 1):
            d.line([cx + s * 95 + q * 20, cy + 428, cx + s * 95 + q * 20, cy + 452], fill=PLUM, width=4)

    # coleira + plaquinha com o V
    d.rounded_rectangle([cx - 150, cy + 82, cx + 150, cy + 122], radius=20, fill=PLUM)
    glow_tag = _radial(S, cx, cy + 150, 120, GLOW, 1.2, 0.95)
    img.alpha_composite(glow_tag)
    d = ImageDraw.Draw(img)
    d.ellipse([cx - 40, cy + 112, cx + 40, cy + 192], fill=GOLD, outline=PLUM, width=5)
    d.polygon([(cx - 22, cy + 134), (cx - 8, cy + 134), (cx, cy + 164), (cx + 8, cy + 134), (cx + 22, cy + 134), (cx + 6, cy + 178), (cx - 6, cy + 178)], fill=PLUM)

    # orelhas caídas (mexem)
    for s in (-1, 1):
        ear = Image.new("RGBA", (300, 420), (0, 0, 0, 0))
        ImageDraw.Draw(ear).ellipse([60, 20, 240, 400], fill=CARAMEL_D, outline=PLUM, width=7)
        ang = s * (18 + 7 * math.sin(t * k * 3 + (0 if s < 0 else 1.3)))
        ear = ear.rotate(ang, resample=Image.BICUBIC, expand=False)
        img.alpha_composite(ear, (int(cx + s * 215 - 150), int(cy - 125 - 180 + breathe * 0.2)))
    d = ImageDraw.Draw(img)

    # cabeça
    hx, hy = cx, cy - 105 + breathe * 0.3
    d.ellipse([hx - 235, hy - 205, hx + 235, hy + 205], fill=CARAMEL, outline=PLUM, width=7)
    d.ellipse([hx - 40, hy - 200, hx + 40, hy - 110], fill=MUZZLE)  # listra
    d.ellipse([hx - 135, hy - 10, hx + 135, hy + 160], fill=MUZZLE)
    # bochechas
    ch = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    cd = ImageDraw.Draw(ch)
    for s in (-1, 1):
        cd.ellipse([hx + s * 170 - 36, hy + 40 - 22, hx + s * 170 + 36, hy + 40 + 22], fill=(255, 140, 150, 170))
    img.alpha_composite(ch.filter(ImageFilter.GaussianBlur(6)))
    d = ImageDraw.Draw(img)

    # sobrancelhas-pintinha
    for s in (-1, 1):
        d.ellipse([hx + s * 92 - 14, hy - 120 - 12, hx + s * 92 + 14, hy - 120 + 12], fill=MUZZLE)
    # olhos
    bp = t % 3.0
    blink = 1.0
    if bp > 2.85:
        blink = max(0.08, abs(bp - 2.925) / 0.075)
    if mood == "sleepy":
        blink = 0.25
    ry = 40 * blink
    for s in (-1, 1):
        ex, ey = hx + s * 92, hy - 55
        d.ellipse([ex - 30, ey - ry, ex + 30, ey + ry], fill=PLUM)
        if blink > 0.5:
            d.ellipse([ex - 14, ey - 26, ex + 4, ey - 8], fill=(255, 255, 255))
            d.ellipse([ex + 8, ey + 8, ex + 18, ey + 18], fill=(255, 255, 255, 220))
    # focinho
    d.ellipse([hx - 44, hy + 8, hx + 44, hy + 58], fill=PLUM)
    d.ellipse([hx - 20, hy + 14, hx + 2, hy + 26], fill=(255, 255, 255, 200))
    d.line([hx, hy + 58, hx, hy + 92], fill=PLUM, width=7)
    d.arc([hx - 62, hy + 60, hx, hy + 124], start=20, end=160, fill=PLUM, width=7)
    d.arc([hx, hy + 60, hx + 62, hy + 124], start=20, end=160, fill=PLUM, width=7)
    if mood != "sleepy":
        tl = 8 * math.sin(t * k * 6)
        d.ellipse([hx - 30, hy + 96, hx + 30, hy + 160 + tl], fill=(255, 128, 140), outline=PLUM, width=5)
        d.line([hx, hy + 100, hx, hy + 150], fill=(224, 96, 112), width=4)
    return img.resize((size, size), Image.LANCZOS)

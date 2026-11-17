import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from viz import *

W, H = 1080, 1350


def fit_lines(text, maxw, maxh, start=90, minsz=46, var="Medium Italic", ratio=1.34):
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    sz = start
    while sz >= minsz:
        f = font(LORA_I, sz, var)
        lines = wrap_text(probe, text, f, maxw)
        if len(lines) * sz * ratio <= maxh:
            return f, lines, int(sz * ratio)
        sz -= 2
    f = font(LORA_I, minsz, var)
    return f, wrap_text(probe, text, f, maxw), int(minsz * ratio)


def header(img, th, W_, x_off=0, label=True):
    """selo no topo: emblema + marca"""
    L = Image.new("RGBA", (W_, 260), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    draw_emblem(d, W_ // 2, 112, 34, th["accent"])
    f = font(INTER, 22)
    d.text((W_ // 2, 176), "V I R O U   V E R S O S", font=f, fill=th["fg"] + (215,), anchor="mm")
    rgba_over(img, np.array(L), x_off, 40)


def footer(img, th, W_, x_off, idx=None, total=None):
    L = Image.new("RGBA", (W_, 150), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    f = font(INTER_M, 24)
    d.text((W_ // 2, 40), "@virouversos", font=f, fill=th["fg"] + (200,), anchor="mm")
    if idx and total:
        bw = 360
        x0 = W_ // 2 - bw // 2
        d.line([x0, 92, x0 + bw, 92], fill=th["fg"] + (60,), width=3)
        d.line([x0, 92, x0 + bw * idx / total, 92], fill=th["accent"] + (255,), width=3)
        d.text((W_ // 2, 118), f"{idx:02d} / {total:02d}", font=font(INTER_M, 20), fill=th["accent"] + (230,), anchor="mm")
    rgba_over(img, np.array(L), x_off, H - 170)


def poem_block(img, th, text, x_off, W_=W, label=None, center_y=None):
    f, lines, lh = fit_lines(text, 820, 600)
    layer = text_layer(lines, f, W_, th["fg"], th["accent"], lh)
    hh = layer.shape[0]
    cy = center_y or H * 0.50
    y = int(cy - hh / 2)
    y = max(y, 300)
    scrim(img, W_ / 2 + x_off, y + hh / 2, 520, hh * 0.62 + 90, th.get("scrim", 0.32))
    if label:
        L = Image.new("RGBA", (W_, 120), (0, 0, 0, 0))
        d = ImageDraw.Draw(L)
        d.text((W_ // 2, 40), label, font=font(INTER, 24), fill=th["accent"] + (255,), anchor="mm")
        draw_ornament(d, W_ // 2, 86, 120, th["accent"])
        rgba_over(img, np.array(L), x_off, y - 70)
    rgba_over(img, layer, x_off, y)


def cover_block(img, th, title, x_off, W_=W):
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    sz = 132
    while sz > 70:
        f = font(LORA, sz, "Bold")
        lines = wrap_text(probe, title, f, 880)
        if len(lines) <= 3 and max(probe.textlength(l, font=f) for l in lines) <= 880:
            break
        sz -= 4
    lh = int(sz * 1.12)
    layer = text_layer(lines, f, W_, th["fg"], th["accent"], lh, glow=0.45)
    hh = layer.shape[0]
    y = int(H * 0.47 - hh / 2)
    scrim(img, W_ / 2 + x_off, y + hh / 2, 560, hh * 0.7 + 90, th.get("scrim", 0.32))
    rgba_over(img, layer, x_off, y)
    L = Image.new("RGBA", (W_, 260), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    d.text((W_ // 2, 40), th["label"], font=font(INTER, 26), fill=th["accent"] + (255,), anchor="mm")
    draw_ornament(d, W_ // 2, 92, 130, th["accent"])
    rgba_over(img, np.array(L), x_off, y - 110)
    # dica de arrastar
    L2 = Image.new("RGBA", (W_, 100), (0, 0, 0, 0))
    d2 = ImageDraw.Draw(L2)
    d2.text((W_ // 2 - 20, 40), "A R R A S T E", font=font(INTER, 24), fill=th["fg"] + (210,), anchor="mm")
    ax = W_ // 2 + 100
    d2.line([ax, 40, ax + 46, 40], fill=th["accent"] + (255,), width=4)
    d2.line([ax + 34, 28, ax + 48, 40, ax + 34, 52], fill=th["accent"] + (255,), width=4)
    rgba_over(img, np.array(L2), x_off, int(H * 0.68))


def cta_block(img, th, x_off, W_=W):
    L = Image.new("RGBA", (W_, 760), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    d.text((W_ // 2, 90), "Gostou?", font=font(LORA, 104, "Bold"), fill=th["fg"] + (255,), anchor="mm")
    draw_ornament(d, W_ // 2, 190, 140, th["accent"])
    cx = W_ // 2
    icon_heart(d, cx - 220, 330, 78, th["accent"])
    icon_bookmark(d, cx, 330, 80, th["accent"])
    icon_send(d, cx + 220, 330, 80, th["accent"])
    for i, t in enumerate(["Curta", "Salve", "Envie"]):
        d.text((cx - 220 + 220 * i, 420), t, font=font(INTER_M, 28), fill=th["fg"] + (225,), anchor="mm")
    d.text((cx, 560), "Siga para mais versos", font=font(LORA_I, 50, "Medium Italic"), fill=th["fg"] + (235,), anchor="mm")
    d.text((cx, 650), "@virouversos", font=font(INTER, 56), fill=th["fg"] + (255,), anchor="mm")
    # sombra
    alpha = L.split()[3]
    sh = Image.new("RGBA", L.size, (0, 0, 0, 0))
    sh.putalpha(alpha.filter(ImageFilter.GaussianBlur(14)).point(lambda v: int(v * 0.5)))
    out = Image.alpha_composite(sh, L)
    scrim(img, W_ / 2 + x_off, H * 0.5 - 40, 520, 330, 0.5)
    rgba_over(img, np.array(out), x_off, int(H * 0.5 - 400))


def render_single(theme, title, text, out_path, seed=11):
    base, layers, th = build_scene(theme, W, H, seed=seed)
    img = composite_static(base, layers, th, W, H)
    header(img, th, W, 0)
    poem_block(img, th, text, 0, label=title.upper())
    footer(img, th, W, 0)
    fin = finish(img, grain_pool(H, W, 1, 6.5, seed)[0], vignette(H, W, 0.38))
    Image.fromarray(fin).save(out_path, optimize=True)


def render_carousel(theme, title, slides, out_dir, seed=21):
    """slides: lista de textos (sem 'Slide N:' e sem @virouversos). Gera capa + versos + CTA."""
    n = len(slides) + 2
    PW = W * n
    base, layers, th = build_scene(theme, PW, H, seed=seed, tiles=n)
    pano = composite_static(base, layers, th, PW, H, Wt=W)
    os.makedirs(out_dir, exist_ok=True)
    grain = grain_pool(H, W, 1, 6.5, seed)[0]
    vig = vignette(H, W, 0.38)
    for i in range(n):
        crop = pano[:, i * W:(i + 1) * W].copy()
        header(crop, th, W, 0)
        if i == 0:
            cover_block(crop, th, title, 0)
        elif i == n - 1:
            cta_block(crop, th, 0)
        else:
            poem_block(crop, th, slides[i - 1], 0)
        if 0 < i < n - 1:
            footer(crop, th, W, 0, idx=i + 1, total=n)
        else:
            footer(crop, th, W, 0)
        Image.fromarray(finish(crop, grain, vig)).save(f"{out_dir}/slide_{i + 1:02d}.png", optimize=True)
    return n


if __name__ == "__main__":
    os.makedirs("/tmp/out/v2/test", exist_ok=True)
    tests = [
        ("1. Ruídos do Agora", "Café frio", "O café esfriou no balcão\nenquanto o dia me puxava pelo braço.\nHá pausas que só chegam\nquando a gente esquece de pedir."),
        ("2. Cidade em Verso", "Fila do pão", "Na fila do pão cabe o bairro inteiro:\na pressa do moço, o bom-dia da senhora,\na conversa que ninguém começou.\nA cidade é isso:\ngente esperando junto\nsem saber que é companhia."),
        ("3. O que a gente não diz", "Silêncio", "Nem todo silêncio é paz.\nAlguns são palavras\nque cansaram de esperar a coragem."),
        ("4. Fecha o Ano em Verso", "Pequenas vitórias", "Levantar da cama já foi poema.\nResponder aquela mensagem, verso.\nO ano pesou,\ne você ainda escreve."),
    ]
    for i, (th, t, tx) in enumerate(tests, 1):
        render_single(th, t, tx, f"/tmp/out/v2/test/single_{i}.png")
        print("ok", i)

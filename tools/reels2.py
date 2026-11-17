import sys, os, math, random, subprocess, wave
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from viz import *

W, H = 1080, 1920
FPS = 30
PAN = 420


def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def crop_rows(pil):
    arr = np.array(pil)
    rows = np.where(arr[..., 3].max(axis=1) > 0)[0]
    if len(rows) == 0:
        return None
    y0, y1 = int(rows[0]), int(rows[-1]) + 1
    return arr[y0:y1], y0


def prep_layer(arr):
    return arr[..., :3].astype(np.float32), (arr[..., 3:4].astype(np.float32) / 255.0)


def blend(frame, rgb, al, y0, k):
    if k <= 0.003:
        return
    h = rgb.shape[0]
    ya, yb = max(0, int(y0)), min(H, int(y0) + h)
    if yb <= ya:
        return
    sa = ya - int(y0)
    sb = sa + (yb - ya)
    a = al[sa:sb] * k
    frame[ya:yb] = frame[ya:yb] * (1 - a) + rgb[sa:sb] * a


# ---------------------------------------------------------------- áudio
ROOTS = {"waves": (146.83, "minor"), "city": (110.0, "major"), "moon": (130.81, "minor"), "sunrise": (98.0, "major")}
PENT = {"major": [0, 2, 4, 7, 9], "minor": [0, 3, 5, 7, 10]}


def synth_audio(path, dur, chimes, key, seed=3):
    sr = 44100
    n = int(dur * sr)
    t = np.arange(n) / sr
    root, mode = ROOTS[key]
    rng = random.Random(seed)
    # pad suave
    pad = np.zeros(n)
    for mult, lvl in [(1, 0.10), (1.5, 0.07), (2, 0.06), (2.0 * (2 ** (PENT[mode][1] / 12)), 0.04)]:
        for det in (-0.6, 0.6):
            f = root * mult + det
            lfo = 0.65 + 0.35 * np.sin(2 * math.pi * (0.07 + 0.03 * mult) * t + rng.uniform(0, 6))
            pad += lvl * lfo * np.sin(2 * math.pi * f * t)
    fade = np.minimum(1, t / 3.0) * np.minimum(1, (dur - t) / 3.5)
    pad *= fade
    # sinos (notas da pentatônica a cada verso)
    bell = np.zeros(n)
    idx = 2
    for t0 in chimes:
        idx = max(0, min(9, idx + rng.choice([-2, -1, 1, 2, 3])))
        semis = PENT[mode][idx % 5] + 12 * (idx // 5)
        f = root * 4 * (2 ** (semis / 12))
        i0 = int(t0 * sr)
        m = min(n - i0, int(4.5 * sr))
        if m <= 0:
            continue
        tt = np.arange(m) / sr
        env = np.exp(-tt * 1.9) * (1 - np.exp(-tt * 90))
        tone = np.sin(2 * math.pi * f * tt) + 0.28 * np.sin(2 * math.pi * f * 2.01 * tt) + 0.10 * np.sin(2 * math.pi * f * 3.99 * tt)
        bell[i0:i0 + m] += 0.16 * env * tone
    # eco
    def delay(x, sec, g):
        d = int(sec * sr)
        y = np.zeros_like(x)
        y[d:] = x[:-d] * g
        return y
    bell_e = bell + delay(bell, 0.37, 0.38) + delay(bell, 0.74, 0.2) + delay(bell, 1.2, 0.1)
    L = pad + bell_e
    R = pad + delay(bell_e, 0.012, 1.0) * 0.95
    st = np.stack([L, R], 1)
    st = st / max(1e-6, np.abs(st).max()) * 0.55
    pcm = (st * 32767).astype(np.int16)
    with wave.open(path, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(pcm.tobytes())


# ---------------------------------------------------------------- construção do reel
def build_reel(theme_name, title, stanzas, out_mp4, label=None, seed=5, preview=None, cta_lines=None):
    th = THEMES[theme_name]
    key = th["key"]
    rng = random.Random(seed)
    base, layers, _ = build_scene(theme_name, W, H, seed=seed, pan_margin=PAN)
    frame0 = base.copy()
    if "stars" in layers:
        rgba_over(frame0, np.array(layers["stars"][0]), 0, 0)
    scrim(frame0, W / 2, H * 0.50, 580, 560, th.get("scrim", 0.30))
    vig = vignette(H, W, 0.40)
    grains = grain_pool(H, W, 6, 2.6, seed)

    # camadas móveis
    cfg = {"city": [("far", 1, 5), ("mid", 1, 9), ("near", 1, 14)],
           "moon": [("ridge_far", 1, 3), ("fog2", -1, 7), ("ridge_near", 1, 6), ("fog1", 1, 11)],
           "sunrise": [("hill_far", 1, 3), ("bokeh", -1, 9), ("hill_near", 1, 6)],
           "waves": []}[key]
    moving = []
    for name, d, sp in cfg:
        c = crop_rows(layers[name])
        if c:
            moving.append((c[0], c[1], d, sp))

    # estrelas que piscam
    twink = []
    if "stars" in layers:
        pts = [p for p in layers["stars"][1] if p[2] >= 2][:60]
        for (x, y, r) in pts:
            twink.append((x, y, rng.uniform(0, 6.28), rng.uniform(0.6, 1.6)))
    star_sp = sprite_glow(9, (255, 250, 240))

    # partículas
    acc = th["accent"]
    sprites = {r: sprite_glow(r, acc) for r in (6, 9, 14, 22)}
    parts = []
    for _ in range(46):
        r = rng.choice([6, 6, 9, 9, 14, 22])
        up = -1 if key == "moon" else 1
        parts.append(dict(x=rng.uniform(0, W), y=rng.uniform(0, H), r=r, vy=up * rng.uniform(10, 34) * (0.6 + r / 22),
                          vx=rng.uniform(-8, 8), ph=rng.uniform(0, 6.28), sp=rng.uniform(0.4, 1.2)))

    # --- timeline
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    fp = font(LORA_I, 76, "Medium Italic")
    lh = int(76 * 1.36)
    gap = 26
    T_TITLE = 3.0
    t = 0.2
    events = []
    chimes = []
    title_ev = dict(t0=t, t1=t + T_TITLE)
    chimes.append(t + 0.4)
    t = title_ev["t1"] + 0.1
    scenes = []
    for st in stanzas:
        verses = []
        total = 0
        for v in st:
            lines = wrap_text(probe, v, fp, 880)
            verses.append(lines)
            total += len(lines) * lh
        total += gap * (len(st) - 1)
        top = int(H * 0.50 - total / 2)
        y = top
        vs = []
        for i, lines in enumerate(verses):
            arr = text_layer(lines, fp, W, th["fg"], th["accent"], lh, pad=60)
            rgb, al = prep_layer(arr)
            vs.append(dict(rgb=rgb, al=al, y=y - 60, ts=t + i * 2.1))
            chimes.append(t + i * 2.1 + 0.15)
            y += len(lines) * lh + gap
        t_end = t + (len(st) - 1) * 2.1 + 0.9 + 2.3
        scenes.append(dict(v=vs, t0=t, t1=t_end))
        t = t_end + 0.5
    T_OUT0 = t
    T_OUT1 = t + 4.0
    chimes.append(T_OUT0 + 0.5)
    dur = T_OUT1 + 0.8

    # título
    f_title = None
    sz = 128
    while sz > 70:
        f_title = font(LORA, sz, "Bold")
        tl = wrap_text(probe, title, f_title, 880)
        if len(tl) <= 2 and max(probe.textlength(x, font=f_title) for x in tl) <= 880:
            break
        sz -= 4
    tarr = text_layer(tl, f_title, W, th["fg"], th["accent"], int(sz * 1.12), glow=0.5)
    t_rgb, t_al = prep_layer(tarr)
    t_y = int(H * 0.47 - tarr.shape[0] / 2)
    Lb = Image.new("RGBA", (W, 200), (0, 0, 0, 0))
    db = ImageDraw.Draw(Lb)
    db.text((W // 2, 40), label or th["label"], font=font(INTER, 27), fill=th["accent"] + (255,), anchor="mm")
    draw_ornament(db, W // 2, 96, 140, th["accent"])
    lb_rgb, lb_al = prep_layer(np.array(Lb))
    lb_y = t_y - 90

    # cabeçalho / rodapé
    Hd = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(Hd)
    draw_emblem(hd, W // 2, 345, 36, th["accent"])
    hd.text((W // 2, 412), "V I R O U   V E R S O S", font=font(INTER, 22), fill=th["fg"] + (215,), anchor="mm")
    hd.text((W // 2, 1500), "@virouversos", font=font(INTER_M, 26), fill=th["fg"] + (200,), anchor="mm")
    hd_rgb, hd_al = prep_layer(np.array(Hd))

    # outro (CTA)
    Co = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(Co)
    cy0 = int(H * 0.5 - 320)
    cd.text((W // 2, cy0), "Gostou?", font=font(LORA, 104, "Bold"), fill=th["fg"] + (255,), anchor="mm")
    draw_ornament(cd, W // 2, cy0 + 100, 140, th["accent"])
    cx = W // 2
    icon_heart(cd, cx - 220, cy0 + 235, 78, th["accent"])
    icon_bookmark(cd, cx, cy0 + 235, 80, th["accent"])
    icon_send(cd, cx + 220, cy0 + 235, 80, th["accent"])
    for i, tx in enumerate(["Curta", "Salve", "Envie"]):
        cd.text((cx - 220 + 220 * i, cy0 + 325), tx, font=font(INTER_M, 28), fill=th["fg"] + (225,), anchor="mm")
    for i, tx in enumerate(cta_lines or ["Siga para mais versos"]):
        cd.text((cx, cy0 + 450 + 60 * i), tx, font=font(LORA_I, 50, "Medium Italic"), fill=th["fg"] + (235,), anchor="mm")
    cd.text((cx, cy0 + 560), "@virouversos", font=font(INTER, 58), fill=th["fg"] + (255,), anchor="mm")
    co_rgb, co_al = prep_layer(np.array(Co))
    # sombra do outro
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh.putalpha(Co.split()[3].filter(ImageFilter.GaussianBlur(14)).point(lambda v: int(v * 0.5)))
    sh_rgb, sh_al = prep_layer(np.array(sh))

    glow_sp = sprite_glow(560, th["glows"][0][3]) if key in ("sunrise", "city") else None
    glow_pos = (W * 0.5, H * 0.80) if key == "sunrise" else (W * 0.72, H * 0.73)
    wave_h = int(H * 0.62)
    wave_y0 = int(H * 0.58 - wave_h / 2)

    def render(tm):
        f = frame0.copy()
        # brilho pulsante
        if glow_sp is not None:
            blit_add(f, glow_sp, glow_pos[0], glow_pos[1], 0.10 + 0.07 * math.sin(tm * 0.8))
        if key == "waves":
            Lw = Image.new("RGBA", (W, wave_h), (0, 0, 0, 0))
            waves_draw(Lw, W, wave_h, tm, th, cy=wave_h / 2, amp=H * 0.075)
            gl = np.array(Lw.filter(ImageFilter.GaussianBlur(7)), np.float32)
            f[wave_y0:wave_y0 + wave_h] += gl[..., :3] * (gl[..., 3:4] / 255.0) * 1.4
            rgba_over(f, np.array(Lw), 0, wave_y0)
        # estrelas piscando
        for (x, y, ph, sp) in twink:
            k = 0.5 + 0.5 * math.sin(tm * sp + ph)
            blit_add(f, star_sp, x, y, 0.55 * k)
        # camadas com paralaxe
        for arr, y0, d, sp in moving:
            ox = (sp * tm) if d > 0 else (PAN - sp * tm)
            rgba_over(f, arr, -int(ox), y0)
        # partículas
        for p in parts:
            x = (p["x"] + p["vx"] * tm + 18 * math.sin(tm * 0.6 * p["sp"] + p["ph"])) % W
            y = (p["y"] - p["vy"] * tm) % H
            k = 0.25 + 0.55 * (0.5 + 0.5 * math.sin(tm * p["sp"] * 1.4 + p["ph"]))
            blit_add(f, sprites[p["r"]], x, y, k * (0.55 if p["r"] >= 14 else 1.0))
        # cabeçalho e rodapé
        blend(f, hd_rgb, hd_al, 0, ease((tm - 0.1) / 0.8) * (1 - ease((tm - (T_OUT1 - 0.3)) / 0.6) * 0.0))
        # título
        a_t = ease((tm - title_ev["t0"]) / 0.9) * (1 - ease((tm - (title_ev["t1"] - 0.7)) / 0.7))
        if a_t > 0:
            rise = (1 - ease((tm - title_ev["t0"]) / 0.9)) * 30
            blend(f, t_rgb, t_al, t_y + rise, a_t)
            blend(f, lb_rgb, lb_al, lb_y + rise, a_t)
        # cenas
        for sc in scenes:
            fade_out = 1 - ease((tm - (sc["t1"] - 0.7)) / 0.7)
            if tm < sc["t0"] or tm > sc["t1"]:
                continue
            for v in sc["v"]:
                if tm < v["ts"]:
                    continue
                e = ease((tm - v["ts"]) / 0.9)
                blend(f, v["rgb"], v["al"], v["y"] + (1 - e) * 34, e * fade_out)
        # outro
        if tm >= T_OUT0:
            a_o = ease((tm - T_OUT0) / 0.9)
            pulse = 1.0 + 0.012 * math.sin(tm * 2.0)
            blend(f, sh_rgb, sh_al, 0, a_o)
            blend(f, co_rgb, co_al, 0, a_o)
        f *= vig
        f += grains[int(tm * 15) % 6]
        return np.clip(f, 0, 255).astype(np.uint8)

    if preview is not None:
        for pt in preview:
            Image.fromarray(render(pt)).save(f"/tmp/reel_prev_{int(pt * 10):04d}.png")
        return dur

    wav = out_mp4.replace(".mp4", ".wav")
    synth_audio(wav, dur, chimes, key, seed)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-i", wav, "-c:v", "libx264", "-preset", "veryfast", "-crf", "24", "-maxrate", "6M", "-bufsize", "12M", "-pix_fmt", "yuv420p", "-r", str(FPS),
           "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", out_mp4]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    nfr = int(dur * FPS)
    for i in range(nfr):
        p.stdin.write(render(i / FPS).tobytes())
    p.stdin.close()
    p.wait()
    os.remove(wav)
    return dur


if __name__ == "__main__":
    os.makedirs("/tmp", exist_ok=True)
    stanzas = [["Sem cola, sem agulha,", "só nó em retalho de pano."],
               ["Cada nó, um abraço", "que ninguém precisou explicar."],
               ["Abayomi:", "encontro precioso."],
               ["Hoje, no Dia da Consciência Negra,", "lembramos que a memória", "também se faz com as mãos."]]
    d = build_reel("2. Cidade em Verso", "Abayomi", stanzas, "/tmp/x.mp4", label="20 DE NOVEMBRO · CONSCIÊNCIA NEGRA",
                   preview=[1.5, 5.0, 9.0, 20.5, 25.0])
    print("dur", d)

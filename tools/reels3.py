"""Reels v3 (modelo 'narrado'): nome do famoso gigante no quadro 0 + pergunta falada,
voz humana sincronizada com o texto, cada frase parada 3-4 s com fade suave (sem corte rapido),
barra de progresso, CTA falado e final em loop.
Uso: build_reel3(...). Tempos dos segmentos vem da narracao (ffmpeg silencedetect)."""
import sys, os, math, random, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reels2 import *  # noqa: F401,F403  (viz helpers, ease, blend, synth_audio...)

FADE = 0.55  # fade longo e suave entre frases


# ---------------------------------------------------------------- trilha original (piano suave + pad)
MOODS = {
    # (nota raiz MIDI, acordes como graus em semitons + qualidade, bpm)
    "hope": dict(root=60, bpm=84, prog=[(0, "M"), (7, "M"), (9, "m"), (5, "M")]),     # C G Am F
    "calm": dict(root=57, bpm=66, prog=[(0, "m"), (8, "M"), (3, "M"), (10, "M")]),    # Am F C G
    "rise": dict(root=62, bpm=78, prog=[(0, "M"), (9, "m"), (5, "M"), (7, "M")]),     # D Bm G A
}
TRI = {"M": [0, 4, 7], "m": [0, 3, 7]}


def _mf(m):
    return 440.0 * 2 ** ((m - 69) / 12.0)


def synth_music(path, dur, mood="hope", seed=3):
    sr = 44100
    n = int(dur * sr)
    cfg = MOODS[mood]
    rng = random.Random(seed)
    beat = 60.0 / cfg["bpm"]
    bar = 4 * beat
    out = np.zeros(n)
    pad = np.zeros(n)
    t_all = np.arange(n) / sr

    def pluck(freq, t0, ln, amp):
        i0 = int(t0 * sr)
        m = min(n - i0, int(ln * sr))
        if m <= 0:
            return
        tt = np.arange(m) / sr
        env = np.exp(-tt * 2.6) * (1 - np.exp(-tt * 220))
        tone = np.sin(2 * math.pi * freq * tt) + 0.35 * np.sin(2 * math.pi * freq * 2 * tt) * np.exp(-tt * 4) \
            + 0.12 * np.sin(2 * math.pi * freq * 3 * tt) * np.exp(-tt * 7)
        out[i0:i0 + m] += amp * env * tone

    nbars = int(dur / bar) + 1
    for b in range(nbars):
        deg, q = cfg["prog"][b % len(cfg["prog"])]
        base = cfg["root"] + deg
        notes = [base + x for x in TRI[q]]
        t0 = b * bar
        # baixo (nota raiz, oitava abaixo) no 1o tempo
        pluck(_mf(base - 12), t0, bar * 0.95, 0.20)
        # arpejo em colcheias
        pat = [0, 1, 2, 1, 2, 1, 0, 1] if mood != "calm" else [0, 2, 1, 2, 0, 2, 1, 2]
        for k, idx in enumerate(pat):
            tt0 = t0 + k * beat * 0.5
            if tt0 >= dur:
                break
            nt = notes[idx % 3] + (12 if idx == 2 and k % 4 == 2 else 0)
            vel = 0.16 + 0.05 * (k % 2 == 0) + rng.uniform(-0.015, 0.015)
            pluck(_mf(nt + 12), tt0 + rng.uniform(0, 0.012), 2.2, vel)
        # pad suave sustentando o acorde
        i0 = int(t0 * sr)
        m = min(n - i0, int((bar + 0.6) * sr))
        if m > 0:
            tt = np.arange(m) / sr
            env = np.minimum(1, tt / 0.9) * np.minimum(1, (bar + 0.6 - tt) / 0.9)
            for x in notes:
                for det in (-0.5, 0.5):
                    pad[i0:i0 + m] += 0.035 * env * np.sin(2 * math.pi * (_mf(x) + det) * tt)
    fade = np.minimum(1, t_all / 1.2) * np.minimum(1, (dur - t_all) / 2.0)
    mono = (out + pad) * fade

    def delay(x, sec, g):
        d = int(sec * sr)
        y = np.zeros_like(x)
        y[d:] = x[:-d] * g
        return y
    wet = mono + delay(mono, beat * 0.75, 0.30) + delay(mono, beat * 1.5, 0.16)
    L = wet
    R = wet + delay(wet, 0.015, 1.0) * 0.9
    st = np.stack([L, R], 1)
    st = st / max(1e-6, np.abs(st).max()) * 0.8
    import wave
    pcm = (st * 32767).astype(np.int16)
    with wave.open(path, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(pcm.tobytes())


def build_reel3(theme_name, name, question, segs, cta_from, narr_mp3, narr_dur, out_mp4,
                tag=None, cta_lines=None, cta_title="Salve e envie", seed=5, preview=None, loop_tail=1.6, mood="hope", music_vol=0.55, photo=None):
    """segs: [(texto, t0)] das frases do poema (fim = t0 da proxima; ultima termina em cta_from)."""
    th = THEMES[theme_name]
    key = th["key"]
    rng = random.Random(seed)
    base, layers, _ = build_scene(theme_name, W, H, seed=seed, pan_margin=PAN)
    frame0 = base.copy()
    if "stars" in layers:
        rgba_over(frame0, np.array(layers["stars"][0]), 0, 0)
    scrim(frame0, W / 2, H * 0.50, 600, 600, th.get("scrim", 0.30) + 0.08)
    vig = vignette(H, W, 0.40)
    grains = grain_pool(H, W, 6, 2.6, seed)
    cfg = {"city": [("far", 1, 5), ("mid", 1, 9), ("near", 1, 14)],
           "moon": [("ridge_far", 1, 3), ("fog2", -1, 7), ("ridge_near", 1, 6), ("fog1", 1, 11)],
           "sunrise": [("hill_far", 1, 3), ("bokeh", -1, 9), ("hill_near", 1, 6)],
           "waves": []}[key]
    moving = []
    for nm, d, sp in cfg:
        c = crop_rows(layers[nm])
        if c:
            moving.append((c[0], c[1], d, sp))
    twink = []
    if "stars" in layers:
        pts = [p for p in layers["stars"][1] if p[2] >= 2][:60]
        for (x, y, r) in pts:
            twink.append((x, y, rng.uniform(0, 6.28), rng.uniform(0.6, 1.6)))
    star_sp = sprite_glow(9, (255, 250, 240))
    acc = th["accent"]
    sprites = {r: sprite_glow(r, acc) for r in (6, 9, 14, 22)}
    parts = []
    for _ in range(40):
        r = rng.choice([6, 6, 9, 9, 14, 22])
        up = -1 if key == "moon" else 1
        parts.append(dict(x=rng.uniform(0, W), y=rng.uniform(0, H), r=r, vy=up * rng.uniform(10, 30) * (0.6 + r / 22),
                          vx=rng.uniform(-8, 8), ph=rng.uniform(0, 6.28), sp=rng.uniform(0.4, 1.2)))

    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    dur = narr_dur + loop_tail + 0.6
    T_LOOP = narr_dur + 0.5  # a partir daqui o gancho volta (fim emenda no inicio)

    # ---- gancho (quadro 0): NOME grande + pergunta
    f_name = None
    sz = 200
    while sz > 90:
        f_name = font(LORA, sz, "Bold")
        if probe.textlength(name.upper(), font=f_name) <= 900:
            break
        sz -= 6
    nm_arr = text_layer([name.upper()], f_name, W, acc, acc, int(sz * 1.1), glow=0.9, pad=70)
    nm_rgb, nm_al = prep_layer(nm_arr)
    f_q = font(LORA_I, 84, "Medium Italic")
    q_lines = wrap_text(probe, question, f_q, 880)
    q_arr = text_layer(q_lines, f_q, W, th["fg"], th["accent"], int(84 * 1.3), pad=60)
    q_rgb, q_al = prep_layer(q_arr)
    gap_h = 30
    tot = nm_arr.shape[0] + gap_h + q_arr.shape[0]
    y_nm = int(H * 0.47 - tot / 2)
    y_q = y_nm + nm_arr.shape[0] + gap_h
    hook_end = segs[0][1] - 0.15 if segs else 3.0
    ph_rgb = ph_al = None
    if photo:
        # foto fornecida/autorizada pelo dono: recorte quadrado em circulo com anel na cor de destaque
        D = 380
        im = Image.open(photo).convert("RGB")
        w0, h0 = im.size
        side = min(w0, h0)
        cx0 = int(w0 * 0.49 - side / 2)
        cx0 = max(0, min(w0 - side, cx0))
        im = im.crop((cx0, 0, cx0 + side, side)).resize((D, D), Image.LANCZOS)
        PW = D + 120
        Ph = Image.new("RGBA", (PW, PW), (0, 0, 0, 0))
        glow = Image.new("RGBA", (PW, PW), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow)
        gd.ellipse((50, 50, PW - 50, PW - 50), fill=tuple(acc) + (170,))
        glow = glow.filter(ImageFilter.GaussianBlur(22))
        Ph.alpha_composite(glow)
        ring = Image.new("RGBA", (PW, PW), (0, 0, 0, 0))
        ImageDraw.Draw(ring).ellipse((60 - 8, 60 - 8, PW - 60 + 8, PW - 60 + 8), fill=tuple(acc) + (255,))
        Ph.alpha_composite(ring)
        mk = Image.new("L", (D, D), 0)
        ImageDraw.Draw(mk).ellipse((0, 0, D - 1, D - 1), fill=255)
        Ph.paste(im, (60, 60), mk)
        Pw = Image.new("RGBA", (W, PW), (0, 0, 0, 0))
        Pw.alpha_composite(Ph, ((W - PW) // 2, 0))
        ph_rgb, ph_al = prep_layer(np.array(Pw))
        ph_y = 400
        y_nm += 230
        y_q += 230

    # ---- frases do poema
    fp = font(LORA_I, 80, "Medium Italic")
    lh = int(80 * 1.34)
    scenes = []
    for i, (txt, t0) in enumerate(segs):
        t1 = segs[i + 1][1] if i + 1 < len(segs) else cta_from
        lines = wrap_text(probe, txt, fp, 880)
        arr = text_layer(lines, fp, W, th["fg"], th["accent"], lh, pad=60)
        rgb, al = prep_layer(arr)
        scenes.append(dict(rgb=rgb, al=al, y=int(H * 0.50 - arr.shape[0] / 2), t0=t0, t1=t1))

    # ---- cabecalho / rodape
    Hd = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(Hd)
    draw_emblem(hd, W // 2, 345, 36, th["accent"])
    hd.text((W // 2, 412), "V I R O U   V E R S O S", font=font(INTER, 22), fill=th["fg"] + (215,), anchor="mm")
    if tag:
        hd.text((W // 2, 470), tag, font=font(INTER_M, 26), fill=th["accent"] + (235,), anchor="mm")
    hd.text((W // 2, 1500), "@virouversos", font=font(INTER_M, 26), fill=th["fg"] + (200,), anchor="mm")
    hd_rgb, hd_al = prep_layer(np.array(Hd))

    # ---- CTA
    Co = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(Co)
    cy0 = int(H * 0.5 - 320)
    cd.text((W // 2, cy0), cta_title, font=font(LORA, 96, "Bold"), fill=th["fg"] + (255,), anchor="mm")
    draw_ornament(cd, W // 2, cy0 + 100, 140, th["accent"])
    cx = W // 2
    icon_bookmark(cd, cx - 140, cy0 + 235, 80, th["accent"])
    icon_send(cd, cx + 140, cy0 + 235, 80, th["accent"])
    for i, tx in enumerate(["Salve", "Envie"]):
        cd.text((cx - 140 + 280 * i, cy0 + 325), tx, font=font(INTER_M, 28), fill=th["fg"] + (225,), anchor="mm")
    for i, tx in enumerate(cta_lines or ["Conta nos comentários"]):
        cd.text((cx, cy0 + 450 + 60 * i), tx, font=font(LORA_I, 50, "Medium Italic"), fill=th["fg"] + (235,), anchor="mm")
    cd.text((cx, cy0 + 450 + 60 * len(cta_lines or [0]) + 50), "@virouversos", font=font(INTER, 58), fill=th["fg"] + (255,), anchor="mm")
    co_rgb, co_al = prep_layer(np.array(Co))
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh.putalpha(Co.split()[3].filter(ImageFilter.GaussianBlur(14)).point(lambda v: int(v * 0.5)))
    sh_rgb, sh_al = prep_layer(np.array(sh))

    glow_sp = sprite_glow(560, th["glows"][0][3]) if key in ("sunrise", "city") else None
    glow_pos = (W * 0.5, H * 0.80) if key == "sunrise" else (W * 0.72, H * 0.73)
    wave_h = int(H * 0.62)
    wave_y0 = int(H * 0.58 - wave_h / 2)

    def render(tm):
        f = frame0.copy()
        if glow_sp is not None:
            blit_add(f, glow_sp, glow_pos[0], glow_pos[1], 0.10 + 0.07 * math.sin(tm * 0.8))
        if key == "waves":
            Lw = Image.new("RGBA", (W, wave_h), (0, 0, 0, 0))
            waves_draw(Lw, W, wave_h, tm, th, cy=wave_h / 2, amp=H * 0.075)
            gl = np.array(Lw.filter(ImageFilter.GaussianBlur(7)), np.float32)
            f[wave_y0:wave_y0 + wave_h] += gl[..., :3] * (gl[..., 3:4] / 255.0) * 1.4
            rgba_over(f, np.array(Lw), 0, wave_y0)
        for (x, y, ph, sp) in twink:
            k = 0.5 + 0.5 * math.sin(tm * sp + ph)
            blit_add(f, star_sp, x, y, 0.55 * k)
        for arr, y0, d, sp in moving:
            ox = (sp * tm) if d > 0 else (PAN - sp * tm)
            rgba_over(f, arr, -int(ox), y0)
        for p in parts:
            x = (p["x"] + p["vx"] * tm + 18 * math.sin(tm * 0.6 * p["sp"] + p["ph"])) % W
            y = (p["y"] - p["vy"] * tm) % H
            k = 0.25 + 0.55 * (0.5 + 0.5 * math.sin(tm * p["sp"] * 1.4 + p["ph"]))
            blit_add(f, sprites[p["r"]], x, y, k * (0.55 if p["r"] >= 14 else 1.0))
        blend(f, hd_rgb, hd_al, 0, 1.0)
        # gancho: visivel desde o quadro 0 (sem fade de entrada); some devagar; volta no loop
        a_h = 1 - ease((tm - hook_end) / FADE)
        if tm >= T_LOOP:
            a_h = ease((tm - T_LOOP) / FADE)
        if a_h > 0:
            pulse = 1.0 + 0.02 * math.sin(tm * 2.2)
            if ph_rgb is not None:
                blend(f, ph_rgb, ph_al, ph_y, a_h)
            blend(f, nm_rgb, nm_al, y_nm, a_h)
            blend(f, q_rgb, q_al, y_q, a_h)
        # frases (fade suave)
        for sc in scenes:
            if tm < sc["t0"] - 0.05 or tm > sc["t1"] + 0.05:
                continue
            a_in = ease((tm - sc["t0"]) / FADE)
            a_out = 1 - ease((tm - (sc["t1"] - FADE)) / FADE)
            blend(f, sc["rgb"], sc["al"], sc["y"] + (1 - a_in) * 18, min(a_in, a_out))
        # CTA
        if cta_from <= tm:
            a_o = ease((tm - cta_from) / FADE) * (1 - ease((tm - T_LOOP) / FADE))
            blend(f, sh_rgb, sh_al, 0, a_o)
            blend(f, co_rgb, co_al, 0, a_o)
        # barra de progresso fina
        pw = int(W * 0.5 * min(1.0, tm / dur))
        x0 = W // 4
        f[1560:1564, x0:x0 + W // 2] = f[1560:1564, x0:x0 + W // 2] * 0.7 + 60
        f[1560:1564, x0:x0 + pw] = np.array(acc, np.float32)
        f *= vig
        f += grains[int(tm * 15) % 6]
        return np.clip(f, 0, 255).astype(np.uint8)

    if preview is not None:
        for pt in preview:
            Image.fromarray(render(pt)).save(f"{out_mp4}.prev_{int(pt * 10):04d}.png")
        return dur

    pad = out_mp4.replace(".mp4", "_pad.wav")
    synth_music(pad, dur, mood, seed)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-i", pad, "-i", narr_mp3,
           "-filter_complex", "[1:a]volume=" + str(music_vol) + "[m];[2:a]volume=1.25,asplit=2[n][sc];[m][sc]sidechaincompress=threshold=0.02:ratio=9:attack=25:release=500[mc];[mc][n]amix=inputs=2:duration=longest:normalize=0,alimiter=limit=0.95[a]",
           "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-maxrate", "6M", "-bufsize", "12M",
           "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "aac", "-b:a", "160k", "-t", f"{dur:.2f}", "-movflags", "+faststart", out_mp4]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(int(dur * FPS)):
        p.stdin.write(render(i / FPS).tobytes())
    p.stdin.close()
    p.wait()
    os.remove(pad)
    return dur

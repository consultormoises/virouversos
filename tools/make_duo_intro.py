import sys, subprocess, math, numpy as np
sys.path.insert(0, "/home/claude/virouversos/tools")
from viz import *
from mascot import draw_lume, draw_verso
from PIL import Image, ImageDraw

W, H, FPS, DUR = 1080, 1920, 30, 6
base, layers, th = build_scene("3. O que a gente não diz", W, H, seed=12)
bg = composite_static(base, layers, th, W, H)
bgfin = finish(bg.copy(), grain_pool(H, W, 1, 6.5, 12)[0], vignette(H, W, 0.45)).astype(np.float32)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
f1 = font(LORA, 92, "Bold"); f2 = font(LORA_I, 46, "Medium Italic"); f3 = font(INTER, 32)
warm = np.array([255, 214, 130], np.float32)
out = sys.argv[1]
p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                      "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
for i in range(FPS * DUR):
    t = i / FPS
    ang = 2 * math.pi * t / DUR
    lx, ly = 540 + 235 * math.cos(ang), 700 + 100 * math.sin(2 * ang)
    pulse = 0.85 + 0.15 * math.sin(2 * math.pi * 3 * t / DUR * 3)
    # luz ao redor do Lume
    d2 = (xx - lx) ** 2 + (yy - ly) ** 2
    Ls = np.exp(-d2 / (2 * 330.0 ** 2)) * pulse
    Lb = np.exp(-d2 / (2 * 170.0 ** 2)) * pulse
    frame = bgfin.copy()
    # relumina o fundo
    frame = frame * (1 + 0.35 * Ls[..., None]) + warm * 0.30 * Ls[..., None] * 0.5
    # Verso (reluminado pela luz do Lume)
    dog = draw_verso(t, 900, "happy")
    dog_arr = np.asarray(dog).astype(np.float32)
    ox, oy = 90, 800
    sub = np.zeros((H, W, 4), np.float32)
    sub[oy:oy + 900, ox:ox + 900] = dog_arr[: min(900, H - oy), : min(900, W - ox)]
    a = sub[..., 3:4] / 255.0
    lit = sub[..., :3] * (0.58 + 0.85 * Ls[..., None]) + warm * 0.28 * Ls[..., None]
    lit = np.clip(lit, 0, 255)
    frame = frame * (1 - a) + lit * a
    # brilho aditivo (screen) antes do Lume
    g = (warm * 0.9)[None, None, :] * (Lb[..., None] * 0.8 + Ls[..., None] * 0.3)
    frame = 255 - (255 - np.clip(frame, 0, 255)) * (255 - np.clip(g, 0, 255)) / 255
    # Lume
    lume = draw_lume(t, 560, "happy", glow=1.9)
    la = np.zeros((H, W, 4), np.float32)
    px, py = int(lx - 280), int(ly - 300)
    la[py:py + 560, px:px + 560] = np.asarray(lume).astype(np.float32)
    aa = la[..., 3:4] / 255.0
    frame = frame * (1 - aa) + la[..., :3] * aa
    img = Image.fromarray(np.clip(frame, 0, 255).astype(np.uint8)).convert("RGBA")
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dr = ImageDraw.Draw(L)
    a1 = int(255 * min(1, max(0, (t - 0.3) / 0.8))); a2 = int(255 * min(1, max(0, (t - 1.1) / 0.8)))
    dr.text((W // 2 - 70, 175), "Oi, eu sou", font=f1, fill=(255, 249, 238, a1), anchor="mm")
    dr.text((W // 2 - 70, 285), "o Verso!", font=f1, fill=(255, 249, 238, a1), anchor="mm")
    dr.text((W // 2 - 70, 395), "e esta é a minha amiga Lume.", font=f2, fill=(255, 249, 238, a2), anchor="mm")
    dr.text((W // 2, 1640), "Juntos, a gente acende uma luz nos seus dias.", font=f3, fill=(255, 224, 160, a2), anchor="mm")
    dr.text((W // 2, 1790), "@virouversos", font=font(INTER, 34), fill=(255, 249, 238, 210), anchor="mm")
    img.alpha_composite(L)
    p.stdin.write(np.asarray(img.convert("RGB")).tobytes())
p.stdin.close(); p.wait()
print("ok")

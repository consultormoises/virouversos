import sys, subprocess, numpy as np
sys.path.insert(0, "/home/claude/virouversos/tools")
from viz import *
from mascot import draw_lume
from PIL import Image, ImageDraw

W, H, FPS, DUR = 1080, 1920, 30, 6
th_name = "4. Fecha o Ano em Verso"
base, layers, th = build_scene(th_name, W, H, seed=9)
bg = composite_static(base, layers, th, W, H)
grain = grain_pool(H, W, 1, 6.5, 9)[0]
vig = vignette(H, W, 0.38)
bgfin = finish(bg.copy(), grain, vig)

f1 = font(LORA, 96, "Bold"); f2 = font(LORA_I, 46, "Medium Italic"); f3 = font(INTER, 30)
out = sys.argv[1]
p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                      "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
for i in range(FPS * DUR):
    t = i / FPS
    frame = Image.fromarray(bgfin).convert("RGBA")
    mood = "wow" if 1.2 < t < 2.2 else "happy"
    m = draw_lume(t, 1040, mood)
    frame.alpha_composite(m, (20, 430))
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    a1 = int(255 * min(1, max(0, (t - 0.4) / 0.8)))
    a2 = int(255 * min(1, max(0, (t - 1.2) / 0.8)))
    d.text((W // 2, 250 - 10 * (1 - a1 / 255)), "Oi, eu sou o Lume!", font=f1, fill=(255, 249, 238, a1), anchor="mm")
    d.text((W // 2, 350), "o vagalume do Virou Versos", font=f2, fill=(255, 249, 238, a2), anchor="mm")
    d.text((W // 2, 425), "Eu acendo uma luz nos seus dias.", font=f3, fill=(255, 224, 160, a2), anchor="mm")
    d.text((W // 2, 1790), "@virouversos", font=font(INTER, 34), fill=(255, 249, 238, 200), anchor="mm")
    frame.alpha_composite(L)
    p.stdin.write(np.asarray(frame.convert("RGB")).tobytes())
p.stdin.close(); p.wait()
print("ok")

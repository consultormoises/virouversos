import sys, os
sys.path.insert(0, "/home/claude/virouversos/tools")
from stamp import stamp
R = "/home/claude/virouversos/v2/"
V = lambda m: ("verso", m, (700, 850, 440))      # canto inferior direito
L = lambda m: ("lume", m, (-70, -70, 400))       # canto superior esquerdo
BOTH = lambda m: [("verso", m, (560, 840, 540)), ("lume", m, (-90, 840, 520))]
def it(x):
    c, m, (px, py, s) = x
    return (c, m, (px, py), s)

plans = {
 "2026-11-23_eu-estou-bem": {1: [V("doubt"), L("happy")], 2: [V("doubt")], 3: [L("doubt")], 4: [L("sad")], 5: [V("sad")], 6: [L("happy")], 7: [V("happy")], "cta": "both"},
 "2026-11-22_espera-de-chuva": {1: [L("happy")], 2: [V("doubt")], 3: [L("happy")], 4: [V("sad")], 5: [L("happy")], 6: [V("happy")], 7: [L("happy")], "cta": "both"},
 "2026-11-29_a-pedra-no-bolso": {1: [V("doubt")], 2: [L("doubt")], 3: [V("happy")], 4: [L("sad")], 5: [V("sad")], 6: [V("sad")], 7: [V("happy")], "cta": "both"},
 "2026-11-30_balanco": {1: [V("happy"), L("happy")], 2: [L("happy")], 3: [V("doubt")], 4: [L("happy")], 5: [V("happy")], 6: [L("sad")], 7: [V("celebrate")], "cta": "both"},
 "2026-12-06_luz-do-corredor": {1: [V("happy"), L("happy")], 2: [L("happy")], 3: [L("happy")], 4: [V("happy")], 5: [L("happy")], 6: [V("happy")], 7: [L("happy")], 8: [V("celebrate")], "cta": "both"},
}
for folder, plan in plans.items():
    d = R + folder + "/"
    n = max(k for k in plan if isinstance(k, int)) + 1   # indice da arte do CTA
    for i in range(1, n):
        items = [it(x) for x in plan[i]]
        stamp(d + f"slide_{i:02d}.png", d + f"c_slide_{i:02d}.png", items)
    c = [("verso", "celebrate", (560, 860), 520), ("lume", "celebrate", (-80, 860), 500)]
    stamp(d + "cta_final.png", d + f"c_slide_{n:02d}.png", c)
    print(folder, n)
# imagens unicas
singles = {
 "2026-11-18_gabarito": ("post.png", [("verso", "happy", (720, 900), 360)]),
 "2026-11-25_a-casa-fala-baixo": ("post.png", [("lume", "sad", (-60, -60), 380)]),
 "2026-12-02_pequenas-vitorias": ("post.png", [("verso", "celebrate", (680, 860), 420)]),
}
for folder, (f, items) in singles.items():
    stamp(R + folder + "/" + f, R + folder + "/c_post.png", items)
    print(folder)

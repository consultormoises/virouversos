import sys, os
sys.path.insert(0, "/home/claude/virouversos/tools")
from feed import render_carousel
from stamp import stamp
from openpyxl import load_workbook
ws = load_workbook("/tmp/out/cronograma_virouversos_completo.xlsx")["Cronograma"]
TH = [r for r in ws.iter_rows(min_row=2, values_only=True) if r[0] and str(r[0])[:10]=="2026-11-22"][0][3]
slides = ["Em 2019, uma senhora de 93 anos\nempinando pipa virou vídeo\ncom 6 milhões de views.",
 "Ninguém ficou olhando a pipa.\nTodo mundo viu alguém\nque não pediu licença pra ser feliz.",
 "Ela disse que estava\nadorando ser famosa.\nMas a graça era brincar.",
 "E você?\nQuantas coisas deixou pra \"quando der\"\npor achar que passou da idade?",
 "Ninguém passa da idade\nde ser feliz.\nA sua pipa ainda te espera."]
t = "/tmp/rehook/pipa"; os.makedirs(t, exist_ok=True)
n = render_carousel(TH, "Por que a vovó da pipa viralizou?", slides, t, seed=96)
d = "/home/claude/virouversos/v2/2026-11-17_vovo-da-pipa/"; os.makedirs(d, exist_ok=True)
V = lambda m: ("verso", m, (700, 850), 440); L = lambda m: ("lume", m, (-70, -70), 400)
plan = {1: [V("happy"), L("doubt")], 2: [L("wow")], 3: [V("happy")], 4: [L("happy")], 5: [V("doubt")], 6: [V("celebrate")]}
for i in range(1, n):
    stamp(f"{t}/slide_{i:02d}.png", f"{d}p_slide_{i:02d}.png", plan.get(i, []))
stamp(f"{t}/slide_{n:02d}.png", f"{d}p_slide_{n:02d}.png", [("verso","celebrate",(560,860),520),("lume","celebrate",(-80,860),500)])
print(n)

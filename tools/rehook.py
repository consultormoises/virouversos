"""Recria capas/titulos com gancho (pergunta/curiosidade) e carimba personagens. Saida: h_slide_NN.png / h_post.png"""
import sys, os, re
sys.path.insert(0, "/home/claude/virouversos/tools")
from feed import render_carousel, render_single
from stamp import stamp
from openpyxl import load_workbook
R = "/home/claude/virouversos/v2/"
T = "/tmp/rehook/"
ws = load_workbook("/tmp/out/cronograma_virouversos_completo.xlsx")["Cronograma"]
rows = {str(r[0])[:10]: r for r in ws.iter_rows(min_row=2, values_only=True) if r[0]}
def sl(ds):
    return [s.strip() for s in re.split(r"Slide \d+:\s*", rows[ds][6])[1:] if s.strip() != "@virouversos"]
TH3, TH2, TH4 = rows["2026-11-23"][3], rows["2026-11-22"][3], rows["2026-11-30"][3]
V = lambda m: ("verso", m, (700, 850), 440)
L = lambda m: ("lume", m, (-70, -70), 400)
chuva = ["Sessenta e cinco cidades\nolham pro céu do Ceará\ncom a mesma pergunta.",
 "Quem espera chuva\naprende a ler nuvem\ncomo quem lê carta de amor.",
 "A terra rachada\nnão é só falta d'água:\né saudade com sede.",
 "E ainda assim\no povo planta, reza, divide o balde,\ninventa jeito de ficar.",
 "Esperança é isso:\ncontinuar de pé\nmesmo com o céu em silêncio.",
 "Que a chuva volte.\nE que a gente aprenda\na chegar a tempo\npra quem espera."]
posts = {
 "2026-11-22_espera-de-chuva": (TH2, "65 cidades esperam chuva. Você sabia?", chuva, 41,
   {1: [L("doubt")], 2: [V("doubt")], 3: [L("happy")], 4: [V("sad")], 5: [L("happy")], 6: [V("happy")], 7: [L("happy")]}),
 "2026-11-23_eu-estou-bem": (TH3, "Qual é a frase que mais esconde?", sl("2026-11-23"), 52,
   {1: [V("doubt"), L("doubt")], 2: [V("doubt")], 3: [L("doubt")], 4: [L("sad")], 5: [V("sad")], 6: [L("happy")], 7: [V("happy")]}),
 "2026-11-29_a-pedra-no-bolso": (TH3, "O que você ainda carrega no bolso?", sl("2026-11-29"), 63,
   {1: [V("doubt"), L("doubt")], 2: [L("doubt")], 3: [V("happy")], 4: [L("sad")], 5: [V("sad")], 6: [V("sad")], 7: [V("happy")]}),
 "2026-11-30_balanco": (TH4, "O que não coube na planilha do seu ano?", sl("2026-11-30"), 74,
   {1: [V("doubt"), L("doubt")], 2: [L("happy")], 3: [V("doubt")], 4: [L("happy")], 5: [V("happy")], 6: [L("sad")], 7: [V("celebrate")]}),
 "2026-12-06_luz-do-corredor": (TH4, "Quem acende a luz do seu corredor?", sl("2026-12-06"), 85,
   {1: [V("doubt"), L("happy")], 2: [L("happy")], 3: [L("happy")], 4: [V("happy")], 5: [L("happy")], 6: [V("happy")], 7: [L("happy")], 8: [V("celebrate")]}),
}
for folder, (theme, title, slides, seed, plan) in posts.items():
    t = T + folder; os.makedirs(t, exist_ok=True)
    n = render_carousel(theme, title, slides, t, seed=seed)
    d = R + folder + "/"
    for i in range(1, n):
        stamp(f"{t}/slide_{i:02d}.png", f"{d}h_slide_{i:02d}.png", plan.get(i, []))
    stamp(f"{t}/slide_{n:02d}.png", f"{d}h_slide_{n:02d}.png",
          [("verso", "celebrate", (560, 860), 520), ("lume", "celebrate", (-80, 860), 500)])
    print(folder, n)
# imagens unicas
singles = {
 "2026-11-18_gabarito": ("A vida tem gabarito?", "2026-11-18", [("verso", "happy", (720, 900), 360)], 31),
 "2026-11-25_a-casa-fala-baixo": ("Você ouviu o planeta?", None, [("lume", "sad", (-60, -60), 380)], 32),
 "2026-12-02_pequenas-vitorias": ("Qual foi sua vitória pequena?", "2026-12-02", [("verso", "celebrate", (680, 860), 420)], 33),
}
txt = {
 "2026-11-18_gabarito": "Milhões de mãos tremeram sobre a mesma folha,\ncada uma com um sonho\nque não cabe em alternativa.\nA vida não traz gabarito:\na gente marca, segue,\ne entende a resposta depois.\nVocê é maior que a nota.",
 "2026-11-25_a-casa-fala-baixo": "Enquanto o mundo se reúne\npra falar de clima,\no planeta continua falando baixo:\num rio que seca,\numa chuva fora de hora,\num verão que chegou antes.\nÉ a nossa casa\npedindo pra ser escutada.",
 "2026-12-02_pequenas-vitorias": "Levantar da cama já foi poema.\nResponder aquela mensagem, verso.\nO ano pesou,\ne você ainda escreve.",
}
themes = {"2026-11-18_gabarito": TH2, "2026-11-25_a-casa-fala-baixo": TH3, "2026-12-02_pequenas-vitorias": TH4}
for folder, (title, _, items, seed) in singles.items():
    t = T + folder; os.makedirs(t, exist_ok=True)
    render_single(themes[folder], title, txt[folder], f"{t}/post.png", seed=seed)
    stamp(f"{t}/post.png", R + folder + "/h_post.png", items)
    print(folder)

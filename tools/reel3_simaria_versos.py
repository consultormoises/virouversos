import sys
sys.path.insert(0,"/home/claude/virouversos/tools")
from reels3 import *
S="/tmp/reels3"
segs=[("Teve uma noite que durou meses, e quase ninguém viu a chuva por dentro.",3.64),
      ("Mas quem diz em voz alta acende a primeira janela.",8.98),
      ("Pedir ajuda não é fraqueza: é abrir a porta pra luz entrar.",12.95),
      ("A tempestade passa, e o céu lembra como é azul.",17.57),
      ("Quem segura a sua mão quando a noite é longa?",21.46),
      ("Se estiver pesado, ligue 188: CVV, 24 horas.",24.42)]
mode=sys.argv[1]
d=build_reel3("3. O que a gente não diz","Simaria","o que a tempestade ensinou?",segs,29.86,S+"/audio/simaria2.mp3",33.41,S+"/out/simaria2.mp4",
  tag="", cta_lines=["Conta nos comentários","CVV 188 · 24 horas"], mood="calm",
  preview=[0.5,10.0,26.0,31.0] if mode=="prev" else None)
print(d)

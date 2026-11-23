import sys
sys.path.insert(0,"/home/claude/virouversos/tools")
from reels3 import *
D="/home/claude/virouversos/v2/2026-11-23_thiago-viana"
segs=[("Tem voz que canta pro vazio,\ne o vazio guarda o eco.",4.14),
      ("Um dia o vídeo corre,\ne o mundo inteiro escuta.",8.45),
      ("Quem espera com esperança\nnão espera parado.",12.15),
      ("Continue.\nA sua hora também vai chegar.",15.24),
      ("O que você segue fazendo\nmesmo sem plateia?",18.56)]
mode=sys.argv[1]
d=build_reel3("1. Ruídos do Agora","Thiago Viana","você continuaria sem ninguém olhando?",segs,21.57,D+"/narracao_v2.mp3",26.75,D+"/reel_v3.mp4",
  tag="",cta_lines=["Conta nos comentários"],mood="hope",music_vol=0,
  preview=[0.3,5.5,16.5,19.5,23.5] if mode=="prev" else None)
print(d)

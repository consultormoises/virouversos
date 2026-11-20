import sys
sys.path.insert(0,"/home/claude/virouversos/tools")
from reels3 import *
S="/tmp/reels3"
segs=[("Ela era a única do Pará naquela lista de indicados.",3.25),
      ("Foi de vestido de palha e látex, feito com o que a terra dá.",6.56),
      ("Sonhar grande não pede que você deixe de ser quem é.",10.43),
      ("Leve a sua terra com você, e vá longe sem se perder.",13.81),
      ("Qual sonho seu parecia grande demais?",17.56)]
mode=sys.argv[1]
d=build_reel3("4. Fecha o Ano em Verso","Zaynara","foi de palha ao Grammy. Por quê?",segs,20.0,S+"/audio/zay.mp3",24.27,S+"/out/zay.mp4",
  tag="GRAMMY LATINO 2026",cta_lines=["Conta nos comentários"],
  preview=[0.0,4.5,8.0,18.5,21.8,25.2] if mode=="prev" else None)
print(d)

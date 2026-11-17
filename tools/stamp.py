"""Aplica um personagem (Lume/Verso) com expressao sobre uma arte pronta.
stamp(src, out, [(char, mood, pos, size), ...]); pos = canto sup. esquerdo do sprite."""
import sys
sys.path.insert(0, "/home/claude/virouversos/tools")
from PIL import Image
from mascot import draw_lume, draw_verso

def stamp(src, out, items, t=1.0):
    im = Image.open(src).convert("RGBA")
    for char, mood, pos, size in items:
        fn = draw_lume if char == "lume" else draw_verso
        sp = fn(t, size, mood)
        im.alpha_composite(sp, pos)
    im.convert("RGB").save(out, optimize=True)

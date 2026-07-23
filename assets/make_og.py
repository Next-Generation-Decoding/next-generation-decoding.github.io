#!/usr/bin/env python3
"""Generate assets/og.png (1200x630) — denoising-grid motif matching the site."""
import math, os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1200, 630

def font(paths, size):
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

SERIF_B = font(['/System/Library/Fonts/Supplemental/Georgia Bold.ttf',
                '/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf',
                '/Library/Fonts/Georgia Bold.ttf'], 66)
SERIF_R = font(['/System/Library/Fonts/Supplemental/Georgia.ttf',
                '/System/Library/Fonts/Supplemental/Times New Roman.ttf'], 27)
MONO = font(['/System/Library/Fonts/Menlo.ttc',
             '/System/Library/Fonts/Supplemental/Courier New.ttf'], 21)
MONO_S = font(['/System/Library/Fonts/Menlo.ttc',
               '/System/Library/Fonts/Supplemental/Courier New.ttf'], 19)

# --- base vertical gradient ---
img = Image.new('RGB', (W, H), (11, 16, 32))
d = ImageDraw.Draw(img)
top, bot = (11, 16, 32), (21, 28, 54)
for y in range(H):
    t = y / H
    d.line([(0, y), (W, y)], fill=(int(top[0]+(bot[0]-top[0])*t),
                                   int(top[1]+(bot[1]-top[1])*t),
                                   int(top[2]+(bot[2]-top[2])*t)))

# --- denoising grid overlay ---
overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
od = ImageDraw.Draw(overlay)
COLORS = [(91, 83, 255), (111, 119, 255), (18, 179, 166), (43, 54, 99), (58, 70, 128)]
cell = 60
size = int(cell * 0.66)
pad = (cell - size) // 2
cols, rows = W // cell + 1, H // cell + 1
for gy in range(rows):
    for gx in range(cols):
        f = math.sin(gx * 0.55) + math.cos(gy * 0.6 + gx * 0.2)
        ci = 0 if f > 1.1 else 1 if f > 0.4 else 2 if f < -1.1 else 3 if f < -0.3 else 4
        order = (gx / cols) * 0.42 + (gy / rows) * 0.30
        prog = max(0.0, min(1.0, (0.72 - order) / 0.42))
        x, y = gx * cell + pad, gy * cell + pad
        if prog > 0.05:
            c = COLORS[ci]
            od.rounded_rectangle([x, y, x + size, y + size], radius=int(size * 0.22),
                                 fill=(c[0], c[1], c[2], int(prog * 95)))
        else:
            od.rectangle([x + size*0.35, y + size*0.35, x + size*0.52, y + size*0.52],
                         fill=(124, 132, 184, 55))
img = Image.alpha_composite(img.convert('RGBA'), overlay)

# --- left veil for legibility ---
veil = Image.new('RGBA', (W, H), (0, 0, 0, 0))
vd = ImageDraw.Draw(veil)
edge = 0.74
for x in range(W):
    t = x / W
    a = int(225 * max(0.0, (edge - t)) / edge) if t < edge else 0
    vd.line([(x, 0), (x, H)], fill=(11, 16, 32, a))
img = Image.alpha_composite(img, veil).convert('RGB')

d = ImageDraw.Draw(img)
M = 74
WHITE = (247, 248, 252)
ACCENT = (160, 155, 255)
TEAL = (79, 214, 203)
MUTED = (176, 182, 204)

d.text((M, 84), "NEURIPS 2026 WORKSHOP", font=MONO, fill=ACCENT)
d.text((M, 138), "Beyond Next-Token", font=SERIF_B, fill=WHITE)
d.text((M, 210), "Prediction", font=SERIF_B, fill=WHITE)
d.text((M, 300), "Diffusion & Flow Models", font=SERIF_B, fill=ACCENT)
# accent underline
d.rectangle([M, 384, M + 96, 388], fill=(91, 83, 255))
d.text((M, 414), "Discrete diffusion & flow models for", font=SERIF_R, fill=MUTED)
d.text((M, 448), "next-generation, non-causal decoding.", font=SERIF_R, fill=MUTED)
# bottom meta row
d.text((M, 520), "DEC 11-12, 2026", font=MONO_S, fill=TEAL)
d.text((M + 210, 520), "SUBMISSIONS DUE AUG 29", font=MONO_S, fill=MUTED)

out = os.path.join(HERE, 'og.png')
img.save(out, 'PNG', optimize=True)
print("wrote", out, os.path.getsize(out), "bytes")

"""
contact_sheet.py — QA helper: put chosen frames of one or more GIFs side by side in one PNG.

Usage:
  python3 contact_sheet.py sheet.png out/gif/b-interpolation.gif --frames 50,100,150,200

Each row is one GIF; each column one frame index (clamped to the GIF's length).
"""
import argparse

from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("out")
ap.add_argument("gifs", nargs="+")
ap.add_argument("--frames", default="45,90,140,200", help="comma-separated frame indexes")
a = ap.parse_args()
idx = [int(x) for x in a.frames.split(",")]

ims = [Image.open(g) for g in a.gifs]
w, h = ims[0].size
sheet = Image.new("RGB", (len(idx) * (w + 10), len(ims) * (h + 10)), "#777777")
for r, im in enumerate(ims):
    for c, k in enumerate(idx):
        im.seek(min(k, im.n_frames - 1))
        sheet.paste(im.convert("RGB"), (c * (w + 10), r * (h + 10)))
sheet.save(a.out)
print(f"{a.out}: {len(ims)} GIFs × {len(idx)} frames")

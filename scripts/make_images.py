"""Generates the sample 'original' (unoptimized) images, then compresses them.
Replace the files in images-original/ with your own photos and re-run:  python3 scripts/make_images.py --compress-only
"""
import os, sys, random, math
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIG = os.path.join(ROOT, "images-original")
OUT = os.path.join(ROOT, "images")

SPECS = {
    # name: (width, height, color1, color2)
    "profile":   (1600, 1600, (108, 77, 230), (236, 120, 190)),
    "about":     (2000, 1400, (52, 120, 246), (120, 220, 200)),
    "project-1": (2400, 1500, (255, 140, 90), (200, 70, 150)),
    "project-2": (2400, 1500, (40, 180, 160), (30, 80, 170)),
    "project-3": (2400, 1500, (250, 200, 70), (240, 90, 90)),
}

def make(name, w, h, c1, c2):
    random.seed(name)
    img = Image.new("RGB", (w, h))
    px = img.load()
    for y in range(h):
        for x in range(w):
            t = (x / w + y / h) / 2
            px[x, y] = tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))
    d = ImageDraw.Draw(img, "RGBA")
    for _ in range(26):
        r = random.randint(h // 12, h // 4)
        cx, cy = random.randint(0, w), random.randint(0, h)
        d.ellipse([cx - r, cy - r, cx + r, cy + r],
                  fill=(255, 255, 255, random.randint(20, 70)))
    for _ in range(14):
        x0, y0 = random.randint(0, w), random.randint(0, h)
        d.rounded_rectangle([x0, y0, x0 + random.randint(150, 500), y0 + random.randint(80, 260)],
                            radius=24, fill=(0, 0, 0, random.randint(15, 45)))
    img = img.filter(ImageFilter.GaussianBlur(1.2))
    # photographic-style noise so the "original" is realistically heavy
    noise = Image.effect_noise((w, h), 28).convert("RGB")
    img = Image.blend(img, noise, 0.08)
    img.save(os.path.join(ORIG, name + ".jpg"), "JPEG", quality=95, subsampling=0)

def compress(name, max_w):
    src = Image.open(os.path.join(ORIG, name + ".jpg")).convert("RGB")
    if src.width > max_w:
        src = src.resize((max_w, round(src.height * max_w / src.width)), Image.LANCZOS)
    src.save(os.path.join(OUT, name + ".webp"), "WEBP", quality=78, method=6)
    return src.size

if __name__ == "__main__":
    os.makedirs(ORIG, exist_ok=True); os.makedirs(OUT, exist_ok=True)
    if "--compress-only" not in sys.argv:
        for n, (w, h, a, b) in SPECS.items():
            make(n, w, h, a, b)
    widths = {"profile": 600, "about": 900}
    for n in SPECS:
        print(n, compress(n, widths.get(n, 800)))

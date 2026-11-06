"""Prints a before/after size table (bytes) for CSS, JS and images."""
import os, gzip
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def size(p): return os.path.getsize(os.path.join(ROOT, p))
def gz(p): return len(gzip.compress(open(os.path.join(ROOT, p), "rb").read(), 9))
def kb(b): return f"{b/1024:.1f} KB"

rows = [("css/style.css", "css/style.min.css"), ("js/script.js", "js/script.min.js")]
for n in ["profile", "about", "project-1", "project-2", "project-3"]:
    rows.append((f"images-original/{n}.jpg", f"images/{n}.webp"))

tb = ta = 0
print(f"{'File':<22}{'Before':>12}{'After':>12}{'Saved':>9}")
for b, a in rows:
    sb, sa = size(b), size(a); tb += sb; ta += sa
    print(f"{os.path.basename(a):<22}{kb(sb):>12}{kb(sa):>12}{(1-sa/sb)*100:>8.1f}%")
print(f"{'TOTAL':<22}{kb(tb):>12}{kb(ta):>12}{(1-ta/tb)*100:>8.1f}%")
print("\nGzip transfer (CSS/JS):")
for b, a in rows[:2]:
    print(f"  {os.path.basename(b)} -> {os.path.basename(a)}: {kb(gz(b))} -> {kb(gz(a))}")

"""Dependency-free CSS/JS minifier used to produce style.min.css and script.min.js.
For production-grade output use the npm build (Terser + csso):  npm run build
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def minify_css(src):
    src = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
    src = re.sub(r"\s+", " ", src)
    src = re.sub(r"\s*([{};,>])\s*", r"\1", src)
    src = re.sub(r":\s+", ":", src)
    src = src.replace(";}", "}")
    src = re.sub(r"\(\s+", "(", src)
    src = re.sub(r"\s+\)", ")", src)
    return src.strip()

def minify_js(src):
    out, i, n = [], 0, len(src)
    def need_space(prev, nxt):
        w = lambda c: c.isalnum() or c in "_$"
        return w(prev) and w(nxt)
    while i < n:
        c = src[i]
        if c in "'\"`":
            q, j = c, i + 1
            while j < n and src[j] != q:
                j += 2 if src[j] == "\\" else 1
            out.append(src[i:j + 1]); i = j + 1
        elif src.startswith("//", i):
            while i < n and src[i] != "\n": i += 1
        elif src.startswith("/*", i):
            i = src.index("*/", i) + 2
        elif c.isspace():
            j = i
            while j < n and src[j].isspace(): j += 1
            prev = out[-1][-1] if out else ""
            nxt = src[j] if j < n else ""
            if prev and nxt and need_space(prev, nxt):
                out.append(" ")
            i = j
        else:
            out.append(c); i += 1
    return "".join(out)

def run(name, fn, src_rel, dst_rel):
    s = open(os.path.join(ROOT, src_rel), encoding="utf-8").read()
    m = fn(s)
    open(os.path.join(ROOT, dst_rel), "w", encoding="utf-8").write(m)
    print(f"{src_rel}: {len(s.encode())} B -> {dst_rel}: {len(m.encode())} B")

if __name__ == "__main__":
    run("css", minify_css, "css/style.css", "css/style.min.css")
    run("js", minify_js, "js/script.js", "js/script.min.js")

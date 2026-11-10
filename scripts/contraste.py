#!/usr/bin/env python3
"""Les jetons de couleur du site, mesurés (S06) : chaque couleur de texte tient 4,5:1 sur chaque fond, et un trait qui
doit se voir (--edge) 3:1, dans le clair et dans le sombre. Lit les jetons dans style.css ; 1 si un écart.

    python3 scripts/contraste.py
"""
import os, re, sys

CSS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "style.css")
TEXTES = ["--text", "--body", "--secondary", "--accent", "--warn", "--problem"]
FONDS = ["--window", "--group", "--sunken", "--control"]
PAIRES = [("--accent", "--accent-soft", 4.5)] + [("--edge", f, 3.0) for f in ("--window", "--group", "--control")]


def jetons(bloc):
    return dict(re.findall(r"(--[\w-]+):\s*(#[0-9a-fA-F]{6})\b", bloc))


def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def ratio(a, b):
    x, y = sorted((lum(a), lum(b)), reverse=True)
    return (x + 0.05) / (y + 0.05)


css = open(CSS).read()
clair = jetons(re.search(r":root\s*\{(.*?)\}", css, re.S).group(1))
sombre = dict(clair)
sombre.update(jetons(re.search(r"prefers-color-scheme: dark\)\s*\{\s*:root[^{]*\{(.*?)\}", css, re.S).group(1)))
ecarts = 0
for nom, t in (("clair", clair), ("sombre", sombre)):
    lignes = [(a, b, 4.5) for a in TEXTES for b in FONDS] + PAIRES
    for a, b, mini in lignes:
        r = ratio(t[a], t[b])
        ok = r >= mini
        ecarts += not ok
        print(f"{nom:7} {a:12} sur {b:14} {r:5.2f}:1 {'ok' if ok else f'< {mini}'}")
print(f"{ecarts} écart(s).")
sys.exit(1 if ecarts else 0)

#!/usr/bin/env python3
"""La ponctuation française des pages du site (S35, S11), à passer avant de fusionner.

    python3 scripts/typo.py            corrige les pages
    python3 scripts/typo.py --verifie  dit seulement ce qui reste à corriger ; 1 s'il en reste

Dans le texte et les attributs lus (alt, aria-label, title, placeholder, content) : l'apostrophe courbe, une espace
insécable avant « : ; ? ! » et « › », et à l'intérieur des guillemets. Ni le code, ni les scripts, ni les styles. Les
pages de version sont faites par dossiers.py : elles n'y passent pas.
"""
import re, sys, os

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ["index.html", "fonctionnalites/index.html", "guides/index.html", "confidentialite/index.html"]
NB = "&nbsp;"


def texte(t):
    t = re.sub(r"(?<=[A-Za-zÀ-ÿ])'(?=[A-Za-zÀ-ÿ0-9])", "’", t)
    t = re.sub(r" ([:;?!»›])", NB + r"\1", t)
    t = re.sub(r"« ", "«" + NB, t)
    return t


def attribut(m):
    return f'{m.group(1)}="{texte(m.group(2))}"'


def passe(s):
    morceaux = re.split(r"(<[^>]+>)", s)
    dedans = 0
    sortie = []
    for m in morceaux:
        if m.startswith("<"):
            nom = re.match(r"</?\s*([a-zA-Z0-9]+)", m)
            nom = nom.group(1).lower() if nom else ""
            if nom in ("script", "style", "code", "pre"):
                dedans += -1 if m.startswith("</") else 1
            m = re.sub(r'\b(alt|aria-label|title|placeholder|content)="([^"]*)"',
                       lambda a: attribut(a) if not re.match(r"(https?:|width|light|text/|summary|website|fr_)", a.group(2)) else a.group(0), m)
            sortie.append(m)
        else:
            sortie.append(m if dedans > 0 else texte(m))
    return "".join(sortie)


if __name__ == "__main__":
    reste = 0
    for page in PAGES:
        chemin = os.path.join(RACINE, page)
        avant = open(chemin).read()
        apres = passe(avant)
        if apres != avant:
            n = sum(1 for a, b in zip(avant.splitlines(), apres.splitlines()) if a != b)
            reste += n
            print(f"{page} : {n} ligne(s)")
            if "--verifie" not in sys.argv:
                open(chemin, "w").write(apres)
    sys.exit(1 if reste and "--verifie" in sys.argv else 0)

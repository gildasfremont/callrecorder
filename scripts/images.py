#!/usr/bin/env python3
"""Les images du site à leur poids (S02, S18).

    python3 scripts/images.py            refait les variantes réduites et vérifie les pages
    python3 scripts/images.py --verifie  vérifie seulement : chaque <img> déclare width et height, chaque grande
                                         image a son srcset ; 1 s'il manque quelque chose

Une grande image a une variante réduite à côté d'elle, `nom-<largeur>w.webp`, pour les écrans où elle s'affiche petite :
le navigateur choisit dans le srcset. Les captures de l'app restent sans perte (VP8L), les illustrations à l'encre en
WebP avec perte, comme l'original. Les PNG des pages passent en WebP sans perte.
"""
import os, re, subprocess, sys, tempfile
from PIL import Image

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ["index.html", "fonctionnalites/index.html", "guides/index.html", "confidentialite/index.html"]
# Image → largeur de la variante réduite. Une capture plein écran passe à la moitié ; une illustration à ce qu'il faut
# pour deux fois sa taille sur téléphone.
VARIANTES = {
    "img/appels.webp": 1280, "img/appels-reunion.webp": 1280, "img/appels-note.webp": 1280,
    "img/calendrier.webp": 1280, "img/transcription.webp": 1180,
    "img/pixel-7.webp": 300, "img/pixel-7-reunion.webp": 300, "img/pixel-7-notes.webp": 300,
    "img/micro-mat.webp": 400, "img/gildas.webp": 340, "img/reunion.webp": 600,
    "img/benefices/cassettes.webp": 600, "img/benefices/jack.webp": 700, "img/benefices/micro.webp": 600,
    "img/benefices/telephone.webp": 600, "img/benefices/ordinateur.webp": 600,
}
# Le micro de la marque a déjà ses tailles, recopiées de marque/icone (marque.py) : img/icone-micro-64.png sert de
# variante réduite, sans en calculer une autre.
MARQUE = {
    "img/icone-micro.webp": "img/icone-micro-64.png",
}
GRANDE = 600  # au-delà de cette largeur, une image sans srcset est signalée


def sans_perte(chemin):
    with open(chemin, "rb") as f:
        tete = f.read(40)
    return b"VP8L" in tete


def variante(src, largeur):
    base, _ = os.path.splitext(src)
    sortie = f"{base}-{largeur}w.webp"
    im = Image.open(os.path.join(RACINE, src))
    h = round(im.height * largeur / im.width)
    with tempfile.NamedTemporaryFile(suffix=".png") as t:
        im.convert("RGBA").resize((largeur, h), Image.LANCZOS).save(t.name)
        opts = ["-lossless", "-z", "9"] if sans_perte(os.path.join(RACINE, src)) else ["-q", "85", "-alpha_q", "100", "-m", "6"]
        subprocess.run(["cwebp", "-quiet", *opts, t.name, "-o", os.path.join(RACINE, sortie)], check=True)
    return sortie


def verifie():
    manque = []
    for page in PAGES:
        texte = open(os.path.join(RACINE, page)).read()
        for m in re.finditer(r"<img\b[^>]*>", texte):
            balise = m.group(0)
            src = re.search(r'src="([^"?]+)', balise).group(1)
            chemin = os.path.normpath(os.path.join(RACINE, os.path.dirname(page), src))
            if "width=" not in balise or "height=" not in balise:
                manque.append(f"{page} : {src} sans width ni height")
            if os.path.exists(chemin) and Image.open(chemin).width > GRANDE and "srcset=" not in balise:
                if os.path.relpath(chemin, RACINE) in VARIANTES:
                    manque.append(f"{page} : {src} sans srcset")
    for ligne in manque:
        print(ligne)
    print(f"{len(manque)} écart(s).")
    return 1 if manque else 0


if __name__ == "__main__":
    if "--verifie" not in sys.argv:
        for src, largeur in VARIANTES.items():
            print(variante(src, largeur))
    sys.exit(verifie())

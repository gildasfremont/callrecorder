#!/usr/bin/env python3
"""Captures annotées du dossier : une image du banc d'inventaire, recadrée, avec des cadres numérotés posés sur les
vraies positions des vues (relevées dans le JSON du même état).  python3 design/recos/ux-android/outils/annote.py"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont

BANC = "phone/android/app/build/dossier"
OUT = "design/recos/ux-android/images"
os.makedirs(OUT, exist_ok=True)
ECHELLE = 0.5  # 1236 px → 618 px : 1,5 px par dp
try:
    FONTE = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
except OSError:
    FONTE = ImageFont.load_default()
ROUGE = (214, 40, 40)

def vues(nom):
    d = json.load(open(f"{BANC}/{nom}.json")); return d["densite"], d["vues"]

def trouve(vs, cle, valeur, n=0):
    t = [v for v in vs if (v.get(cle) or "").startswith(valeur) and v["l"] > 0]
    return t[n] if len(t) > n else None

def annote(nom, sortie, marques, coupe=None, hauteur=None):
    """marques : [(cle, valeur, etiquette, marge_dp)] ; cle 'texte' ou 'description', ou ('zone', x, y, l, h)."""
    d, vs = vues(nom)
    im = Image.open(f"{BANC}/{nom}.png").convert("RGB")
    dr = ImageDraw.Draw(im)
    for i, m in enumerate(marques, 1):
        if m[0] == "zone":
            _, x, y, l, h, etiq = m
        else:
            cle, val, etiq, marge = m
            v = trouve(vs, cle, val)
            if v is None: print("introuvable", nom, val); continue
            x, y, l, h = v["x"] - marge, v["y"] - marge, v["l"] + 2 * marge, v["h"] + 2 * marge
        box = [x * d, y * d, (x + l) * d, (y + h) * d]
        dr.rectangle(box, outline=ROUGE, width=7)
        r = 26
        cx, cy = box[0] - 4, box[1] - 4
        cx, cy = max(r + 2, cx), max(r + 2, cy)
        dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=ROUGE)
        dr.text((cx, cy), str(i), fill="white", font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30) if FONTE else None, anchor="mm")
    if coupe:
        x0, y0, x1, y1 = [int(c * d) for c in coupe]
        im = im.crop((x0, y0, x1, y1))
    im = im.resize((int(im.width * ECHELLE), int(im.height * ECHELLE)), Image.LANCZOS)
    im.save(f"{OUT}/{sortie}.png", optimize=True)
    return f"{OUT}/{sortie}.png"

def cote(noms, sortie, legendes, coupe=None):
    """Plusieurs états côte à côte, même recadrage."""
    ims = []
    for n in noms:
        d, _ = vues(n)
        im = Image.open(f"{BANC}/{n}.png").convert("RGB")
        if coupe: im = im.crop(tuple(int(c * d) for c in coupe))
        ims.append(im.resize((int(im.width * ECHELLE), int(im.height * ECHELLE)), Image.LANCZOS))
    W = sum(i.width for i in ims) + 16 * (len(ims) - 1); H = max(i.height for i in ims) + 34
    s = Image.new("RGB", (W, H), (255, 255, 255)); dr = ImageDraw.Draw(s); x = 0
    f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 17)
    for im, lg in zip(ims, legendes):
        s.paste(im, (x, 34)); dr.text((x + 4, 8), lg, fill=(60, 60, 60), font=f); x += im.width + 16
    s.save(f"{OUT}/{sortie}.png", optimize=True)

E = lambda ecran, etat, conf="clair-100": f"{ecran}--{etat}--{conf}"
H = 915

# 1. États vides.
annote(E("accueil", "vide"), "p01-accueil-vide", [("zone", 12, 70, 388, 700, "")], coupe=(0, 0, 412, H))
annote(E("accueil", "recherche-sans-resultat"), "p01-recherche-sans-resultat", [("zone", 12, 70, 388, 700, ""), ("texte", "Enregistrer une réunion", "", 6)], coupe=(0, 0, 412, H))
annote(E("conversation", "filtre-sans-resultat"), "p01-filtre-sans-resultat", [("description", "", "", 0)] and [("zone", 12, 120, 388, 560, "")], coupe=(0, 0, 412, H))
# 2. Conversation en cours.
annote(E("conversation", "en-direct"), "p02-en-direct", [("zone", 60, 760, 292, 90, "")], coupe=(0, 0, 412, H))
annote(E("accueil", "enregistrement"), "p02-accueil-enregistrement", [("texte", "Arrêter l'enregistrement", "", 8)], coupe=(0, 0, 412, H))
# 3. Texte des appels.
annote(E("reglages", "manuel"), "p03-appels", [("texte", "Tous les appels", "", 6)], coupe=(0, 60, 412, 300))
# 4. Police à 200 %.
annote(E("conversation", "transcrite-avec-son", "clair-200"), "p04-conversation-200", [("texte", "13:", "", 2), ("texte", "SM", "", 2), ("texte", "Télécharger", "", 4)], coupe=(0, 0, 412, H))
annote(E("mise-en-route", "aucun-mac", "clair-200"), "p04-mise-en-route-200", [("texte", "Scanner le code du Mac", "", 6)], coupe=(0, 250, 412, 700))
annote(E("accueil", "liste", "clair-200"), "p04-accueil-200", [("texte", "13:", "", 2)], coupe=(0, 0, 412, H))
# 6. Lien perdu.
cote([E("accueil", "liste"), E("accueil", "lien-perdu")], "p06-lien-perdu-identique", ["Mac connecté", "Mac injoignable, 1 en attente"], coupe=(0, 0, 412, 500))
annote(E("reglages", "manuel"), "p06-reglages-mac", [("description", "Mac, MacBook Air", "", 2)], coupe=(0, 260, 412, 380))
annote(E("journal", "sans-reponse-du-mac"), "p06-journal", [("texte", "Le Journal est sur", "", 6)], coupe=(0, 0, 412, 300))
# 9. Dates.
annote(E("accueil", "recherche-resultats"), "p09-recherche-sans-date", [("texte", "Je peux m'en occuper", "", 4)], coupe=(0, 0, 412, 460))
annote(E("conversation", "transcrite-avec-son"), "p09-entete-sans-jour", [("texte", "13:", "", 3)], coupe=(0, 0, 412, 150))
# Sombre : l'accent.
annote(E("accueil", "ecoute", "sombre-100"), "p05-sombre-ecoute", [("texte", "● Écoute", "", 4)], coupe=(0, 0, 412, 260))
annote(E("reglages", "calendrier-sans-calendrier", "sombre-100"), "p05-sombre-relier", [("texte", "Relier un calendrier", "", 4)], coupe=(0, 60, 412, 400))
annote(E("accueil", "calendrier", "sombre-100"), "p05-sombre-aujourdhui", [("texte", "8", "", 4)], coupe=(0, 50, 412, 300))
# Lecteur et répliques.
annote(E("conversation", "transcrite-avec-son"), "p11-lecteur", [("description", "Lire", "", 2), ("description", "Position dans le son", "", 2), ("texte", "00:04", "", 2), ("texte", "M", "", 2)], coupe=(0, 50, 412, 320))
# Grisés actifs.
annote(E("conversation", "pas-encore-transcrite"), "p10-grise-actif", [("description", "Copier", "", 2), ("description", "Télécharger", "", 2)], coupe=(0, 740, 412, H))
# Réglages : double alerte.
annote(E("reglages", "calendrier-sans-calendrier"), "p13-double-alerte", [("texte", "Aucun calendrier relié", "", 4), ("description", "Calendrier, Non relié", "", 2)], coupe=(0, 60, 412, 460))
# Calendrier : flèches.
annote(E("accueil", "calendrier"), "p18-fleches", [("description", "Mois précédent", "", 0), ("description", "Mois suivant", "", 0)], coupe=(0, 60, 412, 140))
# Liste : en attente du Mac.
annote(E("accueil", "en-attente-du-mac"), "p19-en-attente", [("texte", "Réunion", "", 50)], coupe=(0, 50, 412, 200))
# Mise en route : saut de mise en page.
cote([E("mise-en-route", "aucun-mac"), E("mise-en-route", "connexion"), E("mise-en-route", "autre-wifi")], "p20-mise-en-route-etats",
     ["Aucun Mac relié", "Connexion…", "Autre Wi-Fi"], coupe=(0, 280, 412, 640))
# Boîtes de dialogue : l'accent d'Android.
cote(["dialogue--supprimer--clair-100", "dialogue--appels--clair-100"], "p21-dialogues", ["Supprimer la conversation ?", "Enregistrer les appels"], coupe=(0, 0, 412, 286))
# Interrupteur des appels allumé : la teinte d'Android.
annote(E("reglages", "tout-le-temps-appels-allumes"), "p21-interrupteur", [("texte", "Enregistrer les appels", "", 40)], coupe=(0, 220, 412, 290))
print("ok")

# Vignettes de tous les états : clair et sombre à 100 %, clair à 200 % (inventaire).
import glob
os.makedirs(f"{OUT}/etats", exist_ok=True)
for f in sorted(glob.glob(f"{BANC}/*--*--*.png")):
    n = os.path.basename(f)[:-4]
    if not n.endswith(("clair-100", "sombre-100", "clair-200")) or n.startswith("dialogue"): continue
    im = Image.open(f).convert("RGB")
    im = im.resize((im.width // 4, im.height // 4), Image.LANCZOS)
    im.save(f"{OUT}/etats/{n}.webp", "WEBP", quality=88, method=6)
print("vignettes", len(glob.glob(f"{OUT}/etats/*.webp")))

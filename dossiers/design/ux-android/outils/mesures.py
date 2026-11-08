#!/usr/bin/env python3
"""Mesures sur les arbres de vues du banc d'inventaire (DossierTest.kt → phone/android/app/build/dossier/*.json).

  python3 design/recos/ux-android/outils/mesures.py [dossier-du-banc]

Écrit dans design/recos/ux-android/donnees/ :
  contrastes.csv      chaque couple texte/fond rendu (dédoublonné), WCAG 2 et APCA, clair et sombre
  cibles.csv          chaque vue touchable : taille en dp, nom et rôle d'accessibilité, par état et taille de police
  accessibilite.csv   ce que TalkBack recevra : rôle, nom, titre, état, et les manques
  police.csv          textes coupés, rognés ou qui se chevauchent, par taille de police
  textes-rendus.csv   chaque texte rendu, sa taille et sa couleur, par état
  mesures-resume.json les totaux cités dans le dossier
"""
import csv, glob, json, os, sys, re, collections, math

BANC = sys.argv[1] if len(sys.argv) > 1 else "phone/android/app/build/dossier"
OUT = "design/recos/ux-android/donnees"

def rgb(h):  # "#AARRGGBB"
    v = int(h[1:], 16); return ((v >> 24) & 255) / 255, (v >> 16) & 255, (v >> 8) & 255, v & 255
def sur(fond, c):
    a, r, g, b = rgb(c); _, R, G, B = rgb(fond)
    return (round(r * a + R * (1 - a)), round(g * a + G * (1 - a)), round(b * a + B * (1 - a)))
def lum(c):
    def ch(x):
        x /= 255; return x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4
    r, g, b = c; return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)
def wcag(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True); return (la + 0.05) / (lb + 0.05)
def apca(texte, fond):
    """APCA-W3 0.0.98G-4g (SAPC), Lc signé : positif texte sombre sur fond clair."""
    def y(c):
        r, g, b = [(x / 255) ** 2.4 for x in c]; return 0.2126729 * r + 0.7151522 * g + 0.0721750 * b
    def clamp(v): return v if v > 0.022 else v + (0.022 - v) ** 1.414
    yt, yb = clamp(y(texte)), clamp(y(fond))
    if abs(yb - yt) < 0.0005: return 0.0
    if yb > yt:
        s = (yb ** 0.56 - yt ** 0.57) * 1.14
        return 0.0 if s < 0.1 else (s - 0.027) * 100
    s = (yb ** 0.65 - yt ** 0.62) * 1.14
    return 0.0 if s > -0.1 else (s + 0.027) * 100
def hexrgb(c): return "#%02X%02X%02X" % c

def seuil_apca(px, gras):
    """Seuils APCA « bronze » simplifiés (tableau de correspondance police/Lc, 2022) : Lc minimal pour un texte de contenu."""
    if px >= 24 or (px >= 16 and gras): return 60
    if px >= 16: return 75 if not gras else 60
    if px >= 14: return 90 if not gras else 75
    return 100  # en dessous de 14 px, APCA réserve le texte à l'accessoire (Lc 100 pour du contenu)

fichiers = sorted(glob.glob(f"{BANC}/*--*--*.json"))
etats = []
for f in fichiers:
    nom = os.path.basename(f)[:-5]
    ecran, etat, conf = nom.split("--")
    theme, police = conf.split("-")
    d = json.load(open(f))
    etats.append((ecran, etat, theme, int(police), d))

contrastes = {}
cibles, a11y, police_rows, rendus = [], [], [], []
for ecran, etat, theme, police, d in etats:
    vues = d["vues"]
    racine = vues[0]
    par_chemin = {v["chemin"]: v for v in vues}
    for v in vues:
        if v["l"] <= 0 or v["h"] <= 0: continue
        if "texte" in v and v["texte"].strip() and ecran != "dialogue":  # le fond des boîtes d'Android (InsetDrawable) n'est pas relevé
            fg = sur(v["fond"], v["couleurTexte"])
            bg = sur("#FF000000", v["fond"])
            alpha = v.get("alpha", 1)
            if alpha < 1: fg = tuple(round(f * alpha + b * (1 - alpha)) for f, b in zip(fg, bg))
            px = v["tailleDp"]; gras = v.get("graisse", 400) >= 500
            cle = (theme, hexrgb(fg), hexrgb(bg), round(px, 1), gras)
            e = contrastes.setdefault(cle, {"n": 0, "exemples": collections.OrderedDict()})
            e["n"] += 1
            e["exemples"].setdefault(f"{ecran}/{etat}: {v['texte'][:40]!r}", None)
            if police == 100:
                rendus.append((ecran, etat, theme, v["texte"].replace("\n", " ⏎ ")[:120], round(v["tailleSp"], 1), v.get("graisse", 400), hexrgb(fg), v["couleurTexte"], hexrgb(bg), v["classe"]))
            if v.get("points", 0) or v.get("debordeVertical"):
                police_rows.append((police, theme, ecran, etat, v["texte"].replace("\n", " ⏎ ")[:80], round(v["tailleSp"], 1), round(v["l"], 1), round(v["h"], 1),
                                    "points" if v.get("points") else "", "rogné en hauteur" if v.get("debordeVertical") else "", ""))
        # Une réplique (texte sélectionnable) est « cliquable » pour Android mais n'est pas une cible ; la barre de
        # position est une cible sans être « cliquable ».
        selectionnable = v["classe"] == "TextView" and v["cliquable"] and not v.get("description")
        if (v["cliquable"] and not selectionnable) or v["classe"] == "SeekBar":
            nom_a11y = v.get("description") or v.get("texte") or ""
            if not nom_a11y:  # nom tiré des enfants, comme TalkBack
                nom_a11y = " ".join(w.get("texte", "") for k, w in par_chemin.items() if k.startswith(v["chemin"] + "/") and w.get("texte") and w.get("importantA11y", 0) != 2).strip()
            cibles.append((police, theme, ecran, etat, v["classe"], v.get("roleA11y", ""), nom_a11y.replace("\n", " ⏎ ")[:70], round(v["l"], 1), round(v["h"], 1),
                           "oui" if min(v["l"], v["h"]) < 48 - 0.5 else "", "oui" if v["l"] < 24 or v["h"] < 24 else "", v["actif"], v.get("alpha", 1)))
            if police == 100 and theme == "clair":
                role = v.get("roleA11y", "").split(".")[-1]
                manque = []
                if role in ("LinearLayout", "FrameLayout", "ImageView", "View"): manque.append("rôle absent (pas « bouton »)")
                if not nom_a11y: manque.append("sans nom")
                if v.get("alpha", 1) < 0.9 and v["actif"]: manque.append("grisé mais actif")
                if v["classe"] in ("ListView",): continue
                if v["classe"] == "LinearLayout" and "etatA11y" in v and "Switch" not in role: manque.append("interrupteur annoncé comme bloc")
                a11y.append((ecran, etat, v["classe"], role, nom_a11y.replace("\n", " ⏎ ")[:70], v.get("etatA11y", ""), v.get("choisi", ""), "; ".join(manque)))
    if police == 100 and theme == "clair":
        for v in vues:
            if "texte" in v and v["texte"] and not v["cliquable"]:
                # Titres : ce qui ressemble à un titre de groupe ou de jour (14 sp gras, couleur « titre »).
                if v.get("graisse", 400) >= 500 and 13.5 <= v["tailleSp"] <= 14.5:
                    a11y.append((ecran, etat, v["classe"], "titre visuel", v["texte"][:70], "", "", "" if v.get("titreA11y") else "titre non déclaré (isAccessibilityHeading)"))
        # Chevauchements de textes frères (la barre du bas à 200 %).
    if police == 200:
        textes = [v for v in vues if v.get("texte") and v["l"] > 0]
        for i, a in enumerate(textes):
            for b in textes[i + 1:]:
                if a["chemin"].rsplit("/", 1)[0] == b["chemin"].rsplit("/", 1)[0]: continue
                if a["texte"].isdigit() and b["texte"].isdigit(): continue  # cases du calendrier : la vue remplit la case
                ix = min(a["x"] + a["l"], b["x"] + b["l"]) - max(a["x"], b["x"])
                iy = min(a["y"] + a["h"], b["y"] + b["h"]) - max(a["y"], b["y"])
                gap = max(a["x"], b["x"]) - min(a["x"] + a["l"], b["x"] + b["l"])
                if iy > 4 and -1 < gap < 2 and abs(a["y"] - b["y"]) < 4:
                    police_rows.append((police, theme, ecran, etat, f"{a['texte'][:30]} | {b['texte'][:30]}", round(a["tailleSp"], 1), "", "", "", "", f"collés ({gap:.1f} dp)"))

os.makedirs(OUT, exist_ok=True)
def ecrire(nom, entetes, rangs):
    with open(f"{OUT}/{nom}", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(entetes); w.writerows(rangs)

rang_c = []
for (theme, fg, bg, px, gras), e in contrastes.items():
    a = tuple(int(fg[i:i + 2], 16) for i in (1, 3, 5)); b = tuple(int(bg[i:i + 2], 16) for i in (1, 3, 5))
    r = wcag(a, b); lc = apca(a, b)
    grand = px >= 24 or (px >= 18.66 and gras)
    seuil = 3 if grand else 4.5
    sa = seuil_apca(px, gras)
    rang_c.append((theme, fg, bg, px, "oui" if gras else "", round(r, 2), seuil, "OK" if r >= seuil else "ÉCHEC", round(lc, 1), sa, "OK" if abs(lc) >= sa else "sous le seuil",
                   e["n"], " | ".join(list(e["exemples"].keys())[:4])))
rang_c.sort(key=lambda x: (x[0], x[5]))
ecrire("contrastes.csv", ["theme", "texte", "fond", "taille_dp", "gras", "wcag2", "seuil_wcag", "wcag_1.4.3", "apca_lc", "seuil_apca", "apca", "occurrences", "exemples"], rang_c)
ecrire("cibles.csv", ["police_%", "theme", "ecran", "etat", "classe", "role_a11y", "nom_a11y", "largeur_dp", "hauteur_dp", "sous_48dp", "sous_24dp_wcag_2.5.8", "actif", "alpha"], cibles)
ecrire("accessibilite.csv", ["ecran", "etat", "classe", "role", "nom", "etat_a11y", "choisi", "manques"], a11y)
ecrire("police.csv", ["police_%", "theme", "ecran", "etat", "texte", "taille_sp", "largeur_dp", "hauteur_dp", "points", "rogne", "autre"], police_rows)
ecrire("textes-rendus.csv", ["ecran", "etat", "theme", "texte", "taille_sp", "graisse", "couleur_composee", "couleur_code", "fond_compose", "classe"], rendus)

# Couples statiques que le banc ne relève pas : icônes, indices, couleurs d'état sur les fonds, dans les deux thèmes.
FONDS = {"clair": (0xF5, 0xF5, 0xF5), "sombre": (0x1E, 0x1E, 0x1E)}
def ink(theme, a):
    base = (0, 0, 0) if theme == "clair" else (255, 255, 255); f = FONDS[theme]
    return tuple(round(x * a + y * (1 - a)) for x, y in zip(base, f))
def carte(theme, a=0.05): return ink(theme, a)
statiques = [
    ("Accent LinkService.ACCENT en texte (Relier un calendrier, Journal, aujourd'hui)", {"clair": (0x00, 0x64, 0xD2), "sombre": (0x00, 0x64, 0xD2)}, "fond"),
    ("Accent du sombre prévu par Tone.INFO (#409CFF)", {"clair": (0x00, 0x64, 0xD2), "sombre": (0x40, 0x9C, 0xFF)}, "fond"),
    ("Accent sur carte (Relier un calendrier dans le groupe)", {"clair": (0x00, 0x64, 0xD2), "sombre": (0x00, 0x64, 0xD2)}, "carte"),
    ("Icônes secondaires (ink 0,6/0,62)", {"clair": ink("clair", 0.6), "sombre": ink("sombre", 0.62)}, "fond"),
    ("Chevron des Réglages (ink 0,4)", {"clair": ink("clair", 0.4), "sombre": ink("sombre", 0.4)}, "carte"),
    ("Heure d'une réplique (ink 0,5)", {"clair": ink("clair", 0.5), "sombre": ink("sombre", 0.5)}, "fond"),
    ("Point d'un jour (ink 0,45)", {"clair": ink("clair", 0.45), "sombre": ink("sombre", 0.45)}, "fond"),
    ("Vignette par défaut (ink 0,55) sur sa plaque 0,07", {"clair": ink("clair", 0.55), "sombre": ink("sombre", 0.55)}, "plaque"),
    ("Signal #3B45FD sur plaque", {"clair": (0x3B, 0x45, 0xFD), "sombre": (0x3B, 0x45, 0xFD)}, "plaque"),
    ("WhatsApp #25D366 sur plaque", {"clair": (0x25, 0xD3, 0x66), "sombre": (0x25, 0xD3, 0x66)}, "plaque"),
    ("Telegram #26A5E4 sur plaque", {"clair": (0x26, 0xA5, 0xE4), "sombre": (0x26, 0xA5, 0xE4)}, "plaque"),
    ("Meet #00897B sur plaque", {"clair": (0x00, 0x89, 0x7B), "sombre": (0x00, 0x89, 0x7B)}, "plaque"),
    ("Point rouge des appels #D32F2F", {"clair": (0xD3, 0x2F, 0x2F), "sombre": (0xD3, 0x2F, 0x2F)}, "fond"),
    ("Enregistrement Tone.LIVE", {"clair": (0xC4, 0x1E, 0x14), "sombre": (0xFF, 0x45, 0x3A)}, "fond"),
    ("Avertissement Tone.WARNING sur carte", {"clair": (0xA0, 0x47, 0x0A), "sombre": (0xFF, 0x9F, 0x0A)}, "carte"),
    ("Texte blanc sur bouton accent (Scanner le code du Mac)", {"clair": (255, 255, 255), "sombre": (255, 255, 255)}, "accent"),
    ("Bouton accent sur fond (contour de la forme)", {"clair": (0x00, 0x64, 0xD2), "sombre": (0x00, 0x64, 0xD2)}, "fond"),
    ("Barre de position au repos (ink 0,12)", {"clair": ink("clair", 0.12), "sombre": ink("sombre", 0.12)}, "carte"),
    ("Carte (ink 0,05) contre le fond : la masse se voit-elle ?", {"clair": carte("clair"), "sombre": carte("sombre")}, "fond"),
]
rang_s = []
for nom, couleurs, fond in statiques:
    for theme in ("clair", "sombre"):
        f = {"fond": FONDS[theme], "carte": carte(theme), "plaque": ink(theme, 0.07), "accent": (0x00, 0x64, 0xD2)}[fond]
        c = couleurs[theme]
        rang_s.append((nom, theme, hexrgb(c), hexrgb(f), round(wcag(c, f), 2), round(apca(c, f), 1)))
ecrire("contrastes-statiques.csv", ["element", "theme", "couleur", "fond", "wcag2", "apca_lc"], rang_s)

resume = {
    "etats_captures": len(etats), "ecrans": len({e[0] for e in etats}), "etats_distincts": len({(e[0], e[1]) for e in etats}),
    "couples_contraste": len(rang_c), "couples_wcag_echec": sum(1 for r in rang_c if r[7] == "ÉCHEC"),
    "couples_apca_sous_seuil": sum(1 for r in rang_c if r[10] != "OK"),
    "cibles_relevees": len(cibles), "cibles_sous_48dp_100": sum(1 for r in cibles if r[0] == 100 and r[9]),
    "cibles_distinctes_sous_48dp_100": len({(r[2], r[6], r[7], r[8]) for r in cibles if r[0] == 100 and r[1] == "clair" and r[9]}),
    "a11y_manques": sum(1 for r in a11y if r[7]),
    "police_problemes": collections.Counter(r[0] for r in police_rows),
    "textes_rendus_100": len(rendus),
    "contrastes_statiques": len(rang_s),
}
json.dump(resume, open(f"{OUT}/mesures-resume.json", "w"), indent=1, ensure_ascii=False, default=str)
print(json.dumps(resume, ensure_ascii=False, default=str, indent=1))

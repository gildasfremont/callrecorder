#!/usr/bin/env python3
"""Relevé statique de l'app Android : textes visibles, tailles de police, couleurs, opacités, dp, rayons, icônes.

Lancer depuis la racine du dépôt :  python3 design/recos/ux-android/outils/inventaire_code.py
Écrit des CSV dans design/recos/ux-android/donnees/. Chaque ligne porte fichier:ligne.
"""
import csv, os, re, glob, collections, json

RACINE = os.getcwd()
SRC = "phone/android/app/src/main/java/fyi/gildas/callrecorder"
RES = "phone/android/app/src/main/res"
OUT = "design/recos/ux-android/donnees"
os.makedirs(OUT, exist_ok=True)

fichiers = sorted(glob.glob(f"{SRC}/*.kt") + glob.glob(f"{SRC}/*.java"))
lignes = {f: open(f, encoding="utf-8").read().split("\n") for f in fichiers}
court = lambda f: os.path.relpath(f, "phone/android/app/src/main")

# Écrans et pièces d'interface (le reste est le service, le lien, la capture).
INTERFACE = {"HomeScreen.kt", "ConversationScreen.kt", "SettingsScreen.kt", "SetupScreen.kt", "Screen.kt", "Look.kt", "Pastille.kt", "MainActivity.kt", "CallService.kt", "LinkService.kt"}

def ecrire(nom, entetes, rangs):
    with open(f"{OUT}/{nom}", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(entetes); w.writerows(rangs)
    return len(rangs)

# ---------- Textes visibles ----------
CONTEXTES = [
    ("notification-titre", r"setContentTitle\("), ("notification-texte", r"setContentText\("), ("notification-canal", r"NotificationChannel\("),
    ("notification-action", r"Action\.Builder\("), ("dialogue-titre", r"setTitle\("), ("dialogue-message", r"setMessage\("),
    ("dialogue-bouton", r"set(Positive|Negative|Neutral)Button\("), ("toast", r"Toast\.makeText"), ("indice", r"hint\s*="),
    ("nom-a11y", r"contentDescription\s*="), ("etat-a11y", r"stateDescription\s*="), ("ligne-pied", r"footRow\("), ("ligne-chevron", r"chevronRow\("),
    ("bouton-icone", r"iconButton\("), ("outil", r"\btool\("), ("mode", r"Triple\("), ("menu", r"menu\.add\("), ("arret", r"problem\s*="),
    ("libelle", r"label\("), ("texte", r"\btext\s*="), ("titre-ecran", r"\bto\s+\(|->\s*\"|to\s+\""),
]
LOG = re.compile(r"\b(Link\.)?log\(|Log\.[iwed]\(|Exception\(|getSharedPreferences|putExtra|getString\(\"|optString|optBoolean|optLong|put\(\"|JSONObject|Regex|startsWith|contains\(\"|split\(|MODEL|\.json|\.pcm|\.m4a|\.opus|\.txt\"|RELATIVE_PATH|_tcp|DISPLAY_NAME")
CHAINE = re.compile(r'"((?:[^"\\$]|\\.|\$\{[^}]*\}|\$[a-zA-Z_]+)*)"')
FR = re.compile(r"[A-Za-zÀ-ÿ]{2,}")
textes = []
for f, ls in lignes.items():
    for i, l in enumerate(ls, 1):
        if LOG.search(l) or l.strip().startswith(("//", "*", "/*", "import", "package", "@")):
            continue
        for m in CHAINE.finditer(l):
            s = m.group(1)
            if not FR.search(s) or len(s) < 2: continue
            if re.fullmatch(r"[a-z_\-]+(\.[a-z_]+)*", s): continue  # identifiants
            if re.fullmatch(r"[A-Za-z_]+", s) and s[0].islower(): continue
            if s in {"sans-serif-medium", "HmacSHA256", "AES/GCM/NoPadding", "SHA-256", "UTF-8", "CallRecorder"} and "label" not in l: continue
            ctx = next((n for n, p in CONTEXTES if re.search(p, l)), "autre")
            textes.append((court(f), i, ctx, s, l.strip()[:160]))
# Manifeste et ressources.
for f in [f"phone/android/app/src/main/AndroidManifest.xml", f"{RES}/values/strings.xml"]:
    for i, l in enumerate(open(f, encoding="utf-8").read().split("\n"), 1):
        for m in re.finditer(r'android:label="([^"]+)"', l): textes.append((os.path.relpath(f, "phone/android/app/src/main"), i, "etiquette-android", m.group(1), l.strip()[:160]))
        m = re.search(r'<string name="([^"]+)">(.*)</string>', l)
        if m: textes.append((os.path.relpath(f, "phone/android/app/src/main"), i, "ressource:" + m.group(1), m.group(2).replace("\\'", "'"), ""))
n_textes = ecrire("textes.csv", ["fichier", "ligne", "contexte", "texte", "code"], textes)

# ---------- Tailles de police ----------
tailles = []
for f, ls in lignes.items():
    for i, l in enumerate(ls, 1):
        for m in re.finditer(r"textSize\s*=\s*([\d.]+)f", l):
            tailles.append((court(f), i, float(m.group(1)), "textSize", l.strip()[:140]))
        for m in re.finditer(r"label\(([^()]*(?:\([^()]*\)[^()]*)*)\)", l):
            args = m.group(1)
            t = re.search(r"(?:,\s*|size\s*=\s*)([\d.]+)f", args)
            bold = "bold = true" in args
            tailles.append((court(f), i, float(t.group(1)) if t else 16.0, "label" + (" gras" if bold else "") + ("" if t else " (défaut 16)"), l.strip()[:140]))
        if "RelativeSizeSpan" in l:
            m = re.search(r"RelativeSizeSpan\(([\d.]+)f", l); tailles.append((court(f), i, round(16 * float(m.group(1)), 2), "RelativeSizeSpan × 16", l.strip()[:140]))
n_tailles = ecrire("tailles-police.csv", ["fichier", "ligne", "sp", "forme", "code"], tailles)

# ---------- Couleurs ----------
couleurs = []
for f, ls in lignes.items():
    for i, l in enumerate(ls, 1):
        for m in re.finditer(r"0x([0-9A-Fa-f]{8})", l):
            if "and 0x" in l and m.group(1).upper() in ("00FFFFFF",): continue
            couleurs.append((court(f), i, "#" + m.group(1).upper(), "littérale", l.strip()[:140]))
        for m in re.finditer(r"ink\(([\d.]+)\)", l): couleurs.append((court(f), i, f"ink({m.group(1)})", "opacité du texte", l.strip()[:140]))
        for m in re.finditer(r"(LinkService\.ACCENT|Tone\.(LIVE|WARNING|INFO|OK|NEUTRAL|STOPPED)|look\.(secondary|title|text|background|floating))", l):
            couleurs.append((court(f), i, m.group(1), "nommée", l.strip()[:140]))
n_couleurs = ecrire("couleurs.csv", ["fichier", "ligne", "valeur", "forme", "code"], couleurs)

# ---------- Opacités ----------
opac = []
for f, ls in lignes.items():
    for i, l in enumerate(ls, 1):
        for m in re.finditer(r"(?:ink|mass)\(([^)]*)\)", l):
            for a in re.findall(r"(?<![\w.])0\.\d+", m.group(1)): opac.append((court(f), i, float(a), m.group(0), l.strip()[:140]))
        for m in re.finditer(r"alpha\s*=\s*(?:if[^0-9]*)?([\d.]+)f", l): opac.append((court(f), i, float(m.group(1)), "alpha de vue", l.strip()[:140]))
        for m in re.finditer(r"or 0x([0-9A-F]{2})000000", l): opac.append((court(f), i, round(int(m.group(1), 16) / 255, 3), "teinte + alpha 0x" + m.group(1), l.strip()[:140]))
n_opac = ecrire("opacites.csv", ["fichier", "ligne", "opacite", "forme", "code"], opac)

# ---------- dp : espacements, tailles, rayons ----------
dps = []
def role(l, pos):
    avant = l[:pos]
    for mot, r in [("setPadding", "marge interne"), ("Margin", "marge externe"), ("setMargins", "marge externe"), ("marginStart", "marge externe"), ("marginEnd", "marge externe"), ("topMargin", "marge externe"), ("bottomMargin", "marge externe"),
                   ("minimumHeight", "hauteur mini"), ("minHeight", "hauteur mini"), ("minimumWidth", "largeur mini"), ("LayoutParams", "taille"), ("cornerRadius", "rayon"), ("elevation", "élévation"), ("setBounds", "taille icône"), ("compoundDrawablePadding", "marge interne")]:
        if mot in avant[-60:]: r0 = r
    try: return r0
    except NameError: return "autre"
for f, ls in lignes.items():
    for i, l in enumerate(ls, 1):
        for m in re.finditer(r"dp\(([\d.]+)\)", l):
            dps.append((court(f), i, float(m.group(1)), role(l, m.start()), l.strip()[:140]))
        for m in re.finditer(r"\b(mass|flat)\(([\d.]+)", l):
            dps.append((court(f), i, float(m.group(2)), "rayon", l.strip()[:140]))
        for m in re.finditer(r"(icon|iconButton|kindPlate)\([^)]*?,\s*(\d+)\)", l):
            dps.append((court(f), i, float(m.group(2)), "taille icône", l.strip()[:140]))
n_dp = ecrire("dp.csv", ["fichier", "ligne", "dp", "role", "code"], dps)

# ---------- Icônes ----------
dessins = sorted(os.path.splitext(os.path.basename(p))[0] for p in glob.glob(f"{RES}/drawable/*.xml"))
usages = collections.defaultdict(list)
for f, ls in lignes.items():
    for i, l in enumerate(ls, 1):
        for m in re.finditer(r"R\.drawable\.(\w+)|android\.R\.drawable\.(\w+)", l):
            nom = m.group(1) or ("android:" + m.group(2))
            usages[nom].append(f"{court(f)}:{i}")
icones = [(d, len(usages.get(d, [])), " ".join(usages.get(d, []))) for d in dessins] + [(k, len(v), " ".join(v)) for k, v in usages.items() if k.startswith("android:")]
n_icones = ecrire("icones.csv", ["icone", "usages", "ou"], icones)

resume = {"textes": n_textes, "tailles": n_tailles, "couleurs": n_couleurs, "opacites": n_opac, "dp": n_dp, "icones": n_icones,
          "fichiers": len(fichiers), "lignes_de_code": sum(len(v) for v in lignes.values())}
json.dump(resume, open(f"{OUT}/inventaire-resume.json", "w"), indent=1, ensure_ascii=False)
print(resume)

# ---------- Visible ou technique ----------
# Une chaîne est « visible » si elle sort à l'écran, dans une notification ou une boîte ; le reste (journal, formats,
# autorisations, chemins) est technique. Règle automatique, puis exceptions relevées à la main.
TECH = re.compile(r"^(android\.|package:|com\.|image/|text/|\.|%|yyyy|MMMM|\$\{android|\$\{month|\$\{Build|\$start|ble\\|AES|mCalls|journal\.|\$\{stamp|\[\$)|^[a-zé]")
JOURNAL = {("LinkService.kt", 297), ("LinkService.kt", 394), ("LinkService.kt", 443), ("LinkService.kt", 474), ("LinkService.kt", 487), ("Speech.kt", 245),
           ("MainActivity.kt", 189), ("SetupReceiver.kt", 27), ("Recordings.kt", 339), ("Voices.kt", 221), ("Voices.kt", 224),
           ("HomeScreen.kt", 198), ("Screen.kt", 176), ("ConversationScreen.kt", 233), ("ConversationScreen.kt", 365)}
p = f"{OUT}/textes.csv"
r = list(csv.DictReader(open(p, encoding="utf-8")))
for x in r:
    f, l = x["fichier"].split("/")[-1], int(x["ligne"])
    vis = not TECH.search(x["texte"]) and (f, l) not in JOURNAL
    if x["texte"] in ("Mac", "votre Mac", "Votre Mac"): vis, x["contexte"] = True, "nom-par-defaut"
    if (f, l) == ("Agenda.kt", 125): x["contexte"] = "notification-titre (Agenda.at)"
    x["visible"] = "oui" if vis else "non"
with open(p, "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=["fichier", "ligne", "contexte", "visible", "texte", "code"]); w.writeheader(); w.writerows(r)
print("textes visibles :", sum(x["visible"] == "oui" for x in r))

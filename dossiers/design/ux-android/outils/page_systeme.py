"""Page « Système et migration » : le système unifié proposé, ses contrastes recalculés, et la table de migration
« valeur actuelle → nouvelle », fichier par fichier, tirée des relevés (tailles-police.csv, dp.csv, couleurs.csv)."""
import collections, csv
from commun import *

# --- Mesures (mêmes formules que mesures.py) ---
def lum(c):
    def ch(x):
        x /= 255; return x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4
    return 0.2126 * ch(c[0]) + 0.7152 * ch(c[1]) + 0.0722 * ch(c[2])
def wcag(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True); return (la + 0.05) / (lb + 0.05)
def h2c(h): h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
def mix(c, b, a): return tuple(round(x * a + y * (1 - a)) for x, y in zip(c, b))

FOND = {"clair": h2c("F5F5F5"), "sombre": h2c("1E1E1E")}
INK = {"clair": (0, 0, 0), "sombre": (255, 255, 255)}
def ink(t, a): return mix(INK[t], FOND[t], a)
def carte(t): return ink(t, 0.05)

TYPO = [
    ("titre-ecran", "titleLarge", 22, 400, 28, "Titre d'une rubrique : Réglages ; titre de la mise en route"),
    ("titre-objet", "titleMedium", 16, 500, 22, "Titre d'une conversation ou du Journal (avec son détail) ; mois du calendrier"),
    ("corps", "bodyLarge", 16, 400, 22, "Répliques, titres de ligne, champs, lignes de pied et de réglage, chiffres du calendrier, états vides"),
    ("soutien", "bodyMedium", 14, 400, 20, "Méta d'une ligne, détail d'un en-tête, phrase d'un réglage, valeur d'une rangée"),
    ("titre-groupe", "titleSmall", 14, 500, 20, "Jours de la liste, titres de groupe, nom de qui parle"),
    ("action-texte", "labelLarge", 14, 500, 20, "Boutons texte et pleins (Relier un calendrier, Scanner le code du Mac, Arrêter · 12:34)"),
    ("outil", "labelMedium", 12, 500, 16, "Mots sous les outils, lettres des jours"),
    ("accessoire", "bodySmall", 12, 400, 16, "Heures d'une réplique, temps du lecteur"),
]
# fichier:ligne → (rôle, note)
MIGR_TYPO = {
    "ConversationScreen.kt:56": "titre-objet", "ConversationScreen.kt:57": "soutien", "ConversationScreen.kt:61": "corps", "ConversationScreen.kt:64": "corps",
    "ConversationScreen.kt:98": "accessoire", "ConversationScreen.kt:178": "outil", "ConversationScreen.kt:320": "décor 13 dp", "ConversationScreen.kt:324": "titre-groupe",
    "ConversationScreen.kt:325": "accessoire", "ConversationScreen.kt:326": "corps", "HomeScreen.kt:71": "corps", "HomeScreen.kt:240": "titre-groupe", "HomeScreen.kt:272": "corps",
    "HomeScreen.kt:273": "soutien", "HomeScreen.kt:284": "titre-objet", "HomeScreen.kt:289": "outil", "HomeScreen.kt:316": "corps", "Screen.kt:37": "corps", "Screen.kt:133": "corps",
    "Screen.kt:146": "corps", "Screen.kt:147": "soutien", "SettingsScreen.kt:32": "soutien", "SettingsScreen.kt:35": "corps", "SettingsScreen.kt:55": "soutien",
    "SettingsScreen.kt:58": "action-texte", "SettingsScreen.kt:87": "soutien", "SettingsScreen.kt:110": "corps", "SettingsScreen.kt:121": "titre-groupe",
    "SettingsScreen.kt:125": "titre-ecran", "SetupScreen.kt:16": "titre-ecran", "SetupScreen.kt:17": "corps", "SetupScreen.kt:20": "action-texte",
}

COULEURS = [  # nom, clair, sombre, rôle, fond de contrôle
    ("fond", "#F5F5F5", "#1E1E1E", "Fond de l'écran", None),
    ("texte", "#1D1D1F", "#F5F5F7", "Texte principal", "fond"),
    ("secondaire", "ink 0,60", "ink 0,62", "Texte et icônes secondaires, heures, chevrons", "carte"),
    ("titre", "ink 0,56", "ink 0,62", "Titres de jour et de groupe", "fond"),
    ("desactive", "ink 0,38", "ink 0,38", "Contrôle désactivé (Material 3 : 38 %)", None),
    ("piste", "ink 0,50", "ink 0,50", "Piste de la barre de position", "carte"),
    ("carte", "ink 0,05", "ink 0,05", "Masse d'un groupe, d'une carte", None),
    ("plaque", "ink 0,07", "ink 0,07", "Vignette, capsule Liste/Calendrier", None),
    ("choisi", "ink 0,12", "ink 0,12", "Toucher, élément choisi (sauf jour : accent plein)", None),
    ("accent", "#0064D2", "#409CFF", "Action, lecture, aujourd'hui, Journal", "carte"),
    ("sur-accent", "#FFFFFF", "#1E1E1E", "Texte et icône sur un fond accent", "accent"),
    ("moi", "#0057B8", "#409CFF", "« Moi » et ses initiales (sur sa teinte 12 %)", "teinte-moi"),
    ("autres", "#A0470A", "#FF9F0A", "Initiales des autres (sur leur teinte 12 %)", "teinte-autres"),
    ("enregistrement", "#C41E14", "#FF453A", "En cours, Arrêter, point rouge des appels", "fond"),
    ("avertissement", "#A0470A", "#FF9F0A", "Ce qui empêche quelque chose", "carte"),
    ("flottant", "#FFFFFF F0", "#2C2C2E F0", "Barre flottante, pastille", None),
    ("whatsapp", "#128C7E", "#25D366", "Vignette WhatsApp", "plaque"),
    ("signal", "#3B45FD", "#7A82FF", "Vignette Signal", "plaque"),
    ("telegram", "#1C7DB8", "#26A5E4", "Vignette Telegram", "plaque"),
    ("meet", "#00897B", "#00A896", "Vignette Meet", "plaque"),
]
def valeur(t, v):
    if v.startswith("ink"): return ink(t, float(v.split()[1].replace(",", ".")))
    return h2c(v.split()[0])
def fond_de(t, nom):
    if nom == "fond": return FOND[t]
    if nom == "carte": return carte(t)
    if nom == "plaque": return ink(t, 0.07)
    if nom == "accent": return valeur(t, "#0064D2" if t == "clair" else "#409CFF")
    if nom == "teinte-moi": return mix(valeur(t, "#0064D2" if t == "clair" else "#409CFF"), FOND[t], 0.12)
    if nom == "teinte-autres": return mix(valeur(t, "#A0470A" if t == "clair" else "#FF9F0A"), FOND[t], 0.12)

ESP = [(4, "Écart dans un groupe serré : icône/texte d'un champ, lignes d'une liste"), (8, "Icône et son texte ; entre deux groupes de lignes"), (12, "Marge de l'écran et des cartes ; entre vignette et texte"),
       (16, "Marge de lecture (répliques) ; entre deux blocs"), (24, "Entre deux groupes de réglages ; bas de la barre flottante"), (32, "État vide, mise en route")]
FORMES = [("ligne", "8 dp", "Ligne touchable, vignette, case"), ("carte", "12 dp", "Groupe, carte, lecteur, champ"), ("pilule", "hauteur ÷ 2", "Bouton plein, capsule, barre flottante, pastille, rond")]

MIGR_RAYON = {"ConversationScreen.kt:81": "pilule (48 dp → 24)", "ConversationScreen.kt:130": "<b>pilule : 64 dp → 32</b> (aujourd'hui 24 : pas une capsule)", "ConversationScreen.kt:173": "pilule (56 dp → 28)",
              "ConversationScreen.kt:355": "pilule (36 dp → 18) : inchangé", "HomeScreen.kt:64": "pilule (52 → 26) : inchangé", "HomeScreen.kt:114": "pilule : inchangé", "HomeScreen.kt:312": "pilule ; choisi = accent plein (P08)",
              "Pastille.kt:42": "pilule : inchangé", "Screen.kt:65": "pilule : inchangé", "SetupScreen.kt:25": "pilule : inchangé"}
ECHELLE = {2, 4, 8, 12, 16, 24, 32}
def proche(v):
    return min(sorted(ECHELLE), key=lambda x: (abs(x - v), -x))

def construire():
    c = ["<h1>Système et migration : 8 rôles de texte sur 4 tailles, 20 couleurs nommées, 6 espacements, 3 formes</h1>",
         """<p class="lead">Un système pour l'app Android, tiré de ce qu'elle emploie déjà (inventaire) et de Material 3, sans changer son allure de Mac :
mêmes masses grises, même accent, mêmes formes. Il remplace 6 tailles de texte par 4, 9 gris par 4 opacités nommées, 13 marges par 6, 7 rayons par 3 formes,
et donne à l'accent une valeur sombre. Chaque ligne de la table de migration est un emploi relevé dans le code.</p>"""]
    # Typo
    c.append('<h2 id="typo">1. Texte</h2>')
    usages = collections.Counter(MIGR_TYPO.values())
    c.append(tableau(["Rôle", "Material 3", "Taille", "Graisse", "Interligne", "Emplois après", "Pour"],
                     [[f"<code>{r}</code>", t, f"{s} sp", g, f"{l} sp", usages.get(r, 0), e(p)] for r, t, s, g, l, p in TYPO], brut=True))
    c.append('<p class="note">Une exception voulue : les initiales dans leur rond restent en 13 dp (ni sp ni rôle), parce que le rond ne grandit pas avec la police et que le nom écrit à côté porte le sens (P04).</p>')
    # Couleurs
    c.append('<h2 id="couleurs">2. Couleurs</h2>')
    rangs = []
    for nom, cl, so, role, f in COULEURS:
        cells = [f"<code>{nom}</code>"]
        for t, v in (("clair", cl), ("sombre", so)):
            rgb = valeur(t, v)
            cells.append(f'<span class="sw" style="background:rgb{rgb}"></span><code>{e(v)}</code>')
        for t, v in (("clair", cl), ("sombre", so)):
            if f:
                r = wcag(valeur(t, v), fond_de(t, f)); seuil = 3 if nom in ("piste", "whatsapp", "signal", "telegram", "meet") else 4.5
                cells.append(f'<span class="{"ok" if r >= seuil else "ko"}">{r:.2f}:1</span> <span style="color:var(--sec)">sur {f}</span>')
            else: cells.append("—")
        cells.append(e(role)); rangs.append(cells)
    c.append(tableau(["Nom", "Clair", "Sombre", "Contraste clair", "Contraste sombre", "Rôle"], rangs, brut=True))
    c.append('<p class="note">Seuils : 4,5:1 pour du texte, 3:1 pour un repère graphique (piste, logos ; WCAG 1.4.11). Tous les couples du système passent. Les couleurs de marque prennent une variante par thème, comme le font les apps qui posent un logo sur un fond neutre ; la teinte reste reconnaissable.</p>')
    # Espacements, formes
    c.append('<h2 id="espacements">3. Espacements</h2>')
    c.append(tableau(["Valeur", "Pour"], [[f"{v} dp", p] for v, p in ESP]))
    c.append("<p>Plus 2 dp, réservé à l'écart entre deux pièces collées (Liste/Calendrier, rangées d'un groupe), et les tailles de cible : 36, 44 → 48, 48, 64.</p>")
    c.append('<h2 id="formes">4. Formes</h2>')
    c.append(tableau(["Forme", "Rayon", "Pour"], FORMES))
    c.append("<p>Une fonction <code>pill(view)</code> calcule le rayon à la mesure (<code>height / 2</code>) au lieu de l'écrire : la barre flottante est aujourd'hui en rayon 24 pour 64 dp de haut.</p>")
    # Composants
    c.append('<h2 id="composants">5. Composants</h2>')
    c.append(tableau(["Composant", "Mesures", "États", "Accessibilité"], [
        ["Barre d'écran (bar)", "64 dp mini, hauteur libre ; retour 48 ; titre titleLarge ou titleMedium + soutien", "—", "titre : heading"],
        ["Ligne de conversation (talkRow)", "64 dp mini, padding 8, vignette 44 (icône 20, rayon 8), écart 12, corps + soutien", "normale, en cours (rouge), en attente (« pas encore sur le Mac »)", "rôle bouton ; description sans symboles"],
        ["Ligne de pied (footRow)", "48 dp, icône 24, écart 8, corps", "normale, rouge (Arrêter)", "rôle bouton"],
        ["Rangée de réglage (chevronRow)", "48 dp, corps + soutien à droite, chevron 16 en secondaire", "normale, avertissement", "rôle bouton ; « nom, valeur »"],
        ["Rangée à interrupteur", "48 dp, Switch du thème (accent de l'app)", "allumé, éteint, sans effet (38 %)", "rôle interrupteur, état"],
        ["Bouton plein", "48 dp mini, pilule, labelLarge, sur-accent", "repos, appui, attente (indicateur à la place)", "rôle bouton"],
        ["Barre flottante", "pilule, flottant, élévation 6 ; outils 76 × 56 (icône 22 + outil) ; icônes seules ≥ 130 %", "outil actif, désactivé (38 %)", "outils : rôle bouton, isEnabled"],
        ["Capsule d'enregistrement", "pilule ; photo 48 ; Arrêter 48 rouge, « Arrêter · 12:34 » labelLarge", "en cours ; 4 s « Arrêté · Reprendre »", "rôle bouton ; temps en stateDescription"],
        ["État vide", "centré, padding 32 ; corps + soutien", "accueil, recherche, filtre, jour, Journal", "liveRegion polite pour la recherche"],
        ["Lecteur", "carte rayon 12 ; Lire 48 accent ; temps accessoire de part et d'autre ; piste 48 dp touchables", "lecture, pause", "Lire/Pause ; « 3 min sur 47 »"],
        ["Réplique", "rond 36 (13 dp), nom titre-groupe, heure accessoire, texte corps 1,38", "Moi, autres, sans voix (en direct)", "rond caché à TalkBack"],
        ["Jour du calendrier", "48 dp ; choisi : rond plein accent 40 ; aujourd'hui : cercle accent", "choisi, aujourd'hui, avec point", "isSelected"],
    ]))
    # Migration
    c.append('<h2 id="migration">6. Migration, fichier par fichier</h2>')
    c.append("<p>Tirée des relevés : chaque ligne est un emploi du code. Les changements qui corrigent un problème renvoient à sa fiche.</p>")
    T = lire("tailles-police.csv"); D = lire("dp.csv"); C = lire("couleurs.csv"); O = lire("opacites.csv")
    par_fichier = collections.defaultdict(list)
    ROLES = {r: (s, g) for r, _, s, g, _, _ in TYPO}
    for t in T:
        k = f"{t['fichier'].split('/')[-1]}:{t['ligne']}"
        role = MIGR_TYPO.get(k, "?")
        avant = f"{float(t['sp']):g} sp{' medium' if 'gras' in t['forme'] else ''}"
        if role in ROLES:
            s, g = ROLES[role]; apres = f"{role} ({s} sp{' medium' if g == 500 else ''})"
        else: apres = role
        change = avant.split()[0] != f"{ROLES.get(role, (0,))[0]}" or ("medium" in avant) != (ROLES.get(role, (0, 400))[1] == 500)
        par_fichier[t["fichier"].split("/")[-1]].append((int(t["ligne"]), "texte", avant, apres, change, f"<code>{e(t['code'][:90])}</code>"))
    for x in D:
        f = x["fichier"].split("/")[-1]; k = f"{f}:{x['ligne']}"; v = float(x["dp"])
        if x["role"] == "rayon":
            apres = MIGR_RAYON.get(k, "ligne (8)" if v == 8 else "carte (12)" if v == 12 else "pilule")
            par_fichier[f].append((int(x["ligne"]), "rayon", f"{v:g}", apres, "inchangé" not in apres and v not in (8, 12), f"<code>{e(x['code'][:90])}</code>"))
        elif x["role"] in ("marge interne", "marge externe") and v not in ECHELLE and v != 108:
            par_fichier[f].append((int(x["ligne"]), "espacement", f"{v:g} dp", f"{proche(v)} dp", True, f"<code>{e(x['code'][:90])}</code>"))
        elif x["role"] in ("taille", "hauteur mini") and v == 44:
            par_fichier[f].append((int(x["ligne"]), "taille", "44 dp", "48 dp (P10)" if "playButton" in x["code"] else "44 dp (vignette, non touchable) : inchangé", "playButton" in x["code"], f"<code>{e(x['code'][:90])}</code>"))
    for x in C:
        f = x["fichier"].split("/")[-1]; v = x["valeur"]
        apres = {"LinkService.ACCENT": "look.accent (P03)", "ink(0.5)": "secondaire (P08)", "ink(0.45)": "secondaire ou piste", "ink(0.4)": "secondaire (P08)", "ink(0.55)": "secondaire",
                 "#FFD32F2F": "enregistrement (P15)", "#FF25D366": "whatsapp (variante par thème, P08)", "#FF26A5E4": "telegram (variante par thème)", "#FF3B45FD": "signal (variante par thème)", "#FF00897B": "meet",
                 "#1F000000": "teinte 0,12", "#FFFFFFFF": "sur-accent (P03)"}.get(v)
        if apres and not (f == "LinkService.kt"):
            par_fichier[f].append((int(x["ligne"]), "couleur", v, apres, True, f"<code>{e(x['code'][:90])}</code>"))
    for x in O:
        f = x["fichier"].split("/")[-1]; v = float(x["opacite"])
        if x["forme"] == "alpha de vue":
            par_fichier[f].append((int(x["ligne"]), "état", f"alpha {v:g}", "isEnabled = false + desactive 0,38 (P09)", True, f"<code>{e(x['code'][:90])}</code>"))
    total = sum(1 for v in par_fichier.values() for r in v if r[4])
    c.append(f"<p><b>{total}</b> changements, {sum(len(v) for v in par_fichier.values())} emplois examinés, dans {len(par_fichier)} fichiers.</p>")
    for f in sorted(par_fichier):
        rangs = sorted(par_fichier[f])
        n = sum(1 for r in rangs if r[4])
        c.append(f"<h3><code>{e(f)}</code> · {n} changement{'s' if n > 1 else ''}</h3>")
        c.append(tableau(["Ligne", "Quoi", "Actuel", "Nouveau", "Code"], [[r[0], r[1], e(r[2]), (r[3] if r[4] else f'<span style="color:var(--sec)">{r[3]}</span>'), r[5]] for r in rangs], brut=True))
    with open(f"{DONNEES}/migration.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(["fichier", "ligne", "quoi", "actuel", "nouveau", "change"])
        for f in sorted(par_fichier):
            for r in sorted(par_fichier[f]): w.writerow([f, r[0], r[1], r[2], r[3].replace("<b>", "").replace("</b>", ""), "oui" if r[4] else "non"])
    c.append('<h2 id="design-md">7. Ce que DESIGN.md dirait</h2>')
    c.append("""<p>À reporter dans DESIGN.md, section Téléphone, dans le même commit que la migration (règle du dépôt : « une valeur qui change s'y change dans le même commit ») :</p>
<pre>- Texte : titleLarge 22, titleMedium 16 medium, bodyLarge 16, bodyMedium 14, titleSmall/labelLarge 14 medium, labelMedium 12 medium, bodySmall 12 (Material 3).
- Accent #0064D2, en sombre #409CFF ; sur l'accent, blanc (sombre : #1E1E1E). « Moi » #0057B8 (sombre #409CFF).
- Opacités du texte : 1, 0,6 (secondaire), 0,56/0,62 (titre), 0,38 (désactivé) ; masses 0,05, 0,07, 0,12 ; piste 0,50.
- Espacements : 4, 8, 12, 16, 24, 32 (2 pour deux pièces collées).
- Formes : ligne 8, carte 12, pilule (hauteur ÷ 2).
- Les pièces d'Android (boîtes, interrupteur, curseur) prennent l'accent par le thème de l'app.</pre>""")
    page("systeme.html", "Système et migration UX Android", "\n".join(c), "Échelle de texte, couleurs, espacements, formes, composants, et la table de migration fichier par fichier.")

if __name__ == "__main__":
    construire()

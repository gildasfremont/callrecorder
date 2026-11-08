"""Pages « Plan », « Références » et « Synthèse » (index)."""
import collections, re
from commun import *
from problemes import P, R, GRAV, FREQ

LOTS = [
    ("L1", "Ce qui trompe ou bloque, pour peu", "Les écrans disent « rien », l'arrêt est là où l'on regarde, le sombre se lit, les textes disent vrai, les petites cibles et contrastes passent.",
     "Faible : retouches locales. P02 crée une capsule dans l'app : la factoriser avec Pastille.kt pour ne pas avoir deux dessins. P05 change un texte de 25ea4c4 : scripts/retours.py ne le bloque pas (ce n'est pas un retour)."),
    ("L2", "Accessibilité et état", "TalkBack, la police agrandie, la notification, l'état du Mac, les autorisations, la couleur des pièces d'Android, les Réglages.",
     "Moyen : P04 change la hauteur des barres (vérifier chaque écran à 100, 130, 200 % au banc). P06 Live Update n'existe qu'en Android 16 : garder le chemin ancien. P12 déplace la demande Bluetooth : vérifier le lien sans Wi-Fi commun (SPEC-telephone.md)."),
    ("L3", "Détails", "Retour prédictif, pastille rattrapable, initiales, suppression, canaux, flèches, mise en route, ponctuation.",
     "P11 touche la navigation entière : tests du banc (retour, recherche) à garder verts. P15 ajoute un état à une fenêtre d'accessibilité : à essayer sur le Pixel pendant un vrai appel. P18 dépend d'un champ du protocole (#32)."),
    ("L4", "Système", "Échelle de texte, opacités, espacements, formes, et DESIGN.md à jour (table de migration).",
     "Visible partout : à livrer d'un bloc, après L1-L3, pour ne pas mélanger correction et restylage. Les captures du site et du canvas prod changent."),
]

def heures(effort):
    m = re.match(r"([\d.]+)\s*(h|min)", effort)
    v = float(m.group(1)); return v if m.group(2) == "h" else v / 60

def plan():
    c = ["<h1>Plan : 4 lots, dans l'ordre, environ " + f"{sum(heures(x['effort']) for x in P):.0f}" + " heures de travail</h1>",
         '<p class="lead">Les 24 recos regroupées par lot, du plus utile au moins cher d\'abord. Les efforts comptent le code, le passage au banc et la relecture à l\'écran ; ils ne comptent pas l\'attente des tests du Mac.</p>']
    for lot, nom, but, risques in LOTS:
        xs = sorted([x for x in P if x["lot"] == lot], key=lambda x: -x["score"])
        h = sum(heures(x["effort"]) for x in xs)
        c.append(f'<h2 id="{lot}">{lot}. {e(nom)} · {len(xs)} recos · {h:.1f} h</h2><p>{e(but)}</p>')
        c.append(tableau(["Ordre", "Problème", "Score", "Effort", "Fichiers touchés"], [[i + 1, f'<a href="problemes.html#{x["id"]}">{x["id"]}</a> {e(x["titre"])}', x["score"], x["effort"],
                 " ".join(sorted({f"<code>{e(s[0].split(':')[0].split(' ')[0].split(';')[0])}</code>" for s in x["spec"]}))] for i, x in enumerate(xs)], brut=True))
        c.append(f'<p class="note"><b>Risques.</b> {e(risques)}</p>')
    c.append("<h2>Ce qui touche à un choix déjà tranché</h2>")
    c.append(tableau(["Reco", "Choix", "Ce que la reco garde"], [[f'<a href="problemes.html#{x["id"]}">{x["id"]}</a>', e(x["tranche"]), e(x["choix"][:220])] for x in P if x["tranche"]], brut=True))
    c.append("<h2>Comment vérifier chaque lot</h2><ul>"
             "<li>Repasser le banc d'inventaire (<code>outils/DossierTest.kt</code> copié dans <code>src/test</code>, puis retiré) et <code>outils/mesures.py</code> : les critères d'acceptation sont écrits pour ses sorties (contrastes, cibles, accessibilité, police).</li>"
             "<li>Le banc de l'app (<code>gradlew testDebugUnitTest</code>) reste vert ; deux de ses tests échouent entre minuit et une heure (heure du conteneur), sans lien avec ces recos.</li>"
             "<li>Sur le Pixel : TalkBack (navigation par titres, annonces), police à 200 %, écran verrouillé pendant un enregistrement, un vrai appel WhatsApp avec la pastille.</li>"
             "<li>Écarts à reporter dans les issues : #32 (P18, initiales dans le protocole) ; #31 n'est touché par aucune reco.</li></ul>")
    page("plan.html", "Plan UX Android", "\n".join(c), "Les recos en 4 lots, ordre, effort, risques.")

def references():
    c = ["<h1>Références : les règles citées, vérifiées en ligne le 8 novembre 2026</h1>",
         '<p class="lead">Chaque reco cite une règle précise de cette liste. Les pages d\'Android et de WCAG ont été ouvertes pendant ce travail et les passages clés relus ; ceux qui fondent un choix sont cités ci-dessous. Material 3 (m3.material.io) se charge en JavaScript : ses pages sont citées par leur adresse, et l\'échelle typographique par la documentation de material-components-android.</p>']
    usage = collections.defaultdict(list)
    for x in P:
        for k in x["refs"]: usage[k].append(x["id"])
    CIT = {
        "a16": "« For apps targeting Android 16 (API level 36) or higher and running on an Android 16 or higher device, the predictive back system animations […] are enabled by default. Additionally, onBackPressed is not called and KeyEvent.KEYCODE_BACK is not dispatched anymore. »",
        "anotif": "« VISIBILITY_PUBLIC: the notification's full content shows on the lock screen. […] VISIBILITY_PRIVATE: only basic information, such as the notification's icon and the content title, shows on the lock screen. »",
        "alive": "« Must request promotion using EXTRA_REQUEST_PROMOTED_ONGOING or NotificationCompat.Builder#setRequestPromotedOngoing. Must be ongoing. Must have a contentTitle set. […] Must NOT setColorized to TRUE. »",
        "afont": "« Starting in Android 14, the system supports font scaling up to 200% […] the system applies a nonlinear scaling curve. »",
        "a48": "« we recommend that each interactive UI element have a focusable area, or touch target size, of at least 48dp×48dp. »",
        "m3type": "titleLarge 22 sp ; titleMedium 16 sp medium ; titleSmall 14 sp medium ; bodyLarge 16 ; bodyMedium 14 ; bodySmall 12 ; labelLarge 14 medium ; labelMedium 12 medium ; labelSmall 11 medium.",
        "m3snack": "« Snackbars provide brief messages about app processes at the bottom of the screen. […] can also offer the ability to perform an action, such as undoing an action. »",
        "adyn": "« Dynamic Color, which was added in Android 12, enables users to personalize their devices to align tonally with the color scheme of their personal wallpaper. »",
    }
    c.append(tableau(["Règle", "Citée par", "Passage"], [[f'<a href="{e(u)}">{e(t)}</a>', " ".join(f'<a href="problemes.html#{i}">{i}</a>' for i in usage.get(k, [])), e(CIT.get(k, ""))] for k, (t, u) in R.items()], brut=True))
    c.append("<h2>Conventions d'apps de référence</h2>")
    c.append("""<p>Ce travail s'est fait sans téléphone. Les conventions d'apps de Google ne sont citées que lorsqu'une documentation de Google les décrit (Live Updates : appels, minuteurs, trajets ; Snackbar : annulation ; retour prédictif : l'aperçu de l'écran d'en dessous). Les autres comparaisons (« l'Enregistreur de Google montre un chronomètre », « Google Photos réduit sa barre en icônes ») restent à vérifier sur un Pixel avant d'être opposées à un choix ; aucune reco ne repose sur elles seules.</p>""")
    c.append("<h2>Sources du dépôt</h2><ul><li>DESIGN.md (Téléphone, Écarts connus) ; TEXTES.md (principes 1 à 8, Vocabulaire, Par élément) ; SPEC-telephone.md (Votre voix pendant les appels ; Notifications).</li><li>Captures du Mac 0.24.0 : <code>design/recos/captures-mac-0.24.0/</code> (lecture.webp, enregistrement.webp, telephones.webp).</li><li>Code du Mac pour le vocabulaire : CallsWindow.swift:255, CallCard.swift:228, StatusPage.swift:123, Onboarding.swift:442, SettingsParts.swift:86-88.</li></ul>")
    page("references.html", "Références UX Android", "\n".join(c), "Règles WCAG, Android et Material 3 citées par le dossier, vérifiées.")

def index():
    inv = json_("inventaire-resume.json"); mes = json_("mesures-resume.json")
    top = sorted(P, key=lambda x: (-x["score"], -x["gravite"], x["id"]))[:10]
    CHIFFRE = {
        "P01": "4 états sur 34 sans un mot", "P02": "0 contrôle d'arrêt sur l'écran en direct", "P03": "11 emplois ; 2,10 à 2,98:1 en sombre", "P04": "15 états sur 34 rognés à 200 %",
        "P05": "1 phrase qui promet « tous les appels »", "P06": "0 durée ; visibilité privée sur 6 canaux", "P07": "0 vue différente entre Mac relié et injoignable", "P08": "3,88:1 sur 19 rendus ; piste 1,17:1",
        "P09": "85 éléments sans rôle ; 7 titres non déclarés", "P10": "4 pièces : 44, 26, 42,7 et 41,7 dp", "P13": "6 résultats sans date", "P23": "6 tailles, 7 rayons, 9 gris",
    }
    c = ["<h1>L'app Android de Callrecorder, relue en détail : 24 problèmes prouvés, les dix premiers corrigeables en une semaine</h1>",
         f"""<p class="lead">Relecture UX de l'app Android (branche <code>recos-design</code>, 7 novembre 2026), centrée sur les détails : ce qu'on comprend en trois secondes, si l'on sait que ça enregistre, la hiérarchie, les textes, les cibles, TalkBack, la police agrandie, le sombre, l'écran verrouillé. Tout ce qui est affirmé est mesuré par un banc qui rend chaque état de l'app, ou lu dans le code avec son fichier:ligne.</p>""",
         f"""<div class="grid">
<div class="chiffre"><b>{mes['etats_captures']}</b><span>écrans rendus : 34 états (+ boîtes, pastille) × clair/sombre × police 100/130/200 %</span></div>
<div class="chiffre"><b>{inv['textes']}</b><span>chaînes relevées, dont 148 visibles, avec fichier:ligne</span></div>
<div class="chiffre"><b>{inv['tailles'] + inv['couleurs'] + inv['opacites'] + inv['dp'] + inv['icones']}</b><span>valeurs de style relevées (tailles, couleurs, opacités, dp, icônes)</span></div>
<div class="chiffre"><b>{mes['couples_contraste'] + mes['contrastes_statiques']}</b><span>contrastes calculés (WCAG 2 et APCA)</span></div>
<div class="chiffre"><b>{mes['cibles_relevees']}</b><span>cibles tactiles mesurées</span></div>
<div class="chiffre"><b>{len(P)}</b><span>problèmes, chacun avec options, choix, spécification et critères</span></div>
</div>"""]
    c.append("<h2>Les dix problèmes qui comptent le plus</h2>")
    c.append(tableau(["", "Problème", "Mesure", "Gravité", "Effort"], [[i + 1, f'<a href="problemes.html#{x["id"]}">{x["id"]}</a> {e(x["titre"])}', e(CHIFFRE.get(x["id"], "")), GRAV[x["gravite"]], x["effort"]] for i, x in enumerate(top)], brut=True))
    c.append(f"""<p>Les dix ensemble : environ {sum(heures(x['effort']) for x in top):.0f} heures. Les 24 : environ {sum(heures(x['effort']) for x in P):.0f} heures, en quatre lots (<a href="plan.html">Plan</a>).</p>""")
    c.append("""<h2>Ce qui tient déjà</h2><p>La liste par jour et ses vignettes qui disent ce qu'était la conversation ; le pied à une main ; la confirmation de suppression qui dit la conséquence (« Elle reste sur MacBook Air ») ; les modes d'enregistrement qui disent ce qu'ils font ; la mise en route en une étape ; toutes les cibles à 48 dp ou plus sauf quatre ; un sombre complet hors l'accent ; le texte principal à 15,4:1. Les recos sont des retouches, pas une refonte.</p>""")
    c.append("<h2>Sommaire</h2><ol>" + "".join(f'<li><a href="{p}">{e(t)}</a> — {d}</li>' for p, t, d in [
        ("inventaire.html", "Inventaire", "34 états en images, 24 composants, 148 textes, vocabulaire Mac/Android, typographie, couleurs, opacités, espacements, rayons, icônes, notifications, autorisations"),
        ("mesures.html", "Mesures", "contrastes WCAG 2 et APCA en clair et en sombre, hors texte, cibles, sémantique TalkBack, police agrandie, mise en page, poids"),
        ("problemes.html", "Problèmes et recos", "24 fiches : symptôme, preuve, cause, impact, options, choix, règle, spécification, critères"),
        ("prototypes.html", "Prototypes", "11 écrans retouchés en HTML/CSS aux vraies valeurs, avant et après, clair et sombre"),
        ("systeme.html", "Système et migration", "8 rôles de texte, 20 couleurs nommées avec leurs contrastes, espacements, formes, composants, 66 changements fichier par fichier"),
        ("plan.html", "Plan", "4 lots dans l'ordre, effort, risques, choix déjà tranchés"),
        ("references.html", "Références", "WCAG 2.2, Android, Material 3, vérifiées")]) + "</ol>")
    c.append("""<h2>Méthode</h2><ul>
<li><b>Banc d'inventaire</b> (<a href="outils/DossierTest.kt">outils/DossierTest.kt</a>) : un test Robolectric qui ouvre les vrais écrans de l'app sur des conversations fictives, dans 34 états, en clair et en sombre, à 100, 130 et 200 %, et relève l'arbre des vues (taille, texte, couleur, fond composé, rôle, nom et état d'accessibilité). Copié dans <code>phone/android/app/src/test</code> le temps d'un passage, puis retiré : aucun fichier de l'app n'est modifié.</li>
<li><b>Relevé du code</b> (<a href="outils/inventaire_code.py">outils/inventaire_code.py</a>) : chaînes, tailles, couleurs, opacités, dp, icônes, avec fichier:ligne.</li>
<li><b>Mesures</b> (<a href="outils/mesures.py">outils/mesures.py</a>) : contrastes WCAG 2 et APCA-W3 0.0.98G, cibles, manques d'accessibilité, textes rognés.</li>
<li><b>Pages</b> : générées depuis ces données (<code>outils/page_*.py</code>) ; les fiches des problèmes sont dans <a href="outils/problemes.py">outils/problemes.py</a>.</li>
<li><b>Refaire</b> : depuis la racine du dépôt, copier <code>DossierTest.kt</code> dans <code>phone/android/app/src/test/java/fyi/gildas/callrecorder/</code>, lancer <code>phone/android/gradlew -p phone/android testDebugUnitTest --tests '*DossierTest'</code>, retirer le fichier, puis <code>python3 outils/inventaire_code.py</code>, <code>mesures.py</code>, <code>annote.py</code>, <code>page_*.py</code> (avec <code>PYTHONPATH=design/recos/ux-android/outils</code>).</li></ul>
<h2>Limites</h2><ul><li>Pas de téléphone : TalkBack, l'écran verrouillé et le rendu des notifications sont déduits du code et de la documentation d'Android, pas observés. Les boîtes d'Android sont rendues par Robolectric, pas par un Pixel.</li>
<li>Le banc ne dessine pas le bouton radio coché (état relevé, dessin absent).</li>
<li>Le premier livrable de cette relecture (<a href="../ux-android.html">ux-android.html</a>, 18 recos) reste en place ; ce dossier le remplace et le prouve.</li></ul>""")
    page("index.html", "UX Android, dossier", "\n".join(c), "Relecture UX détaillée de l'app Android de Callrecorder : synthèse, sommaire, méthode.")

if __name__ == "__main__":
    plan(); references(); index()

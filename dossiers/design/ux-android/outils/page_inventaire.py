"""Page « Inventaire » : tout ce que l'app montre et tout ce que le code emploie, avec fichier:ligne et comptes."""
import collections, glob, os, re
from commun import *

ETATS = [
    ("accueil", "liste", "Ouverture, Mac relié, six conversations sur cinq jours", "Jours en titres, vignette de 44 dp, titre, « heure · durée · personnes », pied à deux lignes"),
    ("accueil", "vide", "Première ouverture après la mise en route", "Barre du haut, puis rien jusqu'au pied"),
    ("accueil", "recherche-ouverte", "Toucher Rechercher", "Champ « Rechercher » à la place de la barre, liste vide, pied toujours là"),
    ("accueil", "recherche-resultats", "Taper « lundi »", "Une ligne par conversation : titre et réplique trouvée, sans jour"),
    ("accueil", "recherche-sans-resultat", "Taper « facture »", "Rien entre le champ et le pied"),
    ("accueil", "calendrier", "Toucher Calendrier", "Mois, lettres des jours, points, jour touché en gris, aujourd'hui en bleu, conversations du jour"),
    ("accueil", "calendrier-jour-vide", "Mois suivant", "Mois sans point, liste vide sous le mois"),
    ("accueil", "enregistrement", "Enregistrer une réunion", "Jour + ligne « Réunion · ● En cours » en rouge ; pied : Arrêter l'enregistrement (rouge), Prendre une photo"),
    ("accueil", "enregistrement-appel", "Appel pendant que le service des appels est allumé", "Ligne « Appel », sinon identique"),
    ("accueil", "ecoute", "Mode Tout le temps", "Ligne Journal en tête, « ● Écoute depuis » en bleu ; pied inchangé"),
    ("accueil", "en-attente-du-mac", "Un enregistrement fini, pas encore parti", "Ligne « Réunion · 5 min », rien ne dit qu'elle attend"),
    ("accueil", "lien-perdu", "Mac injoignable, un enregistrement en attente", "Identique à « en attente du Mac »"),
    ("conversation", "transcrite-avec-son", "Toucher une conversation récente", "En-tête (vignette 36 dp, titre, détail), lecteur, répliques, barre flottante à 4 outils"),
    ("conversation", "transcrite-sans-son", "Conversation dont le son léger est parti", "Sans lecteur"),
    ("conversation", "longue", "Huit répliques, trois voix", "Initiales en rond, nom, heure, texte"),
    ("conversation", "filtre", "Rechercher dans la conversation, « lundi »", "Champ gris, les seules répliques qui contiennent le mot"),
    ("conversation", "filtre-sans-resultat", "Rechercher « budget »", "Champ gris, rien dessous"),
    ("conversation", "pas-encore-arrivee", "Enregistrement fini, pas encore sur le Mac", "« Pas encore arrivée sur MacBook Air. », Copier et Télécharger grisés"),
    ("conversation", "pas-encore-transcrite", "Arrivée sur le Mac, pas de texte", "« Pas encore transcrite. »"),
    ("conversation", "aucune-parole", "Texte du Mac vide", "« Aucune parole reconnue »"),
    ("conversation", "en-direct", "Ouvrir la conversation qui s'enregistre (transcription du téléphone allumée)", "Heure, texte qui arrive ; ni lecteur, ni barre, ni ⋯"),
    ("conversation", "en-direct-rien", "Idem, avant la première phrase", "« Rien d'entendu pour l'instant. »"),
    ("journal", "sans-reponse-du-mac", "Toucher Journal, le Mac ne répond pas", "« Le Journal est sur MacBook Air. »"),
    ("journal", "pas-encore-transcrit", "Le Mac répond, rien de transcrit", "« Pas encore transcrit. »"),
    ("journal", "avec-texte", "Le Mac a envoyé le Journal", "Répliques, Rechercher et Copier"),
    ("reglages", "manuel", "Réglages, mode Manuel", "Trois modes avec leur phrase, Enregistrer les appels, Intégrations (Calendrier, Mac)"),
    ("reglages", "calendrier-sans-calendrier", "Mode Événements du calendrier, aucun calendrier", "Avertissement et Relier un calendrier sous le choix ; Calendrier « Non relié » en orange"),
    ("reglages", "calendrier-du-mac", "Calendrier relié au Mac", "Calendrier « MacBook Air »"),
    ("reglages", "tout-le-temps-appels-allumes", "Tout le temps, service des appels allumé", "Interrupteur allumé, teinte d'Android"),
    ("mise-en-route", "aucun-mac", "Première ouverture", "Icône, « Aucun Mac relié », chemin sur le Mac, Scanner le code du Mac"),
    ("mise-en-route", "sans-google-play", "Téléphone sans Google Play", "Phrase de repli, pas de bouton"),
    ("mise-en-route", "connexion", "Code lu, lien en cours", "« Connexion à MacBook Air… », sans bouton ni indicateur"),
    ("mise-en-route", "autre-wifi", "Mac injoignable depuis ce Wi-Fi", "« Connectez ce téléphone au même Wi-Fi que MacBook Air », « « Maison-5G » »"),
    ("pastille", "seule", "Hors de l'app, pendant un enregistrement", "Capsule, Prendre une photo (gris), Arrêter (rouge), 48 dp chacun"),
]

COMPOSANTS = [
    ("label()", "Screen.kt:37", "TextView, taille en sp, couleur, gras en sans-serif-medium, une ligne avec points", "partout (26 appels dans 5 écrans)"),
    ("icon()", "Screen.kt:45", "ImageView teintée, 24 dp par défaut, cachée à TalkBack", "pied, vignettes, outils"),
    ("iconButton()", "Screen.kt:59", "ImageButton 48×48 dp, icône 22 dp, toucher en rond (flat 24), nom pour TalkBack", "Retour, Rechercher, Fermer, Liste, Calendrier, Plus, mois"),
    ("kindPlate() / paintPlate()", "Screen.kt:95", "Vignette de type : masse 0,07, rayon taille/5,5, icône de marque", "en-tête d'une conversation (36 dp)"),
    ("bar()", "Screen.kt:107", "Barre d'écran : retour, vignette, titre et détail, action ; minimumHeight 64 mais posée en hauteur fixe dp(64) par les écrans", "Conversation, Journal, Réglages"),
    ("footRow()", "Screen.kt:123", "Ligne de pied : 48 dp de haut, icône 24 + texte 16 sp, toucher en masse rayon 12", "Accueil (4 variantes)"),
    ("chevronRow()", "Screen.kt:137", "Rangée nom / valeur / chevron 16 dp, 48 dp, valeur en 15 sp", "Réglages › Intégrations"),
    ("talkRow()", "HomeScreen.kt:260", "Ligne de conversation : 64 dp mini, vignette 44 dp (icône 20), titre 16 sp, méta 14 sp, une ligne chacun", "Accueil, recherche, calendrier"),
    ("dayCell()", "HomeScreen.kt:307", "Case du mois : 48 dp de haut, chiffre 15 sp, point 4 dp ; choisi = masse 0,12", "Calendrier"),
    ("switcher", "HomeScreen.kt:62", "Deux iconButton 52×48 dans une capsule (rayon 26), le choisi en masse 0,12", "Accueil"),
    ("field (recherche)", "HomeScreen.kt:69", "EditText sans fond, 16 sp, indice « Rechercher »", "Accueil"),
    ("playerCard", "ConversationScreen.kt:99", "Carte : Lire 44×44 (accent), SeekBar, temps 12 sp", "Conversation avec son"),
    ("find (filtre)", "ConversationScreen.kt:62", "EditText sur masse rayon 12, 16 sp", "Conversation"),
    ("toolbar + tool()", "ConversationScreen.kt:128 / 168", "Barre flottante (rayon 24, élévation 6) ; outil 76×56 mini, icône 22, mot 12 sp", "Conversation, Journal"),
    ("lineView() / fill()", "ConversationScreen.kt:319", "Réplique : rond 36 dp à initiales 13 sp gras, nom 15 sp gras, heure 13 sp (ink 0,5), texte 16 sp sélectionnable", "Conversation, Journal, en direct"),
    ("radios", "SettingsScreen.kt:27", "RadioButton à deux lignes (nom 16 sp, phrase 14 sp secondaire), teinte accent unique", "Réglages"),
    ("agendaMissing", "SettingsScreen.kt:51", "Avertissement 14 sp + bouton texte « Relier un calendrier » 48 dp", "Réglages"),
    ("calls", "SettingsScreen.kt:88", "Rangée à interrupteur non touchable ; toucher ouvre une boîte d'instructions", "Réglages"),
    ("scan", "SetupScreen.kt:18", "Bouton plein accent, capsule, 48 dp fixes, icône 18", "Mise en route"),
    ("Pastille", "Pastille.kt:23", "Fenêtre d'accessibilité, capsule (rayon 24, 0xF0 blanc), deux ImageView 48 dp", "Hors de l'app"),
    ("Point rouge", "CallService.kt:125", "Vue 12 dp, #D32F2F, en haut à droite, non touchable", "Pendant un appel, pastille absente"),
    ("AlertDialog (Android)", "ConversationScreen.kt:396, 412 ; SettingsScreen.kt:100, 180, 194 ; MainActivity.kt:202", "Boîtes du thème DeviceDefault", "Détails, Supprimer, appels, Calendrier, Mac, lecteur de code"),
    ("PopupMenu", "ConversationScreen.kt:400", "Menu ⋯ à une entrée", "Conversation"),
    ("Toast", "ConversationScreen.kt:372, 386 ; MainActivity.kt:182", "Retour bref", "Copier (< Android 13), Télécharger, lecteur de code"),
]

NOTIFS = [
    ("enregistre (« Enregistrement »)", "LOW", "1", "Enregistre / « Depuis 14:02 » ; Écoute", "Arrêter (icône pause du système) ; Enregistrer une réunion", "barre indéterminée si enregistre ; setWhen ; ongoing", "LinkService.kt:1020-1050"),
    ("pret (« Prêt »)", "MIN", "1", "Prêt (« Mode essai. » si essai)", "—", "ongoing, sans heure", "LinkService.kt:1024"),
    ("reunion (« Réunions »)", "HIGH", "2", "« « Titre » commence » ou « Une réunion commence sur MacBook Air » / « Touchez pour l'enregistrer. »", "toucher", "délai = fin de la réunion", "LinkService.kt:72-95, 493"),
    ("ecoute (« Écoute arrêtée »)", "DEFAULT, sans son", "2", "L'écoute est arrêtée / « Touchez pour la reprendre. »", "toucher", "", "LinkService.kt:72-95"),
    ("risque (« Réunions à risque »)", "DEFAULT", "4", "« « Titre » 14:00 risque de ne pas s'enregistrer » / cause", "Ouvrir le réglage (= toucher)", "une fois par réunion", "LinkService.kt:254-276"),
    ("arret (« Enregistrement arrêté »)", "DEFAULT", "3", "« Arrêté au bout d'une heure », « Arrêté : il reste moins de 500 Mo », « Le micro ne répond plus… »", "Reprendre (sauf 500 Mo)", "", "LinkService.kt:1006-1018 ; Recordings.kt:137, 314, 383, 396"),
]

AUTOS = [
    ("Micro", "RECORD_AUDIO", "Code du Mac scanné ; Enregistrer ; un mode automatique", "MainActivity.kt:255-260, 263, 152", "« Autoriser Callrecorder à enregistrer de l'audio ? »"),
    ("Notifications", "POST_NOTIFICATIONS", "Avec le micro (même boîte de suite)", "MainActivity.kt:256", "« Autoriser … à vous envoyer des notifications ? »"),
    ("Appareils à proximité", "BLUETOOTH_SCAN, BLUETOOTH_ADVERTISE", "Avec le micro, Android 12 et plus", "MainActivity.kt:257", "« … trouver les appareils à proximité, s'y connecter et déterminer leur position relative ? »"),
    ("Agenda", "READ_CALENDAR", "Relier un calendrier", "MainActivity.kt:275-278 ; SettingsScreen.kt:71, 179", "« … accéder à votre agenda ? »"),
    ("Photos", "READ_MEDIA_IMAGES", "Première photo", "MainActivity.kt:297-302", "« … accéder aux photos et vidéos ? »"),
    ("Service d'accessibilité", "BIND_ACCESSIBILITY_SERVICE", "Rangée Enregistrer les appels → boîte → Réglages d'Android", "SettingsScreen.kt:88-114", "Page Accessibilité d'Android, avertissement « contrôle total »"),
    ("Refus définitif", "—", "Après un refus « Ne plus demander »", "MainActivity.kt:289-292", "Ouverture directe des infos de l'app, sans message"),
]

VOCAB = [
    ("Enregistrer une réunion", "Enregistrer une réunion", "identique"),
    ("Réglages", "Réglages (› Paramètres)", "identique"),
    ("● En cours (liste)", "● En cours (liste) ; « Enregistrement en cours » (carte)", "identique en liste ; la conversation Android n'a pas la carte"),
    ("Aujourd'hui · …", "Aujourd'hui · … ; Hier · …", "« Hier » manque sur Android (Screen.kt:177 ; CallsWindow.swift:255)"),
    ("Pas encore transcrite.", "Pas encore transcrite (Réglages) ; « pas transcrite » dans la liste (CallCard.swift:228)", "point final en plus sur Android ; rien dans la liste Android"),
    ("Aucune parole reconnue", "Aucune parole reconnue", "identique, mais sans point quand ses voisins en ont un"),
    ("Rechercher dans la conversation", "Rechercher dans la transcription", "écart de mot"),
    ("Prendre une photo · Arrêter (pastille, icônes seules)", "Le temps, Capturer et Arrêter (pastille)", "fonctions voisines ; le Mac montre le temps, Android non (tranché le 2026-11-07)"),
    ("Moi (initiale « M »)", "Moi (initiales « GF »)", "écart"),
    ("CallRecorder (étiquette Android)", "Callrecorder dans les phrases (DESIGN.md, Marque)", "écart"),
    ("Manuel · Événements du calendrier · Tout le temps", "idem (SettingsParts.swift:86-88)", "identique"),
    ("Journal", "Journal (JournalPane.swift:229)", "identique"),
    ("Détails, Télécharger", "— (le Mac n'a ni l'un ni l'autre, il a Partager)", "propre au téléphone"),
]

def construire():
    inv = json_("inventaire-resume.json")
    textes = [t for t in lire("textes.csv") if t["visible"] == "oui"]
    tailles = lire("tailles-police.csv")
    couleurs = lire("couleurs.csv")
    opac = lire("opacites.csv")
    dps = lire("dp.csv")
    icones = lire("icones.csv")

    c = []
    c.append("<h1>Inventaire : 34 états, 24 composants, 148 textes, et chaque valeur du code avec son emplacement</h1>")
    c.append(f"""<p class="lead">Tout ce que l'app Android montre, relevé de deux façons : à l'écran, par le banc d'inventaire
(<code>outils/DossierTest.kt</code>, 34 états × clair et sombre × police 100, 130 et 200 %), et dans le code, par
<code>outils/inventaire_code.py</code> ({inv['fichiers']} fichiers, {inv['lignes_de_code']} lignes). Chaque valeur porte son fichier:ligne
et son nombre d'emplois. Les CSV complets sont dans <a href="donnees/">donnees/</a>.</p>""")
    c.append('<ul class="toc">' + "".join(f'<li><a href="#{a}">{t}</a></li>' for a, t in [
        ("etats", "1. Écrans et états"), ("composants", "2. Composants"), ("textes", "3. Textes visibles"), ("vocabulaire", "4. Vocabulaire, Mac et Android"),
        ("typo", "5. Typographie"), ("couleurs", "6. Couleurs"), ("opacites", "7. Opacités"), ("espacements", "8. Espacements et tailles"),
        ("rayons", "9. Rayons"), ("icones", "10. Icônes"), ("notifications", "11. Notifications"), ("autorisations", "12. Autorisations")]) + "</ul>")

    # 1. États
    c.append('<h2 id="etats">1. Écrans et états : 7 surfaces, 34 états</h2>')
    c.append("<p>Chaque état photographié en clair et en sombre à 100 %, et en clair à 200 % (la taille maximale d'Android 14 et plus). Les vignettes ouvrent l'image. Limite du banc : Robolectric ne dessine pas l'animation du bouton radio coché (l'état coché est bien relevé, <code>coche: true</code>), ni la vraie matière des boîtes de dialogue d'un Pixel.</p>")
    rangs = []
    for ecran, etat, comment, quoi in ETATS:
        imgs = []
        for conf, lg in (("clair-100", "clair"), ("sombre-100", "sombre"), ("clair-200", "200 %")):
            f = f"images/etats/{ecran}--{etat}--{conf}.webp"
            if os.path.exists(f"{DOSSIER}/{f}"):
                imgs.append(f'<a href="{f}"><img src="{f}" alt="{e(ecran)} {e(etat)} {lg}" width="77" height="171" loading="lazy" style="border-radius:5px;box-shadow:0 0 0 1px var(--line);margin-right:4px"></a>')
        rangs.append([f"<b>{e(ecran)}</b><br>{e(etat)}", e(comment), e(quoi), "".join(imgs)])
    c.append(tableau(["Écran / état", "Comment on y arrive", "Ce qu'on voit", "Clair · sombre · 200 %"], rangs, brut=True))
    c.append("<p>Hors banc, lus dans le code : les notifications (§ 11), les boîtes d'autorisation d'Android (§ 12), le point rouge des appels, la page Accessibilité d'Android. Les huit boîtes de dialogue de l'app sont relevées par le banc (<code>donnees/dialogues.json</code> ci-dessous, images dans <code>images/p21-dialogues.webp</code>).</p>")

    # 2. Composants
    c.append('<h2 id="composants">2. Composants : 24 pièces</h2>')
    c.append(tableau(["Pièce", "Où", "Ce qu'elle est (valeurs du code)", "Employée dans"], [[f"<code>{e(a)}</code>", f"<code>{e(b)}</code>", e(d), e(u)] for a, b, d, u in COMPOSANTS], brut=True))
    c.append('<p class="note">Écarts relevés : <code>bar()</code> prévoit <code>minimumHeight = 64</code> mais trois écrans la posent dans une hauteur fixe <code>dp(64)</code> (HomeScreen.kt:102, ConversationScreen.kt:145, SettingsScreen.kt:125) ; la barre flottante a un rayon 24 pour 64 dp de haut, ce n\'est pas la capsule que décrit DESIGN.md ; le bouton Lire (44 dp) et la vignette de liste (44 dp) sont les seules pièces sous 48.</p>')

    # 3. Textes
    c.append(f'<h2 id="textes">3. Textes visibles : {len(textes)} chaînes</h2>')
    c.append(f"<p>Relevé automatique des chaînes du code ({inv['textes']} en tout), trié en visibles et techniques (journal, formats, autorisations) ; la règle de tri est dans <code>outils/inventaire_code.py</code>. À l'écran, le banc a rendu 156 textes distincts (<code>donnees/textes-rendus.csv</code>).</p>")
    par_ctx = collections.Counter(t["contexte"] for t in textes)
    c.append(tableau(["Contexte", "Nombre"], [[k, v] for k, v in par_ctx.most_common()]))
    doublons = collections.defaultdict(list)
    for t in textes: doublons[t["texte"]].append(f"{t['fichier'].split('/')[-1]}:{t['ligne']}")
    dbl = [(k, v) for k, v in doublons.items() if len(set(v)) > 1]
    c.append(f"<h3>Chaînes écrites à plusieurs endroits ({len(dbl)})</h3>")
    c.append(tableau(["Texte", "Où"], [[e(k), " ".join(f"<code>{e(x)}</code>" for x in sorted(set(v)))] for k, v in sorted(dbl)], brut=True))
    c.append("<details><summary>Les " + str(len(textes)) + " textes, avec fichier:ligne</summary>" + tableau(["Fichier:ligne", "Contexte", "Texte"],
             [[code_lien(t["fichier"], t["ligne"]), e(t["contexte"]), e(t["texte"])] for t in textes], brut=True) + "</details>")

    # 4. Vocabulaire
    c.append('<h2 id="vocabulaire">4. Vocabulaire, Mac et Android</h2>')
    c.append(tableau(["Android", "Mac 0.24", "Écart"], VOCAB))

    # 5. Typographie
    c.append('<h2 id="typo">5. Typographie : 6 tailles, 2 graisses</h2>')
    rendus = lire("textes-rendus.csv")
    t_code = collections.Counter((float(t["sp"]), "gras" in t["forme"]) for t in tailles)
    t_rendu = collections.Counter((float(r["taille_sp"]), int(r["graisse"]) >= 500) for r in rendus)
    M3 = {(12, False): "bodySmall", (12, True): "labelMedium", (14, False): "bodyMedium", (14, True): "titleSmall / labelLarge", (16, False): "bodyLarge", (16, True): "titleMedium", (22, False): "titleLarge"}
    rangs = []
    for (sp, gras) in sorted(set(t_code) | set(t_rendu)):
        ou = [f"{t['fichier'].split('/')[-1]}:{t['ligne']}" for t in tailles if float(t["sp"]) == sp and ("gras" in t["forme"]) == gras]
        rangs.append([f"{sp:g} sp", "medium (500)" if gras else "regular (400)", t_code.get((sp, gras), 0), t_rendu.get((sp, gras), 0),
                      M3.get((int(sp), gras), "<span class=ko>hors échelle M3</span>") if sp == int(sp) else "<span class=ko>hors échelle M3</span>",
                      " ".join(f"<code>{e(x)}</code>" for x in ou)])
    c.append(tableau(["Taille", "Graisse", "Dans le code", "Textes rendus (34 états, clair, 100 %)", "Rôle Material 3 le plus proche", "Où"], rangs, brut=True))
    c.append('<p class="note">13, 15 et 17 sp n\'existent pas dans l\'échelle de Material 3 (12, 14, 16, 22…). Six tailles à 1 sp d\'écart se distinguent mal entre elles : 13 et 14, 15 et 16, 16 et 17 sont côte à côte dans la même vue (en-tête 17/13, ligne 16/14, réplique 15/16/13). Le gras est <code>sans-serif-medium</code> (Screen.kt:35), la graisse 500 de Roboto : juste.</p>')

    # 6. Couleurs
    c.append('<h2 id="couleurs">6. Couleurs : 92 emplois</h2>')
    cc = collections.Counter(x["valeur"] for x in couleurs)
    def pastille(v):
        m = re.fullmatch(r"#([0-9A-F]{2})([0-9A-F]{6})", v)
        return f'<span class="sw" style="background:#{m.group(2)};opacity:{int(m.group(1),16)/255:.2f}"></span>' if m else ""
    rangs = [[pastille(v) + f"<code>{e(v)}</code>", n, " ".join(f"<code>{e(x['fichier'].split('/')[-1])}:{x['ligne']}</code>" for x in couleurs if x["valeur"] == v)] for v, n in cc.most_common()]
    c.append(tableau(["Valeur", "Emplois", "Où"], rangs, brut=True))
    c.append("""<h3>Doublons, quasi-doublons et écarts</h3><ul>
<li><b>L'accent a deux sources</b> : <code>LinkService.ACCENT</code> (#0064D2, 11 emplois directs) et <code>Look.Tone.INFO</code>, qui seul prévoit le sombre (#409CFF, Look.kt:50, 1 emploi). Les 11 emplois directs restent #0064D2 en sombre : voir <a href="mesures.html#sombre">Mesures</a>.</li>
<li><b>Deux rouges d'enregistrement</b> : <code>Tone.LIVE</code> (#C41E14 / #FF453A) et le point des appels en dur <code>#D32F2F</code> (CallService.kt:129).</li>
<li><b>Les couleurs de marque</b> (WhatsApp, Signal, Telegram, Meet, Screen.kt:87-90) n'ont qu'une valeur pour les deux thèmes.</li>
<li><b>Les boîtes et l'interrupteur</b> prennent la couleur du thème d'Android (#475D92 relevé par le banc, la couleur dynamique sur un Pixel), pas l'accent de l'app.</li>
<li><b>Le fond des teintes</b> s'écrit <code>or 0x1F000000</code> (12,2 %, HomeScreen.kt:253, ConversationScreen.kt:355) quand le reste dit 0,12 : quasi-doublon.</li></ul>""")

    # 7. Opacités
    c.append('<h2 id="opacites">7. Opacités : 9 valeurs pour 5 rôles</h2>')
    oc = collections.Counter(float(x["opacite"]) for x in opac)
    rangs = [[f"{v:g}", n, " ".join(f"<code>{e(x['fichier'].split('/')[-1])}:{x['ligne']}</code> {e(x['forme'])}" for x in opac if float(x["opacite"]) == v)] for v, n in sorted(oc.items())]
    rangs += [["0,6 / 0,62", "via look.secondary (22)", "<code>Look.kt:23</code> secondaire"], ["0,56 / 0,62", "via look.title (3)", "<code>Look.kt:24</code> titre de groupe"]]
    c.append(tableau(["Opacité", "Emplois", "Où"], rangs, brut=True))
    c.append('<p class="note">Entre 0,40 et 0,62, six gris pour du texte ou des icônes secondaires (0,40 chevron ; 0,45 point du jour et neutre ; 0,50 heure des répliques ; 0,55 vignette ; 0,56 titre ; 0,60 secondaire). Le contraste les départage : 0,50 sur fond clair donne 3,9:1, sous le seuil de 4,5 (voir Mesures).</p>')

    # 8. Espacements
    c.append('<h2 id="espacements">8. Espacements et tailles : 199 valeurs en dp</h2>')
    ECHELLE = {2, 4, 8, 12, 16, 24, 32}
    roles = collections.defaultdict(collections.Counter)
    for x in dps: roles[x["role"]][float(x["dp"])] += 1
    rangs = []
    for r, cnt in sorted(roles.items()):
        vals = " ".join(f'<span class="{"ko" if r in ("marge interne", "marge externe") and v not in ECHELLE else ""}">{v:g}</span>×{n}' for v, n in sorted(cnt.items()))
        rangs.append([e(r), sum(cnt.values()), vals])
    c.append(tableau(["Rôle", "Emplois", "Valeurs (dp) × nombre ; en rouge, hors de l'échelle proposée 2·4·8·12·16·24·32"], rangs, brut=True))
    hors = [x for x in dps if x["role"] in ("marge interne", "marge externe") and float(x["dp"]) not in ECHELLE]
    c.append(f"<details><summary>Les {len(hors)} marges hors échelle, avec fichier:ligne</summary>" + tableau(["Où", "dp", "Code"], [[code_lien(x["fichier"], x["ligne"]), x["dp"], f"<code>{e(x['code'])}</code>"] for x in hors], brut=True) + "</details>")

    # 9. Rayons
    c.append('<h2 id="rayons">9. Rayons : 7 valeurs pour 3 formes</h2>')
    rr = [x for x in dps if x["role"] == "rayon"]
    rangs = []
    FORME = {"8": "ligne, vignette (DESIGN : 8)", "12": "carte (DESIGN : 12)", "18": "rond 36 dp (initiales)", "20": "outil 76×56 : ni rond ni capsule", "22": "rond 44 dp (Lire)", "24": "capsule 48 dp, rond 48 dp ; barre flottante 64 dp : <b>pas une capsule</b>", "26": "capsule 52 dp (Liste/Calendrier)"}
    for v, n in sorted(collections.Counter(x["dp"] for x in rr).items(), key=lambda a: float(a[0])):
        k = str(int(float(v)))
        rangs.append([f"{float(v):g}", n, FORME.get(k, ""), " ".join(f"<code>{e(x['fichier'].split('/')[-1])}:{x['ligne']}</code>" for x in rr if x["dp"] == v)])
    c.append(tableau(["Rayon (dp)", "Emplois", "Forme obtenue", "Où"], rangs, brut=True))

    # 10. Icônes
    c.append(f'<h2 id="icones">10. Icônes : {len(icones)} dessins</h2>')
    c.append(tableau(["Icône", "Emplois", "Où"], [[f"<code>{e(i['icone'])}</code>", i["usages"], " ".join(f"<code>{e(x.split('/')[-1])}</code>" for x in i["ou"].split())] for i in icones], brut=True))
    c.append('<p class="note">Tailles : 16 (chevron), 18 (mois, scanner), 20 (vignettes), 22 (boutons, outils), 24 (pied). <code>ic_retour</code> sert aussi de « mois précédent » quand « mois suivant » prend <code>chevron</code> : deux dessins pour un couple. L\'action Arrêter de la notification prend <code>android.R.drawable.ic_media_pause</code>, une pause.</p>')

    # 11. Notifications
    c.append('<h2 id="notifications">11. Notifications : 6 canaux, 4 identifiants</h2>')
    c.append(tableau(["Canal (nom montré dans Android)", "Importance", "Id", "Titre / texte", "Actions", "Particularités", "Où"], NOTIFS))
    c.append('<p class="note">Aucune ne règle <code>setVisibility</code> : toutes sont <code>VISIBILITY_PRIVATE</code> (Android ne montre que l\'icône et le titre sur l\'écran verrouillé masquant le contenu). Aucune n\'a de <code>category</code> (CATEGORY_SERVICE, CATEGORY_REMINDER).</p>')

    # 12. Autorisations
    c.append('<h2 id="autorisations">12. Autorisations : 7 moments</h2>')
    c.append(tableau(["Quoi", "Permission", "Quand l'app la demande", "Où", "Ce qu'Android affiche (formulation approchée, à relire sur le Pixel)"], AUTOS))
    dlg = json_("../../../../phone/android/app/build/dossier/dialogues--clair-100.json") if os.path.exists("phone/android/app/build/dossier/dialogues--clair-100.json") else []
    if dlg:
        import json as _j
        _j.dump(dlg, open(f"{DONNEES}/dialogues.json", "w"), ensure_ascii=False, indent=1)
    dlg = json_("dialogues.json")
    c.append("<h3>Boîtes de dialogue de l'app (relevées par le banc)</h3>")
    c.append(tableau(["Boîte", "Titre", "Message", "Boutons"], [[d["nom"], d.get("titre", ""), d.get("message", "") or " · ".join(d.get("entrees", [])), " · ".join(x for x in (d.get("negatif"), d.get("neutre"), d.get("positif")) if x)] for d in dlg]))

    page("inventaire.html", "Inventaire UX Android", "\n".join(c), "Chaque écran, état, composant et valeur de l'app Android, avec fichier:ligne.")

if __name__ == "__main__":
    css(); construire()

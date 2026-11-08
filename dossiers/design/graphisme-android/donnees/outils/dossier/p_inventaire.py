from commun import *
import collections, math, re

ETATS = [
    # (écran, état, image, comment, variantes)
    ('Accueil', 'Liste par jour', 'accueil', 'Des conversations reçues du Mac', 'clair, sombre, 360, 600, 200 %'),
    ('Accueil', 'Vide', 'accueil-vide', 'Aucune conversation', 'clair, sombre, 360, 600, 200 %'),
    ('Accueil', 'En écoute (Journal en tête)', 'accueil-ecoute', 'Mode « Tout le temps »', 'clair, sombre, 360, 600, 200 %'),
    ('Accueil', 'Enregistrement en cours', 'accueil-enregistre', 'Une réunion enregistre', 'clair, sombre, 360, 600, 200 %'),
    ('Accueil', 'Calendrier', 'calendrier', 'Bouton Calendrier', 'clair, sombre, 360, 600, 200 %'),
    ('Accueil', 'Recherche', 'recherche', 'Rechercher, « lundi »', 'clair, sombre, 360, 600, 200 %'),
    ('Accueil', 'Icônes des sortes de conversation', 'icones', 'WhatsApp, Signal, Telegram, Meet, mobile, réunion', 'clair, sombre, 360, 600, 200 %'),
    ('Accueil', 'Recherche : vignettes', 'icones-recherche', 'Résultats avec leur icône', 'clair, sombre, 360, 600, 200 %'),
    ('Conversation', 'Lue, avec le son léger', 'conversation', 'Ouverte depuis la liste', 'clair, sombre, 360, 600, 200 %'),
    ('Conversation', 'Recherche ouverte', 'conversation-recherche', 'Barre du bas › Rechercher', 'clair, sombre, 360, 600, 200 %'),
    ('Conversation', 'Réunion à plusieurs voix', 'site-reunion', 'Voix 1, Voix 2, Moi', 'clair, sombre, 360, 600, 200 %'),
    ('Conversation', 'En direct, rien d\'entendu', 'direct-rien', 'Pendant l\'enregistrement', 'clair, sombre, 360, 600, 200 %'),
    ('Conversation', 'En direct, texte du téléphone', 'conversation-en-direct', 'Transcription Google sur le téléphone', 'clair, sombre'),
    ('Conversation', 'Pas encore arrivée sur le Mac', 'avant-transcription', 'Enregistrée, pas envoyée', 'clair, sombre, 360, 600, 200 %'),
    ('Conversation', 'Pas encore transcrite', 'pas-encore-transcrite', 'Sur le Mac, sans texte', 'clair, sombre, 360, 600, 200 %'),
    ('Conversation', 'Aucune parole reconnue', 'aucune-parole', 'Transcrite, vide', 'clair, sombre, 360, 600, 200 %'),
    ('Conversation', 'En-tête : icône d\'app', 'icones-entete', 'Signal', 'clair, sombre, 360, 600, 200 %'),
    ('Conversation', 'En-tête sans texte du Mac', 'icones-entete-sans-texte', 'Telegram', 'clair, sombre, 360, 600, 200 %'),
    ('Journal', 'Sur le Mac (vide)', 'journal-vide', 'Ligne Journal', 'clair, sombre, 360, 600, 200 %'),
    ('Réglages', 'Événements du calendrier, aucun calendrier', 'reglages', 'Pied › Réglages', 'clair, sombre, 360, 600, 200 %'),
    ('Mise en route', 'Aucun Mac relié', 'mise-en-route', 'Premier lancement', 'clair, sombre, 360, 600, 200 %'),
    ('Site', 'Accueil du site (Pixel 7)', 'site-accueil', 'Image du site', 'clair, sombre, 360, 600, 200 %'),
    ('Site', 'Notes vocales du site', 'site-notes', 'Image du site', 'clair, sombre, 360, 600, 200 %'),
    ('Pastille', 'Pendant un enregistrement', 'pastille', 'Hors de l\'app', 'clair'),
]

HORS_BANC = [
    ('Mise en route', 'Connexion à « Mac »…', 'SetupScreen.kt', 59, 'Titre seul, sans bouton'),
    ('Mise en route', 'Même Wi-Fi que le Mac', 'SetupScreen.kt', 60, 'Titre + nom du Wi-Fi entre guillemets'),
    ('Mise en route', 'Problème du lien', 'SetupScreen.kt', 61, 'Titre + texte de Link.problem'),
    ('Mise en route', 'Lecteur de code absent', 'SetupScreen.kt', 64, 'Texte + Lecteur.CAMERA, sans bouton'),
    ('Boîte', 'Enregistrer les appels (accessibilité)', 'SettingsScreen.kt', 101, 'Texte numéroté, 2 boutons'),
    ('Boîte', 'Calendrier relié', 'SettingsScreen.kt', 180, 'Titre + une phrase, OK'),
    ('Boîte', 'Mac (état du lien)', 'SettingsScreen.kt', 196, 'Titre = nom du Mac, OK, Scanner un code'),
    ('Boîte', 'Détails d\'une conversation', 'ConversationScreen.kt', 396, 'Lignes séparées par \\n, OK'),
    ('Boîte', 'Supprimer la conversation ?', 'ConversationScreen.kt', 413, 'Supprimer en LIVE, Annuler'),
    ('Boîte', 'Lecteur de code indisponible', 'MainActivity.kt', 202, 'OK'),
    ('Menu', '⋯ › Supprimer', 'ConversationScreen.kt', 401, 'PopupMenu d\'Android'),
    ('Toast', '« Copié » (avant Android 13)', 'ConversationScreen.kt', 372, ''),
    ('Toast', '« Dans Téléchargements › CallRecorder »', 'ConversationScreen.kt', 386, ''),
    ('Notification', 'Prêt (IMPORTANCE_MIN)', 'LinkService.kt', 980, 'Toujours là ; sans action'),
    ('Notification', 'Écoute', 'LinkService.kt', 981, 'Action « Enregistrer une réunion »'),
    ('Notification', 'Enregistre · Depuis HH:MM', 'LinkService.kt', 982, 'Barre indéterminée, action « Arrêter » (icône pause)'),
    ('Notification', '« Réunion » commence / L\'écoute est arrêtée', 'LinkService.kt', 87, 'IMPORTANCE_HIGH ou DEFAULT'),
    ('Notification', 'Réunion à risque', 'LinkService.kt', 270, 'Action « Ouvrir le réglage »'),
    ('Notification', 'Enregistrement arrêté', 'LinkService.kt', 1011, 'Action « Reprendre »'),
    ('Fenêtre', 'Point rouge des appels', 'CallService.kt', 129, '12 dp, #D32F2F, en haut à droite'),
    ('Icône', 'Icône adaptative', 'res/mipmap-anydpi-v26/ic_launcher.xml', 1, 'Fond blanc, micro 150/432 px'),
    ('Icône', 'Petite icône des notifications', 'res/drawable/micro_notif.xml', 1, 'Silhouette du micro'),
]

COMPOSANTS = [
    ('label()', 'Screen.kt', 37, 'Tout texte de l\'app', 'taille 16 par défaut, couleur look.text, medium si bold, une ligne + « … » si oneLine'),
    ('icon()', 'Screen.kt', 45, 'Icône décorative', '24 dp par défaut, teinte passée, cachée à l\'accessibilité'),
    ('iconButton()', 'Screen.kt', 59, 'Icône qu\'on touche', '48 × 48 dp, icône 22 dp, fond flat(24), contentDescription'),
    ('pressable()', 'Screen.kt', 53, 'Masse qui répond', 'Ripple ink 0,12 sur une masse'),
    ('flat()', 'Screen.kt', 56, 'Sans fond au repos', 'Ripple ink 0,12, masque de rayon 12 par défaut'),
    ('kindIcon() / kindTint()', 'Screen.kt', 76, 'Ce qu\'était la conversation', '7 icônes ; 4 couleurs de marque, ink 0,55 sinon'),
    ('kindPlate()', 'Screen.kt', 95, 'Vignette 36 dp (en-tête)', 'masse 0,07, rayon size/5,5 (6,5 dp), icône 18'),
    ('talkRow()', 'HomeScreen.kt', 260, 'Ligne de conversation', '≥ 64 dp, padding 8, vignette 44 (rayon 8, icône 20), titre 16, méta 14'),
    ('Row.Day', 'HomeScreen.kt', 240, 'Titre de jour', '14 sp medium, title (0,56), padding 12/12/12/6'),
    ('switcher', 'HomeScreen.kt', 63, 'Liste / Calendrier', 'capsule rayon 26, 2 boutons 52 × 48, choisi masse 0,12'),
    ('field (accueil)', 'HomeScreen.kt', 69, 'Recherche de l\'accueil', 'EditText 16 sp, sans fond, 42,7 dp de haut'),
    ('dayCell()', 'HomeScreen.kt', 307, 'Jour du calendrier', '48 dp de haut, 1/7 de la largeur ; choisi 0,12 ; aujourd\'hui ACCENT gras ; point 4 dp'),
    ('footRow()', 'Screen.kt', 123, 'Ligne du pied', '≥ 48 dp, padding 8/12, icône 24, texte 16'),
    ('bar()', 'Screen.kt', 107, 'Barre d\'un écran', '64 dp fixes ; Retour 48 ; vignette 36 ; titre 17 ; détail 13'),
    ('chevronRow()', 'Screen.kt', 137, 'Ligne des Réglages', '≥ 48 dp, padding 12/8, nom 16, valeur 15, chevron 16 dp'),
    ('playerCard', 'ConversationScreen.kt', 99, 'Lecteur du son léger', 'carte rayon 12, padding 12/10 ; Lire 44 dp ACCENT ; SeekBar 26 dp ; temps 12 sp'),
    ('find (conversation)', 'ConversationScreen.kt', 62, 'Rechercher dans la conversation', 'EditText 16 sp, masse rayon 12, padding 14/10, 41,7 dp de haut'),
    ('lineView() / fill()', 'ConversationScreen.kt', 319, 'Réplique', 'rond 36 (13 sp medium), nom 15 medium, heure 13 à 0,5, texte 16 × 1,15'),
    ('toolbar / tool()', 'ConversationScreen.kt', 128, 'Barre flottante du bas', 'capsule rayon 24, elevation 6, outils ≥ 76 × 56, icône 22, mot 12 sp'),
    ('RadioButton des modes', 'SettingsScreen.kt', 27, 'Mode d\'enregistrement', '16 sp + explication × 0,875 secondaire, padding 10/12/12/12'),
    ('agendaMissing', 'SettingsScreen.kt', 51, 'Manque de calendrier', 'texte 14 WARNING + bouton texte ACCENT 14 medium'),
    ('calls (interrupteur)', 'SettingsScreen.kt', 88, 'Enregistrer les appels', 'carte 12, padding 12/8, Switch du système'),
    ('heading()', 'SettingsScreen.kt', 121, 'Titre de groupe', '14 sp medium, title, padding 4'),
    ('scan (bouton plein)', 'SetupScreen.kt', 18, 'Scanner le code du Mac', 'capsule ACCENT, texte blanc 16 medium, icône 18'),
    ('Pastille', 'Pastille.kt', 36, 'Pendant l\'enregistrement', 'capsule rayon 24, floating, elevation 4, 2 × 48 dp'),
    ('Point rouge', 'CallService.kt', 125, 'Pendant un appel', '12 dp, #D32F2F, x 12, y 36 dp'),
    ('AlertDialog / PopupMenu / Toast / Switch', '—', None, 'Composants du système', 'Theme.DeviceDefault.DayNight (AndroidManifest.xml:30)'),
]

def lab_of(h):
    r, g, b, _ = parse(h)
    def lin(v):
        v /= 255
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    R, G, B = lin(r), lin(g), lin(b)
    X = (0.4124 * R + 0.3576 * G + 0.1805 * B) / 0.95047
    Y = (0.2126 * R + 0.7152 * G + 0.0722 * B)
    Z = (0.0193 * R + 0.1192 * G + 0.9505 * B) / 1.08883
    f = lambda t: t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
    return (116 * f(Y) - 16, 500 * (f(X) - f(Y)), 200 * (f(Y) - f(Z)))

def de(a, b):
    A, B = lab_of(a), lab_of(b)
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(A, B)))

def build():
    b = ['<h1>Inventaire</h1><p class="lede">Tout ce que l\'app dessine, tiré du code et du relevé de l\'arbre des vues : écrans et états, composants, puis chaque valeur (taille, graisse, couleur, opacité, espacement, rayon, icône, texte), avec où elle sert et combien de fois. Les tableaux complets sont dans <a href="donnees/">donnees/</a>.</p>']
    # --- écrans et états
    b.append('<h2 id="etats">1. Écrans et états</h2><p>Le banc (Robolectric, API 35, 412 × 915 dp, xxhdpi) ouvre chaque état ; une copie du banc, hors du dépôt, l\'a rejoué en <b>6 variantes</b> : clair, sombre, 360 dp de large, 600 dp, et texte à 200 % (échelle non linéaire d\'Android 14). Le relevé de chaque écran (place, taille et couleur de chaque vue, ce qu\'elle dit à l\'accessibilité) est dans <code>donnees/</code> par les CSV <code>mesures-*</code>. Cliquer une vignette ouvre l\'image.</p>')
    tr = []
    for e, s, img, how, var in ETATS:
        th = f'<a href="images/etats/clair-{img}.webp">clair</a>' + (f' · <a href="images/etats/sombre-{img}.webp">sombre</a>' if img != 'pastille' else '')
        if img in ('accueil', 'conversation-recherche', 'reglages', 'calendrier', 'mise-en-route', 'site-reunion'):
            th += f' · <a href="images/etats/texte200-{img}.webp">200 %</a> · <a href="images/etats/etroit-{img}.webp">360 dp</a>'
        tr.append([esc(e), esc(s), esc(how), esc(var), th])
    b.append(table(['Écran', 'État', 'Comment', 'Variantes relevées', 'Images'], tr))
    b.append('<div class="grid3">' + ''.join(f'<figure><a href="images/etats/clair-{i}.webp"><img loading="lazy" src="images/etats/clair-{i}.webp" alt="{esc(s)}"></a><figcaption>{esc(e)} · {esc(s)}</figcaption></figure>'
                                         for e, s, i, *_ in ETATS if i in ('accueil', 'accueil-enregistre', 'calendrier', 'site-reunion', 'conversation-en-direct', 'reglages')) + '</div>')
    b.append('<h3>Hors du banc : lus dans le code</h3>')
    b.append(table(['Où', 'État', 'Source', 'Forme'], [[esc(a), esc(s), src(f, l) if not f.startswith('res') else src('phone/android/app/src/main/' + f), esc(n)] for a, s, f, l, n in HORS_BANC]))
    b.append(f'<p><b>{len(ETATS)}</b> états au banc, <b>{len(HORS_BANC)}</b> lus dans le code : <b>{len(ETATS) + len(HORS_BANC)}</b> états en tout.</p>')
    # --- composants
    b.append('<h2 id="composants">2. Composants</h2><p>L\'app n\'utilise ni Compose ni Material Components : des vues Android dessinées à la main (<code>LinearLayout</code>, <code>TextView</code>, <code>GradientDrawable</code>, <code>RippleDrawable</code>) sur le thème <code>Theme.DeviceDefault.DayNight</code>. Les pièces communes sont dans <code>Screen.kt</code>, les valeurs dans <code>Look.kt</code>.</p>')
    b.append(table(['Composant', 'Source', 'Rôle', 'Valeurs'], [[f'<code>{esc(n)}</code>', src(f, l) if l else esc(f), esc(r), esc(v)] for n, f, l, r, v in COMPOSANTS]))
    # --- valeurs
    b.append('<h2 id="valeurs">3. Valeurs</h2>')
    def agg(name, title, intro, key=lambda r: r['valeur'], extra=None):
        rs = rows(name)
        groups = collections.OrderedDict()
        for r in sorted(rs, key=lambda r: (key(r), r['fichier'], int(r['ligne']))):
            groups.setdefault(key(r), []).append(r)
        data = []
        for k, g in sorted(groups.items(), key=lambda kv: -len(kv[1])):
            locs = ', '.join(src(r['fichier'], r['ligne']) for r in g[:12]) + (f' … <span class="small">+{len(g) - 12}</span>' if len(g) > 12 else '')
            roles = '; '.join(sorted(set(r['role'] for r in g if r['role'])))[:160]
            data.append([f'<code>{esc(k)}</code>' + (extra(k) if extra else ''), str(len(g)), esc(roles), locs])
        b.append(f'<h3>{title}</h3>{intro}')
        b.append(table(['Valeur', 'Fois', 'Rôles', 'Où (fichier:ligne)'], data, num=(1,)))
        return groups
    sizes = agg('inventaire-texte_tailles', '3.1 Tailles de texte (sp)', '<p>31 réglages de taille, <b>6 tailles</b> différentes (12, 13, 14, 15, 16, 17) plus une taille relative (× 0,875, soit 14 sp sur 16). L\'échelle de Material 3 en a 4 dans cette plage (12, 14, 16, 22 ; <a href="https://github.com/material-components/material-components-android/blob/master/docs/theming/Typography.md">Typography.md</a>). Quasi-doublons : 13 et 12 (heures, détail, temps du lecteur), 15 et 16 (nom de réplique, valeur des Réglages, états vides), 17 et 16 (titre de barre).</p>')
    agg('inventaire-graisses', '3.2 Graisses', '<p>Deux graisses : regular (400) partout, medium (500, <code>sans-serif-medium</code>) pour 10 rôles, et un <b>gras (700)</b> isolé pour le chiffre d\'aujourd\'hui dans le calendrier (<code>Typeface.BOLD</code>, HomeScreen.kt:316) : le seul 700 de l\'app.</p>')
    agg('inventaire-interlignes', '3.3 Interlignes', '<p>Interlignage par défaut de Roboto (environ 1,17) partout, sauf les répliques et la mise en route (× 1,15 en plus) et les modes des Réglages (+ 2 dp). Aucune hauteur de ligne fixe : à 200 %, les lignes grandissent mais les conteneurs de hauteur fixe (barre de 64 dp, ronds de 36 dp) non.</p>')
    # couleurs, avec ΔE entre couleurs proches
    cols = rows('inventaire-couleurs')
    allc = sorted(set(r['valeur'] for r in cols if r['valeur'].startswith('#') and r['role'] != 'masque binaire' and r['valeur'][1:3] not in ('00', '1F')))
    near = []
    for i, x in enumerate(allc):
        for y in allc[i + 1:]:
            if x[3:] == y[3:]: continue
            d = de(x, y)
            if d < 12: near.append((d, x, y))
    agg('inventaire-couleurs', '3.4 Couleurs littérales', '<p>24 couleurs écrites en dur, dont 17 opaques : le texte et le fond (clair, sombre), 4 couleurs d\'état × 2 modes, 4 couleurs de marque, l\'accent, le verre, et un rouge isolé (<code>#D32F2F</code>, le point des appels). <code>LinkService.ACCENT</code> sert <b>14 fois</b> hors de sa définition, dont 7 pour du texte ou un trait qui reste <code>#0064D2</code> en sombre.</p>',
        extra=lambda k: sw('#' + k[3:] if k.startswith('#') and len(k) == 9 else '#000') if k.startswith('#') else '')
    b.append('<h4>Couleurs proches (ΔE76 &lt; 12)</h4>' + table(['Couleur A', 'Couleur B', 'ΔE', 'Lecture'],
        [[sw('#' + x[3:]) + x, sw('#' + y[3:]) + y, fr(d, 1), {'#FFC41E14|#FFD32F2F': 'Deux rouges d\'enregistrement : LIVE et le point des appels', '#FF1D1D1F|#FF1E1E1E': 'Texte clair et fond sombre : sans conséquence', '#FFF5F5F5|#FFF5F5F7': 'Fond clair et texte sombre : sans conséquence', '#FFD32F2F|#FFFF453A': 'Point des appels et LIVE sombre'}.get(f'{x}|{y}', '')] for d, x, y in sorted(near)], num=(2,)))
    agg('inventaire-opacites', '3.5 Opacités', '<p>Les gris sont des opacités du texte, comme sur le Mac. Relevé : 0,05 (carte), 0,07 (bouton, vignette), 0,12 (toucher, choisi, piste), 0,122 (<code>0x1F</code>, fond des ronds et du Journal), 0,4 (chevron, outils inactifs), 0,45 (neutre, points), 0,5 (heures), 0,55 (icône neutre), 0,56 (titre de groupe), 0,6 (secondaire), 0,62 (secondaire et titre en sombre). <b>Quasi-doublons</b> : 0,12 et 0,122 ; 0,55, 0,56, 0,6 et 0,62 ; 0,45 et 0,5. Sept nuances de gris de texte pour trois rôles (secondaire, titre, discret).</p>')
    dpg = agg('inventaire-dp', '3.6 Espacements et tailles (dp)', '<p>175 valeurs en dp, 21 différentes. L\'échelle d\'espacement du Mac (DESIGN.md) est 4, 6, 8, 10, 12, 16, 20, 24. Hors de cette échelle, en espacement : <b>2</b> (11 fois), <b>3</b>, <b>14</b> (9 fois : padding des champs, marges de la mise en route). Les autres valeurs hors échelle sont des tailles d\'objets (32, 36, 44, 48, 52, 56, 64, 76, 108).</p>',
        key=lambda r: r['valeur'].zfill(3))
    agg('inventaire-rayons', '3.7 Rayons', '<p>Rayons : 8 (ligne, vignette), 12 (carte, défaut de <code>flat</code>), 18 (rond de 36), 20 (outil), 22 (Lire), 24 (capsule de 48), 26 (switcher), et <code>size / 5,5</code> pour la vignette (8 à 44 dp, <b>6,5 à 36 dp</b>). DESIGN.md annonce 12 / 8 / capsule.</p>')
    agg('inventaire-elevations', '3.8 Élévations', '<p>Deux élévations pour le même rôle (ce qui flotte) : 6 dp pour la barre du bas, 4 dp pour la pastille.</p>')
    agg('inventaire-icones', '3.9 Icônes utilisées', '<p>28 icônes, 26 dessinées pour l\'app (vectorielles, 24 dp) et 2 d\'Android (<code>android.R.drawable.ic_media_pause</code> pour « Arrêter » dans la notification).</p>')
    dr = rows('inventaire-drawables')
    b.append('<h4>Dessin des icônes (res/drawable)</h4>' + table(['Icône', 'Dessin', 'Fichier'], [[f'<code>{esc(r["valeur"])}</code>', esc(r['role']), src(r['fichier'])] for r in dr]))
    strokes = collections.Counter()
    for r in dr:
        m = re.search(r'trait ([\d./]+)', r['role'])
        if m:
            for s_ in m.group(1).split('/'): strokes[s_] += 1
    b.append('<p>Épaisseurs de trait relevées : ' + ', '.join(f'<b>{k}</b> ({v} icônes)' for k, v in sorted(strokes.items())) + '. Material Symbols n\'a qu\'un trait par graisse.</p>')
    # textes
    tx = rows('inventaire-textes')
    b.append('<h3>3.10 Textes</h3><p>Chaque chaîne du code qui peut s\'afficher (écrans, boîtes, notifications, raisons d\'arrêt), relevée par motif puis filtrée à la main des chaînes techniques. Les contrôles typographiques sont dans la page <a href="mesures.html#typo">Mesures</a>.</p>')
    b.append('<details><summary>Les ' + str(len(tx)) + ' chaînes</summary>' + table(['Texte', 'Où'], [[esc(r['valeur']), src(r['fichier'], r['ligne'])] for r in tx]) + '</details>')
    page('inventaire.html', 'Inventaire', '\n'.join(b))
    return {'etats': len(ETATS) + len(HORS_BANC), 'composants': len(COMPOSANTS)}

if __name__ == '__main__':
    print(build())

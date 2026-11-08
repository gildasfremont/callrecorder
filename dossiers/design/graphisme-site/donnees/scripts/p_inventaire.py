import sys; sys.path.insert(0, '/tmp/claude-0/outils')
from commun import *
import json
from collections import Counter, defaultdict

X = json.load(open(f'{DON}/extraction.json'))
V = lire('css-valeurs.csv'); R = lire('css-resume.csv'); M = lire('css-mort.csv')
T = lire('textes.csv'); C = lire('cibles.csv'); I = lire('images.csv'); TF = lire('typographie-fr.csv'); ST = lire('styles-texte-1440.csv')
P = ['accueil', 'fonctionnalites', 'guides', 'versions', 'confidentialite']
out = []
w = out.append
w('<h1>Inventaire</h1><p class="chapo">Tout ce que le site affiche et tout ce que son CSS déclare, compté et situé. Les valeurs viennent du code (<code>style.css</code>, les cinq <code>index.html</code>, les trois <code>.js</code>) et du rendu (Chromium, 375, 768 et 1440 px, chaque état).</p>')
nb = dict(decl=len(V), regles=294, mortes=len(M), textes=len(T), cibles=len(C), images=len(I), couleurs=len([r for r in R if r['categorie'] == 'couleur']), tailles=len([r for r in R if r['categorie'] == 'taille']), styles=len(ST))
w('<div class="chiffres">' + ''.join(f'<div><b>{fr(v) if isinstance(v,int) else v}</b><span>{t}</span></div>' for v, t in [
    (nb['decl'], 'valeurs déclarées dans le CSS et le HTML'), (294, 'règles CSS'), (nb['mortes'], 'règles qui ne s’appliquent à rien'), (nb['textes'], 'textes rendus, par page, largeur et état'),
    (nb['styles'], 'styles de texte distincts à 1440'), (nb['couleurs'], 'couleurs distinctes dans le CSS'), (nb['tailles'], 'tailles de police déclarées'), (nb['images'], 'images visibles'), (nb['cibles'], 'cibles cliquables mesurées')]) + '</div>')
w('<ol class="sommaire"><li><a href="#pages">Pages et états</a></li><li><a href="#composants">Composants</a></li><li><a href="#typo">Typographie</a></li><li><a href="#couleurs">Couleurs</a></li><li><a href="#espacements">Espacements</a></li><li><a href="#rayons">Rayons</a></li><li><a href="#ombres">Ombres</a></li><li><a href="#divers">Graisses, interlignes, approches, ruptures, mouvement</a></li><li><a href="#images">Images</a></li><li><a href="#icones">Icônes et logos</a></li><li><a href="#textes">Textes et ponctuation</a></li><li><a href="#mort">CSS mort</a></li><li><a href="#meta">En-têtes, favicon, partage</a></li></ol>')

# Pages
w('<h2 id="pages">Pages et états</h2><p>Cinq pages. Chacune a été rendue à trois largeurs, et dans chaque état qu’un visiteur peut produire : les trois onglets de l’accueil, les deux scénarios d’installation, toutes les questions des Guides dépliées, le formulaire du message ouvert.</p>')
rows = []
for p in P:
    r = {'page': p}
    for lw in (375, 768, 1440):
        h = [x for x in X['pages'] if x['page'] == p and x['largeur'] == lw and x['etat'] == 'repos']
        r[f'hauteur {lw}'] = fr(h[0]['hauteur']) if h else ''
    r['états'] = ', '.join(sorted({x['etat'] for x in X['pages'] if x['page'] == p}))
    r['textes'] = len([t for t in T if t['page'] == p and t['largeur'] == '1440'])
    r['images'] = len([i for i in I if i['page'] == p])
    r['cibles'] = len([c for c in C if c['page'] == p and c['largeur'] == '1440'])
    r['écran 1440 × 900'] = fr(round(int(h[0]['hauteur']) / 900, 1)) if h else ''
    rows.append(r)
w(table(rows, ['page', 'hauteur 375', 'hauteur 768', 'hauteur 1440', 'écran 1440 × 900', 'textes', 'images', 'cibles', 'états'], num=('hauteur 375', 'hauteur 768', 'hauteur 1440', 'textes', 'images', 'cibles', 'écran 1440 × 900')))
w('<p class="petit">Hauteurs en px CSS. « Écran » : nombre d’écrans de 900 px à faire défiler. Largeur du document à 375 px : 432 px sur l’accueil (le micro déborde ; <code>html { overflow-x: clip }</code> empêche le défilement horizontal, vérifié sur iPhone 13 émulé : <code>scrollX</code> reste à 0).</p>')

# Composants
COMP = [
 ('Barre du haut', '.nav', '438–452, 510–518', 'toutes', 'repos, cachée en descendant, de retour en remontant', 'focus : anneau du navigateur'),
 ('Cartouche « callrecorder »', '.nav .home .marque', '443–447', 'toutes', 'repos', 'focus : anneau du navigateur (rectangle autour d’une forme arrondie)'),
 ('Lien de la barre', '.nav .links a', '450–451, 27', 'toutes', 'repos, survol (soulignement), page en cours (gris)', 'focus : navigateur'),
 ('Bouton', '.button', '31–37, 58', 'toutes', 'repos, survol (luminosité 1,04)', 'appui, focus : navigateur'),
 ('Bouton principal', '.button.hero', '41–56', 'accueil', 'repos, survol, appui', 'focus : navigateur'),
 ('Contrôle segmenté', '.tabs, .install-tabs', '120–125, 295–297', 'accueil', 'choisi, repos', 'survol, appui, focus : navigateur'),
 ('Scène : capture, Pixel 7, Claude', '.stage', '106–159', 'accueil', 'trois onglets', '—'),
 ('Fenêtre de Claude (illustration)', '.claude', '134–159, 188', 'accueil', 'trois contenus', 'contraste de la source (3,69:1)'),
 ('Dock d’icônes', '.dock .app', '215–238', 'accueil', 'repos, survol (grossit, nom)', 'focus, toucher : rien, le nom n’apparaît jamais'),
 ('Carte de bénéfice', '.benefits li', '531–573', 'accueil', 'repos', '— (non cliquable)'),
 ('Ligne de commande', '.cmdline', '255–281', 'accueil', 'repos, survol, appui, focus (accent), copiée', 'texte coupé à tous les états'),
 ('Étapes numérotées et touches', '.steps, kbd', '285–310', 'accueil', 'repos', '—'),
 ('Aide au pied d’un groupe', '.install .help', '290–292', 'accueil', 'repos', '—'),
 ('Groupe et ligne', '.group, .row', '201–211', 'guides, versions', 'repos', 'filet entre les lignes'),
 ('Question dépliable', 'details.row', '392–411', 'guides', 'fermée, ouverte', 'survol (curseur seul), focus : navigateur'),
 ('Version et badge', '.version, .latest', '414–420, 584–585', 'versions', 'repos', '—'),
 ('Sommaire', '.toc', '497–507, 521–527', 'fonctionnalites ≥ 1000 px', 'repos, survol, page en cours', 'focus : navigateur'),
 ('Figure de fonctionnalité', '.feature figure', '478–484, 577–582', 'fonctionnalites', 'repos', '—'),
 ('Lien « Toutes les fonctionnalités → »', '.more', '465–466', 'accueil', 'repos, survol', 'focus : navigateur'),
 ('Pied et bulle de Gildas', 'footer, .author', '324–341, 389, 491–492', 'toutes', 'repos', '—'),
 ('Message : texte, Dicter, Envoyer', '.message, .rec-toggle, .send', '343–388', 'toutes', 'repos, survol (Dicter), focus (Dicter, texte), Envoyer désactivé, dictée en cours, envoyé, problème', '—'),
 ('Infobulle du dock', '.dock .app::after', '231–237', 'accueil', 'survol', 'jamais au clavier ni au toucher'),
 ('« Copié »', '.cmdline .copied', '271–284', 'accueil', 'apparition, disparition (mouvement réduit respecté)', '—'),
 ('Configuration requise', '.req, .req.warn', '98–101, 198, 241–242', 'accueil', 'neutre, avertissement', '—'),
 ('Lien dans le texte', 'a', '26–27', 'toutes', 'repos (couleur seule), survol (soulignement)', 'focus : navigateur ; 1,11:1 à 2,05:1 avec le texte autour'),
]
w(f'<h2 id="composants">Composants</h2><p>{len(COMP)} composants, avec les états que le CSS leur donne et ceux qui manquent. Lignes de <code>style.css</code>.</p>')
w(table([dict(zip(['composant', 'sélecteur', 'lignes', 'pages', 'états dessinés', 'états manquants ou défauts'], c)) for c in COMP], ['composant', 'sélecteur', 'lignes', 'pages', 'états dessinés', 'états manquants ou défauts']))
etats = sum(len(c[4].split(',')) for c in COMP); manq = sum(1 for c in COMP if 'navigateur' in c[5] or 'rien' in c[5] or 'jamais' in c[5])
w(f'<p>{etats} états dessinés ; {manq} composants sur {len(COMP)} n’ont pas de focus dessiné et prennent celui du navigateur, ou n’en ont pas du tout.</p>')

# Typographie
w('<h2 id="typo">Typographie</h2>')
w('<h3>Familles</h3>')
fam = [r for r in R if r['categorie'] == 'famille']
w(table([dict(famille=r['valeur'], occurrences=r['occurrences'], lieux=r['lieux']) for r in fam], ['famille', 'occurrences', 'lieux'], num=('occurrences',)))
w('<p>Chargées depuis Google Fonts : Host Grotesk 400 et 500 (seule la 500 sert : 0 texte rendu en 400), Archivo 500 en largeur 112, limitée aux lettres <code>acdelor</code> du cartouche. Le texte courant est en police du système (SF Pro sur Mac ; Inter dans nos rendus Linux).</p>')
w('<h3>Tailles déclarées</h3>')
ts = [r for r in R if r['categorie'] == 'taille']
w(table([dict(taille=r['valeur'][:60], occurrences=r['occurrences'], lieux=r['lieux']) for r in ts], ['taille', 'occurrences', 'lieux'], num=('occurrences',)))
sz = Counter(round(float(t['taille']), 2) for t in T if t['largeur'] == '1440')
w(f'<h3>Tailles rendues à 1440 px</h3><p>{len(sz)} tailles distinctes sur {sum(sz.values())} textes. Les tailles non entières viennent des <code>clamp()</code> en <code>cqw</code> de la fenêtre de Claude.</p>')
w(table([dict(taille=fr(k), textes=v) for k, v in sorted(sz.items())], ['taille', 'textes'], num=('taille', 'textes')))
w(f'<h3>Styles de texte rendus à 1440 px</h3><p>{len(ST)} combinaisons distinctes de famille, taille, graisse, interligne et couleur.</p>')
w(table(ST, ['famille', 'taille', 'graisse', 'interligne', 'couleur', 'occurrences', 'pages', 'selecteurs'], num=('taille', 'graisse', 'interligne', 'occurrences')))

# Couleurs
cols = [r for r in R if r['categorie'] == 'couleur']
w(f'<h2 id="couleurs">Couleurs</h2><p>{len(cols)} valeurs distinctes, {sum(int(r["occurrences"]) for r in cols)} emplois. Neuf seulement sont des variables (<code>:root</code>, lignes 2–14) ; le reste est écrit en dur.</p>')
enc = [r for r in cols if r['valeur'].startswith('rgba(20,40,80')]
w(f'<p><b>Quasi-doublons.</b> L’encre bleu nuit <code>rgba(20,40,80, x)</code> revient avec {len(enc)} opacités différentes : ' + ', '.join(sorted({r["valeur"][14:-1] for r in enc}, key=float)) + '. Deux autres encres proches s’y ajoutent : <code>rgba(30,60,120,.07)</code> (fond du contrôle segmenté) et <code>rgba(0,60,180,.5)</code>. Les bords d’un même rôle (contour d’un groupe, d’un bouton) vont de 0,08 à 0,16.</p>')
w(table([dict(c=sw(r['valeur']) + e(r['valeur']), occurrences=r['occurrences'], lieux=r['lieux']) for r in cols], ['c', 'occurrences', 'lieux'], num=('occurrences',), raw=('c',)).replace('<th class="">c</th>', '<th>couleur</th>'))

# Espacements
sp = [r for r in R if r['categorie'] == 'espacement']
SCALE = [0, 2, 4, 6, 8, 10, 12, 16, 20, 24, 28, 32, 40, 48, 56, 64, 80, 96, 120, 160]
def px(v):
    try: return float(v.replace('px', '')) if v.endswith('px') or v == '0' else None
    except: return None
ons = [r for r in sp if px(r['valeur']) is not None and abs(px(r['valeur'])) in SCALE]
offs = [r for r in sp if px(r['valeur']) is not None and abs(px(r['valeur'])) not in SCALE]
other = [r for r in sp if px(r['valeur']) is None]
w(f'<h2 id="espacements">Espacements</h2><p>{sum(int(r["occurrences"]) for r in sp)} valeurs de marge, de retrait, d’écart et de position. En px : {sum(int(r["occurrences"]) for r in ons)} tombent sur l’échelle 2, 4, 6, 8, 10, 12, 16, 20, 24, 28, 32, 40, 48, 56, 64, 80, 96, 120, 160 (celle de l’app, prolongée pour les grandes marges du site) ; {sum(int(r["occurrences"]) for r in offs)} n’y sont pas ; {sum(int(r["occurrences"]) for r in other)} sont relatives (em, %, cqw, calc).</p>')
w('<h3>Hors échelle</h3>' + table([dict(valeur=r['valeur'], occurrences=r['occurrences'], lieux=r['lieux']) for r in sorted(offs, key=lambda r: abs(px(r['valeur'])))], ['valeur', 'occurrences', 'lieux'], num=('occurrences',)))
w('<details class="donnees"><summary>Toutes les valeurs d’espacement</summary>' + table([dict(valeur=r['valeur'], occurrences=r['occurrences'], lieux=r['lieux']) for r in sp], ['valeur', 'occurrences', 'lieux'], num=('occurrences',)) + '</details>')

# Rayons
ra = [r for r in R if r['categorie'] == 'rayon']
w(f'<h2 id="rayons">Rayons</h2><p>{len(ra)} valeurs pour {sum(int(r["occurrences"]) for r in ra)} emplois. Des voisins sans rôle distinct : 4, 5, 6, 7 px ; 8, 9, 10, 11 px ; 16, 18, 20, 22 px. Les rayons en % et em dessinent les fenêtres de macOS à l’échelle de la capture et la forme du cartouche : ils restent.</p>')
w(table([dict(valeur=r['valeur'], occurrences=r['occurrences'], lieux=r['lieux']) for r in ra], ['valeur', 'occurrences', 'lieux'], num=('occurrences',)))

# Ombres
om = [r for r in V if r['categorie'] == 'ombre' and r['valeur'] != 'none']
w(f'<h2 id="ombres">Ombres et filtres</h2><p>{len(om)} déclarations, {len({r["valeur"] for r in om})} différentes. Trois rôles : un contour (1 px d’encre), une carte posée (ombre large, faible), une capture qui flotte (ombre longue). Chaque rôle a aujourd’hui trois à six variantes.</p>')
w(table([dict(valeur=r['valeur'], sélecteur=r['selecteur'], lieu=f"{r['fichier']}:{r['ligne']}") for r in om], ['valeur', 'sélecteur', 'lieu']))

# Divers
w('<h2 id="divers">Graisses, interlignes, approches, ruptures, mouvement</h2>')
for cat, titre in [('graisse', 'Graisses'), ('interligne', 'Interlignes'), ('approche', 'Approches'), ('rupture', 'Points de rupture'), ('mouvement', 'Mouvement'), ('opacite', 'Opacités'), ('plan', 'Plans (z-index)')]:
    rr = [r for r in R if r['categorie'] == cat]
    w(f'<h3>{titre}</h3>' + table([dict(valeur=r['valeur'], occurrences=r['occurrences'], lieux=r['lieux']) for r in rr], ['valeur', 'occurrences', 'lieux'], num=('occurrences',)))
w('<p>Sept points de rupture : 452, 480, 640, 760, 980, 1000, 1600 px. 640 sert huit fois, 760 trois fois ; 980 et 1000 sont à 20 px l’un de l’autre.</p>')

# Images
tot = sum(int(r['octets'] or 0) for r in I)
w(f'<h2 id="images">Images</h2><p>{len(I)} images visibles, {fr(round(tot / 1024))} Ko au total. « Échelle » : largeur affichée × 2 ÷ largeur du fichier, soit la taille du dessin par rapport à sa taille réelle sur un écran Retina (1 = taille réelle ; 0,5 = moitié).</p>')
w(table([dict(page=r['page'], image=r['src'].split('/')[-1], format=r['format'], ko=fr(round(int(r['octets'] or 0) / 1024)), naturelle=f"{r['nat_l']}×{r['nat_h']}", **{'375': r['echelle_375'], '768': r['echelle_768'], '1440': r['echelle_1440']}, contour='découpe' if r['decoupe'] == 'True' else (r['bord'] and 'cadre') or '', dimensions='oui' if r['attr_dim'] == 'True' else 'non', paresseux=r['loading']) for r in I],
           ['page', 'image', 'format', 'ko', 'naturelle', '375', '768', '1440', 'contour', 'dimensions', 'paresseux'], num=('ko', '375', '768', '1440')))

# Icônes
w('<h2 id="icones">Icônes et logos</h2>')
dock = [('Zoom', 'pile/zoom.png', 'tuile'), ('Microsoft Teams', 'pile/teams.png', 'tuile'), ('Google Meet', 'pile/meet.webp', 'tuile, glyphe sur blanc'), ('WhatsApp', 'pile/whatsapp.webp', 'tuile'), ('Slack', 'pile/slack.png', 'tuile'), ('FaceTime', 'logos/facetime.png', 'icône macOS entière'), ('Téléphone (iPhone)', 'dock/telephone.png', 'tuile'), ('Webex', 'dock/webex.png', 'tuile'), ('Messenger', 'dock/messenger.png', 'tuile'), ('Loom', 'dock/loom.png', 'tuile'), ('Doctolib', 'dock/doctolib.png', 'tuile'), ('Jitsi Meet', 'dock/jitsi.png', 'tuile'), ('Safari', 'logos/safari.png', 'icône macOS entière'), ('Google Chrome', 'logos/chrome.png', 'icône macOS entière'),
        ('Claude', 'logos/claude-app.png', 'icône macOS entière'), ('Codex', 'logos/codex.png', 'icône macOS entière'), ('Cursor', 'dock/cursor.png', 'tuile'), ('VS Code', 'dock/vscode.png', 'tuile, glyphe sur blanc'), ('Gemini CLI', 'dock/gemini.png', 'tuile'), ('LM Studio', 'dock/lmstudio.png', 'tuile'), ('Hermes Agent', 'logos/hermes.png', 'tuile')]
rows = []
for n, f, k in dock:
    p = f'/tmp/site/img/{f}'
    try:
        from PIL import Image; im = Image.open(p); dim = f'{im.width}×{im.height}'
    except Exception: dim = ''
    rows.append(dict(nom=n, fichier=f, traitement=k, naturelle=dim, ko=fr(round(os.path.getsize(p) / 1024)), **{'affichée 375': '22 px (17,6 dans la tuile)', 'affichée 1440': '56 px (44,8)'}))
w(f'<p>{len(dock)} icônes d’apps dans les deux docks de l’accueil ; elles viennent de trois dossiers (<code>pile/</code>, <code>dock/</code>, <code>logos/</code>), en PNG de 256 px, et ne sont pas toutes traitées de la même façon (tuile rentrée de 10 %, glyphe sur blanc, icône entière).</p>')
w(table(rows, ['nom', 'fichier', 'traitement', 'naturelle', 'ko', 'affichée 375', 'affichée 1440'], num=('ko',)))
w('<p>Icônes dessinées dans le CSS (SVG en données) : la flèche du bouton principal (<code>style.css:51</code>), le téléchargement (<code>:318</code>, règle morte), le micro de Dicter (<code>:359</code>), le chevron des Guides (bordures, <code>:399–403</code>). Icône du site : micro, 16, 32, 64 et 180 px (PNG), plus <code>icone-micro.webp</code> (256 px, 76 Ko) affichée à 19 px dans la fenêtre de Claude.</p>')

# Textes
w(f'<h2 id="textes">Textes et ponctuation</h2><p>{len(T)} textes rendus (une ligne par élément, page, largeur et état), dans <a href="donnees/textes.csv">textes.csv</a> avec leur style calculé et leur contraste. Ponctuation française, comptée sur le texte visible de chaque page (<a href="donnees/typographie-fr.csv">typographie-fr.csv</a>, et chaque lieu à corriger avec sa ligne dans <a href="donnees/typographie-fr-lieux.csv">typographie-fr-lieux.csv</a>) :</p>')
keys = [k for k in TF[0] if k != 'page']
w(table([dict(cas=k, **{p['page']: p[k] for p in TF}, total=sum(int(p[k]) for p in TF)) for k in keys], ['cas'] + [p['page'] for p in TF] + ['total'], num=tuple([p['page'] for p in TF] + ['total'])))

# CSS mort
etat = {'.nav.hidden', '.cmdline .copied', '.message.sent .rec-bar, .message.sent textarea, .message.sent .message-actions', '.author .message.sent .sent-status', '.rec-state.problem', 'details.row[open] summary::after', '.req.warn', '.intro .req.warn'}
mort = [m for m in M if m['selecteur'] not in etat]
w(f'<h2 id="mort">CSS mort</h2><p>Sur 294 règles, {len(M)} ne trouvent aucun élément dans les cinq pages au repos. {len(M) - len(mort)} ne servent qu’à un état posé par le script (barre cachée, « Copié », message envoyé, question ouverte, Mac incompatible) : elles vivent. Les {len(mort)} autres ne s’appliquent à rien : restes de la pile d’icônes en éventail (<code>.pair</code>, <code>.pile</code>), de la page de téléchargement (<code>.download</code>, <code>.file</code>), de l’ancienne scène (<code>.stage .detail</code>), de titres de ligne (<code>.row h3</code>) et d’autres. Lighthouse estime le CSS inutilisé à 10 Kio sur l’accueil.</p>')
w(table([dict(sélecteur=m['selecteur'], ligne=m['ligne']) for m in mort], ['sélecteur', 'ligne'], num=('ligne',)))

# Meta
MT = lire('meta.csv')
w('<h2 id="meta">En-têtes, favicon, partage</h2><p>Chaque page déclare son titre, sa description, ses aperçus Open Graph (1200 × 630, JPEG), quatre icônes (16, 32, 64, 180 px) et <code>color-scheme: light only</code>. Aucune ne déclare <code>og:image:alt</code> ni <code>theme-color</code>.</p>')
w('<details class="donnees"><summary>Toutes les balises</summary>' + table(MT, ['page', 'balise']) + '</details>')

ecrire('inventaire.html', page('inventaire.html', 'Inventaire du site', 'Chaque page, état, composant et valeur du site de Callrecorder, comptés et situés.', '\n'.join(out)))

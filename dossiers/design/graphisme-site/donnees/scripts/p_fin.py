import sys, csv, json, importlib; sys.path.insert(0, '/tmp/claude-0/outils')
from commun import *
from PIL import Image
import problemes_data; importlib.reload(problemes_data)
P = {p['id']: p for p in problemes_data.P}
AA = {r['mesure']: r for r in lire('avant-apres.csv')}

# ——— Prototypes ———
o = []; w = o.append
w('<h1>Prototypes</h1><p class="chapo">Les cinq pages du site, refaites avec toutes les recos retenues, à côté des pages actuelles. Ce sont de vraies pages : mêmes HTML, mêmes images, mêmes textes, même CSS, plus une feuille qui corrige. Tous les états se manipulent : survol, focus au clavier, onglets, questions dépliables, message.</p>')
w('<div class="chiffres"><div><b><a href="prototypes/index.html">Comparateur</a></b><span>avant et après côte à côte, 5 pages, 375 / 768 / 1440 px, clair et sombre (option), défilement lié</span></div><div><b><a href="prototypes/etats.html">États</a></b><span>chaque composant dans chacun de ses états, avant et après</span></div><div><b><a href="prototypes/css/apres.css">apres.css</a></b><span>toutes les corrections, rangées par problème (P1…P23)</span></div></div>')
w('<h2>Comment ils sont faits</h2><ul><li><b>Avant</b> : les cinq <code>index.html</code> du dépôt du site au commit <code>953f6d3</code>, avec <code>style.css</code> copié tel quel (<code>prototypes/css/site-953f6d3.css</code>). Les images viennent du site en ligne. Le formulaire n’envoie rien.</li>'
  '<li><b>Après</b> : les mêmes pages, transformées par <code>donnees/scripts/prototypes.py</code> (repère <code>&lt;main&gt;</code>, typographie française, chemins de menu, extraits recadrés, carte iPhone, Confidentialité en masses…), et <code>apres.css</code> chargé après le CSS du site. Les extraits recadrés sont dans <code>prototypes/img/</code>.</li>'
  '<li><b>Sombre</b> : une option (P23), qui va contre un choix tranché ; activée seulement par <code>?theme=sombre</code>. Le site actuel n’a pas de sombre : dans le comparateur, seul l’après change.</li>'
  '<li><b>Mesuré</b> : les scripts de mesure ont tourné sur l’après ; résultats dans <a href="mesures.html#avant-apres">Mesures</a>.</li></ul>')
PAIRS = [('p01-fonctionnalites-reunions.webp', 1, 'Fonctionnalités, Réunions, 1440 px : fenêtre entière à ×0,63 → extrait à ×1.'), ('p02-ligne-375.webp', 2, 'Ligne d’installation, 375 px.'), ('p03-versions-1440.webp', 3, 'Versions, 1440 px.'), ('p05-docks-375.webp', 5, 'Docks, 375 px.'),
         ('p06-sources-1440.webp', 6, 'Sources des citations (et P15, la source sur sa ligne).'), ('p07-focus-onglets.webp', 7, 'Focus au clavier sur le contrôle segmenté ; segments non choisis en gris secondaire.'), ('p10-cartes-1440.webp', 10, 'Cartes de l’accueil (et P17, largeur 760).'),
         ('p12-sous-titre-versions-375.webp', 12, 'En-tête des Versions, 375 px.'), ('p13-confidentialite-1440.webp', 13, 'Confidentialité, 1440 px.'), ('p14-guides-1440.webp', 14, 'Guides, 1440 px.'), ('p16-titre-fonctionnalites-1440.webp', 16, 'Titre des Fonctionnalités, 1440 px.'),
         ('p17-accueil-bords-1440.webp', 17, 'Accueil, 1440 px, réduit de moitié : les bords.'), ('p21-titre-1440.webp', 21, 'Titre de l’accueil.'), ('p23-accueil-sombre-1440.webp', 23, 'Accueil en sombre (option) : fond et texte inversés, Claude et les cartes restent du papier.')]
w('<h2>Avant et après, image par image</h2><p>Les mêmes cadrages, pris sur les deux prototypes à l’échelle 2, affichés ici à leur taille CSS.</p>')
for f, n, c in PAIRS:
    wd = Image.open(f'{D}/images/{f}').width
    wd = wd if f.startswith('p17') else wd // 2
    w(f'<figure id="i{n}"><img src="images/{f}" width="{min(wd, 1048)}" alt="{e(c)}" loading="lazy"><figcaption><a href="problemes.html#p{n}">P{n}</a> · {e(c)}</figcaption></figure>')
ecrire('prototypes.html', page('prototypes.html', 'Prototypes avant et après', 'Les cinq pages du site de Callrecorder, avant et après les recos, en vraies pages à manipuler.', '\n'.join(o)))

# ——— Plan ———
o = []; w = o.append
LOTS = [
 ('Lot 1 · Accessibilité et corrections sans risque', [9, 6, 8, 20, 7, 15, 16, 2], '4 h', 'Faible : rien ne change de place ; P6 change --secondary, partagé avec DESIGN.md (même commit).', 'axe-core à 0 sur les cinq pages ; contrastes ≥ 4,5:1 ; l’anneau sur la planche des états.'),
 ('Lot 2 · Captures et images', [1, 3, 4], '1,5 jour', 'Moyen : chaque extrait est un choix de cadrage ; respecter les règles de capture de DESIGN.md (rectangle et liseré pour un extrait, contour et drop-shadow pour un objet) ; ne jamais écraser une vignette de version.', 'échelles 0,8–1,05 à 1440 ; CLS ≤ 0,1 ; accueil ≤ 1 400 Ko ; scripts/controle-captures.py passe.'),
 ('Lot 3 · Typographie', [11, 12, 21, 18], '1 jour', 'Moyen : la passe typographique touche 434 lieux de texte ; <code>scripts/retours.py</code> compare des textes, il faut vérifier qu’il ne prend pas une apostrophe changée pour un texte retiré qui revient (le dire dans le commit si besoin). L’échelle de texte grandit les cartes de l’accueil d’une ligne.', 'typographie-fr.csv à 0 ; ≤ 6 tailles en px hors titres ; aucun « › » en début de ligne.'),
 ('Lot 4 · Mise en page', [5, 14, 17, 13, 10], '4 h + décisions', 'Moyen : P10 et P13 touchent des textes (une phrase déplacée, quatre titres) et attendent Gildas ; P14 va contre la convention observée, pour suivre le principe tranché.', 'bords communs à 1440 ; dock ≥ 40 px à 375 ; 0 filet entre lignes ; douze paragraphes intacts.'),
 ('Lot 5 · Système', [19, 22], '1 jour', 'Moyen à fort : ≈ 230 lignes de style.css ; risque de régression visuelle. Faire la migration valeur par valeur, comparer les rendus avant et après au pixel (même script que les prototypes), et ne garder un écart que s’il est voulu.', 'aucune couleur littérale hors :root et Claude ; 0 règle morte ; rendus identiques hors écarts listés.'),
 ('Option · Sombre', [23], '1 jour', 'Revient sur dfc6ecb ; dépend du lot 5 ; demande des captures sombres de l’app.', 'contraste ≥ 4,5:1 en sombre sur chaque couple.'),
]
w('<h1>Plan</h1><p class="chapo">Les 23 recos en six lots, dans l’ordre où les faire. Chaque lot se livre seul, se vérifie par ses critères, et ne dépend que des précédents.</p>')
tot = 0
rows = []
for i, (t, ids, eff, risque, verif) in enumerate(LOTS, 1):
    rows.append({'ordre': i, 'lot': t, 'problèmes': ' '.join(f'<a href="problemes.html#p{n}">P{n}</a>' for n in ids), 'effort': eff, 'risques': risque, 'vérification': verif})
w(table(rows, ['ordre', 'lot', 'problèmes', 'effort', 'risques', 'vérification'], raw=('problèmes', 'risques', 'vérification')))
w('<p>Effort total, lots 1 à 5 : <b>environ 4 jours</b> pour une personne qui connaît le site, vérifications comprises (somme des estimations par problème : ≈ 25 h, plus le recadrage, la relecture des rendus et les allers-retours). L’option sombre : un jour de plus.</p>')
w('<h2>Détail des efforts</h2>' + table([{'n': f'<a href="problemes.html#p{p["id"]}">P{p["id"]}</a>', 'problème': e(p['titre']), 'gravité': p['grav'], 'effort': p['effort']} for p in problemes_data.P], ['n', 'problème', 'gravité', 'effort'], raw=('n', 'problème')))
w('<h2>Ce qui touche à un choix déjà tranché</h2>')
TR = [(23, 'Thème clair uniquement', '<code>55a2120</code>, <code>dfc6ecb</code> ; DESIGN.md', 'Rien n’est changé ; l’option est prototypée pour décider sur pièce. La convention observée (9 sites sur 10 à thème fixe) soutient le choix.'),
      (21, 'Titre « Souvenez-vous de tout » et sa coupure', '<code>1e46486</code> ; <code>style.css:60–67</code>', 'Ni le titre ni la coupure ne changent ; seul le trait d’union est raccourci.'),
      (5, 'Le Dock des apps prises en charge', '<code>bd505a4</code>', 'Le Dock reste ; il passe sur deux rangées sous 640 px. La convention observée (une liste avec les noms) est l’option D.'),
      (14, 'Pas de filets', 'DESIGN.md, Principes et Écarts connus', 'La reco applique le principe, contre la convention observée des FAQ (filets sur 5 sites sur 5). À confirmer.'),
      (10, 'Carte iPhone et textes de l’accueil', '<code>d08fba2</code> ; TEXTES.md', 'Une phrase déplacée, mot pour mot ; à confirmer.'),
      (13, 'Titres de Confidentialité', 'TEXTES.md : un mot nouveau entre avec la décision de Gildas', 'Quatre titres proposés ; à écrire par Gildas.'),
      (6, 'Gris secondaire du site', 'DESIGN.md, tableau du site', '#566175 → #515c70 ; DESIGN.md change dans le même commit. L’accent #0064d2 ne change pas.'),
      (2, 'Ligne de commande coupée', '<code>55a2120</code>', 'Aucune raison écrite ; la reco l’ouvre.')]
w(table([{'P': f'<a href="problemes.html#p{n}">P{n}</a>', 'choix': c, 'origine': s, 'ce que fait la reco': r} for n, c, s, r in TR], ['P', 'choix', 'origine', 'ce que fait la reco'], raw=('P', 'origine')))
w('<h2>Ce que Gildas seul peut trancher</h2><ol><li>P10 : replier la carte iPhone dans les cassettes (prototypé), ou commander un dessin.</li><li>P13 : les quatre titres de Confidentialité.</li><li>P5 : garder le Dock en grille au téléphone (prototypé), ou la liste avec noms des sites de référence.</li><li>P14 : le principe sans filets, ou la convention des FAQ.</li><li>P23 : rester en clair (recommandé), ou l’option sombre.</li></ol>')
w('<h2>Vérifier sans humain</h2><p>Les scripts de <code>donnees/scripts/</code> refont toutes les mesures sur n’importe quelle version du site : <code>BASE=&lt;url&gt; node extrait.js &lt;dossier&gt;</code>, <code>node axe.js</code>, puis <code>python3 compare.py</code> pour l’avant / après. Chaque critère d’acceptation de <a href="problemes.html">Problèmes</a> se lit dans leur sortie.</p>')
ecrire('plan.html', page('plan.html', 'Plan de travail', 'Les recos graphiques du site de Callrecorder en lots, dans l’ordre, avec effort, risques et choix déjà tranchés.', '\n'.join(o)))

# ——— Synthèse ———
o = []; w = o.append
w('<h1>Le site, relu par un graphiste</h1><p class="chapo">Relecture complète du site de Callrecorder : les cinq pages, chaque état, aux trois largeurs, en clair et en sombre. Tout ce qui est affirmé ici se prouve par une mesure, une capture ou une ligne de code ; les données brutes sont à côté.</p>')
w('<div class="chiffres">' + ''.join(f'<div><b>{v}</b><span>{t}</span></div>' for v, t in [
    ('965', 'valeurs du CSS inventoriées, ligne par ligne'), ('1 500', 'textes rendus, chacun avec son contraste WCAG et APCA'), ('25', 'composants et leurs états'), ('124 + 131', 'cibles mesurées à 375 et 1 440 px'), ('82', 'images, échelle et poids'),
    ('10 + 20', 'rapports Lighthouse et passes axe'), ('50', 'observations sur 13 sites de référence'), ('23', 'problèmes, spécifiés et prototypés')]) + '</div>')
w('<h2>Les dix problèmes qui comptent le plus</h2><ol>')
TOP = [(1, 'Les captures des Fonctionnalités sont à ×0,63 : le texte de l’app tombe à 8 px sur ordinateur, 3,5 px sur téléphone (4 figures sur 10). Après : ×0,81 à ×1.'),
       (2, 'La commande d’installation est coupée par « … » à toutes les largeurs : « | zsh » n’est jamais visible. Aucun des sites d’installation observés ne coupe.'),
       (3, 'Les vignettes des Versions vont de ×0,33 à ×1,89 ; 21 images sans dimensions, CLS 0,109. Après : ×0,81 à ×1.'),
       (4, 'L’accueil pèse 2 491 Ko ; à la taille utile, 1 245 Ko. LCP mobile 5,1 s (seuil : 2,5 s).'),
       (5, 'Au téléphone, 21 icônes d’apps à 22 px, et leur nom n’apparaît qu’au survol de la souris.'),
       (6, '18 textes sous WCAG AA (sources des citations, 3,69:1), chevron à 2,65:1, 67 textes secondaires sous APCA. Après : 0 sous WCAG.'),
       (7, '13 composants sur 25 sans focus dessiné, quatre dessins de focus différents. Après : un seul anneau.'),
       (8, 'axe-core : 118 nœuds en violation sur 5 règles (pas de main, liens indistincts du texte à 1,11:1). Après : 0.'),
       (10, 'Une carte de l’accueil sur six a perdu son objet depuis d08fba2 ; la série se décale.'),
       (11, '360 apostrophes droites pour 1 courbe ; 41 signes doubles sur une espace sécable ; 48 « › » qui peuvent commencer une ligne.')]
for n, t in TOP: w(f'<li><a href="problemes.html#p{n}"><b>P{n}</b></a> · {e(t)}</li>')
w('</ol>')
w('<h2>Avant, après</h2>' + table([dict(mesure=k, avant=AA[k]['avant'], après=AA[k]['apres']) for k in ['textes sous WCAG 2 AA (1.4.3)', 'contraste WCAG le plus bas', 'textes sous APCA (seuil Bronze)', 'violations axe (nœuds, 5 pages × 2 largeurs)', 'captures sous ×0,8 à 1440', 'captures au-dessus de ×1,05 à 1440', 'captures Fonctionnalités et Versions à 375 : échelle min', 'tailles de texte distinctes à 1440']], ['mesure', 'avant', 'après'], num=('avant', 'après')))
w('<p class="petit">Mesuré sur le site en ligne et sur les <a href="prototypes.html">prototypes</a>, avec les mêmes scripts. Poids des images et Lighthouse de l’après : non mesurés (les prototypes chargent les images du site en ligne) ; le gain est calculé image par image dans <a href="mesures.html#poids">Mesures</a>.</p>')
w('<h2>Le dossier</h2><ul class="sommaire">'
  '<li><a href="inventaire.html">Inventaire</a> : pages, états, 25 composants, typographie, 54 couleurs, espacements, rayons, ombres, 82 images, 21 icônes, ponctuation, 49 règles mortes.</li>'
  '<li><a href="mesures.html">Mesures</a> : Lighthouse, axe, contrastes WCAG 2 et APCA, cibles, échelles, poids, avant et après.</li>'
  '<li><a href="problemes.html">Problèmes et recos</a> : 23 problèmes, chacun avec preuve, cause, impact, options, choix, règles, spécification et critères.</li>'
  '<li><a href="prototypes.html">Prototypes</a> : les cinq pages refaites, à manipuler, et la planche des états.</li>'
  '<li><a href="systeme.html">Système et migration</a> : les variables, et chaque déclaration de style.css avec sa nouvelle valeur.</li>'
  '<li><a href="plan.html">Plan</a> : six lots, ≈ 4 jours, les risques, et ce qui revient à Gildas.</li></ul>')
w('<h2>Ce qui a été regardé, et comment</h2><p>Le site en ligne (<a href="https://gildasfremont.github.io/callrecorder/">gildasfremont.github.io/callrecorder</a>), identique au dépôt <code>gildasfremont/callrecorder</code> au commit <code>953f6d3</code>. Rendus Chromium aux trois largeurs et dans chaque état ; Lighthouse 12.2.1 et axe-core 4.10.2 ; extraction de chaque texte, cible et image avec ses styles calculés ; inventaire statique de <code>style.css</code> ; observation de 13 sites de référence (installation, focus, onglets, icônes, sommaire, FAQ, journal des versions, sombre, typographie, confidentialité). Lus avant : DESIGN.md, TEXTES.md, MANIFESTE.md, le CLAUDE.md du site. Aucun autre travail de designer n’a été lu.</p>')
w('<h2>Ce qui va bien, et reste</h2><ul><li>Le rythme vertical (160 / 56 px) et la scène de l’accueil : capture, Pixel 7 et fenêtre de Claude, ombres qui suivent les contours.</li><li>La palette : neuf valeurs nommées, une encre bleu nuit cohérente ; le texte courant à 10,2:1.</li><li>Les aperçus de partage (sauf Versions, P22) et le respect de <code>prefers-reduced-motion</code>.</li><li>Le contrôle de compatibilité du Mac, discret et juste.</li><li>Le choix du clair : 9 des 10 sites de référence ont un thème fixe.</li></ul>')
w('<h2>Où la reco va contre la convention observée</h2><ul><li><a href="problemes.html#p14">P14</a> : les FAQ de référence séparent leurs questions par des filets (5 sur 5) ; la reco suit le principe « pas de filets » de Gildas.</li><li><a href="problemes.html#p5">P5</a> : au téléphone, les sites de référence passent les icônes en liste avec leur nom ; la reco garde le Dock, en deux rangées.</li></ul>')
w('<p class="petit">La première liste, plus courte, reste dans <a href="../graphisme-site.html">graphisme-site.html</a>.</p>')
ecrire('index.html', page('index.html', 'Le site, relu par un graphiste', 'Dossier de relecture graphique du site de Callrecorder : synthèse, inventaire, mesures, 23 problèmes, prototypes, système et plan.', '\n'.join(o)))

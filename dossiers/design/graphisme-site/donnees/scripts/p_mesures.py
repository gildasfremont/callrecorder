import sys; sys.path.insert(0, '/tmp/claude-0/outils')
from commun import *
import json
from collections import Counter, defaultdict
LH = lire('lighthouse-resume.csv'); AX = json.load(open(f'{DON}/axe.json')); AXB = json.load(open(f'{DON}/axe-apres.json'))
CT = lire('contrastes.csv'); C = lire('cibles.csv'); I = lire('images.csv'); PI = lire('poids-images-accueil.csv'); AA = lire('avant-apres.csv'); TF = lire('typographie-fr.csv')
FAILS = json.load(open(f'{DON}/lighthouse-echecs.json'))
out = []; w = out.append
w('<h1>Mesures</h1><p class="chapo">Ce qui a été mesuré, avec quel outil, et ce qui en sort. Chaque tableau renvoie à son fichier brut.</p>')
w('<h2>Méthode</h2><ul>'
  '<li><b>Rendu</b> : Chromium sans tête (Playwright), viewports 375 × 900, 768 × 900 et 1440 × 900, échelle 1 pour les mesures et 2 pour les captures. Chaque page est parcourue jusqu’en bas pour charger les images paresseuses, puis mesurée dans chaque état (<code>scripts/extrait.js</code>).</li>'
  '<li><b>Contraste WCAG 2</b> : rapport de luminance relative (WCAG 2.1, critère <a href="https://www.w3.org/TR/WCAG21/#contrast-minimum">1.4.3</a>) entre la couleur calculée du texte et son fond effectif, composé à travers les fonds semi-transparents des parents. Seuil 4,5:1, ou 3:1 pour 24 px et plus (18,66 px en gras).</li>'
  '<li><b>APCA</b> : formule 0.0.98G-4g (<code>apca-w3</code> 0.1.9), en valeur absolue Lc. Seuils « Bronze » simplifiés : Lc 75 pour le texte courant (sous 18 px, ou sous 16 px en gras), Lc 60 de 18 à 24 px, Lc 45 au-delà (<a href="https://git.apcacontrast.com/documentation/APCA_in_a_Nutshell">APCA in a Nutshell</a>). APCA n’est pas une norme ; il sert ici à repérer ce que WCAG 2 laisse passer de justesse.</li>'
  '<li><b>Cibles</b> : boîte de chaque lien, bouton, résumé et champ ; distance au centre de la cible voisine. WCAG 2.2 <a href="https://www.w3.org/TR/WCAG22/#target-size-minimum">2.5.8</a> : 24 × 24 px, ou un cercle de 24 px autour qui ne touche aucune autre cible ; un lien dans une phrase en est exempté. Apple, <a href="https://developer.apple.com/design/human-interface-guidelines/accessibility#Buttons-and-controls">HIG, Accessibility</a> : 44 × 44 pt au toucher.</li>'
  '<li><b>Lighthouse 12.2.1</b>, profils mobile et ordinateur, sur le site en ligne. <b>axe-core 4.10.2</b>, règles WCAG 2.0 à 2.2 A et AA et bonnes pratiques, à 375 et 1440 px, questions des Guides dépliées.</li>'
  '<li><b>Après</b> : les mêmes scripts sur les prototypes (<a href="prototypes.html">prototypes.html</a>), servis en local.</li></ul>')

# Avant / après
w('<h2 id="avant-apres">Avant et après, sur les mêmes mesures</h2>')
w(table([dict(mesure=r['mesure'], avant=r['avant'], après=r['apres']) for r in AA if not r['avant'].startswith('{')], ['mesure', 'avant', 'après'], num=('avant', 'après')))
w('<p class="petit">Les textes mesurés sont plus nombreux après : la carte iPhone repliée, les chemins de menu découpés en étapes, les titres de Confidentialité. Les 111 textes encore sous APCA : 87 liens à l’accent <code>#0064d2</code> (Lc 69, 4,97:1 en WCAG 2 ; option B de <a href="problemes.html#p6">P6</a>, non retenue), 12 libellés de la fenêtre de Claude à 11 px sur téléphone, 9 extraits de code gris sur gris clair, 3 « Copier » de la ligne de commande (13 px).</p>')

# Lighthouse
w('<h2 id="lighthouse">Lighthouse</h2><p>Fichiers <a href="donnees/lighthouse-resume.csv">lighthouse-resume.csv</a> et un JSON par page et profil (captures retirées).</p>')
w(table([dict(page=r['page'], performance=r['performance'], accessibilité=r['accessibility'], **{'bonnes pratiques': r['best-practices']}, seo=r['seo'], **{'LCP ms': fr(int(r['lcp_ms'])), 'FCP ms': fr(int(r['fcp_ms'])), 'CLS': r['cls'], 'poids Ko': fr(int(r['poids_ko']))}) for r in LH],
          ['page', 'performance', 'accessibilité', 'bonnes pratiques', 'seo', 'FCP ms', 'LCP ms', 'CLS', 'poids Ko'], num=('performance', 'accessibilité', 'bonnes pratiques', 'seo', 'FCP ms', 'LCP ms', 'CLS', 'poids Ko')))
w('<p>Audits sous 0,9 :</p>' + table([dict(audit=k, titre=v[0][1], pages=len(v), exemple=f'{v[0][0]} : {v[0][2]}') for k, v in FAILS.items()], ['audit', 'titre', 'pages', 'exemple'], num=('pages',)))
w('<p>L’accueil pèse 2 465 Ko et met 5,1 s à afficher sa plus grande image sur le profil mobile (4G lente simulée) : c’est la seule page sous 90 en performance. Les Versions décalent leur mise en page (CLS 0,109, au-delà de 0,1) : 21 images n’ont ni <code>width</code> ni <code>height</code>.</p>')

# axe
w('<h2 id="axe">axe-core</h2><p>Fichiers <a href="donnees/axe.json">axe.json</a> (avant) et <a href="donnees/axe-apres.json">axe-apres.json</a> (après : aucune violation).</p>')
w(table([dict(page=v['page'], largeur=v['largeur'], règle=v['regle'], impact=v['impact'], nœuds=v['noeuds'], aide=v['aide'], exemple=(v['exemples'][0]['cible'] if v['exemples'] else '')) for v in AX], ['page', 'largeur', 'règle', 'impact', 'nœuds', 'aide', 'exemple'], num=('largeur', 'nœuds')))
w('<ul><li><b>landmark-one-main</b> et <b>region</b> : aucune page n’a de <code>&lt;main&gt;</code> ; le contenu n’est dans aucun repère, sauf la barre et le pied. Sur l’accueil, le pied est en plus dans la section Installation, jamais fermée (3 <code>&lt;section&gt;</code> ouvertes, 2 fermées).</li><li><b>color-contrast</b> : la source des citations de Claude, <code>#8a8576</code> sur blanc, 3,68:1.</li><li><b>link-in-text-block</b> : deux liens des Guides ne se distinguent du texte que par la couleur, à 2,05:1 et 1,11:1 du texte autour (3:1 demandé, WCAG <a href="https://www.w3.org/TR/WCAG21/#use-of-color">1.4.1</a>).</li><li><b>target-size</b> : un lien du sommaire des Fonctionnalités, partiellement couvert au moment du test par la barre collante.</li></ul>')

# Contrastes
w(f'<h2 id="contrastes">Contraste de chaque couple texte et fond</h2><p>{len(CT)} couples distincts sur les {fr(sum(int(r["occurrences"]) for r in CT))} textes rendus. Le site n’a pas de thème sombre (<code>color-scheme: light only</code>) : les rendus en <code>prefers-color-scheme: dark</code> sont identiques au pixel près aux rendus clairs, ces chiffres valent pour les deux. Fichier <a href="donnees/contrastes.csv">contrastes.csv</a>.</p>')
w(table([dict(texte=sw(r['texte']) + e(r['texte']), fond=sw(r['fond']) + e(r['fond']), WCAG=fr(r['wcag_min']), APCA=fr(r['apca_lc_min'], 1), textes=r['occurrences'], **{'sous WCAG': r['echecs_wcag'], 'sous APCA': r['echecs_apca']}, tailles=r['tailles'], exemples=e(r['exemples'][:160])) for r in CT],
          ['texte', 'fond', 'WCAG', 'APCA', 'textes', 'sous WCAG', 'sous APCA', 'tailles', 'exemples'], num=('WCAG', 'APCA', 'textes', 'sous WCAG', 'sous APCA'), raw=('texte', 'fond', 'exemples')))
w('<p>Contrastes hors texte (WCAG <a href="https://www.w3.org/TR/WCAG21/#non-text-contrast">1.4.11</a>, 3:1) : chevron des Guides <code>#93a0b4</code> sur blanc, <b>2,65:1</b> ; anneau des numéros d’étape <code>rgba(20,40,80,.14)</code>, 1,4:1 (décoratif, le chiffre porte le sens) ; contour des groupes, 1,3:1 (la masse blanche sur le fond fait la séparation : 1,13:1, et c’est voulu, sans filet).</p>')

# Cibles
w('<h2 id="cibles">Taille des cibles</h2><p>Fichier <a href="donnees/cibles.csv">cibles.csv</a>.</p>')
rows = []
for lw in ('375', '1440'):
    cc = [c for c in C if c['largeur'] == lw]
    rows.append({'largeur': lw, 'cibles': len(cc), 'sous 24 px sans espace (2.5.8)': sum(1 for c in cc if c['wcag_258'] == 'False' and c['dans_phrase'] != 'True'), 'liens dans une phrase (exemptés)': sum(1 for c in cc if c['dans_phrase'] == 'True'), 'sous 44 px (HIG)': sum(1 for c in cc if c['hig_44'] == 'False' and c['dans_phrase'] != 'True')})
w(table(rows, list(rows[0].keys()), num=tuple(list(rows[0].keys())[1:])))
small = sorted([c for c in C if c['largeur'] == '375' and c['dans_phrase'] != 'True' and float(c['min']) < 30], key=lambda c: float(c['min']))
seen = set(); sm = []
for c in small:
    k = (c['sel'].split(' > ')[-1], c['texte'])
    if k in seen: continue
    seen.add(k); sm.append(c)
w('<p>Les plus petites à 375 px, hors liens dans une phrase :</p>' + table([dict(page=c['page'], élément=c['sel'].split(' > ')[-1], texte=c['texte'], largeur=fr(float(c['l']), 1), hauteur=fr(float(c['h']), 1), voisine=c['dist_voisin']) for c in sm[:20]], ['page', 'élément', 'texte', 'largeur', 'hauteur', 'voisine'], num=('largeur', 'hauteur', 'voisine')))
w('<p>Les icônes du dock ne sont pas des cibles : ni lien, ni bouton, ni <code>tabindex</code>. Leur nom n’apparaît qu’au survol de la souris.</p>')

# Échelle des captures
w('<h2 id="echelles">Échelle des captures</h2><p>Largeur affichée × 2 ÷ largeur du fichier. 1 : le texte de l’app à sa taille réelle sur un écran Retina ; 0,5 : à moitié. Le texte de l’app fait 13 pt ; à ×0,63, il tombe à 8 px ; à ×0,27, à 3,5 px. Apple ne descend pas sous 10 pt sur macOS (<a href="https://developer.apple.com/design/human-interface-guidelines/typography#Specifications">HIG, Typography, Specifications</a>).</p>')
caps = [r for r in I if r['page'] in ('fonctionnalites', 'versions', 'guides') and 'gildas' not in r['src']]
w(table([dict(page=r['page'], image=r['src'].split('/')[-1], naturelle=r['nat_l'], **{'375': r['echelle_375'], '768': r['echelle_768'], '1440': r['echelle_1440']}, **{'texte de l’app à 1440 (px)': fr(13 * float(r['echelle_1440']), 1) if r['echelle_1440'] else ''}) for r in caps], ['page', 'image', 'naturelle', '375', '768', '1440', 'texte de l’app à 1440 (px)'], num=('naturelle', '375', '768', '1440', 'texte de l’app à 1440 (px)')))

# Poids
tot0 = sum(int(r['octets']) for r in PI); tot1 = sum(int(r['octets_a_la_taille_utile']) for r in PI)
w(f'<h2 id="poids">Poids des images de l’accueil</h2><p>Pour chaque image : le fichier servi, et le même redimensionné à deux fois sa plus grande taille affichée (le plus qu’un écran Retina puisse montrer), en WebP (qualité 92, ou sans perte pour les icônes). Total : <b>{fr(round(tot0 / 1024))} Ko → {fr(round(tot1 / 1024))} Ko</b>. Fichier <a href="donnees/poids-images-accueil.csv">poids-images-accueil.csv</a>.</p>')
w(table([dict(image=r['image'], naturelle=r['naturelle'], **{'affichée max': r['affichee_max_css'], 'utile (×2)': r['utile_2x'], 'Ko': fr(round(int(r['octets']) / 1024)), 'Ko à la taille utile': fr(round(int(r['octets_a_la_taille_utile']) / 1024))}) for r in PI],
          ['image', 'naturelle', 'affichée max', 'utile (×2)', 'Ko', 'Ko à la taille utile'], num=('naturelle', 'affichée max', 'utile (×2)', 'Ko', 'Ko à la taille utile')))

# Typo FR
w('<h2 id="typo-fr">Ponctuation française</h2><p>Comptes sur le texte visible ; règles de l’Imprimerie nationale (<i>Lexique des règles typographiques en usage à l’Imprimerie nationale</i>) : espace insécable avant le deux-points, espace fine insécable avant le point-virgule, le point d’exclamation et le point d’interrogation, insécables à l’intérieur des guillemets, apostrophe typographique.</p>')
keys = [k for k in TF[0] if k != 'page']
w(table([dict(cas=k, total=sum(int(p[k]) for p in TF)) for k in keys], ['cas', 'total'], num=('total',)))

ecrire('mesures.html', page('mesures.html', 'Mesures du site', 'Lighthouse, axe, contrastes WCAG 2 et APCA, cibles, échelles et poids des images du site de Callrecorder, avant et après.', '\n'.join(out)))

import sys, re; sys.path.insert(0, '/tmp/claude-0/outils')
from commun import *
V = lire('css-valeurs.csv'); M = lire('css-mort.csv')
mortes = {int(m['ligne']) for m in M if m['selecteur'] not in {'.nav.hidden', '.cmdline .copied', '.rec-state.problem', 'details.row[open] summary::after', '.req.warn', '.intro .req.warn', '.message.sent .rec-bar, .message.sent textarea, .message.sent .message-actions', '.author .message.sent .sent-status'}} | {39}
out = []; w = out.append
w('<h1>Système et migration</h1><p class="chapo">Une seule valeur par rôle, comme <code>DESIGN.md</code> le pose pour l’app. Les variables ci-dessous sont celles du prototype (<a href="prototypes/css/apres.css">prototypes/css/apres.css</a>). Puis, pour chaque déclaration de <code>style.css</code>, sa valeur actuelle et la nouvelle, ligne par ligne.</p>')
w('<p>Principe : ne rien inventer. Chaque variable reprend une valeur déjà présente sur le site ou dans l’app (les opacités <code>Hover.fill</code> et <code>Chip.fill</code>, l’échelle d’espacement 4 à 24, les rayons 6, 10, 12), sauf là où une mesure impose un changement (contrastes, P6). Les lignes mortes sont à supprimer, pas à migrer.</p>')

# Variables
TOK = [
 ('Couleur', '--window', '#edf2f8', 'fond de page', 'inchangé'), ('Couleur', '--group', '#ffffff', 'groupes, cartes, boutons', 'inchangé'),
 ('Couleur', '--text', '#142338', 'titres, texte fort', 'inchangé'), ('Couleur', '--body', '#2c3a50', 'texte courant', 'inchangé'),
 ('Couleur', '--secondary', '#515c70', 'texte secondaire', '#566175 → #515c70 : APCA Lc 73 → 75,1 sur le fond ; WCAG 5,55 → 5,99'),
 ('Couleur', '--accent', '#0064d2', 'liens, bouton principal, focus', 'inchangé (DESIGN.md le fixe)'), ('Couleur', '--border', 'rgba(20,40,80,.14)', 'contours', 'remplace .1, .12, .14, .15, .16 des contours'),
 ('Couleur', '--warn', '#b25000', 'Mac incompatible, problème d’envoi', 'remplace #8a5a00'), ('Couleur', '--help', '#f4f7fb', 'pied d’un groupe', 'nommé'),
 ('Couleur', '--tint-accent', '#e6f0fc', 'badge « Dernière »', 'remplace #e6eef9 (mort)'), ('Couleur', '--fill-hover', 'rgba(20,40,80,.05)', 'survol d’une ligne, d’un segment', 'remplace .04 et #dfe7f1'),
 ('Couleur', '--fill-chosen', 'rgba(20,40,80,.07)', 'fond du contrôle segmenté, ligne choisie', 'remplace rgba(30,60,120,.07), .06, #eaf0f7'),
 ('Couleur', '--edge-capture', 'rgba(20,40,80,.25)', 'liseré d’une capture rectangulaire', 'remplace .2 et .25'), ('Couleur', '--chevron', '#6f7c92', 'chevron des Guides', '#93a0b4 → #6f7c92 : 2,65 → 4,2:1'),
 ('Couleur', '--nav-bg', 'rgba(237,242,248,.88)', 'barre du haut', 'nommé'), ('Couleur', '--cmd-bg / --cmd-bg-hover / --cmd-text', '#1e1e1e / #2c2c2e / #e8e8e8', 'ligne de commande', 'nommés'),
 ('Couleur', '--claude-*', '#faf9f5, #29261b, #736e5c, #e6e2d6, #f0eee6, #dcdad3, #6b6759', 'fenêtre de Claude (illustration)', 'nommés ; source #8a8576 → #736e5c : 3,5 → 4,85:1'),
 ('Couleur', '--rec', '#e0352b', 'point de dictée', 'nommé'),
 ('Texte', '--t-legende', '13px', 'badges, touches, infobulles, « Copier »', 'remplace 12, 13, 14 (kbd)'), ('Texte', '--t-second', '15px', 'tout le secondaire', 'remplace 14 et 15'),
 ('Texte', '--t-texte', '17px (16 sous 640 px)', 'tout le texte courant', 'remplace 16 et 17'), ('Texte', '--t-chapo', 'clamp(19px, 2.2vw, 22px)', 'phrase sous un titre', 'remplace trois clamp voisins'),
 ('Texte', '--t-titre-carte', '24px (19 sous 640 px)', 'titre d’une carte', 'remplace 24 et 18'), ('Texte', 'h1, h2, titre de l’accueil', 'clamp existants', 'titres', 'inchangés'),
 ('Interligne', '--lh-texte / --lh-court / --lh-titre', '1.55 / 1.4 / 1.2', 'texte, lignes courtes et code, titres', 'remplace 1.45, 1.5, 1.6 ; 1.04 et 1.08 restent aux très grands titres'),
 ('Rayon', '--r-xs / --r-s / --r-m / --r-l / --r-pill', '6 / 10 / 12 / 20 / 999px', 'touche et code / bouton, ligne de commande / groupe / carte / capsule', 'remplace 4–7, 8–11, 16–22'),
 ('Ombre', '--shadow-1', '0 0 0 1px var(--border), 0 1px 1px rgba(20,40,80,.08)', 'bouton, contour posé', 'remplace 4 variantes'), ('Ombre', '--shadow-2', '0 0 0 1px var(--border), 0 10px 30px -18px rgba(20,40,80,.25)', 'carte', '—'),
 ('Ombre', '--shadow-3', '0 22px 50px -16px rgba(20,40,80,.28)', 'capture rectangulaire qui flotte', 'remplace .25 et .32'), ('Ombre', '--drop', 'drop-shadow(…14) drop-shadow(…22)', 'capture à contour', 'inchangé, nommé'),
 ('Focus', '--focus', '0 0 0 2px var(--window), 0 0 0 4px var(--accent)', 'tout élément au clavier', 'nouveau (P7)'),
 ('Espacement', 'échelle', '2, 4, 6, 8, 10, 12, 16, 20, 24, 28, 32, 40, 48, 56, 64, 80, 96, 120, 160', 'tout retrait, marge, écart', 'celle de l’app (4 à 24), prolongée'),
 ('Rupture', 'points', '452, 640, 1000, 1600 px', 'géométrie du micro / téléphone / sommaire et scène / sommaire dans la marge', 'remplace 480, 760, 980'),
]
w('<h2 id="variables">Les variables</h2>' + table([dict(zip(['famille', 'variable', 'valeur', 'rôle', 'origine'], t)) for t in TOK], ['famille', 'variable', 'valeur', 'rôle', 'origine']))
w('<p>Échelle typographique, rendue avec les vraies polices du site :</p><div class="carte" style="background:#edf2f8;color:#142338">'
  '<div style="font:500 60px/1.08 \'Host Grotesk\',-apple-system,sans-serif;letter-spacing:-.02em">Titre de page 60</div>'
  '<div style="font:500 38px/1.2 \'Host Grotesk\',-apple-system,sans-serif;letter-spacing:-.01em;margin-top:8px">Titre de partie 38</div>'
  '<div style="font:500 24px/1.25 \'Host Grotesk\',-apple-system,sans-serif;margin-top:8px">Titre de carte 24</div>'
  '<div style="font:22px/1.45 -apple-system,sans-serif;color:#2c3a50;margin-top:8px">Chapô 19 à 22 : Vos conversations mémorisées.</div>'
  '<div style="font:17px/1.55 -apple-system,sans-serif;color:#2c3a50;margin-top:8px">Texte 17 : la transcription se fait sur place, sans compte ni serveur.</div>'
  '<div style="font:15px/1.4 -apple-system,sans-serif;color:#515c70;margin-top:8px">Secondaire 15 : macOS 15 ou plus récent · Mac M1 ou plus récent</div>'
  '<div style="font:600 13px/1.3 -apple-system,sans-serif;color:#0064d2;margin-top:8px"><span style="background:#e6f0fc;padding:1px 7px;border-radius:6px">Légende 13 : Dernière</span></div></div>')

# Migration : tailles
TAILLE = {22: ('17px', 'inchangé, --t-texte'), 32: ('15px', '--t-second'), 98: ('15px', '--t-second'), 101: ('15px', '--t-second'), 121: ('15px', '--t-second'), 122: ('14px', 'exception gardée : trois segments sur 343 px'),
 144: ('.92em', 'illustration, garde'), 147: ('.9em', 'illustration, garde'), 136: ('clamp(…)', 'illustration, garde'), 188: ('12.5px', 'illustration, garde'), 185: ('var(--t-chapo)', '19–23 → 19–22'), 196: ('var(--t-chapo)', '18–20 → 19–22'), 459: ('var(--t-chapo)', '18–20 → 19–22'),
 43: ('clamp(18px, 2.2vw, 21px)', 'garde (bouton principal)'), 194: ('garde', 'h2'), 458: ('garde', 'h1 des pages'), 91: ('garde', 'h1 de l’accueil, lié au micro'),
 202: ('15px', '--t-second'), 209: ('—', 'règle morte'), 211: ('var(--t-texte)', '16 → 17'), 227: ('var(--t-second)', '14 → 15'), 234: ('var(--t-legende)', '13'), 241: ('var(--t-second)', '15'), 262: ('13px', 'code mono, garde'), 267: ('var(--t-legende)', '13'), 273: ('var(--t-legende)', '13'),
 285: ('var(--t-texte)', '16 → 17'), 288: ('var(--t-legende)', '12 → 13'), 290: ('var(--t-second)', '15'), 301: ('var(--t-texte)', '17'), 304: ('var(--t-legende)', '13'), 308: ('var(--t-legende)', '14 → 13'), 325: ('var(--t-second)', '15'), 334: ('var(--t-texte)', '16 → 17'), 335: ('var(--t-second)', '15'),
 345: ('var(--t-second)', '14 → 15'), 355: ('inherit', 'garde'), 369: ('var(--t-legende)', '13'), 373: ('var(--t-texte)', '16 → 17 (≥ 16 : pas de zoom sur iOS)'), 381: ('inherit', 'garde'), 384: ('var(--t-second)', '14 → 15'), 389: ('var(--t-texte)', '15 → 16 sous 640'),
 395: ('var(--t-texte)', '17'), 404: ('var(--t-texte)', '16 → 17'), 409: ('var(--t-second)', 'code 14 → 15'), 416: ('var(--t-second)', '14 → 15'), 420: ('var(--t-legende)', '12 → 13'), 443: ('16px', 'cartouche, garde'), 449: ('var(--t-second)', '15'), 465: ('var(--t-texte)', '17'), 474: ('var(--t-texte)', '17'),
 476: ('var(--t-second)', '15'), 493: ('var(--t-texte)', '17'), 494: ('22px', 'règle reprise par les masses de Confidentialité (P12)'), 502: ('var(--t-second)', '15'), 537: ('var(--t-titre-carte)', '24'), 538: ('var(--t-texte)', '16 → 17'), 563: ('var(--t-titre-carte)', '18 → 19 sous 640'), 564: ('var(--t-texte)', '14 → 16 sous 640')}
rows = []
for r in V:
    if r['categorie'] != 'taille' or r['fichier'] != 'style.css': continue
    l = int(r['ligne']); new, note = TAILLE.get(l, ('—', 'règle morte, à supprimer') if l in mortes else ('?', ''))
    if l in mortes and l not in (494,): new, note = '—', 'règle morte, à supprimer'
    rows.append({'lieu': f'style.css:{l}', 'sélecteur': r['selecteur'][:60], 'média': r['media'], 'actuel': r['valeur'][:40], 'nouveau': new, 'note': note})
w(f'<h2 id="m-tailles">Migration : tailles de police</h2><p>{len(rows)} déclarations.</p>' + table(rows, ['lieu', 'sélecteur', 'média', 'actuel', 'nouveau', 'note']))

# Migration : couleurs
def coul(v, sel, prop):
    s = sel
    if '.claude' in s: return {'#29261b': '--claude-ink', '#faf9f5': '--claude-paper', '#8a8576': '--claude-muted (#736e5c)', '#6b6759': '--claude-title', '#e6e2d6': '--claude-line', '#f0eee6': '--claude-bubble', '#dcdad3': '--claude-dot', '#ebe8de': 'supprimé avec le filet de la barre (option) ou --claude-line', '#fff': '--group'}.get(v, 'garde (ombre de la fenêtre)')
    m = re.match(r'rgba\(20,40,80,(\.\d+)\)', v)
    if m:
        a = float(m.group(1))
        if prop in ('box-shadow', 'filter'):
            if a in (.14, .15, .16, .1, .12) and 'inset' not in prop and ('0 0 0' in s or True): pass
            return '--shadow-1/2/3 ou --drop selon le rôle (voir Ombres)'
        if prop.startswith('border'): return '--edge-capture' if a >= .2 else '--border'
        if prop == 'background': return '--fill-hover' if a <= .05 else '--fill-chosen'
        return '--border'
    return {'#fff': '--group', '#ffffff': '--group', '#2a86f5': 'règle morte (.button.default)', '#0064d2': '--accent', 'rgba(0,60,180,.5)': 'règle morte', '#eaf0f7': '--fill-chosen', '#dfe7f1': '--fill-hover', '#f7f7f8': '--group + brightness(.97)', 'rgba(30,60,120,.07)': '--fill-chosen',
            '#1e1e1e': '--cmd-bg', '#2c2c2e': '--cmd-bg-hover', '#e8e8e8': '--cmd-text', 'rgba(44,44,46,0)': 'garde (fondu du « Copier », retiré par P3)', '#93a0b4': '--chevron (#6f7c92)', '#b25000': '--warn', '#8a5a00': '--warn', '#e0352b': '--rec', 'rgba(224,53,43,.22)': '--rec à 22 %',
            '#e6eef9': 'règle morte', '#e6f0fc': '--tint-accent', '#f4f7fb': '--help', 'rgba(237,242,248,.88)': '--nav-bg', 'rgba(240,240,240,.95)': '--group', 'rgba(255,255,255,.6)': 'color-mix(--group 60 %)', 'transparent': 'garde', 'currentcolor': 'garde'}.get(v, '?')
rows = []
for r in V:
    if r['categorie'] != 'couleur' or r['fichier'] != 'style.css': continue
    l = int(r['ligne'])
    new = 'règle morte, à supprimer' if l in mortes else coul(r['valeur'], r['selecteur'], r['propriete'])
    rows.append({'lieu': f'style.css:{l}', 'sélecteur': r['selecteur'][:50], 'propriété': r['propriete'], 'actuel': sw(r['valeur']) + e(r['valeur']), 'nouveau': e(new)})
w(f'<h2 id="m-couleurs">Migration : couleurs</h2><p>{len(rows)} emplois dans <code>style.css</code> (hors <code>:root</code>).</p>' + table(rows, ['lieu', 'sélecteur', 'propriété', 'actuel', 'nouveau'], raw=('actuel', 'nouveau')))

# Rayons
def ray(v):
    try: p = float(v.replace('px', ''))
    except: return 'garde (relatif : fenêtre de macOS ou cartouche)'
    if p == 0: return '0'
    if p in (999,): return '--r-pill'
    if 4 <= p <= 7: return '--r-xs (6)'
    if 8 <= p <= 11: return '--r-s (10)'
    if p == 12: return '--r-m (12)'
    if 16 <= p <= 22: return '--r-l (20)'
    return 'garde'
rows = [{'lieu': f"style.css:{r['ligne']}", 'sélecteur': r['selecteur'][:60], 'actuel': r['valeur'], 'nouveau': 'règle morte' if int(r['ligne']) in mortes else ray(r['valeur'])} for r in V if r['categorie'] == 'rayon' and r['fichier'] == 'style.css']
w(f'<h2 id="m-rayons">Migration : rayons</h2><p>{len(rows)} déclarations. Exception gardée : les segments du contrôle segmenté (8 px dans 10 px, rayon intérieur = rayon extérieur − retrait de 3 px, arrondi).</p>' + table(rows, ['lieu', 'sélecteur', 'actuel', 'nouveau']))

# Ombres
def omb(sel, v):
    if 'drop-shadow' in v and 'decoupe' in sel and 'extrait' not in sel and 'petite' not in sel: return '--drop'
    if 'claude' in sel: return 'garde (illustration)'
    if 'inset' in v or 'niveau' in v or '100vmax' in v: return 'garde'
    if '.button' in sel and 'hover' not in sel: return '--shadow-1'
    if 'benefits' in sel: return '--shadow-2'
    if 'stage' in sel or 'feature figure img' in sel or 'thumb' in sel: return '--shadow-3'
    if v.strip() == '0 0 0 1px var(--border)': return 'garde'
    return 'garde'
rows = [{'lieu': f"style.css:{r['ligne']}", 'sélecteur': r['selecteur'][:60], 'actuel': r['valeur'][:90], 'nouveau': 'règle morte' if int(r['ligne']) in mortes else omb(r['selecteur'], r['valeur'])} for r in V if r['categorie'] == 'ombre' and r['fichier'] == 'style.css' and r['valeur'] != 'none']
w(f'<h2 id="m-ombres">Migration : ombres</h2>' + table(rows, ['lieu', 'sélecteur', 'actuel', 'nouveau']))

# Espacements hors échelle
SCALE = [0, 2, 4, 6, 8, 10, 12, 16, 20, 24, 28, 32, 40, 48, 56, 64, 80, 96, 120, 160]
rows = []
for r in V:
    if r['categorie'] != 'espacement' or r['fichier'] != 'style.css' or not r['valeur'].endswith('px'): continue
    try: p = float(r['valeur'][:-2])
    except: continue
    if abs(p) in SCALE: continue
    n = min(SCALE, key=lambda s: (abs(s - abs(p)), s)); n = -n if p < 0 else n
    l = int(r['ligne'])
    rows.append({'lieu': f'style.css:{l}', 'sélecteur': r['selecteur'][:55], 'propriété': r['propriete'], 'actuel': r['valeur'], 'nouveau': 'règle morte' if l in mortes else (f'{n}px' if abs(p) > 2 else 'garde (réglage optique)')})
w(f'<h2 id="m-espacements">Migration : espacements hors échelle</h2><p>{len(rows)} valeurs ; chacune va à la marche la plus proche. Les décalages de 1 à 3 px qui calent une icône sur une ligne de base restent.</p>' + table(rows, ['lieu', 'sélecteur', 'propriété', 'actuel', 'nouveau']))

# Ruptures
rows = [{'lieu': f"style.css:{r['ligne']}", 'actuel': r['propriete'] + ' ' + r['valeur'], 'nouveau': {'480px': 'max-width 452px', '760px': 'max-width 640px', '980px': 'max-width 999px (même que le sommaire)'}.get(r['valeur'], 'garde')} for r in V if r['categorie'] == 'rupture']
w('<h2 id="m-ruptures">Migration : points de rupture</h2><p>Quatre : 452 (géométrie du micro, calculée), 640 (téléphone), 1000 (sommaire, scène en recouvrement), 1600 (sommaire dans la marge). Le passage de 760 à 640 touche la marge de la scène, le rythme des sections et la grille des versions entre 641 et 760 px ; à vérifier sur iPad mini en portrait (744 px).</p>' + table(rows, ['lieu', 'actuel', 'nouveau']))

# Fichier par fichier
w('<h2 id="fichiers">Fichier par fichier</h2>' + table([
 {'fichier': 'style.css', 'ce qui change': 'variables en tête ; 71 tailles, 96 couleurs, 55 rayons, 39 ombres migrées comme ci-dessus ; 49 règles mortes retirées ; règles des P3, P5, P7, P8, P10–P16, P18, P19', 'lignes touchées (estimation)': '≈ 230 sur 585'},
 {'fichier': 'index.html', 'ce qui change': '<main>, fermeture de la section Installation, trait d’union du titre, <wbr> de la commande, sources de Claude sans « · », carte iPhone, tabindex du dock, typographie', 'lignes touchées (estimation)': '≈ 40'},
 {'fichier': 'fonctionnalites/index.html', 'ce qui change': '<main>, quatre extraits recadrés et leurs largeurs, typographie, chemins', 'lignes touchées (estimation)': '≈ 30'},
 {'fichier': 'guides/index.html', 'ce qui change': '<main>, chemins (<b> → .chemin), typographie (117 apostrophes, 17 deux-points)', 'lignes touchées (estimation)': '≈ 60'},
 {'fichier': 'versions/index.html', 'ce qui change': '<main>, largeur de chaque vignette, dix extraits recadrés, typographie, chemins', 'lignes touchées (estimation)': '≈ 70'},
 {'fichier': 'confidentialite/index.html', 'ce qui change': '<main>, quatre masses titrées, chemins, typographie', 'lignes touchées (estimation)': '≈ 25'},
 {'fichier': 'img/', 'ce qui change': 'dix extraits de versions, quatre extraits de fonctionnalités, images de l’accueil à leur taille utile (−1,2 Mo), aperçu de partage des Versions', 'lignes touchées (estimation)': '≈ 30 fichiers'},
 {'fichier': 'DESIGN.md (callrecorder-app)', 'ce qui change': 'le tableau du site : variables, échelle, ruptures ; retirer « Des filets sur le site » des écarts connus', 'lignes touchées (estimation)': '≈ 30'},
 {'fichier': 'scripts/', 'ce qui change': 'un contrôle de typographie française et de contraste avant de fusionner, à côté de retours.py', 'lignes touchées (estimation)': 'nouveau'}], ['fichier', 'ce qui change', 'lignes touchées (estimation)']))
ecrire('systeme.html', page('systeme.html', 'Système et migration', 'Les variables du site de Callrecorder et, pour chaque déclaration de style.css, sa valeur actuelle et la nouvelle.', '\n'.join(out)))
